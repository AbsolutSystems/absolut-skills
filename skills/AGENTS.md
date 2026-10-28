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
- `feature` — living feature docs in `docs/features/<slug>/` (page + `sources/`); owns
  `references/feature-format.md` and `scripts/xlsx_text.py`.
- `implement` — executes a proposal's approved `## Plan` step by step in any session.
- `deliver` — unattended loop over a feature's roadmap through `tech-lead`, `implement`, `finish` and `fix`; owns
  `references/autopilot.md` (the policy that replaces their questions, the stage brief and the report format).
- `finish` — wraps up a branch; merges and archives change proposals; owns `references/review.md` and
  `references/analysis.md`.
- `health` — periodic whole-project check; writes HTML to `docs/health/`; owns `assets/health.css`,
  `references/html-format.md` and `scripts/git_signals.py`.
- `issue` — saves known problems to `docs/issues/`; owns `references/issue-format.md` (file name, priority rubric,
  lifecycle), which every skill that saves or closes issues links.
- `fix` — works through `docs/issues/`; reuses the `tech-lead` Bug and Feature paths.
- `docs-check` — read-only audit: `agent-docs` and `spec-docs` steps 1–4, plugin status.
- `spec-tests` — scenario test coverage report; the brief lives in `spec-docs/references/analysis.md`.
- `worktree-create`, `worktree-close` — branch + git worktree in `../<repo>-worktrees/`; close keeps the branch.

## Dependencies between skills

- `init` and `finish` read `agent-docs/SKILL.md` and `spec-docs/SKILL.md` and follow them; `health` reuses
  `agent-docs/references/analysis.md` and `finish/references/review.md`; `tech-lead` proposals use
  `spec-docs/references/markdown-format.md`; `finish` runs `spec-docs/scripts/spec_lint.py`; `implement` finds proposals
  like `finish`; `tech-lead` reads `estimate`'s `analysis.md` (format in `estimate/references/estimate-format.md`) —
  renaming its sections means updating the From estimate path; `feature` seeds from it too. `tech-lead` (From feature),
  `finish` (step 6) and `docs-check` follow `feature/references/feature-format.md`; `spec_lint.py` checks feature pages
  (phase status words, `AC<n>` anchors, `sources/`) — change the format and the script together.
- Renaming or restructuring a step or reference in one skill means updating every skill that links to it — the
  validator checks link targets and `#anchors`, but not step numbers or section names quoted in prose.
- `deliver` follows `tech-lead` (From feature), `implement`, `finish`, `fix` and `finish/references/review.md`;
  `references/autopilot.md` names their questions and gates (finish review, spec drift, contract tests, implement
  deviations) — a new question or gate in those skills needs a policy line there, or the unattended run stalls on it.
- `references/recommended-plugins.md` (repo root) is shared by `init` and `help`.
- `fix` follows `tech-lead`'s `#bug` and `#feature` paths and `tech-lead` routes known-issue requests to `fix/SKILL.md`;
  `docs-check` follows `agent-docs` and `spec-docs` steps 1–4 and `init` step 6 by number — renumbering them means
  updating it. `health` closes issues by their `**Key:**`, so the snapshot `key` format and `issue-format.md` change together.

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
  principles block in a project's root `AGENTS.md` — `init` writes, `agent-docs` preserves; `docs/features/` —
  `feature` writes, `tech-lead` sets a phase `in progress`, `finish` sets it `done` and updates the page, `deliver`
  writes `<slug>/delivery.md`; `sources/` are never edited after saving.
- `docs/issues/` — any skill that finds a problem writes, only with the user's consent (`deliver` without asking, by
  its policy); deleted (with the fix, in the same diff) by `fix`, `tech-lead` (Bug), `finish` (archiving a proposal with `**Issue:**`) and `health` (finding
  gone). Never numbered: the priority prefix and slug avoid cross-branch collisions.
- Files generated in user projects are in English, except spec pages (`spec-docs --lang`) and pages that follow
  their language (`lang` in the marker on the first line of `docs/spec/index.md`): change proposals, health reports,
  issues, estimate analyses and feature pages (sources keep their own); an estimate's `client.md` follows the client's request (`estimate --lang`).
