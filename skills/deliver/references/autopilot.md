# Autopilot policy

How the stages of `as:deliver` follow the other skills with nobody to ask. The skills stay as they are; this policy
replaces their questions and approval gates.

## The rule

Wherever a followed skill says **ask**, **approve**, **confirm** or **offer**, do not ask: take the option the skill
would recommend — the recommended option, the preselected items, the smaller and more reversible change, the one that
keeps the existing contract — and record it as an assumption:

- in the proposal, as a note under `## Open questions`:
  `> [!NOTE]` / `> Assumed by as:deliver: <question> — <choice>, because <reason>.`
- outside a proposal (finish, fix, review), in the stage report; the loop writes it to `delivery.md`.

Start-up decisions from `delivery.md` and the feature page (acceptance criteria, non-goals, decisions) bind every
choice. An assumption never contradicts them.

## Human-only decisions

Do not assume these; return **blocked** with the question, the options and your recommendation:

- changing, adding or removing an acceptance criterion, a non-goal or a decision of the feature page;
- a contradiction between the feature page, its sources and the code that the page does not settle;
- deleting or irreversibly migrating user data;
- a new external service, paid dependency, licence or credential, or a security or permission model change not
  named by the feature page;
- breaking a contract used outside the repository (public API, event, file format) when the phase does not name it;
- a phase that cannot be delivered without one of the above.

## Per skill

**tech-lead** (Plan stage, [From feature](../../tech-lead/SKILL.md#from-feature)):

- Size: a feature phase always gets a change proposal with a `## Plan`, whatever its size (`as:finish` closes the
  phase through it).
- Clarify: answer from the page, its sources, the code and the start-up decisions; the rest by the rule.
- Options: run the architecture subagents when the size calls for them, then pick your recommendation; the table and
  the reason go to `## Decision` as usual.
- Write the proposal and its `## Plan` without the approval step; large changes get milestones. Set the phase
  `🔄 in progress`. No plan mode, no handoff — the loop implements it next.
- A change outside the roadmap → not this run: save it as an issue (`spec-gap`) instead of adding a phase.

**implement** (Implement stage): one milestone per stage (the whole plan without milestones). Baseline red → return
failed. A deviation that stays within the phase's scenarios and modules → edit `## Plan` (or the scenario) and record
the assumption; one that changes the scope → blocked. Do not ask between milestones — the stage ends at the milestone.

**finish** (Finish stage):

- Baseline red → return failed (the loop repairs it).
- Review: fix every Must and Should finding; save the ones still failing after one fix attempt as issues
  (Must → `p2`, `p1` for data or security; Should → `p3`); drop Nice findings.
- Spec: proposals of this branch are confirmed; ID collision → renumber to the next free IDs; scenarios not
  implemented → keep the proposal open and add an unticked `## Plan` step for each (the loop implements them). Drift explained by the proposal or the
  feature's acceptance criteria → intended; any other drift → unintended: fix the code. Unsure → keep the spec, save a
  `spec-gap` issue.
- `**Verify:**` — run it if it runs locally, else leave it as an open item for the report.
- Contract tests: cover every `MISSING` and `PARTIAL` scenario of the merged proposals and the new behaviour. A new
  test that fails because the code breaks its scenario → fix the code; a scenario that looks wrong → keep the test out
  of the diff and save a `spec-gap` issue. Never weaken an assertion.
- Agent docs: apply only facts the branch made false or necessary (commands, rules, pitfalls); skip the rest.
- A module named by the proposal without a spec page → create it with the `spec-docs` procedure for that module, so
  the proposal can merge; other touched modules without a page → note them for the report.
- Do not commit — the loop does.

**fix** (Fix stage): the issues the loop selected; no list, no choice. `S` without a contract change → fixed here,
test-first, issue deleted. `M`/`L` or a contract change → a proposal through the tech-lead path as above (the loop
implements and finishes it); its `**Issue:**` meta line closes the issue. Evidence gone → delete the issue.

**Final review**: review the whole diff from the base with the host review tool or
[../../finish/references/review.md](../../finish/references/review.md). Fix Must and Should findings as in finish,
rerun the checks; result `clean` only when no Must or Should finding was found.

**Issues** (any stage): saved per [../../issue/references/issue-format.md](../../issue/references/issue-format.md)
without asking, with `**Source:**` `as:deliver`, duplicates merged into the existing file. Out-of-plan problems in
nearby code are saved, never fixed in passing.

## Stage brief

```text
You are one stage of an unattended feature delivery (as:deliver). Nobody can answer questions.

Stage: {stage} — {target: proposal path, milestone, issue files, or base for the final review}
Feature page: docs/features/{slug}/index.md
Start-up decisions and earlier assumptions: {from delivery.md}
Checks: {test, lint, type-check, build commands}
Repair only: failing output of the previous attempt: {output}

Read {skill path}/SKILL.md and follow it for this stage only, with the policy in
{deliver skill path}/references/autopilot.md replacing every question and approval. If you cannot start subagents,
do their work yourself, in sequence. Run the checks before you return. Do not commit, push or switch branches.

Return exactly these sections:
- Result: done | blocked | failed (for the final review: clean | fixed)
- Changes: files changed and what each change does, in one line each
- Assumptions: each choice made by the policy, with its reason
- Issues: saved and deleted (file names)
- Checks: commands run and their result
- Blocked: the question, the options and your recommendation (only when blocked)
```

## Report

`docs/features/<slug>/delivery.md`, in the feature page's language. It is checked by `spec_lint.py` like the page:
link only files that stay — the feature page, archived proposals, the code; an open proposal (archived later) and
an issue (deleted when fixed) are named in backticks, not linked.

```markdown
# Delivery: Partial order cancellation

**Feature:** [Partial order cancellation](index.md) · **Branch:** `deliver/partial-cancel` · **Base:** `a1b2c3d` · **Started:** 2026-10-27 22:10

**Result:** ⏹️ stopped — a scenario without a test, its issue is p4.

## Done criteria

| Criterion | |
|-----------|-|
| All phases done, no open proposal | ✅ |
| Checks green | ✅ |
| `spec_lint.py` OK | ✅ |
| Added and changed scenarios tested | ❌ `ORD-016`, issue `p4-ord-016-scenario-unclear` |
| Final review without Must | ✅ |
| No p1–p3 issue from this run | ✅ |

## Assumptions to review

- Start-up: Q2 refunds go to the original payment method (confirmed by the user).
- [Phase 2 proposal](../../spec/changes/archive/2026-10-28-partial-cancel-refunds.md#open-questions): cancelling the
  last item cancels the order.

## Stages

| # | Stage | Result | Notes |
|---|-------|--------|-------|
| 1 | Plan phase 2 | done | `partial-cancel-refunds`, 2 assumptions |
| 2 | Implement milestone 1 | done | |

## Open items

- `**Rollout:**` deploy Billing first. Set aside: none.
```

The header (feature, branch, base, start) and the start-up decisions under `## Assumptions to review` are written
before the first stage; the stages table is appended stage by stage; the result, criteria, the rest of the assumptions
and open items at the end of the run (rewritten when a run resumes). Commits are in `git log <base>..`.
