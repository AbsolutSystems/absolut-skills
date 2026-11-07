# Guidelines subagent brief

One subagent per topic. Fill the placeholders and pass verbatim:

```text
You are measuring how one application writes one kind of code, so the team can decide on rules for a coding agent.
Read-only: do not modify files. Do not describe the code; count and compare.

Application root: {app path}
Topic: {topic}
Checklist (what to measure, usual conflicts, questions): {the topic's section of guidelines/references/topics.md}
Existing guideline: {content of .guidelines/{topic}-guideline.md or "none"}
Rules already enforced by tools: {linter, formatter, type checker, architecture tests — with config paths, or "none"}
Working principles block: {its rules or "none"}
Recently changed files of the app (last 6 months): {list, or "none: history too short or one bulk commit — use counts
only"}

For every checklist item that applies, find each variant in use and count the places (files, classes or call sites;
say which). For each, note how many of the recently changed files use it. Read enough code to be sure a count means
what you claim; sample when a count is large and say so. Skip what a listed tool already enforces.

Return exactly these sections:
1. Conventions — one line each: the candidate rule (imperative, about new code), followed in n of m places, used in r
   of the recent changes, evidence paths (2–3).
2. Conflicts — one block each: the role, each variant with its count, recent-change count and 2 paths; which variant
   recent changes favour.
3. Reference candidates — 2–4 files that follow the conventions, are recent, small and tested: path and what each
   demonstrates.
4. Traps — mistakes this code invites (a helper that must be used, an order of calls, a base class), each with
   evidence; files frequently changed in fix commits count as evidence.
5. Drift — rules of the existing guideline that recent code contradicts: the rule, the contradiction, paths.
6. Open questions — what only the team can answer for this topic, with likely answers as options.
7. Tool candidates — conventions an architecture test or a lint rule could enforce, with the tool.
```
