# Estimate format

An estimate is two Markdown files in one folder: the internal analysis the team works from, and the client document
that is sent without editing. `as:estimate` writes both; `as:tech-lead docs/estimates/<slug>` reads the analysis.

## Files

```text
docs/estimates/<slug>/analysis.md   # internal: requirements, impact with paths, findings, assumptions, step estimate
docs/estimates/<slug>/client.md     # for the client: PRD, estimate per block, assumptions, questions, suggestions
```

Marker on the first line of each: `<!-- as:estimate lang=… -->`. Block names are client-facing labels in the client
language, identical in both files ([`estimate_totals.py --check`](../scripts/estimate_totals.py) matches rows by them).

## `analysis.md`

Section headings and the table columns `Step | Block | Min | Likely | Max` stay exactly as below, in English — the
script reads `## Estimate` and `## Optional additions`, `as:tech-lead` reads the other sections by name. Other columns
may follow `Max`.

```markdown
<!-- as:estimate lang=en -->
# Partial order cancellation — analysis

**Status:** draft · **Revision:** 1 · **Date:** 2026-10-26, commit `a1b2c3d` · **Client:** [client.md](client.md) · **Modules:** orders, billing

## Requirements

- **R1** — Customer cancels single items of a placed order ("we want to remove one product without cancelling all").
- **R2** — Refund of the cancelled item (inferred: the request says "money back as usual").

## What exists today

- R1: only whole-order cancellation — `orders/OrderFacade.java` `cancelOrder`; spec [ORD-007](../../spec/backend/orders.md#ORD-007).
- R2: refunds per order in `billing/RefundService.java`; no partial refund.

## Findings

| # | Type | Finding | Evidence | Effect | To client |
|---|------|---------|----------|--------|-----------|
| F1 | gap | Request says nothing about shipped orders | `OrderStatus.SHIPPED` | +2 h if returns flow is needed | Q1 |
| F2 | alternative | Cancel by quantity instead of whole lines | lines have `quantity` | +3 h | suggestion S1 |

## Assumptions

- **A1** — Shipped orders cannot be partially cancelled (answer to Q1 may add returns: +6–10 h).

## Client questions

- **Q1** — What should happen when the order is already shipped?

## Estimate

| Step | Block | Min | Likely | Max | Covers |
|------|-------|-----|--------|-----|--------|
| 1.1 `cancelItems` in Orders with status rules; contract tests | Anulowanie pozycji | 3 | 4 | 6 | R1, A1 |
| 1.2 Partial refund on `OrderItemsCancelled`; tests | Anulowanie pozycji | 2 | 3 | 5 | R2 |
| 1.3 Cancel button and confirmation in order details | Anulowanie pozycji | 2 | 3 | 5 | R1 |
| 2.1 Clarifications, demo, acceptance | Komunikacja | 1 | 2 | 3 | — |

## Optional additions

| Step | Block | Min | Likely | Max | Covers |
|------|-------|-----|--------|-----|--------|
| S1 Cancel part of a line's quantity | Częściowa ilość | 2 | 3 | 5 | F2 |

## Totals

| Block | Min | Likely | Max | Expected |
|-------|-----|--------|-----|----------|
| Anulowanie pozycji | 7 | 10 | 16 | 10,5 |
| Komunikacja | 1 | 2 | 3 | 2 |
| Total | 8 | 12 | 19 | 12,5 |

## Risks

- Billing receives the event before deployment — order of deploys; covered in `max` of 1.2.

## History

- 2026-10-26 — revision 1.
```

- `**Status:**` — `draft`, `sent`, `accepted` (set by `as:estimate` or `as:tech-lead` when the user confirms the client
  accepted it), `rejected`.
- `## Totals` is the script's last output (blocks of `## Estimate` and the total); `as:tech-lead` compares its plan
  with each block's `max`.
- Before a revision rewrites a `client.md` the client has seen (status not `draft`), it is kept as
  `client-r<revision>.md`.
- Accepted suggestions are moved to `## Estimate` by a revision, so `## Estimate` is always the work the client
  agreed to.
- Steps are numbered per block (`1.1`, `2.1`), options `S<n>`; findings `F<n>`, assumptions `A<n>`, questions `Q<n>`
  keep their numbers across revisions (a resolved one is marked, not renumbered).

## `client.md`

Written in the client language, for a non-technical reader: no paths, class names or internal module names. Headings
below are translated; the structure stays.

```markdown
<!-- as:estimate lang=pl -->
# Częściowe anulowanie zamówienia — analiza i wycena

**Wersja:** 1 · **Data:** 2026-10-26

## Jak rozumiemy potrzebę

Klient chce usunąć pojedynczy produkt z zamówienia bez anulowania całości; zwrot pieniędzy za ten produkt.

## Specyfikacja (PRD)

### Cel i użytkownicy
### Przepływy
1. Klient otwiera szczegóły zamówienia … 
### Wymagania funkcjonalne
- … (R1, R2 in plain words)
### Wymagania niefunkcjonalne
### Poza zakresem
- Zwroty po wysyłce (patrz pytanie 1).

## Wycena

| Zakres | Godziny (min–max) | Oczekiwane |
|--------|-------------------|------------|
| Anulowanie pozycji | 7–16 h | 10,5 h |
| Komunikacja | 1–3 h | 2 h |
| **Razem** | 8–19 h | 12,5 h |

Wycena zakłada pracę programisty znającego aplikację, wspieranego narzędziami AI; obejmuje implementację, testy
automatyczne i komunikację. Nie obejmuje: testów manualnych/QA, wdrożenia na produkcję.

## Założenia

- Zamówienia już wysłane nie mogą być częściowo anulowane (inaczej +6–10 h).

## Pytania

1. Co ma się dziać, gdy zamówienie zostało już wysłane?

## Sugestie

| Sugestia | Dlaczego | Godziny (min–max) | Oczekiwane |
|----------|----------|-------------------|------------|
| Częściowa ilość | Klient zamówił 3 sztuki i chce zwrócić 1 | 2–5 h | 3,5 h |
```

- Each block of `## Estimate` is one row of the estimate table, each option one row of the suggestions table; the
  first cell is the block name, the row shows the range `min–max h`, then the expected value `x h`, in this order
  (an amount column may follow when the user gave a rate). Hours cells end in `h` in every language — the script
  ignores other cells. The total row is in the same table as the blocks.
- "Not included" lists the items of [estimation.md](estimation.md#not-included-unless-the-user-prices-it) the user did
  not price.
