# Templates

Templates are shapes, not forms: drop every section with nothing that passes the line test, keep within the line
budgets, write in English. Paths are relative to the file's directory. Include a "Specification" section only when the
linked `docs/spec/` pages exist.

Never write what an agent reads from the code in seconds: stack and versions (manifests), directory contents, public
API, dependencies, framework conventions. Write the rule behind them only when the code does not enforce it.

## Repo root `AGENTS.md` (≤ ~25 lines)

```markdown
# <Project name>

<One sentence: what the product is.>

## Repository map

- `backend/` — <one line>. See `backend/AGENTS.md`.
- `frontend/` — <one line>. See `frontend/AGENTS.md`.
- `docs/spec/` — human-readable specification of module contracts; start at `docs/spec/index.html`.

## Commands

- `<command>` — <what it does> (only repo-wide commands that are not obvious from the manifests).

## Shared rules

- <Rules that apply to every app and that the tooling does not enforce: branching, commit format, review, CI.>

<Working principles block or its `off` marker, if present — owned by as:init, keep as is.>
```

## App root `AGENTS.md` (≤ ~50 lines)

```markdown
# <App name>

## Commands

- `<build>` / `<test>` / `<single test>` / `<run locally>` / `<lint>` — exact invocations, with required env or profiles.

## Rules

- <Architecture rule the code does not enforce, e.g. "Modules talk only through events in `<path>`; no direct calls.">
- <Target vs legacy, e.g. "New tests use AssertJ; Hamcrest in `<path>` is legacy, do not extend it.">
- <Where new code goes / reference module to copy: `<path>`.>

## Internal libraries

- `<internal-lib>` — <what it provides; what not to re-implement by hand>.

## Pitfalls

- <App-wide trap with its consequence, e.g. "Integration tests need Docker; without it they are skipped, not failed.">

## Specification

Read the module's page before changing its observable behaviour; tag contract tests with scenario IDs (`<PREFIX>-NNN`):

- `<module dir>` → `<relative path>/docs/spec/<app>/<module>.html`

## Guidelines

Read the relevant file before working in that area:

- `.guidelines/testing-guideline.md` — read before writing or changing tests.
```

## Module `AGENTS.md` (≤ ~20 lines, only when the module has pitfalls or rules)

```markdown
# <Module name>

## Rules

- <Boundary or usage rule, e.g. "Do not call `OrderRepository` from outside this module; use `OrderFacade`.">

## Pitfalls

- <Invariant, non-obvious behaviour or legacy part, with the consequence of getting it wrong.>

## Commands

- `<single-module test command>` (only if it differs from the app pattern).
```

## `CLAUDE.md` (next to every `AGENTS.md`)

```markdown
@AGENTS.md
```

## Guidelines (`<app>/.guidelines/<topic>-guideline.md`)

Only rules the user confirmed or a tool enforces, plus reference files to copy. Common shape:

```markdown
# <Topic> guideline

<One sentence: scope of this guideline.>

## Rules

- <Imperative rule.> (e.g. "Use `<lib>` for X; do not use Y.")

## Reference examples

- `<path>` — <what it demonstrates>.
```

Topics: **testing** (what a new feature must ship with, which test level for what, data setup helpers to use),
**libraries** (preferred choice when two exist, how to add a dependency), **architecture** (where new code goes, allowed
communication), **code-style** (conventions the formatter/linter does not cover). **api**, **data**, **security** and
frontend topics only when the team has rules for them.
