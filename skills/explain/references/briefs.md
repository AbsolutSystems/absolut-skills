# Explain briefs

## Inventory

One per touched module, read-only, a small model. Used by [explain](../SKILL.md) step 2.

```text
You list the structure of one module, before and after a change. Read-only: do not modify files. List facts with
evidence; do not explain, judge or guess from names.

Repository: {path}
Module: {module directory}
Before: {merge-base} (read with `git show {merge-base}:<file>` and `git ls-tree -r {merge-base} -- {module directory}`)
After: {the working tree, or the PR head}  — for a module page: after only
Files changed in this module: {from the diff's --name-status}

List, for before and for after:
- Components: the units a reader would name (service, controller, repository, job, UI screen, store), with the file
- Entry points: public functions, classes, routes, events, CLI commands, with the file
- Dependencies: every use of another module, a database or an external system — target, and the evidence (file and
  the import, call or client line, quoted)

Return exactly these sections:
- Before: the three lists (or "n/a")
- After: the three lists
- Moved: symbols that disappear here and appear in another module's file, if you saw the target (file before → file
  after)
- Not listed: files you skipped and why (generated, tests, too large)
Every item without a file and a quoted line is left out.
```

## Tracing

One per flow or module, read-only. Used by [explain](../SKILL.md) step 2.

```text
You trace how one behaviour works in the code, so it can be explained to {audience: a developer new to this code |
a business reader}. Read-only: do not modify files.

Repository: {path}
Behaviour: {flow, module path or question}
Scope: {for a change: the diff command and its files; otherwise "current code"}
Known context: {spec scenarios with IDs, acceptance criteria, AGENTS.md notes that apply}

Start at the entry points (route, handler, job, public function, UI action) and follow the behaviour to its result
and side effects (stored data, messages, events, calls to other systems). Read the code; do not guess from names.
For a change, describe before and after (`git show {merge-base}:{file}` for before).

Return exactly these sections:
- Steps: the flow in order, one line each — what happens in plain words, then `path:symbol`
- Decisions: each branch point — the condition in plain words, the outcomes, `path:symbol`
- Calculations: each formula or conversion — inputs, the rule written as a spreadsheet-style formula, rounding and
  where it happens, `path:symbol`; existing tests with their expected values (file, test name, scenario ID)
- Data: what is read and written, migrations or schema changes
- Errors and edges: what happens on missing data, zero, limits, failure of a dependency; what the user sees
- Unclear: behaviour you could not determine from the code, or that contradicts the known context
```

## Fact check

One per page, read-only, on the session model, never a subagent that researched the page. Used by
[explain](../SKILL.md) step 5.

```text
You check a page that explains code to people, claim by claim. Read-only: do not modify files. Assume each claim is
wrong until the code or the source proves it.

Code: {path of the code — for a PR, its worktree at the PR head}
Page: {absolute path of docs/explain/<page>.html}
Before: {merge-base, for a change; otherwise "n/a"}
After: {for a change: the working tree, or the PR head <headRefOid> in the worktree; otherwise the current code}
Sources: {docs/features/<slug>/sources/, for a feature; otherwise "n/a"}

List every claim the page makes about the code or the sources: each diagram node (the component or step exists, its
label is what it does), each edge (the dependency or call exists, in that direction), each delta mark (added, removed,
moved, changed — check against before), each before/after row, each rule and its scenario ID, each `path:symbol`,
each test named and the value it expects, each value quoted from a source, each example card (its formula gives
the stated result; its status — `matches`, `differs`, `to-confirm` — fits what the code and the source say). Check each in the code or the source
yourself; do not trust the page's wording.

Return exactly one line per claim:
<section id> — <claim in short> — confirmed | refuted | unclear — evidence (file and line or quoted text; for
refuted, what is true instead)
Then: claims you could not check, and why.
```
