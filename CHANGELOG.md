# Changelog

## 1.10.0

- New `qa-docs` skill: writes and maintains `docs/qa/` for a web app — environments and how to start them, test
  accounts as environment variable names, roles, app-wide UI rules `R<n>` and cross-feature journeys `J<n>` written as
  intent with checkpoints a screenshot can decide. Drafts it from the code, the feature pages and `AGENTS.md`; later
  runs report drift, outdated journeys, criteria too vague to check and the last result of every criterion and
  journey. Acceptance criteria stay on the feature pages.
- New `qa` skill: checks the running web app in a browser — a feature's criteria, the journeys, or what the branch
  touches (`branch`). One executor subagent per scenario, in sequence, saves screenshots, console errors and failed
  requests; a judge subagent that never saw the run decides `PASS` / `FAIL` / `OUTDATED` / `BLOCKED`. Report in
  `docs/qa/runs/` with the screenshots of failures (the rest in gitignored `.qa/`), failures offered as issues.
  `explore <area>` tries to break one area. Opens only local or listed test environments, never production.
- `deliver`: a QA stage after a clean final review when `docs/qa/` exists, run by the loop in the main thread;
  failures become run issues and are fixed in the run; done needs a QA run without failures (skipped and said so when
  the browser tool or the app is not available).
- `finish` suggests `as:qa branch`, `feature` suggests `as:qa-docs` after criteria change, `help` and README gain the
  QA flow; `playwright` joins the recommended plugins, browser tools in the host mappings.

## 1.9.0

- `deliver` takes `docs/issues [request]` as a second target: an unattended run over the saved issues (request as in
  `fix`: `all p1`, `bugs in orders`; none → all open). Start-up shows the selection (`remove-tests` and `docs` issues
  left out) and asks once; the loop runs a Fix stage per issue, most important first, larger ones through
  plan → implement → finish. A blocked or unrepairable issue is skipped (changes stashed, question in the report) and
  the run goes on. Done when every selected issue is closed or skipped; report in `docs/deliveries/<branch>.md`;
  `--max-stages` defaults to 40 for issues.

## 1.8.0

- New `deliver` skill: delivers a documented feature (`docs/features/<slug>`) unattended, e.g. overnight. Start-up
  asks once — open questions with a recommended answer each, branch, green checks, host permissions — then loops
  without asking: plan the next phase (`tech-lead`), implement a milestone (`implement`), wrap up (`finish`), fix the
  issues the run saved (`fix`), final review of the whole branch. Each stage runs in a fresh subagent; where the
  followed skill would ask, the autopilot policy (`deliver/references/autopilot.md`) takes the recommended option and
  records it as `Assumed by as:deliver`. Commits each green stage locally, never pushes; stops at the done criteria,
  a human-only decision, checks it cannot repair (changes stashed), no progress or `--max-stages`; resumes on rerun.
  Morning report in `docs/features/<slug>/delivery.md`.
- `help`, README: Unattended feature flow; host mappings: permissions and subagents for an unattended run.

## 1.7.0

- New `feature` skill: living feature docs in `docs/features/<slug>/` — `index.md` with why, users and goals,
  non-goals, user-level acceptance criteria (`AC<n>`) linked to the module scenarios that realise them, a roadmap of
  phases (one change proposal each), decisions and sources; `sources/` keeps the client's PDF, spreadsheets, pasted
  e-mails and meeting notes verbatim, and every criterion and decision links its source. Seeds from an accepted
  estimate, documents an existing feature from the code and archived proposals, records new material and what it
  changes, and maps a legacy documentation folder file by file (`git mv` after approval). Catalogue in
  `docs/features/index.md`; format in `feature/references/feature-format.md`.
- `feature/scripts/xlsx_text.py`: `.xlsx` sheets as Markdown tables (stdlib only), saved next to the original.
- `tech-lead`: `docs/features/<slug>` plans the next phase (From feature path); proposals for a phase carry a
  `**Feature:**` meta line with the criteria they realise and set the phase `in progress`; feature pages of the
  touched modules are read when grounding features and bugs.
- `finish`: archiving a proposal with `**Feature:**` marks its phase done, fills `**Realised by:**`, the Now line and
  the feature status.
- `spec_lint.py` also checks `docs/features/` (`--features`): links and anchors, `AC<n>` anchors, phases `in progress`
  linking an open proposal and `done` linking an archived one, every file in `sources/` listed; runs without
  `docs/spec/`. `docs-check` reports its feature errors.
- `estimate` suggests `as:feature` for multi-phase requests; `agent-docs` links `docs/features/index.md` from the root
  `AGENTS.md`; `help`: Feature roadmap flow.

## 1.6.0

- Known problems live in `docs/issues/`: one Markdown file per problem, `p<1-4>-<slug>.md` with the priority in the
  name (`p1` data loss, security or a blocker … `p4` clean-up), kind, effort, evidence (file, symbol and a code excerpt, never
  line numbers) and a suggested fix; fixed means
  deleted in the same diff. Format and priority rubric in `issue/references/issue-format.md`.
- New `issue` skill: saves a described problem, or collects the findings reported earlier in the conversation (for
  example by `/code-review` or `/claude-security`) and asks which to save; checks the evidence, merges duplicates.
- New `fix` skill: lists open issues by priority and effort and recommends one, or takes a slug or a request ("10 most
  important bugs"); re-checks the evidence, fixes small ones test-first and deletes the issue, plans larger ones as a
  change proposal with an `**Issue:**` meta line. Replaces `tech-lead health` / `H-NNN`; `tech-lead` routes "fix the
  most important bugs" to it.
- Skills save what they do not fix now (with consent): `finish` (unfixed Must/Should review findings, deferred
  regressions, failing new tests) and closes the issue of an archived proposal; `health` (larger findings, with the
  finding's `**Key:**`) and deletes the issues whose findings are gone; `spec-docs` and `init` (behaviour confirmed as
  a bug, instead of an open-question note; existing bug notes are moved); `tech-lead` (a deferred bug with its root
  cause); `implement` (problems outside the plan).
- One command, one job: new `docs-check` skill (audit of agent docs, spec and plugins without writes) replaces
  `--check` of `agent-docs`, `spec-docs` and `init`; new `spec-tests` skill replaces `spec-docs --tests`. Removed
  `health --no-fix`, `init --no-principles` and `init --no-plugins` — those steps already ask.
- `help`: "Which command" table ("I want to… → command") shown first and as the `which` topic, also in README;
  `issues` topic and Known issues flow.

## 1.5.0

- New `estimate` skill: analyses a client's feature request against the code and spec, flags gaps, conflicts with
  current behaviour, better alternatives and worthwhile additions, and prices a step plan in `min / likely / max`
  hours for a developer who knows the code and works with an AI agent (tests and communication included, manual QA
  and deployment listed as not included). Writes `docs/estimates/<slug>/analysis.md` (internal) and `client.md` (PRD,
  estimate per block, assumptions, questions, priced suggestions) in the client's language; revisions after the
  client's answers. `scripts/estimate_totals.py` sums blocks, computes PERT expected values and checks `client.md`.
- `tech-lead`: `docs/estimates/<slug>` plans an accepted estimate from its analysis — re-checks the code instead of
  exploring again, asks only open client questions, warns when the plan exceeds the estimate; the proposal links it in
  an `**Estimate:**` meta line.
- `help`: client request flow in the `flows` topic.

## 1.4.0

- Health fixes flow: `tech-lead` takes `health` (proposes the next findings from the newest `docs/health/*.json`,
  skipping planned ones, and plans the one you choose) or `H-NNN` (one finding), starting from the finding's evidence;
  refactors keep behaviour (tests pin it first), removing tests needs per-test consent. The proposal records the
  finding in a `**Health:**` meta line.
- `health`: `M`/`L` findings are no longer turned into task briefs in the conversation — the summary points to
  `as:tech-lead H-NNN`, then `as:implement` and `as:finish`; findings with an open proposal are shown as in progress.
- `help`: new `flows` topic — how the commands chain for a feature, a bug, health fixes, parallel work and upkeep.
- README reorganised around the workflow: how to work with `as`, the flows, a command table and what gets written
  where; skill details and development notes follow.

## 1.3.0

- New `implement` skill: executes the approved `## Plan` of the branch's change proposal step by step in any session
  (tests first for `error`/`edge` scenarios, ticks each step, stops and proposes a plan edit on deviations), so a new
  session or a cheaper model continues from the file, not the conversation. `tech-lead` points to it.
- `tech-lead`: sizes the task first — small changes skip subagents, the options step and the change proposal; the
  description no longer triggers on questions about how existing code works.
- Scenario IDs across branches: `tech-lead` reserves IDs counting other local and remote branches, and `finish`
  checks that a proposal's added IDs are still free on the default branch before merging it.
- `finish`: one read-only subagent per touched module with a short diff-anchored brief (`finish/references/analysis.md`:
  proposal status, spec drift, new behaviour, tests, docs — only what the diff changed) feeds the spec, test and docs
  steps instead of three full `spec-docs`/`agent-docs` fan-outs; contract tests cover the proposal and the new
  behaviour, older gaps are left to `spec-docs --tests`; steps renumbered (`--no-tests`, `--no-docs` now skip 7 and 8). It
  runs the proposal's `**Verify:**` and lists `**Rollout:**` items in the summary.
- Scripts (Python, stdlib only): `health/scripts/git_signals.py` computes churn, change coupling and frequently fixed
  tests (and recognises `test_*.py` files); `spec-docs/scripts/spec_lint.py` checks IDs, anchors, links, leftover
  HTML and IDs reserved twice by parallel proposals — used by `spec-docs` verify and `finish`, and usable in CI.
- Host mappings: on Claude Code read-only subagents run on a smaller model; on Codex without subagents `tech-lead`
  gives one recommended architecture and compares options only on request.
- `skills/AGENTS.md`: language rule corrected — health reports follow the spec language; `health` has no `--lang`.

## 1.2.0

- `tech-lead`: the approved implementation plan is saved as a `## Plan` checklist in the change proposal
  (`docs/spec/changes/<slug>.md`), so it survives the session and is reviewed with the PR; steps are ticked during
  implementation, and changes made during plan-mode approval are written back. `finish` verifies unticked steps
  before archiving the proposal.
- `agent-docs`: maps spec pages to directories by the Markdown `**Source:**` meta line (the `<dl class="meta">` of
  legacy HTML pages only as a fallback).
- `finish`: baseline and reruns include the documented lint, type-check and build commands; the summary suggests
  `/claude-security` when the diff touches authentication, input handling, secrets or data access.
- `tech-lead`: the bug path ends with a handoff — approval, failing test first, fix, `as:finish`.
- `worktree-create`: copies ignored `.env*` files from any depth (monorepo apps) and offers to install dependencies;
  the undocumented `z <branch>` alias is removed.
- `finish`: lint and type errors only in unchanged files are recorded as pre-existing and do not stop the run.
- Validator: `disable-model-invocation` must match `policy.allow_implicit_invocation`; `#fragment` links must point to
  an existing heading or `<a id>` anchor; `skills/*/references/*.md` are link-checked too, ignoring examples in fenced
  code blocks and code spans.

## 1.1.0

- `spec-docs`: the specification is Markdown (`docs/spec/**/*.md`) formatted for people — breadcrumbs, table of
  contents, quoted SHALL sentences, scenarios with kind markers and Given/When/Then lists, `> [!NOTE]` open questions,
  stable `<a id>` anchors for scenario links. A legacy HTML spec is converted one to one on the next run (pages and
  change proposals), links to it are rewritten and `spec.css` is removed when unused.
- `tech-lead` writes change proposals and `finish` merges and archives them in Markdown; `agent-docs`, `init` and
  `help` point to `.md` pages.
- `health` keeps its HTML report and now owns the stylesheet: `docs/health/health.css` (from `assets/health.css`);
  older reports linking `../spec/spec.css` are relinked.

## 1.0.0

- `tech-lead`: large changes go to plan mode with milestones instead of `/feature-dev:feature-dev`, which cannot skip
  its exploration and architecture phases and would redo the design.
- Claude mapping: built-in `code-review` (local diff) is distinguished from the `code-review` plugin (PR); built-in
  skills are used only when the Claude Code version lists them. `claude-security` is invoked as `/claude-security`.
- `agent-docs`: writes only what the code cannot tell (line test); no purpose, stack, public API or dependencies
  sections; module `AGENTS.md` only for modules with pitfalls or rules; new `PRUNE` status; spec module links move to
  the app `AGENTS.md`. `finish` only corrects or adds necessary facts. Based on arXiv:2602.11988.

## 0.4.0

- `worktree-create` skill: creates a branch and a git worktree in `../<repo>-worktrees/<name>` from the current branch
  or `from <branch>`; asks before reusing an existing branch and offers to copy ignored `.env*` files.
- `worktree-close` skill: offers to commit uncommitted changes, shows unpushed commits and ignored files to be deleted,
  then removes the worktree (never `--force`) and keeps the branch.

## 0.3.1

- `agent-docs`: detects `AGENTS.md` ↔ `CLAUDE.md` symlinks and migrates them to regular files.
- `recommended-plugins.md`: retry with `claude plugin marketplace update claude-plugins-official` when a plugin is
  not found in an outdated local marketplace copy.
- Maintainer docs: `AGENTS.md` (regular file instead of a symlink), `skills/AGENTS.md`, `.guidelines/` for skill
  authoring and testing.

## 0.3.0

- `tech-lead` skill (auto-invoked): designs features and investigates bugs grounded in code, `AGENTS.md` and spec;
  parallel architecture options, decision record and proposed scenarios in `docs/spec/changes/<slug>.html`, plan, and
  handoff to plan mode or `/feature-dev`. `finish` merges implemented proposals into the spec and archives them;
  `spec-docs` reserves their IDs; `health` flags stale proposals.
- `health` skill: periodic whole-project check (hotspots, structural and change coupling, coverage and test quality,
  dead code, duplication, dependencies, docs drift) with configured or consented ephemeral tools; dated HTML report and
  JSON snapshot with trends in `docs/health/`; fixes small items on request. `spec.css` v2 adds report classes.
- `finish` skill: wraps up a feature on the branch's changes — simplify, review, spec drift check (intended vs
  regression), missing contract tests tagged with scenario IDs, `AGENTS.md` refresh; tests after each code change.
- `help` skill replaces `hello`: installation check, recommended Anthropic plugins status, and a workflow guide
  (onboarding, plan mode, build, review, commit, docs).
- `init` skill: runs `agent-docs`, then `spec-docs` for a chosen scope, then links the spec from `AGENTS.md`, with one
  shared inventory and an approval gate before each write; offers an opt-in, versioned Working principles block for the
  repo root `AGENTS.md` (inspired by ponytail); finally checks the recommended Anthropic plugins and
  installs missing ones with consent.
- `spec-docs` skill: builds and audits a human-readable HTML specification in `docs/spec/` (system, app and module
  contract pages with Given/When/Then scenarios and stable IDs) sharing one `spec.css`; `--tests` reports which contract
  scenarios are covered by tests.
- `agent-docs`: when `docs/spec/` exists, repo/app/module `AGENTS.md` link their spec page; missing links are reported as drift.

## 0.2.0

- `agent-docs` skill: builds and audits hierarchical `AGENTS.md` (+ `CLAUDE.md` importing it) and per-app `.guidelines/`, asks about ambiguities and recommends improvements.

## 0.1.0

- Initial structure for the `as` plugin (marketplace `absolut-skills`) for Claude Code and Codex.
- `hello` skill as a template.
- `tools/validate.py` — format validation for manifests and skills.
