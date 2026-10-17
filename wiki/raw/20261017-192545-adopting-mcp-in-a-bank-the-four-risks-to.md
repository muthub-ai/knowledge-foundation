---
type: Source
title: 'Adopting MCP in a bank: the four risks to solve first'
resource: https://muthub.org/writing/adopting-mcp-in-a-bank.md
hash: sha256:ba52bfd167a07a30f9989f9e33658a8f03b2c5a73238b388f79336bbd9c66753
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2025-04-22'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Adopting MCP in a bank: the four risks to solve first

Published 2025-04-22. Adapted from my LinkedIn post of April 18, 2025.

**MCP standardizes how an agent connects to a tool; it does nothing to decide whether that agent should be allowed to.** After months of looking at the Model Context Protocol through the eyes of a bank's architecture review, that is the sentence I keep coming back to. The protocol is good. It is also, by design, silent on most of the questions a regulator, an auditor or a model risk officer will ask.

That silence is not a flaw. A wire protocol should not encode a bank's risk appetite. But it means the work that matters most sits outside the spec, and teams that treat a working MCP connection as a finished integration are measuring the wrong thing. Here are the four areas I would resolve before any agent in a regulated institution gets a tool that can change anything.

## Security: the attack surface is the tool description

Most security reviews start by asking whether the server is patched and authenticated. Those questions matter, but the more interesting risks live where traditional API review never looked. Earlier this month, [Invariant Labs described tool poisoning attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks), in which hidden instructions inside a tool's description steer the model while the user sees only a short, harmless tool name. The same research showed two variants that should worry anyone running a shared environment: a server that changes its tool description after the client approved it (a rug pull), and a malicious server whose description changes how the agent uses a different, trusted server.

The lesson for a bank is uncomfortable. Text that a model reads behaves like code, even if no engineer would call it that. The current specification says as much: [clients must treat tool annotations as untrusted unless they come from trusted servers](https://modelcontextprotocol.io/specification/2025-03-26/server/tools), and a human should always be able to deny a tool call. Prompt injection sits at the top of the [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/), with excessive agency not far behind. In MCP those two risks meet.

My working rule is that tool metadata gets the same treatment as code. It is pinned, hashed and diffed on every change, and a changed description goes back through approval. Teams find this tedious until the first time a description changes underneath them.

## Auditability: reconstruct the decision behind the call

Supervisors expect lineage, explainability and decisions you can defend after the fact. MCP gives you a clean record of the tool call: which tool, which arguments, what came back. That record is necessary and nowhere near sufficient. When an examiner asks why a customer's limit changed, the agent called update_limit is not an answer.

What you need is the chain around the call: the user request, the context the model saw, the policy version that permitted the action, the identity the agent acted under, and the human approval if one was required. Most of that lives in the host application, not the protocol. In my experience the teams that get this right design the audit record first and build the agent around it. Teams that bolt logging on later end up with mountains of tool traces and still cannot answer the examiner's question.

## Privacy and residency: context is a data flow

Every time an agent pulls a customer record into its context window, that record has moved. It may have left a region, reached a third-party model provider, or landed in a log nobody classified. Banks already have strong rules for data minimization and purpose limitation. The gap is that agents create new, implicit data flows that existing controls never see.

The fix is mostly plumbing. Classify each MCP server by the highest sensitivity of data it can return. Filter or tokenize sensitive fields at the server, before they reach the model, instead of trusting a prompt to ignore them. Keep regional deployments of servers that touch regulated data, and record the model endpoint as a processor in your data maps. None of this is new. It has to be applied to a new kind of pipe.

## Maturity: plan for a protocol that keeps moving

The protocol has changed a lot in a short time. The [March 2025 authorization specification](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization) brings OAuth 2.1 to HTTP transports and requires PKCE for every client. That is progress, but authorization is still optional, local servers read credentials from the environment, and the example flow has each MCP server acting as its own authorization server. A bank already has an identity provider. I would require servers to accept its tokens, scope each token to one server, and never pass a received token through to downstream APIs.

Registries will help once they exist. The project's published roadmap plans an official MCP Registry for centralized server discovery, designed as an API layer that marketplaces build on. Until then, public directories offer discovery, not assurance, and a bank should not wait. Build an internal catalog: assess each public server once, publish the approved versions internally, block everything else. Legacy integration, performance at enterprise scale and the upkeep of many small servers are still real costs. I budget for them as ongoing platform work, not a one-time project.

## A worked example: onboarding one server

Abstract controls are easier to agree with than to apply, so here is how I would take a single MCP server from request to production. Suppose a team wants an agent to look up a customer's recent transactions to help service staff answer questions.

First, classify the server by the most sensitive thing it can return, which here is customer financial data. That one decision sets the rest: regional deployment, field-level masking for account numbers, and a model endpoint approved for that data class. Second, scope it to read-only, with a token bound to that server alone and no ability to pass it downstream. Third, pin the tool descriptions, hash them, and register the approved version in the internal catalog so a later change triggers review instead of silently taking effect.

Fourth, write the audit record before the agent exists: who asked, under which identity, which policy version allowed it, what the model saw and what it returned. Then run it with a person reviewing every response for a defined period. Only when the record can answer a mock examiner's question end to end would I consider a second tool, and a write tool would go through the same steps again with a mandatory human approval in front of it. The pattern is slow for the first server and fast for the tenth, because the controls are reused.

## Use the risk framework you already have

The mistake I see most often is a parallel governance track for agents. Banks already run model risk management, third-party risk management, data governance and change control. MCP adoption should plug into all four. A vendor's MCP server is a third-party component. An agent that makes or influences decisions belongs in the model inventory. A changed tool description is a change, and it goes through change control.

The [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) and its Generative AI Profile give engineers and risk partners a shared vocabulary built around govern, map, measure and manage. I use it less as a checklist and more as a translation layer, so that both sides mean the same thing when they say a control exists.

One sequencing rule has served me well. Start with read-only tools on low-sensitivity data, with a human approving every action. Widen scope only when the audit record proves you can reconstruct what happened. Autonomy is earned with evidence, one tool at a time.

> Architecture is not what you say you'll build; it's what you actually allow into production.

**What to do on Monday morning:**

- Inventory every MCP server already in use across engineering, including local ones in developer tools, and classify each by the most sensitive data it can return.
- Require tool descriptions to be pinned, hashed and diffed, and route any changed description back through approval like a code change.
- Draft the audit record schema for one agent use case and test whether it can answer a mock examiner's question end to end.
- Stand up an internal catalog of approved MCP servers and block agents from connecting to any server that is not listed in it.

The security concerns are real, and I think they are solvable with controls banks already know how to run. What I am still testing is where the line should sit between what a person must approve and what an agent may do alone. Where have you drawn that line for MCP tools in your organization, and what evidence moved it?

**Bottom line:** MCP solves connectivity. Trust is still an architecture problem: identity, policy, audit and a governed server catalog decide whether a bank can use it safely.
