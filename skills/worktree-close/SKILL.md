---
name: worktree-close
description: "Close a git worktree: check that its changes are committed (offering to commit them if not), then remove the worktree folder and its git registration while keeping the branch. Use only when the user explicitly invokes as:worktree-close."
disable-model-invocation: true
argument-hint: "[<name>]"
---

# Worktree close

Removes a linked worktree's folder and its entry in `git worktree list`. The branch and its commits stay. Never closes
the main worktree, never uses `--force`, never deletes a branch. Answer in the user's language. Host mechanics are in
[claude-tools.md](../../references/claude-tools.md) and [codex-tools.md](../../references/codex-tools.md).

## Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex)

- `<name>` — optional: branch name or folder name of the worktree. Without it, the current worktree is closed if it is
  not the main one; otherwise ask which one, listing the linked worktrees.

## Steps

1. **Select** — parse `git worktree list --porcelain`; the first entry is the main worktree `<main>`. Match `<name>`
   against each linked worktree's branch (`refs/heads/<name>`) or folder name. No match → stop and list the linked
   worktrees. The match is `<main>` → stop. `<path>` = the matched worktree.
2. **State** — `git -C <path> status --porcelain`. Empty → step 4.
3. **Commit** — show `git -C <path> status --short` and `git -C <path> diff --stat HEAD`, and propose a commit message
   based on the diff. Ask: commit all changes with this message (the user may edit it) / stop. On approval run
   `git -C <path> add -A` and `git -C <path> commit -m "<message>"`; on failure (e.g. a hook) show the output and stop.
   If the user wants to keep some files out of the commit, stop without deleting anything. Re-run step 2; it must be clean.
4. **Before removal** — collect and show:
   - commits on no remote: `git -C <path> log --oneline HEAD --not --remotes` — for information only, the branch stays;
   - ignored files that will be deleted with the folder: `git -C <path> status --ignored --porcelain` entries starting
     with `!!` (e.g. `.env`, `node_modules/`).
   Ask for confirmation to remove `<path>`; without it, stop.
5. **Remove** — if the session's working directory is inside `<path>`, switch to `<main>` first (see the host mapping).
   Run `git -C <main> worktree remove <path>` (ignored files are removed with it); if git refuses, show its message and
   stop. Then `git -C <main> worktree prune`, and `rmdir` the parent `<repo>-worktrees` directory only if it is now empty.
6. **Verify and summarise** — `<path>` no longer exists and is absent from `git worktree list`; `git -C <main> branch
   --list <branch>` still shows the branch. Report: branch, last commit (`git -C <main> log -1 --oneline <branch>`),
   how many commits exist only locally (step 4), and the next step (e.g. open a PR, or `git branch -d <branch>` once merged).
