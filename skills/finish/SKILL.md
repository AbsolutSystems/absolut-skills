---
name: finish
description: "Wrap up a delivered feature on the current branch: simplify the changed code, review it, check the touched modules against the Markdown spec (intended change vs regression), write missing contract tests tagged with scenario IDs, and refresh AGENTS.md docs — only for what the branch changed, with tests after every code change and approval before each write. Does not commit. Use only when the user explicitly invokes as:finish."
disable-model-invocation: true
argument-hint: "[base] [--no-simplify] [--no-review] [--no-tests] [--no-docs]"
---

# Finish

Close a feature before committing and opening a PR. This skill owns only the scope, the order and the approval
gates. Spec rules come from [spec-docs](../spec-docs/SKILL.md), docs rules from [agent-docs](../agent-docs/SKILL.md),
simplify and review criteria from [references/review.md](references/review.md) — read them and follow them.

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `[base]` — ref to compare against (default: merge-base with the default branch).
- `--no-simplify`, `--no-review`, `--no-tests`, `--no-docs` — skip steps 3, 4, 7, 8.

Host-specific mechanics (subagents, asking questions, which simplify/review tools to use):
[Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).

Order matters: simplify before review, so the review judges the code that ships and catches anything simplify broke;
spec and tests after the code is final; docs last.

## Procedure

### 1. Scope

- Base: `[base]`, else `git merge-base HEAD origin/HEAD`, else the merge-base with `main` or `master`.
- Changed files: commits since base plus uncommitted and untracked changes (`git diff --name-only <base>`,
  `git status --porcelain`). Ignore generated files, `docs/spec/` and `docs/issues/`.
- Map files to apps and modules using the `Source` entries of `docs/spec/` pages, the `AGENTS.md` tree, and the
  classification heuristics in [../agent-docs/references/analysis.md](../agent-docs/references/analysis.md).
- Show the scope (base, files count, touched modules). Empty diff → stop.

### 2. Baseline checks

Run the test commands listed in the relevant `AGENTS.md` files — per module when a single-module command exists,
otherwise the app's test command — plus the documented lint, type-check and build commands for the touched apps. If
no test command is documented, ask for it. Failing tests, build, or lint and type errors in the changed files → stop
and report: do not polish code that does not work yet. Lint and type errors only in unchanged files are pre-existing:
record them, say so once, and continue. "Rerun the tests" below means rerunning these checks; only failures beyond
the recorded ones count.

### 3. Simplify

Simplify only the changed code, without changing behaviour, using the host tool or the criteria in
[references/review.md](references/review.md). Then rerun the tests. If they fail, revert the simplification that broke
them and report it.

### 4. Review

Review the diff from base using the host tool or [references/review.md](references/review.md). Present the findings
grouped Must / Should / Nice, each with a concrete failure scenario. Ask which to fix, fix only those, rerun the tests.
Then offer to save the unfixed Must and Should findings as issues (multi-select, all preselected; Nice only on
request) per [../issue/references/issue-format.md](../issue/references/issue-format.md), `**Source:**` `as:finish review`.

### 5. Analysis

One read-only pass per touched module, anchored in the diff, feeds steps 6–8. First, in the main thread: find the
branch's open proposals (step 6, "Change proposals first", confirmed with the user) and run the cheap pass of the
`spec-docs` test coverage (`git grep -n '<ID>'` over test directories for the scenario IDs of the touched modules and
the proposals). Then fan out one read-only subagent per touched module (batch tiny sibling modules), in parallel, with
the brief in [references/analysis.md](references/analysis.md): base and module directory (the subagent runs the
diff itself), spec page, proposal scenarios, cheap-pass hits and `AGENTS.md`. With `--no-tests` or `--no-docs`, drop the Tests or Docs section from the brief.

Steps 6–8 use these reports and do not rerun the analysis; after a code fix in step 6, rerun it only for that module.
Without subagents, run it sequentially.

### 6. Spec

Skip if `docs/spec/` does not exist; say once that `as:spec-docs` would make the contract checkable.

If `docs/spec/` still has legacy `*.html` pages, propose the `spec-docs` migration (its step 5, "Migrate first") for the
whole spec before anything else, with approval; without it, read the pages as they are and write nothing to them.

**Change proposals first.** Open proposals in `docs/spec/changes/*.md` that belong to this branch (slug in the branch
name or commit messages, or affected modules among the touched ones), as confirmed in step 5. For each:

- check its `## Plan` (if present): every unticked step is verified against the code and the diff — ticked when done,
  otherwise listed as an open item;
- take the status of every `added`/`changed`/`removed` scenario from the Proposal sections of step 5: implemented,
  partly, or not;
- run its `**Verify:**` check if it can be run locally, else ask the user to confirm it; carry its `**Rollout:**`
  items to the summary as open items;
- before merging, check that its added IDs are still free:
  [spec_lint.py](../spec-docs/scripts/spec_lint.py) `--against origin/HEAD` (or the default branch), or by hand with
  `git grep -hoE '<PREFIX>-R?[0-9]+' origin/HEAD -- docs/spec`. An ID taken meanwhile by another branch → stop,
  propose the next free numbers, and after approval renumber them in the proposal and in the tests;
- merge the implemented ones into the module pages per `spec-docs` rules (keep the proposal's IDs; `removed` →
  removed status), and ask what to do with the rest: keep the proposal open, or drop those scenarios;
- when all is merged or dropped, set the proposal's `**Status:**` (`implemented` / `dropped`), fix its relative links
  for the new depth, and move it to `docs/spec/changes/archive/<YYYY-MM-DD>-<slug>.md`. An `implemented` proposal
  with an `**Issue:**` meta line closes that issue: delete the issue file with `git rm` in the same diff (a `dropped`
  one leaves the issue open).

Drift explained by a merged proposal is intended by definition. For the remaining items of the Spec drift and New
behaviour sections from step 5, ask the user to classify each:

- **Intended** — part of this feature: update the page per `spec-docs` rules (a new behaviour candidate becomes a
  scenario with a new ID, changed scenarios keep their ID, removed ones get the removed status).
- **Unintended** — a regression: report it as a bug and fix the code (then rerun the tests). Never adjust the spec to
  match a bug. Only if the user explicitly defers the fix, save it as a `bug` issue instead.

Touched modules without a spec page whose New behaviour section is not empty: offer to create the page with the
`spec-docs` procedure for that module.

### 7. Contract tests

Take the Tests sections from step 5 — the proposal scenarios and the new behaviour the diff added. Older gaps of the
module are out of scope (`as:spec-tests` reports them). For `MISSING` and `PARTIAL` scenarios — those from the
merged proposals first, then `error` and `edge` — show the list and ask which to cover. Then write the tests:

- through the module's public entry points, not internal classes;
- following `.guidelines/testing-guideline.md` and its reference test, in the existing test location and style;
- with the scenario ID in the test name or tag (for example `@Tag("ORD-003")`, `it("ORD-003 rejects …")`).

Run the new tests. A new test that fails points to a bug or a wrong scenario: report it and ask — fix the code, correct the
scenario, or save a `bug` issue (then leave that test out of the diff); never weaken the assertion to make it pass.

### 8. Agent docs

Run `agent-docs` for the touched directories with the Docs sections from step 5 as its module analysis (its own
analysis only for the parents, when the map of apps or modules changed), then its questions, report, approval and
write. Only fix facts the branch made false and add facts it made necessary (a new command, rule or pitfall); never add
descriptions of the new code. This also links new spec pages.

### 9. Summary

Short summary: code simplified, review fixes, proposals merged or kept open, spec scenarios added/changed/removed, tests added (with scenario IDs),
docs updated, issues saved and closed, open items (unfixed findings, unclassified drift, failing tests, proposal `**Rollout:**` items). Do not commit. Next steps:
`/commit-commands:commit-push-pr` (or `/commit-commands:commit`), then `/code-review:code-review` on the PR — Claude
Code only, if installed. If the diff touches authentication, authorisation, input handling, secrets or data access,
first suggest a security scan of the branch's changes with `/claude-security` (Claude Code only, if installed).
