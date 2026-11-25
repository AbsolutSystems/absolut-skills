---
name: roadmap
description: "Discuss the direction of a whole application or a large module at product level and, when it is bigger than one feature, keep it as a roadmap in docs/roadmap/<slug>/: direction, users and goals, what is out of scope, a preliminary specification as plain-language capabilities, product decisions, open questions and stages — each stage is one feature, later documented with as:feature and planned with as:tech-lead. Sizes the topic first: one feature is sent to as:feature and one change to as:tech-lead without writing a roadmap. No technical design. Also refreshes stage statuses from the feature pages and records what changed in the direction. Use only when the user explicitly invokes as:roadmap."
disable-model-invocation: true
argument-hint: "<direction, application or module to discuss | docs/roadmap/<slug>> [--lang en|pl]"
---

# Roadmap

Be the user's product partner one level above a feature: talk through where an application or a large module should
go, decide whether it is one feature or many, and for many keep one page that says the direction, what was agreed
and the stages. A stage is one feature; its criteria, phases and technical design are settled later, per stage, with
`as:feature` and `as:tech-lead`. Do not write production code, feature pages, module pages or change proposals here.

Host-specific mechanics (subagents, asking questions): [Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).
Format: [references/roadmap-format.md](references/roadmap-format.md).

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `<description>` — the direction in the user's words; files and text pasted in the same message are its first sources.
- `docs/roadmap/<slug>` — an existing roadmap: refresh the stage statuses, and discuss what changed (a new stage, a
  new order, a dropped stage, a decision, an answered question).
- `--lang en|pl` — language of a new page (default: the spec language, `lang` in the marker on the first line of
  `docs/spec/index.md`, else English). Existing pages keep theirs.

Converse in the user's language.

## Stance

- Product level, exact. Talk about users, problems, what a person can do and see, rules and limits, order and
  dependencies. "Users can export reports" is too vague; "an accountant downloads the month's invoices as one file
  the accounting system accepts" is the level to reach.
- No technical design: no architecture, libraries, data model or APIs. A technical question that comes up is noted
  as an open question for `as:tech-lead`. The one technical fact that belongs here is what already exists.
- Code and docs first, questions second: never ask what the spec, the feature pages or the code already answer.
- Challenge the direction when warranted: an existing capability that already covers a stage, a smaller first stage
  that proves the idea, a stage nobody asked for. Say it once, plainly, then respect the decision.
- Every question carries a recommendation with a reason; before any choice, explain it as in the host mapping's
  "Asking the user to choose".

## Procedure

### 1. Inventory

- Read `docs/roadmap/index.md` and the pages that may overlap; an existing roadmap for the same area → update it
  instead of creating a second one.
- Read what exists: `docs/features/index.md` and the pages in the area, the spec map (`docs/spec/index.md`, app
  pages), `docs/estimates/`, and the root and app `AGENTS.md`. Where these are missing or thin, fan out read-only
  subagents with the brief "Explore" in [../tech-lead/references/briefs.md](../tech-lead/references/briefs.md), asking
  only what the product does today in the area — not how.
- Read every new source in full (rules and the spreadsheet script as in
  [../feature/references/feature-format.md](../feature/references/feature-format.md#sources)).
- Update: read the page and the feature page linked from each stage; derive each stage's status from it
  ([format](references/roadmap-format.md#stage-status)) and note the stages whose stored status differs.
- New topic: when the request and what exists already show it is one change or one feature, say so now and
  redirect as in [step 3](#3-size) instead of discussing it here; when unsure, go on.

### 2. Discuss

Say in a few lines what exists today in the area, then ask in small batches, most decisive first, with options taken
from the sources and from what exists. Cover only what is still unknown:

- the direction: which problem, for whom, why now, and what would make it a success;
- the capabilities — what each kind of user will be able to do that they cannot today, in plain language;
- the rules and limits the user already knows (who may do what, amounts, deadlines, what must never happen);
- what is out of scope, and what is deliberately left for later;
- order: what must exist first, what proves the idea soonest, what can be dropped if time runs out.

Restate what was agreed after each batch. Stop when the capabilities can be listed and ordered.

### 3. Size

New roadmaps only — an update of an existing roadmap skips this step and goes to step 4 for the stages that change
(none → step 5). Decide from the agreed capabilities and say it in one or two lines with the reason; the user may
override it.

- **One change** — one module, one behaviour, fits one change proposal → stop, write nothing, and suggest
  `as:tech-lead <summary>`.
- **One feature** — one capability serving one user goal, describable by a handful of acceptance criteria, shipped
  in a few phases → stop, write nothing, and suggest `as:feature <summary>`. Give the summary of what was agreed as
  text the user can pass to it, so nothing discussed is lost.
- **Roadmap** — several capabilities that are each worth shipping on their own, or serve different users or goals, a
  new application or module, or an order and dependencies between them that must be agreed → continue.

### 4. Shape the stages

- Group the capabilities into stages. One stage = one feature: one user goal, valuable when shipped alone, small
  enough for one feature page (a stage needing more than ~5 phases is two stages).
- Order them by dependency first, then by value. The first stage is the smallest one that gives a real user
  something working; a stage that only prepares ground (no user-visible value) is merged into the stage that needs it.
- A capability that exists already is marked as existing, not planned again; a feature page that already covers a
  stage is linked from it.
- Every capability belongs to exactly one stage or to "out of scope".

### 5. Report and gate

Show, briefly:

- new roadmap: slug, direction, users and goals, out of scope, the stages in order (goal, capabilities, depends on),
  decisions, open questions (technical ones marked for `as:tech-lead`), and the source files to save;
- an existing feature page that will get a `**Roadmap:**` link;
- update: status corrections from step 1 (stage, stored → derived, the feature page it comes from), and each change
  agreed in step 2. Changing a stage that already has a feature page changes that feature too: say so and suggest
  `as:feature docs/features/<slug>` after this run.

Ask for approval: all, a subset, or cancel.

### 6. Write

- Sources first, as in [../feature/SKILL.md](../feature/SKILL.md) step 5, into `docs/roadmap/<slug>/sources/`.
- Write `docs/roadmap/<slug>/index.md` from the skeleton, or edit the existing page minimally: keep hand-written
  text and every `C`, `D`, `Q` ID and stage number; new ones take the next number; a dropped stage keeps its section
  with the dropped status. Set `**Updated:**` to today and the current commit (`git rev-parse --short HEAD`) and
  rewrite the Now line.
- Add or update the row in `docs/roadmap/index.md` (create it from the skeleton when missing).
- A stage linked to a feature page that existed before: add `**Roadmap:**` to that page's meta line
  ([format](../feature/references/feature-format.md)) — the only edit of a feature page here.
- Do not touch module pages, proposals, estimates or code. Never delete a page or a source without consent.

### 7. Verify

- Run `python3 <spec-docs skill directory>/scripts/spec_lint.py --features docs/roadmap` from the repository root
  ([../spec-docs/scripts/spec_lint.py](../spec-docs/scripts/spec_lint.py)) and fix every `ERROR` in the roadmap
  pages: broken links and anchors, sources not listed. Without `python3`, check the same by hand.
- No technical design slipped in: a sentence naming a technology, a table, an endpoint or a class is removed or
  turned into an open question.
- Every capability is in exactly one stage; the top of the page fits about one screen.

### 8. Summary

Files written, the stages in order with their status, open questions, and what was not checked (sources not
readable, areas not explored). Next: `as:feature docs/roadmap/<slug>` documents the next `planned` stage as a
feature (it links the feature from the stage), then `as:tech-lead docs/features/<slug>` plans its phases; when the
direction changes or a stage ships → `as:roadmap docs/roadmap/<slug>`. If the repository has `AGENTS.md` files and
the catalogue is new, suggest `as:agent-docs` so the root `AGENTS.md` links it. Do not commit.
