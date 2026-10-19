# Subagent briefs

Fill the placeholders and pass verbatim. All subagents are read-only.

## Explore

```text
Read-only: do not modify files. You are helping a tech lead understand the current code before designing a change.

Change being discussed: {one paragraph}
Area: {directories / modules}
Relevant AGENTS.md and spec excerpts: {excerpts or "none"}

Find and report, each with file paths:
1. Entry points involved today (endpoints, facades, handlers, jobs, UI routes).
2. Existing code that already does part of this or something similar — candidates to reuse or extend.
3. Data model and persistence involved; migrations tool in use.
4. Tests covering this area and their level (unit, integration, contract), one representative path each.
5. Constraints visible in code: boundaries, permissions, validation, feature flags, configuration.
6. Surprises: inconsistencies, legacy paths, behaviour that contradicts the spec.
Keep it under 40 lines.
```

## Architecture

```text
Read-only: do not modify files. Propose one architecture for a change, optimising for: {minimal change | clean
boundaries | scale and future needs}.

Change and requirements: {agreed requirements and scenarios so far}
What exists today: {summary from exploration, with paths}
Project rules: {architecture and other relevant guideline excerpts, working principles}

Return:
1. Approach — 3–6 sentences.
2. Changes — modules and files to add or modify; new or changed public contract (operations, events, endpoints).
3. Data — schema changes, migrations, backfill.
4. Fit — how it follows or bends the project's architecture rules.
5. Risks — what can go wrong; compatibility and rollout concerns.
6. Effort — S / M / L with a one-line justification.
7. When this option is the wrong choice.
Be concrete and honest about downsides; do not pad.
```

## Investigate

```text
Read-only: do not modify files. Verify or disprove one hypothesis about a bug.

Symptom: {expected vs actual, inputs, environment}
Code path: {entry point and files}
Hypothesis: {one cause}

Trace the code path for the given input. Report: verdict (confirmed / disproved / inconclusive), evidence (file:line,
values), and if confirmed, the minimal reproduction and other callers affected by the same cause.
```
