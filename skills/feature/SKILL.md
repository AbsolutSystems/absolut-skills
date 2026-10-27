---
name: feature
description: "Create and maintain a feature's living documentation in docs/features/<slug>/: why it exists, users and goals, non-goals, user-level acceptance criteria linked to the module scenarios that realise them, a roadmap of phases (one change proposal each), decisions and the sources they came from — client orders, PDFs, spreadsheets, pasted e-mails and meeting notes saved verbatim in sources/. Seeds a feature from an accepted estimate, records new sources and what they change, refreshes the roadmap and status, documents an existing feature from the code and archived proposals, and maps a legacy documentation folder into the format. Use only when the user explicitly invokes as:feature."
disable-model-invocation: true
argument-hint: "<description | file… | docs/features/<slug> | docs/estimates/<slug> | legacy folder> [--lang en|pl]"
---

# Feature

Keep one page per feature that a person or an agent reads first: why, what the user gets, where the work stands and
what comes next, with links to the module contracts, the change proposals and the sources. The page is a distillate;
sources are kept verbatim next to it. Do not write production code, module pages or change proposals here — phases are
planned with `as:tech-lead docs/features/<slug>`.

Host-specific mechanics (subagents, asking questions): [Claude Code](../../references/claude-tools.md), [Codex](../../references/codex-tools.md).
Format, sources and legacy rules: [references/feature-format.md](references/feature-format.md).

Arguments (`$ARGUMENTS` in Claude Code, plain text after the mention in Codex):

- `<description>` — a new feature in the user's words; files (a PDF order, a spreadsheet, notes) and text pasted in
  the same message (an e-mail, agreed points) are its first sources.
- `docs/features/<slug>` — update an existing feature: with new sources (files or pasted text) record them and what
  they change; without, refresh the roadmap and status and ask what changed.
- `docs/estimates/<slug>` — seed a feature from an estimate (written by `as:estimate`).
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
- From an estimate: requirements `R1…Rn` become acceptance criteria candidates, its blocks and steps the phase
  candidates, its open client questions the open questions; the estimate becomes a source by link.
- Retroactive: rebuild the criteria from the module scenarios already implemented (they are `**Realised by:**`) and
  the done phases from the archived proposals; ask about the why — the code does not know it.
- Update: compare each roadmap phase with its proposal (open in `changes/`, archived as `implemented` or `dropped`,
  or missing) and each `**Realised by:**` link with the module pages (removed or renumbered scenarios).

### 3. Clarify

Ask in small batches, most decisive first, with options from the sources and the code. Cover only what is still
unknown: the problem and who has it, how success is measured, non-goals, acceptance criteria the sources leave vague,
and the split into phases — each phase ends with working, tested value and fits one change proposal; the first phase
is the smallest one worth shipping. Contradictions between sources: ask which wins (it becomes a decision) or keep
it as an open question. Stop when the page can be written.

### 4. Report and gate

Show, briefly:

- new feature: purpose, acceptance criteria (one line each, with the source), phases with their AC, open questions,
  and the source files to save;
- update: what each new source changes — AC added, changed or removed, new decisions, contradictions — each with a
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
  text and every `AC`, `D`, `Q` ID; new ones take the next number; removed criteria get the removed status. Set
  `**Updated:**` to today and the current commit (`git rev-parse --short HEAD`) and rewrite the Now line.
- Add or update the feature's row in `docs/features/index.md` (create it from the skeleton when missing).
- Do not touch module pages, proposals, estimates or code. Never delete a page or a source without consent.

### 6. Verify

- Run `python3 <spec-docs skill directory>/scripts/spec_lint.py` from the repository root
  ([../spec-docs/scripts/spec_lint.py](../spec-docs/scripts/spec_lint.py); it checks `docs/features/` too) and fix
  every `ERROR` in the feature pages: links and anchors, roadmap phases against proposals, sources not listed. Without
  `python3`, check the same by hand.
- The top of the page fits about one screen; source text is linked, not copied.

### 7. Summary

Files written (page, catalogue, sources saved or moved), acceptance criteria and phases, open questions, and what was
not checked (sources not readable, areas not explored). Next: `as:tech-lead docs/features/<slug>` plans the next
`planned` phase as a change proposal (then `as:implement` and `as:finish`, which updates this roadmap); a new e-mail
or document → `as:feature docs/features/<slug>` with it. If the repository has `AGENTS.md` files and the catalogue is
new, suggest `as:agent-docs` so the root `AGENTS.md` links it. Do not commit.

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
