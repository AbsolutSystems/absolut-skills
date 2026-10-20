# Absolut Skills — catalogue

| Skill | Claude Code | Codex | Purpose |
|-------|-------------|-------|---------|
| `help` | `/as:help` | `$as:help` | Installation check, recommended plugins status, and how to work with `as`, Anthropic plugins and plan mode |
| `tech-lead` | `/as:tech-lead` | `$as:tech-lead` | Design partner (auto-invoked): grounds features and bugs in code and spec, compares architectures, writes a change proposal and plan, hands off to plan mode |
| `init` | `/as:init` | `$as:init` | Onboard a repo: `agent-docs`, then `spec-docs` for a chosen scope, then links between them |
| `finish` | `/as:finish` | `$as:finish` | Wrap up a feature: simplify, review, spec drift check, missing contract tests, docs refresh — for the branch's changes |
| `health` | `/as:health` | `$as:health` | Periodic project health: hotspots, coupling, coverage and test quality, dead code, deps, docs drift; report with trends in `docs/health/` |
| `worktree-create` | `/as:worktree-create` | `$as:worktree-create` | New branch and git worktree in `../<repo>-worktrees/<name>`, from the current branch or `from <branch>`; optionally copies `.env*` |
| `worktree-close` | `/as:worktree-close` | `$as:worktree-close` | Offers to commit leftovers, then removes the worktree folder; the branch stays |
| `agent-docs` | `/as:agent-docs` | `$as:agent-docs` | Build and audit minimal `AGENTS.md`/`CLAUDE.md` docs and `.guidelines/` holding only what the code cannot tell; prunes the rest |
| `spec-docs` | `/as:spec-docs` | `$as:spec-docs` | Human-readable Markdown spec of module contracts (scenarios with stable IDs) in `docs/spec/`, plus scenario test coverage report |

Every skill lives in `skills/<name>/`:

- `SKILL.md` — frontmatter (`name` = directory name, `description`) plus host-agnostic instructions.
- `agents/openai.yaml` — Codex interface (display name, short description, default prompt) and invocation policy.

`tech-lead` is the only skill the model may invoke on its own; keep its `description` narrow so it does not trigger on
small edits.

A command-like skill, one the user invokes explicitly and the model should not trigger on its own, sets
`disable-model-invocation: true` in `SKILL.md` and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.
