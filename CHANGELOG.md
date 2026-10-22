# Changelog

## 1.2.0

- `tech-lead`: the approved implementation plan is saved as a `## Plan` checklist in the change proposal
  (`docs/spec/changes/<slug>.md`), so it survives the session and is reviewed with the PR; steps are ticked during
  implementation, and changes made during plan-mode approval are written back. `finish` verifies unticked steps
  before archiving the proposal.
- `agent-docs`: maps spec pages to directories by the Markdown `**Source:**` meta line (the `<dl class="meta">` of
  legacy HTML pages only as a fallback).
- `finish`: baseline and reruns include the documented lint, type-check and build commands; the summary suggests
  `/claude-security` when the diff touches authentication, input handling, secrets or data access.
- `tech-lead`: the bug path ends with a handoff — approval, failing test first, fix, `as:finish`.
- `worktree-create`: copies ignored `.env*` files from any depth (monorepo apps) and offers to install dependencies;
  the undocumented `z <branch>` alias is removed.
- `finish`: lint and type errors only in unchanged files are recorded as pre-existing and do not stop the run.
- Validator: `disable-model-invocation` must match `policy.allow_implicit_invocation`; `#fragment` links must point to
  an existing heading or `<a id>` anchor; `skills/*/references/*.md` are link-checked too, ignoring examples in fenced
  code blocks and code spans.

## 1.1.0

- `spec-docs`: the specification is Markdown (`docs/spec/**/*.md`) formatted for people — breadcrumbs, table of
  contents, quoted SHALL sentences, scenarios with kind markers and Given/When/Then lists, `> [!NOTE]` open questions,
  stable `<a id>` anchors for scenario links. A legacy HTML spec is converted one to one on the next run (pages and
  change proposals), links to it are rewritten and `spec.css` is removed when unused.
- `tech-lead` writes change proposals and `finish` merges and archives them in Markdown; `agent-docs`, `init` and
  `help` point to `.md` pages.
- `health` keeps its HTML report and now owns the stylesheet: `docs/health/health.css` (from `assets/health.css`);
  older reports linking `../spec/spec.css` are relinked.

## 1.0.0

- `tech-lead`: large changes go to plan mode with milestones instead of `/feature-dev:feature-dev`, which cannot skip
  its exploration and architecture phases and would redo the design.
- Claude mapping: built-in `code-review` (local diff) is distinguished from the `code-review` plugin (PR); built-in
  skills are used only when the Claude Code version lists them. `claude-security` is invoked as `/claude-security`.
- `agent-docs`: writes only what the code cannot tell (line test); no purpose, stack, public API or dependencies
  sections; module `AGENTS.md` only for modules with pitfalls or rules; new `PRUNE` status; spec module links move to
  the app `AGENTS.md`. `finish` only corrects or adds necessary facts. Based on arXiv:2602.11988.

## 0.4.0

- `worktree-create` skill: creates a branch and a git worktree in `../<repo>-worktrees/<name>` from the current branch
  or `from <branch>`; asks before reusing an existing branch and offers to copy ignored `.env*` files.
- `worktree-close` skill: offers to commit uncommitted changes, shows unpushed commits and ignored files to be deleted,
  then removes the worktree (never `--force`) and keeps the branch.

## 0.3.1

- `agent-docs`: detects `AGENTS.md` ↔ `CLAUDE.md` symlinks and migrates them to regular files.
- `recommended-plugins.md`: retry with `claude plugin marketplace update claude-plugins-official` when a plugin is
  not found in an outdated local marketplace copy.
- Maintainer docs: `AGENTS.md` (regular file instead of a symlink), `skills/AGENTS.md`, `.guidelines/` for skill
  authoring and testing.

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
