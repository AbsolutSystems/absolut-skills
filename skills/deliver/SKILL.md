---
name: deliver
description: "Deliver a whole documented feature unattended (for example overnight): after one round of start-up checks and questions, loops through the feature's roadmap without asking — plans each phase with as:tech-lead, implements it with as:implement, wraps it up with as:finish, fixes the issues the run saved with as:fix, and ends with a review of the whole branch — taking the recommended option at every point where those skills would ask and recording it as an assumption. Commits after every green stage on the feature branch, never pushes; stops when the done criteria hold (all phases done, checks green, spec lint OK, scenarios tested, no Must findings, no p1–p3 issues from the run), at a decision only a human may take, or at its limits. Writes a morning report to docs/features/<slug>/delivery.md. Use only when the user explicitly invokes as:deliver."
disable-model-invocation: true
argument-hint: "docs/features/<slug> [--max-stages <n>]"
---

# Deliver

Run the whole feature flow — plan, implement, finish, fix — in a loop until the feature is done, with nobody to ask.
This skill owns only the start-up checks, the loop, the commits and the report. Every stage follows another skill's
`SKILL.md` with the [autopilot policy](references/autopilot.md) in place of its questions. State lives in files (the
feature page, the proposals' `## Plan`, `docs/issues/`, git history), so a crashed or stopped run resumes with the same
command. Converse in the user's language. Host mechanics (subagents, permissions for an unattended run):
[Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `docs/features/<slug>` — the feature to deliver (written by `as:feature`). Without it → stop and suggest `as:feature`.
- `--max-stages <n>` — stop after this many stages (default 20; a phase usually takes 3–5).

## Procedure

### 1. Start-up (the only step that asks)

The user is still here: settle everything now, then never ask again.

- **Feature** — read the page ([format](../feature/references/feature-format.md)). Phases `⏳ planned` or `🔄 in progress`
  are the work; none → stop, nothing to deliver. No `docs/spec/` → stop and suggest `as:spec-docs` for the feature's
  modules: finish merges each phase into the module pages. Run `spec_lint.py` (as in `feature` step 6); any error →
  stop and say which skill fixes it (`as:feature`, `as:spec-docs`) — the done criteria need it `OK`.
- **Open questions** — the page's `## Open questions` and the open client questions of a linked estimate. For each,
  propose the answer you would recommend, with a reason, and ask in one batch: confirm or correct. Answers are not
  written to the page (that is `as:feature`'s job); they go to the report as start-up decisions and bind every stage.
  A question the user leaves open is decided by the policy at the stage that needs it.
- **Branch** — on the default branch → offer `deliver/<slug>` (or `as:worktree-create`). Uncommitted changes on a
  new run → ask to commit or stash them first; the run commits stage by stage and must not mix in foreign changes (on
  a resume they are an interrupted stage: leave them to the loop). Record the base (`git merge-base HEAD origin/HEAD`,
  else the default branch).
- **Checks** — the test, lint, type-check and build commands from the relevant `AGENTS.md` files; none documented →
  ask for them. Run them: anything red → stop. A run that starts on red cannot tell its own breakage from the old.
- **Host** — the run must not stall on permission prompts: check the setup described in the host mapping and tell the
  user what is missing.
- **Resume** — `delivery.md` already exists → read its base, start-up decisions, stages and stop reason; ask only
  about new open questions; say where the run continues.

Show the plan: phases to deliver, the done criteria ([step 4](#4-done)), the limits, and that it commits locally
without pushing. Ask once to start. Then write the header of `delivery.md` (base, branch, start-up decisions; format in
[references/autopilot.md](references/autopilot.md#report)) and commit it — every stage reads it. From here on, ask
nothing: questions are answered by the policy.

### 2. Loop

Each stage starts from the files, not from memory — re-read them every time (the conversation may have been compacted):

1. **Tree** — uncommitted changes at the start of a stage mean an interrupted stage: run the checks; green → commit
   them as that stage, red → a repair stage (below).
2. **Pick the next stage**, first match wins:

   | State | Stage | Follows |
   |-------|-------|---------|
   | run proposal without `## Plan` | **Plan** — complete it with a `## Plan` | [tech-lead From feature](../tech-lead/SKILL.md#from-feature) |
   | run proposal with unticked `## Plan` steps | **Implement** the next milestone (the whole plan when it has none) | [implement](../implement/SKILL.md) |
   | run proposal, all steps ticked | **Finish** — simplify, review, merge and archive, contract tests, docs | [finish](../finish/SKILL.md) |
   | issues added on this branch (`git diff --name-only --diff-filter=A <base> -- docs/issues`) with `p1`–`p3`, not named by an open proposal | **Fix** — the first by priority (several `S` of one module together) | [fix](../fix/SKILL.md) |
   | a `⏳ planned` phase | **Plan** the first one: proposal, scenarios, `## Plan` | [tech-lead From feature](../tech-lead/SKILL.md#from-feature) |
   | none of the above, and the last stage was not a final review that came back clean | **Final review** of the whole branch diff from base | [review](../finish/references/review.md) |
   | none | done → [step 4](#4-done) | |

   A **run proposal** is an open proposal in `docs/spec/changes/` with this feature's `**Feature:**` meta line, or one
   added on this branch (`git diff --name-only --diff-filter=A <base> -- docs/spec/changes`, e.g. by a Fix stage).

3. **Run the stage** in a fresh subagent with the brief from [references/autopilot.md](references/autopilot.md#stage-brief)
   (no subagents → run it in the main thread). The main thread keeps only the returned report.
4. **Verify** — rerun the checks yourself; do not trust the stage report alone. Red → one **repair** stage (brief with
   the failing output, goal: green without weakening a test). Still red → set the stage's changes aside with
   `git stash push -u -m "as:deliver <stage>"` (nothing is lost) and stop.
5. **Log** — append the stage to `delivery.md` ([format](references/autopilot.md#report)): stage, result,
   assumptions, issues saved and closed.
6. **Commit** — stage the files of the report's Changes and `docs/` (`git add -A -- <paths>`, deletions included) and
   commit `as:deliver(<slug>): <stage> — <one line>`, with the stage's assumptions and
   issues in the body. Other files the stage left (coverage output, traces, a generated `.env`) stay uncommitted and are
   listed in the log. Every stage commits at least its log line, so `git log <base>..` is the run's history.

### 3. Stop conditions

Stop the loop (then [step 5](#5-report)) when:

- a stage returns **blocked** — a decision the policy reserves for a human
  ([list](references/autopilot.md#human-only-decisions)); later phases depend on earlier ones, so the run stops;
- the checks stay red after the repair stage;
- **no progress** — a stage other than a clean final review changed nothing but its log line, or a review finding or issue already fixed in this run
  comes back (record it as an issue and stop instead of looping);
- `--max-stages` is reached.

Never: push, merge, rebase, amend or reset commits, delete branches, edit `sources/`, change or remove acceptance
criteria or non-goals, drop a phase, or weaken a test or a scenario to make it pass.

### 4. Done

All must hold; check each with its command, not from the stage reports:

- every roadmap phase is `✅ done` or `🗑️ dropped` and no run proposal is open;
- the checks from step 1 are green;
- `spec_lint.py` prints `OK`;
- every scenario added or changed by this run's proposals (archived since base) has a test with its ID
  (`git grep -n '<ID>'` over the test directories), `error` and `edge` ones included;
- the final review found no Must finding left unfixed;
- no `p1`–`p3` issue added on this branch is left open.

A criterion that fails while a row of the stage table still matches → back to the loop, within the limits. One that
fails with no row left (a scenario without a test whose issue is `p4`, a lint error outside the run) → stop and report
it.

### 5. Report

Finish `delivery.md`: result (done / stopped and why), the done criteria with ✅/❌, phases delivered with their
archived proposals, **assumptions to review** (start-up decisions plus every `Assumed by as:deliver` note in
the run's proposals), issues saved and closed, set-aside changes (stash name), open `**Rollout:**` and `**Verify:**`
items. Commit it. In the conversation: the same in a few lines, where to start the review (assumptions first), and next
steps: read `git log <base>..` (the commits), then `/commit-commands:commit-push-pr` (Claude Code, if installed); after a stop, fix the
cause and rerun `as:deliver docs/features/<slug>` — it resumes.
