# Analysis: detection heuristics and subagent brief

## Classifying directories

**Skip** (never get their own file; mention in the parent only if relevant):
`node_modules`, `vendor`, `dist`, `build`, `target`, `out`, `.next`, `coverage`, generated code (`generated`, `gen`,
files with "do not edit" headers), test fixtures and snapshots, assets-only directories, and directories with 1–2 files.

**App root** — a directory containing an application or service manifest:

- JVM: `pom.xml`, `build.gradle`, `build.gradle.kts` with an application plugin / Spring Boot / main class.
- JS/TS: `package.json` with `start`/`dev`/`build` scripts or a framework (Next, Vite, Nest, Express, Angular…).
- Python: `pyproject.toml`/`setup.cfg` with an entry point or framework (Django, FastAPI, Flask).
- Go `go.mod` with `main` packages, Rust `Cargo.toml` with a `[[bin]]`/`src/main.rs`, .NET `*.csproj`, etc.
- A manifest that only builds a library (shared package) is a **module**, not an app root.
- If the repo root itself is the only app, merge repo root and app root.

**Module**:

- Modules of a modular monolith: sibling packages under a common parent (e.g. `src/main/java/<org>/<app>/modules/*`,
  `src/modules/*`, `apps/*/src/*`) that each own a domain and have similar internal structure. Document the parent in the
  app `AGENTS.md` ("modules live in …") and give each module its own file.
- Workspace packages (`workspaces` in `package.json`, `pnpm-workspace.yaml`, Gradle `settings.gradle` includes, Maven
  `<modules>`, Cargo/Go workspaces).
- Other directories with a clear, non-trivial responsibility, within `--depth`.

When a deep Java/Kotlin package path has no content of its own (`src/main/java/com/acme/...`), place the module file at
the directory that actually holds the module code, not at intermediate package directories.

## Collecting guideline material (app roots)

- **Testing**: test frameworks and assertion/mocking libraries from manifests; where tests live and naming patterns; unit vs
  integration vs e2e split (directories, tags, profiles, testcontainers, in-memory DBs); fixtures/builders/factories;
  how to run all tests and a single test; CI test steps. Pick one representative test per kind as a reference path.
- **Libraries**: dependencies grouped by role. Internal libraries — same groupId/scope/organization as the project,
  private registry, or a sibling repo/package (e.g. `preboot`) — are listed first with what they provide, as far as the
  code shows. Detect duplicates for the same role (two HTTP clients, two mappers) and raise them as questions.
- **Architecture**: modules and boundaries, how modules talk (direct calls, events, ports), layering inside a module,
  enforced rules (ArchUnit, dependency-cruiser, eslint boundaries), where a new module/feature goes, a reference module.
- **Code style**: formatter/linter config, naming conventions observed in the code, error handling and logging patterns,
  DTO/mapping conventions.
- **Optional areas**, only if present: API (OpenAPI, versioning, controllers), data (migrations tool, ORM, transactions),
  security (auth, permissions), frontend specifics (state management, components, styling, i18n).

## Subagent brief

Fill the placeholders and pass verbatim:

```text
You are analyzing one directory of a repository to document it for coding agents. Read-only: do not modify files.

Directory: {dir}
Level: {repo-root | app-root | module}
Children that get their own AGENTS.md: {list or "none"}
Child reports (if any): {reports}
Existing AGENTS.md / CLAUDE.md / .guidelines content: {content or "none"}

Read manifests, entry points, configuration, and a representative sample of code and tests. Prefer evidence over
assumptions; cite file paths. Do not describe children in depth — one line each.
{For app-root: also collect guideline material for testing, libraries, architecture, code style, and optional areas
(API, data, security, frontend) that exist.}

Return exactly these sections:
1. Purpose — 1–3 sentences.
2. Map — subdirectories and key files, one line each.
3. Commands — build/test/run/lint commands that exist, with where they are defined.
4. Facts — architecture, libraries, conventions, pitfalls; each with an evidence path.
5. Guideline material — (app-root only) per area: rules observed, reference file paths.
6. Drift — for each claim in the existing docs that is false or outdated: the claim, why it is wrong, evidence.
7. Open questions — what cannot be determined from code and matters to an agent; propose likely answers as options.
8. Recommendations — concrete improvements that would help a coding agent (missing scripts, env docs, reference examples, inconsistencies).
```
