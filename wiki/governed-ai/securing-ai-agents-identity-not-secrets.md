---
type: Note
id: 594bcd1a643b
title: 'Securing AI agents: identity, not secrets'
description: Agents act on their own, at machine speed, across many systems. Static
  credentials and perimeter thinking don't hold up. Attested identity, explicit delegation
  and policy enforced outside the model do.
tags:
- governed-ai
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
  body_hash: sha256:f33fbba601baaeae46fcaeb46b0a47dd8d2c90409b6472b351e878306045eeec
sources:
- id: s1
  resource: /raw/20261017-192545-securing-ai-agents-identity-not-secrets.md
  title: 'Securing AI agents: identity, not secrets'
kind: Essay
status: stable
stale_after: '2027-10-17T00:00:00Z'
classification: public
owner: human:muthu
canonical_essay: https://muthub.org/writing/securing-ai-agents-identity-not-secrets
verified:
  by: human:muthu
  at: '2026-10-18T02:01:22Z'
---

# Overview

Agents act on their own, at machine speed, across many systems. Static credentials and perimeter thinking don't hold up. Attested identity, explicit delegation and policy enforced outside the model do.[^s1]

# What it covers

- Agents are workloads, so give them workload identity
- What the MCP specification now gives you
- The toxic agent flow: when every identity check passes
- Context-aware access, enforced outside the model
- A practical checklist

# Bottom line

Trust in agents starts with identity built for machines: attested, short-lived, delegated and checked by policy the model cannot argue with. The more capable agents become, the less optional this gets.

# Read the original

The full essay is on muthub.org: [Securing AI agents: identity, not secrets](https://muthub.org/writing/securing-ai-agents-identity-not-secrets).

[^s1]: Securing AI agents: identity, not secrets, muthub.org, 2025-05-29.

# See also

* [Adopting MCP in a bank: the four risks to solve first](adopting-mcp-in-a-bank-the-four-risks-to-solve-first.md) - The Model Context Protocol standardizes how agents connect to tools and data. It is silent on whether they should. Four risk areas a regulated institution should resolve before agents get tools.
* [Designing an enterprise MCP registry: the control point agents need](designing-an-enterprise-mcp-registry-the-control-point.md) - As agents multiply, every enterprise needs an authoritative directory of the tools they can call. What a governed MCP registry must do, what the official registry leaves to you, and the mistakes to avoid.
