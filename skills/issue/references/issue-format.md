# Issue format

Known problems that are not fixed yet live in `docs/issues/`, one Markdown file per problem. The list of open
problems is the list of files; a fixed problem is a deleted file (git history keeps it). Every skill that finds a
problem it does not fix now offers to save it here, always with the user's consent.

## File name

`docs/issues/p<1-4>-<slug>.md`, for example `p1-exhaustion-divides-by-zero.md`.

- `p<1-4>` is the priority, so `ls docs/issues` lists the most important first.
- `<slug>` is a short descriptive kebab-case English name. It is the stable name of the issue: `as:fix <slug>`, the
  `**Issue:**` meta line of a change proposal and the conversation refer to it. A priority change is a `git mv` to the new
  prefix; the slug stays.
- No sequence numbers, so parallel branches never collide. Two branches that save the same problem under different
  slugs are caught by the duplicate check below.

## Priority

One rubric, so issues from different sessions and skills compare:

| Priority | Meaning |
|----------|---------|
| `p1` | Data loss or corruption, security hole, crash or blocker in a main flow |
| `p2` | Wrong result or broken feature in a main flow, no workaround |
| `p3` | Edge case, degraded behaviour, or a workaround exists |
| `p4` | Cosmetic, technical debt, clean-up |

Mapping from other sources: `as:health` severity `high` → `p2` (`p1` when it is about data or security), `medium` →
`p3`, `low` → `p4`; `as:finish` review Must → `p1`/`p2`, Should → `p3`, Nice → `p4`; external reviews by the same
rubric.

## Content

```markdown
# WatchReconciler drops bodyMassKg when merging

**Kind:** bug · **Priority:** p2 · **Effort:** S · **Module:** [Watch sync](../spec/watch-sync.md) · **Found:** 2026-10-26 · **Source:** as:spec-docs

## Problem

What happens and what should happen instead, as a concrete failure scenario. The spec scenario it violates, if any
([WS-014](../spec/watch-sync.md#WS-014)).

## Evidence

- `WatchReconciler.merge(phone:watch:)` in `Context/Data/WatchReconciler.swift` — copies only the score fields, so
  `bodyMassKg` set on the phone is lost:

  ~~~swift
  return Snapshot(scores: watch.scores, date: phone.date)
  ~~~

## Suggested fix

Root cause if known, and the fix in one or two sentences.
```

Meta line:

- `**Kind:**` — `bug`, `security`, `spec-gap` (behaviour the spec does not define), or the `as:health` categories
  `review`, `refactor`, `delete`, `add-tests`, `remove-tests`, `deps`, `docs`.
- `**Priority:**` — as in the file name. `**Effort:**` — `S` (one module, a few files, no contract change), `M`, `L`.
- `**Module:**` — link to the module's spec page, else the module directory in backticks.
- `**Found:**` — date. `**Source:**` — who found it: `as:finish review`, `as:health`, `as:spec-docs`, `as:tech-lead`,
  `/code-review`, `/claude-security`, `user`, …
- `**Key:**` — only for `as:health` findings: the finding's `key` from the snapshot, so the next run recognises it.

Language: like change proposals, the spec language (`lang` in the marker on the first line of `docs/spec/index.md`),
else English. Kind, priority and effort values, headings and file names stay English.

## Rules

- **Evidence or no issue** — at least one location that shows the problem (or a command and its output).
- **Stable locations** — never line numbers: they go stale with the next edit. Name the file and the symbol
  (`Class.method`, function, endpoint, config key) and quote the few lines that show the problem (an excerpt that
  `git grep` finds), so the place can be found again after the code moves.
- **Duplicates** — before writing, compare with the existing files by title, module and evidence files. A duplicate
  means adding new evidence to the existing file (with consent), not a new file. shortcut: matching by reading titles
  and evidence; with hundreds of issues, add an index or a script.
- **Consent** — list the candidate issues with priority and title and ask which to save (multi-select).
- **Planned** — a change proposal that fixes an issue names it in its meta line: `` · **Issue:** `<slug>` `` (a plain
  slug, not a link: the prefix may change and the file is deleted when fixed). `as:fix` skips issues an open proposal
  names.
- **Closing** — the diff that fixes the problem deletes the file (`git rm`), so the fix and the closed issue land in
  one commit: `as:fix` after a direct fix, `as:finish` when it archives a proposal that links it, `as:health` when a
  finding with the issue's `**Key:**` is gone. An issue the team decides not to fix is deleted with the user's consent.
