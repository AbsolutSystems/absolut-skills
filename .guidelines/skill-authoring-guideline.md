# Skill authoring guideline

How to write and change skills, references and assets in `skills/` and `references/`.

## Rules

- Frontmatter keys: only those in `SKILL_KEYS` of `tools/validate.py` (`name`, `description`, `disable-model-invocation`,
  `user-invocable`, `allowed-tools`, `argument-hint`, `model`). `description` ≤ 1024 characters, double-quoted as in the existing skills.
- `description` says what the skill does and when to use it. Command-like skills end with "Use only when the user
  explicitly invokes as:<name>." and set `disable-model-invocation: true` plus `policy.allow_implicit_invocation: false`
  in `agents/openai.yaml`.
- Keep `SKILL.md` a procedure: numbered steps, approval gates before writes, "never delete without consent", a verify
  step, a short summary. Move long material (templates, briefs, tool tables) to `references/` and link it.
- Host-agnostic text only: refer to "subagents" and "ask the user"; put tool names (AskUserQuestion, EnterPlanMode,
  Skill tool, Codex equivalents) in `references/claude-tools.md` / `references/codex-tools.md`.
- Arguments: document them under "Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex)".
  An argument is a target (path, description, name) or a tuning value (`--lang`, `--depth`, `--since`). A mode that
  changes the procedure (audit only, a report of another kind) is a separate skill, not a flag; do not add a flag
  that duplicates a question the skill already asks.
- A problem a skill finds and does not fix now is offered as an issue per
  `skills/issue/references/issue-format.md` (with consent), not left only in the summary.
- Links are relative to the file and must resolve (checked by the validator); refer to other skills by path, not by copying.
- Assets that projects receive (e.g. `health.css`) are copied with a shell copy by the skill, never retyped by the agent.
- Deterministic work the agent would otherwise redo in every run (counting, parsing, linting) goes to
  `scripts/<name>.py`: standard library only, run from the project root with a path relative to the skill's
  directory, output the agent can read (JSON or `ERROR …` lines), linked from the skill, with a manual fallback when
  `python3` is missing. Judgement (mapping files to modules, classifying drift) stays in the procedure.
- Subagent briefs are fenced `text` blocks with `{placeholders}` and an exact list of sections to return.
- Instructions and generated docs are in English.

## Reference examples

- `skills/agent-docs/SKILL.md` — full procedure with analysis, clarification, report, gated write and verify.
- `skills/init/SKILL.md` — orchestrator that reuses other skills.
- `skills/tech-lead/SKILL.md` — model-invocable skill with a narrow description.
- `skills/agent-docs/references/analysis.md` — subagent brief format.
