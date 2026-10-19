---
name: finish
description: "Wrap up a delivered feature on the current branch: simplify the changed code, review it, check the touched modules against the HTML spec (intended change vs regression), write missing contract tests tagged with scenario IDs, and refresh AGENTS.md docs — only for what the branch changed, with tests after every code change and approval before each write. Does not commit. Use only when the user explicitly invokes as:finish."
disable-model-invocation: true
argument-hint: "[base] [--no-simplify] [--no-review] [--no-tests] [--no-docs]"
---

# Finish

Close a feature before committing and opening a PR. This skill owns only the scope, the order and the approval
gates. Spec rules come from [spec-docs](../spec-docs/SKILL.md), docs rules from [agent-docs](../agent-docs/SKILL.md),
simplify and review criteria from [references/review.md](references/review.md) — read them and follow them.

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `[base]` — ref to compare against (default: merge-base with the default branch).
- `--no-simplify`, `--no-review`, `--no-tests`, `--no-docs` — skip steps 3, 4, 6, 7.

Host-specific mechanics (subagents, asking questions, which simplify/review tools to use):
[Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).

Order matters: simplify before review, so the review judges the code that ships and catches anything simplify broke;
spec and tests after the code is final; docs last.

## Procedure

### 1. Scope

- Base: `[base]`, else `git merge-base HEAD origin/HEAD`, else the merge-base with `main` or `master`.
- Changed files: commits since base plus uncommitted and untracked changes (`git diff --name-only <base>`,
  `git status --porcelain`). Ignore generated files and `docs/spec/`.
- Map files to apps and modules using the `AGENTS.md` tree and the `Source` entries of `docs/spec/` pages.
- Show the scope (base, files count, touched modules). Empty diff → stop.

### 2. Baseline tests

Run the test commands listed in the relevant `AGENTS.md` files — per module when a single-module command exists,
otherwise the app's test command. If none is documented, ask for it. Failing tests → stop and report: do not polish
code that does not work yet.

### 3. Simplify

Simplify only the changed code, without changing behaviour, using the host tool or the criteria in
[references/review.md](references/review.md). Then rerun the tests. If they fail, revert the simplification that broke
them and report it.

### 4. Review

Review the diff from base using the host tool or [references/review.md](references/review.md). Present the findings
grouped Must / Should / Nice, each with a concrete failure scenario. Ask which to fix, fix only those, rerun the tests.

### 5. Spec

Skip if `docs/spec/` does not exist; say once that `as:spec-docs` would make the contract checkable.

**Change proposals first.** Find open proposals in `docs/spec/changes/*.html` that belong to this branch (slug in the
branch name or commit messages, or affected modules among the touched ones); confirm with the user. For each:

- check every `added`/`changed`/`removed` scenario against the code: implemented, partly, or not;
- merge the implemented ones into the module pages per `spec-docs` rules (keep the proposal's IDs; `removed` →
  `data-status="removed"`), and ask what to do with the rest: keep the proposal open, or drop those scenarios;
- when all is merged or dropped, set the proposal's status (`implemented` / `dropped`, body `data-status` and `meta`),
  fix its relative links for the new depth, and move it to `docs/spec/changes/archive/<YYYY-MM-DD>-<slug>.html`.

Drift explained by a merged proposal is intended by definition. For the remaining drift in touched modules, run the
`spec-docs` analysis and drift check for those modules only, and ask the user to classify each item:

- **Intended** — part of this feature: update the page per `spec-docs` rules (new IDs for new scenarios, changed
  scenarios keep their ID, removed ones get `data-status="removed"`).
- **Unintended** — a regression: report it as a bug and fix the code (then rerun the tests). Never adjust the spec to
  match a bug.

Touched modules without a spec page that gained public behaviour: offer to create the page (`spec-docs` rules,
including the shared `spec.css`).

### 6. Contract tests

Run the `spec-docs` test coverage for the touched modules. For `MISSING` and `PARTIAL` scenarios — those from the
merged proposals first, then `error` and `edge` — show the list and ask which to cover. Then write the tests:

- through the module's public entry points, not internal classes;
- following `.guidelines/testing-guideline.md` and its reference test, in the existing test location and style;
- with the scenario ID in the test name or tag (for example `@Tag("ORD-003")`, `it("ORD-003 rejects …")`).

Run the new tests. A new test that fails points to a bug or a wrong scenario: report it and ask; never weaken the
assertion to make it pass.

### 7. Agent docs

Run `agent-docs` for the touched directories (and their parents when the map of apps or modules changed): report,
approval, write. This also links new spec pages.

### 8. Summary

Short summary: code simplified, review fixes, proposals merged or kept open, spec scenarios added/changed/removed, tests added (with scenario IDs),
docs updated, open items (unfixed findings, unclassified drift, failing tests). Do not commit. Next steps:
`/commit-commands:commit-push-pr` (or `/commit-commands:commit`), then `/code-review:code-review` on the PR — Claude
Code only, if installed.
