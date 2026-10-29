---
name: qa-docs
description: "Create and maintain docs/qa/, what as:qa checks in a browser for a web application: environments and how to start them, test accounts (environment variable names, never secrets) and data, roles, app-wide UI rules (viewports, empty, error and loading states), and journeys — cross-feature user paths J1…Jn written as intent with observable checkpoints. Drafts it from the routes, roles and UI conventions in the code, the feature pages' acceptance criteria and AGENTS.md; on later runs reports drift (criteria and screens no journey covers, journeys naming removed screens or roles), the last result of every criterion and journey from the run reports, outdated journeys and criteria too vague to check, and writes only the suggestions the user accepts. Web applications only. Use only when the user explicitly invokes as:qa-docs."
disable-model-invocation: true
argument-hint: "[area | path]"
---

# QA docs

Keep `docs/qa/` true to the application, so `as:qa` knows where the app runs, who logs in, which rules hold on every
screen and which paths across features must work. Acceptance criteria stay on the feature pages; this skill never
copies or edits them. Writes only `docs/qa/index.md` and `docs/qa/journeys.md`, after approval, and — with consent — issues. Converse in the user's
language. Format: [references/qa-format.md](references/qa-format.md). Host mechanics (subagents, asking questions,
the browser tool): [Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `[area | path]` — limit the analysis and the suggestions to one area of the app (a feature slug, a route prefix
  such as `/admin`, a source directory). Default: the whole app.

## Procedure

### 1. Driver

Find the web front end: a framework entry (`package.json` with a web framework, server-rendered templates, an
`index.html`), its routes and its start command. None → say that `as:qa` has a driver only for web applications and
stop. Several front ends (a shop and an admin panel) → one `docs/qa/` covering all, with an environment row each.

### 2. Analysis

Read `docs/qa/` if it exists, `docs/features/index.md` and the feature pages (acceptance criteria, `**Realised by:**`),
the latest run reports in `docs/qa/runs/` (the newest per target), and the root and app `AGENTS.md` (start, seed,
test commands). Then fan out one read-only subagent per front end with the brief in
[references/analysis.md](references/analysis.md); without subagents, run it in the main thread.

Optional, when the app answers on a local URL and the host has a browser tool: open the main screens once to confirm
the routes found in the code, without logging in or submitting anything. Say in one line if it was skipped.

### 3. Draft or drift

**No `docs/qa/`** — draft `index.md` and `journeys.md` from the analysis per the format:

- environments from the start commands and configuration (`local` always; `staging` only when the repository names
  one); accounts as environment variable names; roles and app-wide rules from what the code enforces;
- journeys for the paths that cross features or screens: sign-up and first use, the main business flow end to end, a
  role boundary (a user who must not reach a screen), and the flows the analysis marks critical. Keep the list short —
  the feature criteria are executed on their own.

Ask in one batch only what the code cannot tell: which accounts and data exist and how to reset them, which flows are
critical for the business, and whether a staging URL may be used.

**`docs/qa/` exists** — compare it with the analysis and list suggestions, each with its reason and evidence:

- **Missing** — screens, roles or feature criteria that no journey and no feature page covers; a new front end or
  environment; a new app-wide rule the code now enforces (a new breakpoint, an error boundary).
- **Drift** — journeys, checkpoints or rules that name screens, controls, roles or routes the code no longer has; a
  start command or seed that changed.
- **Outdated** — checkpoints a run marked `OUTDATED`: propose the corrected step or checkpoint. When the correction
  would contradict a feature's acceptance criterion, the app is wrong, not the journey: offer a `bug` issue instead.
- **Vague** — a criterion with no outcome visible in the browser, or a checkpoint a screenshot cannot decide ("works
  correctly"): propose a sharper checkpoint, or a journey for the criterion. A criterion itself is changed only with
  `as:feature` — say so; never edit the feature page.
- **Removed** — journeys whose path no longer exists: mark them removed per the format, never delete or renumber.

### 4. Coverage

From the run reports: a table of every active criterion (`<slug>/AC<n>`) and journey with its last result (`PASS`,
`FAIL`, `OUTDATED`, `BLOCKED`, or `never run`), the report it comes from and its date. Criteria and journeys never run,
or whose last run is older than the latest change to the code they cross, are listed first.

### 5. Approval and write

Show the draft (new) or the suggestions grouped as in step 3 (existing), and ask which to apply (multi-select, all
preselected). Write only those. New journeys and rules take the next free `J<n>` / `R<n>`; existing IDs never change.
Update `**Updated:**` in `index.md`. Problems in the app found on the way (a route that crashes, a role check missing)
→ offer to save them as issues per [../issue/references/issue-format.md](../issue/references/issue-format.md),
`**Source:**` `as:qa-docs`.

### 6. Verify and summary

Check that every relative link in `index.md` and `journeys.md` resolves (including `#AC<n>` anchors on feature pages)
and that no `J<n>`, `J<n>-<m>` or `R<n>` is used twice. Summary: files written, journeys and rules added, changed and
removed, the coverage gaps that remain, issues saved. Next: `as:qa journeys` (or `as:qa docs/features/<slug>`), with
the app running.
