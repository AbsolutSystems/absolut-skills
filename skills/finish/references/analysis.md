# Analysis: diff-anchored module brief

One read-only subagent per touched module (`finish` step 5). Unlike the full `spec-docs` and `agent-docs` briefs, it
looks only at what the branch changed, so it stays short and fits a smaller model.

The subagent computes the diff itself from `{base}` and `{dir}`, so the main thread does not paste hunks and large
diffs need no special handling.

Fill the placeholders and pass verbatim:

```text
Read-only: do not modify files. Report what this branch's diff changed in one module, nothing else. Do not describe
code the diff did not touch, and do not describe the code itself: report contract, test and docs consequences only.

Module: {dir}
Base: {base}
Diff: run `git diff {base} -- {dir}` (committed and uncommitted changes) and read the files listed by
`git ls-files --others --exclude-standard -- {dir}` (new untracked files, all of them added).
Spec page: {Markdown content, or "none"}
Open change proposal scenarios for this module: {ID, change (added | changed | removed), Given / When / Then, or "none"}
Scenario IDs found in tests (cheap pass): {ID → file:line, or "none"}
Module AGENTS.md: {content, or "none"}

Return exactly these five sections, each item with evidence (file:line), at most 10 lines per section, "none" if empty:
1. Proposal — for each proposal scenario: implemented | partly | not, and what is missing.
2. Spec drift — statements or scenario IDs on the spec page that the diff made false: the claim, what the code does
   now. Ignore everything the diff did not touch.
3. New behaviour — observable behaviour the diff added or changed (seen by a caller through the module's public entry
   points) with no scenario on the page or in the proposal: a one-line Given / When / Then candidate and its kind
   (happy | error | edge).
4. Tests — for each scenario in 1, item in 2 and candidate in 3: COVERED | PARTIAL | MISSING by a test through the
   public entry point, with the test file and name. PARTIAL: only internal classes, part of the Then, or the behaviour mocked away.
   For items in 2, a test that still asserts the old behaviour is PARTIAL — name it.
5. Docs — lines of the module AGENTS.md the diff made false (quote them), and commands, rules or pitfalls the diff
   introduced that an agent would get wrong without a line. Not descriptions of the new code.
```
