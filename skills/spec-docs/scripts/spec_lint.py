#!/usr/bin/env python3
"""Check a Markdown spec written by as:spec-docs (stdlib only); suitable for CI.

Usage: spec_lint.py [--spec docs/spec] [--features docs/features] [--against REF]
Checks: no legacy *.html pages; raw HTML only in the marker and anchors; anchor IDs well-formed and unique outside
changes/; one ID prefix per module page; relative links and #anchors resolve; IDs added by open proposals are not
used by the spec or by another open proposal, nor on REF (e.g. origin/HEAD) when --against is given.
Feature pages (when the features directory exists): raw HTML, links and anchors as above; anchors are AC<n>; a
phase heading ending in "🔄 in progress" links an open proposal in spec/changes/, one ending in "✅ done" links
spec/changes/archive/; every file in <feature>/sources/ (except dotfiles) is linked from the feature's index.md.
Exit code 1 when anything is wrong. Formats: ../references/markdown-format.md,
../../feature/references/feature-format.md.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ANCHOR_RE = re.compile(r'<a id="([^"]+)"></a>')
ID_RE = re.compile(r"^[A-Z]{2,4}-(R\d+|\d{3})$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FENCE_RE = re.compile(r"^(```|~~~).*?^\1[ \t]*$", re.MULTILINE | re.DOTALL)
CODE_SPAN_RE = re.compile(r"`[^`\n]*`")
RAW_HTML_RE = re.compile(r"<(?![a-zA-Z][\w+.-]*:)[a-zA-Z/!]")  # not autolinks <https://…>
ADDED_RE = re.compile(r"\*\*Change:\*\*[^\n]*\badded\b")
AC_RE = re.compile(r"^AC\d+$")
IN_PROGRESS_RE = re.compile(r"🔄\s*in progress$")
DONE_RE = re.compile(r"✅\s*done$")


def prose(text: str) -> str:
    """Text without fenced blocks and code spans (keeps line numbers)."""
    text = FENCE_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    return CODE_SPAN_RE.sub("", text)


def anchors(text: str) -> set[str]:
    found = set(ANCHOR_RE.findall(text))
    for line in prose(text).splitlines():
        m = HEADING_RE.match(line)
        if m:
            heading = ANCHOR_RE.sub("", m.group(2)).replace("`", "").strip().lower()
            found.add(re.sub(r"[^\w\- ]", "", heading).replace(" ", "-"))
    return found


def added_ids(text: str) -> list[str]:
    """IDs whose heading section (up to the next heading) says **Change:** … added."""
    result, current, body = [], None, []
    for line in prose(text).splitlines() + ["# end"]:
        if HEADING_RE.match(line):
            if current and ADDED_RE.search("\n".join(body)):
                result.append(current)
            ids = ANCHOR_RE.findall(line)
            current, body = (ids[0] if ids else None), []
        else:
            body.append(line)
    return result


def ids_on_ref(ref: str, spec: Path) -> set[str]:
    out = subprocess.run(
        ["git", "grep", "-hoE", r'<a id="[A-Z]{2,4}-(R[0-9]+|[0-9]{3})"></a>', ref, "--", str(spec),
         f":(exclude){spec / 'changes'}"],
        capture_output=True, text=True,
    )
    if out.returncode > 1:
        raise RuntimeError(out.stderr.strip())
    return set(ANCHOR_RE.findall(out.stdout))


def lint(spec: Path, against: str | None = None) -> list[str]:
    errors: list[str] = []
    errors += [f"{p}: legacy HTML page, migrate with as:spec-docs" for p in sorted(spec.rglob("*.html"))]
    pages = sorted(spec.rglob("*.md"))
    texts = {p: p.read_text(encoding="utf-8") for p in pages}
    owners: dict[str, list[Path]] = defaultdict(list)
    open_added: dict[str, list[Path]] = defaultdict(list)

    for page, text in texts.items():
        rel = page.relative_to(spec).parts
        in_changes = rel[0] == "changes"
        errors += html_errors(page, text)
        ids = ANCHOR_RE.findall(text)
        errors += [f"{page}: malformed ID {i!r} (expected PREFIX-NNN or PREFIX-R<n>)" for i in ids if not ID_RE.match(i)]
        if in_changes:
            if len(rel) == 2:
                for i in added_ids(text):
                    open_added[i].append(page)
            continue
        for i in ids:
            owners[i].append(page)
        prefixes = {i.split("-")[0] for i in ids if ID_RE.match(i)}
        if len(prefixes) > 1:
            errors.append(f"{page}: several ID prefixes {sorted(prefixes)} on one module page")

    errors += [f"duplicate ID {i!r} in {', '.join(map(str, ps))}" for i, ps in sorted(owners.items()) if len(ps) > 1]
    for i, ps in sorted(open_added.items()):
        if len(ps) > 1:
            errors.append(f"ID {i!r} added by several open proposals: {', '.join(map(str, ps))}")
        if i in owners:
            errors.append(f"{ps[0]}: added ID {i!r} already used in {owners[i][0]}")
    if against:
        taken = ids_on_ref(against, spec)
        errors += [f"{ps[0]}: added ID {i!r} already used on {against}" for i, ps in sorted(open_added.items())
                   if i in taken and i not in owners]

    for page, text in texts.items():
        errors += link_errors(page, text)
    return errors


def html_errors(page: Path, text: str) -> list[str]:
    errors = []
    for n, line in enumerate(prose(text).splitlines(), 1):
        rest = ANCHOR_RE.sub("", line)
        if RAW_HTML_RE.search(rest) and not (n == 1 and line.startswith("<!-- as:")):
            errors.append(f"{page}:{n}: raw HTML outside the marker and anchors")
    return errors


def local_links(page: Path, text: str) -> list[tuple[str, Path, str]]:
    """(target, destination path, fragment) of every relative link."""
    result = []
    for target in LINK_RE.findall(prose(text)):
        if re.match(r"^[a-z]+:", target):
            continue
        rel_target, _, fragment = target.partition("#")
        result.append((target, (page.parent / rel_target) if rel_target else page, fragment))
    return result


def link_errors(page: Path, text: str) -> list[str]:
    errors = []
    for target, dest, fragment in local_links(page, text):
        if not dest.exists():
            errors.append(f"{page}: broken link {target!r}")
        elif fragment and dest.suffix == ".md" and fragment not in anchors(dest.read_text(encoding="utf-8")):
            errors.append(f"{page}: broken anchor {target!r}")
    return errors


def roadmap_errors(page: Path, text: str) -> list[str]:
    """Phases (`###` headings ending in a status marker, any language): "🔄 in progress" links spec/changes/<slug>.md,
    "✅ done" links spec/changes/archive/."""
    errors, phase, targets = [], None, []

    def check_phase() -> None:
        if phase is None:
            return
        if IN_PROGRESS_RE.search(phase) and not any("changes/" in t and "/archive/" not in t for t in targets):
            errors.append(f"{page}: phase {phase!r} is in progress but links no open proposal in spec/changes/")
        elif DONE_RE.search(phase) and not any("changes/archive/" in t for t in targets):
            errors.append(f"{page}: phase {phase!r} is done but links no archived proposal in spec/changes/archive/")

    for line in prose(text).splitlines():
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) <= 3:
            check_phase()
            is_phase = len(m.group(1)) == 3 and (IN_PROGRESS_RE.search(m.group(2)) or DONE_RE.search(m.group(2)))
            phase, targets = (m.group(2) if is_phase else None), []
        elif phase is not None:
            targets += LINK_RE.findall(line)
    check_phase()
    return errors


def lint_features(features: Path) -> list[str]:
    errors: list[str] = []
    for page in sorted(features.rglob("*.md")):
        if "sources" in page.relative_to(features).parts:
            continue
        text = page.read_text(encoding="utf-8")
        errors += html_errors(page, text) + link_errors(page, text) + roadmap_errors(page, text)
        errors += [f"{page}: malformed anchor {i!r} (expected AC<n>)" for i in ANCHOR_RE.findall(text) if not AC_RE.match(i)]
    for sources in sorted(features.glob("*/sources")):
        index = sources.parent / "index.md"
        text = index.read_text(encoding="utf-8") if index.exists() else ""
        linked = {dest.resolve() for _, dest, _ in local_links(index, text)}
        errors += [f"{index}: source {f.name!r} is not listed under Sources" for f in sorted(sources.rglob("*"))
                   if f.is_file() and not f.name.startswith(".") and f.resolve() not in linked]
    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--spec", default="docs/spec", type=Path)
    parser.add_argument("--features", default="docs/features", type=Path,
                        help="feature pages from as:feature; checked when the directory exists")
    parser.add_argument("--against", help="git ref whose spec pages must not already use IDs added by open proposals")
    args = parser.parse_args(argv)
    if not args.spec.is_dir() and not args.features.is_dir():
        print(f"neither {args.spec} nor {args.features} is a directory", file=sys.stderr)
        return 1
    if args.against and not args.spec.is_dir():
        print(f"--against needs {args.spec}", file=sys.stderr)
        return 1
    try:
        errors = lint(args.spec, args.against) if args.spec.is_dir() else []
        if args.features.is_dir():
            errors += lint_features(args.features)
    except RuntimeError as exc:
        print(f"git grep failed: {exc}", file=sys.stderr)
        return 1
    for error in errors:
        print(f"ERROR {error}")
    print(f"{len(errors)} error(s)" if errors else "OK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
