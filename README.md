# Absolut Skills

A workflow for **Claude Code** and **Codex**: commands that take a change from idea to merged PR — design with a
tech lead, a plan saved in the repository, step-by-step implementation, a finishing pass that keeps the spec and docs
true — plus periodic health checks that feed the next round of fixes. Shipped as one plugin, `as`, from the
`absolut-skills` marketplace.

| Host | Invocation |
|------|------------|
| Claude Code | `/as:<skill>` |
| Codex | `$as:<skill>` |

Examples below use the Claude Code syntax; in Codex replace `/as:` with `$as:`. Not sure where to start? Run
`/as:help` (or `/as:help flows`).

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

## Which command when

| I want to… | Command |
|------------|---------|
| start with a repository (agent docs, spec, plugins) | `/as:init` |
| design a feature, investigate a bug, choose between options | `/as:tech-lead` (also starts on its own) |
| analyse and price a client's feature request | `/as:estimate` |
| keep a feature's why, acceptance criteria, roadmap and sources (PDF, e-mails) in one place | `/as:feature` |
| continue an approved plan, also in a new session | `/as:implement` |
| deliver a whole documented feature, or fix all saved problems, unattended (e.g. overnight) | `/as:deliver` |
| wrap up a feature before the PR (simplify, review, spec, tests, docs) | `/as:finish` |
| save a problem to fix later (also findings of `/code-review`) | `/as:issue` |
| fix the saved problems, most important first | `/as:fix` |
| check whether agent docs and spec still match the code (no writes) | `/as:docs-check` |
| update agent docs / the spec | `/as:agent-docs` / `/as:spec-docs` |
| see which spec scenarios have no tests | `/as:spec-tests` |
| review the health of the whole project | `/as:health` |
| work on several branches at once | `/as:worktree-create` / `/as:worktree-close` |
| learn how it all fits together | `/as:help flows` |

## How to work with `as`

Three ideas run through every command:

- **State lives in files, not in the conversation.** A plan is a checklist in `docs/spec/changes/<slug>.md`, a known
  problem is a file in `docs/issues/`, a health check is a snapshot in `docs/health/<date>.json`. Any step can continue in a new session or with a cheaper model.
- **Nothing is written to code before you approve a plan**, and nothing is committed by `as` — you commit at the end.
  The one exception is `as:deliver`: you hand it a whole feature or the saved issues, it decides as you would by the recommended options,
  commits each green stage locally and leaves the review (and the push) to you.
- **Docs follow the code.** `AGENTS.md` tells agents what the code cannot; `docs/spec/` describes module contracts as
  scenarios with stable IDs (`ORD-003`) that tests refer to; `docs/features/` keeps each feature's why, acceptance
  criteria and roadmap across many changes. `as:finish` keeps them current.

### 1. Onboard a repository (once)

```text
/as:init                            # AGENTS.md tree, spec for chosen modules, links, recommended plugins
```

On a large project specify 2–3 central modules first and add more later with `/as:spec-docs <path>`.

### 2. Feature or change

```text
/as:tech-lead I want customers to cancel single items of an order
    → grounds in code and spec, asks, compares options, writes docs/spec/changes/cancel-items.md with ## Plan
    → implements a small change after approval, or hands off to plan mode
/as:implement                       # (new session) continues the first unticked step of the plan
/as:finish                          # simplify, review, merge the proposal into the spec, missing tests, docs
/commit-commands:commit-push-pr     # commit, push, open the PR
```

`as:tech-lead` also starts on its own when you describe a feature or ask "how should we…". A small change in one
module gets a short plan without a proposal.

### 3. Client feature request to estimate

```text
/as:estimate docs/requests/cancel-items.md     # or paste the client's e-mail after the command
    → reads the request, grounds it in code and spec, flags gaps, conflicts and better alternatives
    → step plan priced min / likely / max h (developer who knows the code + AI agent)
    → docs/estimates/cancel-items/analysis.md (internal) and client.md (PRD, estimate, questions, suggestions)
/as:estimate docs/estimates/cancel-items       # revision with the client's answers
/as:tech-lead docs/estimates/cancel-items      # accepted: plan from the analysis, then the feature flow
```

### 4. Feature documentation and roadmap

```text
/as:feature cancel single items — order in the attached PDF, e-mail below   # or docs/estimates/<slug>, or a legacy folder
    → saves the sources verbatim in docs/features/cancel-items/sources/ (PDF, .xlsx + its text, pasted e-mails)
    → docs/features/cancel-items/index.md: why, acceptance criteria linked to module scenarios, phases, decisions
/as:tech-lead docs/features/cancel-items       # plans the next phase as a change proposal → the feature flow
/as:feature docs/features/cancel-items         # a new e-mail or document: records it and what it changes
```

`as:finish` marks the phase done on the feature page; "read `docs/features/<slug>/index.md`" is the briefing for any
later session.

Or let `/as:deliver docs/features/cancel-items` run the whole roadmap unattended (see [`deliver`](#deliver--a-whole-feature-or-all-issues-unattended)).

### 5. Bug

```text
/as:tech-lead why are refunds sometimes doubled?
    → reproduces, finds the violated or missing scenario, verifies hypotheses, root cause
    → failing test first, then the fix after you approve the plan (or saved to docs/issues/ if you defer it)
/as:finish
```

### 6. Known issues

```text
/as:issue                           # after /code-review, /claude-security or a review: save the findings you defer
/as:fix                             # open issues by priority, recommends one, fixes it and deletes its file
/as:fix 10 most important bugs      # ... or a selection, one by one; larger ones get a proposal → /as:implement
```

Every skill that finds a problem it does not fix now (`finish` review, `health`, `spec-docs` "rule or bug?",
`tech-lead` bug, `implement`) offers to save it as `docs/issues/p<1-4>-<slug>.md` — priority in the file name, so
`ls docs/issues` is the list. Fixed means deleted, in the same diff as the fix.

### 7. Health check (once a sprint or month)

```text
/as:health                          # report + snapshot in docs/health/, fixes the small (S) items you pick,
                                    # saves the larger ones you choose to docs/issues/
/as:fix                             # later: the Known issues flow
```

An issue from health keeps the finding's key, so the next `/as:health` shows it as tracked and closes it once the
finding is gone.

### 8. Parallel work

```text
/as:worktree-create feature-x       # new branch + folder ../<repo>-worktrees/feature-x; open a new session there
/as:worktree-close feature-x        # offers to commit leftovers, removes the folder, keeps the branch
```

### 9. Keeping docs true

```text
/as:docs-check                      # audit AGENTS.md, .guidelines and the spec against the code, no writes
/as:agent-docs                      # apply: refresh AGENTS.md / .guidelines (asks before writing)
/as:spec-docs                       # apply: refresh the spec (asks before writing)
/as:spec-tests                      # which scenarios have no tests
```

### Plan mode and other plugins

In Claude Code, `as:tech-lead` hands medium and large changes to **plan mode** (Shift+Tab): Claude plans without
editing and implements after you approve. In Codex, ask for a plan and say not to edit until you approve it.
`as` works with the recommended Anthropic plugins (`/as:help` shows which are installed): `commit-commands` for commits
and PRs, `code-review` on an open PR, `claude-security` for security-sensitive changes, `frontend-design` for UI.

### What gets written where

| Path | Written by | Contents |
|------|------------|----------|
| `AGENTS.md`, `CLAUDE.md`, `.guidelines/` | `init`, `agent-docs`, `finish` | What agents must know that the code does not say |
| `docs/spec/**/*.md` | `init`, `spec-docs`, `finish` | Module contracts: requirements and scenarios with IDs |
| `docs/spec/changes/<slug>.md` | `tech-lead`, `implement` (ticks) | Open change proposal: decision, scenarios, `## Plan` |
| `docs/spec/changes/archive/` | `finish` | Merged proposals — the decision log |
| `docs/features/<slug>/` | `feature`; phase status by `tech-lead`, `finish`; `delivery.md` by `deliver` | Feature page (why, acceptance criteria, roadmap, decisions) and `sources/` kept verbatim |
| `docs/estimates/<slug>/` | `estimate` | Client request analysis and hour estimate: `analysis.md` (internal), `client.md` (to send) |
| `docs/deliveries/<branch>.md` | `deliver` | Report of an unattended issues run |
| `docs/issues/p<1-4>-<slug>.md` | `issue`, `finish`, `health`, `spec-docs`, `tech-lead`, `implement`, `docs-check`, `spec-tests`; deleted by `fix`, `finish`, `health`, `deliver` | Known problems not fixed yet, one file each, priority in the name |
| `docs/health/` | `health` | Dated HTML reports, JSON snapshots, index with trends |

## Commands

| Command | Arguments | When |
|---------|-----------|------|
| `/as:help` | `[which\|flows\|onboarding\|plan\|build\|review\|finish\|commit\|worktree\|docs\|health\|issues]` | How to work with `as`, installed plugins |
| `/as:init` | `[path] [--spec <path>… \| all] [--no-spec] [--lang en\|pl]` | Once per repository |
| `/as:tech-lead` | `<feature, bug or question>` \| `docs/estimates/<slug>` \| `docs/features/<slug>` | Before any non-trivial change |
| `/as:estimate` | `<request text or file> [--lang en\|pl]` \| `docs/estimates/<slug>` | Client asks for a feature quote; revision after answers |
| `/as:feature` | `<description, files>` \| `docs/features/<slug>` \| `docs/estimates/<slug>` \| `<legacy folder>` `[--lang en\|pl]` | A feature spanning several changes, or new client material |
| `/as:implement` | `[slug] [--step <n>]` | Execute an approved plan, in any session |
| `/as:deliver` | `docs/features/<slug>` \| `docs/issues [request]` `[--max-stages <n>]` | A documented feature or the saved issues, delivered unattended |
| `/as:finish` | `[base] [--no-simplify] [--no-review] [--no-tests] [--no-docs]` | Feature done, before the PR |
| `/as:issue` | `[problem description]` | Save a problem you will not fix now |
| `/as:fix` | `[slug or request]` | Work through `docs/issues/`, most important first |
| `/as:health` | `[path] [--quick] [--since <period>]` | Once a sprint or month |
| `/as:worktree-create` | `<name> [from <branch>]` | Start parallel work |
| `/as:worktree-close` | `[<name>]` | Parallel work done |
| `/as:docs-check` | `[path]` | Audit agent docs and spec, no writes |
| `/as:agent-docs` | `[path] [--depth <n>]` | Agent docs refresh |
| `/as:spec-docs` | `[path] [--lang en\|pl]` | Spec refresh |
| `/as:spec-tests` | `[path]` | Scenario test coverage |

## Skills in detail

### `help` — how to work with `as`

Confirms the plugin is installed, lists `as` skills, shows which recommended Anthropic plugins are installed
([`references/recommended-plugins.md`](references/recommended-plugins.md): `feature-dev`, `frontend-design`,
`code-simplifier`, `code-review`, `commit-commands`, `claude-security`), and walks through the workflow: onboarding,
planning in plan mode, building, review, commit, keeping docs true, and how the commands chain into flows.

```text
/as:help                            # everything
/as:help flows                      # one topic: which | flows | onboarding | plan | build | review | finish | commit | worktree | docs | health | issues
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
failing test first; after you approve the plan it implements the fix and suggests `/as:finish`. A bug you defer is
saved to `docs/issues/` with its root cause. No production code is written before you approve the plan.

With `docs/estimates/<slug>` it plans a client-accepted `as:estimate` from its analysis: re-checks the listed code,
asks only the open client questions, and starts from the estimate's steps, warning when the plan exceeds its `max`.

Asked to fix known problems ("fix the most important bugs"), it follows `as:fix` over `docs/issues/`.

```text
/as:tech-lead I want customers to cancel single items of an order
/as:tech-lead why are refunds sometimes doubled?
```

### `issue` and `fix` — known problems

`docs/issues/` is a small file-based tracker: one Markdown file per problem not fixed yet, named
`p<1-4>-<slug>.md` — `p1` data loss, security or a blocker, `p2` a broken main flow, `p3` an edge case or a
workaround exists, `p4` clean-up — with kind, effort, evidence (file, `Class.method` and a code excerpt — no line numbers) and a suggested fix
([format](skills/issue/references/issue-format.md)). Every skill that finds a problem it does not fix now offers to
save it there; `issue` saves the ones found elsewhere.

```text
/as:issue                           # collect the findings of /code-review, /claude-security or a review, pick what to save
/as:issue cooldown starts on a failed refresh   # one problem in your words
/as:fix                             # open issues by priority and effort, recommends one
/as:fix exhaustion-divides-by-zero  # one issue by slug or title words
/as:fix 10 most important bugs      # a selection, fixed one by one
```

`fix` re-checks each issue's evidence against the current code (gone → offers to delete the file), fixes small ones
test-first after you approve the plan and deletes the issue file in the same diff, and turns larger ones into a change
proposal (`**Issue:** <slug>` in its meta line) for `/as:implement`; `/as:finish` deletes the issue when it archives
that proposal. Refactors keep behaviour (tests pin it first); removing tests needs per-test consent.

### `estimate` — client feature request analysis and hour estimate

Your analyst partner for a client's feature request. It reads the request (text, e-mail or file), grounds each
requirement in the code and spec, and reviews the request for gaps (error cases, permissions, existing data,
notifications…), conflicts with current behaviour, smaller or better alternatives and worthwhile additions. Then it
breaks the work into steps — a plan, not code — priced `min / likely / max` hours for a developer who knows the code
and works with an AI coding agent, including tests and communication. Totals and expected values (PERT, rounded up to
0.5 h) come from a script, not the model's arithmetic.

It writes two files after your approval: `docs/estimates/<slug>/analysis.md` (requirements, impact with paths,
findings, assumptions, step estimate, risks) and `client.md` in the client's language (PRD, estimate per block,
assumptions, questions, suggestions priced separately, what is not included). Run it again on the folder with the
client's answers for a new revision; after acceptance, `as:tech-lead docs/estimates/<slug>` plans the implementation
from the analysis instead of exploring again.

```text
/as:estimate <pasted request or path>
/as:estimate docs/estimates/cancel-items       # revision after the client's answers
```

### `feature` — living feature documentation

One folder per feature, `docs/features/<slug>/`: `index.md` is the page you (or an agent) read first — why, users and
goals, non-goals, acceptance criteria (`AC1…`) linked to the module scenarios that realise them, a roadmap of phases
(each one change proposal), decisions and a list of sources; `sources/` keeps the material verbatim — the client's
PDF, spreadsheets (with their text extracted by a script), pasted e-mails and meeting notes. The page is a
distillate: every criterion and decision links its source, so a later e-mail that changes something is recorded as a
decision, not lost.

It starts from a description with files or pasted text, from an accepted estimate, from an existing feature (rebuilt
from the code and archived proposals), or from a legacy documentation folder (each file mapped to a feature and a
role, moved with `git mv` after your approval). `as:tech-lead docs/features/<slug>` plans the next phase, `as:finish`
marks it done; `spec_lint.py` checks links, sources and that phase statuses match their proposals.

```text
/as:feature <description, files, pasted e-mail>
/as:feature docs/features/cancel-items         # new material or roadmap change
/as:feature docs/old-specs                     # map a legacy folder
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

### `deliver` — a whole feature or all issues, unattended

Hand it a feature page and leave (overnight): it asks its questions at the start — open questions with a recommended
answer each, branch, green checks, permissions that will not prompt — then loops without asking. Each stage runs in a
fresh subagent and follows an existing skill: `tech-lead` plans the next phase, `implement` builds a milestone,
`finish` reviews, merges the proposal and adds contract tests, `fix` closes the issues the run saved, and a final review
covers the whole branch. Where those skills would ask, it takes the recommended option and records it as an
assumption (`Assumed by as:deliver` in the proposal). Every green stage is a local commit; nothing is pushed.

It stops when all phases are done, checks are green, `spec_lint.py` is OK, the new scenarios have tests, the review has
no Must finding and no p1–p3 issue from the run is open — or earlier, at a decision only a human may take (acceptance
criteria, data deletion, a new external service, a breaking public contract), at checks it cannot repair (the stage's
changes go to a stash), when it stops making progress, or at `--max-stages`. `docs/features/<slug>/delivery.md` is the
morning report: criteria, assumptions to review first, stages and commits. Rerunning the command resumes.

Point it at `docs/issues` instead (optionally with a request as in `fix`: `all p1`, `bugs in orders`) and it works
through the saved problems the same way: you confirm the selection at the start, then each issue gets a Fix stage
(small ones fixed test-first, larger ones planned, implemented and finished), most important first. Issues are
independent, so one that needs a human decision or cannot be made green is skipped (its changes go to a stash) and the
run goes on. `remove-tests` and `docs` issues are left for a human. Done when every selected issue is closed or skipped; the
report is `docs/deliveries/<branch>.md`, skipped issues with their questions first.

```text
/as:deliver docs/features/cancel-items
/as:deliver docs/features/cancel-items --max-stages 40
/as:deliver docs/issues
/as:deliver docs/issues all p1 and p2
```

### `init` — onboard a repository

Runs `agent-docs`, then `spec-docs`, then links the spec from `AGENTS.md`, sharing one inventory and one round of
questions. Asks for approval before writing each part. On a brownfield project start with a spec for 2–3 central
modules and extend it later with `spec-docs`.

```text
/as:init                            # inventory, then asks which modules to specify
/as:init --spec backend/orders      # spec only for the given modules (or --spec all / --no-spec)
/as:docs-check                      # audit both, write nothing
```

With your consent it adds a fixed **Working principles** block to the repo root `AGENTS.md` — rules that keep agents
from over-engineering (reuse before writing, no speculative abstractions, root-cause fixes, tests for non-trivial
logic, never cutting validation or security). The text lives in
[`skills/init/references/working-principles.md`](skills/init/references/working-principles.md) and is updated when its
version changes; declining leaves an `off` marker so you are not asked again; `agent-docs` keeps the block untouched.
Inspired by [ponytail](https://github.com/DietrichGebert/ponytail).

At the end it checks the recommended Anthropic plugins (see `help` below) and installs missing ones after you
agree.

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
3. **Simplify**, then tests. 4. **Review** — findings Must / Should / Nice, you pick fixes, then tests; unfixed ones can be saved to `docs/issues/`.
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
```

Tools: first what the project already has (JaCoCo, ArchUnit, dependency-cruiser, knip, …); missing ones run once
without being added to the project (`uvx lizard`, `npx madge`, `npx jscpd`, osv-scanner, …) only with your consent;
git history and code reading always (churn, change coupling and frequently fixed tests are computed by
`skills/health/scripts/git_signals.py`). The report goes to `docs/health/<date>.html` with a `<date>.json` snapshot, so
the next run shows what improved or got worse. Small findings are fixed with tests before and after; tests are
removed only with per-test consent; larger findings you choose are saved to `docs/issues/` (with the finding's key)
for `/as:fix`, and the next run deletes the issues whose findings are gone.

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
converted to Markdown on the next run (content and IDs unchanged, links from `AGENTS.md` updated). Behaviour you
confirm as a bug is not specified: it goes to `docs/issues/` (older specs that parked bugs as open questions get them
moved).

An audit without writes is `/as:docs-check` (agent docs and spec together). `/as:spec-tests` reports which scenarios
are verified by tests (`COVERED` / `PARTIAL` / `MISSING`) and can save the gaps as issues; to make its mapping
deterministic, put the scenario ID in contract test names or tags (e.g. `@Tag("ORD-003")`,
`it("ORD-003 rejects out-of-stock order")`).

`skills/spec-docs/scripts/spec_lint.py` (Python, no dependencies) checks the spec mechanically: unique and well-formed
IDs, no ID reserved twice by parallel branches (`--against origin/HEAD`), resolving links and anchors, no leftover
HTML. Copy it into the repository and run it in CI to keep the spec consistent without an agent.

When `docs/spec/` exists, `agent-docs` links it from the repo `AGENTS.md` and lists the module pages in each app
`AGENTS.md` (links, not `@` imports), so an agent knows a module's contract before changing its behaviour. Run
`agent-docs` after `spec-docs` creates new pages.

## Development

### Structure

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

### Adding a skill / command

1. Copy `skills/help/` to `skills/<new-name>/` (lowercase kebab-case) and replace its body.
2. In `SKILL.md`, set `name: <new-name>` and a specific `description` (when to use it, ≤1024 characters).
   For a command the user invokes explicitly, add `disable-model-invocation: true`.
3. In `agents/openai.yaml`, set `display_name`, `short_description`, `default_prompt` (`$as:<new-name> ...`);
   for an explicit-only command, set `policy.allow_implicit_invocation: false`.
4. Add a row to [`skills/README.md`](skills/README.md).
5. Run the validation.

### Validation

```bash
python3 tools/validate.py              # manifests, frontmatter, openai.yaml, links
uv run --with pytest pytest tests      # validator and script tests
claude plugin validate .               # optional: official Claude Code check
```
