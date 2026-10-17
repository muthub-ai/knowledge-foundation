---
type: Source
title: 'Securing AI agents: identity, not secrets'
resource: https://muthub.org/writing/securing-ai-agents-identity-not-secrets.md
hash: sha256:2c6dbed6d270df2b419393d17d9e8ca3d0d7ef54eaabd417ccb434138c4cfbdf
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2025-05-29'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Securing AI agents: identity, not secrets

Published 2025-05-29. Adapted from my LinkedIn posts of May 11 and May 27, 2025.

**Every AI agent should be treated as a workload with its own verifiable identity, and nothing it does should depend on a secret someone pasted into a config file.** That premise sounds obvious. Most agent deployments I see still violate it.

Agents act on their own, at machine speed, across many systems. Static API keys and network perimeters were designed for a world where a person sat behind each request, or a service did one predictable thing. Neither assumption holds anymore. Last October [Gartner predicted that by 2028, 25% of enterprise breaches will be traced back to AI agent abuse](https://www.gartner.com/en/newsroom/press-releases/2024-10-22-gartner-unveils-top-predictions-for-it-organizations-and-users-in-2025-and-beyond), from both external and malicious internal actors. My guess is that a good share of those breaches will start with an identity problem: a credential that was too broad, too long-lived or never tied to a specific agent.

## Agents are workloads, so give them workload identity

An agent that reads data and calls tools is a workload acting on someone's behalf. We already have a mature pattern for workloads. [SPIFFE](https://spiffe.io/docs/latest/spiffe-about/overview/) defines short-lived cryptographic identity documents, called SVIDs, issued only after the node or workload has been attested, and rotated automatically. A workload proves what it is at runtime instead of presenting a long-lived secret that anyone who copies it can reuse.

For agents I would add something workload identity alone does not cover: delegation. An agent rarely acts purely for itself. It acts for a user, inside a task. So the credential it presents to a tool should carry three facts: which agent, on whose behalf, and for what purpose. Drop any one of the three and your audit log can no longer tell an authorized action from a hijacked one.

## What the MCP specification now gives you

The [MCP authorization specification](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization), added in the March 2025 revision, makes much of this practical for HTTP-based servers. It builds on OAuth 2.1 and requires PKCE for every client. A bearer token must accompany every HTTP request, even within the same session, and tokens may never appear in a query string. Servers should enforce token expiration and rotation and keep lifetimes limited. When a server delegates login to a third-party identity provider, it issues its own token bound to that session rather than handing the upstream token to the client, and the spec tells implementers to consider the security implications of token chaining.

That is real progress over the shared API keys most early servers relied on. It still leaves two things to you. The spec does not spell out how a token is tied to the one server it was meant for, so audience checks deserve explicit attention in your own design. And it does not decide what an agent may do with a perfectly valid token. That is the policy layer's job, and in most designs I review it is the thinnest part.

There is one gap worth calling out. The same specification says servers running over the local STDIO transport should not follow this flow and should instead retrieve credentials from the environment. That is sensible for a developer laptop. In an enterprise it is exactly where long-lived secrets hide: a personal access token in an environment variable, shared across every local server the developer has installed. My rule is that local servers are for experiments, and anything that touches production data runs as a remote server behind proper authorization.

## The toxic agent flow: when every identity check passes

Earlier this week [Invariant Labs disclosed a toxic agent flow](https://invariantlabs.ai/blog/mcp-github-vulnerability) involving the official GitHub MCP server. A malicious issue planted in a public repository could steer an agent, during a routine request to look at open issues, into pulling data from the user's private repositories and publishing it in a public pull request. The researchers were clear that the server code itself was not flawed. They called it an architectural problem at the level of the agent system.

This is the part I find most instructive. Every identity check in that scenario passed. The agent held a legitimate token with legitimate scope. What failed was the absence of any rule between untrusted input and privileged action. The token reached every repository the user could see, and nothing in the session understood that reading a stranger's issue should narrow what the agent does next, not widen it.

Two lessons follow. Scope credentials to the task, not to the user's full reach. And treat the trust level of what an agent has read as an input to authorization. Identity tells you who is acting. It cannot tell you whether the actor has just been manipulated.

## Context-aware access, enforced outside the model

Static roles assume the risk of an action is fixed. For agents it is not. Reading a customer record during a service request is routine. The same read moments after the agent ingested an external email deserves a second look. Policy should weigh the agent's identity, the delegating user, the task, the data sensitivity and what has entered the context during the session.

The enforcement point has to sit outside the model. A model can be talked into things; a policy engine evaluating a signed request cannot. That is how I think about guardrails in general: the model proposes, deterministic code decides. The OWASP GenAI Security Project's [Agentic AI: Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/), published in February, is a good reference for the threat classes your policy layer should expect to meet.

## A practical checklist

- Give every agent its own attested identity and short-lived credentials. Never let an agent reuse a human's token.
- Carry delegation explicitly, so agent, user and task travel with every call.
- Scope each grant to the task, separate read from write, and expire grants when the task ends.
- Treat everything an agent reads from outside as untrusted, including issues, documents, emails and web pages, and let that taint reduce what it may do next.
- Enforce critical rules deterministically, outside the model, and require human approval for irreversible actions.
- Log every tool call with identity, delegation, inputs, policy decision and result.

In the large regulated organizations I have worked in, the hardest item on that list is not technical. It is convincing teams that a working demo running on a shared service account is technical debt from day one. Retrofitting identity later means re-plumbing every integration the agent touched, usually under audit pressure.

> The model proposes, deterministic code decides.

Identity is the least glamorous part of agentic AI and the part that decides whether anything else can be trusted. So here is the test I would run first: how many of the agents in your environment today could tell you, for a given action, exactly whose authority they were using?

**Bottom line:** Trust in agents starts with identity built for machines: attested, short-lived, delegated and checked by policy the model cannot argue with. The more capable agents become, the less optional this gets.
