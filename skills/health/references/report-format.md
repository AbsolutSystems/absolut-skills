# Report and snapshot format

Health pages follow [html-format.md](html-format.md) — content only, one stylesheet, only the listed vocabulary — and
link `health.css`. Report language follows the spec pages (`lang` in the marker on the first line of
`docs/spec/index.md`), else English.

## `docs/health/<YYYY-MM-DD>.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="generator" content="as:health">
  <title>Health 2026-10-19 — Shop</title>
  <link rel="stylesheet" href="health.css">
</head>
<body>
  <nav class="crumbs"><a href="index.html">Health</a> › 2026-10-19</nav>
  <header>
    <h1>Health — 2026-10-19</h1>
    <p class="lead">3 high, 7 medium, 12 low findings. Coverage up, one new cycle.</p>
    <dl class="meta">
      <dt>Commit</dt><dd><code>a1b2c3d</code></dd>
      <dt>Scope</dt><dd><code>.</code>, history since 12 months</dd>
      <dt>Baseline</dt><dd><a href="2026-09-15.html">2026-09-15</a></dd>
      <dt>Tools</dt><dd>lizard (ephemeral), JaCoCo (configured), madge (ephemeral), git</dd>
      <dt>Excluded</dt><dd><code>frontend/src/generated</code>, i18n bundles</dd>
    </dl>
  </header>
  <main>
    <section id="modules">
      <h2>Modules</h2>
      <table>
        <thead><tr><th>Module</th><th class="num">Complexity (max)</th><th class="num">Churn</th><th class="num">Coverage</th><th class="num">Cycles</th><th class="num">Findings</th></tr></thead>
        <tbody>
          <tr><td><a href="../spec/backend/orders.md">orders</a></td><td class="num">34</td><td class="num">58</td><td class="num">61% <span class="trend" data-dir="up">+6</span></td><td class="num">1</td><td class="num">4</td></tr>
        </tbody>
      </table>
    </section>
    <section id="findings">
      <h2>Findings</h2>
      <article class="finding" id="H-001" data-severity="high">
        <h3>H-001 — <code>OrderService.java</code> is a hotspot with 22% coverage</h3>
        <dl class="meta">
          <dt>Category</dt><dd><span class="badge">add-tests</span></dd>
          <dt>Effort</dt><dd>M</dd>
          <dt>Evidence</dt><dd>58 commits, max complexity 34, coverage 22% — <code>backend/src/.../OrderService.java</code></dd>
          <dt>Since baseline</dt><dd>persists (was H-003)</dd>
        </dl>
        <p>Cover cancellation and partial-payment paths through the orders facade.</p>
      </article>
    </section>
    <section id="resolved">
      <h2>Resolved since baseline</h2>
      <ul><li>H-002 (2026-09-15) — cycle <code>billing ↔ orders</code> removed.</li></ul>
    </section>
    <section id="coupling">
      <h2>Coupling</h2>
      <p>Cycles, fan-in/fan-out leaders, and cross-module change coupling, as tables.</p>
    </section>
    <section id="notes">
      <h2>Not checked</h2>
      <aside class="note">Mutation testing not run. Dependency scan failed: osv-scanner image unavailable.</aside>
    </section>
  </main>
  <footer><a href="index.html">← All runs</a></footer>
</body>
</html>
```

`span.trend` shows the direction of the value, not good/bad — the text says which is better.

## `docs/health/index.html`

Header "Health", then `<section id="runs">` with a table: date (link), commit, high/medium/low counts, coverage,
cycles, with `trend` spans against the previous run. Newest first. Footer link to `../spec/index.md` if it exists.

## `docs/health/<YYYY-MM-DD>.json`

```json
{
  "date": "2026-10-19",
  "commit": "a1b2c3d",
  "scope": ".",
  "since": "12 months",
  "tools": [{"name": "lizard", "source": "ephemeral", "status": "ok"}],
  "excluded": ["frontend/src/generated"],
  "modules": {
    "orders": {
      "path": "backend/src/main/java/com/acme/shop/orders",
      "loc": 4200,
      "complexityMax": 34,
      "complexitySum": 610,
      "churn": 58,
      "coverageLine": 0.61,
      "coverageBranch": 0.48,
      "cycles": 1,
      "fanIn": 5,
      "fanOut": 3,
      "deadCode": 2,
      "duplicationPct": 3.1,
      "vulnerableDeps": 0
    }
  },
  "findings": [
    {
      "id": "H-001",
      "category": "add-tests",
      "severity": "high",
      "effort": "M",
      "module": "orders",
      "files": ["backend/src/main/java/com/acme/shop/orders/OrderService.java"],
      "key": "add-tests:backend/src/main/java/com/acme/shop/orders/OrderService.java",
      "summary": "Hotspot with 22% coverage"
    }
  ]
}
```

Use `null` for metrics that were not measured, never `0`. `key` (category + primary file or module pair) identifies the
same finding across runs: matching keys mean "persists", a baseline key missing now means "resolved".
