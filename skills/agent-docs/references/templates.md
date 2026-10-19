# Templates

Templates are shapes, not forms: drop sections with nothing true to say, keep within the line budgets, write in English.
Paths are relative to the file's directory. Include a "Specification" section only when the linked `docs/spec/` page exists.

## Repo root `AGENTS.md` (≤ ~40 lines)

```markdown
# <Project name>

<1–3 sentences: what the product is and who uses it.>

## Repository map

- `backend/` — <one line>. See `backend/AGENTS.md`.
- `frontend/` — <one line>. See `frontend/AGENTS.md`.
- `infra/` — <one line>.
- `docs/spec/` — human-readable specification of module contracts; start at `docs/spec/index.html`.

## Commands

- `<command>` — <what it does> (only repo-wide commands).

## Shared rules

- <Rules that apply to every app: branching, commit format, code review, CI.>

<Working principles block or its `off` marker, if present — owned by as:init, keep as is.>
```

## App root `AGENTS.md` (≤ ~80 lines)

```markdown
# <App name>

<1–3 sentences: what this application does and its role in the project.>

## Stack

- <Language/runtime, framework, build tool, database, messaging.>

## Architecture

- <Style, e.g. modular monolith. Modules live in `<path>`; one module = one domain.>
- <How modules communicate and what dependencies are allowed.>
- <Reference module to copy when adding a new one: `<path>`.>

## Key libraries

- `<internal-lib>` (internal) — <what it provides; what not to re-implement>.
- `<lib>` — <role>.

## Specification

- `<relative path>/docs/spec/<app>/index.html` — module map and cross-module flows (for humans; read when a task changes behaviour across modules).

## Commands

- `<build>` / `<test>` / `<single test>` / `<run locally>` / `<lint>`.

## Guidelines

Read the relevant file before working in that area:

- `.guidelines/testing-guideline.md` — read before writing or changing tests.
- `.guidelines/libraries-guideline.md` — read before adding a dependency or solving a cross-cutting concern.
- `.guidelines/architecture-guideline.md` — read before adding a module or crossing module boundaries.
- `.guidelines/code-style-guideline.md` — read before writing new code.
```

## Module `AGENTS.md` (≤ ~40 lines)

```markdown
# <Module name>

<1–2 sentences: responsibility / domain.>

## Contents

- `<subdir or key file>` — <one line>.

## Public API

- <Entry points other modules may use: facades, events, endpoints.>

## Dependencies

- <Modules and libraries this one depends on; what must not depend on it.>

## Pitfalls

- <Non-obvious behaviour, invariants, legacy parts.>

## Specification

- `<relative path>/docs/spec/<app>/<module>.html` — public contract as scenarios with IDs (`<PREFIX>-NNN`). Read before
  changing the module's observable behaviour; tag contract tests with scenario IDs; report scenarios that no longer hold.
```

## `CLAUDE.md` (next to every `AGENTS.md`)

```markdown
@AGENTS.md
```

## Guidelines (`<app>/.guidelines/<topic>-guideline.md`)

Common shape for every guideline:

```markdown
# <Topic> guideline

<One sentence: scope of this guideline.>

## Rules

- <Imperative rule.> (e.g. "Use `<lib>` for X; do not use Y.")

## Reference examples

- `<path>` — <what it demonstrates>.
```

Topic-specific content to cover when there is evidence:

- **testing** — test levels and what each covers; frameworks and helpers; location and naming; data setup (builders,
  fixtures, testcontainers); what a new feature must ship with; how to run all tests and a single test.
- **libraries** — internal libraries first (what they provide, what not to re-implement); libraries by role; preferred
  choice when two exist; how to add a dependency.
- **architecture** — modules and boundaries; allowed dependencies and communication; layering inside a module; where new
  code goes; enforced rules (ArchUnit, lint boundaries).
- **code-style** — formatter/linter; naming; error handling; logging; DTO/mapping conventions.
- **api**, **data**, **security**, frontend topics (state, components, styling, i18n) — only when the area exists.
