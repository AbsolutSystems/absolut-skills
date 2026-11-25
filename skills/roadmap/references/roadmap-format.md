# Roadmap format

A roadmap page is the product-level view of a whole application or a large module: where it is going, what was
agreed, and the stages that get it there. One stage is one feature. The page holds no technical design and never
repeats what lives below it: a stage's acceptance criteria, phases and sources are on its feature page
([../../feature/references/feature-format.md](../../feature/references/feature-format.md)), behaviour is in
`docs/spec/` — the roadmap links them.

| Level | Page | Split into | Written by |
|-------|------|------------|------------|
| Application or large module | `docs/roadmap/<slug>/index.md` | stages — one feature each | `as:roadmap` |
| Feature | `docs/features/<slug>/index.md` | phases — one change proposal each | `as:feature` |
| Change | `docs/spec/changes/<slug>.md` | plan steps | `as:tech-lead` |

## Files

```text
docs/roadmap/
  index.md                          # catalogue: one row per roadmap
  <slug>/
    index.md                        # the roadmap page
    sources/                        # material the direction is based on, never edited after it is saved
    mockups/                        # optional: HTML mockups of the application's frame and their viewer
```

Same rules as spec pages ([../../spec-docs/references/markdown-format.md](../../spec-docs/references/markdown-format.md)):
the constructs and readability rules listed there, marker `<!-- as:roadmap lang=… -->` on the first line, relative
links. Pages follow the spec language (`lang` in the marker of `docs/spec/index.md`), else English; fixed values stay
English. Sources follow the rules of
[feature sources](../../feature/references/feature-format.md#sources): saved verbatim, named
`<YYYY-MM-DD>-<kind>-<topic>.<ext>`, each listed in `## Sources`.

## Page skeleton

The top of the page — meta line, Now line, Direction, Users and goals, Out of scope — fits in about one screen.

```markdown
<!-- as:roadmap lang=en -->
[Roadmaps](../index.md) › Customer self-service

# Customer self-service

Customers change and follow their own orders without writing to support.

**Status:** active · **Updated:** 2026-11-25, commit `a1b2c3d` · **Scope:** module — orders and the customer account

**Now:** stage 1 in progress — [Partial order cancellation](../../features/partial-cancel/index.md). **Next:** stage 2, address change.

**On this page:** [Stages](#stages) · [Screens](#screens) · [Decisions](#decisions) · [Open questions](#open-questions) · [Sources](#sources)

## Direction

Support spends most of its time on changes a customer could make alone: removing an item, a new address, a missed
delivery. Each stage moves one of them to the customer account, the most frequent first ([notes](sources/2026-11-20-meeting-direction.md)).

## Users and goals

- **Customer** — fixes an order without waiting for an answer.
- **Support agent** — handles exceptions only, and sees what the customer changed.
- **Success:** order-change requests to support drop by half within a quarter of stage 2 shipping.

## Out of scope

- Returns after delivery (a separate flow, not planned here).
- Changes to orders placed by phone.

---

## Stages

### Stage 1 — Cancel single items

**Status:** 🔄 in progress · **Feature:** [Partial order cancellation](../../features/partial-cancel/index.md) · **Depends on:** —

The customer removes an unwanted item and keeps the rest of the order.

- **C1** — A customer cancels one or more items of an order that has not shipped.
- **C2** — The amount of the cancelled items is refunded the way the order was paid.

### Stage 2 — Change the delivery address

**Status:** ⏳ planned · **Depends on:** —

The customer corrects the address while the parcel can still be redirected.

- **C3** — A customer changes the delivery address until the order is handed to the carrier.
- **C4** — A change that raises the delivery cost shows the difference before it is confirmed.

### Stage 3 — Order history for support

**Status:** ⏳ planned · **Depends on:** stages 1, 2

- **C5** — A support agent sees every change the customer made to an order, with the time.

## Screens

**Navigation:** customer account → Orders → order details. Support panel → Orders → order details. · **Mockups:** [viewer](mockups/index.html)

| Screen | Who | What it is for | Reached from | Stage |
|--------|-----|----------------|--------------|-------|
| Order details | Customer | See one order and change it | Orders list, e-mail link | exists — changed in 1, 2 |
| Cancel items | Customer | Pick the items to cancel and see the refund | Order details | 1 |
| Order changes | Support agent | What the customer changed, with the time | Order details in the support panel | 3 |

## Decisions

- **D1** — Most frequent support request first: cancellation before address change ([notes](sources/2026-11-20-meeting-direction.md)).
- **D2** — Every self-service change is allowed only before shipping; later changes stay with support.
- **D3** — Changes open in a side panel over the order, not on separate screens; versions A and C rejected ([mockups](mockups/index.html)).

## Open questions

> [!NOTE]
> **Q1** — Does a cancelled item free its stock immediately, or after the refund? *(product)*

> [!NOTE]
> **Q2** — Can the carrier integration redirect a parcel after the label is printed? *(technical — `as:tech-lead`, stage 2)*

## Sources

| Source | Date | What it is | Gave |
|--------|------|------------|------|
| [notes](sources/2026-11-20-meeting-direction.md) | 2026-11-20 | Direction meeting | D1, C1–C5 |

---

[← Roadmaps](../index.md)
```

- `**Status:**` of the roadmap: `draft` (no stage has a feature page yet), `active`, `done` (every stage `done` or `dropped`),
  `paused`, `dropped`. `**Updated:**` is the date and commit of the last write. `**Scope:**` says `application` or
  `module — <which>`.
- `**Now:**` says which stage is happening and which comes next, in one line; agents read it first.
- Stages: `### Stage <n> — <name>` (translated with the page), numbered in the order they are meant to ship and
  never renumbered. The status is on the `**Status:**` line under the heading, not in the heading — `spec_lint.py`
  reads a status in a `###` heading as a feature phase and would ask for its change proposal.
- Capabilities `C<n>` are the preliminary specification: one sentence each, what a named kind of user can do or see,
  with the rule or limit that matters, in plain language — no Given/When/Then, no technology. They are numbered
  across the page, never renumbered or reused, and each belongs to one stage. They become the candidates for the
  feature's acceptance criteria; once the feature page exists, its criteria are the truth and the capabilities stay
  as the record of what was agreed.
- `## Screens` is the map of the screens the stages add or change, for a roadmap with a user interface: the
  navigation in one line, then one row per screen — who uses it, what it is for, where it is reached from, and the
  stage that builds it (`exists` for a screen that is there today). It names screens, it does not design them: the
  steps and states of each are settled on the feature page (`## User flow`). No user interface → the section is
  left out. `**Mockups:**` links the viewer of the roadmap's mockups — only when the user asked for them and
  `mockups/` exists, otherwise the line and a decision like D3 are left out
  ([mockups](../../feature/references/mockups.md)): the frame of the application (navigation, layout of a typical
  screen) and, for a new application, the look chosen between versions — a decision that binds every stage.
- A capability that already exists is written as such on its stage ("exists — Orders", with a link to its spec or feature page).
- Decisions `D<n>` are product decisions that bind every stage. Questions `Q<n>` end with *(product)* or
  *(technical — `as:tech-lead`, stage <n>)*; an answered question becomes a decision or a capability and is removed.

### Stage status

A stage's status is derived from its feature page; the roadmap stores a copy that `as:roadmap docs/roadmap/<slug>`
refreshes. The feature page wins.

| Stage `**Status:**` | When |
|---------------------|------|
| `⏳ planned` | no `**Feature:**` link yet |
| `🔄 in progress` | linked feature is `draft`, `active` or `paused` (say `draft` or `paused` after the link) |
| `✅ done` | linked feature is `shipped` |
| `🗑️ dropped` | linked feature is `dropped`, or the stage was dropped in a roadmap discussion (a decision records why) |

Emoji and English words are fixed.

## Catalogue (`docs/roadmap/index.md`)

```markdown
<!-- as:roadmap lang=en -->
# Roadmaps

Where the product is going, stage by stage. Each stage is one [feature](../features/index.md).

| Roadmap | Status | Direction | Now |
|---------|--------|-----------|-----|
| [Customer self-service](customer-self-service/index.md) | active | Customers change their own orders | stage 1 of 3 |
```

The link to `../features/index.md` is left out when `docs/features/` does not exist.

## Ownership

`as:roadmap` writes the page, its `mockups/` and the catalogue. `as:feature`, when it documents a stage
(`as:feature docs/roadmap/<slug>`), adds the stage's `**Feature:**` link, sets it to `🔄 in progress`, and brings the roadmap's `**Status:**`, Now line,
`**Updated:**` and catalogue row in line with it. Later status changes are copied from the feature pages only by
`as:roadmap`, which also adds `**Roadmap:**` to a feature page that existed before its stage. `as:doctor` and
`as:docs-check` lint the pages. Other skills only read.
