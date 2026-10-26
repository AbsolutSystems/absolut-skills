---
name: fix
description: "Work through the known problems in docs/issues/ (saved by as:issue, as:health, as:finish, as:spec-docs, as:tech-lead): lists open issues by priority and effort, recommends what to fix next, or takes one by name or a request like \"the 10 most important bugs\". Re-checks each issue's evidence against the current code, fixes small ones test-first after approval and deletes the issue file in the same diff, and plans larger ones as a change proposal through as:tech-lead. Use only when the user explicitly invokes as:fix."
disable-model-invocation: true
argument-hint: "[slug or request]"
---

# Fix

Pick known problems from `docs/issues/` and fix them, most important first. Issue format and priority rubric:
[../issue/references/issue-format.md](../issue/references/issue-format.md). Investigation and planning follow
[tech-lead](../tech-lead/SKILL.md) — read it and follow the paths named below. Answer in the user's language. Host
mechanics: [Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `[slug or request]` — an issue slug or words from its title (`bodymass`), or a request in the user's words
  (`10 most important bugs`, `all p1`, `tests in orders`). No argument — show the list and recommend one.

## Procedure

1. **Load** — read the meta line and title of every `docs/issues/*.md`. None → say so and suggest `as:issue` (save a
   problem) or `as:health` (find some). Drop the issues named by an `**Issue:**` meta line of an open proposal in
   `docs/spec/changes/` — they are planned; mention them in one line with their proposal.
2. **Choose** — order by priority, then effort (`S` first), then date.
   - Slug or title words → that issue; several matches → list them and ask.
   - A request → filter by it (kind, priority, module) and take the first N in that order.
   - No argument → a table of the first 10: file, kind, priority, effort, module, title. Recommend one with a reason —
     usually the first, unless a later one unblocks it or several `S` issues in one module are cheaper together.

   Show the selection and ask (multi-select). Several `S` issues of one module may become one plan; otherwise handle
   the selected issues one at a time, in order, each through steps 3–5.
3. **Re-check** the issue's evidence against the current code: find the symbol, then a line of the excerpt (`git grep -F`); a
   moved or renamed symbol is followed, not treated as resolved. Gone → say it looks resolved, offer to delete the file
   (`git rm`) and move to the next. Priority no longer fits the rubric → propose the `git mv` to the new prefix.
4. **Fix**, starting from the issue's evidence and suggested fix instead of searching from scratch. Size from its
   `**Effort:**` (the user may override):
   - `bug`, `security`, `spec-gap` → the tech-lead [Bug](../tech-lead/SKILL.md#bug) path: reproduce, root cause, plan
     with a failing test first, approval, fix.
   - `refactor`, `review`, `delete`, `deps` → observable behaviour stays: no scenario changes ("No contract change"),
     and the plan starts by running or adding tests that pin the current behaviour.
   - `add-tests` → tests only, tagged with the scenario IDs they verify; a missing scenario is a specification gap —
     propose it in a change proposal.
   - `remove-tests` → list each test with the reason and get explicit consent per test; never one that is the only
     test of a spec scenario or an error path.
   - `docs` → hand over to `as:agent-docs` or `as:spec-docs` for the affected path, or `as:finish` / drop for a stale
     change proposal; delete the issue when that is done.

   An `S` issue without a contract change is fixed here after the user approves the short plan: failing test first,
   then the fix, then the module's tests. `M`/`L` issues, or any contract change → the tech-lead
   [Feature](../tech-lead/SKILL.md#feature) path from step 2, with `` · **Issue:** `<slug>` `` in the
   proposal's meta line; then `as:implement` and `as:finish`. In a series, an `M`/`L` issue ends the series:
   ask whether to continue with the next issue after its proposal is written.
5. **Close** — after a direct fix and green tests, delete the issue file with `git rm` (or `rm` if untracked), so the
   fix and the closed issue land in one diff. An issue fixed through a proposal stays until `as:finish` archives the
   proposal. Never delete an issue that is not fixed without the user's consent.
6. **Summary** — issues fixed and deleted, issues planned (proposal paths), issues skipped, tests added, files changed.
   Do not commit. Next: `as:finish` on the changes, then commit.
