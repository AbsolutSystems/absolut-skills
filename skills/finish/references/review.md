# Simplify and review criteria

Simplify: used when the host has no dedicated simplify tool, and as the bar its output must meet. Review: the bar of
[as:review](../../review/SKILL.md) and of any change checked against it. Scope is always
the diff from the base; read the surrounding code and, when a signature or behaviour changes, every caller.

## Simplify

Goal: the same behaviour with less, clearer code. Never change behaviour, public contracts or error handling.

- Replace new code with what the codebase, the standard library or an installed dependency already provides.
- Remove dead code, unused parameters, speculative options, abstractions and wrappers with a single use, and leftover
  debugging.
- Flatten needless nesting, merge duplicated branches, use clear names; follow the existing conventions and structure.
- Keep validation at trust boundaries, error handling that prevents data loss, and security checks.
- Leave code outside the diff alone, except a caller that must change with it.

## Review

Look for, in this order of weight:

1. Bugs — wrong results, broken edge cases, broken callers.
2. Security and data loss — injection, missing authorization, secrets, destructive operations without guards.
3. Behaviour under expected load — N+1 queries, unbounded loops or memory, missing pagination or timeouts.
4. Risky logic without a test.
5. Needless slowness.
6. Unnecessary code.

Every finding must name a concrete input or situation that produces the wrong outcome; drop findings without one.
Before reporting, check that the input can reach the code (callers, validation upstream, types, framework guarantees)
and that no existing guard or test already handles it. Report only what the diff introduces or makes reachable. Not
findings: style, naming, formatting, alternative designs without a defect, what lint, types or tests already enforce,
hypothetical future needs. No quota — zero findings is a valid result.
Propose the smallest fix, preferring deletion. Group findings:

- **Must fix** — bugs, security, data loss.
- **Should fix** — load problems, untested risky logic.
- **Nice to have** — speed, unnecessary code.

Each finding: file and line, what the code does, the failure scenario, the fix. End with a verdict: ship, or the list
of fixes needed first, and what was not checked.
