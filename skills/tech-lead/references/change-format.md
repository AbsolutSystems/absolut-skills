# Change proposal format

A change proposal describes a planned change to the contract before it is implemented: why, what was decided, and
which scenarios will be added, changed or removed. Module pages in `docs/spec/` keep describing the current behaviour
until `as:finish` merges the proposal after implementation and moves it to `docs/spec/changes/archive/`, where it
remains as the decision record.

## Files

```text
docs/spec/changes/<slug>.md                     # open proposal (slug: short kebab-case title)
docs/spec/changes/archive/<YYYY-MM-DD>-<slug>.md  # merged by as:finish; status implemented or dropped
```

Same rules as spec pages ([../../spec-docs/references/markdown-format.md](../../spec-docs/references/markdown-format.md)):
the constructs and readability rules listed there, marker `<!-- as:tech-lead lang=… -->` on the first line, relative
links (`../`; `../../` in `archive/`).

## IDs

- **Added** scenarios reserve the next free number of the module's prefix, counting IDs on the module page **and** in
  every open proposal. Added requirements likewise (`<PREFIX>-R<n>`).
- **Changed** and **removed** scenarios use their existing ID.
- A new module gets a new prefix, unique across the spec and open proposals.

## Skeleton

```markdown
<!-- as:tech-lead lang=en -->
[System](../index.md) › Changes › Partial order cancellation

# Partial order cancellation

Customers can cancel single items of a placed order until it ships.

**Status:** open · **Proposed:** 2026-10-19, commit `a1b2c3d` · **Modules:** [Orders](../backend/orders.md), [Billing](../backend/billing.md)

## Why

Support handles ~40 requests a week to remove one item; today the whole order must be cancelled.

## Scope

- **In:** cancel one or more items before shipping; refund the item amount.
- **Out:** cancelling after shipping (returns flow), partial quantity of one item.

## Decision

| Option | Summary | Effort | Main risk |
|--------|---------|--------|-----------|
| A — extend `cancelOrder` | Optional item list on the existing operation | S | Ambiguous semantics for empty list |
| **B — new `cancelItems`** | Separate operation, emits `OrderItemsCancelled` | M | Billing must handle a new event |

**Chosen: B.** Keeps `cancelOrder` semantics intact for existing callers; the new event lets Billing refund without querying Orders.

## Scenarios

### <a id="ORD-R4"></a>ORD-R4 — Cancel items

**Change:** 🆕 added

> The module **SHALL** cancel selected items of an order that has not shipped.

#### <a id="ORD-014"></a>ORD-014 — Cancel one item before shipping

**Kind:** ✅ happy · **Change:** 🆕 added

- **Given** a placed order with two items, not shipped
- **When** the customer cancels one item
- **Then** the item is cancelled and `OrderItemsCancelled` is emitted with its amount

#### <a id="ORD-015"></a>ORD-015 — Order already shipped

**Kind:** ❌ error · **Change:** 🆕 added

- **Given** a shipped order
- **When** the customer cancels an item
- **Then** the request is rejected with `ALREADY_SHIPPED`

---

### Changed scenarios

#### <a id="ORD-004"></a>ORD-004 — Order total

**Kind:** ✅ happy · **Change:** ✏️ changed

- **Given** an order with cancelled items
- **When** its total is read
- **Then** cancelled items are excluded (was: all items)

## Open questions

> [!NOTE]
> Should cancelling the last item cancel the whole order? Assumed yes; confirm with product.

---

[← System](../index.md)
```

- `**Change:**` (`added`, `changed`, `removed`) on every requirement and scenario. A changed scenario states the new
  behaviour and says what it was in one parenthesis; a removed one keeps its last text.
- Changed and removed scenarios outside an added requirement go under a `### Changed scenarios` heading.
- When the change touches several modules, put a `**Module:** [Orders](../backend/orders.md)` line before each module's
  requirements and scenarios, so heading levels stay the same as on module pages.
- `**Status:**` in the meta line is `open`, then `implemented` or `dropped` when archived; `as:finish` updates it.
