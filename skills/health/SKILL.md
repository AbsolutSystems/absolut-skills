---
name: health
description: "Periodic health check of the whole project (or a subtree): hotspots (churn x complexity), structural and change coupling, test coverage and test quality (missing, excessive or weak tests), dead code, duplication, dependencies and docs drift. Uses tools the project already has, runs missing ones ephemerally with consent, falls back to git history and code reading. Writes a dated HTML report and metrics snapshot to docs/health/ with trends, then fixes the small items the user picks. Use only when the user explicitly invokes as:health."
disable-model-invocation: true
argument-hint: "[path] [--quick] [--since <period>] [--no-fix]"
---

# Health

Find where the project needs attention and turn it into a prioritised list: what to review, refactor, delete, test
more, test less, upgrade or re-document. `as:finish` looks at one branch; this skill looks at the whole codebase over
time.

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `[path]` — limit the run to this subtree (default: repository root).
- `--quick` — git signals and already configured tools only: no coverage run, no ephemeral tools, no test-quality review.
- `--since <period>` — git history window, in `git log --since` syntax (default `12 months`).
- `--no-fix` — stop after the report.

Host-specific mechanics (subagents, asking questions): [Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).

References: tools per ecosystem — [references/tools.md](references/tools.md); how to compute signals and prioritise —
[references/signals.md](references/signals.md); report and snapshot format — [references/report-format.md](references/report-format.md).

## Rules

- Read-only until step 6, except writing `docs/health/`. Tool output goes to a temporary directory. After every tool,
  `git status --porcelain` must show no changes outside `docs/health/`; if a tool left files, remove exactly those and
  report it.
- Never add dependencies, plugins or config to the project. Ephemeral tools (`npx`, `uvx`, `pipx run`, `docker run`)
  only with consent.
- Every finding needs evidence: a metric and file paths. No evidence, no finding.

## Procedure

### 1. Inventory

- Apps and modules: from `AGENTS.md` files, else the heuristics in
  [../agent-docs/references/analysis.md](../agent-docs/references/analysis.md) ("Classifying directories").
- Ecosystems and already configured tools: scripts in manifests, plugins in build files, config files, existing
  coverage reports and their age (see [references/tools.md](references/tools.md)).
- Previous snapshots: `docs/health/*.json` — the latest is the trend baseline.
- `docs/spec/` and `AGENTS.md` presence (for the docs signals).

### 2. Tool plan

Show one table: signal → tool → source (`configured` / `ephemeral` / `git+LLM`) → expected cost (fast / minutes /
runs the test suite). Ask which `ephemeral` tools may run (multi-select) and whether to run the test suite with
coverage when no fresh coverage report exists. With `--quick`, show the plan without asking and skip both.

### 3. Collect

Run independent parts in parallel; see [references/signals.md](references/signals.md) for each computation.

- **Git** (always, main thread): churn per file, hotspots, change coupling across modules, frequently fixed tests,
  ownership concentration.
- **Tools**: complexity, structural coupling and cycles, coverage, dead code, duplication, dependencies.
- **Docs**: the `as:agent-docs --check` and `as:spec-docs --check` analyses in report-only form (no questions, no
  writes), `as:spec-docs --tests` when `docs/spec/` exists, and open change proposals in `docs/spec/changes/` older
  than 30 days (a `docs` finding: implement, merge with `as:finish`, or drop).
- **Test quality** (not with `--quick`): one read-only subagent per module with the brief from
  [references/signals.md](references/signals.md), focused on hotspots — gaps (risky code without tests, untested error
  paths) and excess (tests without assertions, tests of internals, over-mocking, duplicates, slow or flaky tests).

If a tool fails, record it in the report and continue with the remaining signals.

### 4. Synthesize

- Per module: a scorecard of metrics, each with a trend against the baseline snapshot.
- Findings: `H-NNN` (numbered per run), category (`review | refactor | delete | add-tests | remove-tests | deps | docs`),
  severity (`high | medium | low`), effort (`S | M | L`), evidence, suggested action. Order as described in
  [references/signals.md](references/signals.md) ("Prioritising").
- Compare with the baseline findings: mark which earlier findings are resolved and which persist.

### 5. Report

- In chat: the top 10 findings, and one paragraph on the trend (what improved, what got worse).
- Write `docs/health/<YYYY-MM-DD>.html`, `docs/health/<YYYY-MM-DD>.json` and update `docs/health/index.html` as
  defined in [references/report-format.md](references/report-format.md). Same-day rerun overwrites that day's files.
- Styling: pages link `health.css`. Copy `assets/health.css` from this skill's directory to `docs/health/health.css`
  with a shell copy (do not read or retype it); if it exists and differs, ask before overwriting — compare the version
  in its first line. Older reports linking `../spec/spec.css` (written before 1.1.0) are relinked to `health.css`.

Check the written pages like spec pages: `grep -nE 'style=|<style|<script|<svg' docs/health/*.html` finds nothing, and
every relative link resolves.

With `--no-fix`, finish here with a short summary.

### 6. Act

Ask which findings to handle (multi-select; `S` effort preselected).

- **`S` findings** — fix one at a time: run the module's tests, make the change, rerun the tests, check it against
  [../finish/references/review.md](../finish/references/review.md). New tests follow the app's
  `.guidelines/testing-guideline.md`.
- **Removing tests** — only with explicit consent per test, with the reason shown, and never a test that is the only
  one covering a spec scenario or an error path.
- **`M` and `L` findings** — do not implement. Write a task brief for each (problem, evidence, proposed approach, risks,
  how to verify) for plan mode or `/feature-dev:feature-dev`.

Finish with a summary: findings fixed, briefs produced, files changed. Do not commit; suggest `as:finish` on the
changes, then committing.
