---
name: guidelines
description: "Write or improve an application's .guidelines/<topic>-guideline.md (testing, architecture, api, data, frontend, libraries, code-style, security) from the conventions its existing code actually follows: counts how consistently each convention is followed and which variant recent changes use, settles conflicts (target vs legacy) with the team, picks reference files to copy, and writes only the rules an agent would otherwise get wrong, after approval. Use only when the user explicitly invokes as:guidelines."
disable-model-invocation: true
argument-hint: "[app path] [topic ...]"
---

# Guidelines

A guideline tells a coding agent how this team writes one kind of code: which of two conventions is the target, what
a new endpoint, test or migration must look like, and which file to copy. The code shows what exists; only the team
knows which of it is the model. This skill measures the existing code to ask the right questions, and writes the
answers as short rules with reference examples.

**Line test** (as in [agent-docs](../agent-docs/SKILL.md)): a rule stays only if, without it, an agent would write the
code differently from the team or have to guess. Not rules: what a linter, formatter, type checker or architecture
test already enforces, descriptions of the code, and general advice the working principles block or any textbook
already gives.

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `[app path]` — the application whose `.guidelines/` to write (default: the only app; several → ask).
- `[topic ...]` — one or more of the topics in [references/topics.md](references/topics.md); without one, ask in
  step 1.

Host-specific mechanics (subagents, asking questions): [Claude Code](../../references/claude-tools.md),
[Codex](../../references/codex-tools.md). Answer in the user's language; guideline files are in English.

## Procedure

### 1. Scope

- App root: by the "Classifying directories" heuristics in
  [../agent-docs/references/analysis.md](../agent-docs/references/analysis.md). Read its `AGENTS.md`, its
  `.guidelines/`, the working principles block in the root `AGENTS.md`, and the tool configs that already enforce
  rules (linter, formatter, type checker strictness, ArchUnit/Konsist, dependency-cruiser, import-linter).
- Topics: without the argument, show one table — topic, existing file (yes/no), how much code it would govern (from a
  quick look: test files, controllers, migrations, components) — and ask which to do (multi-select). Recommend
  `testing` when it is missing: it changes most of what an agent writes. More than three topics → do three now and
  name the rest as the next run.

### 2. Analysis

One read-only subagent per topic, with the brief in [references/briefs.md](references/briefs.md) and the topic's
checklist from [references/topics.md](references/topics.md). Run them in parallel; without subagents, one topic after
another in the main thread. Each returns conventions with counts (followed / not followed), conflicts with the
variant recent changes use (files of the app changed in the last 6 months, from
`git log --since="6 months" --name-only --format= -- <app>`), reference candidates, traps, drift of an existing
guideline, and open questions — each with evidence paths. When the history is shorter than that, or one bulk commit
(an import, a reformat) touched most files, recency means nothing: say so, and decide on counts alone.

### 3. Clarify with the user

This is the main work: the team decides, the counts make the questions concrete. In small batches, most impactful
first:

1. **Conflicts** — "two ways to do X: A (n files, m of the recent changes), B (…). Which is the target?" Recommend the
   variant recent changes use (the more common one when recency means nothing). The other becomes legacy: not used in
   new code, not migrated unless a task is about it.
2. **Candidate rules** — a numbered list with their counts, in batches of about ten; the user keeps or drops by
   number. Mark as recommended those followed in at least ~80% of the places (and in recent changes); one followed in
   50–80% is asked as "rule or not?"; below that it is a conflict, not a rule.
3. **What the code cannot show** — the topic's questions from [references/topics.md](references/topics.md) that the
   analysis left open (for example what test level a new feature must ship with).

Unanswered questions are left out, not guessed.

### 4. Draft and report

Draft each file in the guideline shape of
[../agent-docs/references/templates.md](../agent-docs/references/templates.md): scope sentence, `## Rules`,
`## Reference examples`. Rules:

- Imperative, about new code, one line each; the reason in a few words only when the rule looks arbitrary without it.
- Legacy as one line: "`<B>` is legacy: do not use it in new code."
- Reference examples: 2–4 files that follow the rules, are recent, small and tested, each with what it demonstrates.
- About 40 lines per file at most; a longer one is split by topic.
- An existing guideline: keep the team's rules, add the confirmed ones, mark drift (a rule recent code contradicts) as
  a question, not a silent change.

Show each draft with the evidence next to every rule (counts and paths — the evidence is not written to the file),
plus the rules worth enforcing with a tool instead (an ArchUnit test, a lint rule). Ask for approval: all, a selected
subset, or cancel.

### 5. Write

- Write `<app>/.guidelines/<topic>-guideline.md`. Existing file: minimal edits, only the approved changes.
- Add each new file to the guideline index of the app `AGENTS.md` (`- .guidelines/<topic>-guideline.md — read before
  <trigger>.`, the shape in the `agent-docs` templates), creating the `## Guidelines` section if needed; touch
  nothing else in that file. No app `AGENTS.md` yet → create it with only that section, plus a `CLAUDE.md` holding
  exactly `@AGENTS.md`, and suggest `as:agent-docs` (or `as:init`) for the rest.

### 6. Verify

Every path under `## Reference examples` exists; every index entry matches a file in `.guidelines/` and every file
has an entry; no rule repeats what a configured tool enforces. Fix and recheck.

### 7. Issues and summary

Offer the tool-enforcement candidates as `p4` issues per
[../issue/references/issue-format.md](../issue/references/issue-format.md) (multi-select, with consent). Summary:
files written or updated, rules added, conflicts decided (target and legacy), open questions left. Do not commit.
`as:agent-docs` keeps the index in sync later; `as:doctor` reports an index that drifted.
