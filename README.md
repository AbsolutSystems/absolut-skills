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
/as:help plan                       # one topic: onboarding | plan | build | review | commit | docs
```

### `tech-lead` — design partner (starts on its own)

The only `as` skill Claude may start by itself: when you want to discuss a feature, investigate a bug, or choose
between technical options. It behaves like a tech lead:

1. **Grounds** the topic in code, `AGENTS.md` and the spec (parallel exploration subagents) before asking anything.
2. **Clarifies** with targeted questions, and challenges the request when a smaller or existing solution fits.
3. **Compares** 2–3 architectures from parallel subagents (minimal change / clean boundaries / scale) and recommends one.
4. Records the **decision and proposed scenarios** in `docs/spec/changes/<slug>.html` — module pages keep describing
   current behaviour until `as:finish` merges the proposal and archives it in `docs/spec/changes/archive/` (decision log).
5. Writes the **plan** (steps, tests per scenario ID, risks) and offers the **handoff**: implement directly (small),
   switch to plan mode (medium), or launch `/feature-dev:feature-dev` with the agreed brief (large).

Bugs follow their own path: reproduce, find the violated or missing scenario, verify hypotheses, root cause, then a
failing test first. No production code is written before you approve the plan.

```text
/as:tech-lead I want customers to cancel single items of an order
/as:tech-lead why are refunds sometimes doubled?
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

1. **Scope** — changed files → touched modules. 2. **Baseline tests** — stops if red.
3. **Simplify**, then tests. 4. **Review** — findings Must / Should / Nice, you pick fixes, then tests.
5. **Spec** — drift in touched modules: intended (spec updated) or regression (fixed as a bug).
6. **Contract tests** — writes tests for uncovered scenarios, tagged with scenario IDs.
7. **Agent docs** — refreshes `AGENTS.md` for touched directories. 8. **Summary** — nothing is committed; suggests
`/commit-commands:commit-push-pr`.

Simplify runs before review so the review sees the code that ships. In Claude Code it uses the built-in `/simplify`
and `/code-review`; elsewhere the criteria in `skills/finish/references/review.md`.

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
git history and code reading always. The report goes to `docs/health/<date>.html` with a `<date>.json` snapshot, so
the next run shows what improved or got worse. Small findings are fixed with tests before and after; tests are
removed only with per-test consent; larger findings become task briefs for plan mode or `/feature-dev:feature-dev`.

### `agent-docs` — documentation tree for coding agents

Builds and keeps up to date a hierarchical set of docs that an agent reads progressively: a short overview at the repo
root, more detail inside each application and module, and detailed rules in `.guidelines/` loaded only when needed.

```text
/as:agent-docs                      # whole repository: analyse, ask, report, write after approval
/as:agent-docs --check              # audit only: report, questions and recommendations, no writes
/as:agent-docs backend              # limit the run to one subtree
/as:agent-docs --depth 3            # deepest directory level that may get its own AGENTS.md (default 4)
```

In Codex use `$as:agent-docs` with the same arguments.

Resulting layout (example monorepo):

```text
AGENTS.md                           # what the project is + map: backend/, frontend/, ...
CLAUDE.md                           # @AGENTS.md
backend/AGENTS.md                   # purpose, stack, architecture (where modules live), key libraries, commands, guideline index
backend/CLAUDE.md                   # @AGENTS.md
backend/.guidelines/
  testing-guideline.md              # test levels, frameworks, data setup, how to run a single test
  libraries-guideline.md            # internal libraries (e.g. preboot) first, preferred choices
  architecture-guideline.md         # module boundaries, allowed dependencies, where new code goes
  code-style-guideline.md           # naming, error handling, logging, mapping
backend/src/.../modules/orders/AGENTS.md   # responsibility, public API, dependencies, pitfalls
frontend/AGENTS.md
...
```

How a run works:

1. **Inventory** — classifies directories (repo root / app root / module / skip) and shows the planned tree.
2. **Analysis** — read-only subagents, bottom-up (modules → apps → repo root); each reports facts with evidence,
   drift in existing docs, open questions and recommendations.
3. **Questions** — asks you about what code cannot tell (role of an internal library, conflicting conventions,
   unclear or legacy directories, testing strategy).
4. **Report** — one row per file: `NEW` / `UPDATE` (with drift list) / `OK` / `STALE` / `MIGRATE`, plus
   recommendations that would make an agent more effective (missing scripts, env docs, reference examples…).
5. **Write** (after your approval) — minimal edits that keep hand-written sections; never deletes files without consent.
6. **Verify** — every referenced path and command exists; guideline indexes match `.guidelines/`.

Generated docs are in English. `.guidelines/` files are referenced from the app `AGENTS.md`, not `@`-imported, so they
do not fill the context until the agent needs them. Review the result with `git diff`; re-running should report `OK`.

### `spec-docs` — HTML specification of module contracts

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
  spec.css                          # one shared stylesheet, copied from the skill
  index.html                        # system: purpose, actors, apps/modules, main flows
  backend/index.html                # app: modules and cross-module flows (monorepo only)
  backend/orders.html               # module contract: operations, requirements, scenarios, rules, dependencies
```

Pages contain content only — no inline styles or scripts — so an agent updating them does not spend tokens on
styling. Open `docs/spec/index.html` in a browser; it also prints well. To make `--tests` mapping deterministic, put the
scenario ID in contract test names or tags (e.g. `@Tag("ORD-003")`, `it("ORD-003 rejects out-of-stock order")`).

When `docs/spec/` exists, `agent-docs` adds a one-line "Specification" link to the repo, app and module `AGENTS.md`
files (a link, not an `@` import), so an agent knows the module's contract before changing its behaviour. Run
`agent-docs` after `spec-docs` creates new pages.

## Structure

```text
.claude-plugin/plugin.json        # Claude Code manifest (name "as")
.claude-plugin/marketplace.json   # Claude Code marketplace "absolut-skills"
.codex-plugin/plugin.json         # Codex manifest (name "as", skills ./skills/)
.agents/plugins/marketplace.json  # Codex marketplace "absolut-skills"
skills/<name>/SKILL.md            # skill (= command) — shared by both hosts
skills/<name>/agents/openai.yaml  # Codex metadata for the skill
references/                       # host-specific notes
tools/validate.py                 # format validation
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
uv run --with pytest pytest tests      # validator tests
claude plugin validate .               # optional: official Claude Code check
```
