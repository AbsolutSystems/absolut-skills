---
name: feature
description: "Create and maintain a feature's living documentation in docs/features/<slug>/: why it exists, users and goals, non-goals, user-level acceptance criteria linked to the module scenarios that realise them, the user flow through the screens (with optional HTML mockups, in versions to choose from), a roadmap of phases (one change proposal each), decisions and the sources they came from — client orders, PDFs, spreadsheets, pasted e-mails and meeting notes saved verbatim in sources/. Seeds a feature from an accepted estimate or a roadmap stage, records new sources and what they change, refreshes the roadmap and status, documents an existing feature from the code and archived proposals, and maps a legacy documentation folder into the format. Use only when the user explicitly invokes as:feature."
disable-model-invocation: true
argument-hint: "<description | file… | docs/features/<slug> | docs/estimates/<slug> | docs/roadmap/<slug> [stage] | legacy folder> [--lang en|pl]"
---

# Feature

Keep one page per feature that a person or an agent reads first: why, what the user gets and how they move through
it, where the work stands and
what comes next, with links to the module contracts, the change proposals and the sources. The page is a distillate;
sources are kept verbatim next to it. Do not write production code, module pages or change proposals here — phases are
planned with `as:tech-lead docs/features/<slug>`.

Host-specific mechanics (subagents, asking questions): [Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).
Format, sources and legacy rules: [references/feature-format.md](references/feature-format.md). Mockups:
[references/mockups.md](references/mockups.md).

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `<description>` — a new feature in the user's words; files (a PDF order, a spreadsheet, notes) and text pasted in
  the same message (an e-mail, agreed points) are its first sources.
- `docs/features/<slug>` — update an existing feature: with new sources (files or pasted text) record them and what
  they change; without, refresh the roadmap and status and ask what changed.
- `docs/estimates/<slug>` — seed a feature from an estimate (written by `as:estimate`).
- `docs/roadmap/<slug> [stage]` — document one stage of a roadmap (written by `as:roadmap`) as a feature: the stage
  the user names, else the first `⏳ planned` one.
- A folder outside `docs/features/` — map legacy documentation into features ([Legacy](#legacy)).
- An existing feature named in the description (no page yet, code and archived proposals exist) — document it
  retroactively.
- `--lang en|pl` — language of a new page (default: the spec language, `lang` in the marker on the first line of
  `docs/spec/index.md`, else English). Existing pages keep theirs.

Converse in the user's language.

## Procedure

### 1. Inventory

- Read `docs/features/index.md` and the pages of features that may overlap; an existing slug for the same capability
  → update it instead of creating a second one.
- Read the spec map (`docs/spec/index.md`, app pages), open proposals in `docs/spec/changes/` and archived ones with a
  `**Feature:**` line for this feature, and `docs/estimates/` for a matching estimate.
- A legacy folder → [Legacy](#legacy) first.
- Read every new source in full. Spreadsheets: run
  `python3 <this skill's directory>/scripts/xlsx_text.py <file.xlsx>` and read its output (it is saved in step 5).
  A source that cannot be read → ask for an export (PDF, CSV).
- Pick the slug (short kebab-case) for a new feature and say it with the planned file names of the sources.

### 2. Ground

- Find the modules involved and their current scenarios: the spec pages first, then the code where the spec is
  missing or thin. Fan out read-only subagents with the brief "Explore" in
  [../tech-lead/references/briefs.md](../tech-lead/references/briefs.md) only for areas the spec does not cover, in parallel.
- A feature with a user interface: find the screens the user will pass through that exist today and how neighbouring
  flows behave there (entry points, confirmations, empty and error states) — the new flow follows them unless the
  user decides otherwise.
- From an estimate: requirements `R1…Rn` become acceptance criteria candidates, its blocks and steps the phase
  candidates, its open client questions the open questions; the estimate becomes a source by link.
- From a roadmap stage (format: [../roadmap/references/roadmap-format.md](../roadmap/references/roadmap-format.md)):
  the stage's goal and the roadmap's direction give the why, its capabilities `C<n>` are the acceptance criteria
  candidates, the roadmap's out of scope the non-goal candidates, its open questions for this stage the open
  questions, its `## Screens` rows for this stage the screens the flows start from. The roadmap's decisions bind
  the feature (also the look chosen there) — link them, do not copy; the roadmap becomes a source by link. A stage that already links a feature → update that feature instead.
- Retroactive: rebuild the criteria from the module scenarios already implemented (they are `**Realised by:**`), the
  user flow from the screens as they are, and the done phases from the archived proposals; ask about the why — the
  code does not know it.
- Update: compare each roadmap phase with its proposal (open in `changes/`, archived as `implemented` or `dropped`,
  or missing) and each `**Realised by:**` link with the module pages (removed or renumbered scenarios).

### 3. Clarify

Ask in small batches, most decisive first, with options from the sources and the code. Cover only what is still
unknown: the problem and who has it, how success is measured, non-goals, acceptance criteria the sources leave vague,
the user flow, and the split into phases — each phase ends with working, tested value and fits one change proposal; the first phase
is the smallest one worth shipping. Contradictions between sources: ask which wins (it becomes a decision) or keep
it as an open question. Stop when the page can be written.

**User flow** — for a feature with a user interface, the page is not ready for planning without it. Propose each
flow from the criteria and the existing screens, then settle what the criteria do not say: where the user starts,
the steps (screen, action, what they see next), what an empty state shows, what happens on each error and when
access is missing, and where the user lands after success. Behaviour only — no visual design. An existing page
without the section gets it on its next update. No user interface (an API, a background job) → one line saying so.

**Mockups** — once the flow is proposed, ask whether to show its screens as mockups, with your recommendation
([when](references/mockups.md#when)). On yes, follow [references/mockups.md](references/mockups.md): high fidelity
from the application's own styles when it has screens already, low fidelity otherwise; 2–3 versions where there is
a real choice, each a whole page behind a tab of the viewer. Give the path of `mockups/index.html`, name the version
you recommend, and iterate on the user's remarks until they pick. Every remark that changes behaviour changes the
flow text too. These are the only files written before step 4.

### 4. Report and gate

Show, briefly:

- new feature: purpose, acceptance criteria (one line each, with the source), the user flows (steps in one line
  each, with their states), the mockups and the version chosen per screen, phases with their AC, open questions,
  the roadmap stage it will be linked from (if any), and the source files to save;
- update: what each new source changes — AC added, changed or removed, flows changed, new decisions, contradictions — each with a
  short quote of the source; roadmap and status corrections from step 2; changes of the phases the user asked for.
  A change that touches a phase `in progress` needs its proposal adjusted too: say so and suggest `as:tech-lead` on
  that proposal after this run.

Ask for approval: all, a subset, or cancel.

### 5. Write

- Sources first: save pasted text verbatim with its header, copy files with a shell copy (from inside the repository:
  `git mv`), and write the spreadsheet text next to each `.xlsx` (`xlsx_text.py <file.xlsx> > <file>.md`; list both in one
  `## Sources` row). Never edit
  or overwrite an existing source; a newer version is a new file.
- Write `docs/features/<slug>/index.md` from the skeleton, or edit the existing page minimally: keep hand-written
  text and every `AC`, `UF`, `D`, `Q` ID; new ones take the next number; removed criteria get the removed status. Set
  `**Updated:**` to today and the current commit (`git rev-parse --short HEAD`) and rewrite the Now line.
- Mockups: rename each chosen version without its letter, delete the rejected ones, bring `tabs.js` in line, link
  the viewer from each flow's meta line and record each choice as a decision.
- Add or update the feature's row in `docs/features/index.md` (create it from the skeleton when missing).
- From a roadmap stage: put `**Roadmap:**` with a link to the roadmap page on the feature's meta line, and on the
  roadmap page add the stage's `**Feature:**` link, set the stage to `🔄 in progress`, and bring the roadmap's
  `**Status:**` (`draft` → `active`), Now line, `**Updated:**` and its row in `docs/roadmap/index.md` in line with
  that — nothing else there.
- Do not touch module pages, proposals, estimates or code. Never delete a page or a source without consent.

### 6. Verify

- Run `python3 <spec-docs skill directory>/scripts/spec_lint.py` from the repository root
  ([../spec-docs/scripts/spec_lint.py](../spec-docs/scripts/spec_lint.py); it checks `docs/features/` too) and fix
  every `ERROR` in the feature pages: links and anchors, roadmap phases against proposals, sources not listed. Without
  `python3`, check the same by hand. When a roadmap page was edited, run it again with `--features docs/roadmap`.
- The top of the page fits about one screen; source text is linked, not copied.
- A feature with a user interface has `## User flow`: every active criterion a user reaches through the interface is
  named by a flow, and every flow says its empty, error and no-access states (or "none").
- Mockups: no version letters left, every file is in `tabs.js` and opens, the viewer is linked from its flow, and
  no mockup shows a step, state or wording the flow text does not have.

### 7. Summary

Files written (page, catalogue, sources saved or moved, mockups), acceptance criteria and phases, open questions, and what was
not checked (sources not readable, areas not explored, where a mockup only approximates the application's look). Next: `as:tech-lead docs/features/<slug>` plans the next
`planned` phase as a change proposal (then `as:implement` and `as:finish`, which updates this roadmap); a new e-mail
or document → `as:feature docs/features/<slug>` with it. If the repository has `AGENTS.md` files and the catalogue is
new, suggest `as:agent-docs` so the root `AGENTS.md` links it. If acceptance criteria were added or changed and
`docs/qa/` exists, suggest `as:qa-docs` to bring the journeys in line. When the criteria involve calculations or
thresholds, suggest `as:explain docs/features/<slug>` to check the logic with the business on worked examples. If
the clarification showed several capabilities that are each worth shipping alone, say once that
`as:roadmap` fits better (stages, one feature each). Do not commit.

## Legacy

A folder of older documentation (argument outside `docs/features/`) is mapped before steps 2–4 run for the
features it yields.

1. List its files (`git ls-files <folder>`, else `ls -R`) with type, size and the date of the last commit.
2. Read them — read-only subagents in batches for more than ~10 files, each returning per file: what it is, which
   capability it belongs to, date, and whether it describes module behaviour or a feature's why and scope.
3. Propose the mapping table of [references/feature-format.md](references/feature-format.md#legacy-material): file →
   feature (existing or new slug) → role → new file name. Uncertain rows become questions.
4. After approval, run steps 2–4 per feature, then move the approved files in step 5. `module contract` files are
   listed in the summary for `as:spec-docs`; the emptied legacy folder is removed only with consent.
