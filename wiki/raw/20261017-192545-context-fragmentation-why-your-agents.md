---
type: Source
title: 'Context fragmentation: why your agents keep starting from zero'
resource: https://muthub.org/writing/context-fragmentation.md
hash: sha256:5d16a5885890e473898a6622d4771193c0d20a6bd383d17d6aa7a1d6327dd4e5
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2026-06-30'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Context fragmentation: why your agents keep starting from zero

Published 2026-06-30. Part 2 of the Context Engineering series.

**Your agents are brittle because your context is in pieces, and a better model will not fix that.** Ask a simple question about almost any enterprise application: *what breaks if this goes down?* The answer exists. It is just in eight places. Some of it is in the code, some in the configuration database, some in last year's incident tickets, some in an architecture diagram nobody has opened since it was approved, some in a chat thread, and the most important part is in the head of an engineer who is on vacation.

That is context fragmentation. Each fragment is accurate on its own terms, and none of them answers the question. Every person or agent who needs the answer has to reassemble it from scratch, every time.

## Where context lives today

- **Code and pipelines** tell you *what* the system does, never *why*.
- **Tickets and backlogs** hold intent and decisions, buried in comment threads.
- **Incident and change records** hold failure modes and fixes, written under pressure and rarely revisited.
- **Configuration databases and catalogs** hold relationships, often incomplete or out of date.
- **Wikis and architecture documents** hold the design as approved, not as built.
- **Chat and meetings** hold the real reasoning, and then lose it.
- **People** hold everything else.

Atlassian's State of Teams research found that executives and teams spend [a quarter of their workweek](https://petri.com/inefficient-information-management-costing-businesses/) just trying to find relevant data. Humans at least have colleagues to ask and instincts about which source to distrust. An agent has neither.

## Why agents feel it first

A human expert carries an internal map: which wiki pages are stale, which team really owns a service, which dashboard to ignore. An agent has only what it retrieves. Give it fragments and it will stitch them into an answer that is plausible, consistent with each source, and wrong. The failure is quiet, which makes it worse than an error message.

Google's announcement of the Open Knowledge Format named the problem directly: knowledge sits in [metadata catalogs, wikis, code comments and the heads of a few senior engineers](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing), and every agent builder ends up solving the same context-assembly problem from scratch. In a large enterprise that duplication happens inside one company. Every team building an assistant writes its own connectors, its own retrieval and its own prompts over the same scattered sources.

## Three symptoms you will recognize

1. **Every AI use case rebuilds the same plumbing.** The incident assistant, the coding agent and the risk chatbot each connect to the same systems in slightly different ways, and each needs its own security review.
2. **Agents disagree with each other.** Two assistants give different answers about the same application because they retrieved different fragments. Trust collapses the first time a senior leader notices.
3. **Fixes do not stick.** Someone corrects a wrong answer in one tool, and the other tools never learn. The knowledge was corrected, but only in one fragment.

## Why more retrieval is not the answer

The instinctive fix is a bigger index: connect everything, embed everything, let the agent search. It helps at first. But retrieval over fragments returns fragments. It does not decide which source is authoritative, which version is current, or how two facts relate. And because of [context rot](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), pushing more raw material into the window often makes the answer worse.

This is where I part ways with much of the common advice. Search quality is rarely the binding constraint. The binding constraint is that nobody has done the synthesis, so every query pays for it again, at inference time, with no memory of the last attempt.

Andrej Karpathy's *LLM wiki* idea points somewhere better. Instead of re-deriving answers from raw sources on every query, the model [compiles knowledge once](https://noqta.tn/en/blog/karpathy-llm-wiki-knowledge-base-beyond-rag-2026) into maintained, linked pages and answers from those. Synthesis is done once, kept current and reused.

## From fragments to one coherent unit

The organizing idea I keep returning to is simple: **give every application one coherent, governed body of context**, assembled from the fragments, owned by the team that runs it, and readable by people and agents alike. It is a curated layer, not a new system of record, and for each application it answers the same things: what it does, why it exists, what it depends on, what depends on it, how it fails, how it is secured and who to call.

Once that unit exists, agents stop starting from zero. The incident assistant, the coding agent and the architecture reviewer all read the same context. A correction made once is a correction everywhere. The question *what breaks if this goes down?* becomes a lookup and a traversal instead of an investigation.

In my experience a useful outline covers a handful of areas, the same way, for every application:

- **Purpose:** the business capability it serves and who depends on it.
- **Architecture:** components, data flows and the patterns it follows.
- **Dependencies in both directions:** what it calls and what calls it, so blast radius can be traced.
- **Security and data handling:** classification, identities, controls and exceptions.
- **Resiliency and failure modes:** how it fails, how it recovers and what happened last time.
- **Operations:** runbooks, on-call ownership and recent changes.
- **Decisions:** the key trade-offs and why they were made.

The outline matters as much as the content. When every application follows the same structure, an agent can move through any of them the same way, reading a short index first and opening detail only when needed. Anthropic describes this as [progressive disclosure](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): letting an agent discover context layer by layer instead of loading everything up front.

## Why regulated industries feel it more

In a bank or an insurer, fragmentation is also a control problem. When an examiner asks how a critical application depends on its upstream systems, or why a risk was accepted, the organization needs one answer with evidence. Fragmented context produces several answers, assembled by different people under time pressure. Consistency is a control, and fragmentation makes it impossible to demonstrate.

AI governance raises the stakes. If an agent recommends an action, you need to show what it knew and where that knowledge came from. That is only practical when context lives in one governed place with clear provenance, rather than in whatever an agent happened to retrieve that afternoon.

## Who funds the fix

Fixing fragmentation pays off on both sides of the ledger, and that is its quiet advantage in a budget conversation. Product teams change systems faster, reuse architecture instead of rediscovering it, and make portfolio decisions with a clear view of what depends on what. Incident responders trace blast radius in minutes, root-cause analysis rests on evidence rather than memory, and risk teams see exposure without commissioning a study. It is one of the rare investments that a technology leader and a risk leader will fund together, which in my experience is the best predictor that it survives the next budget cycle.

## What to do first

- **Map one critical workflow.** List every source a person consults to triage an incident or approve a change. That list is your fragmentation map.
- **Pick the unit.** For most technology organizations it is the application or service. Define what a complete body of context for one looks like.
- **Name an owner.** Context without an owner fragments again within a quarter.
- **Serve it once.** Expose it through one governed interface, for example an MCP server, so every agent uses the same context instead of building its own.

**What to do on Monday morning:**

- Ask two of your AI assistants the same dependency question about one critical application and put their answers side by side.
- Inventory the connectors your teams built this year to the configuration database, ticketing and code systems, and flag the duplicates.
- Route the next correction to a wrong agent answer back to its source, then check whether every other assistant now reflects the fix.

If you counted the connectors your teams have built to the same five systems this year, how many separate copies of the truth would you find?

**Bottom line:** Your agents are not failing because the models are weak. They are failing because the context is in pieces. Fix fragmentation once, at the level of the application, and every agent you deploy inherits the fix.
