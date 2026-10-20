---
name: help
description: "Show how to work with Claude Code (or Codex) using the as: commands, the recommended Anthropic plugins and plan mode: confirms the plugin is installed, lists as: skills, reports which recommended plugins are installed, and walks through the task workflow from onboarding to planning, building, review, finishing a feature, commit, docs upkeep and periodic health checks. Use only when the user explicitly invokes as:help."
disable-model-invocation: true
argument-hint: "[onboarding|plan|build|review|finish|commit|worktree|docs|health]"
---

# Help

Read-only: do not modify files or install anything. Answer in the user's language. Use the invocation syntax of the
current host: `/as:<skill>` in Claude Code, `$as:<skill>` in Codex.

With a topic argument, show only that section of the guide. Without one, show:

1. **Installed** — one line confirming that `as` is installed, then each skill from `skills/*/SKILL.md` next to this
   file: its invocation and a one-line summary of its `description`.
2. **Recommended plugins** — on Claude Code, check them as described in
   [references/recommended-plugins.md](../../references/recommended-plugins.md) and show `INSTALLED` / `DISABLED` /
   `MISSING` per plugin. For missing or disabled ones, suggest `/as:init` or the `claude plugin` command. On Codex, say
   these are Claude Code plugins and skip.
3. **Guide** — the sections below, concise, as a numbered workflow. Commands of plugins that are not installed are
   marked "(not installed)".

## Guide

### onboarding — once per repository

- `/as:init` — builds the `AGENTS.md` hierarchy, the HTML spec for chosen modules, links between them, and checks the
  recommended plugins. Rerun parts later with `/as:agent-docs` and `/as:spec-docs`.

### plan — before non-trivial changes

- **`as:tech-lead`** starts on its own when you describe a feature, a bug or a design question (or call
  `/as:tech-lead <topic>`): it reads the code and spec first, asks targeted questions, compares 2–3 architectures,
  records the decision and proposed scenarios in `docs/spec/changes/<slug>.html`, writes the plan, and offers the
  next step — plan mode (large changes get milestones).
- **Plan mode** (Claude Code): press Shift+Tab until the mode indicator shows plan mode. Claude reads code, asks
  questions and proposes a plan without editing; you approve it or ask for changes, then it implements.
  Use it for multi-file changes, unclear requirements, and anything that changes a module's contract — ask Claude to
  read the module's spec page (linked from its `AGENTS.md`) while planning.
- **Larger features without `as:tech-lead`**: `/feature-dev:feature-dev <description>` — explores the codebase,
  designs the architecture, implements and reviews in guided phases.
- On Codex: ask for a plan first and say not to edit until you approve it.

### build — implementing

- Claude follows `AGENTS.md` and reads `.guidelines/` when the task touches their area — keep them current.
- UI work: `frontend-design` triggers on its own.
- Changing a module's observable behaviour: update its spec with `/as:spec-docs <module path>` and tag contract tests
  with scenario IDs.

### review — before committing and on the PR

- Default path: `/as:finish` (next section) — it runs simplify and review for you. The items below are for ad-hoc use.
- Ask Claude to run the `code-simplifier` agent on the recent changes.
- `/as:spec-docs --tests` — which contract scenarios lack tests (unhappy paths first).
- Security-sensitive changes or a release: run `/claude-security` (or ask for a security scan).
- PR open: `/code-review:code-review`.

### finish — after delivering a feature

- `/as:finish` — on the branch's changes only: baseline tests → simplify → review (you pick fixes) → spec check for
  touched modules (intended change vs regression) → writes missing contract tests tagged with scenario IDs →
  refreshes `AGENTS.md`. Tests rerun after every code change; nothing is committed.
- `/as:finish <base>` to compare against another ref; `--no-simplify`, `--no-review`, `--no-tests`, `--no-docs` skip steps.

### commit — git workflow

- `/commit-commands:commit` — commit with a generated message.
- `/commit-commands:commit-push-pr` — commit, push and open a PR.
- `/commit-commands:clean_gone` — remove local branches deleted on the remote.

### worktree — parallel branches

- `/as:worktree-create <name> [from <branch>]` — new branch and worktree in `../<repo>-worktrees/<name>`; start a new
  session in that folder to work on it.
- `/as:worktree-close [<name>]` — offers to commit leftovers, then removes the folder; the branch stays.

### docs — keeping documentation true

- Periodically, or after larger refactors: `/as:agent-docs --check` and `/as:spec-docs --check`, then run them without
  `--check` to apply fixes.

### health — once a sprint or month

- `/as:health` — whole-project check: hotspots (often changed and complex code), coupling and cycles, coverage and
  test quality (missing, excessive or weak tests), dead code, duplication, dependencies, docs drift. Writes
  `docs/health/<date>.html` with trends against the previous run, then fixes the small items you pick and turns larger
  ones into task briefs for plan mode.
- `/as:health --quick` for a fast pass (git and configured tools only); `--no-fix` for the report only.
