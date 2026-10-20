# HTML format

Health pages carry content only. All styling lives in `docs/health/health.css`, which targets the elements and classes
listed here — use nothing else, so every page renders consistently and stays cheap to read.

## Rules

- HTML5, UTF-8, `<html lang="en|pl">` matching the report language.
- Exactly one stylesheet: `<link rel="stylesheet" href="health.css">`.
- Forbidden: `<style>`, `style="…"`, `<script>`, `<svg>`, `<img>` with data URIs, `<font>`, presentational attributes
  (`align`, `bgcolor`, `width`), classes not listed below.
- Indent with 2 spaces; one block element per line; no comments except the generated marker in `<head>`.
- Links are relative; links to spec pages point to `../spec/<…>.md`.
- Escape `<`, `>`, `&` in text; put code identifiers, paths, endpoints and values in `<code>`.

## Vocabulary

| Element / class | Use |
|-----------------|-----|
| `<nav class="crumbs">` | Breadcrumbs at the top |
| `<header>` + `<h1>` + `<p class="lead">` | Page title and 1–3 sentence summary |
| `<dl class="meta">` | Commit, scope, baseline |
| `<section id="…">` + `<h2>` | Top-level page sections |
| `<table>` with `<thead>` | Scorecards, findings lists, runs |
| `class="num"` on `<th>`/`<td>` | Numeric table cells (right-aligned) |
| `<article class="finding" id="H-001" data-severity="high\|medium\|low">` | One finding |
| `<span class="trend" data-dir="up\|down\|flat">` | Change against the previous run |
| `<span class="badge">` | Short label, e.g. finding category or effort |
| `<aside class="note">` | Caveat, e.g. what was not checked |
| `<footer>` | Back link to the parent page |
