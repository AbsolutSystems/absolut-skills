# Codex mapping

- Plugin name `as` → skills are available as `$as:<skill>`.
- Use native Codex file and shell primitives.
- `policy.allow_implicit_invocation: false` in `agents/openai.yaml` restricts a skill to explicit invocation.
- Arguments are passed as plain text after the skill mention.
- Subagents: use them if the host provides them; otherwise run the same analysis sequentially in the main thread.
- Without subagents, `as:tech-lead` options: one recommended architecture with its main alternative in a line;
  the 2–3 option comparison only when the user asks for it.
- Asking the user: ask in plain text, numbered, with suggested options, and wait for the answer.
- Simplify and review (`as:finish`): follow `skills/finish/references/review.md`; use subagents for the review if available.
- Plan mode (`as:tech-lead` handoff) is a Claude Code feature: on Codex, present the plan, wait for
  approval, then implement step by step.
- Unattended run (`as:deliver`): start Codex with an approval policy that never asks, e.g.
  `codex --ask-for-approval never --sandbox workspace-write` (tests that need the network fail in that sandbox; use
  `--sandbox danger-full-access` only in a worktree or container you can throw away). Without subagents the stages run
  in the main thread, one after another.
- Worktrees (`as:worktree-create`, `as:worktree-close`): after create, suggest starting Codex in `<path>`; before
  removing a worktree the session is in, run the commands from `<main>` (`git -C <main>` or `cd <main>`).
