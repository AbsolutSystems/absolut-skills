#!/usr/bin/env python3
"""Repository checks for as:doctor (stdlib only): how this repository stands against the as plugin, as JSON.

Usage: doctor.py [--today YYYY-MM-DD]
Run inside the repository (checks its top level). Prints {"checks": [{area, status, detail, fix}]}; status is OK, WARN or INFO.
Exit 1 with an ERROR line when the directory is not a git repository.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path, PurePosixPath

SKILLS = Path(__file__).resolve().parents[2]
MARKER_RE = re.compile(r"<!-- as:working-principles (v(\d+)|off) -->")
VERSION_RE = re.compile(r"<!-- as:working-principles v(\d+) -->")
BLOCK_RE = re.compile(r"<!-- as:working-principles v\d+ -->.*?<!-- /as:working-principles -->", re.DOTALL)
CSS_RE = re.compile(r"css v(\d+)")
# an index entry starts at `.guidelines/`, not inside a longer path such as `backend/.guidelines/`
GUIDELINE_RE = re.compile(r"(?<![\w./-])\.guidelines/([\w./-]+\.md)")
MANIFESTS = ("pom.xml", "build.gradle", "build.gradle.kts", "package.json", "pyproject.toml", "go.mod", "Cargo.toml")
ISSUE_RE = re.compile(r"^p([1-4])-.+\.md$")
STALE_DAYS = {"proposal": 30, "health": 90}
TOOLS = {
    "gh": "as:review <PR> (reading and commenting on pull requests)",
    "uvx": "as:health (lizard and other ephemeral Python tools)",
    "npx": "as:finish (jscpd) and as:health (ephemeral Node tools)",
}


def check(area: str, status: str, detail: str, fix: str = "") -> dict:
    return {"area": area, "status": status, "detail": detail, "fix": fix}


def git(*args: str) -> str:
    return subprocess.run(["git", "-c", "core.quotePath=false", *args], check=True, capture_output=True,
                          text=True).stdout


def principles(root: Path) -> list[dict]:
    reference = (SKILLS / "init/references/working-principles.md").read_text(encoding="utf-8")
    current = int(VERSION_RE.search(reference).group(1))
    agents = root / "AGENTS.md"
    if not agents.is_file():
        return [check("working principles", "WARN", "no root AGENTS.md", "as:init")]
    text = agents.read_text(encoding="utf-8")
    marker = MARKER_RE.search(text)
    if marker is None:
        return [check("working principles", "WARN", "block not added", "as:init")]
    if marker.group(1) == "off":
        return [check("working principles", "INFO", "declined (off marker)")]
    version = int(marker.group(2))
    if version < current:
        return [check("working principles", "WARN", f"v{version}, current is v{current}", "as:init")]
    if version > current:
        return [check("working principles", "WARN", f"v{version}, newer than this plugin's v{current}",
                      "update the as plugin")]
    ours, theirs = BLOCK_RE.search(reference), BLOCK_RE.search(text)
    if theirs is None:
        return [check("working principles", "WARN", f"v{version} without the closing marker", "as:init")]
    if ours and ours.group(0).strip() != theirs.group(0).strip():
        return [check("working principles", "INFO", f"v{version}, customised")]
    return [check("working principles", "OK", f"v{version}")]


def agent_files(root: Path, files: list[str]) -> list[dict]:
    dirs = {str(PurePosixPath(f).parent) for f in files if PurePosixPath(f).name in ("AGENTS.md", "CLAUDE.md")}
    result = []
    for d in sorted(dirs):
        agents, claude = root / d / "AGENTS.md", root / d / "CLAUDE.md"
        where = "repository root" if d == "." else d
        if agents.is_symlink() or claude.is_symlink():
            result.append(check("agent docs", "WARN", f"{where}: AGENTS.md or CLAUDE.md is a symlink", "as:agent-docs"))
        elif not agents.is_file():
            result.append(check("agent docs", "WARN", f"{where}: CLAUDE.md without AGENTS.md", "as:agent-docs"))
        elif not claude.is_file():
            result.append(check("agent docs", "WARN", f"{where}: AGENTS.md without CLAUDE.md", "as:agent-docs"))
        elif claude.read_text(encoding="utf-8").strip() != "@AGENTS.md":
            result.append(check("agent docs", "WARN", f"{where}: CLAUDE.md is not exactly @AGENTS.md",
                                "as:agent-docs"))
    count = sum(1 for f in files if PurePosixPath(f).name == "AGENTS.md")
    if not result:
        result.append(check("agent docs", "OK" if count else "WARN", f"{count} AGENTS.md files",
                            "" if count else "as:init"))
    return result


def guidelines_index(root: Path, files: list[str]) -> list[dict]:
    result = []
    parts = [PurePosixPath(f).parts for f in files]
    owners = {str(PurePosixPath(*p[:p.index(".guidelines")]) if p.index(".guidelines") else ".")
              for p in parts if ".guidelines" in p[:-1]}
    owners |= {str(PurePosixPath(f).parent) for f in files if PurePosixPath(f).name == "AGENTS.md"}
    total = 0
    for d in sorted(owners):
        folder = root / d / ".guidelines"
        present = {p.relative_to(folder).as_posix() for p in folder.rglob("*.md")}
        agents = root / d / "AGENTS.md"
        listed = set(GUIDELINE_RE.findall(agents.read_text(encoding="utf-8"))) if agents.is_file() else set()
        total += len(present)
        where = "repository root" if d == "." else d
        for name in sorted(present - listed):
            result.append(check("guidelines", "WARN", f"{where}: .guidelines/{name} not listed in AGENTS.md",
                                "as:agent-docs"))
        for name in sorted(listed - present):
            result.append(check("guidelines", "WARN", f"{where}: AGENTS.md lists missing .guidelines/{name}",
                                "as:agent-docs"))
        if not present and any((root / d / m).is_file() for m in MANIFESTS):
            result.append(check("guidelines", "INFO", f"{where}: app without guidelines",
                                f"as:guidelines {'.' if d == '.' else d} testing"))
    if not result:
        result.append(check("guidelines", "OK", f"{total} guideline files") if total
                      else check("guidelines", "INFO", "no guideline files", "as:guidelines <app> testing"))
    return result


def assets(root: Path) -> list[dict]:
    result = []
    for skill, name in (("health", "health.css"), ("explain", "explain.css")):
        copy = root / "docs" / skill / name
        if not copy.is_file():
            continue
        ours = CSS_RE.search((SKILLS / skill / "assets" / name).read_text(encoding="utf-8").splitlines()[0])
        theirs = CSS_RE.search(copy.read_text(encoding="utf-8").splitlines()[0] if copy.stat().st_size else "")
        if ours and (theirs is None or int(theirs.group(1)) < int(ours.group(1))):
            found = f"v{theirs.group(1)}" if theirs else "no version"
            result.append(check("assets", "WARN", f"docs/{skill}/{name}: {found}, current is v{ours.group(1)}",
                                f"as:{skill} (asks before overwriting)"))
        else:
            result.append(check("assets", "OK", f"docs/{skill}/{name}"))
    return result


def last_commit_days(path: str, today: date) -> int | None:
    """Days since the last commit touching path; None when never committed (or no commits yet)."""
    try:
        stamp = git("log", "-1", "--format=%cs", "--", path).strip()
    except subprocess.CalledProcessError:
        return None
    return (today - date.fromisoformat(stamp)).days if stamp else None


def proposals(root: Path, today: date) -> list[dict]:
    result = []
    for page in sorted((root / "docs/spec/changes").glob("*.md")):
        days = last_commit_days(str(page.relative_to(root)), today)
        if days is not None and days > STALE_DAYS["proposal"]:
            result.append(check("change proposals", "WARN", f"{page.name}: untouched for {days} days",
                                "implement it, merge it with as:finish, or drop it"))
    return result


def issues(root: Path) -> list[dict]:
    counts, misnamed = {p: 0 for p in "1234"}, []
    for page in sorted((root / "docs/issues").glob("*.md")):
        if m := ISSUE_RE.match(page.name):
            counts[m.group(1)] += 1
        elif page.name.lower() not in ("readme.md", "index.md"):
            misnamed.append(page.name)
    result = []
    if sum(counts.values()):
        detail = ", ".join(f"p{p}: {n}" for p, n in counts.items() if n)
        result.append(check("issues", "WARN" if counts["1"] else "INFO", detail, "as:fix"))
    if misnamed:
        result.append(check("issues", "WARN", f"not named p<1-4>-<slug>.md: {', '.join(misnamed)}",
                            "rename per as:issue's issue format"))
    return result


def health(root: Path, today: date) -> list[dict]:
    dates = []
    for page in (root / "docs/health").glob("????-??-??.json"):
        try:
            dates.append(date.fromisoformat(page.stem))
        except ValueError:
            continue
    if not dates:
        return [check("health", "INFO", "never run", "as:health")]
    days = (today - max(dates)).days
    stale = days > STALE_DAYS["health"]
    return [check("health", "WARN" if stale else "OK", f"last run {days} days ago", "as:health" if stale else "")]


def tools() -> list[dict]:
    missing = [f"{name} — {use}" for name, use in TOOLS.items() if shutil.which(name) is None]
    if not missing:
        return [check("tools", "OK", ", ".join(TOOLS))]
    return [check("tools", "INFO", f"not found: {m}") for m in missing]


def doctor(root: Path, today: date) -> dict:
    files = git("ls-files", "-co", "--exclude-standard").splitlines()
    return {"checks": [
        *principles(root), *agent_files(root, files), *guidelines_index(root, files), *assets(root),
        *proposals(root, today), *issues(root), *health(root, today), *tools(),
    ]}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    args = parser.parse_args(argv)
    try:
        root = Path(git("rev-parse", "--show-toplevel").strip())
        os.chdir(root)  # git paths below are relative to the top level
        report = doctor(root, args.today)
    except subprocess.CalledProcessError as exc:
        print(f"ERROR {exc.stderr.strip() or exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
