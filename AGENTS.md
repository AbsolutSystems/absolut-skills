# Absolut Skills maintainer guidance

Plugin `as` (marketplace `absolut-skills`) for Claude Code and Codex. Commands: `/as:<skill>` (Claude), `$as:<skill>` (Codex).
Skills are Markdown instructions executed by the coding agent; the only executable code is the validator and the
stdlib-only helper scripts in `skills/<name>/scripts/` for deterministic work (git statistics, spec lint).

## Repository map

- `skills/` — one directory per skill (the plugin's content). See `skills/AGENTS.md`.
- `references/` — host mappings (`claude-tools.md`, `codex-tools.md`) and `recommended-plugins.md`, shared by skills.
- `tools/validate.py` — stdlib-only validator for manifests, skill frontmatter, `openai.yaml` and Markdown links.
- `tests/` — pytest tests of the validator and the skill scripts.
- `.claude-plugin/` (manifest + marketplace), `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json` — host manifests.
- `README.md` (user docs), `skills/README.md` (catalogue), `CHANGELOG.md`.

## Rules

- `skills/` is the single host-agnostic source of truth. Host-specific mechanics go in `references/claude-tools.md` and `references/codex-tools.md`.
- Every skill = `skills/<name>/SKILL.md` + `skills/<name>/agents/openai.yaml`. `name` in the frontmatter = directory name.
- Do not add a `commands/` directory — Codex does not support it; a skill is also a slash command in Claude.
- The version is bumped together in `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` and `package.json`.
- A new or changed skill also updates `README.md`, the row in `skills/README.md`, and `CHANGELOG.md`.

## Commands

- `python3 tools/validate.py` — run after every change.
- `uv run --with pytest pytest tests` — validator and script tests.
- `claude plugin validate .` — official Claude Code check (one expected warning: root `CLAUDE.md` is not shipped as context).

## Guidelines

Read the relevant file before working in that area:

- `.guidelines/skill-authoring-guideline.md` — read before adding or editing a skill or a reference file.
- `.guidelines/testing-guideline.md` — read before changing the validator or verifying a skill change.

<!-- as:working-principles v1 -->
## Working principles

Solve the whole task with the least new code.

- Before editing, find everything the change must reach: callers, tests, fixtures, config, exports.
- Prefer, in order: no new code (is it needed at all?), what this codebase already has, the standard library, an
  installed dependency, and only then new code. Never add a dependency for a few lines.
- No abstractions, options, wrappers or "for later" code nobody asked for; keep the existing structure and conventions.
  Deleting beats adding.
- Fixing a bug: fix the root cause once, in the shared code, after checking every caller.
- New non-trivial logic (branching, parsing, money, security) ships with a small test.
- A deliberate shortcut gets a comment: `shortcut: <limit>, <when to upgrade>`.
- Never cut validation at trust boundaries, error handling that prevents data loss, security, accessibility, or anything
  the user asked for.
- End with one or two lines: what was skipped or not checked, and any risk.
<!-- /as:working-principles -->
