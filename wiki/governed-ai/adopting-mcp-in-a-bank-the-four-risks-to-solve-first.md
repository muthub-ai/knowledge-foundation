---
type: Note
id: 4da7278bd99f
title: 'Adopting MCP in a bank: the four risks to solve first'
description: The Model Context Protocol standardizes how agents connect to tools and
  data. It is silent on whether they should. Four risk areas a regulated institution
  should resolve before agents get tools.
tags:
- governed-ai
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
  body_hash: sha256:cc255509a2a691227dc2e6e463e880649f8f45808a3ae54b3f3cbd1b7f5700e2
sources:
- id: s1
  resource: /raw/20261017-192545-adopting-mcp-in-a-bank-the-four-risks-to.md
  title: 'Adopting MCP in a bank: the four risks to solve first'
kind: Essay
status: draft
stale_after: '2027-10-17T00:00:00Z'
classification: public
owner: human:muthu
canonical_essay: https://muthub.org/writing/adopting-mcp-in-a-bank
---

# Overview

The Model Context Protocol standardizes how agents connect to tools and data. It is silent on whether they should. Four risk areas a regulated institution should resolve before agents get tools.[^s1]

# What it covers

- Security: the attack surface is the tool description
- Auditability: reconstruct the decision behind the call
- Privacy and residency: context is a data flow
- Maturity: plan for a protocol that keeps moving
- A worked example: onboarding one server
- Use the risk framework you already have

# Bottom line

MCP solves connectivity. Trust is still an architecture problem: identity, policy, audit and a governed server catalog decide whether a bank can use it safely.

# Read the original

The full essay is on muthub.org: [Adopting MCP in a bank: the four risks to solve first](https://muthub.org/writing/adopting-mcp-in-a-bank).

[^s1]: Adopting MCP in a bank: the four risks to solve first, muthub.org, 2025-04-22.

# See also

* [If you can't prove why an AI wrote it, you can't ship it](if-you-can-t-prove-why-an-ai-wrote-it-you-can-t-ship-it.md) - Shipping AI-generated code without recording where it came from is unmanaged risk. Regulated teams need deterministic provenance for non-deterministic models: line-level attribution, Git-native session history and AI bills of materials.
* [Model is a tool, harness is the strategy](model-is-a-tool-harness-is-the-strategy.md) - Handing an AI agent a production codebase without a harness is like putting a teenager in a sports car with no dual brakes. Deterministic guardrails and sensors, owned as a platform, are what make agents safe to scale.
* [Agent-first data architecture: five principles](../data-ai-platforms/agent-first-data-architecture-five-principles.md) - Data platforms built for people asking questions will strain when the main consumer is software taking actions. Five principles for designing data platforms where agents are first-class users, and why an open lakehouse helps.
* [Designing an enterprise MCP registry: the control point agents need](designing-an-enterprise-mcp-registry-the-control-point.md) - As agents multiply, every enterprise needs an authoritative directory of the tools they can call. What a governed MCP registry must do, what the official registry leaves to you, and the mistakes to avoid.
* [Securing AI agents: identity, not secrets](securing-ai-agents-identity-not-secrets.md) - Agents act on their own, at machine speed, across many systems. Static credentials and perimeter thinking don't hold up. Attested identity, explicit delegation and policy enforced outside the model do.
* [Enterprise Generative AI Architecture](enterprise-generative-ai-architecture.md) - An enterprise-grade Generative AI reference architecture: a governed path from experiment to production, adopted as the reference model across business lines.
