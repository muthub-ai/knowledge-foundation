# ADR 010: Python static site and a dependency-free explorer instead of Quartz and Sigma.js

Status: superseded by ADR 014 on October 17, 2026 (Muthu chose Quartz and Sigma.js)

## Context

The build environment for this work had no access to npm, so Quartz 5 and Sigma.js could not be installed or tested. A site that cannot be tested end to end is not finished.

## Decision

`knowledge-foundation-site` renders the bundle with a small Python generator (markdown, Jinja2) and draws the graph on a 2D canvas with no third-party JavaScript.

## Consequences

Fully tested here (unit and browser tests). Exact control of provenance blocks, JSON-LD, Markdown twins and the site's look. Quartz or Sigma.js remain drop-in options later: both read the same bundle and graph.json. Supersedes the Quartz and Sigma.js choices in design v1.0.
