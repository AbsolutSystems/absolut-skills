#!/usr/bin/env python3
"""Check a Markdown spec written by as:spec-docs (stdlib only); suitable for CI.

Usage: spec_lint.py [--spec docs/spec] [--against REF]
Checks: no legacy *.html pages; raw HTML only in the marker and anchors; anchor IDs well-formed and unique outside
changes/; one ID prefix per module page; relative links and #anchors resolve; IDs added by open proposals are not
used by the spec or by another open proposal, nor on REF (e.g. origin/HEAD) when --against is given.
Exit code 1 when anything is wrong. Format: ../references/markdown-format.md.
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
        for n, line in enumerate(prose(text).splitlines(), 1):
            rest = ANCHOR_RE.sub("", line)
            if RAW_HTML_RE.search(rest) and not (n == 1 and line.startswith("<!-- as:")):
                errors.append(f"{page}:{n}: raw HTML outside the marker and anchors")
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
        for target in LINK_RE.findall(prose(text)):
            if re.match(r"^[a-z]+:", target):
                continue
            rel_target, _, fragment = target.partition("#")
            dest = (page.parent / rel_target) if rel_target else page
            if not dest.exists():
                errors.append(f"{page}: broken link {target!r}")
            elif fragment and dest.suffix == ".md" and fragment not in anchors(dest.read_text(encoding="utf-8")):
                errors.append(f"{page}: broken anchor {target!r}")
    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--spec", default="docs/spec", type=Path)
    parser.add_argument("--against", help="git ref whose spec pages must not already use IDs added by open proposals")
    args = parser.parse_args(argv)
    if not args.spec.is_dir():
        print(f"{args.spec}: not a directory", file=sys.stderr)
        return 1
    try:
        errors = lint(args.spec, args.against)
    except RuntimeError as exc:
        print(f"git grep failed: {exc}", file=sys.stderr)
        return 1
    for error in errors:
        print(f"ERROR {error}")
    print(f"{len(errors)} error(s)" if errors else "OK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
