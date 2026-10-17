---
type: Source
title: 'Designing an enterprise MCP registry: the control point agents need'
resource: https://muthub.org/writing/designing-an-enterprise-mcp-registry.md
hash: sha256:121afd43530b670ba398c6c57575535717abae437408d3fa8cc64cc5972dea2b
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2025-09-18'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Designing an enterprise MCP registry: the control point agents need

Published 2025-09-18. Adapted from my LinkedIn posts of April 3, 2025 and September 8 and 16, 2025.

**An enterprise MCP registry is where agent governance stops being a policy document and becomes something the runtime enforces.** In April 2025, before any official specification existed, I sketched what a large enterprise would need from a directory of Model Context Protocol servers. Since then [the official MCP Registry has launched in preview](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/) and GitHub has shipped [internal registry and allowlist controls for Copilot](https://github.blog/changelog/2025-09-12-internal-mcp-registry-and-allowlist-controls-for-vs-code-insiders/). Both confirm the core idea. Both leave the hardest enterprise questions to us.

## Why a directory turns into a control plane

The obvious reason to build a registry is discovery. Without one, every developer edits a config file by hand and points it at whatever server they found in a forum thread. That works for ten people. At the scale of a large bank it produces hundreds of unreviewed connections and no inventory.

The less obvious reason matters more. A registry is the one place where you can say with confidence which tools exist in your environment. GitHub's design makes the point concrete: administrators point Copilot at an internal registry, and a registry-only policy blocks unlisted servers at runtime (enforced in VS Code Insiders today, with the stable release to follow). Discovery and allowlisting become the same artifact. Once that is true, security review, third-party risk assessment and data classification share a single gate, and the gate is enforced by software instead of by memo.

## What the official registry gives you, and what it leaves out

The upstream registry describes itself as an open catalog and API for publicly available MCP servers. It holds self-reported metadata, moderates through community reports and maintainer denylisting, and publishes an open API specification so others can build compatible sub-registries. Its authors expect enterprises with strict security requirements to run private sub-registries that use the public catalog as their upstream.

I think that is the right division of labor. A public registry can tell you that a server exists and who claims to publish it. It cannot tell you whether that server is safe to connect to customer data. That judgment belongs to you, and the private registry is where you record it, with the evidence attached.

One design question comes up early: should the internal registry only list servers, or should traffic flow through a gateway it controls? I lean toward both, in stages. A listing-only registry is quick to stand up and gives you an inventory. A gateway lets you enforce the pinned version, inspect tool definitions as they are served, and cut off a server in minutes rather than waiting for every client to refresh. For low-risk internal tools, listing is enough. For anything that touches regulated data or can move money, I want the gateway in the path, because a registry entry that clients can ignore is advice, not control.

## Requirements I would hold a design to

My original list of discovery, trust, ecosystem support and metadata still holds. After watching the ecosystem grow through most of this year, I would sharpen it into six requirements.

1. **Authenticated publishing.** Only a verified owner can register, update, deprecate or retire a server, and every change is attributable to a person or pipeline.
2. **Capabilities declared against a taxonomy.** Servers state what they do (read a customer profile, initiate a payment) in terms a policy engine understands, not in free text a model interprets.
3. **Pinned, immutable versions.** An approval attaches to a specific version and a hash of its tool definitions. A new description is a new version and needs review.
4. **Trust tiers clients can query.** Community, internally reviewed and approved for regulated data are different states, and clients filter on them.
5. **Data sensitivity ceilings.** Each entry records the highest classification of data the server can return, so an agent's tools can be matched to its clearance.
6. **Lifecycle and retirement.** Deprecation is announced in the registry, clients are warned, and a retired server stops resolving.

Pinning deserves the most attention. [Invariant Labs showed](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) that a malicious server can change a tool's description after a client has approved it. A registry that approves servers by name rather than by content will keep serving the poisoned version without noticing. Supply chain risk, which OWASP ranks third in its [Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/), arrives through updates at least as often as through first installs.

In practice, an internal entry ends up looking something like this:

```yaml
name: payments-readonly
version: 2.3.1
tool_definitions_sha256: 9f2c...e41a
publisher: team-payments-platform
trust_tier: approved-regulated
capabilities: [payment.status.read, payment.history.read]
data_ceiling: confidential
upstream: null   # internal server, no public source
status: active
```

## The agent registry is the other half

A tool registry answers what can be called. An auditor will also ask who called it. That needs a matching registry of agents, each with an owner, a purpose, an identity, the tool grants it holds, and the model and prompt versions it runs. Google's [Agent2Agent protocol](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) points in a similar direction with its Agent Card, a JSON description an agent publishes so other agents can find out what it does. Inside an enterprise, the same idea becomes an inventory record with an accountable owner.

Join the two registries and you can answer the questions that come up in every serious review: which agents exist, which tools each may call, who approved the grant, and which version of both was running when a given decision was made. In my experience that last question separates a demo from a production system. If you cannot answer it, sooner or later you will have to switch something off to find out.

## Three mistakes I would avoid

The first is building the registry as a wiki page. If clients do not resolve servers through it at runtime, it drifts from reality within a quarter and nobody trusts it. The second is treating approval as a one-time event, when the real risk arrives with each update. The third is routing every review through one central team. The registry should hold the policy and the evidence. Domain teams should own their servers, automated checks should handle most of the gating, and people should review the exceptions.

I would also not wait for the ecosystem to settle. The specifications are open and the APIs are documented, and a basic internal registry that mirrors approved upstream entries is a modest piece of engineering. The operating model around it takes longer to build, which is the best reason to start now.

Every enterprise will make different calls about what belongs in its registry and what stays out. I am curious where others are starting: what is the first thing you would want your MCP registry to block?

**Bottom line:** MCP standardizes the connection. A governed registry decides which connections are allowed. Build the second before you scale the first.
