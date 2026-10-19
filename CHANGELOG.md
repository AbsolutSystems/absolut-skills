# Changelog

## 0.3.0

- `tech-lead` skill (auto-invoked): designs features and investigates bugs grounded in code, `AGENTS.md` and spec;
  parallel architecture options, decision record and proposed scenarios in `docs/spec/changes/<slug>.html`, plan, and
  handoff to plan mode or `/feature-dev`. `finish` merges implemented proposals into the spec and archives them;
  `spec-docs` reserves their IDs; `health` flags stale proposals.
- `health` skill: periodic whole-project check (hotspots, structural and change coupling, coverage and test quality,
  dead code, duplication, dependencies, docs drift) with configured or consented ephemeral tools; dated HTML report and
  JSON snapshot with trends in `docs/health/`; fixes small items on request. `spec.css` v2 adds report classes.
- `finish` skill: wraps up a feature on the branch's changes — simplify, review, spec drift check (intended vs
  regression), missing contract tests tagged with scenario IDs, `AGENTS.md` refresh; tests after each code change.
- `help` skill replaces `hello`: installation check, recommended Anthropic plugins status, and a workflow guide
  (onboarding, plan mode, build, review, commit, docs).
- `init` skill: runs `agent-docs`, then `spec-docs` for a chosen scope, then links the spec from `AGENTS.md`, with one
  shared inventory and an approval gate before each write; offers an opt-in, versioned Working principles block for the
  repo root `AGENTS.md` (inspired by ponytail); finally checks the recommended Anthropic plugins and
  installs missing ones with consent.
- `spec-docs` skill: builds and audits a human-readable HTML specification in `docs/spec/` (system, app and module
  contract pages with Given/When/Then scenarios and stable IDs) sharing one `spec.css`; `--tests` reports which contract
  scenarios are covered by tests.
- `agent-docs`: when `docs/spec/` exists, repo/app/module `AGENTS.md` link their spec page; missing links are reported as drift.

## 0.2.0

- `agent-docs` skill: builds and audits hierarchical `AGENTS.md` (+ `CLAUDE.md` importing it) and per-app `.guidelines/`, asks about ambiguities and recommends improvements.

## 0.1.0

- Initial structure for the `as` plugin (marketplace `absolut-skills`) for Claude Code and Codex.
- `hello` skill as a template.
- `tools/validate.py` — format validation for manifests and skills.
