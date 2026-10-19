# Working principles block

A fixed block of behaviour rules for coding agents, inserted verbatim by `as:init` at the end of the repo root
`AGENTS.md` when the user opts in. `as:agent-docs` preserves it. It is team policy, not a fact derived from code, so it is never generated, paraphrased or merged with other
text — copy everything between the markers, including the markers. The version in the opening marker identifies the
text; when it differs from the block in a repository, replace the whole block.

If the user declines, write only `<!-- as:working-principles off -->` in the root `AGENTS.md`, so later runs do not ask
again. To ask again, the user deletes that line.

```markdown
<!-- as:working-principles v1 -->
## Working principles

Solve the whole task with the least new code.

- Before editing, find everything the change must reach: callers, tests, fixtures, config, exports.
- Prefer, in order: no new code (is it needed at all?), what this codebase already has, the standard library, an
  installed dependency, and only then new code. Never add a dependency for a few lines.
- No abstractions, options, wrappers or "for later" code nobody asked for; keep the existing structure and conventions.
  Deleting beats adding.
- Fixing a bug: fix the root cause once, in the shared code, after checking every caller.
- New non-trivial logic (branching, parsing, money, security) ships with a small test.
- A deliberate shortcut gets a comment: `shortcut: <limit>, <when to upgrade>`.
- Never cut validation at trust boundaries, error handling that prevents data loss, security, accessibility, or anything
  the user asked for.
- End with one or two lines: what was skipped or not checked, and any risk.
<!-- /as:working-principles -->
```
