# Claude Code mapping

- Plugin name `as` → skills are available as `/as:<skill>`.
- Use native Claude Code file and shell tools (Read, Edit, Write, Bash, Glob, Grep).
- `disable-model-invocation: true` in `SKILL.md` makes a skill a slash command only (the model will not invoke it on its own).
- Arguments after the command are available in the skill body as `$ARGUMENTS`.
- Subagents: use the Agent tool with `subagent_type: "Explore"` for read-only analysis; several Agent calls in one message run in parallel.
- Subagent model: read-only briefs that find and classify (Explore, Investigate, `spec-docs`/`agent-docs` analysis,
  coverage, test quality, `finish` analysis, `estimate` Impact, `feature` legacy mapping) pass a smaller model in the Agent tool's `model` parameter (e.g. `sonnet`, or `haiku` for
  plain searches); Architecture briefs, `estimate` Consistency, `review` reviewers and verifiers and the `explain` fact check keep the
  session model; the `explain` inventory may use `haiku`, its tracing `sonnet`.
- Stronger model (opt-in): the subagents that keep the session model above are the judgement subagents. Before a
  skill starts the first of them, unless the session already runs on Fable, ask with AskUserQuestion whether to run
  them on Fable (better judgement, more tokens) — as one more question in a batch the skill asks at that point, when
  it has one. Yes → pass `model: "fable"` in those Agent calls. Ask once per run: the answer also covers a skill
  followed inside it (`finish` → `review`); a run that starts no judgement subagent asks nothing. `as:deliver` asks
  at start-up and records the answer with the start-up decisions; yes → the Plan and Final review stage subagents
  get `model: "fable"` (the other stages, and the review inside the Finish stage, stay on the session model). An
  Agent call refused because of the model → repeat it without `model` and say so in one line.
- Asking the user: use AskUserQuestion (up to 4 questions per call; ask further batches if needed), with concrete options.
- Simplify (`as:finish`): the built-in `simplify` skill via the Skill tool, or the `code-simplifier` agent if that plugin
  is installed; otherwise follow `skills/finish/references/review.md`.
- Review (`as:review`, also inside `as:finish` and `as:deliver`): reviewers and verifiers are Agent tool subagents
  with `subagent_type: "general-purpose"` on the session model (Explore reads excerpts, too little to judge a defect),
  told in the brief to stay read-only; one message with several Agent calls runs them in parallel.
- Explain (`as:explain`): inventory and tracing subagents are `Explore`; the fact check is `general-purpose` on the
  session model, told to stay read-only.
- Built-in skills depend on the Claude Code version: use one only if it appears in the available skills list, else take
  the fallback and say so in one line.
- Plan mode (`as:tech-lead` handoff): switch with the EnterPlanMode tool (the user confirms the switch); in plan mode,
  write the plan to the plan file and request approval with ExitPlanMode.
- Unattended run (`as:deliver`): permission prompts would stall it overnight — start it in auto mode (Shift+Tab until
  the indicator shows it), or with `claude --permission-mode bypassPermissions` only in a worktree or container you can
  throw away; keep the machine awake (`caffeinate -i` on macOS). Stages run as Agent tool subagents on the session
  model; a subagent cannot start subagents, so a stage's fan-outs run in sequence inside it. A long run gets its
  context compacted — the loop re-reads its state from the files every stage.
- Browser (`as:qa`, `as:qa-docs`): the `playwright` plugin from the official marketplace
  ([recommended plugins](recommended-plugins.md)) provides the browser tools `mcp__plugin_playwright_playwright__*`:
  `browser_navigate`, `browser_snapshot` (accessibility tree — find controls here, not by guessing selectors),
  `browser_click`, `browser_type`, `browser_fill_form`, `browser_resize`, `browser_take_screenshot` (`filename`
  relative to the project root, e.g. `.qa/<run>/J1-2-mobile.png` — it writes only inside the session's workspace),
  `browser_console_messages`, `browser_network_requests`, `browser_evaluate` (only to reset test data), `browser_close`.
  They are deferred tools: a subagent loads them first with ToolSearch (`select:<names>`) — say so in the brief. The
  tool also leaves logs and page snapshots in `.playwright-mcp/` in the project root: gitignore it with `.qa/`.
  Missing → `claude plugin install playwright@claude-plugins-official`, then restart the session. Subagents share the
  session's one browser: run them one after another. The judge reads screenshots with Read (it shows images).
- Worktrees (`as:worktree-create`, `as:worktree-close`): do not use EnterWorktree/ExitWorktree — they manage their own
  worktrees in `.claude/worktrees`. After create, suggest `cd <path> && claude` in a new terminal. Before removing a
  worktree the session is in, `cd <main>` in Bash first.
