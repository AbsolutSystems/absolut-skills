# Mockups

A mockup shows a screen of a user flow so the user can react to something they see instead of a description, and
choose between versions of it. Used by `as:feature` (the screens of a feature's flows) and `as:roadmap` (the frame
of a new application). Mockups are static HTML next to the page; they are never application code.

## When

Ask the user whether to show mockups, with a recommendation:

- **yes** — a new screen, a screen that changes its layout, a flow the user hesitates about, or a real choice
  between ways to build it;
- **no** — a small change to an existing screen (a field, a column, a message), or no user interface.

The user's yes is the approval to write files under `mockups/`; nothing else is written before the skill's own
approval gate. A run the user cancels there → ask whether to keep or delete the mockups.

## Fidelity

| Project | Fidelity | Built from |
|---------|----------|------------|
| Has screens already | high — it looks like the next screen of this application | the application's own styles and the markup of its nearest existing screen |
| No look yet (a new application) | low — greyscale, system font, boxes and real text | nothing; layout and content only |

High fidelity:

- Start from the nearest existing screen. With the application running and a browser tool available (host mapping),
  open that screen, take a screenshot and read its structure and computed styles; otherwise read its source: design
  tokens, theme, the stylesheet, the markup its components render.
- Use only what the project has: its colours, spacing, typography and components. A version that needs a component
  the project does not have marks it in the tab's `note` ("needs a new component: date-range picker") — it is a cost
  `as:tech-lead` must see.
- Real content, not lorem ipsum: names, amounts and messages as the criteria and the flow say them, in the
  application's language.
- Say in the summary where the mockup differs from the application (styles only approximated, an icon set missing).

Low fidelity: no colours, no brand, no invented visual style. When the user wants to settle the look of a new
application, show versions of one key screen in different visual directions; the chosen one is recorded as a
decision and later mockups follow it.

## Versions

- Show 2–3 versions only where there is a real choice (edit in the table, in a side panel or on its own screen);
  one version otherwise. Versions differ in layout and interaction, not in decoration.
- Each version is a whole page in its own file. The user switches between them with the tabs of the viewer — one
  version fills the page at a time; never place versions side by side on one page.
- Every version's tab has a `note`: its trade-off in one sentence. Name the one you recommend and why when you ask.
- The user picks one, or a mix ("C, with the button from A") → build the mix as the final file.
- After the choice: the chosen file is renamed without its version letter, the rejected files are deleted,
  `tabs.js` lists what is left, and the choice becomes a decision `D<n>` on the page with its reason and what was
  rejected ("side panel, not a separate screen — the list stays visible; versions A and B rejected").

## Files

```text
docs/features/<slug>/mockups/        # docs/roadmap/<slug>/mockups/ for a roadmap
  index.html                         # the viewer — copied, never edited
  tabs.js                            # the tabs of the viewer
  uf1-1-order-details.html           # one file per screen: uf<flow>-<step>-<screen>
  uf1-2-confirm-a.html               # versions of one screen, while the choice is open
  uf1-2-confirm-b.html
  uf1-2-confirm-error-shipped.html   # a state of a screen: …-empty, …-error-<what>, …-no-access
```

- Copy the viewer with a shell copy from this skill's directory: `cp <feature skill directory>/assets/mockups.html
  <page directory>/mockups/index.html` ([../assets/mockups.html](../assets/mockups.html)). Do not retype or edit it.
- Write `tabs.js` — the tabs in the order of the flow, versions of one screen next to each other:

  ```js
  window.MOCKUPS = {
    title: "Partial order cancellation",
    tabs: [
      { id: "details", label: "1 Order details", file: "uf1-1-order-details.html" },
      { id: "confirm-a", label: "2 Confirm — version A", file: "uf1-2-confirm-a.html", note: "Dialog over the order. Fewest clicks; the refund amount is hidden until it opens." },
      { id: "confirm-b", label: "2 Confirm — version B", file: "uf1-2-confirm-b.html", note: "Side panel. The order stays visible. Recommended." },
      { id: "shipped", label: "2 Error: already shipped", file: "uf1-2-confirm-error-shipped.html" },
    ],
  };
  ```

- Every mockup file is self-contained: styles in a `<style>` block, no build step, no script, no request to the
  network or to the application (a web font the application itself loads is the one exception). It opens from the
  file system.
- A screen file shows one state. Mock the states the flow names (empty, error, no access) for the screens where they
  change what the user sees; a state that is one message in the same layout needs no file of its own.
- Tell the user the path of `mockups/index.html` to open; where the host mapping offers a browser tool the user can
  see, open it for them.
- Narrow viewport: when the flow is used on phones, the mockup is responsive — the user checks it by resizing the
  window; no separate phone files.

## What a mockup is

- **An illustration, not the contract.** Acceptance criteria and user flows are the truth; where a mockup and the
  text differ, the text wins and the mockup is corrected or deleted. A decision the mockup made visible is written
  down as text (a flow step, a state, a decision) — nothing is agreed only in a picture.
- **A pattern for layout and content, not a source of code.** `as:implement` builds the screen from the project's
  components; it never copies a mockup's markup or styles.
- **A record, not a living document.** Mockups are changed while the feature is discussed and its phases are
  planned. After a phase ships its screens, the application is the truth and the mockups are left as they were.

## Links from the page

- A flow's meta line ends with `· **Mockups:** [viewer](mockups/index.html)`; a step may link its screen
  (`1. [Order details](mockups/uf1-1-order-details.html) — …`).
- Every file under `mockups/` except `index.html` and `tabs.js` is in `tabs.js`; files that are not are deleted.
