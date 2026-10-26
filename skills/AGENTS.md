# Skills

Each directory is one skill of the `as` plugin: `SKILL.md` (frontmatter + host-agnostic procedure),
`agents/openai.yaml` (Codex interface and invocation policy), optional `references/` (loaded on demand), `assets/`
(copied verbatim, never generated) and `scripts/` (stdlib-only Python, tested in `tests/test_scripts.py`).

## Contents

- `help` — installation check, plugin status, workflow guide.
- `init` — orchestrates `agent-docs` → `spec-docs` → links → working principles → recommended plugins.
- `agent-docs` — `AGENTS.md`/`CLAUDE.md` hierarchy and `.guidelines/`.
- `spec-docs` — Markdown module contracts in `docs/spec/` (migrates legacy HTML); owns `references/markdown-format.md`
  and `scripts/spec_lint.py`.
- `tech-lead` — design and bug investigation; writes change proposals to `docs/spec/changes/`.
- `estimate` — client feature request analysis and hour estimate; writes `docs/estimates/<slug>/`; owns
  `scripts/estimate_totals.py`.
- `implement` — executes a proposal's approved `## Plan` step by step in any session.
- `finish` — wraps up a branch; merges and archives change proposals; owns `references/review.md` and
  `references/analysis.md`.
- `health` — periodic whole-project check; writes HTML to `docs/health/`; owns `assets/health.css`,
  `references/html-format.md` and `scripts/git_signals.py`.
- `worktree-create`, `worktree-close` — branch + git worktree in `../<repo>-worktrees/`; close keeps the branch.

## Dependencies between skills

- `init` and `finish` read `agent-docs/SKILL.md` and `spec-docs/SKILL.md` and follow them; `health` reuses
  `agent-docs/references/analysis.md` and `finish/references/review.md`; `tech-lead` proposals use
  `spec-docs/references/markdown-format.md`; `finish` runs `spec-docs/scripts/spec_lint.py`; `implement` finds proposals
  like `finish`; `tech-lead` reads `estimate`'s `analysis.md` (format in `estimate/references/estimate-format.md`) —
  renaming its sections means updating the From estimate path.
- Renaming or restructuring a step or reference in one skill means updating every skill that links to it — the
  validator checks link targets and `#anchors`, but not step numbers or section names quoted in prose.
- `references/recommended-plugins.md` (repo root) is shared by `init` and `help`.

## Pitfalls

- Skills with `disable-model-invocation: true` cannot be invoked by another skill; orchestrators read the other
  `SKILL.md` as instructions instead. `tech-lead` is the only model-invocable skill — keep its `description` narrow.
- `finish` step 5 uses its own diff-anchored brief (`finish/references/analysis.md`), not the full `spec-docs` and
  `agent-docs` briefs: one stance per prompt, sized for a smaller model. Steps 6–8 quote its section names
  (Proposal, Spec drift, New behaviour, Tests, Docs) — rename them together.
- `health.css` changes: add classes to `health/references/html-format.md` and bump the version in the file's first
  line (`health` asks before overwriting a project's copy).
- Spec format changes: update the skeletons in `markdown-format.md` and `change-format.md` together, and the "Legacy
  HTML pages" mapping when a construct changes.
- Ownership of generated files: `docs/spec/changes/` — `tech-lead` writes, `implement` ticks `## Plan` steps (and edits
  the plan or scenarios only after approval), `finish` merges and archives, `spec-docs` only reads (and converts legacy HTML
  proposals); `docs/estimates/` — `estimate` writes, `tech-lead` only sets `**Status:** accepted`; the working
  principles block in a project's root `AGENTS.md` — `init` writes, `agent-docs` preserves.
- Files generated in user projects are in English, except spec pages (`spec-docs --lang`) and pages that follow
  their language (`lang` in the marker on the first line of `docs/spec/index.md`): change proposals, health reports and
  estimate analyses; an estimate's `client.md` follows the client's request (`estimate --lang`).
