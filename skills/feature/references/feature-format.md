# Feature format

A feature page is the living, whole-feature view of a capability that usually spans several modules: why it exists,
what the user gets (acceptance criteria), the roadmap of phases, the decisions taken and the sources they came from.
It is the page a person or an agent reads first ("read the feature, then we continue"). It never repeats what lives
elsewhere: behaviour is in the module pages of `docs/spec/`, the plan of a phase is in its change proposal, a decision's
details are in the archived proposal or the source — the feature page links them.

## Files

```text
docs/features/
  index.md                          # catalogue: one row per feature
  <slug>/
    index.md                        # the feature page
    sources/                        # material the feature is based on, never edited after it is saved
      2026-10-12-client-order.pdf   # original files: PDF, spreadsheet, document
      2026-10-12-pricing.xlsx
      2026-10-12-pricing.md         # text of the spreadsheet, from scripts/xlsx_text.py
      2026-10-20-email-refunds.md   # pasted e-mail or chat: header + text verbatim
      2026-10-22-meeting.md         # meeting or call notes
```

Same rules as spec pages ([../../spec-docs/references/markdown-format.md](../../spec-docs/references/markdown-format.md)):
the constructs and readability rules listed there, marker `<!-- as:feature lang=… -->` on the first line, relative
links. Pages follow the spec language (`lang` in the marker of `docs/spec/index.md`), else English; fixed values stay
English. Files under `sources/` keep their own language and format.

## Sources

- **A source is evidence, the page is the distillate.** Saved sources are never edited. Everything taken from them —
  an acceptance criterion, a non-goal, a decision, a question — goes to the page with a link to its source, so an
  agent can work from the page without reading every source.
- File names: `<YYYY-MM-DD>-<kind>-<topic>.<ext>`, kebab-case, no spaces (kinds: `order`, `email`, `meeting`,
  `notes`, `spec`, …; the date is when the material was written, else when it was saved).
- **Pasted text** (an e-mail, chat, agreed points) is saved verbatim as Markdown with a header:

  ```markdown
  # E-mail: Refunds for cancelled items

  **From:** Anna Nowak (client) · **Date:** 2026-10-20 · **Saved:** 2026-10-27

  ---

  <the text, verbatim>
  ```

- **Files** are copied with a shell copy (`cp`, or `git mv` when moved from inside the repository). A spreadsheet
  (`.xlsx`) also gets a Markdown text next to it from
  [../scripts/xlsx_text.py](../scripts/xlsx_text.py); without `python3`, ask the user for a CSV export. Other formats
  the agent cannot read (`.docx`, `.pptx`): ask for a PDF export and keep both.
- **Large or confidential files** (over ~10 MB, personal data, contracts) are not copied without the user's consent:
  list them in `## Sources` by their location instead — an `https://` link, or a path outside the repository in
  backticks (not a relative link, which `spec_lint.py` would report as broken on other machines).
- **Newer wins, explicitly.** When a later source changes an earlier one, a decision records it with links to both.
  A contradiction that cannot be settled becomes an open question.
- An estimate from `as:estimate` stays in `docs/estimates/<slug>/` and is listed in `## Sources` by a link.
- Every file in `sources/` is listed in `## Sources` (checked by `spec_lint.py`), the text of a spreadsheet next to
  its original in the same row.

## Page skeleton

The top of the page — meta line, Now line, Why, Users and goals, Non-goals, Acceptance criteria — fits in about one
screen. Do not copy source text: one line and a link. Decisions and Sources are one line per item.

```markdown
<!-- as:feature lang=en -->
[Features](../index.md) › Partial order cancellation

# Partial order cancellation

Customers cancel single items of a placed order until it ships.

**Status:** active · **Updated:** 2026-10-27, commit `a1b2c3d` · **Modules:** [Orders](../../spec/backend/orders.md), [Billing](../../spec/backend/billing.md)

**Now:** phase 2 in progress — [proposal](../../spec/changes/partial-cancel-refunds.md). **Next:** phase 3, notifications.

**On this page:** [Acceptance criteria](#acceptance-criteria) · [Roadmap](#roadmap) · [Decisions](#decisions) · [Sources](#sources) · [Open questions](#open-questions)

## Why

Support handles ~40 requests a week to remove one item; today the whole order must be cancelled ([order](sources/2026-10-12-client-order.pdf)).

## Users and goals

- **Customer** — removes an unwanted item without losing the rest of the order.
- **Success:** item-removal requests to support drop below 5 a week.

## Non-goals

- Cancelling after shipping (returns flow).

## Acceptance criteria

### <a id="AC1"></a>AC1 — Cancel one item before shipping

> As a customer I can cancel one item of an unshipped order and keep the rest of it.

**Realised by:** [ORD-014](../../spec/backend/orders.md#ORD-014), [ORD-015](../../spec/backend/orders.md#ORD-015) · **Source:** [order](sources/2026-10-12-client-order.pdf)

### <a id="AC2"></a>AC2 — Refund of the cancelled item

> The cancelled item's amount is refunded to the original payment method.

**Realised by:** planned — phase 2 · **Source:** [e-mail](sources/2026-10-20-email-refunds.md)

---

## Roadmap

### Phase 1 — Cancel items ✅ done

Cancel operation and order total without cancelled items · AC1 · [decision](../../spec/changes/archive/2026-10-21-partial-cancel.md)

### Phase 2 — Refunds 🔄 in progress

Refund of cancelled items through Billing · AC2 · [proposal](../../spec/changes/partial-cancel-refunds.md)

### Phase 3 — Notifications ⏳ planned

E-mail to the customer after a cancellation · AC3

## Decisions

- **D1** — a separate `cancelItems` operation instead of extending `cancelOrder` ([phase 1](../../spec/changes/archive/2026-10-21-partial-cancel.md)).
- **D2** — refund to the original payment method, not store credit; replaces the order's "credit" wording ([e-mail](sources/2026-10-20-email-refunds.md), [order](sources/2026-10-12-client-order.pdf)).

## Sources

| Source | Date | What it is | Gave |
|--------|------|------------|------|
| [order](sources/2026-10-12-client-order.pdf) | 2026-10-12 | Client's order | AC1, AC3 |
| [e-mail](sources/2026-10-20-email-refunds.md) | 2026-10-20 | Client on refunds | AC2, D2 |
| [pricing](sources/2026-10-12-pricing.xlsx) ([text](sources/2026-10-12-pricing.md)) | 2026-10-12 | Client's price list | AC3 |
| [estimate](../../estimates/partial-cancel/analysis.md) | 2026-10-14 | Accepted estimate | phases 1–3 |

## Open questions

> [!NOTE]
> **Q1** — Should cancelling the last item cancel the whole order?

---

[← Features](../index.md)
```

- `**Status:**` of the feature: `draft` (not started), `active`, `shipped` (every phase `done` or `dropped`),
  `paused`, `dropped`. `**Updated:**` is the date and commit of the last write.
- `**Now:**` says what is happening and what comes next, in one line; agents read it first.
- Acceptance criteria are user-level outcomes, not Given/When/Then: the scenarios that make them true live in the
  module pages and are linked in `**Realised by:**` (or `planned — phase <n>`). IDs `AC<n>` are local to the page,
  never renumbered or reused; a removed criterion keeps its text with `**Status:** 🗑️ removed` and a struck-through heading.
- Roadmap phases: `### Phase <n> — <name>` (translated with the page) ending in the status `⏳ planned`,
  `🔄 in progress`, `✅ done` or `🗑️ dropped` — emoji and English words fixed, last on the heading line; `spec_lint.py`
  finds phases by them. One phase = one change proposal and ends with working, tested value. An `in progress`
  phase links its open proposal in `docs/spec/changes/`; a `done` phase links the archived one (checked by
  `spec_lint.py`). A phase line lists the AC it delivers.
- Decisions `D<n>` and questions `Q<n>` are numbered like AC and never renumbered.

## Catalogue (`docs/features/index.md`)

```markdown
<!-- as:feature lang=en -->
# Features

What the product does feature by feature: why, acceptance criteria, roadmap and sources. Module contracts: [specification](../spec/index.md).

| Feature | Status | Purpose | Now |
|---------|--------|---------|-----|
| [Partial order cancellation](partial-cancel/index.md) | active | Cancel single items until shipping | phase 2 of 3 |
```

The link to `../spec/index.md` is left out when `docs/spec/` does not exist.

## Legacy material

A folder of older documentation is mapped file by file before anything moves:

| Role | Meaning | Goes to |
|------|---------|---------|
| `source` | Material a feature is based on (order, e-mail, notes, mock-ups, sheets) | `docs/features/<slug>/sources/` |
| `superseded` | An older version of another source | `sources/` too, marked "superseded by …" in `## Sources` |
| `module contract` | Describes how a module behaves | stays; input for `as:spec-docs` |
| `not a feature` | Anything else (setup notes, unrelated) | stays |

Moves use `git mv` (history is kept) and rename to the source naming rule; nothing is deleted.

## Ownership

`as:feature` writes the page and the catalogue. `as:tech-lead` sets a phase to `in progress` and links its proposal;
`as:finish` sets it to `done` or `dropped`, relinks it to the archive, fills `**Realised by:**`, the Now line, the
feature status and the catalogue row. Other skills only read.
