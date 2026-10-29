# QA analysis brief

One read-only subagent per web front end, from `as:qa-docs` step 2. Fill the placeholders and pass verbatim:

```text
You are mapping one web front end so an agent can check it in a browser the way a user does.
Read-only: do not modify files, do not start the application.

Front end: {directory}
Area: {area or route prefix, or "whole app"}
Feature criteria: {list of <slug>/AC<n> with their one-line text, or "none"}
Current docs/qa: {index.md and journeys.md content, or "none"}
AGENTS.md content: {content or "none"}

Read the router and the screens, the auth and permission checks, forms and their validation, layout and breakpoints,
error and empty states, translations, the start and seed commands and the environment configuration. Cite an
evidence path for every claim. Do not invent behaviour; mark guesses as questions.

Return exactly these sections:
1. Start — commands to start the app and its dependencies locally, the local URL and port, seed or reset commands,
   environments named in the repository (URL, kind); evidence paths.
2. Screens — route, screen name, which roles may open it, main actions on it; evidence path.
3. Roles — each role, how it is assigned, which screens or actions it is denied; evidence path.
4. Flows — paths a user takes across several screens or features (sign-up, the main business flow, checkout,
   administration), each as intent-level steps and the observable outcome at the end; which feature criteria
   each crosses. Mark the ones the code treats as critical (payments, data loss, permissions).
5. App-wide rules — what holds on every screen: breakpoints and supported viewports, empty, error and loading state
   components, error boundaries, languages; evidence path.
6. Drift — for each journey, checkpoint, rule or environment in the current docs/qa: still true, or what changed
   (route, control, role, command), with evidence. "none" when there is no docs/qa.
7. Not checkable in a browser — feature criteria whose outcome a user cannot see on a screen (background jobs,
   e-mails, exports), with the reason.
8. Open questions — accounts, data, external services (payments, e-mail) and anything else the code cannot tell;
   propose likely answers as options.
```
