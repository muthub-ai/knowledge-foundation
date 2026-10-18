---
type: Note
id: 48954235a30f
title: If you can't prove why an AI wrote it, you can't ship it
description: 'Shipping AI-generated code without recording where it came from is unmanaged
  risk. Regulated teams need deterministic provenance for non-deterministic models:
  line-level attribution, Git-native session history and AI bills of materials.'
tags:
- governed-ai
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
  body_hash: sha256:6c02eb82676b5a4c4fa3e833ff177e36c28a9084387ca97458e9eb520c65f54f
sources:
- id: s1
  resource: /raw/20261017-192545-if-you-can-t-prove-why-an-ai-wrote-it.md
  title: If you can't prove why an AI wrote it, you can't ship it
kind: Essay
status: stable
stale_after: '2027-10-17T00:00:00Z'
classification: public
owner: human:muthu
canonical_essay: https://muthub.org/writing/if-you-cant-prove-why-an-ai-wrote-it
verified:
  by: human:muthu
  at: '2026-10-18T02:01:22Z'
relations:
- type: builds_on
  target: /context-engineering/self-describing-knowledge-why-the-open-knowledge-format.md
---

# Overview

Shipping AI-generated code without recording where it came from is unmanaged risk. Regulated teams need deterministic provenance for non-deterministic models: line-level attribution, Git-native session history and AI bills of materials.[^s1]

# What it covers

- Provenance is an old idea with a new gap
- The problem with autonomous agents
- Three patterns for code provenance
- What I found testing it
- From SBOM to AI-BOM
- A decision rule for depth

# Bottom line

Provenance is not paperwork. It is what lets a regulated team say yes to agents: every change traceable to its intent, its model and the person who approved it, captured at creation and governed like the code itself.

# Read the original

The full essay is on muthub.org: [If you can't prove why an AI wrote it, you can't ship it](https://muthub.org/writing/if-you-cant-prove-why-an-ai-wrote-it).

[^s1]: If you can't prove why an AI wrote it, you can't ship it, muthub.org, 2026-02-24.

# See also

* [Model is a tool, harness is the strategy](model-is-a-tool-harness-is-the-strategy.md) - Handing an AI agent a production codebase without a harness is like putting a teenager in a sports car with no dual brakes. Deterministic guardrails and sensors, owned as a platform, are what make agents safe to scale.
* [Adopting MCP in a bank: the four risks to solve first](adopting-mcp-in-a-bank-the-four-risks-to-solve-first.md) - The Model Context Protocol standardizes how agents connect to tools and data. It is silent on whether they should. Four risk areas a regulated institution should resolve before agents get tools.
