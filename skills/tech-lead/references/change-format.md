# Change proposal format

A change proposal describes a planned change to the contract before it is implemented: why, what was decided, and
which scenarios will be added, changed or removed. Module pages in `docs/spec/` keep describing the current behaviour
until `as:finish` merges the proposal after implementation and moves it to `docs/spec/changes/archive/`, where it
remains as the decision record.

## Files

```text
docs/spec/changes/<slug>.html                    # open proposal (slug: short kebab-case title)
docs/spec/changes/archive/<YYYY-MM-DD>-<slug>.html  # merged by as:finish; data-status="implemented" or "dropped"
```

Same rules as spec pages ([../../spec-docs/references/html-format.md](../../spec-docs/references/html-format.md)):
content only, one stylesheet (`../spec.css`; `../../spec.css` in `archive/`), only the listed vocabulary.

## IDs

- **Added** scenarios reserve the next free number of the module's prefix, counting IDs on the module page **and** in
  every open proposal. Added requirements likewise (`<PREFIX>-R<n>`).
- **Changed** and **removed** scenarios use their existing ID.
- A new module gets a new prefix, unique across the spec and open proposals.

## Skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="generator" content="as:tech-lead">
  <title>Change: Partial order cancellation</title>
  <link rel="stylesheet" href="../spec.css">
</head>
<body data-status="open">
  <nav class="crumbs"><a href="../index.html">System</a> › Changes › Partial order cancellation</nav>
  <header>
    <h1>Partial order cancellation</h1>
    <p class="lead">Customers can cancel single items of a placed order until it ships.</p>
    <dl class="meta">
      <dt>Status</dt><dd>open</dd>
      <dt>Proposed</dt><dd>2026-10-19, commit <code>a1b2c3d</code></dd>
      <dt>Modules</dt><dd><a href="../backend/orders.html">Orders</a>, <a href="../backend/billing.html">Billing</a></dd>
    </dl>
  </header>
  <main>
    <section id="why">
      <h2>Why</h2>
      <p>Support handles ~40 requests a week to remove one item; today the whole order must be cancelled.</p>
    </section>
    <section id="scope">
      <h2>Scope</h2>
      <ul>
        <li>In: cancel one or more items before shipping; refund the item amount.</li>
        <li>Out: cancelling after shipping (returns flow), partial quantity of one item.</li>
      </ul>
    </section>
    <section id="decision">
      <h2>Decision</h2>
      <table>
        <thead><tr><th>Option</th><th>Summary</th><th>Effort</th><th>Main risk</th></tr></thead>
        <tbody>
          <tr><td>A — extend <code>cancelOrder</code></td><td>Optional item list on the existing operation</td><td>S</td><td>Ambiguous semantics for empty list</td></tr>
          <tr><td><strong>B — new <code>cancelItems</code></strong></td><td>Separate operation, emits <code>OrderItemsCancelled</code></td><td>M</td><td>Billing must handle a new event</td></tr>
        </tbody>
      </table>
      <p><strong>Chosen: B.</strong> Keeps <code>cancelOrder</code> semantics intact for existing callers; the new event lets Billing refund without querying Orders.</p>
    </section>
    <section id="scenarios">
      <h2>Scenarios</h2>
      <article class="req" id="ORD-R4" data-change="added">
        <h3>ORD-R4 — Cancel items</h3>
        <p class="shall">The module SHALL cancel selected items of an order that has not shipped.</p>
        <section class="scenario" id="ORD-014" data-kind="happy" data-change="added">
          <h4>ORD-014 — Cancel one item before shipping</h4>
          <dl class="gwt">
            <dt>Given</dt><dd>a placed order with two items, not shipped</dd>
            <dt>When</dt><dd>the customer cancels one item</dd>
            <dt>Then</dt><dd>the item is cancelled and <code>OrderItemsCancelled</code> is emitted with its amount</dd>
          </dl>
        </section>
        <section class="scenario" id="ORD-015" data-kind="error" data-change="added">
          <h4>ORD-015 — Order already shipped</h4>
          <dl class="gwt">
            <dt>Given</dt><dd>a shipped order</dd>
            <dt>When</dt><dd>the customer cancels an item</dd>
            <dt>Then</dt><dd>the request is rejected with <code>ALREADY_SHIPPED</code></dd>
          </dl>
        </section>
      </article>
      <section class="scenario" id="ORD-004" data-kind="happy" data-change="changed">
        <h4>ORD-004 — Order total (changed)</h4>
        <dl class="gwt">
          <dt>Given</dt><dd>an order with cancelled items</dd>
          <dt>When</dt><dd>its total is read</dd>
          <dt>Then</dt><dd>cancelled items are excluded (was: all items)</dd>
        </dl>
      </section>
    </section>
    <section id="questions">
      <h2>Open questions</h2>
      <aside class="note">Should cancelling the last item cancel the whole order? Assumed yes; confirm with product.</aside>
    </section>
  </main>
  <footer><a href="../index.html">← System</a></footer>
</body>
</html>
```

- `data-change="added|changed|removed"` on requirements and scenarios. A changed scenario states the new behaviour and
  says what it was in one parenthesis; a removed one keeps its last text.
- Scenarios of different modules are grouped under an `<h3>` per module when the change touches several.
- The body's `data-status` is `open`, then `implemented` or `dropped` when archived; `as:finish` updates it and the
  Status entry in `meta`.
