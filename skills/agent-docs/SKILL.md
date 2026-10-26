---
name: agent-docs
description: "Build or update minimal documentation for coding agents that holds only what the code cannot tell: a short repo-root AGENTS.md, per-application AGENTS.md (commands, unenforced rules, internal libraries, target vs legacy) with on-demand .guidelines/, and module AGENTS.md only where a module has pitfalls or rules, each with a CLAUDE.md that imports it. Analyses the code to ask the team the right questions, detects drift, prunes lines the code already shows, recommends improvements. Use only when the user explicitly invokes as:agent-docs."
disable-model-invocation: true
argument-hint: "[path] [--depth N]"
---

# Agent docs

Build and maintain the smallest documentation tree that changes what a coding agent does: commands, rules the code does
not enforce, which of two conventions is the target, what internal libraries provide, and pitfalls. Descriptions of what
the code already shows (purpose, stack, public API, dependencies) are left out — agents read them from the code, and
context files that repeat the repository make agents explore more and cost more without solving more tasks
([Gloaguen et al., 2026](https://arxiv.org/abs/2602.11988)).

**Line test:** a line stays only if, without it, an agent would do something wrong or have to guess.

The code analysis exists to ask the team good questions; their answers are the most valuable content.

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `[path]` — limit the run to this subtree (default: repository root). Parents of the subtree are read for context but not rewritten.
- `--depth N` — deepest directory level that may get its own `AGENTS.md` (default 4, counted from the repo root).

An audit without writes is `as:docs-check`.

Host-specific mechanics (subagents, asking questions): [Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).

## Documentation model

| Level | What it is | Files |
|-------|------------|-------|
| Repo root | Git root | `AGENTS.md` (≤ ~25 lines): one sentence on the product, map of apps (one line each), repo-wide commands, shared rules |
| App root | Directory with an application manifest (`pom.xml`, `build.gradle*`, app `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, …) | `AGENTS.md` (≤ ~50 lines): commands (including a single test), rules the code does not enforce, internal libraries and what not to re-implement, target vs legacy, reference module, index of `.guidelines/`, spec links; plus `.guidelines/*-guideline.md` |
| Module | Module of a modular monolith, workspace package, or directory with a clear responsibility | `AGENTS.md` (≤ ~20 lines) **only when the module has pitfalls or rules** (invariants, "do not call X from outside", legacy parts, a module-specific command) |

- A single-application repository merges repo root and app root into one file.
- Next to every `AGENTS.md` there is a `CLAUDE.md` containing only `@AGENTS.md`.
- A child never repeats what its parent says.
- `.guidelines/` files are **not** imported with `@`; the app `AGENTS.md` lists them with a "read before …" trigger so they are loaded on demand.
- If the repository has a human-readable specification in `docs/spec/` (from `as:spec-docs`), link it, never import it:
  the repo root links `docs/spec/index.md`, and each app lists its module pages in one "Specification" section (the
  module directory from the page's `Source` → page path). See the templates.
- Everything written is in English and is one of: a user's answer, a command that exists, a rule the code does not
  enforce (with evidence it is followed), or a pitfall with evidence. Never describe the code; never invent conventions.

Templates for every file type: [references/templates.md](references/templates.md).
Detection heuristics and the subagent brief: [references/analysis.md](references/analysis.md).

## Procedure

### 1. Inventory

Work in the main thread and keep it cheap:

- List tracked files (`git ls-files`, scoped to `[path]`) and derive the directory tree.
- Find existing `AGENTS.md`, `CLAUDE.md` and `.guidelines/` directories. Check whether either file is a symlink
  (`ls -l`, `git ls-files -s` mode `120000`): an `AGENTS.md` ↔ `CLAUDE.md` symlink is reported as `MIGRATE`.
- If `docs/spec/` exists, map each spec page to its directory using the `**Source:**` entry of its meta line
  (`git grep -n '\*\*Source:\*\*' docs/spec`; legacy `*.html` pages: the `Source` entry of `<dl class="meta">`); do
  not read the pages.
- Classify directories into repo root / app root / module / skip using [references/analysis.md](references/analysis.md).
  Always include directories that already contain `AGENTS.md` or `CLAUDE.md`, so they get audited.
- Show the user the planned tree (which directories get which level) in a compact form before spending effort on analysis.
  If the classification is uncertain (for example: is this directory an app or a shared library?), ask now.

### 2. Analysis (subagents, read-only)

The analysis looks for what an agent would get wrong, not for what the code contains: conflicting conventions, rules
followed but not enforced, invariants and traps, missing or non-obvious commands, and lines in existing docs that only
repeat the code. Fan out one read-only subagent per directory (batch tiny sibling modules into one subagent). Go **bottom-up**:

1. modules,
2. app roots — they receive the module reports instead of re-reading module code, and also collect guideline candidates,
3. repo root — it receives the app reports.

Run independent subagents of the same wave in parallel. Each gets the brief from [references/analysis.md](references/analysis.md)
filled with: the directory, its level, the current contents of its `AGENTS.md`/`CLAUDE.md`/`.guidelines/`, and the list of
child directories that get their own file. Each returns the structured report defined there, including **drift**,
**open questions** and **recommendations**.

If the host has no subagents, do the same analysis sequentially in the main thread, in the same order.

### 3. Clarify with the user

This is the main work of the skill: the team knows what the code cannot show. Collect open questions from all reports, deduplicate them and ask in small batches, most impactful first. Offer concrete
options derived from the code when possible. Typical questions:

- What an internal library (for example `preboot`) provides and what must not be re-implemented by hand.
- Conflicting conventions (two test frameworks, two HTTP clients) — which one is the target, which is legacy.
- Unclear purpose of a directory, or whether it is deprecated.
- Testing strategy when the code does not reveal it (what level of tests a new feature needs).

Record answers as facts in the files they belong to. Unanswered questions are left out of the docs, not guessed.

### 4. Report

Present one table, one row per file to be touched:

| Status | Meaning |
|--------|---------|
| `NEW` | File does not exist and should |
| `UPDATE` | File exists; list each drift item (false claim + evidence) and each missing fact |
| `PRUNE` | File exists; list the lines that fail the line test (they repeat what the code shows) |
| `OK` | File matches the code and every line passes the line test |
| `STALE` | Module file with no pitfalls or rules left, or a file describing removed things |
| `MIGRATE` | `CLAUDE.md` with real content but no `AGENTS.md`, or a symlink between them — content moves to a regular `AGENTS.md` |

Then a **Recommendations** section: what would make a coding agent more effective, beyond documentation. Examples: no
command to run a single test, no lint/format script, undocumented environment variables or missing `.env.example`, no
reference module to copy when adding a new one, inconsistent naming, a detected area without a guideline.

Ask for approval: all, a selected subset, or cancel.

### 5. Write

- New files from the templates. Existing files: minimal edits — keep hand-written sections, fix only false or missing facts.
- `PRUNE`: remove only the lines the user approved; a line that may hold team knowledge is kept and asked about.
- Create or update `.guidelines/` files only for rules the user confirmed or a tool enforces; keep the app `AGENTS.md`
  index in sync.
- Keep the `<!-- as:working-principles … -->` block (or its `off` marker) in the root `AGENTS.md` untouched: it is owned
  by `as:init`, is not drift, and does not count toward the line budget.
- `CLAUDE.md` next to each `AGENTS.md` contains exactly `@AGENTS.md`. For `MIGRATE`, move the content first. If
  either file is a symlink, remove the symlink and write both as regular files — writing through a symlink would make
  `CLAUDE.md` import itself.
- Never delete files (including `STALE` ones) unless the user explicitly approved that deletion.
- Do not touch application code; recommendations are reported, not implemented.

### 6. Verify

- No `AGENTS.md`/`CLAUDE.md` is a symlink, and every `CLAUDE.md` is exactly `@AGENTS.md`.
- Every path mentioned in the written files exists, including links to `docs/spec/` pages; an app whose module spec
  pages are not all listed is reported as `UPDATE`.
- Every written line passes the line test and every file is within its line budget.
- Every command mentioned exists in a manifest, script or build file.
- Each app `AGENTS.md` guideline index matches the files in its `.guidelines/`.

Finish with a short summary (files created / updated / left as is, open items) and suggest reviewing `git diff`.
