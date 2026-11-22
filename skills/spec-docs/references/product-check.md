# Product check

A second look at behaviour before it is written down as intended, or accepted because nothing written forbids it.
Analysts describe what the code does and QA judges compare with what is written; neither asks whether the behaviour
makes sense for the product. This check does, and only that. Used by `as:spec-docs` (step 3, also inside
`as:docs-check` and `as:health`), `as:tech-lead` (Feature step 5), `as:finish` (step 6) and `as:qa` (step 4).

- One read-only subagent per run (per application when the list is long) — never the one that wrote the items, so
  it is not anchored on "the code does it, so it is meant". A judgement subagent: where the host mapping offers a
  stronger model for it, ask the user first, once per run. Without subagents, do the check yourself in a separate
  pass after the items are final.
- It never changes a result, a scenario or the code. Its output is a recommendation: the calling skill asks the user
  (or, unattended, follows the `as:deliver` policy).
- A suspect item is never written to the spec as a scenario on the strength of the code alone.

Fill the placeholders and pass verbatim:

```text
You are the product owner of this application. Behaviour is about to be accepted as intended; say where that would
be wrong for the people who use the product. Read-only: do not modify files.

The code and what was seen in the browser prove what happens, not what was wanted. A written scenario or criterion
proves what someone wrote, not that it is right. You do not check whether the code is consistent — others did.

Product: {purpose and actors, from docs/spec/index.md or the feature page}
Area: {module or feature: what it is for, in one to three sentences}
Written: {acceptance criteria, feature decisions and non-goals, app-wide rules that touch the items, or "none"}
Items: {numbered — the behaviour in one sentence (Given / When / Then, or what the tester saw), status (new |
written: <scenario or criterion ID>), evidence (code path | checkpoint and screenshot path)}

You may read docs/spec/ and docs/features/ to see how neighbouring flows behave, and open the screenshots.

For each item ask: would a person using, supporting or paying for this product expect something else? Look for:
- a record that does not keep who did it, when, or for whom (author, owner, timestamps, status history);
- something the user entered or chose that is dropped, overwritten or changed without telling them;
- a dead end: a state the user cannot leave or correct, an action with no visible result, an error with no way on;
- the same thing working differently in a neighbouring flow of this product;
- a role that sees or can do what its job does not need, or cannot do what it needs;
- a rule that defeats the purpose of the area as stated above.

Report an item only when you can name the harm: who, doing what, loses or misses what. Not findings: taste, wording,
layout, performance, features nobody promised, another design that would also work. A behaviour that a decision or
non-goal under Written chose on purpose is not a bug: report it only as a written rule to reconsider.

Return exactly these sections, "none" if empty:
1. Suspect — item number, what the product should do instead (one sentence), the harm (who, when, what they lose),
   suggested priority (p1 data loss or security, p2 broken main flow, p3 edge case, p4 cosmetic).
2. Written rules to reconsider — the scenario, criterion or decision ID, the harm, what you would change. Only for
   items with status written, or rules under Written.
3. Fine — the remaining item numbers.
```

Reading the result:

- **Suspect, status new** — recommend `bug` to the user, with the harm as the reason. Confirmed → an issue per
  [../../issue/references/issue-format.md](../../issue/references/issue-format.md) (kind `bug`, the intended
  behaviour from the check, evidence from the item), not a scenario.
- **Written rules to reconsider** — a question for the user, never a silent edit: the spec, the feature page and
  `docs/qa/` keep their owners. Confirmed → an issue (`bug` when the code should change, `spec-gap` when the rule
  itself is open); the scenario stays as it is until the fix changes it, and the issue names its ID.
- **In a change proposal draft** (`as:tech-lead`) nothing is built yet, so a Suspect scenario is corrected in the
  draft instead of becoming an issue, and the user sees the correction before approving.
- **Fine** — nothing to do; do not list it to the user.
