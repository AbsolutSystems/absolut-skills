# Absolut Skills — catalogue

| Skill | Claude Code | Codex | Purpose |
|-------|-------------|-------|---------|
| `help` | `/as:help` | `$as:help` | Installation check, recommended plugins status, the flows (client request estimate, feature, bug, known issues, health), and how to work with `as`, Anthropic plugins and plan mode |
| `tech-lead` | `/as:tech-lead` | `$as:tech-lead` | Design partner (auto-invoked): grounds features and bugs in code and spec, compares architectures, writes a change proposal with the plan as a checklist, hands off to plan mode; `docs/estimates/<slug>` plans an accepted estimate |
| `estimate` | `/as:estimate` | `$as:estimate` | Client feature request → analysis partner: grounds it in code, flags gaps, conflicts and better alternatives, prices a step plan in hours (min / likely / max) and writes an internal analysis plus a client document (PRD, estimate, questions, suggestions) to `docs/estimates/<slug>/` |
| `feature` | `/as:feature` | `$as:feature` | Living feature docs in `docs/features/<slug>/`: why, acceptance criteria linked to module scenarios, roadmap of phases (one proposal each), decisions, and sources kept verbatim (PDF, spreadsheets, e-mails); seeds from an estimate, maps legacy folders |
| `implement` | `/as:implement` | `$as:implement` | Executes the approved `## Plan` of the branch's change proposal step by step in any session: tests first, tick, stop on deviations |
| `deliver` | `/as:deliver` | `$as:deliver` | A documented feature, or the saved issues (`docs/issues [request]`), delivered unattended (e.g. overnight): start-up questions, then a loop of `tech-lead` → `implement` → `finish` → `fix` per phase or issue and a final review, taking the recommended option at every question; local commits per stage, stops at done criteria, human-only decisions or limits (an issues run skips a blocked issue and goes on); report in `delivery.md` or `docs/deliveries/` |
| `init` | `/as:init` | `$as:init` | Onboard a repo: `agent-docs`, then `spec-docs` for a chosen scope, then links between them |
| `finish` | `/as:finish` | `$as:finish` | Wrap up a feature: simplify, review, spec drift check, missing contract tests, docs refresh — for the branch's changes |
| `issue` | `/as:issue` | `$as:issue` | Save known problems (described, or found earlier in the conversation, e.g. by `/code-review`) to `docs/issues/p<1-4>-<slug>.md` with evidence |
| `fix` | `/as:fix` | `$as:fix` | Work through `docs/issues/` by priority: re-check, fix test-first and delete the issue, or plan larger ones as a proposal |
| `health` | `/as:health` | `$as:health` | Periodic project health: hotspots, coupling, coverage and test quality, dead code, deps, docs drift; report with trends in `docs/health/`; larger findings go to `docs/issues/` |
| `worktree-create` | `/as:worktree-create` | `$as:worktree-create` | New branch and git worktree in `../<repo>-worktrees/<name>`, from the current branch or `from <branch>`; optionally copies `.env*` and installs dependencies |
| `worktree-close` | `/as:worktree-close` | `$as:worktree-close` | Offers to commit leftovers, then removes the worktree folder; the branch stays |
| `docs-check` | `/as:docs-check` | `$as:docs-check` | Audit agent docs and the spec against the code without writing; offers to save problems as issues |
| `agent-docs` | `/as:agent-docs` | `$as:agent-docs` | Build and update minimal `AGENTS.md`/`CLAUDE.md` docs and `.guidelines/` holding only what the code cannot tell; prunes the rest |
| `spec-docs` | `/as:spec-docs` | `$as:spec-docs` | Human-readable Markdown spec of module contracts (scenarios with stable IDs) in `docs/spec/`; bugs go to `docs/issues/` |
| `spec-tests` | `/as:spec-tests` | `$as:spec-tests` | Which spec scenarios are verified by tests (`COVERED` / `PARTIAL` / `MISSING`) |
| `qa-docs` | `/as:qa-docs` | `$as:qa-docs` | What browser QA checks, in `docs/qa/`: environments, test accounts, roles, app-wide UI rules and cross-feature journeys `J<n>`; reports drift, outdated journeys and the last result per criterion and journey |
| `qa` | `/as:qa` | `$as:qa` | Checks the running web app in a browser: feature criteria and journeys (or what the branch touches) clicked by an executor subagent per scenario, screenshots judged by a separate agent, report in `docs/qa/runs/`, failures offered as issues; `explore <area>` tries to break one area |

Every skill lives in `skills/<name>/`:

- `SKILL.md` — frontmatter (`name` = directory name, `description`) plus host-agnostic instructions.
- `agents/openai.yaml` — Codex interface (display name, short description, default prompt) and invocation policy.

`tech-lead` is the only skill the model may invoke on its own; keep its `description` narrow so it does not trigger on
small edits.

A command-like skill, one the user invokes explicitly and the model should not trigger on its own, sets
`disable-model-invocation: true` in `SKILL.md` and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.
