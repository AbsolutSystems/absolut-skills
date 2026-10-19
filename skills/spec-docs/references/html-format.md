# HTML format

Pages carry content only. All styling lives in `docs/spec/spec.css`, which targets the elements and classes listed here —
use nothing else, so every page renders consistently and stays cheap to read.

## Rules

- HTML5, UTF-8, `<html lang="en|pl">` matching `--lang`.
- Exactly one stylesheet: `<link rel="stylesheet" href="spec.css">` (`../spec.css` one level down).
- Forbidden: `<style>`, `style="…"`, `<script>`, `<svg>`, `<img>` with data URIs, `<font>`, presentational attributes
  (`align`, `bgcolor`, `width`), classes not listed below.
- Indent with 2 spaces; one block element per line; no comments except the generated marker in `<head>`.
- Links between pages are relative. Link to a scenario with `module.html#ORD-003`.
- Escape `<`, `>`, `&` in text; put code identifiers, paths, endpoints and values in `<code>`.

## Vocabulary

| Element / class | Use |
|-----------------|-----|
| `<nav class="crumbs">` | Breadcrumbs at the top: system › app › module |
| `<header>` + `<h1>` + `<p class="lead">` | Page title and 1–3 sentence purpose |
| `<dl class="meta">` | Source path, generated-from commit, ID prefix, status |
| `<section id="…">` + `<h2>` | Top-level page sections (ids: `overview`, `contract`, `requirements`, `rules`, `dependencies`, `glossary`, `questions`, `modules`, `flows`, `actors`) |
| `<table>` with `<thead>` | Contracts, module lists, actor lists |
| `<article class="req" id="ORD-R1">` | One requirement; `<h3>` = `ORD-R1 — <short name>`, then `<p class="shall">` with the SHALL sentence |
| `<section class="scenario" id="ORD-003" data-kind="happy\|error\|edge">` | One scenario inside a requirement; `<h4>` = `ORD-003 — <short name>` |
| `data-status="removed"` | On a removed requirement or scenario; content kept, rendered struck through |
| `<dl class="gwt">` with `<dt>Given</dt><dd>…</dd>`, `When`, `Then` (`And` as extra `dt`) | Scenario steps. Translate the `dt` labels when `--lang pl`: Zakładając / Gdy / Wtedy / Oraz |
| `<ol class="flow">` | Numbered steps of a cross-module flow on system/app pages |
| `<ul class="cards">` + `<li>` with `<a>` and `<p>` | Grid of apps/modules on system/app pages |
| `<aside class="note">` | Open question or caveat |
| `<span class="badge">` | Short label, e.g. operation type (`command`, `query`, `event`, `endpoint`) |
| `<footer>` | Back link to the parent page |
| `data-change="added\|changed\|removed"` | Change proposals only (`docs/spec/changes/`, from `as:tech-lead`) on requirements and scenarios |
| `<article class="finding" id="H-001" data-severity="high\|medium\|low">` | Health reports only (`as:health`): one finding |
| `<span class="trend" data-dir="up\|down\|flat">` | Health reports only: change against the previous run |
| `class="num"` on `<th>`/`<td>` | Numeric table cells (right-aligned) |

## Scenario writing rules

- One requirement = one capability of the module ("The module SHALL reject orders without stock reservation").
- Every requirement has at least one `happy` scenario; add `error` scenarios for each rejection/failure the code
  actually handles (validation, not found, permission, conflict, downstream failure) and `edge` scenarios for limits,
  empty inputs, idempotency, concurrency, time boundaries.
- Given = state before; When = one call through the public contract; Then = observable result (return value, error,
  emitted event, persisted state visible through the contract). No internal method names.
- IDs: requirements `<PREFIX>-R<n>`, scenarios `<PREFIX>-<NNN>` (three digits, sequential per module, never reused).

## Skeleton: module page

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="generator" content="as:spec-docs">
  <title>Orders — Specification</title>
  <link rel="stylesheet" href="../spec.css">
</head>
<body>
  <nav class="crumbs"><a href="../index.html">System</a> › <a href="index.html">Shop backend</a> › Orders</nav>
  <header>
    <h1>Orders</h1>
    <p class="lead">Accepts customer orders, reserves stock and tracks each order until delivery.</p>
    <dl class="meta">
      <dt>Source</dt><dd><code>backend/src/main/java/com/acme/shop/orders</code></dd>
      <dt>Commit</dt><dd><code>a1b2c3d</code></dd>
      <dt>ID prefix</dt><dd><code>ORD</code></dd>
    </dl>
  </header>
  <main>
    <section id="contract">
      <h2>Contract</h2>
      <table>
        <thead><tr><th>Operation</th><th>Type</th><th>Input</th><th>Result</th></tr></thead>
        <tbody>
          <tr><td><code>placeOrder</code></td><td><span class="badge">command</span></td><td>customer, items</td><td>order id or rejection</td></tr>
          <tr><td><code>OrderPlaced</code></td><td><span class="badge">event</span></td><td>—</td><td>emitted after a successful placement</td></tr>
        </tbody>
      </table>
    </section>
    <section id="requirements">
      <h2>Requirements</h2>
      <article class="req" id="ORD-R1">
        <h3>ORD-R1 — Place an order</h3>
        <p class="shall">The module SHALL accept an order only when every item can be reserved.</p>
        <section class="scenario" id="ORD-001" data-kind="happy">
          <h4>ORD-001 — All items in stock</h4>
          <dl class="gwt">
            <dt>Given</dt><dd>every ordered item has enough stock</dd>
            <dt>When</dt><dd>the customer places the order</dd>
            <dt>Then</dt><dd>the order is created with status <code>PLACED</code></dd>
            <dt>And</dt><dd><code>OrderPlaced</code> is emitted</dd>
          </dl>
        </section>
        <section class="scenario" id="ORD-002" data-kind="error">
          <h4>ORD-002 — Item out of stock</h4>
          <dl class="gwt">
            <dt>Given</dt><dd>one ordered item has no stock</dd>
            <dt>When</dt><dd>the customer places the order</dd>
            <dt>Then</dt><dd>the order is rejected with <code>OUT_OF_STOCK</code> and nothing is reserved</dd>
          </dl>
        </section>
      </article>
    </section>
    <section id="rules">
      <h2>Business rules</h2>
      <ul><li>An order total is never negative.</li></ul>
    </section>
    <section id="dependencies">
      <h2>Dependencies</h2>
      <ul>
        <li>Uses: <a href="inventory.html">Inventory</a> — stock reservation.</li>
        <li>Used by: <a href="billing.html">Billing</a> — listens to <code>OrderPlaced</code>.</li>
      </ul>
    </section>
    <section id="glossary">
      <h2>Glossary</h2>
      <dl><dt>Reservation</dt><dd>Stock held for an order until it is paid or cancelled.</dd></dl>
    </section>
    <section id="questions">
      <h2>Open questions</h2>
      <aside class="note">What happens to reservations of orders never paid? No timeout exists in the code.</aside>
    </section>
  </main>
  <footer><a href="index.html">← Shop backend</a></footer>
</body>
</html>
```

## Skeleton: app page (`<app>/index.html`)

Same `<head>` (stylesheet `../spec.css`). Body: `crumbs`, `header` (`h1`, `lead`, `meta` with source path and commit),
then `<section id="modules">` with `<ul class="cards">` (one `li` per module: link + one-line responsibility),
`<section id="flows">` with one `<h3>` + `<ol class="flow">` per main cross-module flow (steps link to scenarios),
optional `rules`, `glossary`, `questions`, and a `footer` linking to `../index.html`.

## Skeleton: system page (`index.html`)

Stylesheet `spec.css`. Body: `header` (`h1` = product name, `lead` = what it does and for whom, `meta` with commit),
`<section id="actors">` (table: actor, what they do), `<section id="modules">` with `cards` for apps (monorepo) or
modules (single app), `<section id="flows">` for the main end-to-end flows, optional `glossary` and `questions`.
No `crumbs` or `footer`.
