---
name: spec-docs
description: "Build or update a human-readable Markdown specification of the application in docs/spec/: a system overview, per-application pages and per-module contract pages with requirements and Given/When/Then scenarios (happy, error and edge paths) with stable IDs, formatted to read well rendered and in diffs. Converts a legacy HTML spec to Markdown. Behaviour confirmed as a bug goes to docs/issues/, not into the spec. Use only when the user explicitly invokes as:spec-docs."
disable-model-invocation: true
argument-hint: "[path] [--lang en|pl]"
---

# Spec docs

Build and maintain a specification **for humans**: what the system does, what each application is for, and what each
module promises to the rest of the application — its public contract, expressed as requirements and scenarios. The same
scenarios are the yardstick for contract-level tests.

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `[path]` — limit the run to this subtree (default: repository root). Pages outside it are read for context but not rewritten.
- `--lang en|pl` — language of the page content (default `en`). IDs, anchors, file names and the fixed values of the
  format (kinds, statuses) stay English.
  When updating existing pages, keep their language unless the user asked to change it.

An audit without writes is `as:docs-check`; the scenario test coverage report is `as:spec-tests`.

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

If the host has no subagents, do the same analysis sequentially in the main thread, in the same order.

### 3. Clarify with the user

Collect open questions from all reports, deduplicate, and ask in small batches, most impactful first, with options
derived from the code. Typical questions:

- Is this behaviour an intended business rule or a bug? Only intended rules go into the spec. A bug becomes an issue
  candidate (kind `bug`, with the evidence from the report and the intended behaviour from the answer) per
  [../issue/references/issue-format.md](../issue/references/issue-format.md), saved in step 5 — not a note on the
  page.
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

Then the issue candidates: the bugs from step 3, and existing `> [!NOTE]` open questions that describe a confirmed
bug rather than an open decision (written that way before 1.6.0) — these move to issues and their notes are removed.
Such a note says what the code does now and what it should do ("known gap", "currently X, should be Y", "is lost
instead of deferred"); a note that asks what the behaviour should be stays a question. Unsure → ask. Each moved note
is re-checked in the code first, so its issue gets current evidence (symbol and excerpt), not just the note's text.

Ask for approval: all, a selected subset, or cancel; issues are chosen separately (multi-select).

### 5. Write

- Create `docs/spec/` if missing.
- **Migrate first**, before any content change, so drift fixes show as a separate diff: convert every legacy page one
  to one with the mapping in [references/markdown-format.md](references/markdown-format.md) — same content, IDs,
  statuses and language, nothing added or dropped — write the `.md` next to it, then delete the `.html` with
  `git rm` (or `rm` if untracked). Proposals keep their status and archive date. Then rewrite links: `.html` → `.md`
  (fragments unchanged) in the converted pages and, only in their link targets, in the files listed in the report.
  Delete `docs/spec/spec.css` unless something still links it (`git grep -l 'spec/spec.css'`) — then keep it and say
  that `as:health` relinks its reports on the next run.
- Approved issues: write them to `docs/issues/` per the issue format (duplicates update the existing file), and
  remove the open-question notes they replace.
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

Finish with a short summary (pages created / updated / left as is, scenarios added / removed, open questions, issues
saved — fix them with `as:fix`) and
suggest reading `docs/spec/index.md` in the repository browser or the IDE's Markdown preview and reviewing `git diff`. If pages were created or removed and the
repository has `AGENTS.md` files, suggest running `as:agent-docs` so the app docs link the new pages.
