# UX report format

`as:ux` writes one report per run to `docs/ux/`. It is evidence of how an area was to use on one day, not a living
page: a later run writes a new report.

```text
docs/ux/
  2026-11-25-checkout.md            # the report
  2026-11-25-checkout/              # screenshots the report links
.qa/2026-11-25-checkout/            # every screenshot of the run — gitignored, never committed
```

The file name is `<YYYY-MM-DD>-<area>.md` with the area in kebab-case; another run of the same area on the same day
takes the next free suffix (`-2`, `-3`, …). The report follows the spec language (`lang` in the marker on the first
line of `docs/spec/index.md`), else English; fixed values (categories, priorities, outcomes) stay English. Same
Markdown rules as spec pages
([../../spec-docs/references/markdown-format.md](../../spec-docs/references/markdown-format.md)).

## Skeleton

```markdown
<!-- as:ux lang=en -->
# UX review: Checkout — 2026-11-25

**Area:** checkout · **URL:** http://localhost:3000 · **Commit:** `a1b2c3d` · **Host:** Claude Code · **Reviewer:** separate agent

**Result:** 3 walks — 2 reached, 1 gave up · 1 mismatch · 4 findings · 1 theme

## Walks

| Walk | Persona | Goal | Viewport | Outcome | Actions |
|------|---------|------|----------|---------|---------|
| W1 | Customer, first visit | "Buy one thing without creating an account" | mobile | gave up | 31 |
| W2 | Customer, returning | "Order again what I bought last month" | desktop | reached | 9 |

## Mismatches

| # | Written | The walk showed | Walk, step | Evidence | Issue |
|---|---------|-----------------|------------|----------|-------|
| M1 | [Checkout UF1](../features/checkout/index.md#user-flow) step 2: guest checkout offered | Only "Sign in" and "Register" are shown | W1, s6 | [screenshot](2026-11-25-checkout/W1-s6.png) | [p2-guest-checkout-hidden](../issues/p2-guest-checkout-hidden.md) |

## Findings

### U1 — No sign that the address was saved

**Category:** feedback · **Priority:** p3 · **Walks:** W1 s12, W2 s5 · **Issue:** [p3-address-save-no-feedback](../issues/p3-address-save-no-feedback.md)

The customer presses "Save" and the form stays as it was; W1 pressed it three times. Cost: repeated actions and doubt
whether the order will go to the right address. [screenshot](2026-11-25-checkout/W1-s12.png)

**Suggested:** after saving, show the saved address in place of the form, with "Change".

## Themes

### T1 — Three different ways to go back

Cart uses a link at the top, delivery a button at the bottom, payment only the browser's back (W1 s8, s14, s19; W2
s4). Larger than one fix: suggest `as:roadmap checkout navigation`.

## Works well

- The order summary stays visible at every step (W2 s3–s8).

## Visual notes

- Delivery options: the price is cut off at 390 px ([screenshot](2026-11-25-checkout/W1-s10.png)).

## Not covered

- Payment by card — no test card in the environment.
```

- `**Reviewer:**` is `separate agent`, or `same agent` when the host has no subagents.
- Outcomes: `reached`, `reached, unsure`, `gave up`, `blocked`.
- Categories: `orientation`, `consistency`, `feedback`, `dead end`, `error recovery`, `wording`, `effort`.
- Findings `U<n>`, mismatches `M<n>` and themes `T<n>` are numbered within the report. A section with nothing says
  "None." rather than being left out, so a reader knows it was looked at.
- The `Issue` cell and line are filled after the user chose what to save; unsaved ones say "not saved".
- Only the screenshots the report links are copied next to it; issues link the report, not `.qa/`.
