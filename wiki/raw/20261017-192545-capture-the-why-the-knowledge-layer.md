---
type: Source
title: 'Capture the why: the knowledge layer enterprise agents are missing'
resource: https://muthub.org/writing/capture-the-why.md
hash: sha256:c62dfbe840415ff3e8d62b46574eb04e504d798191c050e1c1026f7d4d22b3e8
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2026-07-14'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Capture the why: the knowledge layer enterprise agents are missing

Published 2026-07-14. Adapted from my LinkedIn writing on living documentation and the enterprise knowledge layer.

**The bottleneck in enterprise AI is rarely the model; it is that the organization never recorded why it does what it does.** Better models keep arriving every few months. The missing knowledge layer underneath them does not fix itself.

## Enterprise amnesia

Most enterprise AI pilots hit the same wall, and I have started calling it enterprise amnesia. An agent retrieves a little context, calls a tool and takes an action. Then the session closes. The context evaporates, the reasoning disappears, and the next agent starts from scratch, as if the organization had never faced that question before.

People suffer from the same thing, only more slowly. Michael Nygard put it well back in 2011 when he proposed [architecture decision records](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions): one of the hardest things to track over the life of a project is the motivation behind decisions. Without it, a newcomer can either accept a decision blindly or reverse it blindly, and both can do damage. An agent is a permanent newcomer. It arrives fresh in every session.

## Systems of record keep the what

Traditional systems track the *what*: files, tickets, code diffs, transactions. The *why* (the intent, the policies evaluated, the alternatives ruled out, the exception someone approved) mostly lives in meetings, chat threads and people's heads. Reading the code tells you what happens. It rarely tells you why it has to happen that way, or what breaks if you change it.

Foundation Capital gave this gap a useful name. In their essay on [context graphs](https://foundationcapital.com/context-graphs-ais-trillion-dollar-opportunity/), Jaya Gupta and Ashu Garg describe decision traces (the policy applied, the exception granted, the precedent relied on) and a context graph as a living record of decision traces stitched across entities and time so precedent becomes searchable. They also argue that data warehouses receive data after decisions are made, so they sit in the read path rather than the write path. I agree with that point more than with any market sizing. If you want the why, you have to capture it where the decision happens.

One clarification matters here, and the Foundation Capital authors make it too: a context graph is not the model's reasoning. Logging an agent's chain of thought is useful for debugging, but it records what one model said to itself in one session. The why an enterprise needs is institutional: which policy applied, who approved the exception, what precedent it followed, and what changed as a result. Those facts should be true no matter which model read them.

## Context engineering needs something to engineer

Context engineering has become a standard term, for good reason. Anthropic's engineering team defines it as [curating and maintaining the optimal set of tokens during inference](https://anthropic.com/engineering/effective-context-engineering-for-ai-agents), and argues for finding the smallest possible set of high-signal tokens for a task. They also describe agents writing structured notes to memory outside the context window so they can pick up long tasks later.

Here is the point I think gets missed. Context engineering is a retrieval and selection discipline. It can choose the best available context, but it cannot invent context the organization never captured. If the reason a control exists was never written down, no prompt, retriever or memory scheme will surface it. The enterprise knowledge layer is the supply side of context engineering, and most companies are trying to optimize demand without any supply.

## A living document that lies is worse than none

Tools that regenerate documentation from code on every commit are improving quickly, and I use them. They are still far from fully accurate, and they share a blind spot: generated from code, they describe what the code does, which is the part we already had. The why has to come from people or from capture at decision time.

A wrong living document is more dangerous than no documentation, because agents and people both treat it as a source of truth. So every piece of knowledge in the layer needs trust signals: where it came from, when it was last confirmed, who reviewed it, and whether it was written by a person or inferred by a model. Without those signals, you are scaling confident errors.

## Design choices that make knowledge durable

- **Decisions as first-class objects.** Store each decision with its evidence, the rules applied and the outcome, so decisions compound into queryable institutional memory instead of vanishing into logs.
- **Capture in flight, not after the fact.** An explanation written afterwards can sound plausible and still be wrong. Accountability means recording the state, inputs and policy checks while the decision is being made.
- **Deterministic policy gates.** Let models handle messy language, but enforce critical rules deterministically, and keep what the model inferred separate from what the system permitted.
- **Separate reasoning from durable truth.** Models change faster than enterprise architecture. Entities, relationships and decision histories should outlive any model, so an upgrade never breaks what the organization knows.

The last one is the choice I see teams regret skipping. When knowledge lives inside a particular model's fine-tuning or a particular vendor's memory feature, each model change becomes a knowledge migration. Keep the durable layer boring, open and owned by the enterprise.

## A decision trace, worked through

Take an architecture waiver, the kind every large technology organization grants every week. A team wants to run a service on a database pattern the standards do not allow, because a deadline is close and the approved option is not ready. A review board says yes, for twelve months, with conditions.

What usually survives is a ticket marked approved. What should survive is small and specific: the standard being waived and its version, the reason given, the alternatives considered and why they were rejected, the conditions attached, the named approver, the expiry date and the systems affected. That is perhaps ten fields and a paragraph. It takes the requester a few minutes if the review tool asks at the moment of approval, and it is close to impossible to reconstruct a year later.

Now consider who reads it. Eleven months on, an agent preparing a change to that service can see that the waiver is about to expire and that one of its conditions was never met. A new architect asking why the service looks different from its peers gets the answer in one lookup. An auditor sampling exceptions finds the evidence attached to the decision instead of scattered across email. One record serves three readers, which is why I think decision capture pays for itself faster than most documentation efforts.

## Where to start

Do not start with a company-wide knowledge program. Pick one decision flow that is high-stakes, exception-heavy and repeated often, such as a credit exception or an architecture waiver. Capture decision traces in the workflow itself, link them to the policies and evidence involved, and then measure one thing: can the next person or agent facing a similar case find the precedent and understand it?

In large regulated organizations I have worked in, the people who carry the why are usually a handful of senior engineers and risk partners whose calendars are already full. A knowledge layer that captures their reasoning as a by-product of the work, rather than as extra documentation, is the only version I have seen survive.

**What to do on Monday morning:**

- Pick one exception-heavy decision flow, such as architecture waivers, and list the fields a reviewer would need to understand it a year later.
- Add required rationale, approver and expiry fields to that flow's approval form so the why is recorded when the decision is made.
- Ask an agent to explain three past exceptions using only recorded material, and note what it could not find.
- Label every generated document in one repository with whether a person or a model wrote it and when it was last confirmed.

Every enterprise has decisions it keeps relitigating because nobody can find the reasoning from last time. Which decision in your organization would you capture first if you could?

**Bottom line:** If your agent cannot produce the evidence, policy version, tool actions and decision context behind a high-stakes action, you do not yet have an auditable agent. The teams that pull ahead will be the ones that build durable institutional memory, whatever model they happen to run.
