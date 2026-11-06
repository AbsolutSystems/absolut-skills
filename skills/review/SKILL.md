---
name: review
description: "Review a change for real defects with few false positives: your own branch before the PR (diff from base), or someone else's pull request (number or URL, checked out in a separate worktree against the PR's real base branch). Three read-only reviewers with disjoint scopes — correctness and security, goal and contract, UI only when the diff touches it — report only findings with a concrete failure scenario; a separate sceptical verifier then tries to refute each Must and Should finding and drops the ones it refutes. Also checks the PR description against the diff and whether the branch merges cleanly into its base. Own branch: you pick fixes, the rest can be saved to docs/issues/. Pull request: findings become inline GitHub review comments, posted only after you approve them. Use only when the user explicitly invokes as:review."
disable-model-invocation: true
argument-hint: "[<PR number or URL> | <base>] [context]"
---

# Review

Find the defects a change introduces, and only those. A finding is worth the reader's time only when it names an input
or situation that produces a wrong outcome and survives an attempt to refute it. Criteria and severity groups:
[../finish/references/review.md](../finish/references/review.md#review). Subagent briefs:
[references/briefs.md](references/briefs.md). Converse in the user's language. Host mechanics (subagents, asking):
[Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `<PR number or URL>` — **PR mode**: someone else's pull request. Read-only on the code; the output is review
  comments on GitHub.
- `<base>` — **branch mode**: the current branch from this ref. No argument → branch mode from
  `git merge-base HEAD origin/HEAD`, else the merge-base with `main` or `master`.
- `[context]` — free text after the target (for example "focus on the migrations"), passed to every reviewer.

## Procedure

### 1. Target

Set three values the later steps use: the **merge-base** (where the change starts), the **base tip** (what it merges
into) and the **diff command**.

**Branch mode** — the change is the working tree: commits since the merge-base plus uncommitted and untracked changes.
Merge-base: `git merge-base <base> HEAD`. Base tip: `<base>` when it names a branch, else (no argument, or a commit
such as `finish`'s default merge-base) `origin/HEAD`, else `main` or `master`. Diff command: `git diff <merge-base>` (working tree against the merge-base — a three-dot diff would miss uncommitted
work), plus the untracked files from `git ls-files --others --exclude-standard`, read whole.

**PR mode** — needs `gh` authenticated for this repository (else stop and say so). `<remote>` is the git remote that
points at the PR's repository (`gh repo view --json url` matched against `git remote -v`; usually `origin`, `upstream`
when `origin` is your fork):

1. `gh pr view <PR> --json number,title,body,url,state,author,baseRefName,headRefName,headRefOid,closingIssuesReferences`.
   A closed or merged PR → ask whether to continue.
2. `git fetch <remote> <baseRefName> pull/<number>/head` (works for PRs from forks too). Base tip is
   `<remote>/<baseRefName>` — the branch the PR merges into, never an assumed `main`. Merge-base:
   `git merge-base <base tip> <headRefOid>`. Diff command: `git diff <merge-base>...<headRefOid>`.
3. The current worktree is already at `headRefOid` and clean → review in place. Otherwise check it out in a separate
   worktree so your working copy stays untouched: `<parent of main worktree>/<repo>-worktrees/review-pr-<number>`
   (main worktree as in [worktree-create](../worktree-create/SKILL.md) step 1), created with
   `git worktree add --detach <path> <headRefOid>`; on a re-review, an existing clean one is moved with
   `git -C <path> checkout --detach <headRefOid>`. All later commands run there.

Ignore generated files, lockfiles, `docs/issues/`. Show base tip, head, files and `+/-` lines. Empty diff → stop.

### 2. Context

- **Goal** — two or three sentences: what the change is for. Sources by weight: PR description and linked issues,
  change proposal of the branch (`docs/spec/changes/`), commit messages, `[context]`.
- **Rules** — the `AGENTS.md` files and `.guidelines/` on the paths of the changed files; the spec pages
  (`docs/spec/`) of the touched modules.
- **PR mode** — CI status (`gh pr checks <number>`): failing checks are noted, not reviewed; their failures are not
  findings.
- **Description vs diff** — significant changes the description does not mention, or a stated goal the diff does not
  reach, become **questions for the author**, not findings. An imperfect description is normal; raise it only when it
  hides a change or makes the goal impossible to judge.

### 3. Reviewers

Diff of 1500 or more changed lines, or 20 or more files → split it into packages of related files by module or layer
(a file with its test together, at most 5 packages; more → say the PR should be split and review the riskiest 5).
Smaller diffs are one package.

For each package, in parallel, one read-only subagent per lens with the
[reviewer brief](references/briefs.md#reviewer):

| Lens | Covers | When |
|------|--------|------|
| Correctness and security | bugs, edge cases, error handling, concurrency and transactions, injection, authorization, secrets, data loss, behaviour under load | always |
| Goal and contract | the goal is reached, callers and consumers still work, spec scenarios and public API kept or intentionally changed, risky logic without a test | always |
| UI | loading, error and empty states, dead controls, rendering of missing data, double submit and stale state, accessibility that blocks use | the package has UI files |

Without subagents, run the lenses one after another in the main thread, each on its own pass over the diff.

### 4. Verify

Merge the candidates: same place and same cause → one finding (raised by two lenses → note it). Re-grade severity by
the criteria, not by the reviewer's label. Then send every **Must** and **Should** candidate to a sceptical
subagent with the [verifier brief](references/briefs.md#verifier) — one per file or module group, in parallel, never
the subagent that raised it. Without subagents, verify in a separate pass that re-reads the code from scratch.

- `confirmed` — keep.
- `plausible` — the verifier could not refute it, nor confirm it without running the code: keep, marked unverified.
- `refuted` — drop; keep only the count and a one-line reason for the summary.

**Nice** candidates are not verified; show their count and list them only on request.

### 5. Merge check

`git merge-tree --write-tree --name-only <base tip> <head>` (git 2.38+; `<head>` = `headRefOid`, or `HEAD` in branch
mode — committed work only, say so when there are uncommitted changes). Exit 0 → merges cleanly; exit 1 → the lines
after the first (the tree ID) up to the first blank line are the conflicting files; any other exit or an error
message → merge check not run, say why. Older git → skip and say so. This is merge readiness, not a finding.

### 6. Report

In the conversation:

- base ← head (PR: number, title, link), goal, scale, packages, CI;
- **verdict** — `ship` (no Must or Should), `fix first` (confirmed Must), or `fix or answer` (the rest);
- **Must** and **Should** findings: file and line, what the code does, the failure scenario, the smallest fix,
  `confirmed` or `plausible`;
- questions for the author; merge check result;
- not checked: lenses skipped (no UI files), packages left out, `N` findings refuted, `N` Nice findings.

### 7. Act

**Branch mode** — ask which findings to fix (multi-select; confirmed Must preselected). Before the first fix, run the
test, lint, type-check and build commands from the relevant `AGENTS.md` files and record the failures already there
(inside `finish`, its step 2 did this). Fix only the chosen findings, then rerun the checks; a fix that adds a failure
is reverted and reported. Then offer to save the unfixed Must and Should findings as issues (multi-select, all preselected; Nice only
on request) per [../issue/references/issue-format.md](../issue/references/issue-format.md), `**Source:**`
`as:review`.

**PR mode** — never edit the PR's code. Draft one review:

- an inline comment per Must and Should finding, on the line of the new side of the diff: severity, the problem, the
  failure scenario, the suggested fix; a `plausible` finding is phrased as a question. Written in the language of the PR
  description;
- the review body: goal as understood, verdict, questions for the author, merge check result, and the findings whose
  line is outside the diff.

Show the drafts and ask which comments to post (multi-select, all preselected) and the review event: `COMMENT`
(default), `REQUEST_CHANGES` (offered only with a confirmed Must), or `APPROVE` (offered only with no Must or Should).
Posting is public — nothing is sent without this approval. Write the payload to a temporary file outside the
repository and post it in one call:

```bash
gh api repos/{owner}/{repo}/pulls/<number>/reviews --method POST --input <payload.json>
# payload: {"commit_id": "<headRefOid>", "event": "COMMENT", "body": "...",
#           "comments": [{"path": "src/a.ts", "line": 42, "side": "RIGHT", "body": "..."}]}
```

Before posting, check every comment's `line` against the `@@` hunks of that file's new side in the diff; a line
outside them goes into the body instead. A `422` about comments anyway → move all inline comments into the body and
post once more; a `422` about the event (you cannot approve or request changes on your own PR) → post as `COMMENT`.
Show the review URL. Finally, offer to remove
the worktree (`git worktree remove <path>`) — only after the user confirms.

### 8. Summary

Findings per severity (fixed, saved as issues, or posted), refuted count, merge check, and what was not checked. Branch
mode, next steps: `/commit-commands:commit-push-pr` (Claude Code, if installed); if the diff touches authentication,
authorisation, input handling, secrets or data access, suggest `/claude-security` on the branch's changes.
