---
type: Source
title: The cost of unmanaged context
resource: https://muthub.org/writing/the-cost-of-unmanaged-context.md
hash: sha256:ad99d3b15f1fc20892f50347fc159b67a2f61f92d839ac3feebd93b499ee6c20
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2026-06-02'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# The cost of unmanaged context

Published 2026-06-02. Part 1 of the Context Engineering series.

**Unmanaged context is the most expensive line item in enterprise technology, and almost nobody tracks it.** Every enterprise I know can tell you what it spends on cloud, on model APIs and on software licenses. Very few can tell you what it spends on context: the knowledge a person or an agent needs before they can do anything useful. What does this application depend on? Why was it built this way? Who owns it? What broke last time, and how was it fixed?

That knowledge is real and it is expensive to rebuild. In most organizations it is also completely unmanaged. For years we paid for it quietly, through meetings, chat threads and the patience of senior engineers. AI changes the math. Agents consume context at machine speed, and they amplify whatever quality of context they are given. Unmanaged context used to be an inefficiency. Now it is a risk.

## The cost we already pay

The human cost is well documented. Panopto's workplace knowledge study found that knowledge workers spend [5.3 hours a week](https://www.hrdive.com/news/inefficient-knowledge-sharing-costs-large-us-businesses-47m-a-year/527892/) waiting for information from colleagues or recreating information that already exists, and that 42% of institutional knowledge is unique to the person who holds it. Atlassian's State of Teams 2025 put the waste at [2.4 billion hours a year](https://petri.com/inefficient-information-management-costing-businesses/) spent searching for information, and half of the workers surveyed said poor communication had teams duplicating work.

Inside a technology organization the pattern is familiar. Every incident starts with the same scramble to rediscover dependencies. Every risk assessment re-interviews the same experts. Every modernization program opens with months of archaeology. Every new engineer spends a quarter learning things that someone, somewhere, already knew.

We never book any of this as a cost. We call it onboarding, or due diligence, or an incident bridge. Because the spending has friendly names, it never appears in a business case, and nobody is ever asked to reduce it.

## Why AI multiplies it

Models are remarkable at reasoning over what is in front of them and helpless about what is not. Anthropic describes context as [a critical but finite resource](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) and warns of *context rot*: as the token count grows, the model's ability to recall and use what is in the window declines. Thoughtworks' Birgitta Böckeler makes the same point for coding agents: [an agent's effectiveness goes down](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html) when it gets too much context, and the extra context costs money too.

So the naive answer, give the agent everything, fails twice: it costs more and it performs worse. The opposite failure is just as common. MIT's NANDA research on enterprise generative AI reported that only about [5% of integrated pilots](https://www.zirous.com/insights/a-clearer-view-of-mits-genai-data-what-95-of-genai-projects-fail-really-means/) were generating real value, and the diagnosis that stuck with me was the learning gap: tools that do not retain context, do not adapt to the workflow, and make people supply the same background again and again.

Here is the point I think most AI business cases miss. The marginal cost of a new agent is rarely the license. It is the context that agent has to assemble before it is useful. If every agent starts from zero, your context bill grows in step with your AI ambition.

## Four hidden line items

1. **Rediscovery.** People and agents rebuild the same understanding for every incident, change, audit and project. This cost scales with every agent you deploy, because each one starts from nothing.
2. **Inconsistency.** Two teams, or two agents, give different answers to the same question because they assembled context from different fragments. In a regulated business, an inconsistent answer is an audit finding waiting to be written.
3. **Decay.** Context that was right last year and is wrong today. A stale runbook, or a page describing a retired system, is worse than no documentation, because people trust it.
4. **Departure.** Knowledge that leaves with people. Every reorganization and every retirement is an unplanned deletion of institutional memory.

## A familiar night

A payments service starts degrading at two in the morning. The on-call engineer has never touched it. The first forty minutes go to questions rather than fixes: which upstream systems feed it, what changed this week, whether this has happened before, who owns the database underneath it.

The answers exist. They sit in a ticket from last spring, a post-mortem nobody linked, a configuration record with the wrong owner and the memory of a senior engineer who is asleep. Eventually the right person is paged, recognizes the pattern in two minutes and applies the fix they applied last time. In the large regulated banks I have worked in, I have watched some version of this scene more often than I can count.

Nothing in that story shows up in a budget, yet the cost is real: minutes of customer impact, hours of senior attention, and a lesson that will be relearned next time because it still lives in one head. Put an AI agent on that bridge without curated context and very little changes. It searches the same fragments faster, and it is confidently wrong about which ones matter.

## Why this is a leadership problem

Unmanaged context persists because nobody owns it. Data has chief data officers, code has engineering leaders, infrastructure has platform teams. Context, the connective tissue between all of them, has no budget line and no accountable executive. It is everyone's problem and no one's job, which is exactly how valuable things decay.

That is why I treat context as an asset class rather than a tooling choice. Assets get owners, investment cases, quality measures and lifecycle management. Tools get bought, piloted and abandoned. Treat the context your agents depend on as a tool and you will rebuild it for every use case. Treat it as an asset and every use case makes it richer.

## What stays yours when the models change

Models are becoming interchangeable. This year's frontier model is next year's commodity, and most large organizations already run several. What does not commoditize is the context those models reason over: how your systems connect, why decisions were made, what your policies require, what has gone wrong before. No vendor can sell you that, and when it is maintained it compounds. I would spend scarce architecture attention there before spending it on the next model evaluation.

I learned a version of this on data platforms. When we consolidated 360 data scientists onto one ML platform at USAA, shared infrastructure paid off only when shared definitions and clear ownership came with it. Context for agents follows the same rule.

Analysts are arriving at the same place. Gartner expects context engineering features to be built into [80% of the software tools used to build AI applications by 2028](https://atlan.com/know/gartner-context-graphs/), and Foundation Capital argues that the next great enterprise platforms will be [systems of record for decisions](https://ashugarg.substack.com/p/ais-trillion-dollar-opportunity-context), keeping the decision traces that today's systems simply throw away.

## What managed context looks like

- **Owned.** Every piece of context has an accountable owner, just like code and data.
- **Fresh.** It carries a verified date and a review-by date, so agents can tell when it has expired.
- **Traceable.** You can see where it came from and who checked it.
- **Governed.** Access, classification and retention follow the same rules as the systems it describes.
- **Reusable.** Built once and used by every person and agent, instead of reassembled per use case.

None of this needs a moonshot. It needs context to be run as a product with an owner and a lifecycle, rather than left as a by-product of people talking to each other.

## Start by measuring it

You cannot manage what you do not count. Pick one workflow, such as incident triage or change approval, and measure how long it takes to assemble the context before any real work starts. Count how many people get pulled in to answer the same questions. That number is your cost of unmanaged context, and in my experience it is large enough to fund the fix.

**What to do on Monday morning:**

- Time the first hour of your next major incident and record how many minutes go to assembling context before anyone attempts a fix.
- Name one accountable **owner** for the context of your most critical application, with a review-by date attached.
- Add a context-assembly cost line to the business case template for every new AI agent proposal.
- Ask your architects to list the five questions engineers repeatedly ask about one tier-one service, and where each answer lives today.

If you timed the first hour of your next major incident, how much of it would go to rediscovering something your organization already knew?

**Bottom line:** Context is the asset AI runs on, and most enterprises leave it unmanaged. Build it once, govern it once, and let every model you adopt reuse it. The rest of this series covers how.
