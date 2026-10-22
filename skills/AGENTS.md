# Skills

Each directory is one skill of the `as` plugin: `SKILL.md` (frontmatter + host-agnostic procedure),
`agents/openai.yaml` (Codex interface and invocation policy), optional `references/` (loaded on demand) and `assets/`
(copied verbatim, never generated).

## Contents

- `help` — installation check, plugin status, workflow guide.
- `init` — orchestrates `agent-docs` → `spec-docs` → links → working principles → recommended plugins.
- `agent-docs` — `AGENTS.md`/`CLAUDE.md` hierarchy and `.guidelines/`.
- `spec-docs` — Markdown module contracts in `docs/spec/` (migrates legacy HTML); owns `references/markdown-format.md`.
- `tech-lead` — design and bug investigation; writes change proposals to `docs/spec/changes/`.
- `finish` — wraps up a branch; merges and archives change proposals; owns `references/review.md`.
- `health` — periodic whole-project check; writes HTML to `docs/health/`; owns `assets/health.css` and `references/html-format.md`.
- `worktree-create`, `worktree-close` — branch + git worktree in `../<repo>-worktrees/`; close keeps the branch.

## Dependencies between skills

- `init` and `finish` read `agent-docs/SKILL.md` and `spec-docs/SKILL.md` and follow them; `health` reuses
  `agent-docs/references/analysis.md` and `finish/references/review.md`; `tech-lead` proposals use
  `spec-docs/references/markdown-format.md`.
- Renaming or restructuring a step or reference in one skill means updating every skill that links to it — the
  validator checks link targets and `#anchors`, but not step numbers or section names quoted in prose.
- `references/recommended-plugins.md` (repo root) is shared by `init` and `help`.

## Pitfalls

- Skills with `disable-model-invocation: true` cannot be invoked by another skill; orchestrators read the other
  `SKILL.md` as instructions instead. `tech-lead` is the only model-invocable skill — keep its `description` narrow.
- `health.css` changes: add classes to `health/references/html-format.md` and bump the version in the file's first
  line (`health` asks before overwriting a project's copy).
- Spec format changes: update the skeletons in `markdown-format.md` and `change-format.md` together, and the "Legacy
  HTML pages" mapping when a construct changes.
- Ownership of generated files: `docs/spec/changes/` — `tech-lead` writes, `finish` merges and archives, `spec-docs`
  only reads (and converts legacy HTML proposals); the working principles block in a project's root `AGENTS.md` — `init` writes, `agent-docs` preserves.
- Files generated in user projects are in English, except spec and health pages (`--lang`).
