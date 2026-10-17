---
type: Note
id: 9a9ad53a7643
title: 'Self-describing knowledge: why the Open Knowledge Format matters, and what
  enterprises must add'
description: In June, Google Cloud published the Open Knowledge Format, and July's
  v0.2 added provenance, verification and freshness. It is the right foundation. Regulated
  enterprises still need to add ownership, classification and a policy for how much
  trust an agent needs before it acts.
tags:
- context-engineering
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
  body_hash: sha256:2fb4e1683f17e8616e50a24f7740b8d8bed1ae800b581af537b7fbd1f5be86e5
sources:
- id: s1
  resource: /raw/20261017-192545-self-describing-knowledge-why-the-open.md
  title: 'Self-describing knowledge: why the Open Knowledge Format matters, and what
    enterprises must add'
kind: Essay
status: draft
stale_after: '2027-10-17T00:00:00Z'
classification: public
owner: human:muthu
canonical_essay: https://muthub.org/writing/self-describing-knowledge-open-knowledge-format
relations:
- type: builds_on
  target: /context-engineering/passive-capture-knowledge-that-writes-itself-with-humans-who.md
---

# Overview

In June, Google Cloud published the Open Knowledge Format, and July's v0.2 added provenance, verification and freshness. It is the right foundation. Regulated enterprises still need to add ownership, classification and a policy for how much trust an agent needs before it acts.[^s1]

# What it covers

- What OKF is
- Why plain files are the right foundation
- What enterprises must add: knowledge that vouches for itself
- Agents that check before they answer
- Consistency and progressive disclosure
- How it fits with what you already run
- Keep the profile small
- Cautions

# Bottom line

Knowledge for the AI era should be plain, portable and self-describing: Markdown people can read, structure agents can parse, and metadata that says who owns it, where it came from, when it expires and how far to trust it. OKF v0.2 now covers most of that. Enterprises should add ownership, classification and trust policy, together.

# Read the original

The full essay is on muthub.org: [Self-describing knowledge: why the Open Knowledge Format matters, and what enterprises must add](https://muthub.org/writing/self-describing-knowledge-open-knowledge-format).

[^s1]: Self-describing knowledge: why the Open Knowledge Format matters, and what enterprises must add, muthub.org, 2026-09-15.

# See also

* [Passive capture: knowledge that writes itself, with humans who approve it](passive-capture-knowledge-that-writes-itself-with-humans-who.md) - Documentation fails because it is a second job. The knowledge we need is already produced as a by-product of work: commits, tickets, incidents, reviews and decisions. Capture it passively, distill it, and keep a human approval gate before anything becomes trusted.
* [The cost of unmanaged context](the-cost-of-unmanaged-context.md) - Enterprises budget for compute, models and licenses, but almost none budget for the context those models depend on. Unmanaged context is the largest cost nobody tracks, and every new AI agent adds to it.
