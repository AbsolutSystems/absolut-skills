# Subagent briefs

Fill the placeholders and pass verbatim. All subagents are read-only.

## Impact

```text
Read-only: do not modify files. You are helping estimate a client's feature request: find what must change in the
code and how hard it is. Do not design the solution in detail and do not estimate hours.

Requirements: {R1…Rn, one line each}
Area: {directories / modules}
Relevant AGENTS.md and spec excerpts: {excerpts or "none"}

Report per requirement, each with file paths:
1. What exists today — code that already does it or part of it (then say what is missing).
2. What must change — entry points, modules, data model and migrations, UI views.
3. Patterns to follow — a similar feature to copy, with its path and its tests.
4. Difficulty signals — missing tests, high coupling, legacy code, external integrations, permissions, data volume.
Keep it under 50 lines.
```

## Consistency

```text
Read-only: do not modify files. Review a client's feature request as a business analyst who knows the application.
Find what the client did not think of, what contradicts the application, and what would serve them better.

Request: {request text or summary with quotes}
Requirements: {R1…Rn}
What exists today: {impact summary, with paths}
Spec scenarios of the touched modules: {IDs and titles or "none"}

Check: error and edge cases, roles and permissions, existing data (migration, history), notifications, admin and
reporting needs, languages, mobile and responsive views, performance and volumes, privacy and audit, conflicts with
current behaviour or the spec, a smaller version that delivers most of the value, an existing feature that covers it.

Return a table: type (gap | conflict | alternative | addition | risk), finding, evidence (path, scenario ID or request
quote), why it matters to the client, rough effect on effort (none / small / medium / large), and a question or
suggestion phrased for a non-technical client. Only findings that matter for this request — at most 10, most
important first. No generic advice.
```
