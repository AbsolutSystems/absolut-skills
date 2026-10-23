---
name: spec-docs
description: "Build or update a human-readable Markdown specification of the application in docs/spec/: a system overview, per-application pages and per-module contract pages with requirements and Given/When/Then scenarios (happy, error and edge paths) with stable IDs, formatted to read well rendered and in diffs. Converts a legacy HTML spec to Markdown. Can audit drift against the code and report which contract scenarios are covered by tests. Use only when the user explicitly invokes as:spec-docs."
disable-model-invocation: true
argument-hint: "[path] [--check] [--tests] [--lang en|pl]"
---

# Spec docs

Build and maintain a specification **for humans**: what the system does, what each application is for, and what each
module promises to the rest of the application — its public contract, expressed as requirements and scenarios. The same
scenarios are the yardstick for contract-level tests.

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `[path]` — limit the run to this subtree (default: repository root). Pages outside it are read for context but not rewritten.
- `--check` — audit only: report drift between the spec and the code, ask questions, write nothing.
- `--tests` — test coverage report only: map every scenario to the tests that verify it, write nothing.
- `--lang en|pl` — language of the page content (default `en`). IDs, anchors, file names and the fixed values of the
  format (kinds, statuses) stay English.
  When updating existing pages, keep their language unless the user asked to change it.

Host-specific mechanics (subagents, asking questions): [Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).

## Output model

```text
docs/spec/
  index.md               # system: purpose, actors, map of apps/modules, main flows
  changes/               # change proposals from as:tech-lead (open), merged by as:finish into archive/
  <app>/index.md         # application: purpose, modules and how they relate (monorepo only)
  <app>/<module>.md      # module contract: operations, requirements, scenarios, rules, dependencies
```

- A single-application repository has no `<app>/index.md`; module pages live in `docs/spec/<module>.md` and the
  system page covers the application.
- Pages are written for people: GitHub-flavoured Markdown using only the constructs and readability rules of
  [references/markdown-format.md](references/markdown-format.md), so they read well rendered and in a diff.
- Scenario IDs are stable (`<PREFIX>-NNN`) and are never renumbered or reused; tests refer to them.
- The spec describes observable behaviour from the point of view of a caller of the module (another module, a user, an
  external system), not the implementation. No internal class names, no algorithms.
- State only facts backed by the code or by the user's answers. Behaviour that looks like a bug is asked about, not specified.

Page format: [references/markdown-format.md](references/markdown-format.md).
Subagent briefs and report formats: [references/analysis.md](references/analysis.md).

## Procedure

### 1. Inventory

Work in the main thread and keep it cheap:

- List tracked files (`git ls-files`, scoped to `[path]`) and classify directories into app roots and modules using the
  heuristics in [../agent-docs/references/analysis.md](../agent-docs/references/analysis.md) (section "Classifying directories").
- If `AGENTS.md` files exist (from `as:agent-docs`), read them: they give commands, boundary rules and pitfalls cheaply.
- If `docs/spec/` exists, read it and collect every existing page, requirement ID and scenario ID with its kind and
  status, plus the IDs reserved by open proposals in `docs/spec/changes/*.md` (new IDs must skip them).
  Do not edit proposals or `changes/archive/` — they are owned by `as:tech-lead` and `as:finish` — except to migrate them.
- **Legacy HTML:** any `*.html` page under `docs/spec/` (including `changes/` and `archive/`) comes from an earlier
  version. Read it like a Markdown page (see "Legacy HTML pages" in the format reference) and plan its migration: the
  same path with `.md`. Also list tracked files outside `docs/spec/` that link to its `.html` pages
  (`git grep -lE 'spec/[^ )"]*\.html'`), typically `AGENTS.md` files and `docs/health/` pages. Do not read `spec.css`.
- Assign each new module an ID prefix: 2–4 uppercase letters derived from its name, unique across the spec. Existing
  prefixes are kept.
- Show the user the planned pages (path → source directory → prefix). Ask now if a classification is uncertain.

### 2. Analysis (subagents, read-only)

Fan out one read-only subagent per module (batch tiny sibling modules into one), **bottom-up**: modules, then app pages
(fed the module reports), then the system page (fed the app reports). Run independent subagents of one wave in parallel.
Each gets the spec brief from [references/analysis.md](references/analysis.md) with the existing page content and the
existing IDs for that module, and returns the structured report defined there.

With `--tests`, skip this step and go to [Test coverage](#test-coverage).

If the host has no subagents, do the same analysis sequentially in the main thread, in the same order.

### 3. Clarify with the user

Collect open questions from all reports, deduplicate, and ask in small batches, most impactful first, with options
derived from the code. Typical questions:

- Is this behaviour an intended business rule or a bug? (Only intended rules go into the spec.)
- Who the actors are and what a term means in the business domain (glossary).
- Whether an operation is public contract or internal (used by other modules only by accident).
- What should happen in an unhandled error case — record the answer as an open question on the page if it is not
  implemented yet, never as a scenario.

### 4. Report

One table, one row per page:

| Status | Meaning |
|--------|---------|
| `NEW` | Page does not exist and should |
| `UPDATE` | Page exists; list drift items (claim, why it is wrong, evidence) and missing requirements/scenarios |
| `OK` | Page matches the code |
| `STALE` | Page documents a module that no longer exists or was merged |
| `MIGRATE` | Legacy HTML page to convert to Markdown (combined with the status above, e.g. `MIGRATE+UPDATE`) |

Below the table list scenario changes per page: added (new IDs), changed (ID + what changed), removed (ID; will be
marked removed, not deleted). For a migration also list the files outside `docs/spec/` whose links will be
rewritten, and whether `docs/spec/spec.css` can be removed.

With `--check`, stop here. Otherwise ask for approval: all, a selected subset, or cancel.

### 5. Write

- Create `docs/spec/` if missing.
- **Migrate first**, before any content change, so drift fixes show as a separate diff: convert every legacy page one
  to one with the mapping in [references/markdown-format.md](references/markdown-format.md) — same content, IDs,
  statuses and language, nothing added or dropped — write the `.md` next to it, then delete the `.html` with
  `git rm` (or `rm` if untracked). Proposals keep their status and archive date. Then rewrite links: `.html` → `.md`
  (fragments unchanged) in the converted pages and, only in their link targets, in the files listed in the report.
  Delete `docs/spec/spec.css` unless something still links it (`git grep -l 'spec/spec.css'`) — then keep it and say
  that `as:health` relinks its reports on the next run.
- New pages from the skeletons in [references/markdown-format.md](references/markdown-format.md).
- Existing pages: minimal edits. Keep hand-written text, fix only false or missing facts, keep every existing ID.
  New scenarios take the next free number for the prefix. Removed scenarios get the removed status and stay.
- Update the meta line of each written page with the source path and the current commit (`git rev-parse --short HEAD`).
- Apply the readability rules of the format to every page you write, also to existing hand-written text you touch.
- Keep navigation in sync: the system page lists apps/modules, each app page lists its modules, each module page links back.
- Never delete pages (including `STALE` ones) without explicit approval. Do not touch application code, tests or
  `AGENTS.md` files — links from `AGENTS.md` to the spec are maintained by `as:agent-docs`; a migration only rewrites
  their `.html` link targets.

### 6. Verify

- Run [scripts/spec_lint.py](scripts/spec_lint.py) from the repository root (`python3 <this skill's
  directory>/scripts/spec_lint.py`); it must print `OK`. It checks: no `*.html` under `docs/spec/`; raw HTML only in
  the marker and the anchors; IDs well-formed (`<PREFIX>-NNN`, `<PREFIX>-R<n>`), unique outside `changes/`, one prefix
  per module page; IDs added by open proposals not used elsewhere; relative links and `#anchors` resolve. Without
  `python3`, check the same by hand.
- `git grep -nE 'spec/[^ )"]*\.html'` finds no links to spec pages outside `docs/spec/`.
- Every requirement and scenario heading carries its anchor; every scenario has a kind line and Given/When/Then.
- Every source path in a meta line exists.

The script has no dependencies; suggest the user add it to CI (copied into the repository) so the spec stays
checkable without an agent.

Finish with a short summary (pages created / updated / left as is, scenarios added / removed, open questions) and
suggest reading `docs/spec/index.md` in the repository browser or the IDE's Markdown preview and reviewing `git diff`. If pages were created or removed and the
repository has `AGENTS.md` files, suggest running `as:agent-docs` so the app docs link the new pages.

## Test coverage

`--tests` is read-only and requires an existing `docs/spec/`. It answers: does each promise in the contract have a test
that checks it through the module's public entry points?

1. Collect all active scenarios (status not `removed`) with their ID, module, kind and Given/When/Then text. Legacy
   HTML pages are read as they are; suggest migrating them.
2. **Cheap pass:** search test sources for each scenario ID (`git grep -n '<ID>'` over test directories) — in test names,
   tags/annotations or comments. A hit is a candidate match.
3. **Semantic pass:** for scenarios without a hit, fan out one read-only subagent per module with the coverage brief
   from [references/analysis.md](references/analysis.md). It reads the module's tests and classifies each scenario.
   Tests that only exercise internal classes do not count as contract coverage, but are mentioned as `PARTIAL` evidence.
4. Report per module, one row per scenario:

| ID | Kind | Status | Evidence |
|----|------|--------|----------|
| `ORD-003` | error | `COVERED` / `PARTIAL` / `MISSING` | test file path and test name, or what is missing |

Then a summary per module and in total: covered / partial / missing, with a separate count for `error` and `edge`
scenarios (unhappy paths are usually the gap). End with recommendations: which missing scenarios matter most, and — if
the cheap pass found few IDs — tagging contract tests with scenario IDs so future runs map them deterministically.
Do not write tests.
