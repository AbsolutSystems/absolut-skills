# Absolut Skills maintainer guidance

Plugin `as` (marketplace `absolut-skills`) for Claude Code and Codex. Commands: `/as:<skill>` (Claude), `$as:<skill>` (Codex).

- `skills/` is the single host-agnostic source of truth. Host-specific mechanics go in `references/claude-tools.md` and `references/codex-tools.md`.
- Every skill = `skills/<name>/SKILL.md` + `skills/<name>/agents/openai.yaml`. `name` in the frontmatter = directory name.
- Do not add a `commands/` directory — Codex does not support it; a skill is also a slash command in Claude.
- The version is bumped together in `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` and `package.json`.
- After every change: `python3 tools/validate.py` (and optionally `claude plugin validate .`).
