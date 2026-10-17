---
type: Source
title: 'Not another data lake: context needs curation, not collection'
resource: https://muthub.org/writing/not-another-data-lake.md
hash: sha256:13d7c4cdcee5671d59a08ecc000af13859d7bc3627732813625c4cea0cf97213
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2026-07-21'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Not another data lake: context needs curation, not collection

Published 2026-07-21. Part 3 of the Context Engineering series.

**If you build your context layer the way most enterprises built their data lakes, you will get a swamp, and this time agents will drink from it with complete confidence.** When leaders first hear the case for an enterprise context layer, the same question arrives within minutes: *so we copy everything into one place?* I understand the instinct. I have spent much of my career on data platforms, and I remember the same promise a decade ago. Put all the data in the lake and insight will follow.

It mostly did not. A recent fifteen-year retrospective, [What Went Wrong with Data Lakes?](https://arxiv.org/pdf/2606.08266), concludes that the root causes were largely organizational rather than technical. Teams ingested data without purpose, postponed schema and governance, and assumed that access meant usability. The paper's central idea is **governance debt**: the compounding cost of every deferred decision about ownership, metadata and quality, until the lake becomes a swamp.

The same pattern is already forming around enterprise AI, and the stakes are higher. A swamp of data slows analysts down. A swamp of context makes agents wrong at scale.

## Why bulk ingestion fails for context

1. **Volume is not knowledge.** A million chat messages and ten thousand tickets contain the answer to your question, alongside a hundred thousand wrong or outdated ones. Copying them does nothing to tell them apart.
2. **Copies go stale.** The moment you duplicate a source, you own the problem of keeping it in sync, and context about running systems changes daily.
3. **Copies multiply risk.** Every replica of sensitive operational data is another place to secure, classify, retain and audit. In a regulated enterprise that is a reason to say no.
4. **Context rot.** More raw material in an agent's window [degrades its recall](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). The goal is the smallest set of high-signal facts, not the largest pile.

## A curated overlay instead

The alternative is an overlay: a thin, curated layer of knowledge that sits *on top of* the systems of record instead of replacing them. Four design principles make the difference.

**Source systems stay authoritative.** The code repository remains the truth about code, the configuration database the truth about infrastructure, the ticketing system the truth about work. The context layer holds what those systems cannot: synthesis, relationships and rationale. Every claim links back to where it came from, so when the two disagree, everyone knows which one wins.

**Retrieval-first, not copy-first.** Store pointers and summaries, and fetch details just in time. This is how Anthropic describes effective agents: keep [lightweight identifiers](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) such as file paths and load data when it is needed. A context layer should behave the same way at enterprise scale.

**Ownership and governance from day one.** The data lake lesson fits in one sentence: decide ownership and metadata requirements first, because deferral is what turns a lake into a swamp. Every unit of context needs an owner, a classification and a review date before it is published. Zhamak Dehghani's [data mesh](https://martinfowler.com/articles/data-monolith-to-mesh.html) made the same argument for analytical data, that it should be a product owned by the domain that understands it. I would apply that thinking to context even more strictly, because an agent cannot tell a stale page from a current one unless someone has said so.

**Not a production dependency.** A context layer should make people and agents faster and safer, but production systems must never need it to run. If it goes down, you lose speed, not service. That boundary keeps the blast radius small and the architecture honest, and it makes the risk conversation far shorter.

Here is where I disagree with the common advice to start broad and prune later. Pruning almost never happens. Once a source is connected, someone's workflow depends on it, and removing it turns into a negotiation. Start narrow instead: one workflow, the handful of sources it truly needs, and an owner for each. Add a source only when a real question cannot be answered without it. This feels slow in the first quarter. By the third quarter it is faster, because the team is no longer arguing about which of four conflicting answers is right.

## Collection versus curation

- **A lake asks:** what can we ingest? **A context layer asks:** what does a person or agent need to know to act correctly?
- **A lake stores** raw records. **A context layer stores** synthesized knowledge with links to the records.
- **A lake grows** without limit. **A context layer stays** deliberately small, current and reviewed.
- **A lake's quality** is everyone's problem and no one's job. **A context layer's quality** belongs to named owners.

## Signs you are building a context swamp

- Content is added because a connector exists, not because a use case needs it.
- Nobody can say who owns a given piece of knowledge, or when it was last verified.
- The same fact appears in several places with different values.
- Agents cite sources that have since been retired or rewritten.
- Sensitive data shows up in places it was never classified for.
- Teams quietly go back to asking the expert, because the layer is not trusted.

That last sign matches what the retrospective calls *governance gravity*: when governance on the new platform gets hard, organizations drift back to the older, more structured way of working, and the investment becomes shelfware. I have seen this happen with data platforms that were technically excellent. People did not reject the technology. They rejected answers they could not vouch for.

## Retrieval that respects policy

A curated overlay still needs good retrieval, and no single technique is enough. Keyword search finds exact identifiers and error codes. Vector search finds meaning. Code and dependency graphs answer structural questions such as what depends on this. Ontologies resolve the vocabulary differences between teams. The routing layer that chooses among them must also enforce access control, so an agent acting for one user never retrieves knowledge that user is not entitled to see. In a regulated enterprise, policy-aware retrieval is the first requirement, not a later phase.

## Governance debt, applied to context

The retrospective's most useful contribution is a vocabulary for decay, and applied to context the stages are easy to spot. First, content arrives faster than anyone can review it. Then ownership gaps appear, and nobody is sure which version to believe. Then quality slips and agents start citing stale facts. Finally trust collapses and people route around the platform.

The interventions are the same as for data: assign ownership before you publish, require metadata at the door, put quality gates on what agents may treat as verified, and make the debt visible to leadership before it compounds. The cheapest moment to make these decisions is the beginning, which is exactly when teams are most tempted to skip them in favor of speed. My decision rule is blunt: if a source has no owner who will sign for it, it does not go in.

## Isn't this just a knowledge graph?

Partly. Graphs are excellent for relationships, and Gartner's view, as [Atlan summarizes it](https://atlan.com/know/gartner-context-graphs/), is that context graphs augment knowledge graphs rather than replace them; Atlan adds that they carry a procedural layer of decisions, workflows and traces. But a graph is a representation, not a governance model. What matters is curation: who decides what goes in, how it is verified and when it expires. You can store a curated overlay as files, as a graph, or both. You cannot skip the curation.

**What to do on Monday morning:**

- Audit the sources already connected to your AI assistants and flag every one that has no named owner willing to sign for it.
- Write a one-page admission rule requiring an owner, a classification and a review date before anything enters the context layer.
- Test whether an agent acting for a junior user can retrieve knowledge derived from records that user cannot open.
- Ask one team to list facts that appear in several places with different values, and name the authoritative source for each.

Most enterprises already have the connectors to build a lake of context by next quarter. Do you have the owners to build a curated one?

**Bottom line:** We already know what happens when collection is mistaken for knowledge. Build the context layer as a curated overlay: small, owned, retrieval-first and pointing back to the source of truth. Otherwise you are building the next swamp, with agents swimming in it.
