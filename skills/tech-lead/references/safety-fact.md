# Safety fact

Used by [tech-lead](../SKILL.md) (size S plan, Bug step 3 — every bug fix, whatever its size) and
[fix](../../fix/SKILL.md) step 4 (an `S` issue fixed directly). M and L changes on the Feature path do not use it: their
scenarios and `**Risks:**` cover the same ground.

## The fact

The plan of a small change states the one fact the change is safe because of — the thing that, if false, would make
the change break something. "`formatPrice` has three callers and all pass a number" is a list of callers, not that
fact; "every caller passes a value already rounded to cents (`Cart.total`, `cart/Cart.ts`), so dropping the second
rounding changes no output" is.

## Evidence levels

| Level | Evidence |
|-------|----------|
| 1 | Stated |
| 2 | A `file:line` that shows it, or the library's source at the pinned version |
| 3 | The failure walked step by step from its input and shown not to reach the changed code |
| 4 | A script or test that runs the real code and fails loudly when the fact is false |
| 5 | Reproduced in the running application |

- Level 1 is never enough.
- Level 4 is required when the fact lies outside what the type system checks: a wire or file format (JSON an API
  returns, a CSV, a message), a database column or constraint, an event another service consumes, the behaviour of a
  library at its pinned version, ordering in a lifecycle (startup, request, transaction, component mount).
- Otherwise level 2 or 3.

## Where the search stops

A search for callers finds code that names the symbol. It misses these — check each that the change can reach:

- JSON an API returns (frontend, mobile app, a partner, a stored response fixture);
- database columns read by a query, a view, a report or another service;
- events and queues, their consumers and stored messages;
- a consumer written in another language or in another repository;
- feature flags and configuration that select the code path;
- generated code (clients, ORM models, serializers);
- code reached only through configuration or reflection (dependency injection, routing tables, `getattr`, templates).

## Line in the plan

```markdown
**Safe because:** <fact> — level <n> — <evidence: file:line, or the command and its output>
```

When the fact could not be raised above level 1, the line says `unproven` instead of a level, and the plan names the
cheapest check that would raise it:

```markdown
**Safe because:** no client reads `total_cents` from `GET /orders/{id}` — unproven — check: `git grep -n total_cents`
in the mobile repository, or the access log of the last 7 days
```

## Scripts

While planning, a level 4 script lives in a temporary directory outside the repository (`${TMPDIR:-/tmp}/as-safety/`):
`tech-lead` writes no code into the project before the plan is approved. Its command and output go into the line.
During implementation, a script that expresses behaviour becomes the test of the change; any other is deleted, and
its command and output stay in the plan.
