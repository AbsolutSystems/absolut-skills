# Changelog

## 1.22.0

Mockups: the user flow of 1.21.0 described the screens in words; now they can be shown, and chosen between.

- `feature` (Clarify): after proposing the flow it asks whether to show the screens as mockups (recommended for new
  or re-laid-out screens, not for a small change). Static HTML in `docs/features/<slug>/mockups/` — high fidelity,
  built from the application's own styles and its nearest screen, when the project already has a look (or from the
  look chosen on its roadmap); low-fidelity wireframes when it does not. Content is invented, never copied from the
  running application, which is opened only on `localhost` or an environment of `docs/qa/index.md`.
- Versions: 2–3 where there is a real choice. Each version is a whole page; `mockups/index.html` (the viewer,
  `skills/feature/assets/mockups.html`, copied verbatim) has a bar of tabs at the top that swaps the page, with the
  trade-off of the open version next to them. You pick one or a mix; the chosen file stays, the rest are deleted,
  and the choice is recorded as a decision. A version that needs a component the project lacks says so.
- `roadmap`: pages gain `## Screens` — the navigation and one row per screen (who, what for, reached from, stage) —
  and the same mockups question for the frame of the application; for a new application the look can be settled
  there, on versions of one key screen. `feature` starts a stage's flows from its screens.
- Rules in `skills/feature/references/mockups.md`: a mockup is an illustration (the criteria and the flow text win),
  a pattern for layout and content (never copied as code) and a record (not maintained after the screens ship).
- `tech-lead` (From feature) names the mockup in the plan step that builds the screen and names the project
  components it uses; `implement` matches the mockup with the project's own components and styles.
- `deliver` is unchanged: mockups are settled with you in `feature`, before an unattended run.

## 1.21.0

Three additions around what gets built and how it is to use: a roadmap above features, the user flow inside a
feature, and a UX review of the running app.

New skill `roadmap`: the level above a feature. `feature` documents one capability and splits it into phases; there
was nowhere to talk about a whole application or a large module before its features are known.

- `as:roadmap <direction>`: reads what exists, then discusses the direction at product level — users, capabilities,
  rules and limits, scope, order — with no technical design (a technical question becomes an open question for
  `tech-lead`). It sizes the topic first: one change → `as:tech-lead`, one feature → `as:feature` (with the summary
  to pass on), and writes nothing; several capabilities worth shipping alone → a roadmap.
- `docs/roadmap/<slug>/index.md` (format in `skills/roadmap/references/roadmap-format.md`): direction, users and
  goals, out of scope, stages with plain-language capabilities `C<n>` (the preliminary specification), product
  decisions, open questions, sources; catalogue in `docs/roadmap/index.md`. One stage = one feature.
- `as:roadmap docs/roadmap/<slug>`: refreshes stage statuses from the linked feature pages and records changes of
  direction.
- `feature`: new argument `docs/roadmap/<slug> [stage]` — documents a stage as a feature (capabilities become the
  acceptance-criteria candidates), adds `**Roadmap:**` to the feature's meta line and the stage's `**Feature:**` link.
- `tech-lead` (Size first): a topic beyond one feature is not designed there; it suggests `as:roadmap` (never for a
  feature phase or an estimate, so `deliver` is not stopped by it). From feature reads the decisions and out of scope
  of the roadmap the feature belongs to.
- `doctor`, `docs-check` and `feature` (after editing a roadmap page) lint `docs/roadmap/` with `spec_lint.py`.
- `agent-docs`: the root `AGENTS.md` links `docs/roadmap/index.md` when it exists. `help`, README and the catalogue
  list the new skill and flow.
- `deliver` is unchanged: it still delivers one feature, not a roadmap.

User flow in `feature`: acceptance criteria said what the user gets, but not how they move through the screens, so
that was decided during implementation.

- Feature pages gain `## User flow`: flows `UF<n>` with the criteria they cover, where the flow starts, numbered
  steps (screen — action → what the user sees next) and the empty, error and no-access states. Behaviour only, no
  visual design. A feature without a user interface says so in one line.
- `feature` asks about the flow in its Clarify step (proposing it from the criteria and the existing screens) and
  checks in Verify that every criterion reached through the interface is covered. Existing pages get the section on
  their next update.
- `tech-lead` (From feature) treats a flow's steps and states as requirements the proposal's scenarios cover; `qa`
  passes the flows to the executor as details; `qa-docs` reads them.

New skill `ux`: how an area of the running web application is to use, also where nothing is written.

- `as:ux <area | URL>`: proposes 2–4 walks (persona, goal in their words, start, viewport); a walker subagent per
  walk pursues the goal in a browser knowing only what the persona knows and records what it looked for, where it
  hesitated or got lost, with a screenshot per step; a separate reviewer subagent (a judgement subagent in the host
  mappings) reports only findings with a nameable cost to the persona — orientation, consistency, feedback, dead
  ends, error recovery, wording, effort. Flow and behaviour, not visual design.
- Report in `docs/ux/<date>-<area>.md` (format in `skills/ux/references/report-format.md`): walks, mismatches with
  written criteria, flows or rules, findings, themes, what works well. Findings are offered as issues of the new kind
  `ux`, mismatches as `bug`; themes spanning several screens are named as material for `as:roadmap`.
- Same browser setup and safety rules as `qa` (local or listed test environments only); works without `docs/qa/`
  by asking for the URL and role. Changes no code and no docs.

## 1.20.0

Product check: that the code does something is no proof it was wanted. Until now behaviour the written record was
silent about was judged only for consistency with the code, so a ticket saved without its author could be specified
as a scenario or pass QA.

- New brief `skills/spec-docs/references/product-check.md`: one read-only product-owner subagent (a judgement
  subagent in the host mappings) gets the behaviours about to be accepted and reports only those with a nameable harm
  to the product's users — lost author, owner or history, input dropped silently, dead ends, a neighbouring flow that
  works differently, a role with too much or too little — plus written rules to reconsider. It changes nothing: a
  Suspect item is recommended as `bug` and becomes an issue, never a scenario; a doubted written rule is a question.
- `spec-docs` step 3 (also in `docs-check`): runs it over the new and the existing scenarios and rules before the
  "intended or bug?" questions.
- `tech-lead` Feature step 5 (also From estimate and From feature): the draft proposal's added and changed scenarios
  pass it before the user approves — once merged they are intended by definition, so this is the last and cheapest
  place to question them. A Suspect scenario is corrected in the draft.
- `finish` step 6: Spec drift and New behaviour items pass it before the user classifies them.
- `qa` step 4: after the judges, over what the executors saw; the report gains `## Product notes`, `run.json` a
  `product` list, and the evidence page a Product notes box (it reads "Needs attention" even when every checkpoint
  passed). Product notes are offered as issues with the failures.
- `health`: new `product` findings — the product check over the whole spec (not with `--quick`); saved as `bug` or
  `spec-gap` issues, never fixed in the run.
- `deliver`: policy lines for the product check in the Plan, Finish and QA stages — a Suspect item is fixed within the
  stage's scope or saved as an issue, a written rule to reconsider becomes a `spec-gap` issue and an open item.

## 1.19.1

- `deliver`: decides as the product owner. A review question for the author is no longer copied to the report's open
  items: a gap or defect it reveals (missing behaviour, unhandled case) is fixed within the stage's scope or saved as
  an issue, a choice (wording, default, naming) is made and recorded as an assumption; only a human-only decision
  reaches the open items.

## 1.19.0

Evidence by running: four places produce a command, its output or a number a person can check. Ideas from
[pstack](https://github.com/cursor/plugins/tree/main/pstack) (MIT).

- Working principles v3 (`as:doctor` reports `v2, current is v3`): two fixes of one failure did not hold → test the
  assumption they shared before a third; a test fails when the behaviour breaks and survives a refactor (assert what
  callers observe, the expected value from the requirement). `tech-lead` Bug step 2 gains the premise rule.
- `deliver`: a finding, QA failure or issue fixed in the run that comes back gets one more Fix stage under the premise
  rule (the assumption and its observation in the run log); back again → issue, a feature run stops, an issues run
  skips it. In the Finish stage every new `error`/`edge` test is mutation-checked: the production file is copied to
  `${TMPDIR:-/tmp}/as-mutation/`, broken by the smallest edit, the test must fail, the file is restored and its hash
  checked (the Tree step restores leftovers after a crash); a test that survives is strengthened once, then saved as
  an `add-tests` `p3` issue and its scenario does not count as covered.
- Safety fact (`skills/tech-lead/references/safety-fact.md`): the plan of a size S change, of a bug fix (`tech-lead`
  Bug step 3) and of an `S` issue fixed by `fix` states the one fact the change is safe because of —
  `**Safe because:** <fact> — level <n> — <evidence>` — with evidence levels 1–5; level 4 (a script that runs the real
  code) for facts outside the type system; `unproven` plus the cheapest check otherwise. A list of callers is not that
  fact. Unattended, `deliver` runs the named check and records what stays unproven as an assumption.
- `review` step 6 **Prove** (Report, Act and Summary become 7–9; `finish` step 4 follows steps 2–8): asked once when
  there is a `plausible` Must or Should or a `confirmed` Must — one prover subagent per finding writes the smallest
  test of its failure scenario (new files only, one after another) and runs it. `proven` (the command, its output, the
  required output), `disproved` → `refuted` only with proof the scenario reached the code, `unprovable` with the
  reason. Statuses `proven`, `confirmed`, `plausible`, `refuted`; `fix first` on a `proven` or `confirmed` Must. Branch
  mode: a `proven` finding's fix starts from its test; an unfixed one's test moves into the issue. PR mode: in the
  review tree (dependency install asked as in `worktree-create`), the comment states the test and its output, and every
  file the provers wrote is deleted before posting. New Prover brief in `skills/review/references/briefs.md`; provers
  are judgement subagents in the host mappings. `deliver` runs the step without asking (`unprovable` → `p4` issue).
- `tech-lead` **Performance** path (`skills/tech-lead/references/perf.md`) for "X is slow", "make Y faster" or a measured
  regression: claim, baseline (5+ runs, median and range, errors and "did it run" checked), the limiter from a profile
  of an unreported run, the plan after approval, the same measurement after (production-like, A/B alternated; within
  the range → reverted), and a report with the verdict first — or `inconclusive` and why. New issue kind `perf`:
  `fix` routes it to the Performance path, `deliver` leaves it for a human.
- Readable journey IDs: a QA journey is identified by a kebab-case slug given once when it is written
  (`### <a id="checkout-guest"></a>Guest checkout`, checkpoints `checkout-guest-2`, `as:qa checkout-guest
  refund-partial`) instead of `J1`, `J2`, …; renaming changes only the title. Rules in `qa-format.md`: two to four
  words, not `journeys`/`branch`/`explore`, not `j<n>`, no trailing digits, never reused. Existing `J<n>` journeys stay
  valid; `qa-docs` suggests a slug for each ("Legacy IDs"), and a migrated journey keeps `J<n>` as a second anchor and
  a `**Was:** J<n>` line, so old reports, issues and `as:qa J2` still resolve. `qa` lists the journey IDs with titles
  and runs nothing when a named one does not exist.

## 1.18.1

- Every question to the user carries a recommendation and its reason. A batch of many similar decisions (bug or
  intended, keep or remove) is shown as one table — item, what it does today, recommendation, why — and the user only
  accepts it or names the items to change; the recommended option comes first. `spec-docs` analysis subagents mark
  the answer they recommend for each open question, with evidence, and step 3 builds the table from them.

## 1.18.0

- Choices are explained before they are asked: the host mappings (`references/claude-tools.md`,
  `references/codex-tools.md`) gain "Asking the user to choose" — how it works today, a concrete scenario where it
  breaks, how often and how badly, each option's pros, cons and cost, and a recommendation with the reason, in plain
  language — and only then the short question. `tech-lead` points to it before every choice.

## 1.17.0

- `qa` writes an HTML evidence page next to its working screenshots (`.qa/<run>/report.html`): a summary with the
  counts, every result that is not `PASS` linked, broken app-wide rules and what was not checked; then every scenario
  with its steps, what the executor saw, and the screenshot of every step and checkpoint — also the ones that passed —
  with the expected outcome, the judge's reason, console errors and failed requests. A `FAIL` carries a red `FAILED`
  banner and a filter hides the scenarios without problems. The file embeds its images, so it can be moved or sent;
  it is not committed. The executor now takes a screenshot after every step, and the new `scripts/qa_report.py`
  renders the page from `.qa/<run>/run.json` (format in `qa-format.md`) and prints the counts the Markdown report must
  match. Screenshots of failures are copied to `docs/qa/runs/` instead of moved.
- `tech-lead` grounds itself in the code, not in summaries of it: the Explore brief also traces the flow from the
  entry point to storage or output (data, state changes, side effects) and names the 5–10 key files, which the tech
  lead then reads in full before the options, the scenarios and the plan.
- `review` (also inside `finish` and `deliver`): a rule written in `AGENTS.md` or `.guidelines/` that the diff breaks
  is a Should finding without a failure scenario — raised by the goal and contract lens, quoted with its file and
  line, and checked by the verifier (the rule exists, applies to the path, is broken as written, is not enforced by
  lint already). Conventions only inferred from the surrounding code are still not findings.
- `tech-lead` architecture subagents run on Opus whatever the session model (Claude Code), and `tech-lead` no longer
  asks about Fable: the options are short and compared by the main thread and the user, so the stronger model is
  kept for `review`, `estimate`, `explain` and the `deliver` stages, which still ask.
- `feature-dev` is no longer a recommended plugin: `init` does not install it, `doctor` does not report it and `help`
  does not point to it. `tech-lead` → `implement` → `finish` covers its phases; the three points above are what it
  did and `as` did not.

## 1.16.0

- `implement`, `finish`, `review` and `issue` may now be invoked by the model, not only by the user: an agent (or a
  subagent) told to carry out an approved plan, done with a change proposal's plan, asked to review a branch or PR,
  or agreeing with the user to park a problem for later loads the skill itself instead of asking the user to type the
  command. Their descriptions end with a narrow "Use when …; not for …" trigger, `agents/openai.yaml` allows implicit
  invocation, and every write still waits for the user's approval — for `implement` that approval is the proposal's
  approved `## Plan`, and its description excludes code changes without one. `deliver` keeps reading their
  `SKILL.md` as before. The other skills stay commands only.

## 1.15.0

- Stronger model for judgement subagents, opt-in (Claude Code): when the session is not on Fable, `tech-lead`
  (architecture options), `review` (reviewers and verifiers, also inside `finish`), `estimate` (consistency review)
  and `explain` (fact check) ask once per run whether to run those subagents on Fable; everything else stays on the
  session model. `deliver` asks at start-up, records the answer as a start-up decision and applies it to the Plan
  and Final review stages; its stages never ask. A refused model falls back to the session model. The rule lives in
  `references/claude-tools.md`; Codex does not ask.

## 1.14.0

- `review`, from a pilot on three pull requests (17 verified findings: none refuted, 10 with a false supporting
  detail, severity moved on about half):
  - The verifier checks every statement of a finding, not only whether it can be refuted: its line gains
    `correction:`, the report shows the corrected finding, and the brief no longer tells it to assume the finding is
    wrong. A Nice finding that two lenses raised, or that one raised and another dismissed, is verified too;
    reviewers return a `Dismissed` section for that. Nice is defined as cost or clutter with no wrong outcome — doubt
    is a question.
  - Packages are limited by size (under 1500 changed lines each) instead of by number. More than 5 packages → the
    skill asks: review all, review a selection, or stop because the change should be split; the selection follows a
    written ranking (new code, trust boundary, called-into and conflicting packages, size last). `deliver` reviews
    all. Reviewers are told which packages were left out, and a finding relying on one is marked.
  - The merge check runs before the packages are chosen (step 3; reviewers and verify are now steps 4 and 5), so
    conflicting files count as risk.
  - The report leads with coverage; `ship` needs every package reviewed, and `partial` is the verdict of a review
    that left packages out and found nothing. Findings carry their lens and any severity move; questions are merged
    like findings and attached to the finding they belong to; Nice findings are listed, one line each.

## 1.13.0

- New `doctor` skill: a read-only check in seconds of how a repository stands against `as` — working principles
  block (missing, older version, customised, declined), `AGENTS.md`/`CLAUDE.md` pairs and symlinks, the `.guidelines/`
  index, outdated `health.css`/`explain.css` copies, spec and feature lint, change proposals untouched for 30+ days,
  issues per priority and misnamed issue files, apps without guidelines, the last `as:health` run, the CLI tools the
  skills use, and the recommended plugins on Claude Code — each with the command that fixes it. Deterministic part in the tested stdlib script `doctor/scripts/doctor.py`.
  It takes over the plugin status from `help` and `docs-check`.
- New `guidelines` skill: writes an app's `.guidelines/<topic>-guideline.md` (testing, architecture, api, data,
  frontend, libraries, code-style, security) from the conventions its code follows. One subagent per topic counts how
  consistently each convention is followed and which variant the last six months of changes use; the team settles
  conflicts (target vs legacy) and confirms rules; the file holds short rules for new code and reference files to
  copy, nothing a tool already enforces. `agent-docs` no longer creates guideline files or asks about the testing
  strategy: it fixes guideline drift, keeps the index, and recommends `as:guidelines` for a topic without one.
- `finish` step 3 finds **new clones** after simplify: for a diff of 30+ lines, `npx jscpd@5 --similarity
  --baseline-from-ref <base>` lists copies the branch added of code that already exists, which a diff review cannot
  see. Step 4 passes them to `review` as context, where a clone is reported as unnecessary code whose copies a later
  fix would miss; nothing fails on the tool alone. `deliver` runs it without asking.
- `health` reports a project without coverage in its build as a medium finding with the concrete change (JaCoCo or
  Kover plugin, a coverage script with the `lcov` reporter).
- Working principles block **v2**: five one-line rules against structural bugs (parse and validate outside data once,
  where it enters; new business decisions in I/O-free code; illegal states unrepresentable in new code; retried or
  re-run operations idempotent; one owner per piece of state, derived rather than copied, concurrent writers guarded).
  The rules that could invite a refactor apply to new code only. `as:init` offers the update to repositories holding
  v1. The rules and the clone check are adapted from [ub-mode](https://github.com/unclebob/ub-mode).

## 1.12.0

- New `explain` skill: explains code to a person who did not write it, as an HTML page with Mermaid diagrams in
  `docs/explain/` — a change (the current branch, or a PR whose code is read in a separate worktree as in `review`,
  the page written to your working copy and the worktree offered for removal) for a reviewer or stakeholder, a module
  or a question for a newcomer, or a documented feature's logic on worked examples for the business (cards with
  concrete numbers, a matrix, edge cases, validation messages, open questions). A change that calculates or decides by
  thresholds gets example cards too.
- Every number names its source (a test's expected value, a value from `sources/`, or a formula written as a
  spreadsheet cell); hand calculations are `to-confirm`, mismatches `differs` and are offered as issues.
- Research fans out — a structure inventory per touched module (small model, every item with a quoted line as
  evidence) and a tracer per flow; diagrams use only evidenced items. A separate fact-check subagent then checks every
  claim of the written page against the code (the PR head for a PR) and the sources — nodes, edges, delta marks,
  rules, references, test values, card formulas and statuses: refuted claims are removed or corrected, unclear ones
  reworded or moved to open questions.
- A change that alters the structure (files added or removed, code moved between modules, two or more modules, a
  public API removed) gets an architecture delta: one Mermaid diagram of both states with added, removed, moved and
  changed components marked. Labels use the language of the problem, never method names; Mermaid quoting rules and a
  browser render check keep diagrams from failing.
- Ships `explain.css` (base shared with `health.css`, print styles for PDF); Mermaid loads from a CDN. Built from the
  `explain` generator of review-pr-kit, without its project-specific palette and without archify.
- `feature` suggests `as:explain docs/features/<slug>` when criteria involve calculations or thresholds.

## 1.11.0

- New `review` skill: reviews your branch from its base, or a teammate's pull request (number or URL) in a separate
  worktree against the PR's real base branch. Three read-only reviewers with disjoint scopes (correctness and
  security, goal and contract, UI only when the diff touches it; large diffs split into up to 5 packages) report only
  problems the diff introduces, each with a concrete failure scenario — no style or "could be cleaner" findings. A
  separate sceptical verifier then tries to refute every Must and Should finding: refuted ones are dropped and only
  counted, unrefuted but unproven ones are kept as `plausible`. Also turns a PR description that does not match the
  diff into questions for the author and checks with `git merge-tree` that the branch merges cleanly. Branch: you pick
  fixes, the rest can be saved as issues. PR: inline GitHub review comments, posted only after you approve them.
- `finish` step 4 and `deliver` (the review in the Finish stage and the Final review) run `review` instead of the
  built-in `code-review` skill, on both hosts. Unattended, `deliver` fixes `confirmed` findings and fixes a `plausible`
  one only when a failing test shows it first (else a `p4` issue marked unconfirmed).
- `finish/references/review.md` gains the false-positive rules (reachability, introduced by the diff, no quota) and
  stays the shared review bar, also for `health`. Issues from reviews have `**Source:**` `as:review`.

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
- `deliver`: a QA stage after a clean final review when `docs/qa/` exists, run by the loop in the main thread,
  always against the `local` environment of `docs/qa/index.md` (started with its command when it does not answer);
  failures become run issues and are fixed in the run; done needs a QA run without failures (skipped and said so when
  the browser tool, the app or a `local` environment is not available).
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
