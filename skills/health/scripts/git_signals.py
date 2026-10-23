#!/usr/bin/env python3
"""Git signals for as:health (stdlib only): churn, change coupling and frequently fixed tests, as JSON.

Usage: git_signals.py [--since "12 months"] [--path P] [--exclude GLOB ...] [--max-files 30]
Run inside the repository. Definitions: ../references/signals.md.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from collections import Counter
from itertools import combinations

SEP = "\x1e"
FIX_RE = re.compile(r"fix|flaky|flake|stabili[sz]e|retry", re.IGNORECASE)
TEST_RE = re.compile(r"(^|/)(tests?|__tests__|spec)/|(^|/)test_[^/]+$|[._-](test|spec)\.[^/]+$|Tests?\.[^/]+$")
DEFAULT_EXCLUDE = [
    "docs/*", "*/node_modules/*", "*/dist/*", "*/build/*", "*/target/*", "*/generated/*", "*/gen/*",
    "*.lock", "*lock.json", "*lock.yaml", "go.sum", "*.snap", "*/__snapshots__/*",
]


def commits(since: str, path: str) -> list[tuple[str, dict[str, int]]]:
    """(subject, lines changed per file) for each non-merge commit in the window."""
    out = subprocess.run(
        ["git", "-c", "core.quotepath=off", "log", f"--since={since}", "--no-merges", "--no-renames",
         f"--format={SEP}%s", "--numstat", "--", path],
        check=True, capture_output=True, text=True,
    ).stdout
    result = []
    for chunk in out.split(SEP)[1:]:
        subject, *rows = chunk.split("\n")
        lines: dict[str, int] = {}
        for row in rows:
            parts = row.split("\t")
            if len(parts) == 3:
                added, deleted, name = parts
                lines[name] = (int(added) if added.isdigit() else 0) + (int(deleted) if deleted.isdigit() else 0)
        result.append((subject, lines))
    return result


def signals(history, exclude: list[str], max_files: int, min_shared: int = 5, min_confidence: float = 0.5) -> dict:
    def kept(name: str) -> bool:
        return not any(fnmatch.fnmatch(name, g) or fnmatch.fnmatch("/" + name, g) for g in exclude)

    revisions: Counter[str] = Counter()
    lines: Counter[str] = Counter()
    pairs: Counter[tuple[str, str]] = Counter()
    fixed: Counter[str] = Counter()
    skipped = 0
    for subject, changed in history:
        files = sorted(f for f in changed if kept(f))
        revisions.update(files)
        lines.update({f: changed[f] for f in files})
        if FIX_RE.search(subject):
            fixed.update(f for f in files if TEST_RE.search(f))
        if len(files) > max_files:
            skipped += 1
            continue
        pairs.update(combinations(files, 2))

    coupling = []
    for (a, b), shared in pairs.items():
        confidence = shared / min(revisions[a], revisions[b])
        if shared >= min_shared and confidence >= min_confidence:
            coupling.append({"a": a, "b": b, "shared": shared, "confidence": round(confidence, 2)})
    coupling.sort(key=lambda p: (-p["shared"], -p["confidence"], p["a"], p["b"]))
    return {
        "commits": len(history),
        "skipped_large_commits": skipped,
        "churn": [{"file": f, "commits": n, "lines": lines[f]} for f, n in sorted(revisions.items(), key=lambda i: (-i[1], i[0]))],
        "coupling": coupling,
        "frequently_fixed_tests": [{"file": f, "fix_commits": n} for f, n in fixed.most_common() if n >= 2],
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--since", default="12 months")
    parser.add_argument("--path", default=".")
    parser.add_argument("--exclude", action="append", default=[], help="extra glob to exclude (repeatable)")
    parser.add_argument("--max-files", type=int, default=30, help="commits touching more files skip coupling")
    args = parser.parse_args(argv)
    try:
        history = commits(args.since, args.path)
    except subprocess.CalledProcessError as exc:
        print(exc.stderr.strip() or exc, file=sys.stderr)
        return 1
    json.dump(signals(history, DEFAULT_EXCLUDE + args.exclude, args.max_files), sys.stdout, separators=(",", ":"))
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
