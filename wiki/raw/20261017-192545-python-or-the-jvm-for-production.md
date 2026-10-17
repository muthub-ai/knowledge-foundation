---
type: Source
title: Python or the JVM for production enterprise AI? Put the agent where the transaction
  lives
resource: https://muthub.org/writing/python-or-jvm-for-enterprise-ai.md
hash: sha256:12558e07145c529eb785f1655b7a93139ee12553cb224412eab6f730e426cbf5
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2025-06-24'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Python or the JVM for production enterprise AI? Put the agent where the transaction lives

Published 2025-06-24. Adapted from my LinkedIn post of June 19, 2025.

**Before you commit your production AI stack to Python, separate AI research from AI engineering.** Python is unrivaled for prototyping, training and evaluation, and I would not try to change that. But most enterprise AI is not a modeling problem. It is a problem of integration, security and scale, and those problems already have a home in most large firms.

In my conversations with architects and data scientists, this debate tends to split along job titles. Data scientists defend Python. Platform and application architects ask why anyone would rebuild transaction handling in a second runtime. Both are right about their own work. The mistake is letting one group's default become the whole stack.

## What production AI actually does

Look at what a production agent spends its time on. It calls a model over HTTP. Then it reads customer data under entitlements, calls internal services, writes to systems of record, handles retries and idempotency, logs evidence for audit, and fails safely. The model call is the easy part. Everything around it is the system.

Scale shows up in unglamorous ways. An agent that fans out to five internal services per request needs connection pooling, timeouts, circuit breakers and back-pressure. The JVM has mature answers for all of these, and virtual threads in recent Java releases have made highly concurrent, I/O-bound code much simpler to write than it used to be.

In most large financial institutions, almost everything runs on the JVM. Decades of reliability engineering, security tooling, identity integration and operational know-how sit there. When we wire an agent into a payment, a claim or a servicing workflow, the hard questions are about transactions and controls, not about which language has the nicer notebook.

## Infrastructure parity has arrived

Not long ago the honest answer was that the JVM lagged badly. For the building blocks, that gap has closed. [Spring AI reached 1.0 GA in May 2025](https://spring.io/blog/2025/05/20/spring-ai-1-0-GA-released) with a portable client across 20 model providers, a vector store abstraction across 20 databases, annotation-based tool calling, Model Context Protocol client and server support, and Micrometer observability that tracks latency, token usage and tool calls. That last item matters more to a bank than the rest, because it plugs AI into the monitoring stack operations teams already trust.

[LangChain4j reached 1.0 in May 2025](https://github.com/langchain4j/langchain4j/releases/tag/1.0.0) for its core modules, with model clients, retrieval, tool calling and chat memory, while its MCP client followed as a beta. The following week Google announced the [initial Java release of its Agent Development Kit](https://developers.googleblog.com/agents-adk-agent-engine-a2a-enhancements-google-io/), which puts a major cloud provider's agent framework on the JVM alongside its Python original.

## The new frontier is agent frameworks

The conversation has moved past model clients to orchestration, state, error handling and governance. This is where strongly typed, well-instrumented runtimes earn their keep. When an agent can take actions, you want the compiler to catch a malformed tool contract before a customer does.

Typing helps with something less obvious: evidence. When tool inputs and outputs are typed records, every agent step can be logged as structured data that an auditor or a monitoring rule can query, instead of free text someone has to interpret later. It is a small design choice with a large effect on how quickly you can answer an examiner.

Rod Johnson, who created Spring, made a version of this argument with [Embabel](https://thenewstack.io/meet-embabel-a-framework-for-building-ai-agents-with-java/?p=22790880), an open source JVM agent framework that plans toward goals using conditions declared in type-safe code. The aim, as The New Stack described it, is just enough deterministic control over how an agent makes its choices while still letting it find new routes to a goal. That balance is close to what a model risk team wants to see.

I want to be fair about the limits. New agent patterns still tend to appear in Python first, and some JVM pieces are young. Google's Java ADK shipped as version 0.1.0, while the Python version it follows is already at a stable 1.0. If you need this month's research technique, Python will get you there sooner.

## A decision rule I use

Put the agent's orchestration in the runtime that owns the transaction and the controls. Keep Python where it is genuinely the best tool: training, fine-tuning, evaluation harnesses, exploratory data science and some model serving. Connect the two through well-defined service contracts or MCP, not through shared libraries or copied logic. Before choosing, I ask four questions:

1. Which system of record will the agent write to, and which runtime owns it?
2. Where do the entitlement, masking and business rules live today?
3. Who will be on call for this service at 2 a.m., and what do they know?
4. Is the hard part of this use case the model or the integration?

The rule follows the transaction, not the language. A research assistant over public documents, an analytics copilot that never writes to a system of record, or a team whose core services are already in Python can reasonably keep the agent in Python too.

The failure mode to avoid is quiet duplication. When a Python agent layer is bolted beside a Java core, entitlement checks, data masking and business rules get reimplemented in the second language. Now you have two versions of policy that drift apart, and an auditor who asks which one ran. In my experience that duplication costs far more than any productivity gain from a familiar framework.

There is a people argument too. Large firms employ thousands of experienced JVM engineers who understand the domain, the systems of record and the failure modes. Asking them to build agents in the stack they know is faster and safer than standing up a parallel team that must learn the business from scratch. Python skills are easy to hire. Fifteen years of knowing why the settlement batch fails on month-end is not.

## A placement decision, not a language war

None of this is about which language is better. It is about where software that makes judgments should sit relative to the systems it can change. Close to the transaction, the controls are inherited. Far from it, they have to be rebuilt, and rebuilt controls are where audits find gaps. If your agents had to pass the same production readiness review as your core services, which runtime would get them through it faster?

**Bottom line:** The most prudent path to production is rarely a rewrite. Enhance the proven systems you have, with the talent you already employ, and use Python where it is genuinely the best tool.
