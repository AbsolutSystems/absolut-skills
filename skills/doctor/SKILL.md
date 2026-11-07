---
name: doctor
description: "Quick read-only check of how a repository stands against the as plugin: the working principles block version, AGENTS.md/CLAUDE.md pairs and symlinks, the .guidelines/ index, copied stylesheet versions, spec and feature page lint, stale change proposals, open issues, the last health check, the CLI tools the skills need, and (on Claude Code) the recommended plugins. Deterministic, seconds, no subagents and no writes; every problem names the command that fixes it. Use only when the user explicitly invokes as:doctor."
disable-model-invocation: true
---

# Doctor

Read-only: do not modify files, install anything or save issues — report and name the fix. Answer in the user's
language. Use the invocation syntax of the current host: `/as:<skill>` in Claude Code, `$as:<skill>` in Codex. Host
mechanics: [Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).

`doctor` checks that the repository is wired to `as` correctly and up to date; whether the docs tell the truth about
the code is `as:docs-check`, the state of the code itself is `as:health`.

## Procedure

1. **Repository checks** — from the repository root run `python3 <this skill's directory>/scripts/doctor.py`
   ([scripts/doctor.py](scripts/doctor.py)). It prints JSON checks (`area`, `status` `OK` / `WARN` / `INFO`,
   `detail`, `fix`): working principles block, agent docs pairs, guidelines index and apps without guidelines,
   stylesheet copies, change proposals untouched for 30+ days, issues per priority and misnamed issue files, the last
   `as:health` run, and the tools `gh`, `uvx`, `npx`. It checks the repository's top level from any subdirectory.
   `ERROR` → report the message and stop. Without `python3`, check the same by hand, reading the files named above.
2. **Spec lint** — when `docs/spec/` or `docs/features/` exists, run `python3 <spec-docs skill
   directory>/scripts/spec_lint.py` ([../spec-docs/scripts/spec_lint.py](../spec-docs/scripts/spec_lint.py)) and count
   its `ERROR` lines per file; fix: `as:spec-docs <path>` for spec pages, `as:feature docs/features/<slug>` for feature
   pages.
3. **Plugins** — on Claude Code, check the plugins in
   [../../references/recommended-plugins.md](../../references/recommended-plugins.md) as described there:
   `INSTALLED` / `DISABLED` / `MISSING`, with the `claude plugin install` or `enable` command from that file as the
   fix. On Codex, say these are Claude Code plugins and skip.
4. **Report** — one table, `WARN` rows first, then `INFO`, then `OK` collapsed to one line per area:

   | Area | Status | Detail | Fix |
   |------|--------|--------|-----|

   Then at most three next steps, most useful first. Typical ones: `as:init` for a missing or older working
   principles block (it shows the change and asks), `as:agent-docs` for broken agent docs pairs or index,
   `as:guidelines <app> testing` for an app without guidelines, `as:health` when it never ran or is stale.
   `as:docs-check` is the next step when the user wants to know whether the docs still match the code.
