#!/usr/bin/env python3
"""Print the sheets of an .xlsx workbook as Markdown tables (stdlib only), for as:feature sources.

Usage: xlsx_text.py <file.xlsx> > <file>.md
One `## <sheet>` section per sheet, the first non-empty row as the table header, cached values of formulas.
shortcut: dates show as Excel serial numbers and merged cells as one value; upgrade if a project needs them.
Errors are printed as `ERROR …` lines and exit with code 1. Format: ../references/feature-format.md.
"""

from __future__ import annotations

import posixpath
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
PKG_REL = "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"


def column(ref: str) -> int:
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n - 1


def text_of(node: ET.Element) -> str:
    return "".join(t.text or "" for t in node.iter(f"{{{NS['m']}}}t"))


def cell_value(cell: ET.Element, shared: list[str]) -> str:
    kind = cell.get("t")
    if kind == "inlineStr":
        inline = cell.find("m:is", NS)
        return text_of(inline) if inline is not None else ""
    v = cell.find("m:v", NS)
    if v is None or v.text is None:
        return ""
    if kind == "s":
        return shared[int(v.text)]
    if kind == "b":
        return "TRUE" if v.text == "1" else "FALSE"
    return v.text


def sheets(path: str) -> list[tuple[str, list[list[str]]]]:
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        shared = []
        if "xl/sharedStrings.xml" in names:
            shared = [text_of(si) for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS)]
        rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).iter(PKG_REL)}
        result = []
        for sheet in ET.fromstring(z.read("xl/workbook.xml")).iter(f"{{{NS['m']}}}sheet"):
            target = rels[sheet.get(REL_NS)]
            target = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))
            rows = []
            for row in ET.fromstring(z.read(target)).iter(f"{{{NS['m']}}}row"):
                values: dict[int, str] = {}
                for i, cell in enumerate(row.findall("m:c", NS)):
                    values[column(cell.get("r")) if cell.get("r") else i] = cell_value(cell, shared)
                if any(v.strip() for v in values.values()):
                    rows.append([values.get(i, "") for i in range(max(values) + 1)])
            result.append((sheet.get("name"), rows))
        return result


def markdown(book: list[tuple[str, list[list[str]]]]) -> str:
    out = []
    for name, rows in book:
        out.append(f"## {name}\n")
        if not rows:
            out.append("(empty)\n")
            continue
        width = max(len(r) for r in rows)
        cells = [[" ".join(c.split()).replace("|", "\\|") for c in r + [""] * (width - len(r))] for r in rows]
        out.append("| " + " | ".join(cells[0]) + " |")
        out.append("|" + "---|" * width)
        out += ["| " + " | ".join(r) + " |" for r in cells[1:]]
        out.append("")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("ERROR usage: xlsx_text.py <file.xlsx>")
        return 1
    try:
        print(markdown(sheets(argv[0])), end="")
    except (OSError, KeyError, IndexError, ValueError, AttributeError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(f"ERROR {argv[0]}: not a readable .xlsx workbook ({exc})")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
