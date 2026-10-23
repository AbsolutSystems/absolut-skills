# Absolut Skills

A set of commands and skills for **Claude Code** and **Codex**, shipped as a single plugin `as`
from the `absolut-skills` marketplace.

| Host | Invocation |
|------|------------|
| Claude Code | `/as:<skill>` |
| Codex | `$as:<skill>` |

The skill catalogue lives in [`skills/README.md`](skills/README.md).

## Installation

Repository: <https://github.com/AbsolutSystems/absolut-skills>

### Claude Code

Inside Claude Code:

```text
/plugin marketplace add AbsolutSystems/absolut-skills
/plugin install as@absolut-skills
```

or from the shell:

```bash
claude plugin marketplace add AbsolutSystems/absolut-skills
claude plugin install as@absolut-skills
```

Restart the session, then check: `/as:help`. Update later with `/plugin marketplace update absolut-skills`.

### Codex

```bash
codex plugin marketplace add AbsolutSystems/absolut-skills
codex plugin add as@absolut-skills
```

Then check: `$as:help`. Update later with `codex plugin marketplace upgrade`.

### Local development

Point either host at a local clone instead of `AbsolutSystems/absolut-skills`, e.g.
`claude plugin marketplace add ./absolut-skills` or `codex plugin marketplace add ./absolut-skills`.

## Skills

### `help` — how to work with `as`

Confirms the plugin is installed, lists `as` skills, shows which recommended Anthropic plugins are installed
([`references/recommended-plugins.md`](references/recommended-plugins.md): `feature-dev`, `frontend-design`,
`code-simplifier`, `code-review`, `commit-commands`, `claude-security`), and walks through the workflow: onboarding,
planning in plan mode, building, review, commit, keeping docs true.

```text
/as:help                            # everything
/as:help plan                       # one topic: onboarding | plan | build | review | finish | commit | worktree | docs | health
```

### `tech-lead` — design partner (starts on its own)

The only `as` skill Claude may start by itself: when you want to discuss a feature, investigate a bug, or choose
between technical options. It behaves like a tech lead:

1. **Grounds** the topic in code, `AGENTS.md` and the spec (parallel exploration subagents) before asking anything.
2. **Clarifies** with targeted questions, and challenges the request when a smaller or existing solution fits.
3. **Compares** 2–3 architectures from parallel subagents (minimal change / clean boundaries / scale) and recommends one.
4. Records the **decision and proposed scenarios** in `docs/spec/changes/<slug>.md` — module pages keep describing
   current behaviour until `as:finish` merges the proposal and archives it in `docs/spec/changes/archive/` (decision log).
5. Writes the **plan** (steps, tests per scenario ID, risks), saves it as a checklist in the proposal's `## Plan`
   section (ticked as steps are done; `as:finish` checks it), and offers the **handoff**: implement directly (small),
   or switch to plan mode (medium; large gets milestones). It does not hand off to `/feature-dev:feature-dev`, which
   would redo the exploration and architecture already done.

It sizes the task first: a small change in one module gets one recommendation and a short plan, without subagents or
a change proposal.

Bugs follow their own path: reproduce, find the violated or missing scenario, verify hypotheses, root cause, then a
failing test first; after you approve the plan it implements the fix and suggests `/as:finish`. No production code is
written before you approve the plan.

```text
/as:tech-lead I want customers to cancel single items of an order
/as:tech-lead why are refunds sometimes doubled?
```

### `implement` — execute the approved plan

Continues the `## Plan` of the branch's change proposal in any session — also a new one, or with a cheaper model,
because the plan and scenarios live in the file, not in the conversation. For each unticked step: tests first for
`error` and `edge` scenarios (tagged with scenario IDs), code, checks, tick `- [x]`. When the plan turns out wrong, it
stops and proposes an edit to `## Plan` instead of improvising. Nothing is committed; then `/as:finish`.

```text
/as:implement                       # the proposal of this branch, first unticked step
/as:implement cancel-items --step 3
```

### `init` — onboard a repository

Runs `agent-docs`, then `spec-docs`, then links the spec from `AGENTS.md`, sharing one inventory and one round of
questions. Asks for approval before writing each part. On a brownfield project start with a spec for 2–3 central
modules and extend it later with `spec-docs`.

```text
/as:init                            # inventory, then asks which modules to specify
/as:init --spec backend/orders      # spec only for the given modules (or --spec all / --no-spec)
/as:init --check                    # audit both, write nothing
```

With your consent it adds a fixed **Working principles** block to the repo root `AGENTS.md` — rules that keep agents
from over-engineering (reuse before writing, no speculative abstractions, root-cause fixes, tests for non-trivial
logic, never cutting validation or security). The text lives in
[`skills/init/references/working-principles.md`](skills/init/references/working-principles.md) and is updated when its
version changes; declining leaves an `off` marker so you are not asked again; `agent-docs` keeps the block untouched.
Inspired by [ponytail](https://github.com/DietrichGebert/ponytail).

At the end it checks the recommended Anthropic plugins (see `help` below) and installs missing ones after you
agree; skip with `--no-plugins`.

Order matters: `agent-docs` settles apps, modules and boundaries cheaply; `spec-docs` reuses that and asks only about
behaviour; links are added once the spec pages exist.

### `finish` — wrap up a feature

The counterpart of `init`, run after delivering a feature and before the PR. Works only on what the branch changed.

```text
/as:finish                          # changes since the merge-base with the default branch
/as:finish develop                  # compare against another ref
/as:finish --no-tests               # skip steps: --no-simplify, --no-review, --no-tests, --no-docs
```

1. **Scope** — changed files → touched modules. 2. **Baseline checks** — tests, lint, type-check, build; stops if red.
3. **Simplify**, then tests. 4. **Review** — findings Must / Should / Nice, you pick fixes, then tests.
5. **Analysis** — one read-only subagent per touched module reports only what the diff changed: proposal status, spec
drift, new behaviour, its tests, stale docs.
6. **Spec** — merges the branch's change proposal (plan, scenarios, `Verify`, IDs still free on the default branch),
then drift in touched modules: intended (spec updated) or regression (fixed as a bug).
7. **Contract tests** — writes tests for uncovered scenarios, tagged with scenario IDs.
8. **Agent docs** — refreshes `AGENTS.md` for touched directories. 9. **Summary** — nothing is committed; suggests
`/commit-commands:commit-push-pr`, and `/claude-security` when the diff touches security-sensitive code.

Simplify runs before review so the review sees the code that ships. In Claude Code it uses the built-in `/simplify`
and `/code-review` (local diff, not the `code-review` plugin's PR review) when the version has them; elsewhere the criteria in `skills/finish/references/review.md`.

### `health` — periodic project health check

Looks at the whole project, not one branch: where the code is complex *and* often changed (hotspots — the best
review and refactoring candidates), how modules are coupled (cycles, hidden change coupling from git history), where
tests are missing and where there are too many or weak ones, dead code, duplication, vulnerable or outdated
dependencies, and docs drift.

```text
/as:health                          # full check, report, then fix the small items you pick
/as:health --quick                  # git + already configured tools only
/as:health backend --since "6 months"
/as:health --no-fix                 # report only
```

Tools: first what the project already has (JaCoCo, ArchUnit, dependency-cruiser, knip, …); missing ones run once
without being added to the project (`uvx lizard`, `npx madge`, `npx jscpd`, osv-scanner, …) only with your consent;
git history and code reading always (churn, change coupling and frequently fixed tests are computed by
`skills/health/scripts/git_signals.py`). The report goes to `docs/health/<date>.html` with a `<date>.json` snapshot, so
the next run shows what improved or got worse. Small findings are fixed with tests before and after; tests are
removed only with per-test consent; larger findings become task briefs for plan mode or `/feature-dev:feature-dev`.

### `worktree-create` / `worktree-close` — parallel branches in git worktrees

Work on several branches at once, each in its own folder next to the repository (`../<repo>-worktrees/<name>`).

```text
/as:worktree-create feature-x               # new branch feature-x from the current branch
/as:worktree-create feature-x from develop  # ... from develop (local, or origin/develop)
/as:worktree-close feature-x                # close by branch or folder name
/as:worktree-close                          # close the worktree you are in
```

`worktree-create` stops if the branch is already checked out elsewhere, asks before reusing an existing branch, and
offers to copy ignored `.env*` files (also from app directories) from the main worktree and to install dependencies.
`worktree-close` offers to commit uncommitted changes,
shows unpushed commits and ignored files that will be deleted, and after your confirmation runs `git worktree remove`
(never `--force`). The branch is never deleted.

### `agent-docs` — documentation tree for coding agents

Builds and keeps up to date the smallest set of docs that changes what an agent does: commands, rules the code does not
enforce, target vs legacy conventions, internal libraries and pitfalls. It does not describe the code (stack, public API,
dependencies): agents read that themselves, and context files that repeat the repository make agents explore more and
cost more without solving more tasks ([Gloaguen et al., 2026](https://arxiv.org/abs/2602.11988)). Each line must pass
the **line test**: without it, an agent would do something wrong or have to guess. The code analysis mainly produces
questions for the team — their answers are the valuable part.

```text
/as:agent-docs                      # whole repository: analyse, ask, report, write after approval
/as:agent-docs --check              # audit only: report, questions and recommendations, no writes
/as:agent-docs backend              # limit the run to one subtree
/as:agent-docs --depth 3            # deepest directory level that may get its own AGENTS.md (default 4)
```

In Codex use `$as:agent-docs` with the same arguments.

Resulting layout (example monorepo):

```text
AGENTS.md                           # one sentence + map: backend/, frontend/, ... + repo-wide commands
CLAUDE.md                           # @AGENTS.md
backend/AGENTS.md                   # commands, unenforced rules, internal libraries (e.g. preboot), pitfalls, spec links, guideline index
backend/CLAUDE.md                   # @AGENTS.md
backend/.guidelines/                # only rules the team confirmed or a tool enforces
  testing-guideline.md              # what a feature ships with, which test level for what, helpers to use
  architecture-guideline.md         # where new code goes, allowed communication
backend/src/.../modules/orders/AGENTS.md   # only because it has pitfalls or rules
frontend/AGENTS.md
...
```

How a run works:

1. **Inventory** — classifies directories (repo root / app root / module / skip) and shows the planned tree.
2. **Analysis** — read-only subagents, bottom-up (modules → apps → repo root); each reports what an agent would get
   wrong (conflicts, unenforced rules, pitfalls, missing commands) with evidence, lines to prune, drift, open questions
   and recommendations.
3. **Questions** — asks you about what code cannot tell (role of an internal library, conflicting conventions,
   unclear or legacy directories, testing strategy).
4. **Report** — one row per file: `NEW` / `UPDATE` (with drift list) / `PRUNE` / `OK` / `STALE` / `MIGRATE`, plus
   recommendations that would make an agent more effective (missing scripts, env docs, reference examples…).
5. **Write** (after your approval) — minimal edits that keep hand-written sections; never deletes files without consent.
6. **Verify** — every referenced path and command exists; guideline indexes match `.guidelines/`.

Generated docs are in English. `.guidelines/` files are referenced from the app `AGENTS.md`, not `@`-imported, so they
do not fill the context until the agent needs them. Review the result with `git diff`; re-running should report `OK`.

### `spec-docs` — Markdown specification of module contracts

Builds a specification for people, not agents: what the system does, what each application is for, and what each
module promises to the rest of the application — requirements with Given/When/Then scenarios for happy, error and edge
paths. Scenario IDs (e.g. `ORD-003`) are stable, so tests can refer to them.

```text
/as:spec-docs                       # analyse, ask, report, write docs/spec/ after approval
/as:spec-docs --check               # audit only: drift between spec and code, no writes
/as:spec-docs --tests               # coverage report: which scenarios are verified by tests (COVERED / PARTIAL / MISSING)
/as:spec-docs --lang pl             # page content in Polish (default English)
/as:spec-docs backend               # limit the run to one subtree
```

Resulting layout:

```text
docs/spec/
  index.md                          # system: purpose, actors, apps/modules, main flows
  backend/index.md                  # app: modules and cross-module flows (monorepo only)
  backend/orders.md                 # module contract: operations, requirements, scenarios, rules, dependencies
```

Pages are Markdown formatted for people: breadcrumbs, a one-line purpose, a table of contents, requirements as quoted
SHALL sentences, scenarios marked ✅ happy / ❌ error / ⚠️ edge with Given/When/Then lists, open questions as callouts.
They read well on GitHub/GitLab, in an IDE preview and in a diff. A spec written by an earlier version as HTML is
converted to Markdown on the next run (content and IDs unchanged, links from `AGENTS.md` updated). To make `--tests` mapping deterministic, put the
scenario ID in contract test names or tags (e.g. `@Tag("ORD-003")`, `it("ORD-003 rejects out-of-stock order")`).

`skills/spec-docs/scripts/spec_lint.py` (Python, no dependencies) checks the spec mechanically: unique and well-formed
IDs, no ID reserved twice by parallel branches (`--against origin/HEAD`), resolving links and anchors, no leftover
HTML. Copy it into the repository and run it in CI to keep the spec consistent without an agent.

When `docs/spec/` exists, `agent-docs` links it from the repo `AGENTS.md` and lists the module pages in each app
`AGENTS.md` (links, not `@` imports), so an agent knows a module's contract before changing its behaviour. Run
`agent-docs` after `spec-docs` creates new pages.

## Structure

```text
.claude-plugin/plugin.json        # Claude Code manifest (name "as")
.claude-plugin/marketplace.json   # Claude Code marketplace "absolut-skills"
.codex-plugin/plugin.json         # Codex manifest (name "as", skills ./skills/)
.agents/plugins/marketplace.json  # Codex marketplace "absolut-skills"
skills/<name>/SKILL.md            # skill (= command) — shared by both hosts
skills/<name>/agents/openai.yaml  # Codex metadata for the skill
skills/<name>/scripts/            # stdlib-only helpers for deterministic work (optional)
references/                       # host-specific notes
tools/validate.py                 # format validation
tests/                            # tests of the validator and the scripts
```

## Adding a skill / command

1. Copy `skills/help/` to `skills/<new-name>/` (lowercase kebab-case) and replace its body.
2. In `SKILL.md`, set `name: <new-name>` and a specific `description` (when to use it, ≤1024 characters).
   For a command the user invokes explicitly, add `disable-model-invocation: true`.
3. In `agents/openai.yaml`, set `display_name`, `short_description`, `default_prompt` (`$as:<new-name> ...`);
   for an explicit-only command, set `policy.allow_implicit_invocation: false`.
4. Add a row to [`skills/README.md`](skills/README.md).
5. Run the validation.

## Validation

```bash
python3 tools/validate.py              # manifests, frontmatter, openai.yaml, links
uv run --with pytest pytest tests      # validator and script tests
claude plugin validate .               # optional: official Claude Code check
```
