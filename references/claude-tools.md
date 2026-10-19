# Claude Code mapping

- Plugin name `as` → skills are available as `/as:<skill>`.
- Use native Claude Code file and shell tools (Read, Edit, Write, Bash, Glob, Grep).
- `disable-model-invocation: true` in `SKILL.md` makes a skill a slash command only (the model will not invoke it on its own).
- Arguments after the command are available in the skill body as `$ARGUMENTS`.
- Subagents: use the Agent tool with `subagent_type: "Explore"` for read-only analysis; several Agent calls in one message run in parallel.
- Asking the user: use AskUserQuestion (up to 4 questions per call; ask further batches if needed), with concrete options.
- Simplify (`as:finish`): the built-in `/simplify` skill via the Skill tool, or the `code-simplifier` agent if that plugin
  is installed; otherwise follow `skills/finish/references/review.md`.
- Review (`as:finish`): the built-in `/code-review` skill on the local diff via the Skill tool; otherwise follow
  `skills/finish/references/review.md` with read-only subagents.
- Plan mode (`as:tech-lead` handoff): switch with the EnterPlanMode tool (the user confirms the switch); in plan mode,
  write the plan to the plan file and request approval with ExitPlanMode.
- Launching another command (`as:tech-lead` handoff): invoke `feature-dev:feature-dev` with the Skill tool, passing the
  brief as arguments, only after the user agreed. Check it is installed first (`references/recommended-plugins.md`).
