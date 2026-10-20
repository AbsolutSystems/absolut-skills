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

## Looking for what an agent would get wrong (app roots and modules)

Read code to find candidates and questions, not to describe it. Each candidate needs an evidence path.

- **Conflicts** — two libraries, frameworks or patterns for one role (two HTTP clients, two test frameworks, two
  mappers): ask which is the target and which is legacy.
- **Unenforced rules** — conventions followed consistently but not checked by a tool (module boundaries without
  ArchUnit/lint rules, events instead of direct calls, a mandatory base class or helper). Enforced rules need no line.
- **Internal libraries** — same groupId/scope/organization as the project, private registry, or a sibling repo/package
  (e.g. `preboot`): what they provide that an agent might re-implement by hand; ask when the code does not show it.
- **Pitfalls** — invariants, ordering or transaction traps, generated or legacy areas not to edit, tests that skip
  silently, required env or services.
- **Commands** — how to build, test, run a single test, run locally and lint; flag the ones missing or non-obvious
  (profiles, env, wrappers).
- **Testing strategy** — what level of tests a new feature needs, when the code does not make it clear; a reference test
  per kind to copy.
- **Existing docs** — lines that only repeat what the code shows (stack, directory contents, public API, dependencies):
  `PRUNE` candidates.

## Subagent brief

Fill the placeholders and pass verbatim:

```text
You are analyzing one directory of a repository to find what a coding agent would get wrong in it. Read-only: do not
modify files. Do not describe the code: an agent can read it. Report only what the code cannot tell, or tells only
after long exploration.

Directory: {dir}
Level: {repo-root | app-root | module}
Children that get their own AGENTS.md: {list or "none"}
Child reports (if any): {reports}
Existing AGENTS.md / CLAUDE.md / .guidelines content: {content or "none"}

Read manifests, build and CI files, configuration, and a representative sample of code and tests. Cite file paths.
Look for conflicts between conventions, rules followed but not enforced, internal libraries, pitfalls, missing or
non-obvious commands, and the testing strategy.

Return exactly these sections:
1. Map — (repo-root only) apps and top-level directories, one line each.
2. Commands — build/test/single test/run/lint commands that exist, with where they are defined; note missing ones.
3. Candidates — non-inferable facts (rules, target vs legacy, internal libraries, pitfalls), each with an evidence path.
4. Prune — lines in the existing docs that only repeat what the code shows, quoted.
5. Drift — for each claim in the existing docs that is false or outdated: the claim, why it is wrong, evidence.
6. Open questions — what only the team can answer and matters to an agent; propose likely answers as options.
7. Recommendations — concrete improvements that would help a coding agent (missing scripts, env docs, reference
   examples, rules worth enforcing with a tool).
```
