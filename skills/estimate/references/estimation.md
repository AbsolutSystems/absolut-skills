# Estimation rules

Hours are for **one developer who knows this codebase and works with an AI coding agent**: the agent writes most of
the code and tests, the developer plans, steers, reviews and verifies. State this in the client document.

## Steps

- One step = one independently verifiable result, 1–8 h likely. Larger → split; many steps under 1 h → merge.
- Tests are part of the step that needs them (contract tests through the module's public API, error cases first),
  not a separate block.
- Every step covers at least one `R` (or is in the communication block); a requirement without a step is a mistake.
- Reuse what step 2 found: extending existing code is cheaper than the request's wording may suggest; say so.

## Calibrating with an AI agent

The agent shortens well-trodden work and barely helps where understanding or feedback loops dominate.

| Work | Effect of the agent | Typical likely |
|------|---------------------|----------------|
| CRUD, endpoint, form following an existing pattern | strong | 1–3 h |
| Tests following existing tests | strong | inside the step |
| Schema change + migration, small backfill | medium | 1–3 h |
| New UI view with existing components; visual iterations with the client | weak | 3–6 h |
| Logic with many rules (pricing, permissions, states) | medium; review is the cost | 3–8 h |
| Integration with an external API | weak: docs, sandbox, errors | 4–12 h |
| Area without tests, high coupling, legacy | weak; add pinning tests | +30–50 % |
| Data migration of production data, performance work | weak | per case, wide range |

`min` = everything as assumed and the pattern exists; `max` = the realistic bad case (an assumption fails, a hidden
dependency, an extra review round) — not a catastrophe. Each open `Q` or risky `A` widens `max` of the steps it
touches; say which.

## Communication

The communication block (named in the client language) covers clarifying questions, a demo and acceptance: about
10–15 % of the likely total, at least 1 h; more with many open questions or several stakeholders. Write the reason in the step.

## Totals

[`estimate_totals.py`](../scripts/estimate_totals.py) sums min, likely and max per block and in total, and computes
the expected value `(min + 4·likely + max) / 6` per block, rounded up to 0.5 h; the total expected is the sum of the
blocks. Quote the range and the expected value; options are priced separately and never added to the total.

## Not included unless the user prices it

Manual QA and acceptance testing on staging, production deployment and infrastructure, content and translations,
third-party licences, project management beyond the communication block.
