<!-- as:tech-lead lang=en -->
Changes › Readable journey IDs

# Readable journey IDs

QA journeys are identified by a kebab-case slug (`checkout-guest`) instead of `J1`, `J2`, … — readable in a run
report, an issue or a commit without opening `journeys.md`, still a stable anchor and selectable from the command line.

**Status:** open · **Proposed:** 2026-11-18, commit `d16cb8a` (ships with the uncommitted 1.19.0 changes) · **Modules:** [qa-docs](../../../skills/qa-docs/SKILL.md), [qa](../../../skills/qa/SKILL.md), [help](../../../skills/help/SKILL.md)

## Why

`J2-3 FAIL` in a report, an issue file or a `deliver` log says nothing until the reader opens `docs/qa/journeys.md`.
The ID is the only thing that travels everywhere — checkpoint IDs, screenshot names, report targets, issue evidence,
the `as:qa J2 J5` argument — so it should carry the meaning itself.

## Scope

- **In:** journey IDs and their checkpoint IDs in the `docs/qa/` format, `qa-docs` (new IDs, verification, an opt-in
  migration of legacy `J<n>`), `qa` (selection by ID, unknown ID), examples in briefs, host mappings and docs.
- **Out:** app-wide rule IDs `R<n>` (used only inside `index.md` and run reports next to their text); acceptance
  criterion checkpoints `<slug>/AC<n>` (already readable); finding IDs `F<n>` of exploratory runs (local to one report);
  any logic change in `qa_report.py` (it treats IDs as opaque strings).

## Decision

| Option | Summary | Effort | Main risk |
|--------|---------|--------|-----------|
| **A — slug as the ID** | heading `Guest checkout` anchored `checkout-guest`, checkpoints `checkout-guest-<m>`, `as:qa checkout-guest refund-partial` | S | A slug colliding with a target word (`journeys`, `branch`, `explore`); the title may drift from the slug after edits |
| B — keep `J<n>`, always show the title | `J2 (Guest checkout)` in reports, issues, `deliver` logs and commits | S | A rule repeated in many places no validator checks; `J2` in history stays opaque |
| C — do nothing | — | 0 | The problem stays |

**Chosen: A.** The ID itself carries the meaning everywhere it travels; no extra rule for every surface that quotes it.
The slug is given once, when the journey is written, and never changes: renaming a journey changes only its title, so
the anchor, the screenshots and every report or issue that names it stay valid. A journey whose meaning changes is a
new journey, and the old one is marked removed, as today.

**Legacy `J<n>`: both formats accepted, migration opt-in.** Existing `journeys.md` files keep working unchanged. On a
later run `qa-docs` suggests a slug for each legacy journey; an applied journey keeps its old anchor and a
`**Was:** J<n>` line, so links in old run reports and issues still resolve and `as:qa J2` still selects it. A forced
migration was rejected: it would break the references in committed run reports and issues.

### ID rules

- Kebab-case `[a-z][a-z0-9-]*`, two to four words, naming the path from the user's side (`checkout-guest`,
  `admin-blocks-customer`).
- Not a target word of `as:qa` (`journeys`, `branch`, `explore`), not of the form `j<n>`, not ending in `-<digits>`
  (checkpoint IDs append `-<m>`).
- Unique across all journeys of the file, removed ones and `**Was:**` IDs included; never reused.
- Checkpoints: `<journey ID>-<m>`, numbered from 1 within the journey, never renumbered or reused.

## Scenarios

**Module:** qa-docs

### Changed scenarios

#### <a id="QAD-006"></a>QAD-006 — Stable journey IDs

**Kind:** ⚠️ edge · **Change:** ✏️ changed

- **Given** journeys with slug IDs (or legacy `J<n>`)
- **When** a journey is added, renamed or removed
- **Then** a new journey gets a slug ID by the ID rules; renaming changes only the title; no ID or checkpoint ID is
  ever changed, renumbered or reused; a removed journey keeps its text with the removed status (was: IDs `J1…Jn`
  taken in order)

### <a id="QAD-R1"></a>QAD-R1 — Maintain what QA checks

**Change:** ✏️ changed (scenarios added below)

#### <a id="QAD-008"></a>QAD-008 — Slug that breaks the rules

**Kind:** ⚠️ edge · **Change:** 🆕 added

- **Given** a new journey whose natural slug is a target word (`journeys`, `branch`, `explore`), has the form
  `j<n>`, ends in `-<digits>`, or is already taken (also by a removed journey or a `**Was:**` ID)
- **When** `qa-docs` writes it
- **Then** it picks another slug that follows the rules, and the verification step reports any ID used twice

#### <a id="QAD-009"></a>QAD-009 — Legacy `J<n>` journeys

**Kind:** ⚠️ edge · **Change:** 🆕 added

- **Given** a `journeys.md` with `J<n>` IDs
- **When** `qa-docs` runs on the existing `docs/qa/`
- **Then** it suggests, as a group "Legacy IDs", a slug for each legacy journey; an applied one gets the slug as its
  ID, keeps its old `J<n>` as a second anchor and a `**Was:** J<n>` line, and its checkpoints become
  `<slug>-<m>` with the same `<m>`; journeys not applied keep `J<n>`, which stays valid, and new journeys get slugs

---

**Module:** qa

### Changed scenarios

#### <a id="QA-001"></a>QA-001 — Targets

**Kind:** ✅ happy · **Change:** ✏️ changed

- **Given** `docs/qa/index.md`
- **When** the user runs `qa docs/features/<slug>`, `qa journeys`, `qa <journey ID>…`, `qa branch` or
  `qa explore <area>`
- **Then** it runs that feature's AC, all journeys, the named journeys (by slug, legacy `J<n>`, or a former ID from
  `**Was:**`), the AC and journeys touched by the branch's changes, or an exploratory session of the area (was:
  `qa J<n>` only)

### <a id="QA-R1"></a>QA-R1 — Verify the app in a browser

**Change:** ✏️ changed (scenario added below)

#### <a id="QA-013"></a>QA-013 — Unknown journey ID

**Kind:** ❌ error · **Change:** 🆕 added

- **Given** `docs/qa/journeys.md` without a journey `checkout-gest` (current or `**Was:**`)
- **When** the user runs `qa checkout-gest`
- **Then** it runs nothing, lists the active journey IDs with their titles, and asks which were meant

## Plan

- [x] **1. Format** — `skills/qa-docs/references/qa-format.md`: journey example with a slug, the ID rules,
  `**Was:**` and the second anchor for migrated journeys, legacy `J<n>` accepted; file tree and screenshot names,
  run report target (`<journey ID>`), report and `run.json` examples with slug IDs.
- [x] **2. `qa-docs`** — `skills/qa-docs/SKILL.md`: `description` (no "J1…Jn"), step 3 "Legacy IDs" suggestion
  ([QAD-009](#QAD-009)), step 5 new IDs by the rules ([QAD-006](#QAD-006), [QAD-008](#QAD-008)), step 6 uniqueness
  check including removed and `**Was:**` IDs.
- [x] **3. `qa`** — `skills/qa/SKILL.md`: `argument-hint` and Arguments (`<journey ID>…`), step 2 Select resolves a
  slug, `J<n>` or `**Was:**` ID and stops on an unknown one ([QA-001](#QA-001), [QA-013](#QA-013));
  `skills/qa/references/briefs.md` examples. Check `skills/deliver/references/autopilot.md` (QA stage) still needs no
  change — it names no journey ID today.
- [x] **4. Evidence page tests** — `tests/test_scripts.py`: fixture with a slug journey; a test that
  `checkout-guest-2` and legacy `J1-2` both get their anchors and summary links. No change to `qa_report.py` logic
  (docstring only if it quotes `J<n>`).
- [x] **5. Docs and release** — example path in `references/claude-tools.md`; `README.md` (qa-docs/qa section,
  `/as:qa checkout-guest refund-partial`, argument table), `skills/help/SKILL.md`, the `qa-docs` and `qa` rows in
  `skills/README.md`, a bullet in the existing `CHANGELOG.md` 1.19.0 entry. Ships in 1.19.0 together with evidence
  by running: the version stays 1.19.0 in `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` and
  `package.json`.
- [x] **6. Checks** — `python3 tools/validate.py`, `uv run --with pytest pytest tests`, `claude plugin validate .`;
  `git grep -n 'J<n>\|J[0-9]' skills references README.md` shows only legacy mentions.

**Risks:** implemented on top of the uncommitted 1.19.0 changes in the same checkout, which touch
`README.md`, `CHANGELOG.md`, `skills/help/SKILL.md` and `skills/README.md` too — edit only the QA lines there and
commit nothing; 1.19.0 is committed by the user as one release. An agent may still invent `J<n>` for new journeys from habit — the
format's example and step 5 of `qa-docs` show only slugs, and step 6 flags a new `J<n>`.

**Verify:** in a scratch project with a legacy `journeys.md` (`J1`, `J2`), follow `qa-docs`: it offers "Legacy IDs";
apply one — its heading is anchored by the slug and by `J1`, with `**Was:** J1`; `as:qa J1` and `as:qa <slug>` select the
same journey; `as:qa checkout-gest` lists the IDs and runs nothing.

## Open questions

None. Settled with the user on 2026-11-18: option A, legacy `J<n>` accepted with an opt-in migration.

---
