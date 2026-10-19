---
name: agent-docs
description: "Build or update hierarchical documentation for coding agents: a short repo-root AGENTS.md, per-application AGENTS.md with architecture and a .guidelines/ folder (testing, libraries, architecture, code style), and per-module AGENTS.md, each with a CLAUDE.md that imports it. Detects missing files and drift, asks about ambiguities, recommends improvements. Use only when the user explicitly invokes as:agent-docs."
disable-model-invocation: true
argument-hint: "[path] [--check] [--depth N]"
---

# Agent docs

Build and maintain a documentation tree that a coding agent reads progressively: little at the repo root, more as it
descends into an application or module, and detailed rules in `.guidelines/` only when the task needs them.

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `[path]` — limit the run to this subtree (default: repository root). Parents of the subtree are read for context but not rewritten.
- `--check` — audit only: produce the report, questions and recommendations, write nothing.
- `--depth N` — deepest directory level that may get its own `AGENTS.md` (default 4, counted from the repo root).

Host-specific mechanics (subagents, asking questions): [Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).

## Documentation model

| Level | What it is | Files |
|-------|------------|-------|
| Repo root | Git root | `AGENTS.md` (≤ ~40 lines): what the project is, map of top-level directories/apps, global commands, shared rules |
| App root | Directory with an application manifest (`pom.xml`, `build.gradle*`, app `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, …) | `AGENTS.md` (≤ ~80 lines): purpose, stack, architecture, key libraries, commands, index of `.guidelines/`; plus `.guidelines/*-guideline.md` |
| Module | Module of a modular monolith, workspace package, or directory with a clear responsibility | `AGENTS.md` (≤ ~40 lines): responsibility, public API/entry points, dependencies, local pitfalls |

- A single-application repository merges repo root and app root into one file.
- Next to every `AGENTS.md` there is a `CLAUDE.md` containing only `@AGENTS.md`.
- A child never repeats what its parent says.
- `.guidelines/` files are **not** imported with `@`; the app `AGENTS.md` lists them with a "read before …" trigger so they are loaded on demand.
- If the repository has a human-readable specification in `docs/spec/` (from `as:spec-docs`), link it, never import it:
  the repo root links `docs/spec/index.html`, each app links its `docs/spec/<app>/index.html`, and each module whose spec
  page names the module directory as its source links that page. One line each, see the templates.
- Everything written is in English and states only facts backed by the code or by the user's answers. Never invent conventions.

Templates for every file type: [references/templates.md](references/templates.md).
Detection heuristics and the subagent brief: [references/analysis.md](references/analysis.md).

## Procedure

### 1. Inventory

Work in the main thread and keep it cheap:

- List tracked files (`git ls-files`, scoped to `[path]`) and derive the directory tree.
- Find existing `AGENTS.md`, `CLAUDE.md` and `.guidelines/` directories.
- If `docs/spec/` exists, map each spec page to its directory using the `Source` entry of its `<dl class="meta">`
  (grep for it; do not read the pages).
- Classify directories into repo root / app root / module / skip using [references/analysis.md](references/analysis.md).
  Always include directories that already contain `AGENTS.md` or `CLAUDE.md`, so they get audited.
- Show the user the planned tree (which directories get which level) in a compact form before spending effort on analysis.
  If the classification is uncertain (for example: is this directory an app or a shared library?), ask now.

### 2. Analysis (subagents, read-only)

Fan out one read-only subagent per directory (batch tiny sibling modules into one subagent). Go **bottom-up**:

1. modules,
2. app roots — they receive the module reports instead of re-reading module code, and also collect guideline material,
3. repo root — it receives the app reports.

Run independent subagents of the same wave in parallel. Each gets the brief from [references/analysis.md](references/analysis.md)
filled with: the directory, its level, the current contents of its `AGENTS.md`/`CLAUDE.md`/`.guidelines/`, and the list of
child directories that get their own file. Each returns the structured report defined there, including **drift**,
**open questions** and **recommendations**.

If the host has no subagents, do the same analysis sequentially in the main thread, in the same order.

### 3. Clarify with the user

Collect open questions from all reports, deduplicate them and ask in small batches, most impactful first. Offer concrete
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
| `OK` | File matches the code |
| `STALE` | File documents a directory that no longer deserves its own file, or describes removed things |
| `MIGRATE` | `CLAUDE.md` with real content but no `AGENTS.md` — content moves to `AGENTS.md` |

Then a **Recommendations** section: what would make a coding agent more effective, beyond documentation. Examples: no
command to run a single test, no lint/format script, undocumented environment variables or missing `.env.example`, no
reference module to copy when adding a new one, inconsistent naming, a detected area without a guideline.

With `--check`, stop here. Otherwise ask for approval: all, a selected subset, or cancel.

### 5. Write

- New files from the templates. Existing files: minimal edits — keep hand-written sections, fix only false or missing facts.
- Create or update `.guidelines/` files only for areas with evidence or user answers; keep the app `AGENTS.md` index in sync.
- Keep the `<!-- as:working-principles … -->` block (or its `off` marker) in the root `AGENTS.md` untouched: it is owned
  by `as:init`, is not drift, and does not count toward the line budget.
- `CLAUDE.md` next to each `AGENTS.md` contains exactly `@AGENTS.md`. For `MIGRATE`, move the content first.
- Never delete files (including `STALE` ones) unless the user explicitly approved that deletion.
- Do not touch application code; recommendations are reported, not implemented.

### 6. Verify

- Every path mentioned in the written files exists, including links to `docs/spec/` pages; a module with a spec page
  and no link is reported as `UPDATE`.
- Every command mentioned exists in a manifest, script or build file.
- Each app `AGENTS.md` guideline index matches the files in its `.guidelines/`.

Finish with a short summary (files created / updated / left as is, open items) and suggest reviewing `git diff`.
