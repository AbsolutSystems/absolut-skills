# QA format

`docs/qa/` says how to check a web application the way a user uses it: where it runs, who logs in, which rules hold
on every screen, and which paths across features must work. `as:qa-docs` writes it; `as:qa` executes it in a browser
and writes the run reports. It never repeats what lives elsewhere: acceptance criteria stay on the feature pages
(`docs/features/<slug>/index.md`, [format](../../feature/references/feature-format.md)) and are executed from there;
module behaviour stays in `docs/spec/`.

## Files

```text
docs/qa/
  index.md                          # environments, accounts, roles, app-wide UI rules, links
  journeys.md                       # cross-feature paths J1…Jn
  runs/
    2026-10-29-journeys.md          # report of one run (target after the date)
    2026-10-29-journeys/            # screenshots of FAIL and OUTDATED checkpoints only
      J2-3-mobile.png               # <checkpoint>[-<viewport>].png, '/' in an ID becomes '-'
.qa/                                # working screenshots of every checkpoint — gitignored, never committed
```

Same rules as spec pages ([../../spec-docs/references/markdown-format.md](../../spec-docs/references/markdown-format.md)):
the constructs and readability rules listed there, marker `<!-- as:qa-docs lang=… -->` on the first line of
`index.md` and `journeys.md` (`<!-- as:qa lang=… -->` on run reports), relative links. Pages follow the spec language
(`lang` in the marker of `docs/spec/index.md`), else English; fixed values (results, status words) stay English.

## `index.md`

```markdown
<!-- as:qa-docs lang=en -->
# QA

How to check the shop in a browser. What each feature promises: [features](../features/index.md). Cross-feature
paths: [journeys](journeys.md). Last runs: [runs](runs/).

**Updated:** 2026-10-29, commit `a1b2c3d`

## Environments

| Name | URL | Kind | Start |
|------|-----|------|-------|
| local | http://localhost:5173 | local | `docker compose up -d && npm run dev` |
| staging | https://staging.shop.example | staging | deployed from `main` |

Production is never a QA target.

## Accounts and data

| Role | Login | Password | Data |
|------|-------|----------|------|
| customer | `QA_CUSTOMER_EMAIL` | `QA_CUSTOMER_PASSWORD` | `npm run seed:qa` — two products, one placed order |
| admin | `QA_ADMIN_EMAIL` | `QA_ADMIN_PASSWORD` | same seed |

## Roles

- **customer** — browses, orders, sees own orders; never sees `/admin`.
- **admin** — manages products and orders.

## App-wide rules

Checked on every screen of every run, in addition to the scenario's own checkpoints:

- **R1** — viewports: desktop 1440×900 and mobile 390×844; no horizontal scroll, nothing overlaps or is cut off.
- **R2** — every list has an empty state with a hint, not a blank area.
- **R3** — an error from the server shows a message in the page, never a raw error or a blank screen.
- **R4** — no console errors and no 5xx responses during a scenario.
```

- **Environments:** `Kind` is `local` or `staging`; `as:qa` opens only these URLs (and `localhost`) without asking.
  `Start` is the command or the note a person needs to bring the environment up.
- **Accounts:** never write secrets. Login and password columns hold environment variable names (or "ask"); the
  agent reads them from the environment at run time. `Data` says how the test data is created or reset.
- **App-wide rules** `R<n>`: short, observable, checkable from a screenshot, the console or the network. Numbered
  like journeys (below).

## `journeys.md`

A journey is a path a user takes across features or screens that no single acceptance criterion covers. Steps are
**intent**, not selectors: the executor finds the controls, so a changed markup does not break the journey.

```markdown
<!-- as:qa-docs lang=en -->
[QA](index.md) › Journeys

# Journeys

### <a id="J1"></a>J1 — First order

**Role:** customer · **Viewports:** desktop, mobile · **Crosses:** [Cart AC1](../features/cart/index.md#AC1), [Checkout AC2](../features/checkout/index.md#AC2)

**Given:** a logged-out customer, the QA seed loaded.

1. Open the shop and log in.
2. Add the cheapest product to the cart.
3. Check out with the test card.

**Checkpoints:**

- **J1-1** (after step 1) — the header shows the customer's name.
- **J1-2** (after step 2) — the cart badge shows 1 and the cart lists the product with its price.
- **J1-3** (after step 3) — a confirmation page with an order number; the order appears in "My orders".
```

- `J<n>` and checkpoint IDs `J<n>-<m>` are never renumbered or reused. A removed journey keeps its text with
  `**Status:** 🗑️ removed` after the meta line and a struck-through heading (`### <a id="J4"></a>~~J4 — …~~`).
- A checkpoint names an outcome a person can see (text, state, count, page), so a judge can decide it from a
  screenshot. "Works correctly" is not a checkpoint.
- `**Crosses:**` links the acceptance criteria the journey touches (none → leave the field out).

## Acceptance criteria as scenarios

`as:qa` runs a feature's criteria straight from its page: the criterion is the expected outcome, the scenarios in
`**Realised by:**` give the details (inputs, errors). Its checkpoint ID is the feature and criterion,
`<slug>/AC<n>` (in file names `<slug>-AC<n>`). A criterion with no outcome a person can observe in the browser (a background job, an e-mail) is
reported `BLOCKED` with the reason; `as:qa-docs` suggests a journey or a sharper criterion for it.

## Run report

`docs/qa/runs/<YYYY-MM-DD>-<target>.md`, target in kebab-case (`journeys`, `j3`, `branch-qa-skills`,
`feature-cart`, `explore-checkout`); another run of the same target on the same day takes the next free suffix (`-2`, `-3`, …). Every run writes
a report, also one that selected nothing (it says so) — `as:deliver` reads the report its QA stage wrote.

```markdown
<!-- as:qa lang=en -->
[QA](../index.md) › Runs › 2026-10-29 journeys

# QA run: journeys

**Target:** journeys · **URL:** http://localhost:5173 · **Commit:** `a1b2c3d` · **Host:** Claude Code · **Judge:** independent

**Result:** ❌ 1 FAIL · 1 OUTDATED · 5 PASS · 0 BLOCKED

| Checkpoint | Result | Evidence |
|------------|--------|----------|
| J1-1 | PASS | header shows "Anna" |
| J1-2 | FAIL | badge shows 0 after adding — [screenshot](2026-10-29-journeys/J1-2.png); `POST /api/cart` 500 |
| J2-1 | OUTDATED | "Wishlist" moved to the account menu (intended, commit `b2c3d4e`) — [screenshot](2026-10-29-journeys/J2-1.png) |

## App-wide rules

- R1 — FAIL on mobile: checkout button cut off — [screenshot](2026-10-29-journeys/J1-3-mobile.png).

## Findings

Exploratory runs only: each with steps to reproduce, expected and actual, and evidence.

## Issues

Saved: `p2-cart-add-returns-500` (J1-2). Suggested for `as:qa-docs`: J2-1.
```

- Results: `PASS`, `FAIL` (the app breaks an expected outcome or an app-wide rule), `OUTDATED` (the journey no longer
  matches an intended change — see below), `BLOCKED` (could not be checked: missing data, an unreachable step, an
  outcome not visible in the browser; the reason in Evidence).
- **Feature criteria win.** A mismatch with a feature's acceptance criterion is always a `FAIL`. A journey step that
  disagrees with a change made on purpose (a proposal, a feature decision, a commit that says so) is `OUTDATED`.
  When the evidence does not tell which, it is a `FAIL` with the doubt in Evidence.
- `**Judge:**` is `independent` (a subagent judged without the executor's narrative) or `same agent` (no subagents).
- Only the screenshots of `FAIL` and `OUTDATED` checkpoints are moved next to the report; the rest stay in `.qa/`.
  Issues link the report, not `.qa/`.

## Ownership

`as:qa-docs` writes `index.md` and `journeys.md`. `as:qa` writes `runs/` and adds `.qa/` to `.gitignore` (with
consent). Feature pages, the spec and `docs/issues/` keep their own owners; `as:qa` and `as:qa-docs` only offer
issues there.
