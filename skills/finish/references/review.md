# Simplify and review criteria

Used when the host has no dedicated simplify or review tool, and as the bar any tool's output must meet. Scope is always
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
Propose the smallest fix, preferring deletion. Group findings:

- **Must fix** — bugs, security, data loss.
- **Should fix** — load problems, untested risky logic.
- **Nice to have** — speed, unnecessary code.

Each finding: file and line, what the code does, the failure scenario, the fix. End with a verdict: ship, or the list
of fixes needed first, and what was not checked.
