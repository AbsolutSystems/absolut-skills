---
name: spec-tests
description: "Report which contract scenarios of the Markdown spec in docs/spec/ are verified by tests: maps every scenario ID to the tests that check it through the module's public entry points (COVERED / PARTIAL / MISSING), with unhappy paths counted separately, and offers to save the important gaps to docs/issues/. Read-only otherwise; does not write tests. Use only when the user explicitly invokes as:spec-tests."
disable-model-invocation: true
argument-hint: "[path]"
---

# Spec tests

Answer one question: does each promise in the contract have a test that checks it through the module's public entry
points? Requires an existing `docs/spec/` (from `as:spec-docs`). Read-only, except saving issues with consent. Answer
in the user's language. Host mechanics (subagents, asking questions): [Claude Code](../../references/claude-tools.md),
[Codex](../../references/codex-tools.md).

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `[path]` — only the modules under this subtree (default: all spec pages).

## Procedure

1. Collect all active scenarios (status not `removed`) with their ID, module, kind and Given/When/Then text. Legacy
   HTML pages are read as they are; suggest migrating them with `as:spec-docs`. No `docs/spec/` → stop and suggest
   `as:spec-docs`.
2. **Cheap pass:** search test sources for each scenario ID (`git grep -n '<ID>'` over test directories) — in test names,
   tags/annotations or comments. A hit is a candidate match.
3. **Semantic pass:** for scenarios without a hit, fan out one read-only subagent per module with the coverage brief
   from [../spec-docs/references/analysis.md](../spec-docs/references/analysis.md). It reads the module's tests and
   classifies each scenario. Tests that only exercise internal classes do not count as contract coverage, but are
   mentioned as `PARTIAL` evidence.
4. Report per module, one row per scenario:

| ID | Kind | Status | Evidence |
|----|------|--------|----------|
| `ORD-003` | error | `COVERED` / `PARTIAL` / `MISSING` | test file path and test name, or what is missing |

5. Then a summary per module and in total: covered / partial / missing, with a separate count for `error` and `edge`
   scenarios (unhappy paths are usually the gap). End with recommendations: which missing scenarios matter most, and —
   if the cheap pass found few IDs — tagging contract tests with scenario IDs so future runs map them deterministically.
6. **Issues** — offer to save the gaps that matter (one `add-tests` issue per module or per group of related
   scenarios, listing the scenario IDs) per [../issue/references/issue-format.md](../issue/references/issue-format.md);
   ask which (multi-select). Do not write tests — `as:fix` picks the issues up.
