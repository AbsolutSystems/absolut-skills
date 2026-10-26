# Analysis: subagent briefs and report formats

## Finding the public contract

The contract is what other parts of the system (or users and external systems) can rely on. Look for, in order:

- Module facades / services exported from the module root, `api`/`port` packages, `index.ts` exports, workspace
  package `exports`/`main`.
- HTTP/gRPC/GraphQL endpoints, CLI commands, scheduled jobs that act on behalf of users.
- Events and messages emitted or consumed (domain events, Kafka/Rabbit topics, webhooks).
- Persistent state visible to others (shared tables, files) — only when other modules read it.
- Validation, error types and status codes returned through those entry points — these become `error` scenarios.
- Existing contract-level tests (integration, API, module tests) — strong evidence of intended behaviour.

Exclude internal helpers, private classes, and calls that other modules make only because a boundary is leaking (raise
those as open questions instead).

## Spec brief (one module, or app/system level)

Fill the placeholders and pass verbatim:

```text
You are analyzing one part of a repository to write a human-readable specification of its public contract.
Read-only: do not modify files.

Directory: {dir}
Level: {module | app | system}
ID prefix: {PREFIX}
Existing page content: {Markdown, or legacy HTML body, or "none"}
Existing IDs and kinds: {list or "none"} — keep them; next free scenario number is {n}
AGENTS.md content (if any): {content or "none"}
Child reports (app/system level): {reports or "none"}

Describe observable behaviour from the point of view of a caller, not the implementation. Read entry points, public
API, validation and error handling, emitted/consumed events, and contract-level tests. Cite evidence paths for every
claim. Do not invent behaviour; if code is ambiguous or looks like a bug, raise a question.
{module: derive requirements and Given/When/Then scenarios — at least one happy scenario per requirement, plus an
error scenario for each failure the code handles and edge scenarios for limits, empty input, idempotency, concurrency.}
{app/system: derive purpose, actors, module map and the main end-to-end flows from the child reports; read code only
to resolve gaps.}

Return exactly these sections:
1. Purpose — 1–3 sentences in business language.
2. Contract — operations: name, type (command | query | event | endpoint | job), input, result; evidence path.
3. Requirements — for each: ID (existing or new), SHALL sentence, scenarios with ID, kind (happy | error | edge),
   Given / When / Then, evidence path.
4. Business rules — invariants enforced by the code; evidence path.
5. Dependencies — uses (module + why), used by (module + why).
6. Glossary — domain terms with a one-line meaning.
7. Drift — for each claim in the existing page that is false or outdated: the claim / ID, why it is wrong, evidence.
   List existing scenario IDs that no longer apply (to be marked removed).
8. Open questions — what the code cannot tell; propose likely answers as options.
```

## Coverage brief (`as:spec-tests`, one module)

```text
You are checking whether the tests of one module verify its specified contract. Read-only: do not modify files.

Module: {dir}
Test locations: {paths}
Scenarios: {list of ID, kind, Given / When / Then}
Cheap-pass hits (scenario ID found in tests): {ID → file:line, or "none"}

For each scenario, find tests that set up the Given state, perform the When through the module's public entry point
(facade, endpoint, event handler), and assert the Then outcome. Confirm cheap-pass hits actually assert the scenario.

Classify each scenario:
- COVERED — a test exercises it through the public contract and asserts the outcome.
- PARTIAL — a test touches it but only through internal classes, misses part of the Then, or mocks the behaviour away.
- MISSING — no test found.

Return one line per scenario: ID | status | test file path and test name (or what is missing) | short reason.
Then: tests in the module that verify contract behaviour not present in the spec (candidate new scenarios).
```
