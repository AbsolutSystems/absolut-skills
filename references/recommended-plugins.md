# Recommended Claude Code plugins

Plugins from the official Anthropic marketplace `claude-plugins-official`
(<https://github.com/anthropics/claude-plugins-official>) that complement `as`. They exist for Claude Code only; on
Codex, skip any step that checks or installs them and say so in one sentence.

| Plugin | Provides | Invoke | Use when |
|--------|----------|--------|----------|
| `feature-dev` | Guided feature workflow; agents `code-explorer`, `code-architect`, `code-reviewer` | `/feature-dev:feature-dev [description]` | Building a multi-module feature without a prior `as:tech-lead` session (it would redo the design) |
| `frontend-design` | Skill for distinctive, production-grade UI | Triggers automatically on UI work | Building pages, components, frontend apps |
| `code-simplifier` | Agent that simplifies recently changed code without changing behaviour | Ask Claude to run the `code-simplifier` agent | After implementing, before committing |
| `code-review` | Multi-agent pull request review with confidence scoring | `/code-review:code-review` | A PR is open |
| `commit-commands` | Git workflow commands | `/commit-commands:commit`, `/commit-commands:commit-push-pr`, `/commit-commands:clean_gone` | Committing, opening a PR, pruning gone branches |
| `claude-security` | Deep vulnerability scan with verified findings and opt-in patches | `/claude-security` (or ask for a security scan) | Before a release, or after changing auth, input handling or data access |

## Checking

Run `claude plugin list --json`. Each entry has `id` (`<plugin>@claude-plugins-official`), `scope` and `enabled`;
the same plugin may appear once per scope. Classify each recommended plugin:

- `INSTALLED` — an entry with `enabled: true` applies here (scope `user`, or `project`/`local` for this repository).
- `DISABLED` — installed, but no applicable entry is enabled.
- `MISSING` — no entry.

If the command is unavailable, read `~/.claude/plugins/installed_plugins.json` (keys are plugin ids).

## Installing

Only after the user agreed, one plugin at a time:

```bash
claude plugin install <plugin>@claude-plugins-official      # MISSING
claude plugin enable <plugin>@claude-plugins-official       # DISABLED
```

If the marketplace is unknown, first run `claude plugin marketplace add anthropics/claude-plugins-official`. If install
fails with "not found in marketplace", the local copy is outdated: run
`claude plugin marketplace update claude-plugins-official` and retry.
Newly installed plugins become available after the Claude Code session is restarted.
