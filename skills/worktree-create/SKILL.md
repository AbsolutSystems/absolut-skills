---
name: worktree-create
description: "Create a new git branch and a worktree for it next to the repository, in ../<repo>-worktrees/<name>, branched from the current branch or from a given branch; optionally copies ignored local .env files into it. Use only when the user explicitly invokes as:worktree-create."
disable-model-invocation: true
argument-hint: "<name> [from <branch>]"
---

# Worktree create

Creates branch `<name>` and checks it out in a new worktree at `<parent of main worktree>/<repo>-worktrees/<folder>`.
Answer in the user's language. Host mechanics (asking, switching the session to the new folder) are in
[claude-tools.md](../../references/claude-tools.md) and [codex-tools.md](../../references/codex-tools.md).

## Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex)

- `<name>` — required: the new branch name. The folder name is `<name>` with `/` replaced by `-`.
- `from <branch>` (also `z <branch>`) — optional base branch; default is the current branch.

Examples: `feature-x`, `feature/login from develop`.

## Steps

1. **Preflight**
   - `git rev-parse --show-toplevel` — stop if not in a git repository.
   - Main worktree = the first `worktree` entry of `git worktree list --porcelain` (works when invoked from another
     worktree). `<repo>` = its directory name; `<path>` = `<parent of main>/<repo>-worktrees/<folder>`.
   - No `<name>` → ask for it. Validate with `git check-ref-format --branch <name>`; invalid → stop and say why.
2. **Base**
   - Without `from`: `git branch --show-current`. Empty (detached HEAD) → use `git rev-parse HEAD` and say so.
   - With `from <branch>`: use the local branch if `git rev-parse --verify --quiet refs/heads/<branch>` succeeds,
     otherwise `origin/<branch>` if `refs/remotes/origin/<branch>` exists (ask whether to `git fetch origin <branch>`
     first), otherwise any commit-ish if `git rev-parse --verify --quiet "<branch>^{commit}"` succeeds (e.g.
     `origin/develop`, a tag). None → stop and list similar names from `git branch -a --list "*<branch>*"`.
3. **Conflicts** — check before creating anything:
   - `<path>` exists → stop.
   - Branch `<name>` already exists: if `git worktree list --porcelain` shows it checked out, stop and show that
     worktree's path; otherwise ask whether to check out the existing branch (ignoring the base) or stop.
   - No local branch but `refs/remotes/origin/<name>` exists → ask whether to track it (base becomes `origin/<name>`)
     or stop.
4. **Create** — `mkdir -p` the `<repo>-worktrees` directory, then run from the main worktree:
   - new branch: `git worktree add --no-track -b <name> <path> <base>` (no upstream, so `git push -u` later targets
     `<name>`, not the base);
   - tracking `origin/<name>` (approved in step 3): `git worktree add --track -b <name> <path> origin/<name>`;
   - existing branch (approved in step 3): `git worktree add <path> <name>`.
   On error, show git's message and stop; do not retry with `--force`.
5. **Local files** — list ignored `.env*` files at the top level of the main worktree:
   `git -C <main> ls-files --others --ignored --exclude-standard --directory -- '.env*'` (top-level files only).
   If any exist, ask which to copy (multi-select, default none). Copy each with `cp -n` into `<path>`; never overwrite.
6. **Verify** — `git -C <path> branch --show-current` equals `<name>` and `git worktree list` shows `<path>`.
7. **Summary** — path, branch, base (and commit), copied files, how to start working in the new folder (see the host
   mapping), and that `as:worktree-close <name>` removes the folder later while keeping the branch.
