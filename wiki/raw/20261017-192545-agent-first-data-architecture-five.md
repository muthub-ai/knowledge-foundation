---
type: Source
title: 'Agent-first data architecture: five principles'
resource: https://muthub.org/writing/agent-first-data-architecture.md
hash: sha256:fe60f5f273a98001b3eed5d0f6b71ed6b7129b77a229dd091efe2f29c7243729
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2025-09-30'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Agent-first data architecture: five principles

Published 2025-09-30. Adapted from my LinkedIn posts of September 2025 and my Medium writing on lakehouse architecture.

**Data platforms built for people asking questions will strain once the main consumer is software taking actions.** For twenty years we optimized for the analyst with a dashboard: a person who reads a chart, notices that a number looks off, and asks a colleague. An agent does none of that. It reads your metadata literally, queries at machine speed, and acts on what it finds.

That shift is coming faster than most data roadmaps assume. [Gartner predicts](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027) that by 2028 at least 15% of day-to-day work decisions will be made autonomously through agentic AI, up from zero in 2024. Here are the five principles I use when I look at whether a platform is ready for that consumer.

## 1. Design for the machine consumer first

Treat agents as first-class users of the architecture, with interfaces and contracts designed for them rather than bolted onto human dashboards. Zhamak Dehghani's [data mesh principles](https://martinfowler.com/articles/data-mesh-principles.html) already asked us to treat data as a product, with qualities such as discoverability, understandability and trustworthiness. Agents are the most demanding customer that idea has ever had, because they cannot walk over and ask what a column means.

The practical consequence surprises people. A vague column description used to be a minor annoyance. For an agent it is a bug, because the model will confidently fill the gap with a guess. Metadata quality moves from documentation hygiene to production correctness.

This is why I push for data contracts on any dataset an agent can reach: a published schema, an owner, freshness expectations and a description written for a reader who has no tribal knowledge. If a contract breaks, the agent should get an explicit error rather than silently stale data.

## 2. Supply context, and less of it

Agents need to discover, understand and use data without a person approving every request. That means the platform has to provide context for reasoning as well as rows. But more is not better. Anthropic's engineering team describes [context as a finite resource with diminishing marginal returns](https://anthropic.com/engineering/effective-context-engineering-for-ai-agents), and recommends just-in-time retrieval, where agents hold lightweight identifiers and load the underlying data with tools when they need it.

For data platforms this changes API design. Return aggregates, samples and pointers before full result sets. Make it cheap for an agent to ask what exists before it asks for everything. A query that dumps ten thousand rows into a context window is not helpful to the agent; it degrades the reasoning you were trying to support.

## 3. Engineer for bursts and runaway loops

The platform must scale automatically and handle simultaneous requests from many independent agents. Peak load is the easy part to plan for. The harder failure mode is an agent stuck in a retry loop, or a planner that fans a single task out into hundreds of queries.

So elasticity needs a counterweight. Set quotas and cost budgets per agent identity as well as per application. Cache aggressively, because agents ask the same questions far more often than people do. Make it easy to see which agent is driving which workload, so the on-call engineer can stop one misbehaving process without shutting down the rest.

## 4. Put meaning in the platform

Move beyond raw tables. Serve semantic models, knowledge graphs and ontologies so agents understand relationships and business meaning beyond column names. The test I use is simple: ask three agents to compute active customers and see whether they agree.

If they do not, you have a semantics problem that no model upgrade will fix. Agree on business definitions once, publish them as governed objects, and make agents use them. An agent that calculates a key metric three different ways is worse than having no agent at all, because it produces three confident answers.

## 5. Automate governance at machine speed

Agents need their own identities, fine-grained access control and full observability. Auditing and compliance have to run as fast as the agents do, which rules out quarterly access reviews and manual approvals as the main line of defense. Data mesh called this federated computational governance: policies written as code and enforced by the platform.

Agent-to-agent traffic raises the stakes further. Protocols such as Google's [Agent2Agent](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/), which complements MCP by letting agents from different vendors collaborate, mean data can pass through several agents before anyone acts on it. Lineage has to follow the data through each of those hops.

Writes deserve separate treatment. Most agent-ready designs I review focus on read access, because that is where pilots start. The harder problems arrive when agents write back: updating a record, opening a case, adjusting a parameter. Writes need idempotency so a retried call does not double-apply, a clear compensating action for when the agent is wrong, and a record of which agent changed what. I would not let an agent write to a governed table until all three exist. The [OWASP guidance on excessive agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) adds a point I wish more teams followed: enforce authorization in the downstream system rather than trusting the model to decide whether an action is allowed.

## Where I disagree with the common advice

The common advice is to make all your data AI-ready before agents arrive. I think that is a plan to never start. No large enterprise will finish cleaning, describing and contracting its whole estate, and the attempt consumes the budget that should go to the few datasets agents actually need.

I prefer a narrow, certified surface. Pick the ten or twenty data products the first agent use cases depend on, bring those to the standard in this essay, and make everything else unreachable by default. Agents get what has been certified, not whatever a service account happens to see. That reverses the usual pattern, where an agent inherits broad read access from a legacy integration account and the team discovers months later what it could touch.

There is a useful side effect. The certified list becomes a demand signal. When a new use case needs a dataset that is not on it, the request goes to the data owner with a business reason attached, and the use case that needs the data funds the work to bring it up to standard. Data quality stops being an endless cleanup program and becomes a queue ranked by value.

## Why an open lakehouse matters here

For years we kept operational and analytical data in separate worlds: one for reporting, another for ambitious AI projects. That divide added complexity, governance risk and drag. Unifying them on an open lakehouse, with one governed source of truth, is what makes agent-first access practical, because there is one place to enforce policy.

Open table formats add something agents specifically need. [Apache Iceberg](https://iceberg.apache.org/) lets many engines work safely with the same tables at the same time, and supports time travel so a query can run against exactly the same table snapshot later. That second feature is underrated. If an agent records the snapshot it read alongside each decision, you can replay the decision against the data it actually saw. That is the difference between an explanation and a reconstruction.

I learned the value of one governed path at USAA, when we consolidated 360 data scientists onto a single ML platform and cut model deployment from eight weeks to five days. The speed came from standardization, not heroics. Agents will reward the same discipline, and punish its absence faster.

**What to do on Monday morning:**

- List every dataset your current agent pilots can reach and compare it with the datasets they actually need.
- Ask three teams' agents to compute active customers and bring the differing answers to your data governance council.
- Set per-agent query quotas and cost budgets on your main warehouse before the next pilot goes live.
- Block agent writes to governed tables until each has idempotency, a compensating action and per-agent change records.

Most platforms I look at score well on one or two of these principles and poorly on the rest. Which of the five would your platform fail first if a thousand agents showed up tomorrow?

**Bottom line:** The goal is a platform where agents can reason and act safely on governed data. Start by finding which of these five principles your platform violates today, and fix that one first.
