---
name: docs-check
description: "Audit the documentation against the code without changing it: the AGENTS.md/CLAUDE.md hierarchy and .guidelines/ (drift, lines the code already shows, missing facts), the Markdown spec in docs/spec/ (drift, missing scenarios, legacy HTML, known bugs parked as open questions), feature pages in docs/features/ (links, roadmap against proposals) and the recommended plugins. Reports per file with evidence and recommendations, asks the questions the code cannot answer, and offers to save problems to docs/issues/. Use only when the user explicitly invokes as:docs-check."
disable-model-invocation: true
argument-hint: "[path]"
---

# Docs check

Audit [agent-docs](../agent-docs/SKILL.md) and [spec-docs](../spec-docs/SKILL.md) output against the code, as
[init](../init/SKILL.md) would before writing — and stop at the reports. Read both `SKILL.md` files and follow their
steps named below, including the references they link. The only writes are issues in `docs/issues/` the user approves
(and, for bugs moved there, removing the open-question notes they replace). Answer in the user's language. Host
mechanics (subagents, asking questions): [Claude Code](../../references/claude-tools.md),
[Codex](../../references/codex-tools.md).

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `[path]` — limit the audit to this subtree (default: repository root).

## Procedure

1. **Inventory** — `agent-docs` step 1 and the extra `spec-docs` inventory items (existing pages, IDs, prefixes,
   legacy HTML) in one pass, as in `init` step 1. No `AGENTS.md` and no `docs/spec/` → say so and suggest `as:init`.
2. **Agent docs** — `agent-docs` steps 2–4: analysis, questions, and the report with its Recommendations.
3. **Spec** — when `docs/spec/` exists: `spec-docs` steps 2–4 for the pages under `[path]`: analysis, questions, and
   the report, including its issue candidates (bugs from the questions, and `> [!NOTE]` open questions that describe
   a confirmed bug).
4. **Features** — when `docs/features/` exists: run
   [spec_lint.py](../spec-docs/scripts/spec_lint.py) and report its `ERROR` lines for feature pages (broken links to
   scenarios, phases whose status does not match their proposal, sources not listed). Fix with
   `as:feature docs/features/<slug>`.
5. **Plugins** — on Claude Code, the status table of `init` step 6 (`INSTALLED` / `DISABLED` / `MISSING`), report
   only. On Codex, skip.
6. **Issues** — list the issue candidates from step 3, and offer one `docs` issue per file whose drift the user does
   not want to fix now. Ask which to save (multi-select), then write them per
   [../issue/references/issue-format.md](../issue/references/issue-format.md) and remove the notes of moved bugs.
7. **Summary** — files `OK` / `UPDATE` / `NEW` / `PRUNE` / `STALE` / `MIGRATE` per part, open questions, issues
   saved. Next: `as:agent-docs [path]` and `as:spec-docs [path]` apply the reports (they ask before writing), `as:feature` fixes feature pages,
   `as:fix` works through the issues. Do not commit.
