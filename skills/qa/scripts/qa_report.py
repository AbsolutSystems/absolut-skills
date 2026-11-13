#!/usr/bin/env python3
"""Render the evidence page of an as:qa run: one self-contained HTML file (stdlib only).

Usage: qa_report.py .qa/<run>/run.json [--out .qa/<run>/report.html]
Reads the run data written by as:qa (format: ../../qa-docs/references/qa-format.md#evidence-page) and writes a page
with every scenario, its steps, and the screenshot of every step and checkpoint embedded as a data URI, so the file
can be opened, moved or sent on its own. Screenshot paths are relative to the JSON file's directory. Prints JSON:
output path, result counts per checkpoint and viewport, missing screenshots. A malformed run is printed as
`ERROR …` lines with exit code 1 and nothing is written.
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
from html import escape
from pathlib import Path
from typing import Callable

RESULTS = ("FAIL", "BLOCKED", "OUTDATED", "PASS")  # worst first: a scenario takes its worst result
LABELS = {"FAIL": "FAILED", "BLOCKED": "BLOCKED", "OUTDATED": "OUTDATED", "PASS": "PASSED"}
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}

CSS = """
:root{--bg:#f6f7f9;--card:#fff;--text:#1c2330;--muted:#5d6878;--line:#dfe3ea;
--pass:#1a7f47;--pass-bg:#e6f5ec;--fail:#c62828;--fail-bg:#fdeaea;--outdated:#a15c00;--outdated-bg:#fdf1dc;
--blocked:#4f5b6e;--blocked-bg:#e9ecf1}
@media(prefers-color-scheme:dark){:root{--bg:#14171c;--card:#1d2129;--text:#e6e9ee;--muted:#9aa5b5;--line:#323946;
--pass:#5fd08f;--pass-bg:#16301f;--fail:#ff7b72;--fail-bg:#3b1a1a;--outdated:#f0b45a;--outdated-bg:#3a2a10;
--blocked:#aab4c3;--blocked-bg:#2a303b}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 system-ui,sans-serif;display:flex}
nav{position:sticky;top:0;align-self:flex-start;width:270px;flex:none;height:100vh;overflow:auto;padding:20px 14px;
border-right:1px solid var(--line);font-size:14px}
nav a{display:flex;gap:8px;align-items:baseline;padding:4px 6px;border-radius:6px;color:inherit;text-decoration:none}
nav a:hover{background:var(--line)}
nav h2{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:18px 6px 6px}
main{flex:1;min-width:0;max-width:1200px;padding:24px 32px 80px}
h1{margin:0 0 4px;font-size:26px}h2{margin:36px 0 12px;font-size:20px}h3{margin:0;font-size:17px}
.meta,.muted{color:var(--muted)}.meta{font-size:14px}
code{background:var(--line);padding:1px 5px;border-radius:4px;font-size:13px}
.badge{display:inline-block;padding:1px 9px;border-radius:999px;font-size:12px;font-weight:700;letter-spacing:.04em;
white-space:nowrap;color:var(--c);background:var(--b);border:1px solid var(--c)}
.dot{width:9px;height:9px;border-radius:50%;background:var(--c);flex:none}
.PASS{--c:var(--pass);--b:var(--pass-bg)}.FAIL{--c:var(--fail);--b:var(--fail-bg)}
.OUTDATED{--c:var(--outdated);--b:var(--outdated-bg)}.BLOCKED{--c:var(--blocked);--b:var(--blocked-bg)}
.counts{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}
.count{padding:10px 16px;border-radius:10px;background:var(--b);color:var(--c);border:1px solid var(--c);min-width:110px}
.count b{display:block;font-size:26px;line-height:1.1}
.verdict{font-size:18px;font-weight:700;color:var(--c)}
.box{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:12px 0}
.box ul{margin:6px 0;padding-left:20px}.attention{border-color:var(--fail)}
.scenario{background:var(--card);border:1px solid var(--line);border-left:6px solid var(--c);border-radius:10px;
padding:18px 20px;margin:18px 0;scroll-margin-top:12px}
.scenario>header{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.step{margin:18px 0 0;padding-top:14px;border-top:1px dashed var(--line)}
.step .n{display:inline-block;min-width:26px;height:26px;line-height:26px;text-align:center;border-radius:50%;
background:var(--line);font-weight:700;font-size:13px;margin-right:8px}
.step.notdone .n{background:var(--fail);color:#fff}
.observed{margin:4px 0 8px 34px;color:var(--muted)}
.check{margin:12px 0 0 34px;border:1px solid var(--line);border-left:5px solid var(--c);border-radius:8px;
padding:12px 14px;scroll-margin-top:12px}
.check.FAIL{background:var(--fail-bg);border-color:var(--fail)}
.banner{background:var(--fail);color:#fff;font-weight:800;letter-spacing:.08em;padding:4px 10px;border-radius:6px;
margin:-2px 0 10px;display:block}
.views{display:flex;gap:14px;flex-wrap:wrap;margin-top:10px}
.view{flex:1 1 320px;min-width:0;border-top:3px solid var(--c);padding-top:8px}
.shot{display:block;max-height:460px;overflow:hidden;border:1px solid var(--line);border-radius:6px;margin:8px 0;
cursor:zoom-in;background:var(--bg)}
.shot.zoom{max-height:none;cursor:zoom-out}.shot img{display:block;max-width:100%}
.step>.shot{margin-left:34px}
.missing{padding:18px;border:2px dashed var(--fail);border-radius:6px;color:var(--fail);margin:8px 0}
.log{font:12px/1.5 ui-monospace,monospace;color:var(--fail);margin:6px 0;padding-left:18px}
label.filter{display:block;margin:12px 6px;font-size:13px}
body:has(#problems:checked) .scenario.PASS,body:has(#problems:checked) nav a.PASS{display:none}
@media(max-width:900px){body{display:block}nav{position:static;width:auto;height:auto;border:0}main{padding:16px}}
@media print{nav{display:none}.shot{max-height:none}}
"""

JS = "document.addEventListener('click',e=>{const s=e.target.closest('.shot');if(s)s.classList.toggle('zoom')})"


def validate(run: dict) -> list[str]:
    errors = []
    for i, scenario in enumerate(run.get("scenarios", [])):
        sid = scenario.get("id") or f"scenarios[{i}]"
        if not scenario.get("id"):
            errors.append(f"scenarios[{i}]: missing id")
        for j, checkpoint in enumerate(scenario.get("checkpoints", [])):
            cid = checkpoint.get("id") or f"{sid}.checkpoints[{j}]"
            if not checkpoint.get("id"):
                errors.append(f"{cid}: missing id")
            if not checkpoint.get("results"):
                errors.append(f"{cid}: no results (a checkpoint that was not reached is BLOCKED with the reason)")
            for result in checkpoint.get("results", []):
                if result.get("result") not in RESULTS:
                    errors.append(f"{cid}: result {result.get('result')!r} is not one of {', '.join(RESULTS)}")
    if not run.get("scenarios") and not run.get("findings"):
        errors.append("run has no scenarios and no findings")
    return errors


def results(scenario: dict) -> list[str]:
    return [r["result"] for c in scenario.get("checkpoints", []) for r in c["results"]]


def status(scenario: dict) -> str:
    """Worst result of the scenario; a scenario with nothing judged is BLOCKED."""
    found = results(scenario)
    return next((r for r in RESULTS if r in found), "BLOCKED")


def counts(run: dict) -> dict[str, int]:
    found = [r for s in run.get("scenarios", []) for r in results(s)]
    return {r: found.count(r) for r in RESULTS}


def anchor(*parts: object) -> str:
    return "-".join(str(p) for p in parts if p).replace("/", "-").replace(" ", "-")


def badge(result: str) -> str:
    return f'<span class="badge {result}">{LABELS[result]}</span>'


def items(lines: list, cls: str = "") -> str:
    if not lines:
        return ""
    return f'<ul class="{cls}">' + "".join(f"<li>{escape(str(line))}</li>" for line in lines) + "</ul>"


def shot(path: str | None, image: Callable[[str], str | None], missing: list[str], alt: str) -> str:
    if not path:
        return ""
    uri = image(path)
    if uri is None:
        missing.append(path)
        return f'<div class="missing">Screenshot missing: {escape(path)}</div>'
    return f'<span class="shot" title="Click to expand"><img src="{uri}" alt="{escape(alt)}" loading="lazy"></span>'


def render_checkpoint(checkpoint: dict, image, missing: list[str]) -> str:
    found = [r["result"] for r in checkpoint["results"]]
    worst = next(r for r in RESULTS if r in found)
    views = []
    for r in checkpoint["results"]:
        viewport = r.get("viewport", "")
        views.append(
            f'<div class="view {r["result"]}" id="{anchor(checkpoint["id"], viewport)}">'
            f'{badge(r["result"])} <b>{escape(viewport)}</b>'
            f'<div>{escape(r.get("reason", ""))}</div>'
            f'{shot(r.get("screenshot"), image, missing, checkpoint["id"] + " " + viewport)}'
            f'{items(r.get("console", []), "log")}{items(r.get("requests", []), "log")}</div>'
        )
    banner = '<span class="banner">FAILED</span>' if worst == "FAIL" else ""
    return (
        f'<div class="check {worst}" id="{anchor(checkpoint["id"])}">{banner}'
        f'<b>Checkpoint {escape(checkpoint["id"])}</b> {badge(worst)}'
        f'<div><span class="muted">Expected:</span> {escape(checkpoint.get("expected", ""))}</div>'
        f'<div class="views">{"".join(views)}</div></div>'
    )


def render_scenario(scenario: dict, image, missing: list[str]) -> str:
    sid, state = scenario["id"], status(scenario)
    steps = scenario.get("steps", [])
    checkpoints = scenario.get("checkpoints", [])
    meta = " · ".join(
        f"{label}: {escape(str(scenario[key]))}"
        for key, label in (("role", "Role"), ("given", "Given"), ("criterion", "Criterion"))
        if scenario.get(key)
    )
    parts = [
        f'<section class="scenario {state}" id="{anchor(sid)}"><header><h3>{escape(sid)}'
        f' — {escape(scenario.get("name", ""))}</h3>{badge(state)}</header><div class="meta">{meta}</div>'
    ]
    for n, step in enumerate(steps, 1):
        not_done = step.get("not_done")
        parts.append(
            f'<div class="step{" notdone" if not_done else ""}"><span class="n">{n}</span>'
            f'<b>{escape(step.get("action", ""))}</b>{" " + badge("BLOCKED") if not_done else ""}'
            f'<div class="observed">{escape(step.get("observed", ""))}</div>'
            f'{shot(step.get("screenshot"), image, missing, f"{sid} step {n}")}'
        )
        parts += [render_checkpoint(c, image, missing) for c in checkpoints if c.get("after_step") == n]
        parts.append("</div>")
    rest = [c for c in checkpoints if c.get("after_step") not in range(1, len(steps) + 1)]
    parts += [render_checkpoint(c, image, missing) for c in rest]
    if scenario.get("not_executed"):
        parts.append(f'<div class="box"><b>Not executed</b>{items(scenario["not_executed"])}</div>')
    return "".join(parts) + "</section>"


def render_finding(finding: dict, image, missing: list[str]) -> str:
    fid = finding.get("id", "")
    shots = "".join(shot(p, image, missing, fid) for p in finding.get("screenshots", []))
    return (
        f'<section class="scenario FAIL" id="{anchor(fid)}"><header><h3>{escape(fid)} — '
        f'{escape(finding.get("title", ""))}</h3><span class="badge FAIL">{escape(finding.get("priority", "finding"))}'
        f"</span></header><b>Steps to reproduce</b>{items(finding.get('steps', []))}"
        f'<div><span class="muted">Expected:</span> {escape(finding.get("expected", ""))}</div>'
        f'<div><span class="muted">Actual:</span> {escape(finding.get("actual", ""))}</div>{shots}'
        f"{items(finding.get('console', []), 'log')}{items(finding.get('requests', []), 'log')}</section>"
    )


def render(run: dict, image: Callable[[str], str | None]) -> tuple[str, list[str]]:
    """The page and the screenshot paths `image` could not load. `image` maps a path to a data URI or None."""
    missing: list[str] = []
    scenarios, findings, total = run.get("scenarios", []), run.get("findings", []), counts(run)
    title = f"QA run: {run.get('title', '')}"
    problems = [
        f'<li><a href="#{anchor(c["id"], r.get("viewport", ""))}">{escape(c["id"])}</a> {escape(r.get("viewport", ""))} '
        f"{badge(r['result'])} {escape(r.get('reason', ''))}</li>"
        for s in scenarios
        for c in s.get("checkpoints", [])
        for r in c["results"]
        if r["result"] != "PASS"
    ]
    problems += [
        f'<li><a href="#{anchor(f.get("id", ""))}">{escape(f.get("id", ""))}</a> {escape(f.get("title", ""))}</li>'
        for f in findings
    ]
    rules = [
        f"{r.get('id', '')} — {r.get('checkpoint', '')} {r.get('viewport', '')}: {r.get('what', '')}"
        for r in run.get("rules", [])
    ]
    not_checked = list(run.get("skipped", []))
    not_checked += [f"{s['id']}: {line}" for s in scenarios for line in s.get("not_executed", [])]
    clean = not problems and not rules
    meta = " · ".join(
        f"{label}: {value}"
        for label, value in (
            ("Date", escape(run.get("date", ""))),
            ("URL", escape(run.get("url", ""))),
            ("Commit", f"<code>{escape(run.get('commit', ''))}</code>"),
            ("Host", escape(run.get("host", ""))),
            ("Judge", escape(run.get("judge", ""))),
            ("Report", escape(run.get("report", ""))),
        )
        if value not in ("", "<code></code>")
    )
    nav = "".join(
        f'<a class="{status(s)}" href="#{anchor(s["id"])}"><span class="dot {status(s)}"></span>'
        f"{escape(s['id'])} — {escape(s.get('name', ''))}</a>"
        for s in scenarios
    ) + "".join(
        f'<a href="#{anchor(f.get("id", ""))}"><span class="dot FAIL"></span>{escape(f.get("id", ""))} — '
        f"{escape(f.get('title', ''))}</a>"
        for f in findings
    )

    def box(heading: str, body: str, cls: str = "") -> str:
        return f'<div class="box {cls}"><b>{heading}</b>{body}</div>' if body else ""

    page = [
        f'<!doctype html><html lang="{escape(run.get("lang", "en"))}"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title>'
        f"<style>{CSS}</style></head><body>",
        '<nav><a href="#top"><b>Summary</b></a>'
        '<label class="filter"><input type="checkbox" id="problems"> Only scenarios with problems</label>'
        f"<h2>Scenarios</h2>{nav}</nav>",
        f'<main id="top"><h1>{escape(title)}</h1><div class="meta">{meta}</div>',
        f'<p class="verdict {"PASS" if clean else "FAIL"}">'
        f"{'Everything checked passed' if clean else 'Needs attention'}</p>",
        '<div class="counts">'
        + "".join(f'<div class="count {r}"><b>{total[r]}</b>{LABELS[r]}</div>' for r in RESULTS)
        + "</div>",
        box("Needs attention", f"<ul>{''.join(problems)}</ul>" if problems else "", "attention"),
        box("Broken app-wide rules", items(rules), "attention"),
        box("Not checked", items(not_checked)),
        box("Visual notes", items(run.get("notes", []))),
        box("Issues", items(run.get("issues", []))),
    ]
    if scenarios:
        page.append("<h2>Scenarios</h2>" + "".join(render_scenario(s, image, missing) for s in scenarios))
    if findings:
        page.append("<h2>Findings</h2>" + "".join(render_finding(f, image, missing) for f in findings))
    page.append(box("Tried without problems", items(run.get("tried", []))))
    page.append(f"</main><script>{JS}</script></body></html>\n")
    return "".join(page), missing


def data_uri(base: Path, path: str) -> str | None:
    """The image as a data URI; None when it is missing, not an image, or outside `base`."""
    file = (base / path).resolve()
    mime = MIME.get(file.suffix.lower())
    if mime is None or not file.is_relative_to(base.resolve()) or not file.is_file():
        return None
    # shortcut: embeds screenshots at full size (a run of 40 full-page PNGs is tens of MB);
    # downscale or link them when a page gets too heavy to open or send.
    return f"data:{mime};base64,{base64.b64encode(file.read_bytes()).decode('ascii')}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run", type=Path, help="run.json written by as:qa")
    parser.add_argument("--out", type=Path, help="output file (default: report.html next to the run file)")
    args = parser.parse_args()
    try:
        run = json.loads(args.run.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"ERROR {args.run}: {error}")
        return 1
    errors = validate(run) if isinstance(run, dict) else ["the run file must hold a JSON object"]
    if errors:
        print("\n".join(f"ERROR {e}" for e in errors))
        return 1
    page, missing = render(run, lambda path: data_uri(args.run.parent, path))
    out = args.out or args.run.with_name("report.html")
    out.write_text(page, encoding="utf-8")
    print(json.dumps({"output": str(out), "counts": counts(run), "missing_screenshots": missing}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
