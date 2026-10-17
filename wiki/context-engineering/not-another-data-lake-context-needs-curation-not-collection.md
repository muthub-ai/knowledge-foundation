---
type: Note
id: 34f0ff0c0548
title: 'Not another data lake: context needs curation, not collection'
description: 'The tempting answer to fragmented context is to pour everything into
  one place. We tried that with data, and many lakes became swamps. A context layer
  has to be a curated overlay: retrieval-first, owned, and pointing back to the systems
  that hold the truth.'
tags:
- context-engineering
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
  body_hash: sha256:b07416e7849d6a0d9ce516831a2701e34394e80dd1f9ffa602c71737fc522d50
sources:
- id: s1
  resource: /raw/20261017-192545-not-another-data-lake-context-needs.md
  title: 'Not another data lake: context needs curation, not collection'
kind: Essay
status: draft
stale_after: '2027-10-17T00:00:00Z'
classification: public
owner: human:muthu
canonical_essay: https://muthub.org/writing/not-another-data-lake
relations:
- type: builds_on
  target: /context-engineering/context-fragmentation-why-your-agents-keep-starting-from.md
---

# Overview

The tempting answer to fragmented context is to pour everything into one place. We tried that with data, and many lakes became swamps. A context layer has to be a curated overlay: retrieval-first, owned, and pointing back to the systems that hold the truth.[^s1]

# What it covers

- Why bulk ingestion fails for context
- A curated overlay instead
- Collection versus curation
- Signs you are building a context swamp
- Retrieval that respects policy
- Governance debt, applied to context
- Isn't this just a knowledge graph?

# Bottom line

We already know what happens when collection is mistaken for knowledge. Build the context layer as a curated overlay: small, owned, retrieval-first and pointing back to the source of truth. Otherwise you are building the next swamp, with agents swimming in it.

# Read the original

The full essay is on muthub.org: [Not another data lake: context needs curation, not collection](https://muthub.org/writing/not-another-data-lake).

[^s1]: Not another data lake: context needs curation, not collection, muthub.org, 2026-07-21.

# See also

* [Context fragmentation: why your agents keep starting from zero](context-fragmentation-why-your-agents-keep-starting-from.md) - The knowledge an agent needs is scattered across code, tickets, chat, wikis, incident tools and people's heads. Each fragment is accurate and useless alone. Fragmentation, more than model quality, is what makes enterprise agents brittle.
* [Passive capture: knowledge that writes itself, with humans who approve it](passive-capture-knowledge-that-writes-itself-with-humans-who.md) - Documentation fails because it is a second job. The knowledge we need is already produced as a by-product of work: commits, tickets, incidents, reviews and decisions. Capture it passively, distill it, and keep a human approval gate before anything becomes trusted.
