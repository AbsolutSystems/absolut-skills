# Tools per signal and ecosystem

Order of preference for every signal: **configured** (already in the project) → **ephemeral** (run once, with consent,
nothing added to the project) → **git+LLM** (always available). Write tool output to a temporary directory
(`$TMPDIR/as-health/`), never into the repository.

## Detecting configured tools

Look in: manifest scripts (`package.json` scripts, `Makefile`, `justfile`, `tox.ini`/`noxfile.py`, `Taskfile`),
build plugins (`pom.xml` `<plugin>`, `build.gradle*` `plugins {}`), config files (`.dependency-cruiser.*`,
`knip.json`, `.jscpd.json`, `.importlinter`, `detekt.yml`, `ruleset.xml`, `.golangci.yml`, `sonar-project.properties`),
test dependencies (ArchUnit, Konsist), CI steps, and existing reports (`target/site/jacoco/jacoco.xml`,
`build/reports/kover/`, `coverage/lcov.info`, `coverage.xml`, `coverage.out`). A coverage report is fresh when it is
newer than the last commit touching the code it covers.

If the project runs SonarQube/Sonar Cloud or similar, mention it and offer to use its results if the user can export them.

## Complexity (per function, aggregated per file)

| Ecosystem | Configured | Ephemeral |
|-----------|------------|-----------|
| Any | — | `uvx lizard --csv <dirs>` (many languages; cyclomatic complexity, NLOC, function length) |
| JVM | PMD, detekt, Checkstyle | lizard |
| JS/TS | eslint `complexity` rule | lizard |
| Python | radon, ruff `C901` | `uvx radon cc -j <dir>` |
| Go | gocyclo, golangci-lint `gocyclo` | lizard |

## Structural coupling and cycles

| Ecosystem | Configured | Ephemeral |
|-----------|------------|-----------|
| JVM | ArchUnit/Konsist tests, jdeps | `jdeps -summary -recursive <classes dir>` (JDK, needs a compiled build) |
| JS/TS | dependency-cruiser, madge, eslint boundaries | `npx madge --circular --json <src>`; `npx depcruise --output-type json <src>` |
| Python | import-linter | `uvx pydeps --show-deps --no-output <pkg>` |
| Go | — | `go list -deps -json ./...` (Go toolchain) |
| Any | — | git+LLM: imports between module directories from `git grep` on import statements |

Report: module dependency matrix, cycles, modules with highest fan-in and fan-out, imports that cross documented
boundaries (from `AGENTS.md`/`architecture-guideline.md`).

## Test coverage

| Ecosystem | Configured | Ephemeral |
|-----------|------------|-----------|
| JVM | JaCoCo / Kover task | — (needs build changes; recommend instead) |
| JS/TS | `vitest --coverage`, `jest --coverage`, c8 | `npx c8 <test command>` |
| Python | coverage.py, pytest-cov | `uvx --with pytest-cov pytest --cov --cov-report=json:<tmp>` (only if tests run under plain pytest) |
| Go | — | `go test -coverprofile=<tmp>/cover.out ./...` |
| .NET | coverlet | `dotnet test --collect:"XPlat Code Coverage" --results-directory <tmp>` |

Prefer a fresh existing report. Running the suite is "runs the test suite" cost — ask first.
Contract coverage comes from `as:spec-tests` when `docs/spec/` exists.

## Dead code and unused dependencies

| Ecosystem | Configured | Ephemeral |
|-----------|------------|-----------|
| JS/TS | knip, ts-prune, depcheck | `npx knip --reporter json` |
| Python | vulture, deptry | `uvx vulture <dir> --min-confidence 80`; `uvx deptry .` |
| Go | staticcheck `U1000` | `go run golang.org/x/tools/cmd/deadcode@latest ./...` |
| JVM | PMD unused rules, `mvn dependency:analyze` | `mvn -q dependency:analyze` (only reads; no build file changes) |

Dead-code results are candidates: verify reflection, DI, framework entry points and public API before reporting.

## Duplication

| Any | `npx jscpd --reporters json --output <tmp> <dirs>`; PMD CPD if configured |
|-----|---|

## Dependencies: vulnerabilities and age

| Ecosystem | Configured | Ephemeral |
|-----------|------------|-----------|
| Any | Renovate/Dependabot config (report open PR count if visible) | `docker run --rm -v "$PWD:/src:ro" ghcr.io/google/osv-scanner -r /src` or installed `osv-scanner` |
| JS/TS | — | `npm audit --json`, `npm outdated --json` (read-only) |
| Python | — | `uvx pip-audit` |
| JVM | OWASP dependency-check | `mvn -q versions:display-dependency-updates` |

## Optional, expensive

- Mutation testing (test strength) — PIT (JVM), Stryker (JS/TS), mutmut (Python). Only for one module the user picks.
- Security — if the `claude-security` plugin is installed, suggest running it on the hotspots; do not run it here.
