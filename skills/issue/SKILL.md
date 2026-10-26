---
name: issue
description: "Save known problems to docs/issues/ so they survive the session: one Markdown file per problem with priority (p1-p4) in the file name, kind, effort, evidence and a suggested fix. Takes a description, or collects the problems found earlier in the conversation (for example by /code-review, /claude-security or a manual review) and asks which to save. Checks the code read-only for evidence, merges duplicates, writes nothing else. Fix them later with as:fix. Use only when the user explicitly invokes as:issue."
disable-model-invocation: true
argument-hint: "[problem description]"
---

# Issue

Turn a problem into a file in `docs/issues/` that any later session can pick up with `as:fix`. Format, priority rubric
and rules: [references/issue-format.md](references/issue-format.md). This skill does not fix anything. Answer in the
user's language. Host mechanics (subagents, asking questions): [Claude Code](../../references/claude-tools.md),
[Codex](../../references/codex-tools.md).

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `[problem description]` — one problem in the user's words (a symptom, a file or function, a pasted finding).
- No argument — collect the problems reported earlier in this conversation: findings of `/code-review`,
  `/claude-security`, a review, a test run or a discussion. None found → ask the user to describe the problem.

## Procedure

1. **Candidates** — list the problems: one from the argument, or all from the conversation (each with its source).
   Skip the ones already fixed in this session.
2. **Ground** — for each candidate, read the code it points to (read-only; subagents for several unrelated areas) and
   confirm the evidence: file, symbol (`Class.method`) and a short code excerpt — no line numbers —, input and what
   goes wrong. Findings pasted with `file:line` are converted to symbol and excerpt. Map it to a module by the `**Source:**` lines of
   `docs/spec/` pages or the `AGENTS.md` tree, link the spec scenario it violates if there is one, and set kind,
   priority and effort by the rubric. Evidence not confirmed → say so and drop it unless the user insists (then
   write what was observed and mark the evidence `unconfirmed`).
3. **Duplicates** — compare with `docs/issues/*.md` by title, module and evidence files. A duplicate becomes an update
   of the existing file (new evidence, a raised priority via `git mv`), not a new file.
4. **Approve** — show one table: file name, kind, priority, effort, module, title; mark updates of existing files. Ask
   which to save (multi-select, all preselected).
5. **Write** the approved files per the format; create `docs/issues/` if missing. Verify: every file name matches its
   `**Priority:**`, every evidence path and symbol exists and a distinctive line of each excerpt is found by `git grep -F`, every relative link resolves.
6. **Summary** — files written or updated. Next: `as:fix` (shows the list by priority and plans the one you choose) or
   `as:fix <slug>`. Do not commit.
