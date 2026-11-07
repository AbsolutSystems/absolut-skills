# Guideline topics

One file per topic: `<app>/.guidelines/<topic>-guideline.md`. For each topic: what to measure in the code, the
conflicts that usually turn up, and what to ask the team when the code cannot answer. Skip items that do not apply to
the app's stack.

## testing

Trigger: read before writing or changing tests.

- Measure: test frameworks and assertion libraries in use; test levels (unit, slice, integration with a real database
  or Testcontainers, end-to-end) and where each lives; naming of files and test methods; data setup (builders,
  fixtures, factories, SQL scripts, object mothers); mocking style (mocks of own classes vs fakes vs real
  collaborators); how time, randomness and IDs are controlled; how external HTTP is stubbed; tests tagged with spec
  scenario IDs.
- Conflicts: two frameworks or assertion styles (JUnit 4 and 5, AssertJ and Hamcrest, Jest and Vitest), mocks and an
  in-memory fake for the same port, H2 and Testcontainers.
- Ask: what a new feature must ship with (which level, how many paths); what may be mocked; whether a bug fix starts
  with a failing test; slow or flaky areas to avoid.

## architecture

Trigger: read before adding a module, a package or a dependency between modules.

- Measure: layers or slices and the package pattern per module; where business decisions live (entities, services,
  domain objects); direction of calls between modules (direct calls, events, a facade); shared kernel or common
  packages; how a new module is wired (configuration, registration).
- Conflicts: layered and feature-sliced packages side by side; modules calling each other's repositories; logic in
  controllers in some modules and in services in others.
- Ask: the target structure for a new module and the reference module to copy; allowed dependencies between modules;
  where code shared by two modules goes.

## api

Trigger: read before adding or changing an endpoint.

- Measure: controller style; request and response types (DTOs, records, generated from OpenAPI); validation (bean
  validation, schema libraries) and where it runs; error format and the exception-to-status mapping; pagination,
  sorting and filtering parameters; versioning; authentication and authorisation annotations; naming of paths.
- Conflicts: two error formats; entities returned directly next to DTOs; validation in controllers and in services.
- Ask: the error contract clients rely on; how breaking changes are introduced; who consumes the API (a frontend in
  this repository, external clients).

## data

Trigger: read before changing the schema, a query or a transaction.

- Measure: migration tool, file naming and whether migrations are ever edited; ORM vs SQL access and where queries
  live; transaction boundaries; IDs (sequences, UUIDs), timestamps, soft delete, auditing columns; optimistic locking
  (`@Version`, version columns); how bulk operations and imports are written; N+1 guards (fetch joins, entity graphs).
- Conflicts: repository methods and hand-written SQL for the same table; two ID strategies; mixed soft and hard delete.
- Ask: whether migrations must be backward compatible with the running version (zero-downtime deploys); data that must
  never be deleted; reporting or read replicas.

## frontend

Trigger: read before adding a page, a component or client-side state.

- Measure: component structure and file layout; styling approach (CSS modules, Tailwind, a design system and its
  components); server state (React Query, SWR, RTK Query, plain fetch) vs client state (context, a store); forms and
  validation; routing; how API types are obtained (generated or hand-written); data-test attributes and how components
  are tested; i18n.
- Conflicts: two state libraries; raw HTML controls next to design-system components; hand-written API types next to
  generated ones; server state copied into local state.
- Ask: the design system and where its components live; supported browsers and devices; accessibility level expected.

## libraries

Trigger: read before adding a dependency or choosing a library for a task.

- Measure: libraries with overlapping roles (HTTP clients, JSON, date/time, mapping, logging, utilities); internal
  libraries and what they provide; how versions are managed (BOM, catalog, workspace).
- Conflicts: two libraries for one role.
- Ask: the target library per role; what must not be re-implemented because an internal library has it; who approves a
  new dependency.

## code-style

Trigger: read before writing code in this application.

- Measure only what the formatter and linter leave open: naming of classes, methods and files beyond their rules;
  null handling (`Optional`, nullable types); exceptions vs result types; logging (levels, structured fields, what is
  never logged); comments and documentation comments.
- Conflicts: `Optional` and nulls mixed; checked and unchecked exceptions for the same kind of failure.
- Ask: conventions the team holds but no tool checks.

## security

Trigger: read before touching authentication, authorisation, input handling, secrets or personal data.

- Measure: how authentication and authorisation are enforced (filters, annotations, method security, guards); where
  ownership of a resource is checked; input validation and output encoding; secrets handling (env, vault); personal
  data in logs and exports; CSRF, CORS and rate-limit configuration.
- Conflicts: authorisation checked in controllers in some places and in services in others; endpoints without an
  explicit rule.
- Ask: roles and who may do what; data classified as personal or secret; compliance requirements (GDPR retention,
  audit logs).
