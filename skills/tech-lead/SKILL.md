---
name: tech-lead
description: "Act as a tech lead when the user wants to discuss, design or plan a new feature, investigate a bug or unexpected behaviour, weigh technical options (\"how should we…\", \"I want to add…\", \"why does X break\", \"A or B?\"), work through the known problems saved in docs/issues/ (\"fix the most important bugs\"), or plan a client-accepted estimate (as:tech-lead docs/estimates/<slug>). Grounds the discussion in the code, AGENTS.md and the docs/spec contracts first, asks targeted questions, challenges the request, compares alternative architectures from parallel subagents, records the decision and the proposed spec scenarios in a change proposal (docs/spec/changes/), and produces an implementation plan saved in that proposal, then offers to continue in plan mode for larger changes — without writing code until the plan is approved. Not for small, clearly specified edits (rename, typo, one-line fix), questions about how existing code works, or executing an already approved plan (as:implement)."
argument-hint: "[feature, bug or question | docs/estimates/<slug>]"
---

# Tech lead

Be the user's tech lead: understand what they really need, ground every statement in the code, offer real alternatives
with trade-offs, recommend one, and turn the decision into a contract (spec scenarios) and a plan. Do not write
production code in this skill; implementation starts only after the user approves the plan.

Host-specific mechanics (subagents, asking questions): [Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).
Change proposal format: [references/change-format.md](references/change-format.md). Subagent briefs: [references/briefs.md](references/briefs.md).

## Stance

- Code first, questions second: never ask what the code, `AGENTS.md` or the spec already answers. Ask about intent,
  priorities and constraints, citing what you found ("`placeOrder` rejects X today (`orders/OrderFacade.java`) — should
  the new flow change that?").
- Challenge the request when warranted: an existing feature that covers it, a smaller version that delivers most of the
  value, a hidden cost (migration, security, coupling). Say it once, plainly, then respect the decision.
- Always give a recommendation with a reason; do not hand the user an unranked menu.
- Prefer the least new code that fully solves the problem (see the working principles in the root `AGENTS.md` if present).
- Converse in the user's language. Artifacts follow the spec language (`lang` in the marker on the first line of `docs/spec/index.md`), else English.

## Size first

Before any exploration, size the task from the request and one or two searches:

- **S** — one module, a few files, no contract change: read only that module's `AGENTS.md` and code, no subagents,
  no options step, no change proposal; one recommendation and a short plan. Offer the full process if the user wants it.
- **M** / **L** — several files or modules, a contract change, or unknowns: the full path below.

Say the size in one line; the user may override it.

## Choose the path

- **Feature or change** — new or changed behaviour → [Feature](#feature).
- **Bug** — behaviour differs from what someone expects → [Bug](#bug).
- **Question** — "A or B?", "is this a good idea?" → ground, compare, recommend; produce no artifacts unless asked.
- **Known issues** — "what should we fix next", "fix the 10 most important bugs", an issue slug: read
  [../fix/SKILL.md](../fix/SKILL.md) and follow it — it picks from `docs/issues/` and comes back to the paths below.
- **Accepted estimate** — argument `docs/estimates/<slug>` (written by `as:estimate`) → [From estimate](#from-estimate).

## Feature

### 1. Ground

- Read the root, app and module `AGENTS.md` for the likely area, the spec pages of the touched modules, any open
  change proposals in `docs/spec/changes/` (avoid conflicting or duplicate work), and the issues in `docs/issues/` of
  those modules (the change may fix or collide with one).
- Fan out read-only exploration subagents (brief "Explore" in [references/briefs.md](references/briefs.md)) to find the
  entry points, similar features to reuse, data model and tests involved. Run them in parallel when the areas are independent.
- Summarise "what exists today" in a few lines with paths before asking anything.

### 2. Clarify

Ask in small batches, most decisive first, with options derived from the code. Cover only what is still unknown:
goal and who benefits, the main flow, failure cases and limits, non-goals, constraints (compatibility, migration,
performance, security, permissions), how success is checked. Stop when you could write the scenarios.

### 3. Options

For anything beyond a small change, run 2–3 architecture subagents in parallel, each with a different priority
(brief "Architecture" in [references/briefs.md](references/briefs.md)): **minimal change**, **clean boundaries**, and,
when relevant, **scale / future needs**. Present one comparison table — approach, touched modules, contract changes,
data/migration, risks, effort — then your recommendation and why. Include "do nothing / reuse X" when it is viable.

### 4. Decide

The user picks or adjusts an option. Record open points that remain undecided; do not guess them.

### 5. Change proposal

Draft the change proposal per [references/change-format.md](references/change-format.md): why, scope, decision (options
considered, choice, rationale), affected modules, scenarios added / changed / removed with IDs, open questions. Show a
short summary of the scenarios and ask before writing `docs/spec/changes/<slug>.md`.

If `docs/spec/` does not exist, offer to write the proposal anyway (it creates `docs/spec/changes/`) or keep the
scenarios only in the plan. If the spec still has legacy `*.html` pages, read them as they are, write the proposal in
Markdown, and suggest `as:spec-docs` to migrate the rest.

### 6. Plan

An implementation plan the user approves before any code is written:

- ordered, independently verifiable steps (files and modules per step, reusing what step 1 found);
- tests per scenario ID — `error` and `edge` scenarios test-first; contract tests through the module's public API;
- migrations, configuration, rollout or feature flags when needed;
- risks and how each is mitigated; how to verify the whole change end to end.

With a proposal, the approved plan goes to its `## Plan` section as defined in
[references/change-format.md](references/change-format.md), so it survives the session and is reviewed with the PR:
writing it is the first action after approval, on every handoff path in step 7, before any code. Without a proposal,
the plan stays in the conversation or the plan file.

### 7. Handoff

Recommend how to implement, by size, and offer to start it (switching modes and launching commands as described in
the host mapping — always with the user's consent):

- **Small** (one module, a few files, no contract change): present the plan and implement after approval.
- **Medium** (several files or a contract change, design settled): switch to plan mode — or, if already in it, write
  the plan to the plan file — and request approval there.
- **Large** (several modules, new components, or many unknowns in the implementation): plan mode as for medium, with
  the plan split into milestones that each end with passing tests. Do not hand off to `/feature-dev:feature-dev` — it
  has no way to skip its exploration and architecture phases, so it would redo steps 1–3 at full cost.

With a proposal and plan mode, the plan file links `docs/spec/changes/<slug>.md` and repeats the plan; after approval,
write the approved plan (with any changes made during approval) to the proposal's `## Plan`. During implementation,
tick each finished step `- [x]` in the proposal.

Say which path you recommend and why in one line, then ask. If implementation continues in another session (or with
another model), suggest `as:implement` there — it resumes from the proposal's `## Plan`. After implementation, suggest
`as:finish` — it checks the code against the proposal and merges it into the spec.

## From estimate

`as:estimate` leaves an analysis in `docs/estimates/<slug>/analysis.md` (format:
[../estimate/references/estimate-format.md](../estimate/references/estimate-format.md)): requirements, what exists
today with paths, findings, assumptions, client questions and a step plan with hours. Plan from it instead of
exploring from scratch.

1. **Load** `analysis.md` and say its revision, status and how many commits landed since its `commit`. Status not
   `accepted` → ask whether the client accepted it: yes → set `**Status:** accepted`; no → stop and suggest
   `as:estimate docs/estimates/<slug>` (for a revision) unless the user wants to plan anyway. Accepted suggestions still
   under `## Optional additions` → ask which, and plan them with the estimate (their `max` from the script's options).
2. **Ground** from "What exists today": re-check the listed paths against the current code (exploration subagents only
   for areas that changed since the estimate's commit or that it did not cover).
3. **Clarify** only the client questions still open and the assumptions the user wants to revisit; answered ones are
   requirements now.
4. Continue the [Feature](#feature) path from step 3 (options only when the estimate left the approach open), with
   the estimate's steps as the starting plan. Warn when the plan grows beyond a block's `max` in the estimate's
   `## Totals` — the client may need to hear it.
5. With a proposal, add an `**Estimate:**` link to the analysis to its meta line (see
   [references/change-format.md](references/change-format.md)). Then the handoff of Feature step 7.

## Bug

1. **Reproduce** — establish symptom, expected vs actual behaviour, inputs and environment. An issue in
   `docs/issues/` that describes it gives its evidence as a start. Locate the code path
   (exploration subagents for unfamiliar areas). Find the spec scenario for this behaviour:
   - scenario exists and the code violates it → bug;
   - no scenario → specification gap;
   - code matches the scenario → the expectation differs from the contract: this is a feature request → [Feature](#feature).
2. **Hypotheses** — list likely causes, ranked; verify each against code, logs, tests or a minimal reproduction
   (read-only; parallel subagents with brief "Investigate" when there are several). Discard the disproved ones explicitly.
3. **Root cause** — state it with evidence (file, line, input) and the blast radius: other callers and data affected.
4. **Plan** — a failing test first (tagged with the scenario ID), the fix at the root cause, checks of the other
   callers, data repair if needed. A specification gap gets a small change proposal adding the missing `error`/`edge`
   scenario; a pure bug needs none.
5. **Handoff** — ask for approval of the plan, then implement it: the failing test first, then the fix, then the
   tests of the module and of the other callers. A fix that spans several modules or needs a data repair goes through
   plan mode as in Feature step 7. A specification-gap proposal gets the approved plan in its `## Plan` section, as in
   Feature step 6. A fixed bug that had an issue in `docs/issues/` deletes it with `git rm` in the same diff (through
   a proposal: its `**Issue:**` meta line, closed by `as:finish`). After implementation, suggest `as:finish`.
6. **Deferred** — when the user does not fix it now, offer to save it as an issue per
   [../issue/references/issue-format.md](../issue/references/issue-format.md), with the root cause and the planned
   fix, so the investigation is not lost (`**Source:**` `as:tech-lead`).
