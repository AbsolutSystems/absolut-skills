---
name: explain
description: "Explain code to a person who did not write it, as an HTML page with Mermaid diagrams in docs/explain/: a change (the current branch or a pull request) for a reviewer or stakeholder — what changed and why, before and after, how it works, data, tests, risks; a module or a question (\"how is the invoice total calculated\") for a newcomer — flow, rules, examples, where in the code; or a documented feature's logic on worked examples for the business — scenario cards with concrete numbers, a matrix, edge cases and open questions, so a wrong number can be spotted without reading code. Every number comes from a test, a source or a shown calculation; labels are in the language of the problem, not method names. Explains, never judges: findings belong to as:review. Use only when the user explicitly invokes as:explain."
disable-model-invocation: true
argument-hint: "[branch [base] | <PR number or URL> | <path> | docs/features/<slug> | \"<question>\"] [--for dev|business] [--lang en|pl]"
---

# Explain

Write one page that lets a person understand code they did not write, at their level. The page is read, printed to
PDF or sent; it has to stand without the code open. Format, sections and the content rules:
[references/page-format.md](references/page-format.md). Subagent briefs: [references/briefs.md](references/briefs.md).
Converse in the user's language. Host mechanics (subagents, asking): [Claude Code](../../references/claude-tools.md),
[Codex](../../references/codex-tools.md).

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `branch [base]` or no argument — **change**: the current branch's changes from base (as in
  [review](../review/SKILL.md) step 1, branch mode).
- `<PR number or URL>` — **change**: a pull request, read in a separate worktree as in
  [review](../review/SKILL.md) step 1, PR mode.
- `<path>` — **module**: how the module or directory works.
- `"<question>"` — **module**: how one behaviour works across the code ("how is the invoice total calculated").
- `docs/features/<slug>` — **feature**: the feature's logic on worked examples (page by `as:feature`).
- `--for dev|business` — audience. Default: `dev` for a change or module, `business` for a feature.
- `--lang en|pl` — page language (default: the spec language, `lang` in the marker on the first line of
  `docs/spec/index.md`, else English).

## Procedure

### 1. Target

Resolve the kind (change, module, feature) and the slug: `pr-<number>`, `branch-<branch>` (`/` → `-`), the module
directory name, the feature slug, or the question in kebab-case (a few words). Output:
`docs/explain/<kind>-<slug>.html`. Show the kind, audience, sections ([page format](references/page-format.md#sections))
and the output path; an existing page → ask whether to overwrite it (git keeps the old version) or stop.

### 2. Gather

- **Change** — the diff, merge-base and goal as in [review](../review/SKILL.md) steps 1–2, also ignoring
  `docs/explain/` (this skill's own output). For a PR the code is read in that worktree, but the page is written to
  `docs/explain/` of the current working copy. `--name-status` of the
  diff for the [architecture delta](references/page-format.md#architecture-delta) (decide it here, say why);
  migrations and schema files in the diff; tests added or changed; CI status for a PR. The change proposal of the branch
  (`docs/spec/changes/`) supplies the why and the scenarios.
- **Module** — the module's `AGENTS.md` and spec page (scenarios with IDs); its entry points (routes, handlers, jobs,
  public functions).
- **Feature** — the feature page, its acceptance criteria and the module scenarios they link (`**Realised by:**`), its
  `sources/` (spreadsheet text as saved by `feature`; an `.xlsx` without it → `python3 <feature skill directory>/scripts/xlsx_text.py <file.xlsx>`
  ([../feature/scripts/xlsx_text.py](../feature/scripts/xlsx_text.py))), and the tests that carry the scenario IDs (`git grep -n '<ID>'` over the
  test directories).

Then research the code with read-only subagents, in parallel (without subagents, in sequence); the main thread keeps
only their reports:

- **Structure** — a change with an architecture delta, and every module page (its `context` section): one subagent per
  touched module (for a module page, the module itself; for a question, each module its flow passes through) with the [inventory brief](references/briefs.md#inventory) —
  components, entry points and dependencies, before and after for a change, each with its evidence. Mechanical
  listing, so a small model will do.
- **Behaviour** — one subagent per flow or module with the [tracing brief](references/briefs.md#tracing): steps,
  decisions, calculations, errors.

Draw diagrams and tables only from items that carry evidence in these reports. Two reports that disagree, or an item
without evidence → read the code yourself, or leave it out and say so under `questions`. For the delta, match
components across the before and after inventories by responsibility: the same one under a new owner is `moved`, not
`removed` plus `added`.

### 3. Examples

Change and module pages need them when the code calculates, converts or decides by thresholds; feature pages always.
Every number on the page has one source, shown on its card:

- **test** — the expected value of an existing test (file and test name);
- **source** — a value from a document in `sources/` (file and place: sheet and cell, page);
- **calculation** — worked by hand from the code's rule, the formula written in full as in a spreadsheet cell
  (`=ROUND(SUM(B2:B4)*C1; 2)`), so the order of operations and the rounding point are visible.

Never invent a result. A hand calculation without a test, or a code result that differs from a source or an
acceptance criterion, gets the status `to-confirm` or `differs` and an entry under open questions. For a feature not
implemented yet, every card is a calculation from the sources and criteria, status `to-confirm`.

### 4. Write

Write the page per [references/page-format.md](references/page-format.md): its sections for the kind, the vocabulary
only, Mermaid diagrams under the content rules. Copy `assets/explain.css` from this skill's directory to
`docs/explain/explain.css` with a shell copy (do not read or retype it); if it exists and differs, ask before
overwriting — compare the version in its first line.

### 5. Fact check

Send the written page to one read-only subagent with the [fact-check brief](references/briefs.md#fact-check), on the
session model, never one of the researchers. It checks every claim the page makes about the code — diagram nodes and
edges, delta marks, before/after rows, rules and their scenario IDs, `path:symbol` references, test names and their
expected values, values quoted from `sources/` — against the code and the sources. Then:

- `refuted` → remove the claim, or correct it from the evidence the checker gives;
- `unclear` → reword it as uncertain ("appears to…"), or move it to `questions`;
- `confirmed` → keep.

Without subagents, do it yourself in a separate pass that re-reads the code, not the reports. Keep the counts for the
summary.

### 6. Verify

- `grep -nE 'style=|<style|<svg' docs/explain/<page>` finds nothing, and the only `<script>` is the Mermaid line of
  the format.
- Every required section of the kind is present and not empty; every number in the matrix equals the number on its
  card; every card names its source.
- Diagram and card labels pass the content checks of the format: no identifier-like label (`()`, `camelCase`,
  `snake_case`, a dotted path), no sublabel that repeats its label. Fix what fails.
- If the host has a browser tool, open the page and check that every diagram rendered (Mermaid shows "Syntax error
  in text" otherwise); without one, re-check the diagram source against the format's Mermaid rules.
- Read the page top to bottom as the audience: a `business` page is understandable without knowing the code. Rewrite
  what is not.

### 7. Summary

Path of the page and how to open it (any browser; diagrams need the internet once, printing to PDF keeps them),
sections written, the fact check (claims checked, corrected, removed), the open questions, and what was not checked
(flows not traced, numbers without a test). A `differs`
card or a behaviour that breaks an acceptance criterion is a problem found: offer to save it as an issue (`bug`, or
`spec-gap` when the rule is undefined) per [../issue/references/issue-format.md](../issue/references/issue-format.md),
`**Source:**` `as:explain`. Hand calculations without a test: suggest `as:spec-tests` or adding the test. If step 1
created a worktree for a PR, offer to remove it (`git worktree remove <path>`) — only after the user confirms. Do not
commit.
