---
name: estimate
description: "Analyse a client's feature request and estimate it in hours: reads the request, grounds it in the code, AGENTS.md and the docs/spec contracts, reviews the request for gaps, conflicts with current behaviour, better alternatives and worthwhile additions, breaks the work into implementation steps (no code) priced min / likely / max for a developer who knows the code and works with an AI coding agent, and writes an internal analysis plus a client document (PRD, estimate, assumptions, questions, suggestions) to docs/estimates/<slug>/; revises it after the client answers. Use only when the user explicitly invokes as:estimate."
disable-model-invocation: true
argument-hint: "<request text | path to file> [--lang en|pl] | docs/estimates/<slug>"
---

# Estimate

Be the user's analyst partner for a client's feature request: understand what the client really needs, check it
against the code, point out what is missing or would be better done differently, and price a step-by-step plan. The
client receives a document they can decide on; the team keeps the analysis that `as:tech-lead` later turns into a
change proposal. Do not write production code or a change proposal here.

Host-specific mechanics (subagents, asking questions): [Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).
File format: [references/estimate-format.md](references/estimate-format.md). Estimation rules:
[references/estimation.md](references/estimation.md). Subagent briefs: [references/briefs.md](references/briefs.md).

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `<request text | path to file>` — the client's request: pasted text, an e-mail, or a file (Markdown, text, PDF).
- `--lang en|pl` — language of `client.md` (default: the language of the request).
- `docs/estimates/<slug>` — revise an existing estimate with the client's answers (pasted or in a file) → step 8.

## Stance

- Code first: every statement about effort, risk or a gap points to code, a spec scenario or a request quote.
- Partner, not order-taker: say plainly when the request misses a case, contradicts current behaviour, or a smaller or
  different solution gives the client most of the value for less — once, with the reason and the price difference.
- Never guess silently: what is unknown becomes an assumption (`A1…`) or a client question (`Q1…`), and each one
  says how it moves the estimate.
- The client document is for a non-technical reader: no file paths, class names or code jargon.
- Converse in the user's language. `analysis.md` follows the spec language (`lang` in the marker on the first line of
  `docs/spec/index.md`), else English; its headings stay in English (see
  [references/estimate-format.md](references/estimate-format.md)).

## Procedure

### 1. Read the request

Read the request in full. List the client's requirements as `R1…Rn`: one line each, with a short quote or reference
to the source. Mark what is explicit and what you inferred. Pick the slug (short kebab-case title) and the client
language. Check `docs/estimates/` for an existing estimate of the same request — if found, offer a revision (step 8).

### 2. Ground

- Read the root, app and module `AGENTS.md` for the likely areas, the spec pages of the touched modules, open change
  proposals in `docs/spec/changes/` and open estimates (overlap, conflicts, work already planned).
- Fan out read-only subagents with brief "Impact" ([references/briefs.md](references/briefs.md)), one per independent
  area, in parallel. Small requests (one module) need no subagents.
- Summarise "what exists today" per requirement in a few lines with paths; note what already exists and needs no work.

### 3. Consistency review

Review the request as an analyst against the code and the spec — with brief "Consistency" for anything beyond one
module, inline otherwise. Each finding: type (`gap`, `conflict`, `alternative`, `addition`, `risk`), evidence, effect
on the estimate, and the client question or suggestion it becomes. Keep only findings that matter for this client
and this request; drop generic advice.

### 4. Clarify with the user

Ask the user (developer or PM, not the client) only what the code cannot tell and they may know: client context and
priorities, budget or deadline, known decisions, the hourly rate if the client document should show amounts, what
from step 3 to put to the client and what to drop. Everything still unknown becomes an assumption `A<n>` (with the
choice made and its effect on the hours) or a client question `Q<n>`.

### 5. Plan and estimate

Break the work into steps per functional block, following [references/estimation.md](references/estimation.md):

- each step: what it delivers (no code), modules or files, tests, `min / likely / max` hours, linked `R`/`A`/`Q`;
- a communication block (`Communication`, `Komunikacja`, … in the client language) for clarifications, demos and
  acceptance;
- `addition` and `alternative` findings priced as optional rows — never in the total;
- risks with their effect on `max`.

Write this as a draft `docs/estimates/<slug>/analysis.md` (`**Status:** draft`, today's date and the current commit in
the meta line; a new file, nothing is overwritten)
and compute the totals from the repository root with
`python3 <this skill's directory>/scripts/estimate_totals.py docs/estimates/<slug>` — never add hours by hand; copy
its blocks and total into `## Totals`. Without
`python3`, compute them as in [references/estimation.md](references/estimation.md#totals) and add every column twice.

### 6. Report and gate

Show in the conversation: the totals per block and overall (min–max, expected) from step 5, the top 3 risks, the
client questions, the suggestions with their prices, and what is out of the estimate. Ask before writing `client.md`;
adjust the draft on feedback and rerun the script. If the user drops the estimate, offer to delete the draft.

### 7. Write

Write `client.md` per [references/estimate-format.md](references/estimate-format.md) with the block totals and
expected values from the script's last run, then run the script with `--check`; it must end without `ERROR` lines.

Never overwrite an existing estimate without consent — a changed estimate is a revision (step 8).

### 8. Revision

With `docs/estimates/<slug>`: read both files and the client's answers. If `**Status:**` is not `draft`, the client
has seen `client.md` — keep it as `client-r<revision>.md` before changing anything. Then:

- turn answered questions into requirements or resolved assumptions;
- move suggestions the client accepted from `## Optional additions` into `## Estimate` (as steps of their block),
  drop the rejected ones, re-price the rest;
- re-estimate only the affected steps, re-checking their code;
- bump `**Revision:**`, set the meta line's date and commit to today and the current commit, add a line to
  `## History` (date, what changed, total before → after), rerun the script and update `## Totals`;
- then steps 6–7, and set `**Status:**` back to `draft` until the user says it was sent.

Set `**Status:**` to `sent`, `accepted` or `rejected` whenever the user says so.

### 9. Summary

One short block: the files written, what to send (`client.md`) and what stays internal (`analysis.md`), the open
questions count, and the next step — after the client answers, `as:estimate docs/estimates/<slug>`; after acceptance,
`as:tech-lead docs/estimates/<slug>` (it starts from the analysis, then `as:implement` and `as:finish`). State what
was not checked (e.g. areas not explored, an external API not inspected).
