# Signals: how to compute and prioritise

`$SINCE` is the `--since` window (default `12 months`), `$P` the scope path. Use raw `git` output: if the shell wraps
or filters git output (token-saving proxies), bypass that for these commands, or the counts will be wrong.

**Exclude everywhere**: the "Skip" directories from `../agent-docs/references/analysis.md`, generated code (paths
containing `generated`/`gen`, files with "do not edit" headers), lockfiles, `docs/`, and parallel resource files that
always change together by design (i18n/locale bundles, snapshots). Mention the exclusions in the report.

## Git signals

Run [../scripts/git_signals.py](../scripts/git_signals.py) from the repository root (`python3 <this skill's
directory>/scripts/git_signals.py --since "$SINCE" --path "$P"`, plus `--exclude '<glob>'` for project-specific
exclusions). It prints JSON with churn (commits and lines per file), change coupling pairs and frequently fixed tests,
computed as defined below, and calls git directly, so shell proxies do not affect it. Without `python3`, use the
commands below.

**Churn** — commits touching each file:

```bash
git log --since="$SINCE" --format= --name-only --no-renames -- "$P" | grep -v '^$' | sort | uniq -c | sort -rn
```

Lines changed per file (secondary):

```bash
git log --since="$SINCE" --format= --numstat --no-renames -- "$P" | awk 'NF==3 && $1!="-" {a[$3]+=$1+$2} END {for (f in a) print a[f], f}' | sort -rn
```

**Hotspots** — files in the top 20% by churn *and* top 20% by complexity (sum or max of function complexity from the
complexity tool; fallback: non-blank lines of code). Score = churn rank × complexity rank. Hotspots are the primary
candidates for review and refactoring, and where missing tests matter most.

**Change coupling** — files in *different modules* that change in the same commits (skip commits touching more than
30 files — mass renames and formatting):

```bash
git log --since="$SINCE" --format='--%h' --name-only --no-renames -- "$P"
```

For each pair: shared commits `n` and confidence `n / min(revisions(a), revisions(b))`. Report pairs with `n >= 5`
and confidence `>= 0.5`, aggregated to module pairs. Strong cross-module coupling with no import between the modules
means a hidden dependency (shared format, duplicated rule); with imports, a boundary that may be in the wrong place.

**Frequently fixed tests** — test files changed in commits whose subject matches
`fix|flaky|flake|stabili[sz]e|retry` (input: `git log --since="$SINCE" --format='@@%s' --name-only --no-renames`).
Two or more hits: flaky or brittle candidate.

**Ownership concentration** — `git shortlog -sn --since="$SINCE" -- <module>`: one author with more than 80% of the
commits on a hotspot is a knowledge risk; report it as `review`, low severity.

## Tool signals

Normalise every tool's output to per-file and per-module numbers: complexity (max and sum), coverage (line and branch
%), cycles (count and members), fan-in/fan-out, dead-code candidates, duplicated lines %, vulnerable dependencies (by
severity), outdated dependencies (major versions behind).

## Test quality brief (one module)

```text
You are assessing the tests of one module. Read-only: do not modify files.

Module: {dir}
Hotspots in this module: {files with churn and complexity}
Coverage: {per-file coverage or "unknown"}
Frequently fixed tests: {list or "none"}
Testing guideline: {path to .guidelines/testing-guideline.md or "none"}
Spec scenarios without tests: {from spec-docs --tests, or "n/a"}

Read the module's tests, starting with those covering the hotspots, and the production code they exercise.
Report, each with file paths and a one-line reason:
1. Gaps — risky code without tests: hotspots with low coverage, error and edge paths never exercised, public entry
   points with no test.
2. Excess — tests that add cost without protection: no assertions or only "does not throw"; asserting on mocks or
   internals instead of outcomes; mostly mocks; duplicates of another test; testing trivial getters/mapping; slow
   tests (sleeps, real network) where a faster level exists.
3. Brittleness — frequently fixed tests and why (timing, order dependence, shared state, real clock).
For each item propose the action (add, rewrite, merge, delete) and its effort (S/M/L).
```

## Prioritising

Severity:

- **high** — vulnerable dependency (high/critical), cycle between modules, hotspot with coverage below 40% or without
  tests, docs that state false facts.
- **medium** — other hotspots, strong hidden change coupling, flaky tests, excess tests in hotspots, duplication above
  5% in a module, major-version-outdated dependencies.
- **low** — dead code, unused dependencies, excess tests elsewhere, ownership concentration, minor drift.

Effort: **S** — one file or a few lines, no design decision (delete dead code, drop an unused dependency, add a test
for an untested branch, delete a test without assertions). **M** — several files in one module. **L** — crosses
modules or needs a design decision (break a cycle, split a hotspot).

Order: severity, then hotspot score, then effort (smaller first). Cap the report at 30 findings; summarise the rest
per category.
