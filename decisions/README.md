# Architecture decision records

Each record states the context, the decision and its consequences, in the form Michael Nygard proposed. Records are
never edited after acceptance except to mark them superseded or amended; a changed decision gets a new record.

| ADR | Decision | Status |
|---|---|---|
| [001](001-a-git-repository-holding-an-okf-v02-bundle-is-the-system-of.md) | A Git repository holding an OKF v0.2 bundle is the system of record | accepted, October 17, 2026 |
| [002](002-llm-wiki-v2-is-the-engine-in-crow-mode.md) | LLM-Wiki-V2 is the engine, in CROW mode | accepted, October 17, 2026 |
| [003](003-top-level-folders-are-themes-kind-is-frontmatter.md) | Top-level folders are themes; kind is frontmatter | accepted, October 17, 2026 |
| [004](004-no-automated-commits-to-main-each-merge-publishes-a-release.md) | No automated commits to main; each merge publishes a release | accepted, October 17, 2026 |
| [005](005-a-github-app-authors-automated-pull-requests-and-stamp-commi.md) | A GitHub App authors automated pull requests and stamp commits | accepted, October 17, 2026 |
| [006](006-verification-is-the-owner's-approval.md) | Verification is the owner's approval | accepted, October 17, 2026 |
| [007](007-date-rule-for-a-living-wiki.md) | Date rule for a living wiki | accepted, October 17, 2026 |
| [008](008-own-material-in-full-third-party-material-as-notes-and-excer.md) | Own material in full; third-party material as notes and excerpts | accepted, October 17, 2026 |
| [009](009-deterministic-graph-backbone-semantica-behind-an-adapter.md) | Deterministic graph backbone; Semantica behind an adapter | accepted, October 17, 2026 |
| [010](010-python-static-site-and-a-dependency-free-explorer-instead-of.md) | Python static site and a dependency-free explorer instead of Quartz and Sigma.js | superseded by ADR 014 on October 17, 2026 (Muthu chose Quartz and Sigma.js) |
| [011](011-no-change-to-muthuborg.md) | No change to muthub.org | accepted, October 17, 2026; amended by ADR 015 (October 18, 2026) |
| [012](012-public-knowledge-only.md) | Public knowledge only | accepted, October 17, 2026 |
| [013](013-a-local-classifier-decides-the-claude-api-writes.md) | A local classifier decides; the Claude API writes | accepted, October 17, 2026 |
| [014](014-quartz-5-and-sigmajs-4-as-designed.md) | Quartz 5 for the site and Sigma.js 4 for the graph explorer, as designed | accepted, October 17, 2026. Supersedes ADR 010. |
| [015](015-muthub-org-links-to-the-wiki-and-reads-its-counts-without-depending-on-it.md) | muthub.org links to the wiki and reads its counts, without depending on it | accepted, October 18, 2026 (amends ADR 011) |
| [016](016-semantic-layer-entity-resolution-and-ontology-typed-relations.md) | Semantic layer: entity resolution and ontology-typed relations, promoted only by review | accepted, October 18, 2026 (extends ADR 009) |

The site repository's own decisions are in [knowledge-foundation-site/docs/decisions](https://github.com/muthub-ai/knowledge-foundation-site/tree/main/docs/decisions); muthub.org's are in [muthu-v0-portfolio-website/docs/decisions](https://github.com/muthub-ai/muthu-v0-portfolio-website/tree/main/docs/decisions).
