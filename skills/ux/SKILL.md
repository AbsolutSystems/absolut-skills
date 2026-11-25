---
name: ux
description: "Review how a running web application is to use, through a user's eyes: walks one area in a real browser as named personas with a goal each (one walker subagent per walk, a screenshot at every step, where it hesitated or got lost), then a separate reviewer subagent with fresh context turns the walks into findings with a nameable cost to the user — orientation, consistency between screens, missing feedback, dead ends, error recovery, wording, effort. Judges behaviour and flow, not visual design, and covers what no criterion describes. Writes a report with screenshots to docs/ux/, offers findings as ux issues and names the larger themes as material for as:roadmap. Opens only local or listed test environments, never production. Changes no code. Web applications only. Use only when the user explicitly invokes as:ux."
disable-model-invocation: true
argument-hint: "<area | URL> [--env <name>]"
---

# UX

Say what an area of the application is like to use for the people it is for: walk it in a browser as they would,
keep the evidence, and let someone who did not walk judge it. `as:qa` asks whether what is written works; this skill
asks whether it is easy to use, also where nothing is written. Writes only the report, its screenshots and — with
consent — `.gitignore` and issues. Does not fix code and does not edit feature pages, the spec or `docs/qa/`.
Converse in the user's language. Briefs: [references/briefs.md](references/briefs.md). Report:
[references/report-format.md](references/report-format.md). Host mechanics (subagents, asking questions, the browser
tool): [Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `<area>` — screens or a flow in the user's words ("checkout", "the admin's order list"), or a URL to start from.
- `--env <name>` — the environment from `docs/qa/index.md` (default: `local`).
- No target → ask which area, suggesting the ones with the most feature pages or the most recent changes.

## Procedure

### 1. Preflight

As [qa](../qa/SKILL.md) step 1 (driver, URL — never production —, running, accounts, working directory), with one
difference: `docs/qa/index.md` missing is not a stop. Then ask for the URL, the role and the names of the environment
variables that hold its login, and suggest `as:qa-docs` in the summary.

### 2. Frame the walks

- Read who the area is for: the `## Users and goals` and `## User flow` of the feature pages in the area
  (`docs/features/`), the users of a roadmap that covers it (`docs/roadmap/`), and the roles and app-wide rules
  (`R<n>`) of `docs/qa/index.md`. Read no application code — the review is of what a user sees.
- Propose 2–4 walks. A walk = a persona (role, and what they know: first visit or daily use), a goal in their own
  words ("I ordered the wrong size and want to fix it"), a start point and a viewport. Prefer goals that cross
  screens; include one first-visit persona, and one on a narrow viewport when the area is used on phones.
- Show the walks with the URL and ask once to start — with the stronger-model question for the reviewers in the same
  batch, where the host mapping offers one. Then run without asking.

### 3. Walk

Run the walks **one after another** — one browser is shared state. For each, a fresh walker subagent with the Walker
brief: persona, goal, start, URL, login variable names, viewport, the screenshot directory `.qa/<run>/` (`<run>` as
the report's file name without `.md`). The walker pursues the goal knowing only what the persona knows, and records
what it looked for, saw and did; it does not judge. Keep its returned sections.

Without subagents, walk each goal yourself by the same brief and keep only the sections it asks to return.

### 4. Review

For each walk, a fresh reviewer subagent with the Reviewer brief: the persona and goal, the walker's sections with
the screenshots, and what is written about the path (user flows, criteria, app-wide rules). Reviewers may run in
parallel: they do not use the browser. A finding needs a cost to this persona that can be named and a screenshot
that shows it; taste is not a finding.

Without subagents: after all walks, review each from its sections and screenshots in a separate pass, and mark the
report's reviewer `same agent`.

Then, yourself:

- open the screenshots of every finding and drop the ones the evidence does not show;
- merge the same finding from several walks into one and list the walks;
- sort each into **Mismatch** (the app contradicts a written criterion, user flow or app-wide rule — a defect, not an
  opinion), **Finding** (one screen or step) or **Theme** (the same pattern on several screens, or a flow whose shape
  is the problem — too large for one fix).

### 5. Report

Write `docs/ux/<YYYY-MM-DD>-<area>.md` per the [format](references/report-format.md): header, the walks with their
outcome and step count, mismatches, findings, themes, what works well, visual notes and what was not covered. Copy
the screenshots the report links from `.qa/<run>/` to `docs/ux/<run>/`; leave the rest in `.qa/`.

### 6. Issues and summary

- **Mismatches** and **Findings** — offer to save each as an issue per
  [../issue/references/issue-format.md](../issue/references/issue-format.md) (multi-select, `p1`–`p3` preselected):
  a mismatch as `bug`, a finding as `ux`; who is affected and what it costs them, the steps, the report and the
  screenshot as evidence, the suggested behaviour, `**Source:**` `as:ux`. One issue per cause. Add the saved issue
  names to the report.
- **Themes** — not issues: name each with the screens it spans and suggest `as:roadmap <theme>` (or
  `as:feature <theme>` when it is one capability), with the report as its first source.
- Never "fix" a mismatch by editing a criterion, a user flow or a rule to match the app.

Summary: the walks and whether each goal was reached, the counts of mismatches, findings and themes with the saved
issues, what was not covered, and the report path. Do not commit. Next: `as:fix` for the saved issues, `as:roadmap`
for a theme, and the same `as:ux` command after the fixes to compare.
