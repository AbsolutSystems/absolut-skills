---
name: qa
description: "Check a running web application in a real browser the way a user does: executes the acceptance criteria of a feature page and the journeys in docs/qa/ (or the ones the branch's changes touch), one executor subagent per scenario in sequence collecting screenshots, console errors and failed requests at every checkpoint, then a separate judge subagent with fresh context decides PASS, FAIL, OUTDATED or BLOCKED from the evidence and the app-wide UI rules alone. An exploratory mode tries to break one area. Writes a run report to docs/qa/runs/ with the screenshots of failures, and offers failures as issues. Opens only local or listed test environments, never production. Requires docs/qa/ from as:qa-docs. Web applications only. Use only when the user explicitly invokes as:qa."
disable-model-invocation: true
argument-hint: "docs/features/<slug> | journeys | J<n> | branch [base] | explore <area>"
---

# QA

Confirm that the application works for a user: click through the scenarios in a browser, keep the evidence, and let
someone who did not click judge it. The executor never judges its own run. Reads `docs/qa/` and the feature pages;
writes only the run report, its screenshots, and — with consent — `.gitignore` and issues. Does not fix code.
Converse in the user's language. Format of `docs/qa/` and the report:
[../qa-docs/references/qa-format.md](../qa-docs/references/qa-format.md). Briefs:
[references/briefs.md](references/briefs.md). Host mechanics (subagents, asking questions, the browser tool):
[Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `docs/features/<slug>` — the feature's active acceptance criteria.
- `journeys` — every active journey; `J<n>` (several allowed) — those journeys.
- `branch [base]` — the criteria and journeys the branch's changes touch (base as in
  [finish](../finish/SKILL.md) step 1).
- `explore <area>` — an exploratory session of one area (screens or a flow, in the user's words).
- `--env <name>` — the environment from `docs/qa/index.md` (default: `local`).
- No target → ask which, suggesting `branch` on a feature branch and `journeys` otherwise.

## Procedure

### 1. Preflight

Stop at the first failure, with what to do:

- **QA docs** — `docs/qa/index.md` missing → stop, suggest `as:qa-docs`.
- **Driver** — one driver per kind of application:

  | Application | Driver |
  |-------------|--------|
  | Web (browser) | The browser tool from the host mapping |

  The app is not a web application → no driver, stop. The host has no browser tool → stop with the install step from
  the host mapping.
- **URL** — the environment's URL. `localhost`, `127.0.0.1` or a `local`/`staging` row of `index.md` → go on. Any
  other URL → ask before opening it, saying it is not a listed test environment. Never a production URL, even when
  asked: say so and stop.
- **Running** — open the URL. No answer → stop with the environment's `Start` from `index.md` (offer to run a local
  start command in the background, with consent).
- **Accounts** — the environment variables named for the roles the selected scenarios need are set; missing → ask
  for them or skip those scenarios as `BLOCKED`.
- **Working directory** — `.qa/` (and the browser tool's own output directory, if the host mapping names one) not in
  `.gitignore` → ask once to add them (no → delete them after the run, once the report has its screenshots).

### 2. Select

- **Feature** — read the page; every active `AC<n>` is a scenario, with the scenarios of its `**Realised by:**`
  links as details. Planned criteria (`planned — phase <n>`) are skipped and listed.
- **Journeys** — the active journeys of `journeys.md` (or the named `J<n>`).
- **Branch** — the changed files since base (as in [finish](../finish/SKILL.md) step 1); map them to modules (spec
  `Source` entries, `AGENTS.md`) and screens; select the criteria of features whose `**Modules:**` include a touched
  module or whose proposals are on the branch (`**Feature:**` meta line), and the journeys that cross those criteria
  or whose steps pass a touched screen. Nothing on the web front end changed and nothing selected → write a report that says so (result: nothing to
  check) and stop.
- **Explore** — the area; no selection.

Show the list (scenario, checkpoints, role, viewports) with the URL, and ask once to start. Then run without asking.

### 3. Execute

Run the scenarios **one after another** — one browser is shared state. For each, a fresh executor subagent with the
Executor brief from [references/briefs.md](references/briefs.md): the scenario, its checkpoints, the URL, role,
account variable names, data, viewports, the screenshot directory `.qa/<run>/` (`<run>` as the report's file name
without `.md`). Keep only its returned sections. Data the scenario needs and the seed cannot give (an order to
cancel) is prepared through the app itself by the executor, as a user would; when it cannot be, the scenario is
`BLOCKED`.

**Explore** — one explorer subagent with the Explorer brief instead; then open each finding's screenshots yourself
and drop findings the evidence does not show. Go to step 5.

Without subagents, execute each scenario yourself by the same brief, and keep only the sections it asks to return.

### 4. Judge

For each executed scenario, a fresh judge subagent with the Judge brief: expected outcomes, the feature criteria it
covers, the app-wide rules (`R<n>`), the intended changes on this path (open and recently archived proposals, feature
decisions, commit messages since the commit of the previous run report of this target, else since the branch's
base), and the executor's evidence — never its Steps
section. Judges may run in parallel: they do not use the browser.

Without subagents: after all scenarios ran, judge each from its evidence and screenshots in a separate pass, and mark
the report's judge `same agent`.

Before the report, open the screenshots of every `FAIL` yourself and confirm the judge's reason is visible; a reason
you cannot confirm becomes `BLOCKED` with a note.

### 5. Report

Write `docs/qa/runs/<YYYY-MM-DD>-<target>.md` per the format: header (target, URL, commit, host, judge), result
counts, one row per checkpoint and viewport, broken app-wide rules, visual notes from the judges (as a short list),
explorer findings. Move the screenshots of `FAIL` and `OUTDATED` checkpoints and of findings from `.qa/<run>/` to
`docs/qa/runs/<run>/` and link them; leave the rest in `.qa/`.

### 6. Issues and summary

- **FAIL** and explorer findings — offer to save each as a `bug` issue per
  [../issue/references/issue-format.md](../issue/references/issue-format.md) (multi-select, all `p1`–`p3`
  preselected): steps, expected, actual, the run report and the screenshot as evidence, `**Source:**` `as:qa`. One issue
  per cause — several checkpoints failing on the same request are one issue. Add the saved issue names to the report.
- **OUTDATED** — list them; suggest `as:qa-docs` to correct the journeys.
- **BLOCKED** — list them with the reason (missing data, account, unreachable step).

Summary: the result counts, failures with their issues, outdated and blocked checkpoints, the report path. Do not
commit. Next: `as:fix` for the saved issues, `as:qa-docs` for outdated journeys, and the same `as:qa` command after a
fix to confirm it.
