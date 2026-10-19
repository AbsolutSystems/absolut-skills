# Skills

Each directory is one skill of the `as` plugin: `SKILL.md` (frontmatter + host-agnostic procedure),
`agents/openai.yaml` (Codex interface and invocation policy), optional `references/` (loaded on demand) and `assets/`
(copied verbatim, never generated).

## Contents

- `help` — installation check, plugin status, workflow guide.
- `init` — orchestrates `agent-docs` → `spec-docs` → links → working principles → recommended plugins.
- `agent-docs` — `AGENTS.md`/`CLAUDE.md` hierarchy and `.guidelines/`.
- `spec-docs` — HTML module contracts in `docs/spec/`; owns `assets/spec.css` and `references/html-format.md`.
- `tech-lead` — design and bug investigation; writes change proposals to `docs/spec/changes/`.
- `finish` — wraps up a branch; merges and archives change proposals; owns `references/review.md`.
- `health` — periodic whole-project check; writes `docs/health/`.
- `worktree-create`, `worktree-close` — branch + git worktree in `../<repo>-worktrees/`; close keeps the branch.

## Dependencies between skills

- `init` and `finish` read `agent-docs/SKILL.md` and `spec-docs/SKILL.md` and follow them; `health` reuses
  `agent-docs/references/analysis.md` and `finish/references/review.md`; `tech-lead` and `health` pages use the
  vocabulary in `spec-docs/references/html-format.md` and `spec-docs/assets/spec.css`.
- Renaming or restructuring a step or reference in one skill means updating every skill that links to it — the
  validator only checks that link targets exist, not that step numbers or section names still match.
- `references/recommended-plugins.md` (repo root) is shared by `init` and `help`.

## Pitfalls

- Skills with `disable-model-invocation: true` cannot be invoked by another skill; orchestrators read the other
  `SKILL.md` as instructions instead. `tech-lead` is the only model-invocable skill — keep its `description` narrow.
- `spec.css` changes: add classes to `html-format.md` and bump the version in the file's first line (`spec-docs`
  asks before overwriting a project's copy).
- Ownership of generated files: `docs/spec/changes/` — `tech-lead` writes, `finish` merges and archives, `spec-docs`
  only reads; the working principles block in a project's root `AGENTS.md` — `init` writes, `agent-docs` preserves.
- Files generated in user projects are in English, except spec and health pages (`--lang`).
