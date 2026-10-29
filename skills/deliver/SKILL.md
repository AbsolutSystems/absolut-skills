---
name: deliver
description: "Deliver unattended (for example overnight) a whole documented feature, or the known problems saved in docs/issues/: after one round of start-up checks and questions, loops without asking — plans each feature phase with as:tech-lead, implements it with as:implement, wraps it up with as:finish, fixes issues with as:fix, ends with a review of the whole branch and, when docs/qa/ exists, a browser check with as:qa whose failures it fixes — taking the recommended option at every point where those skills would ask and recording it as an assumption. Commits after every green stage on its branch, never pushes; stops when the done criteria hold (all phases done or all selected issues closed, checks green, spec lint OK, scenarios tested, no Must findings, no p1–p3 issues from the run, last QA run without FAIL), at a decision only a human may take, or at its limits. Writes a morning report (docs/features/<slug>/delivery.md, or docs/deliveries/<branch>.md for issues). Use only when the user explicitly invokes as:deliver."
disable-model-invocation: true
argument-hint: "docs/features/<slug> | docs/issues [request] [--max-stages <n>]"
---

# Deliver

Run the whole flow — plan, implement, finish, fix — in a loop until the target is done, with nobody to ask. The target
is a documented feature (its roadmap) or the known problems in `docs/issues/`. This skill owns only the start-up
checks, the loop, the commits and the report. Every stage follows another skill's `SKILL.md` with the
[autopilot policy](references/autopilot.md) in place of its questions. State lives in files (the feature page,
`docs/issues/`, the proposals' `## Plan`, the report, git history), so a crashed or stopped run resumes with the same
command. Converse in the user's language. Host mechanics (subagents, permissions for an unattended run):
[Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `docs/features/<slug>` — **feature run**: deliver the feature's roadmap (page written by `as:feature`).
- `docs/issues [request]` — **issues run**: fix the open issues, optionally filtered by a request in the user's words
  as in [fix](../fix/SKILL.md) (`all p1`, `bugs in orders`, `10 most important`). No request → all open issues.
- No target → stop and suggest `as:feature` (a feature) or `as:issue` (save problems first).
- `--max-stages <n>` — stop after this many stages (default 20 for a feature, 40 for issues; a phase or an `M`/`L`
  issue usually takes 3–5, an `S` issue 1).

## Procedure

### 1. Start-up (the only step that asks)

The user is still here: settle everything now, then never ask again.

- **Feature run** — read the page ([format](../feature/references/feature-format.md)). Phases `⏳ planned` or
  `🔄 in progress` are the work; none → stop, nothing to deliver. No `docs/spec/` → stop and suggest `as:spec-docs`
  for the feature's modules: finish merges each phase into the module pages.
- **Issues run** — load the open issues and order them as [fix](../fix/SKILL.md) step 2 does (priority, effort, date),
  filtered by the request. Unlike fix step 1, keep the issues named by the `**Issue:**` line of an open proposal: mark
  them with the proposal, which becomes part of the run (the loop continues it).
  `remove-tests` and `docs` issues need a human or another skill → not selected; list them. Show the table (file,
  kind, priority, effort, module, title) and ask which to take (multi-select, all preselected). None → stop.
- **Spec lint** — when `docs/spec/` or `docs/features/` exists, run `spec_lint.py` (as in `feature` step 6); any error →
  stop and say which skill fixes it (`as:feature`, `as:spec-docs`) — the done criteria need it `OK`.
- **Open questions** — feature run: the page's `## Open questions` and the open client questions of a linked estimate;
  issues run: the selected `M`/`L` issues whose suggested fix leaves a choice open. For each, propose the answer you
  would recommend, with a reason, and ask in one batch: confirm or correct. Answers are not written to the page or the
  issue; they go to the report as start-up decisions and bind every stage. A question the user leaves open is decided
  by the policy at the stage that needs it.
- **Branch** — on the default branch → offer `deliver/<slug>` (`deliver/issues-<date>` for issues, or
  `as:worktree-create`). Uncommitted changes on a new run → ask to commit or stash them first; the run commits stage
  by stage and must not mix in foreign changes (on a resume they are an interrupted stage: leave them to the loop).
  Record the base (`git merge-base HEAD origin/HEAD`, else the default branch).
- **Checks** — the test, lint, type-check and build commands from the relevant `AGENTS.md` files; none documented →
  ask for them. Run them: anything red → stop. A run that starts on red cannot tell its own breakage from the old.
- **Host** — the run must not stall on permission prompts: check the setup described in the host mapping and tell the
  user what is missing.
- **QA** — when `docs/qa/index.md` exists ([qa](../qa/SKILL.md) step 1): the host has a browser tool, the app
  answers on the `local` environment of `index.md` or its `Start` command brings it up, and the accounts' environment
  variables are set. The QA stage always uses `--env local`; no `local` row → QA is skipped. Anything missing → say that QA will be skipped and why; the report marks the QA criterion
  skipped, not failed. A non-local URL is never used unattended. No `docs/qa/` → no QA stage; suggest `as:qa-docs`
  for next time in one line.
- **Resume** — the report already exists (feature: `docs/features/<slug>/delivery.md`; issues:
  `docs/deliveries/<branch>.md` for the current branch) → read its base, start-up decisions,
  selected and skipped issues, stages and stop reason; ask only about new open questions; say where the run continues.

Show the plan: phases or issues to deliver, the done criteria ([step 4](#4-done)), the limits, and that it commits
locally without pushing. Ask once to start. Then write the header of the report (base, branch, start-up decisions, for
issues the selected list; format in [references/autopilot.md](references/autopilot.md#report)) and commit it — every
stage reads it. From here on, ask nothing: questions are answered by the policy.

### 2. Loop

Each stage starts from the files, not from memory — re-read them every time (the conversation may have been compacted):

1. **Tree** — uncommitted changes at the start of a stage mean an interrupted stage: run the checks; green → commit
   them as that stage, red → a repair stage (below).
2. **Pick the next stage**, first match wins:

   | State | Stage | Follows |
   |-------|-------|---------|
   | run proposal without `## Plan` | **Plan** — complete it with a `## Plan` | [tech-lead From feature](../tech-lead/SKILL.md#from-feature); a proposal with `**Issue:**` and no `**Feature:**`: [tech-lead Feature](../tech-lead/SKILL.md#feature) |
   | run proposal with unticked `## Plan` steps | **Implement** the next milestone (the whole plan when it has none) | [implement](../implement/SKILL.md) |
   | run proposal, all steps ticked | **Finish** — simplify, review, merge and archive, contract tests, docs | [finish](../finish/SKILL.md) |
   | run issue not named by an open proposal | **Fix** — the first by priority (several `S` of one module together) | [fix](../fix/SKILL.md) |
   | feature run: a `⏳ planned` phase | **Plan** the first one: proposal, scenarios, `## Plan` | [tech-lead From feature](../tech-lead/SKILL.md#from-feature) |
   | none of the above, and no final review came back clean since the last stage that changed code | **Final review** of the whole branch diff from base | [review](../finish/references/review.md) |
   | none of the above, QA not skipped at start-up, and no QA stage since that clean final review | **QA** — `docs/features/<slug>` (feature run) or `branch <base>` (issues run) | [qa](../qa/SKILL.md) |
   | none | done → [step 4](#4-done) | |

   A stage **changed code** unless it was a final review that came back clean or a QA stage (they add only the log,
   the QA report and issues).

   A **run issue** is an open issue that is selected in the report (issues run), or added on this branch
   (`git diff --name-only --diff-filter=A <base> -- docs/issues`) with `p1`–`p3` — not skipped in the report and not
   of kind `remove-tests` or `docs` (those wait for a human; the report lists them).
   A **run proposal** is an open proposal in `docs/spec/changes/` with this feature's `**Feature:**` meta line, one
   whose `**Issue:**` names a run issue, or one added on this branch (`git diff --name-only --diff-filter=A <base> --
   docs/spec/changes`, e.g. by a Fix stage) — unless its issue is skipped.

3. **Run the stage** in a fresh subagent with the brief from [references/autopilot.md](references/autopilot.md#stage-brief)
   (no subagents → run it in the main thread). The main thread keeps only the returned report. The **QA** stage
   runs in the main thread instead — a stage subagent cannot start the executor and judge subagents `qa` needs —
   following [qa](../qa/SKILL.md) with the policy; the app is restarted with its `Start` command first when it does
   not reload changed code by itself. The loop keeps only the result counts, the report path and the issues.
4. **Verify** — rerun the checks yourself; do not trust the stage report alone. Red → one **repair** stage (brief with
   the failing output, goal: green without weakening a test). Still red → set the stage's changes aside with
   `git stash push -u -m "as:deliver <stage>"` (nothing is lost); a feature run stops, an issues run skips the issue
   (step 3) and goes on.
5. **Log** — append the stage to the report ([format](references/autopilot.md#report)): stage, result,
   assumptions, issues saved, closed and skipped.
6. **Commit** — stage the files of the report's Changes and `docs/` (`git add -A -- <paths>`, deletions included) and
   commit `as:deliver(<slug>): <stage> — <one line>` (`as:deliver(issues)` for an issues run), with the stage's
   assumptions and issues in the body. Other files the stage left (coverage output, traces, a generated `.env`) stay
   uncommitted and are listed in the log. Every stage commits at least its log line, so `git log <base>..` is the
   run's history.

### 3. Stop conditions

Stop the loop (then [step 5](#5-report)) when:

- a stage returns **blocked** — a decision the policy reserves for a human
  ([list](references/autopilot.md#human-only-decisions)). A feature run stops: later phases depend on earlier ones.
  An issues run skips the issue instead: stash the stage's changes as in step 2.4, add the issue with the question to
  the report's skipped list (the loop no longer picks it or its proposal), commit the log and go on;
- the checks stay red after the repair stage (an issues run skips the issue, as above);
- **no progress** — a stage other than a clean final review or a QA stage changed nothing but its log line, or a review finding, QA failure or
  issue already fixed in this run comes back (record it as an issue and stop instead of looping);
- `--max-stages` is reached.

Never: push, merge, rebase, amend or reset commits, delete branches, edit `sources/`, change or remove acceptance
criteria or non-goals, drop a phase, delete an issue that is not fixed, or weaken a test or a scenario to make it pass.

### 4. Done

All must hold; check each with its command, not from the stage reports:

- feature run: every roadmap phase is `✅ done` or `🗑️ dropped`; issues run: every selected issue is deleted or
  skipped in the report — and no run proposal is open;
- the checks from step 1 are green;
- `spec_lint.py` prints `OK` (when it ran at start-up);
- every scenario added or changed by this run's proposals (archived since base) has a test with its ID
  (`git grep -n '<ID>'` over the test directories), `error` and `edge` ones included;
- the final review found no Must finding left unfixed;
- no `p1`–`p3` issue added on this branch is left open, except skipped ones;
- when QA was not skipped: the report written by the run's last QA stage (named in its log line) has no `FAIL`.

A criterion that fails while a row of the stage table still matches → back to the loop, within the limits. One that
fails with no row left (a scenario without a test whose issue is `p4`, a lint error outside the run) → stop and report
it.

### 5. Report

Finish the report: result (done / stopped and why), the done criteria with ✅/❌, phases delivered or issues closed with
their archived proposals, **assumptions to review** (start-up decisions plus every `Assumed by as:deliver` note in the
run's proposals), issues saved, closed and skipped (with the question for each), set-aside changes (stash names), open
`**Rollout:**` and `**Verify:**` items, the last QA run report (or why QA was skipped) with its `OUTDATED` and
`BLOCKED` checkpoints for `as:qa-docs`. Commit it. In the conversation: the same in a few lines, where to start the
review (assumptions and skipped issues first), and next steps: read `git log <base>..` (the commits), then
`/commit-commands:commit-push-pr` (Claude Code, if installed); after a stop, fix the cause and rerun the same
`as:deliver` command — it resumes.
