---
name: help
description: "Show how to work with Claude Code (or Codex) using the as: commands, the recommended Anthropic plugins and plan mode: confirms the plugin is installed, lists as: skills, reports which recommended plugins are installed, and walks through the task workflow from onboarding to planning, building (implementing an approved plan), review, finishing a feature, commit, docs upkeep, periodic health checks and known issues, and how the commands chain into flows (client request estimate, feature, feature roadmap, unattended feature delivery, bug, known issues, health). Use only when the user explicitly invokes as:help."
disable-model-invocation: true
argument-hint: "[which|flows|onboarding|plan|build|review|finish|commit|worktree|docs|health|issues]"
---

# Help

Read-only: do not modify files or install anything. Answer in the user's language. Use the invocation syntax of the
current host: `/as:<skill>` in Claude Code, `$as:<skill>` in Codex.

With a topic argument, show only that section of the guide. Without one, show:

1. **Installed** — one line confirming that `as` is installed (skills from `skills/*/SKILL.md` next to this file that
   are missing from the table below are listed with a one-line summary of their `description`).
2. **Which command** — the [which](#which--which-command-for-what) table.
3. **Recommended plugins** — on Claude Code, check them as described in
   [references/recommended-plugins.md](../../references/recommended-plugins.md) and show `INSTALLED` / `DISABLED` /
   `MISSING` per plugin. For missing or disabled ones, suggest `/as:init` or the `claude plugin` command. On Codex, say
   these are Claude Code plugins and skip.
4. **Guide** — the sections below, concise, as a numbered workflow. Commands of plugins that are not installed are
   marked "(not installed)".

## Guide

### which — which command for what

Show this table as it is, in the user's language:

| I want to… | Command |
|------------|---------|
| start with a repository (agent docs, spec, plugins) | `as:init` |
| design a feature, investigate a bug, choose between options | `as:tech-lead` (also starts on its own) |
| analyse and price a client's feature request | `as:estimate` |
| keep a feature's why, acceptance criteria, roadmap and sources (PDF, e-mails) in one place | `as:feature` |
| continue an approved plan, also in a new session | `as:implement` |
| deliver a whole documented feature unattended (e.g. overnight) | `as:deliver` |
| wrap up a feature before the PR (simplify, review, spec, tests, docs) | `as:finish` |
| save a problem to fix later (also findings of `/code-review`) | `as:issue` |
| fix the saved problems, most important first | `as:fix` |
| check whether agent docs and spec still match the code (no writes) | `as:docs-check` |
| update agent docs / the spec | `as:agent-docs` / `as:spec-docs` |
| see which spec scenarios have no tests | `as:spec-tests` |
| review the health of the whole project | `as:health` |
| work on several branches at once | `as:worktree-create` / `as:worktree-close` |
| learn how it all fits together | `as:help flows` |

### flows — how the commands chain

Show these as short chains, then point to the sections below for details:

- **Feature**: `as:tech-lead <feature>` (proposal + plan in `docs/spec/changes/<slug>.md`) → implement now or
  `as:implement` in a new session → `as:finish` → `/commit-commands:commit-push-pr`.
- **Client request**: `as:estimate <request>` (analysis, PRD and hour estimate in `docs/estimates/<slug>/`;
  send `client.md`) → `as:estimate docs/estimates/<slug>` with the client's answers → after acceptance
  `as:tech-lead docs/estimates/<slug>` → the Feature flow.
- **Feature roadmap** (a feature that ships in several changes, or comes with client material): `as:feature
  <description, files, pasted e-mail>` (or `docs/estimates/<slug>`, or a legacy docs folder) → page and sources in
  `docs/features/<slug>/` → `as:tech-lead docs/features/<slug>` per phase → the Feature flow (`as:finish` marks the
  phase done); new material → `as:feature docs/features/<slug>`. To brief a new session: "read
  `docs/features/<slug>/index.md`".
- **Unattended feature**: `as:feature …` → `as:deliver docs/features/<slug>` (questions at the start, then the
  Feature flow per phase without asking, local commits, report in `docs/features/<slug>/delivery.md`) → review the
  assumptions and commits → `/commit-commands:commit-push-pr`.
- **Bug**: `as:tech-lead <symptom>` (root cause, failing test, fix after approval; or saved to `docs/issues/` if you
  defer it) → `as:finish` → commit.
- **Known issues**: problems found by any skill, or by `/code-review` and `/claude-security` saved with `as:issue`,
  wait in `docs/issues/p1…p4-<slug>.md` → `as:fix` (list by priority, fixes the one you choose and deletes its file;
  larger ones get a proposal → `as:implement`) → `as:finish` → commit.
- **Health**: `as:health` (report and snapshot in `docs/health/`, fixes small items you pick, saves larger ones as
  issues) → the Known issues flow; the next `as:health` closes issues it no longer finds.
- **Parallel work**: `as:worktree-create <name>`, run any flow there in a new session, `as:worktree-close`.
- **Upkeep**: `as:docs-check` (docs and spec against the code, no writes), `as:spec-tests` (scenarios without tests).

Every step writes its state to files (proposal `## Plan` checklist, `docs/issues/`, `docs/health/*.json`), so each can
start in a new session.

### onboarding — once per repository

- `/as:init` — builds the `AGENTS.md` hierarchy, the Markdown spec for chosen modules, links between them, and checks the
  recommended plugins. Rerun parts later with `/as:agent-docs` and `/as:spec-docs`.

### plan — before non-trivial changes

- **`as:tech-lead`** starts on its own when you describe a feature, a bug or a design question (or call
  `/as:tech-lead <topic>`): it reads the code and spec first, asks targeted questions, compares 2–3 architectures,
  records the decision and proposed scenarios in `docs/spec/changes/<slug>.md`, saves the approved plan there as a checklist, and offers the
  next step — plan mode (large changes get milestones), or `/as:implement` in a new session. Small changes get a short
  plan without subagents or a proposal.
- **Plan mode** (Claude Code): press Shift+Tab until the mode indicator shows plan mode. Claude reads code, asks
  questions and proposes a plan without editing; you approve it or ask for changes, then it implements.
  Use it for multi-file changes, unclear requirements, and anything that changes a module's contract — ask Claude to
  read the module's spec page (linked from its `AGENTS.md`) while planning.
- **Larger features without `as:tech-lead`**: `/feature-dev:feature-dev <description>` — explores the codebase,
  designs the architecture, implements and reviews in guided phases.
- On Codex: ask for a plan first and say not to edit until you approve it.

### build — implementing

- `/as:implement` — continues the approved plan of the branch's change proposal, in this or a new session: tests
  first, ticks each step in `## Plan`, stops to ask when the plan does not fit the code.
- `/as:deliver docs/features/<slug>` — the whole roadmap unattended: plan, implement, finish and fix per phase,
  taking the recommended option where those skills would ask; local commits; stops at done criteria, human-only
  decisions or limits.
- Claude follows `AGENTS.md` and reads `.guidelines/` when the task touches their area — keep them current.
- UI work: `frontend-design` triggers on its own.
- Changing a module's observable behaviour: update its spec with `/as:spec-docs <module path>` and tag contract tests
  with scenario IDs.

### review — before committing and on the PR

- Default path: `/as:finish` (next section) — it runs simplify and review for you. The items below are for ad-hoc use.
- Ask Claude to run the `code-simplifier` agent on the recent changes.
- `/as:spec-tests` — which contract scenarios lack tests (unhappy paths first).
- Findings you do not fix now (from `/code-review`, `/claude-security` or your own review): `/as:issue` saves them to
  `docs/issues/`.
- Security-sensitive changes or a release: run `/claude-security` (or ask for a security scan).
- PR open: `/code-review:code-review`.

### finish — after delivering a feature

- `/as:finish` — on the branch's changes only: baseline tests, lint and build → simplify → review (you pick fixes) →
  one analysis per touched module → merge of the change proposal and spec check (intended change vs regression) → writes missing contract tests tagged with scenario
  IDs → refreshes `AGENTS.md`. Checks rerun after every code change; nothing is committed. Suggests `/claude-security`
  when the diff touches auth, input handling or data access.
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

- Periodically, or after larger refactors: `/as:docs-check` audits `AGENTS.md` and the spec against the code without
  writing; `/as:agent-docs` and `/as:spec-docs` apply the fixes (they ask before writing).
- Feature pages (`docs/features/`): `/as:feature docs/features/<slug>` with a new e-mail or document records it and
  what it changes; `as:finish` updates the roadmap when a phase's proposal is merged.

### health — once a sprint or month

- `/as:health` — whole-project check: hotspots (often changed and complex code), coupling and cycles, coverage and
  test quality (missing, excessive or weak tests), dead code, duplication, dependencies, docs drift. Writes
  `docs/health/<date>.html` and a `<date>.json` snapshot with trends against the previous run, then fixes the small
  items you pick.
- Larger findings you choose are saved to `docs/issues/` (with the finding's key, so the next run closes them when
  they are gone); `/as:fix` works through them.
- `/as:health --quick` for a fast pass (git and configured tools only).

### issues — known problems

- `docs/issues/p<1-4>-<slug>.md` — one file per known problem, priority in the name (`p1` data loss or security …
  `p4` clean-up), so `ls docs/issues` is the list. Written with your consent by `as:finish`, `as:health`,
  `as:spec-docs`, `as:tech-lead`, `as:implement`, `as:docs-check` and `as:spec-tests`.
- `/as:issue [description]` — saves a problem; without a description it collects the findings from the conversation
  (for example after `/code-review` or `/claude-security`) and asks which to save.
- `/as:fix` — lists open issues by priority and effort and recommends one; `/as:fix <slug>` or
  `/as:fix 10 most important bugs`. Small ones are fixed test-first and their file is deleted in the same diff;
  larger ones get a change proposal. Saying "fix the most important bugs" to `as:tech-lead` does the same.
