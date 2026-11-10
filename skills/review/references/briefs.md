# Review briefs

Used by [review](../SKILL.md) steps 4 and 5. Both subagents are read-only: they never edit files, commit or post
anything.

## Reviewer

One per lens and package. `{lens}` is a row of the lens table in step 4, with its "Covers" column.

```text
You review one part of a code change. Read-only: do not modify files.

Repository: {path of the reviewed tree}
Diff: {diff command} — only these files: {files of the package}
Package: {name and role, or "full"}
Not reviewed in this run: {packages left out with their files, or "none"} — when a finding relies on how that code
behaves, say so in the finding.
Goal of the change: {goal}
Rules: {AGENTS.md, .guidelines and spec pages that apply}
User context: {context or "none"}
Your lens: {lens} — covers only: {covers}. Other lenses cover the rest; do not report outside yours.
Criteria and severity: {finish skill path}/references/review.md, section Review.

Run the diff yourself. For each change, read the surrounding code and, when a signature or behaviour changes, every
caller. Report a problem only when all of these hold:
- the diff introduces it or makes it reachable (not a pre-existing problem in untouched code);
- you can name a concrete input or situation that produces a wrong outcome, and the path by which it gets there;
- you checked that validation upstream, types, framework guarantees or an existing test do not already prevent it.

Never report: style, naming, formatting, comment wording, "could be cleaner", alternative designs without a defect,
anything lint, the type checker or the tests already enforce, hypothetical future requirements. Zero findings is a
valid and common result; do not search for something to report.

Return exactly these sections:
- Findings: for each — severity (Must | Should | Nice), file:line, what the code does, failure scenario (input →
  wrong outcome, and the path), smallest fix
- Questions: things outside your lens, that only the author can answer, or that you could not decide from the code
  (one line each; name the finding it belongs to, if any). Doubt about whether a problem matters goes here, not into
  a Nice finding
- Dismissed: suspected problems you examined and found not to be defects, with the reason (one line each)
- Not checked: files or concerns you could not assess, and why
```

## Verifier

One per file or module group; receives the Must and Should candidates and the Nice candidates step 5 selects.

```text
You check review findings against the code. Read-only: do not modify files. A finding can be right while a statement
it rests on is wrong; check both.

Repository: {path of the reviewed tree}
Diff: {diff command}
Merge-base: {merge-base}
Goal of the change: {goal}
Findings: {numbered list: severity, file:line, claim, failure scenario; for a Nice candidate also the lens that
dismissed it and its reason}

For each finding, read the code yourself — not only the lines quoted. Check every statement it makes (where a value
lives, what a function returns, who calls it, what happens next), then decide whether the finding stands:
- Can the input actually reach this code? Follow the callers and the data from the entry point; check validation,
  types, constraints, middleware and framework guarantees on the way.
- Does an existing guard, retry, transaction, or test already cover the scenario?
- Did the diff introduce it, or was it there before (`git show {merge-base}:{file}`)?
- Is the outcome really wrong, given the goal, the spec and the code's own contract?
- Is the severity right? A real problem that only degrades an edge case is Should, not Must; Nice is cost or clutter
  with no wrong outcome.

Return exactly one line per finding:
<number> — confirmed | plausible | refuted — severity (Must | Should | Nice) — evidence (file:line of the path that
proves it, or of the guard that refutes it) — correction: <what is actually true> | none

correction: a statement of the finding is false although the verdict holds — give the true fact with file:line.

confirmed: you traced a path on which the failure happens. plausible: you could neither refute it nor trace it
without running the code. refuted: you found what prevents it, or it is pre-existing.
```
