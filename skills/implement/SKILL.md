---
name: implement
description: "Implement the approved plan of a change proposal (docs/spec/changes/<slug>.md, written by as:tech-lead), resuming in any session: finds the branch's proposal, takes the first unticked step of its ## Plan, writes tests first for error and edge scenarios, implements, runs the checks, ticks the step and continues; stops and asks before deviating from the plan. Does not commit. Use only when the user explicitly invokes as:implement."
disable-model-invocation: true
argument-hint: "[slug] [--step <n>]"
---

# Implement

Execute an approved plan. The contract is the proposal file, not the conversation: everything needed is in its
scenarios and `## Plan`, so a new session (or a cheaper model) can continue where the previous one stopped. Design
decisions are not reopened here — that is `as:tech-lead`. Answer in the user's language. Host mechanics:
[Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `[slug]` — the proposal to implement (default: the one belonging to this branch, see step 1).
- `--step <n>` — start at this step instead of the first unticked one.

## Procedure

1. **Find the proposal** — open proposals in `docs/spec/changes/*.md` whose slug is in the branch name or commit
   messages since the merge-base with the default branch; several or none → list them and ask. No `## Plan` section →
   stop and suggest `as:tech-lead`. Read the proposal, the `AGENTS.md` files of its modules and the linked spec pages.
2. **Baseline** — run the test commands from the relevant `AGENTS.md` files. Failures → report and ask whether to
   continue (they would hide the effect of the steps).
3. **Next step** — the first unticked `- [ ]` step (or `--step <n>`); within milestones, in order. Say which step and
   which scenario IDs it covers.
4. **Implement the step**:
   - tests first for the step's `error` and `edge` scenarios, through the module's public entry points, with the
     scenario ID in the test name or tag; run them and see them fail for the right reason;
   - then the code, reusing what the plan names; then the remaining tests of the step;
   - rerun the module's tests (and lint/type-check/build if documented); fix until green.
5. **Tick** — mark the step `- [x]` in the proposal. A milestone is done when its tests pass; say so before the next.
6. **Deviations** — when the plan is wrong or incomplete (a missing step, a different file, a scenario that cannot
   hold), stop: show the problem with evidence and propose an edit to `## Plan` (or to the scenarios). Edit the
   proposal only after approval, then continue. Never silently implement something other than the plan.
   A problem outside the plan noticed on the way (a bug in nearby code, a missing test) is not fixed in passing:
   offer to save it as an issue per [../issue/references/issue-format.md](../issue/references/issue-format.md).
7. Repeat 3–6 until no step is unticked, or the user stops. Ask before continuing past each milestone.
8. **Summary** — steps done, tests added (with scenario IDs), plan edits, issues saved, open items (unticked steps,
   `**Verify:**` and `**Rollout:**` from the proposal). Do not commit. Next: `as:finish` — it checks the code against the proposal and
   merges it into the spec.
