---
type: Source
title: 'Self-describing knowledge: why the Open Knowledge Format matters, and what
  enterprises must add'
resource: https://muthub.org/writing/self-describing-knowledge-open-knowledge-format.md
hash: sha256:5372c55885579b396b6891af6af95c6c46070918ce7feeef3a6759e55f0ba15b
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2026-09-15'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Self-describing knowledge: why the Open Knowledge Format matters, and what enterprises must add

Published 2026-09-15. Part 5 of the Context Engineering series.

**Knowledge for AI agents should live in plain files that state, on their face, who owns them and how far to trust them.** Throughout this series I have argued that context is the asset AI runs on, that it is fragmented, that it should be curated rather than collected, and that it can be captured from the work itself. The last question is the most practical one: what format should that knowledge take?

On June 12, 2026, Google Cloud published a candidate answer: the [Open Knowledge Format](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing), or OKF. Six weeks later Google shipped [OKF v0.2](https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals), which added provenance and trust signals. I think it gets the foundation right. I also think regulated enterprises need to build on top of it carefully, and together.

## What OKF is

OKF is deliberately small. Knowledge is a directory of Markdown files, one concept per file, where the file path is the concept's identity. Each file carries YAML frontmatter, and only one field is required: `type`. A title, a description, a link to the live resource and tags are recommended. Concepts link to each other with ordinary Markdown links, which turns the directory into a graph. Optional index files support progressive disclosure, and optional log files record history. The [spec and reference code](https://github.com/GoogleCloudPlatform/open-knowledge-format) are public, and since August they have their own repository.

Google's principles are the important part: minimally opinionated, producers and consumers independent of each other, and a **format, not a platform**, with no required cloud, database, model provider or SDK. Google describes OKF as formalizing the [LLM wiki pattern](https://noqta.tn/en/blog/karpathy-llm-wiki-knowledge-base-beyond-rag-2026) Karpathy popularized, and places it in the same family as convention files like AGENTS.md. I find it useful to think of three pieces: instructions for agents (AGENTS.md), executable workflows (skills), and reference knowledge. OKF fills the third.

## Why plain files are the right foundation

- **People and agents read the same thing.** Markdown renders in any editor and on GitHub, and models read it natively.
- **Version control comes free.** Put knowledge in Git and you get history, diffs, review, blame and rollback, the controls engineering already trusts.
- **Retrieval stays flexible.** The same files can feed keyword search, vector indexes or a graph.
- **Switching models stays cheap.** Knowledge outlives any one model, vendor or agent framework when it lives in an open format you own.

## What enterprises must add: knowledge that vouches for itself

Here is my main argument. A regulated enterprise needs every concept to say not only what it *is* but whether it can be **trusted**, and v0.2 went a long way. It added `sources` for provenance, `generated` and `verified` to separate who wrote a concept from who confirmed it, trust tiers derived from them, a `status` lifecycle and a `stale_after` date. I would adopt those as written. What the core still does not say is who is *accountable*: a verifier checked a page once, an owner answers for it next quarter. There is no sensitivity field, and the trust tiers are explicitly advisory, so the rule for which tier an agent needs before it acts is left to each consumer. The spec lets producers add their own keys, and enterprises should converge on a common set.

These are the fields I would standardize on, as a small enterprise profile on top of OKF v0.2:

- **Identity:** a canonical identifier that ties the concept to the system it describes, so two sets of files never disagree about which application they mean.
- **Owner:** the accountable team, distinct from whoever generated or verified it.
- **Classification:** sensitivity and handling rules that travel with the knowledge.
- **Required trust:** the minimum tier an agent needs before acting on the concept, so the policy sits next to the content instead of inside every agent's prompt.

In practice, an enterprise-profiled concept might look like this. Everything above the comment is OKF v0.2, and the rest are producer-defined fields, which the format explicitly allows:

```yaml
---
type: Application
title: Payments Gateway
description: Routes card authorizations between channels and processors.
resource: https://catalog.example.com/apps/payments-gateway
tags: [payments, tier-1]
status: stable
sources:
  - id: gateway-repo
    resource: https://git.example.com/payments/gateway
  - id: pay-1042
    resource: https://tickets.example.com/browse/PAY-1042
generated: { by: capture_agent/v3, at: 2026-09-02T10:15:00Z }
verified: { by: human:j.doe, at: 2026-09-03T09:00:00Z }
stale_after: 2026-12-01T00:00:00Z
# Enterprise profile (producer-defined)
id: app:payments-gateway
owner: team-payments-platform
classification: internal
required_trust: human-reviewed
---
```

Everything here is human-readable and diffable, and none of it requires a proprietary platform. An agent can decide at a glance whether to trust the content below it.

## Agents that check before they answer

Self-describing knowledge changes agent behavior. An agent that can read trust signals can be told to prefer verified knowledge, label drafts as drafts, refuse to act on expired content, and cite its sources by default. That is the difference between an assistant that sounds right and one an auditor can work with.

It also makes governance computable, the underrated benefit. You can measure how much of your knowledge is owned, fresh and verified, and where the gaps sit, with a script instead of a survey. Governance that can be counted gets funded. Governance that lives in a policy document gets audited once a year.

## Consistency and progressive disclosure

Format is half the answer, and consistency is the other half. For a technology organization I would pair the format with a standard set of sections for every application: purpose, architecture and dependencies, security, failure modes, operations and recent changes. A standard outline lets agents move through any application the same way and lets you measure completeness across a portfolio.

OKF's index files make that structure cheap to use. An agent reads a short index for an application, sees what exists, and opens only the concepts it needs. That is the file-system version of the just-in-time loading [Anthropic recommends](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), and a direct answer to context rot. Log files add the history of what changed, when and why, which is exactly the decision trace that systems of record lose.

## How it fits with what you already run

Self-describing knowledge does not replace your catalogs, repositories or configuration database. It sits on top of them and points back to them through the resource and sources fields. Serve the files through an MCP server and every coding agent, chat assistant and operations tool reads the same governed knowledge.

## Keep the profile small

Once teams see the value of metadata, the temptation is to keep adding fields. I have watched this happen with data catalogs: dozens of attributes per table, most of them empty, quietly teaching everyone that the metadata cannot be trusted.

My rule is that a field earns its place only if an agent or a control will act on it. Owner, classification and required trust pass that test easily, as do the core's verification and staleness fields, because each one changes what an agent is allowed to do. Most other details belong in the body of the file, where people can read them, rather than in frontmatter that implies someone maintains them.

Enforce the profile where files are written, not where they are read. A check on the pull request that rejects a concept without an owner or a `stale_after` date costs almost nothing, and it stops decay before it starts.

## Cautions

OKF is at v0.2, and it is early: two versions in six weeks and a new home in August. An [independent review of the spec](https://agentic-ai.readthedocs.io/en/latest/Standards/open-knowledge-format/), written at the v0.1 release, noted that it had no formal governance body, unlike AGENTS.md, which now sits with the Agentic AI Foundation under the Linux Foundation. That has not changed with v0.2: Google still publishes and controls the spec. Validators and ecosystem tooling are still forming, and I have not seen published benchmarks of retrieval or agent gains. Because the core is minimally opinionated, consistency inside a large organization depends on your own conventions.

Treat it as a strong direction rather than a finished standard: adopt the core, pin the version you build against, keep your enterprise fields in a documented profile, and contribute back. The worst outcome would be every enterprise inventing its own incompatible extensions and recreating the fragmentation the format was meant to solve.

**What to do on Monday morning:**

- Pick ten knowledge files for one critical application and check whether each could state its owner, sources and last verified date.
- Draft an enterprise profile of no more than four fields on top of the OKF v0.2 core and circulate it to architecture and risk.
- Add a pull request check that rejects any knowledge file missing an **owner** or a `stale_after` date.
- Instruct one internal agent to label anything below human-reviewed as draft and to decline actions based on stale knowledge.

In the end, the format question is a readiness question. If your organization published its enterprise profile tomorrow, which of these fields would your current knowledge actually be able to fill in?

**Bottom line:** Knowledge for the AI era should be plain, portable and self-describing: Markdown people can read, structure agents can parse, and metadata that says who owns it, where it came from, when it expires and how far to trust it. OKF v0.2 now covers most of that. Enterprises should add ownership, classification and trust policy, together.
