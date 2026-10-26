# Markdown format

Spec pages are GitHub-flavoured Markdown written for people: they must read well both rendered (GitHub, GitLab, IDE
preview) and as plain text in a diff. Use only the constructs listed here, so every page looks the same.

## Rules

- First line: `<!-- as:spec-docs lang=en -->` (`lang=pl` with `--lang pl`; `as:tech-lead` on change proposals). Other
  skills read the spec language from this marker of `docs/spec/index.md`.
- Raw HTML only for that marker and for anchors `<a id="ORD-003"></a>` at the start of requirement and scenario
  headings (stable link targets that survive renaming the heading). No other HTML, no images, no inline styles.
- Links between pages are relative and point to `.md` files. Link to a scenario with `orders.md#ORD-003`.
- Code identifiers, paths, endpoints, error codes and values go in backticks. Escape `|` inside table cells as `\|`.
- Fixed values stay English in every language: kinds (`happy`, `error`, `edge`), statuses (`removed`, `open`,
  `implemented`, `dropped`), changes (`added`, `changed`, `removed`), IDs, anchors and file names.

## Readability

- One `#` title per page, then a breadcrumb line above it (not on the system page), a one to three sentence lead in
  plain business language, and one meta line.
- Heading levels never skip: `##` sections, `###` requirements, `####` scenarios.
- Module pages longer than one screen start with an "On this page" list linking the requirements.
- Short sentences, active voice, domain words from the glossary. Prose is not hard-wrapped; one blank line between
  blocks; no trailing spaces.
- Tables only for lists of things with the same columns (contract, modules, actors); keep cells to one short line.
- A `---` rule separates requirements, so each one reads as a card.
- Never more than one level of nested list.

## Vocabulary

| Construct | Use |
|-----------|-----|
| `[System](../index.md) › [Shop backend](index.md) › Orders` | Breadcrumbs, first line after the marker |
| `# Title` + paragraph | Page title and 1–3 sentence purpose |
| `**Source:** \`path\` · **Commit:** \`a1b2c3d\` · **ID prefix:** \`ORD\`` | Meta line under the lead; add `**Status:**` where relevant |
| `## Section` | Top-level sections, in this order where present: Actors, Modules, Flows, Contract, Requirements, Business rules, Dependencies, Glossary, Open questions |
| Table with header row | Contract, module and actor lists |
| `### <a id="ORD-R1"></a>ORD-R1 — Short name` + `> The module **SHALL** …` | One requirement and its SHALL sentence as a quote |
| `#### <a id="ORD-003"></a>ORD-003 — Short name` | One scenario inside a requirement |
| `**Kind:** ✅ happy`, `❌ error`, `⚠️ edge` | Line under the scenario heading |
| `- **Given** …`, `- **When** …`, `- **Then** …`, `- **And** …` | Scenario steps. With `--lang pl`: **Zakładając** / **Gdy** / **Wtedy** / **Oraz** |
| `**Status:** 🗑️ removed` + `~~ORD-005 — Short name~~` in the heading | Removed requirement or scenario: appended to the kind line, content kept |
| `**Change:** 🆕 added`, `✏️ changed`, `🗑️ removed` | Change proposals only (`docs/spec/changes/`, from `as:tech-lead`), on requirements and scenarios |
| Numbered list | Steps of a cross-module flow; steps link to scenarios |
| Task list `- [ ] **1. Step** — …` | Change proposals only: steps of the `## Plan` section, ticked `- [x]` when done |
| `> [!NOTE]` alert | Open question or caveat (renders as a callout on GitHub, a quote elsewhere); never a known bug — those go to `docs/issues/` |
| Definition list as `- **Term** — meaning` | Glossary |
| ` ```mermaid ` `flowchart LR` | Optional, system and app pages only: map of apps/modules and their dependencies, at most ~15 nodes |

## Scenario writing rules

- One requirement = one capability of the module ("The module SHALL reject orders without stock reservation").
- Every requirement has at least one `happy` scenario; add `error` scenarios for each rejection/failure the code
  actually handles (validation, not found, permission, conflict, downstream failure) and `edge` scenarios for limits,
  empty inputs, idempotency, concurrency, time boundaries.
- Given = state before; When = one call through the public contract; Then = observable result (return value, error,
  emitted event, persisted state visible through the contract). No internal method names.
- IDs: requirements `<PREFIX>-R<n>`, scenarios `<PREFIX>-<NNN>` (three digits, sequential per module, never reused).

## Skeleton: module page

```markdown
<!-- as:spec-docs lang=en -->
[System](../index.md) › [Shop backend](index.md) › Orders

# Orders

Accepts customer orders, reserves stock and tracks each order until delivery.

**Source:** `backend/src/main/java/com/acme/shop/orders` · **Commit:** `a1b2c3d` · **ID prefix:** `ORD`

**On this page:** [Contract](#contract) · [ORD-R1 Place an order](#ORD-R1) · [Business rules](#business-rules) · [Dependencies](#dependencies) · [Open questions](#open-questions)

## Contract

| Operation | Type | Input | Result |
|-----------|------|-------|--------|
| `placeOrder` | command | customer, items | order id or rejection |
| `OrderPlaced` | event | — | emitted after a successful placement |

## Requirements

### <a id="ORD-R1"></a>ORD-R1 — Place an order

> The module **SHALL** accept an order only when every item can be reserved.

#### <a id="ORD-001"></a>ORD-001 — All items in stock

**Kind:** ✅ happy

- **Given** every ordered item has enough stock
- **When** the customer places the order
- **Then** the order is created with status `PLACED`
- **And** `OrderPlaced` is emitted

#### <a id="ORD-002"></a>ORD-002 — Item out of stock

**Kind:** ❌ error

- **Given** one ordered item has no stock
- **When** the customer places the order
- **Then** the order is rejected with `OUT_OF_STOCK` and nothing is reserved

---

## Business rules

- An order total is never negative.

## Dependencies

- **Uses** [Inventory](inventory.md) — stock reservation.
- **Used by** [Billing](billing.md) — listens to `OrderPlaced`.

## Glossary

- **Reservation** — stock held for an order until it is paid or cancelled.

## Open questions

> [!NOTE]
> What happens to reservations of orders never paid? No timeout exists in the code.

---

[← Shop backend](index.md)
```

## Skeleton: app page (`<app>/index.md`)

Marker, breadcrumbs (`[System](../index.md) › <App>`), `#` title, lead, meta line (source path, commit), then
`## Modules` (table: module link, one-line responsibility), optional mermaid map, `## Flows` with one `###` + numbered
list per main cross-module flow (steps link to scenarios), optional Business rules, Glossary, Open questions, and a
closing `---` + `[← System](../index.md)`.

## Skeleton: system page (`index.md`)

Marker, `#` title = product name, lead = what it does and for whom, meta line (commit), `## Actors` (table: actor, what
they do), `## Modules` (table of apps in a monorepo, modules in a single app), optional mermaid map, `## Flows` for the
main end-to-end flows, optional Glossary and Open questions. No breadcrumbs or back link.

## Legacy HTML pages

Earlier versions wrote HTML pages styled by `spec.css`. Convert them one to one — same content, IDs, language and order
— with this mapping:

| HTML | Markdown |
|------|----------|
| `<html lang="pl">`, `<meta name="generator" content="as:…">` | Marker `<!-- as:… lang=pl -->` |
| `<nav class="crumbs">` / `<footer>` | Breadcrumb line / closing back link |
| `<header>` `h1`, `p.lead`, `dl.meta` | Title, lead, meta line |
| `<section id="…">` + `h2` | `## Section` |
| `<article class="req" id="X">` + `h3`, `p.shall` | `### <a id="X"></a>…` + quoted SHALL sentence |
| `<section class="scenario" id="X" data-kind="k">` + `h4`, `dl.gwt` | `#### <a id="X"></a>…`, kind line, Given/When/Then list |
| `data-status="removed"` | `**Status:** 🗑️ removed` and struck-through heading |
| `data-change="…"`; `<body data-status="…">` | `**Change:** …`; `**Status:** …` in the meta line |
| `ul.cards` | Table: link, one-line responsibility |
| `ol.flow`, `aside.note`, `span.badge`, `<code>`, `<table>` | Numbered list, `> [!NOTE]`, plain text, backticks, Markdown table |
| `href="x.html#ID"` | `x.md#ID` |
