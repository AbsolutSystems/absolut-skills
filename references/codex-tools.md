# Codex mapping

- Plugin name `as` → skills are available as `$as:<skill>`.
- Use native Codex file and shell primitives.
- `policy.allow_implicit_invocation: false` in `agents/openai.yaml` restricts a skill to explicit invocation.
- Arguments are passed as plain text after the skill mention.
- Subagents: use them if the host provides them; otherwise run the same analysis sequentially in the main thread.
- Stronger model for judgement subagents: not available — do not ask, they run on the session model.
- Without subagents, `as:tech-lead` options: one recommended architecture with its main alternative in a line;
  the 2–3 option comparison only when the user asks for it.
- Asking the user: ask in plain text, numbered, with suggested options, and wait for the answer.
- Asking the user to choose: first explain each decision in plain language, so the user can decide without reading
  the code: how it works today; when exactly it breaks (a concrete scenario — who does what, what they see); how often
  and how badly; then each option — what changes, pros, cons, cost — and your recommendation with the reason. Explain
  jargon (class names, framework or protocol terms) or leave it out. Only then list the numbered options, kept short
  because the explanation is already above.
  A batch of many similar decisions (bug or intended, keep or remove, one per finding) gets one table per batch
  instead — item, what it does today in a sentence, your recommendation, why — and the question asks only whether to
  accept the table or which items to change. Every question carries a recommendation: list the recommended option
  first, marked "(recommended)"; when you have none, say what is missing to form one. Never ask a bare "which of
  these are bugs?".
- Simplify (`as:finish`): follow `skills/finish/references/review.md`.
- Review (`as:review`, also inside `as:finish` and `as:deliver`): reviewers and verifiers as subagents if available;
  otherwise the lenses run one after another, and verification is a separate pass that re-reads the code. Provers
  (step 6) run one after another as subagents, or in the main thread without subagents.
- Plan mode (`as:tech-lead` handoff) is a Claude Code feature: on Codex, present the plan, wait for
  approval, then implement step by step.
- Unattended run (`as:deliver`): start Codex with an approval policy that never asks, e.g.
  `codex --ask-for-approval never --sandbox workspace-write` (tests that need the network fail in that sandbox; use
  `--sandbox danger-full-access` only in a worktree or container you can throw away). Without subagents the stages run
  in the main thread, one after another.
- Browser (`as:qa`, `as:qa-docs`, `as:ux`): the Playwright MCP server, added once with
  `codex mcp add playwright -- npx @playwright/mcp@latest` (Node.js required), then restart Codex. Its tools are
  named as in [Claude Code](claude-tools.md) without the `mcp__plugin_playwright_playwright__` prefix. The judge views
  screenshots with the host's image viewer. Without subagents, `as:qa` executes every scenario in the main thread
  and judges afterwards in a separate pass (the report marks the judge `same agent`).
- Mockups (`as:feature`, `as:roadmap`): the browser tools are optional, as in [Claude Code](claude-tools.md);
  without them, read the styles from the source and give the user the path of `mockups/index.html` to open.
- Worktrees (`as:worktree-create`, `as:worktree-close`): after create, suggest starting Codex in `<path>`; before
  removing a worktree the session is in, run the commands from `<main>` (`git -C <main>` or `cd <main>`).
