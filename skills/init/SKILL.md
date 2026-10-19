---
name: init
description: "Onboard a repository (greenfield or brownfield) in one run: build or update the AGENTS.md hierarchy with as:agent-docs, then the HTML module specification with as:spec-docs for a chosen scope, then link the spec from AGENTS.md, and finally check (and, with consent, install) the recommended Anthropic plugins. Shares one inventory and one round of questions between both, with an approval gate before each write. Use only when the user explicitly invokes as:init."
disable-model-invocation: true
argument-hint: "[path] [--spec <path>... | --spec all | --no-spec] [--check] [--no-principles] [--no-plugins] [--lang en|pl] [--depth N]"
---

# Init

Run [agent-docs](../agent-docs/SKILL.md) and [spec-docs](../spec-docs/SKILL.md) in the right order as one session.
This skill owns only the order, the shared steps and the approval gates. Everything else — file formats, templates,
subagent briefs, report tables, write and verify rules — comes from those two skills: read both `SKILL.md` files
before starting and follow them, including the references they link.

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `[path]` — limit the run to this subtree (default: repository root).
- `--spec <path>...` — directories (modules or apps) to specify. `--spec all` — every module. `--no-spec` — agent docs only.
  Without any of them, ask after the inventory (step 1).
- `--check` — audit both without writing: run each skill's procedure up to its report and stop; plugins are only reported.
- `--no-principles` — skip the working principles block (step 2).
- `--no-plugins` — skip the recommended plugins check (step 6).
- `--lang en|pl` — language of the spec pages (agent docs are always English). `--depth N` — as in `agent-docs`.

Host-specific mechanics (subagents, asking questions): [Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).

## Why this order

`agent-docs` is cheaper and settles the structure (apps, modules, boundaries, public API, legacy areas). `spec-docs`
then reuses the module reports and `AGENTS.md` instead of rediscovering them, and asks only about behaviour. The links
from `AGENTS.md` to the spec are added last, when the spec pages exist.

## Procedure

### 1. Shared inventory

Do `agent-docs` step 1 (Inventory) and the extra `spec-docs` inventory items (existing `docs/spec/` pages, IDs, ID
prefixes) in one pass. Show one plan: the `AGENTS.md` tree, and the candidate spec pages.

If the spec scope was not given, ask now. Options:

- **Selected modules (recommended for brownfield)** — propose 2–3 central modules: most depended on by other modules,
  most public entry points, or core domain by name. Specifying a large legacy codebase at once costs a lot and raises
  many "rule or bug?" questions.
- **All modules.**
- **No spec** — agent docs only.

### 2. Agent docs

Run `agent-docs` steps 2–4 (Analysis, Clarify, Report). When clarifying, also settle the **working principles** block from
[references/working-principles.md](references/working-principles.md) (skip with `--no-principles`):

- No block and no `off` marker in the root `AGENTS.md`: show the block, mention any existing rules in root
  `AGENTS.md`/`CLAUDE.md` that contradict it, and ask: add / do not add.
- Block with an older version: show what changes and ask whether to update.
- Same version, customised text, or `off` marker: leave it, do not ask.

Keep answers that also matter for the spec
(actors, domain terms, legacy or deprecated parts, intended vs accidental behaviour) to reuse in step 3.

**Gate 1:** ask for approval of the agent docs report. Then run `agent-docs` steps 5–6 (Write, Verify) — without the
"Specification" sections yet — and insert, update or mark `off` the working principles block at the end of the root
`AGENTS.md` exactly as defined in its reference file (create the root `AGENTS.md`/`CLAUDE.md` first if needed). With `--check`, show the report and continue to step 3 without writing.

### 3. Spec

Skip with `--no-spec`. Run `spec-docs` steps 2–4 for the chosen scope only (plus the app and system pages that list
those modules). Feed each module subagent the module report from step 2 and the module's `AGENTS.md`. When
clarifying, do not repeat questions already answered in step 2.

**Gate 2:** ask for approval of the spec report. Then run `spec-docs` steps 5–6 (Write, Verify). With `--check`, show
the report and go to step 6.

### 4. Link

For every spec page that now exists, add the "Specification" section to the matching repo, app and module `AGENTS.md`
as defined in the `agent-docs` templates — minimal edits only. Verify every linked path exists.

### 5. Summary

One short summary for both parts: files created / updated / left as is, scenarios added, open questions left. Then
next steps:

- `as:spec-docs <path>` — extend the spec to further modules, then `as:agent-docs` to link them.
- `as:spec-docs --tests` — scenario test coverage report for the specified modules.
- Review `git diff` and open `docs/spec/index.html` in a browser.
- `as:tech-lead` — starts on its own when you discuss a feature or a bug: design, decision, spec change, plan.
- `as:finish` — after each feature: simplify, review, spec and contract tests, docs for what changed.
- `as:health` — once a sprint or month: hotspots, coupling, tests, dead code, dependencies.
- `as:help` — how to work day to day with these commands, the recommended plugins and plan mode.

### 6. Recommended plugins

Skip with `--no-plugins`. On Codex, say these are Claude Code plugins and skip.

Check the plugins listed in [references/recommended-plugins.md](../../references/recommended-plugins.md) as described
there, and show one table: plugin, status (`INSTALLED` / `DISABLED` / `MISSING`), what it is for. With `--check`, stop
here.

If any is missing or disabled, ask which to install or enable (multi-select, all preselected). Run the install/enable
commands from that file one by one for the chosen plugins only, report each result, and remind the user to restart the
Claude Code session to load them. Never install without consent.

Re-running `as:init` is safe: both skills update existing files with minimal edits and report unchanged files as `OK`.
