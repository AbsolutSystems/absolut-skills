#!/usr/bin/env python3
"""Sum the hours of an estimate written by as:estimate (stdlib only).

Usage: estimate_totals.py docs/estimates/<slug> [--check]
Reads the tables under `## Estimate` and `## Optional additions` in analysis.md (columns Step, Block, Min, Likely,
Max), prints JSON with min / likely / max and the expected value (PERT (min + 4·likely + max) / 6, rounded up to
0.5 h) per block and in total; options are summed per block and never added to the total. With --check, every block
row and a separate total row of client.md must show the numbers printed here in their hours cells ("3–9 h", "5,5 h"). Errors are printed as `ERROR …` lines and
exit with code 1. Format: ../references/estimate-format.md.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

SECTIONS = {"estimate": "blocks", "optional additions": "options"}
COLUMNS = ("min", "likely", "max")
NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)?")
HOURS_CELL_RE = re.compile(r"^[\d.,\s–-]+h$")  # "3–9 h", "5,5 h"


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def hours(cell: str) -> float:
    return float(cell.replace(",", "."))


def half_up(value: float) -> float:
    return math.ceil(round(value * 2, 6)) / 2


def fmt(item: dict) -> str:
    return f"{item['min']:g}–{item['max']:g} h, expected {item['expected']:g} h"


def rows(text: str) -> dict[str, list[dict[str, str]]]:
    """Table rows (column name → cell) under the known `##` headings."""
    result: dict[str, list[dict[str, str]]] = {key: [] for key in SECTIONS.values()}
    section, header = None, None
    for line in text.splitlines():
        if line.startswith("## "):
            section, header = SECTIONS.get(line[3:].strip().lower()), None
        elif not line.lstrip().startswith("|"):
            header = None
        elif section is None:
            continue
        elif header is None:
            header = [c.lower() for c in cells(line)]
        elif not all(set(c) <= set(":- ") for c in cells(line)):
            result[section].append(dict(zip(header, cells(line))))
    return result


def totals(text: str) -> tuple[dict, list[str]]:
    errors: list[str] = []
    result: dict = {}
    for key, table in rows(text).items():
        blocks: dict[str, dict] = {}
        for row in table:
            step = row.get("step", "?")
            try:
                values = [hours(row[c]) for c in COLUMNS]
            except (KeyError, ValueError):
                errors.append(f"step {step!r}: min, likely and max must be numbers")
                continue
            if values != sorted(values):
                errors.append(f"step {step!r}: expected min <= likely <= max")
            name = row.get("block") or "?"
            block = blocks.setdefault(name, {"block": name, "min": 0, "likely": 0, "max": 0, "expected": 0})
            for column, value in zip(COLUMNS, values):
                block[column] += value
            low, likely, high = values
            block["expected"] += (low + 4 * likely + high) / 6
        for block in blocks.values():
            block.update({c: round(block[c], 2) for c in COLUMNS}, expected=half_up(block["expected"]))
        result[key] = list(blocks.values())
    if not result["blocks"]:
        errors.append("no rows in the ## Estimate table")
    result["total"] = {k: round(sum(b[k] for b in result["blocks"]), 2) for k in (*COLUMNS, "expected")}
    return result, errors


def check(result: dict, client: str) -> list[str]:
    """Each block row and a separate total row of client.md must show its min, max and expected hours."""
    table = []
    for line in client.splitlines():
        if line.lstrip().startswith("|"):
            row = [c.strip("*").strip() for c in cells(line)]
            hour_cells = " ".join(c for c in row[1:] if HOURS_CELL_RE.match(c))
            table.append((row[0], {hours(n) for n in NUMBER_RE.findall(hour_cells)}))
    labels = {item["block"] for item in result["blocks"] + result["options"]}

    def shows(item: dict, numbers: set[float]) -> bool:
        return {item["min"], item["max"], item["expected"]} <= numbers

    errors = []
    for item in result["blocks"] + result["options"]:
        found = [numbers for label, numbers in table if label == item["block"]]
        if not found:
            errors.append(f"client.md: no table row for block {item['block']!r}")
        elif not any(shows(item, numbers) for numbers in found):
            errors.append(f"client.md: block {item['block']!r} should show {fmt(item)}")
    if not any(shows(result["total"], numbers) for label, numbers in table if label not in labels):
        errors.append(f"client.md: no total row showing {fmt(result['total'])}")
    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("folder", type=Path, help="docs/estimates/<slug>")
    parser.add_argument("--check", action="store_true", help="check the numbers shown in client.md")
    args = parser.parse_args(argv)
    analysis = args.folder / "analysis.md"
    if not analysis.is_file():
        print(f"{analysis}: not found", file=sys.stderr)
        return 1
    result, errors = totals(analysis.read_text(encoding="utf-8"))
    if args.check and not errors:
        client = args.folder / "client.md"
        errors = check(result, client.read_text(encoding="utf-8")) if client.is_file() else [f"{client}: not found"]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    for error in errors:
        print(f"ERROR {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
