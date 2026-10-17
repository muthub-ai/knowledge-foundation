---
type: Note
id: b98c73dd19f3
title: 'Agent-first data architecture: five principles'
description: Data platforms built for people asking questions will strain when the
  main consumer is software taking actions. Five principles for designing data platforms
  where agents are first-class users, and why an open lakehouse helps.
tags:
- data-ai-platforms
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
  body_hash: sha256:215b4ea0230c8f59080f55b52ff4bdef62f8a289fe032d76c4fc9d7807733824
sources:
- id: s1
  resource: /raw/20261017-192545-agent-first-data-architecture-five.md
  title: 'Agent-first data architecture: five principles'
kind: Essay
status: draft
stale_after: '2027-10-17T00:00:00Z'
classification: public
owner: human:muthu
canonical_essay: https://muthub.org/writing/agent-first-data-architecture
---

# Overview

Data platforms built for people asking questions will strain when the main consumer is software taking actions. Five principles for designing data platforms where agents are first-class users, and why an open lakehouse helps.[^s1]

# What it covers

- 1. Design for the machine consumer first
- 2. Supply context, and less of it
- 3. Engineer for bursts and runaway loops
- 4. Put meaning in the platform
- 5. Automate governance at machine speed
- Where I disagree with the common advice
- Why an open lakehouse matters here

# Bottom line

The goal is a platform where agents can reason and act safely on governed data. Start by finding which of these five principles your platform violates today, and fix that one first.

# Read the original

The full essay is on muthub.org: [Agent-first data architecture: five principles](https://muthub.org/writing/agent-first-data-architecture).

[^s1]: Agent-first data architecture: five principles, muthub.org, 2025-09-30.

# See also

* [Capture the why: the knowledge layer enterprise agents are missing](capture-the-why-the-knowledge-layer-enterprise-agents-are.md) - Most enterprise AI pilots hit the same wall: systems record what happened, but the reasoning behind decisions evaporates. Durable, governed context about the why is the real foundation for useful agents.
* [Adopting MCP in a bank: the four risks to solve first](../governed-ai/adopting-mcp-in-a-bank-the-four-risks-to-solve-first.md) - The Model Context Protocol standardizes how agents connect to tools and data. It is silent on whether they should. Four risk areas a regulated institution should resolve before agents get tools.
* [Python or the JVM for production enterprise AI? Put the agent where the transaction lives](python-or-the-jvm-for-production-enterprise-ai-put-the-agent.md) - Python is unrivaled for research and prototyping. Production enterprise AI is mostly integration, security and scale, and with JVM agent frameworks now arriving, the runtime that owns the transaction is often the right home for the agent.
* [From MLOps to AI engineering: what industrializing ML still teaches us](from-mlops-to-ai-engineering-what-industrializing-ml-still.md) - A trained model is the start of the work, not the end. The lessons of industrializing machine learning carry straight into generative and agentic AI, which is why AI engineering has to unify DataOps, MLOps and DevOps.
* [Data & AI on Public Cloud](../leading-ai-change/data-ai-on-public-cloud.md) - A multi-cloud Data & AI strategy and reusable, pre-approved archetypes that made public-cloud onboarding much faster and modernized a legacy data warehouse.
* [Controlled Data Movement](controlled-data-movement.md) - A configuration-driven, secure data movement pattern built at USAA to move 25B+ records a day, then carried to Wells Fargo as a bank-wide framework for analytics and AI.
