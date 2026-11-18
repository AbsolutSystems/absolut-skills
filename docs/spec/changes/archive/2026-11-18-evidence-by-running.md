<!-- as:tech-lead lang=en -->
Changes › Evidence by running

# Evidence by running

Four places in `as` produce evidence a person can check — a command, its output, a number with its spread — instead
of a judgement made by reading: the premise rule and the mutation check, the safety fact of a small change, the Prove
step of `review`, and a Performance path in `tech-lead`.

**Status:** implemented · **Proposed:** 2026-11-18, commit `d16cb8a` · **Modules:** [init](../../../../skills/init/SKILL.md), [tech-lead](../../../../skills/tech-lead/SKILL.md), [fix](../../../../skills/fix/SKILL.md), [review](../../../../skills/review/SKILL.md), [deliver](../../../../skills/deliver/SKILL.md), [finish](../../../../skills/finish/SKILL.md), [issue](../../../../skills/issue/SKILL.md), [help](../../../../skills/help/SKILL.md)

## Why

`as` verifies mostly by reading. The review verifier is read-only, so a finding it cannot settle without running the
code stays `plausible`. A small change is called safe because its callers were listed. A bug hunt can loop on fixes
that share one wrong assumption. Nothing checks that a new test would fail if the behaviour broke. There is no path
for "this is slow". Agents write the code; what a person can still check is evidence.

## Scope

- **In:** working principles v3 (two lines) and the premise rule in `tech-lead` Bug and `deliver`; a mutation check of
  new `error`/`edge` tests in unattended `deliver` only; the safety fact of `tech-lead` size S, Bug step 3 and `fix`
  `S` issues; a Prove step in `review` after Verify; a Performance path in `tech-lead` with a new issue kind `perf`.
  One release, 1.19.0, after four milestones (A–D).
- **Out:** a learning loop from corrections; a third principle line for numbers (it lives in the Performance path);
  the mutation check in interactive `finish`; Prove as a flag or a separate skill; the safety fact for M and L changes
  on the Feature path (their scenarios and `**Risks:**` cover it; every bug fix keeps it) and in `review`; multi-vendor panels, auto-merge, any change to approval
  gates; new scripts.

## Decision

The architecture comes from the brief ("evidence by running"), with ideas from
[pstack](https://github.com/cursor/plugins/tree/main/pstack) (MIT): `interrogate`, `blast-radius`,
`attack-the-premise`, `test-behavior-not-implementation`, `explain-the-number` with `benchmark-checklist` — the ideas,
not the text. No architecture comparison was run: the brief settles the shape; only the points below were open.

Decided with the user (2026-11-18):

- **Issues run, a problem that comes back twice** — skipped like a blocked issue (the question and the failed
  assumption go to the report's skipped list), the run goes on; a feature run stops, as today. The extra Fix stage is
  an ordinary stage under `--max-stages`; when the limit comes first, the problem is already saved as an issue.
- **Issue kind for a deferred performance problem** — new kind `perf`. `bug` would route it through the Bug path,
  whose failing test first measures nothing. `fix` routes `perf` to the Performance path; `deliver` does not select
  `perf` issues (like `remove-tests` and `docs`): a verdict needs a quiet machine and production-like settings an
  unattended run cannot promise.
- **Mutation check crash safety** — the original is copied to `${TMPDIR:-/tmp}/as-mutation/<tree>/<path>` before the
  edit; the loop's Tree step restores every file found there and checks its recorded hash before anything else, so a
  stage that dies mid-mutation never leaves a broken production file to be committed or "repaired".
- **`tech-lead` writes no code before approval** — a level 4 safety-fact script and the performance measurement
  scripts live in a temporary directory outside the repository while planning; the script enters the tree only during
  implementation, as the test of the change.
- **`unproven` in an unattended run** — the `fix` stage runs the cheapest check the plan names; still `unproven` →
  recorded as an assumption (`skills/AGENTS.md`: a new gate in a followed skill needs a policy line).
- **Prove in PR mode, review in place** — the step records `git status --porcelain` before it and deletes every file
  it added afterwards, then confirms the tree is as before.

## Scenarios

**Module:** [init](../../../../skills/init/SKILL.md)

### <a id="WP-R1"></a>WP-R1 — Working principles v3

**Change:** 🆕 added

> The working principles block **SHALL** carry marker `v3` with a premise line (stop after two failed fixes of one
> failure, test the shared assumption) and a test line (assert what callers observe, expected value from the
> requirement).

#### <a id="WP-001"></a>WP-001 — doctor reports an old block

**Kind:** ✅ happy · **Change:** 🆕 added

- **Given** a repository whose root `AGENTS.md` has the `v2` block
- **When** the user runs `as:doctor`
- **Then** the working principles check reads `v2, current is v3`

**Module:** [tech-lead](../../../../skills/tech-lead/SKILL.md)

### <a id="TL-R1"></a>TL-R1 — Safety fact

**Change:** 🆕 added

> The plan of a size S change and of a bug fix **SHALL** state the one fact the change is safe because of, with an
> evidence level and its evidence.

#### <a id="TL-001"></a>TL-001 — Small change states its safety fact

**Kind:** ✅ happy · **Change:** 🆕 added

- **Given** a size S change
- **When** `tech-lead` writes the short plan
- **Then** it has a line `**Safe because:** <fact> — level <n> — <evidence>`

#### <a id="TL-002"></a>TL-002 — Fact outside the type system

**Kind:** ⚠️ edge · **Change:** 🆕 added

- **Given** a size S change whose safety rests on a JSON response field or a database column
- **When** the plan is written
- **Then** the line carries level 4 with the command and its output, or says `unproven` and names the cheapest check

#### <a id="TL-003"></a>TL-003 — A callers list is not a fact

**Kind:** ❌ error · **Change:** 🆕 added

- **Given** a plan whose only safety argument is the list of callers
- **When** `tech-lead` checks the safety line
- **Then** it is not accepted: a fact is stated and raised above level 1, or marked `unproven`

#### <a id="TL-004"></a>TL-004 — Bug fix checks callers and the fix's safety fact

**Kind:** ✅ happy · **Change:** 🆕 added

- **Given** a bug with a root cause found
- **When** Bug step 3 runs
- **Then** it lists the other callers and states the safety fact of the planned fix

### <a id="TL-R2"></a>TL-R2 — Premise rule

**Change:** 🆕 added

> After two failed fixes or hypotheses built on the same assumption, `tech-lead` **SHALL** state that assumption and
> make an observation that would differ if it were false before trying a third.

#### <a id="TL-005"></a>TL-005 — Two failures on one assumption

**Kind:** ⚠️ edge · **Change:** 🆕 added

- **Given** two hypotheses or fixes of one bug that shared an assumption have failed
- **When** the investigation continues
- **Then** the assumption is written in one sentence, the observation that would refute it is named and made, and no
  third fix is proposed before that

### <a id="TL-R3"></a>TL-R3 — Performance path

**Change:** 🆕 added

> A request that something is slow **SHALL** follow the Performance path: claim, baseline, limiter, plan, after,
> report — with a verdict backed by a number, its run count and range.

#### <a id="TL-006"></a>TL-006 — "X is slow"

**Kind:** ✅ happy · **Change:** 🆕 added

- **Given** the user says an export is slow
- **When** `tech-lead` runs
- **Then** it follows the Performance path and the report gives the verdict, the number with its unit, run count,
  range and limiter

#### <a id="TL-007"></a>TL-007 — Inconclusive measurement

**Kind:** ❌ error · **Change:** 🆕 added

- **Given** a measurement without a named limiter, with a side run untuned, or without checking errors and that the
  work ran
- **When** the report is written
- **Then** the verdict is `inconclusive` with the reason

#### <a id="TL-008"></a>TL-008 — Difference within the noise

**Kind:** ⚠️ edge · **Change:** 🆕 added

- **Given** the after-measurement differs from the baseline by less than the run-to-run range
- **When** the report is written
- **Then** the verdict is "no measurable difference" and the change is reverted

#### <a id="TL-009"></a>TL-009 — Deferred performance problem

**Kind:** ✅ happy · **Change:** 🆕 added

- **Given** the user does not fix the measured problem now
- **When** `tech-lead` offers to save it
- **Then** the issue has kind `perf`, the claim, the baseline and the limiter as evidence

**Module:** [fix](../../../../skills/fix/SKILL.md)

#### <a id="FIX-001"></a>FIX-001 — Direct fix carries a safety fact

**Kind:** ✅ happy · **Change:** 🆕 added

- **Given** an `S` issue without a contract change
- **When** `fix` shows the short plan
- **Then** the plan has a `**Safe because:**` line

#### <a id="FIX-002"></a>FIX-002 — Performance issue

**Kind:** ✅ happy · **Change:** 🆕 added

- **Given** an issue of kind `perf`
- **When** `fix` takes it
- **Then** it follows the `tech-lead` Performance path from its claim and baseline

**Module:** [review](../../../../skills/review/SKILL.md)

### <a id="REV-R1"></a>REV-R1 — Prove step

**Change:** 🆕 added

> After Verify, `review` **SHALL** offer once to prove every `plausible` Must and Should and every `confirmed` Must by
> a test or script that runs, and report each as `proven`, `refuted` or unchanged with the evidence.

#### <a id="REV-001"></a>REV-001 — One question with the cost

**Kind:** ✅ happy · **Change:** 🆕 added

- **Given** a review with at least one `plausible` Must or Should
- **When** Verify ends
- **Then** the user is asked once, with the number of findings and subagents, yes recommended

#### <a id="REV-002"></a>REV-002 — Nothing to prove

**Kind:** ⚠️ edge · **Change:** 🆕 added

- **Given** no `plausible` Must or Should and no `confirmed` Must
- **When** Verify ends
- **Then** the Prove step is skipped without a question

#### <a id="REV-003"></a>REV-003 — Test shows the failure

**Kind:** ✅ happy · **Change:** 🆕 added

- **Given** a finding whose failure scenario a test can show
- **When** its prover's test fails as the finding predicts
- **Then** the finding is `proven`, reported with the command, the output it printed and the output the goal requires

#### <a id="REV-004"></a>REV-004 — Passing test without reach

**Kind:** ⚠️ edge · **Change:** 🆕 added

- **Given** a prover's test passes
- **When** it has no evidence that the scenario reached the code in question
- **Then** the finding stays `plausible`

#### <a id="REV-005"></a>REV-005 — Passing test that reached the code

**Kind:** ✅ happy · **Change:** 🆕 added

- **Given** a prover's test passes
- **When** an assertion that holds only on that path, or line coverage, shows the scenario reached the code
- **Then** the finding moves to `refuted` and is counted

#### <a id="REV-006"></a>REV-006 — No cheap test path

**Kind:** ⚠️ edge · **Change:** 🆕 added

- **Given** a finding about a race or an external system
- **When** its prover finds no cheap test path
- **Then** the result is `unprovable` with the reason and the finding keeps its status

#### <a id="REV-007"></a>REV-007 — PR tree left clean

**Kind:** ❌ error · **Change:** 🆕 added

- **Given** a review in PR mode that ran the Prove step
- **When** the review ends
- **Then** no file the review added remains in the reviewed tree, and the posted comment of a `proven` finding is a
  statement with the test and its output

#### <a id="REV-008"></a>REV-008 — Tests do not run in the review worktree

**Kind:** ❌ error · **Change:** 🆕 added

- **Given** PR mode and a test command that does not run in the review worktree
- **When** the user declines installing dependencies
- **Then** the Prove step is skipped and listed under "not checked"

#### <a id="REV-009"></a>REV-009 — Proven finding in branch mode

**Kind:** ✅ happy · **Change:** 🆕 added

- **Given** a `proven` finding in branch mode
- **When** the user chooses to fix it
- **Then** the fix starts from its test; a `proven` finding not fixed has its test removed from the tree and the test
  code in the issue's evidence

#### <a id="REV-010"></a>REV-010 — Verdict with proven findings

**Kind:** ✅ happy · **Change:** 🆕 added

- **Given** a `proven` or `confirmed` Must
- **When** the report is written
- **Then** the verdict is `fix first`

#### <a id="REV-011"></a>REV-011 — Prover writes only new files

**Kind:** ⚠️ edge · **Change:** 🆕 added

- **Given** a prover whose test does not compile
- **When** it repairs it (at most twice)
- **Then** it edits only the files it created, never an existing file

**Module:** [deliver](../../../../skills/deliver/SKILL.md)

#### <a id="DLV-006"></a>DLV-006 — A fixed problem comes back

**Kind:** ⚠️ edge · **Change:** 🆕 added

- **Given** a finding, QA failure or issue fixed in this run comes back for the first time
- **When** the loop picks the next stage
- **Then** one more Fix stage runs under the premise rule, and the assumption and its test are in the run log

#### <a id="DLV-007"></a>DLV-007 — It comes back again

**Kind:** ❌ error · **Change:** 🆕 added

- **Given** the problem comes back after that Fix stage
- **When** the loop records it
- **Then** it is saved as an issue; a feature run stops, an issues run skips the issue and goes on

#### <a id="DLV-008"></a>DLV-008 — Mutation check of new tests

**Kind:** ✅ happy · **Change:** 🆕 added

- **Given** a Finish stage that writes a test of an `error` or `edge` scenario
- **When** the stage ends
- **Then** the test has a recorded mutation result and every mutated production file has its original hash

#### <a id="DLV-009"></a>DLV-009 — Weak test

**Kind:** ⚠️ edge · **Change:** 🆕 added

- **Given** a new test that still passes with the behaviour broken
- **When** a strengthened assertion, derived from the scenario, still passes
- **Then** an `add-tests` issue `p3` is saved and the scenario does not count as covered

#### <a id="DLV-010"></a>DLV-010 — Stage dies mid-mutation

**Kind:** ❌ error · **Change:** 🆕 added

- **Given** a copy of a production file left in `${TMPDIR:-/tmp}/as-mutation/<tree>/`
- **When** the loop starts its next stage
- **Then** the Tree step restores the file, checks its recorded hash and only then looks at uncommitted changes

#### <a id="DLV-011"></a>DLV-011 — Prove without asking

**Kind:** ✅ happy · **Change:** 🆕 added

- **Given** a review inside a stage with a `plausible` Must or Should
- **When** the policy answers the Prove question
- **Then** the step runs; `proven` → fixed, `disproved` → dropped, `unprovable` → `p4` issue "unconfirmed by as:review"

#### <a id="DLV-012"></a>DLV-012 — Performance issues wait for a human

**Kind:** ⚠️ edge · **Change:** 🆕 added

- **Given** an open issue of kind `perf`
- **When** an issues run selects its issues
- **Then** it is not selected and the report lists it

**Module:** [finish](../../../../skills/finish/SKILL.md)

#### <a id="FIN-002"></a>FIN-002 — Finish follows the Prove step

**Kind:** ✅ happy · **Change:** 🆕 added

- **Given** `finish` step 4 with a `plausible` Must finding
- **When** it follows `review`
- **Then** it runs steps 2–8 of `review`, the Prove question included

## Plan

### Milestone A — Working principles v3 and the premise rule

- [x] **1. Principles v3** — `skills/init/references/working-principles.md` marker `v3` + two lines (premise: two
  fixes of one failure failed → write the shared assumption and test it before a third; tests: assert what callers
  observe, expected value from the requirement). Same block in root `AGENTS.md`. `tests/test_scripts.py`: fixture of
  `test_doctor_reports_outdated_and_broken_setup` to `v2`, expect `v2, current is v3`; edge test expects
  `this plugin's v3`. [WP-001](#WP-001). `doctor.py` reads the marker from the reference — no code change.
- [x] **2. Premise rule in tech-lead** — `skills/tech-lead/SKILL.md` Bug step 2. [TL-005](#TL-005).
- [x] **3. deliver: one more Fix stage** — `skills/deliver/SKILL.md` step 3 "no progress": first return → saved as
  a run issue and one Fix stage under the premise rule (stage brief gets a `Premise:` field with the earlier fixes;
  assumption and its test in the run log); second return → issue; feature run stops, issues run skips it like
  blocked. `references/autopilot.md`: stage brief field, report note. [DLV-006](#DLV-006), [DLV-007](#DLV-007).
- [x] **4. Mutation check** — `autopilot.md` finish → Contract tests: per new `error`/`edge` test, backup to
  `${TMPDIR:-/tmp}/as-mutation/<tree>/<path>` + `git hash-object`, smallest breaking edit, run only that test (else
  the module's command, reading that test's result), restore, hash must match (mismatch fails the stage); survives →
  strengthen once from the scenario; still survives → `add-tests` `p3` issue, not counted covered. Result recorded in
  the stage report. `deliver` step 2.1 Tree: restore anything in the backup dir and check hashes first.
  Interactive `finish` step 7 unchanged. [DLV-008](#DLV-008)…[DLV-010](#DLV-010).
- [x] **5. Docs A + checks** — `README.md` (init principles, deliver), `skills/README.md` deliver row, `CHANGELOG.md`
  1.19.0 entry (started), validate, pytest.

### Milestone B — Safety fact

- [x] **6. Reference** — new `skills/tech-lead/references/safety-fact.md`: the one fact (callers list is not it),
  levels 1–5, level 4 required outside the type system (wire/file format, DB column/constraint, consumed event,
  library at pinned version, lifecycle order), "where the search stops" checklist, line format
  `**Safe because:** <fact> — level <n> — <evidence>` or `unproven` + cheapest check; scripts written in a temp dir
  outside the repo while planning, become the change's test or are deleted with command and output kept in the plan.
- [x] **7. Use it** — `tech-lead` Size S short plan; Bug step 3 (callers check + safety fact of the planned fix);
  `fix` step 4 for a direct `S` fix; `autopilot.md` fix line: `unproven` → run the cheapest check, still unproven →
  assumption. [TL-001](#TL-001)…[TL-004](#TL-004), [FIX-001](#FIX-001).
- [x] **8. Docs B + checks** — README tech-lead/fix, `skills/README.md` rows, CHANGELOG, validate, pytest.

### Milestone C — Prove step in review

- [x] **9. review procedure** — `skills/review/SKILL.md`: new step 6 Prove (Report 7, Act 8, Summary 9); candidates,
  one question with counts, one prover per finding (branch: working tree, sequential; PR: review worktree, install
  question as `worktree-create` step 6, declined → skipped, "not checked"); results `proven` / `disproved` → refuted
  with evidence of reach / `unprovable`; statuses `proven, confirmed, plausible, refuted`; verdict `fix first` on
  proven or confirmed Must; Act branch (fix starts from the test; unfixed proven → test removed, code to issue
  evidence; disproved test removed unless kept); Act PR (proven comment is a statement with test and output;
  `REQUEST_CHANGES` with proven or confirmed Must; `git status --porcelain` before/after, every added file deleted).
  Judgement-subagent line includes provers. Description tightened to fit "proves findings by running a test" ≤ 1024.
  [REV-001](#REV-001)…[REV-011](#REV-011).
- [x] **10. Prover brief** — `skills/review/references/briefs.md`: header corrected (reviewers and verifiers
  read-only; prover adds only new test files), fenced `text` brief with `{placeholders}`, exact return sections
  (result, command, printed output, required output, reach evidence, files created, reason).
- [x] **11. Host mappings** — `references/claude-tools.md` (prover = judgement subagent, `general-purpose`, may add
  test files and run the test command; stronger-model opt-in covers it), `references/codex-tools.md` (without
  subagents the step runs in the main thread).
- [x] **12. Callers of review** — `finish` step 4 "steps 2–8"; `skills/AGENTS.md` (finish names review steps);
  `autopilot.md` review: run Prove without asking, `proven` → fix, `disproved` → dropped, `unprovable` → `p4`
  "unconfirmed by as:review"; fix every proven/confirmed Must and Should; `deliver` done criterion "no proven or
  confirmed Must". Grep every "step N" mention of review before and after. [DLV-011](#DLV-011), [FIN-002](#FIN-002).
- [x] **13. Docs C + checks** — README review section (steps 1–9), `skills/README.md` review row, `help` review topic,
  CHANGELOG, validate, pytest.

### Milestone D — Performance path and release

- [x] **14. Path** — `tech-lead` "Choose the path": Performance ("X is slow", "make Y faster", a measured
  regression); description gains the trigger by tightening (≤ 1024, no trigger dropped). New
  `skills/tech-lead/references/perf.md`: claim, baseline (≥ 5 runs, median, range, errors, work inside the timed
  region), limiter (profile or counters from an unreported run), plan (approval before code), after (same
  measurement, production-like, alternate A/B, ≥ 5 each; within range → revert), report (verdict first; inconclusive
  rules); measurement scripts in a temp dir outside the repo; deferred → `perf` issue.
  [TL-006](#TL-006)…[TL-009](#TL-009).
- [x] **15. `perf` kind** — `skills/issue/references/issue-format.md` kind list; `fix` step 4 routes `perf` to the
  Performance path; `deliver` step 1 and the run-issue definition exclude `perf` like `remove-tests`/`docs`.
  [FIX-002](#FIX-002), [DLV-012](#DLV-012).
- [x] **16. Release docs** — README (tech-lead Performance, pstack credit next to ponytail and ub-mode at line ~472),
  `skills/README.md` tech-lead row, `help` flows (Performance) and topics, `skills/AGENTS.md` if a dependency changed,
  `CHANGELOG.md` 1.19.0 complete, version 1.19.0 in `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`,
  `package.json`.
- [x] **17. Checks** — validate, pytest, `claude plugin validate .` (one expected CLAUDE.md warning), description
  lengths measured.

**Risks:** step numbers of `review` quoted in prose are not checked by the validator — grep before and after step 9;
descriptions at the limit — measure after each edit; a mutated production file left after a crash — fixed backup
path restored by Tree; prover files left in a tree — only new files, `git status` before/after.

**Verify:** done 2026-11-18 on a throwaway Python repository in `$TMPDIR` — the mechanics, run by hand, not a full skill run by a fresh agent: Prove — a planted wrong-sign discount gave `proven` (`uv run --with pytest python -m pytest -q tests/test_prove_discount.py` → `assert 2200 == 1800`, required 1800) after one repair of the prover's own import error; a check-then-act race gave a passing single-thread test with no proof of reach → stays `plausible`; the diff hash of existing files was unchanged and, after deleting the files the provers created, `git status --porcelain` equalled the record (AC3, AC4). Safety fact for renaming `total_cents` in a JSON response: level 4 — `git grep -n total_cents -- web` found `web/app.js:1` reading it and the script printed `['id', 'total_cents']`, so the fact "no client reads it" is false (AC2). Performance: `find_duplicates` on 4000 items, 5 runs each — 38.7 ms (38.0–44.6) → 0.15 ms (0.14–0.19), limiter the function's own time in cProfile, verdict faster (AC7). Not run: `review` end to end with subagents, PR mode against GitHub, `deliver` (AC5, AC6), Codex. Planned: dry-run on a throwaway sample repository in a temporary directory (not this repo): `review` with one
planted defect a test can show and one it cannot (AC3, AC4, PR-mode cleanup simulated on a local branch); one small
`tech-lead` change touching a JSON response (AC2); one "X is slow" request (AC7). `deliver` (AC5, AC6) is not run
unless time allows — the change will say so.

## Open questions

None. Settled with the user on 2026-11-18: see the decision.

---
