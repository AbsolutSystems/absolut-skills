# Codex mapping

- Plugin name `as` → skills are available as `$as:<skill>`.
- Use native Codex file and shell primitives.
- `policy.allow_implicit_invocation: false` in `agents/openai.yaml` restricts a skill to explicit invocation.
- Arguments are passed as plain text after the skill mention.
- Subagents: use them if the host provides them; otherwise run the same analysis sequentially in the main thread.
- Asking the user: ask in plain text, numbered, with suggested options, and wait for the answer.
- Simplify and review (`as:finish`): follow `skills/finish/references/review.md`; use subagents for the review if available.
- Plan mode and `/feature-dev` (`as:tech-lead` handoff) are Claude Code features: on Codex, present the plan, wait for
  approval, then implement step by step.
