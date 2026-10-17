# ADR 014: Quartz 5 for the site and Sigma.js 4 for the graph explorer, as designed

Status: accepted, October 17, 2026. Supersedes ADR 010.

## Context

ADR 010 replaced Quartz and Sigma.js with a Python generator and a hand-written canvas explorer because the build
environment could not reach npm. Muthu asked for Quartz and Sigma.js, as in design v1.0.

## Decision

`knowledge-foundation-site` builds with **Quartz 5**, checked out at a pinned commit (`quartz.ref`) and configured as
Quartz's own default plus a short list of changes (`scripts/make_quartz_config.py`). Two small Python steps wrap it:
`kfsite stage` turns the OKF bundle into Quartz content (provenance callout, sources, site-path links) and `kfsite post`
adds what Quartz does not (JSON-LD, Markdown twins, llms.txt, the explorer). The graph explorer at `/graph/` is
**Sigma.js 4** over graphology, reading `graph.json`. Quartz's own graph component is turned off so there is one graph.

## Consequences

- The site is Quartz: its search, explorer, backlinks, popovers, tag pages, SPA navigation and RSS come for free, and
  upgrades are a pinned-commit bump.
- The knowledge repository is unchanged: the site still reads only the release bundle and graph.json (ADR 004).
- The Quartz build itself can only run where npm is reachable (GitHub Actions, Vercel, the Mac). The staging and
  finishing steps and the Sigma explorer are tested everywhere; the full Quartz build is tested in the site's CI.
