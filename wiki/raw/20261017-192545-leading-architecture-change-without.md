---
type: Source
title: Leading architecture change without direct authority
resource: https://muthub.org/writing/leading-without-authority.md
hash: sha256:4791348d5db3d78adee704b6bda5cd9805f268a7ffb00f5a10567e74cdfef846
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2025-07-08'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Leading architecture change without direct authority

Published 2025-07-08. Adapted from my LinkedIn comments of May 6 and June 30, 2025.

**Most architecture change in a large organization happens without anyone reporting to the architect.** That is one of the hardest parts of senior technical leadership: driving change across teams you do not own, with budgets you do not control. You lead through credibility, influence and, above all, clarity.

I have spent most of my career in that position, in insurance, agribusiness and banking. The org charts differed. The lesson did not. Authority gets you a meeting. It does not get you adoption.

## The real risk is misalignment

If standards are not practical, they will be ignored. If strategy is not tied to delivery, it will not matter. If governance is too heavy, or too light, it will be ineffective. You cannot force transformation. You earn it, one well-communicated standard, one aligned decision, one trusted relationship at a time.

The quiet failure mode is the standard that everyone agrees with and nobody follows. It passes the review board, gets published, and then sits next to a delivery reality that never changed. When I see that, I no longer blame the teams. A standard that is consistently ignored is telling you something about its cost, its clarity or its timing.

Before I publish a standard now, I ask three questions. What does it cost a team to adopt? How will they know they comply? What happens when they cannot? If I cannot answer all three, the standard is not ready, however right it is on paper.

## North Star and firefighting are one job

The constant movement between crafting the target architecture and putting out today's fires is where the real art of architecture lies. It is the daily trade-offs, the guidance given in countless meetings, and the ability to explain the why behind each choice that slowly steer the ship toward the strategic horizon.

Gregor Hohpe calls this [riding the Architect Elevator](https://architectelevator.com/), connecting the strategy "penthouse" with the technology "engine room." I would add that the fires are often where the elevator earns its keep. An outage or a failed audit is the moment when people are most willing to hear why the target architecture matters, provided you show up to help with the fire first. Do not aim for balance. Aim for integration, a rhythm that adapts to the business rather than a fixed split of your calendar.

## Credibility is a currency you spend

Influence without authority behaves like a bank balance. You build it by being right about things that matter, by helping teams hit their dates and by admitting quickly when a standard was wrong. You spend it every time you say no.

That has a practical consequence. Say no rarely, specifically and with an alternative. An architect who blocks ten things a month runs the account dry by spring, and then the one veto that really matters gets escalated around them. An architect who blocks one thing a quarter, with a clear reason and a path forward, usually gets heard.

Credibility also comes from staying close to delivery. Architects who never ship slowly lose the standing to tell others how to ship. I still build prototypes myself, not because anyone needs my code, but because it keeps my judgment honest about what a standard really costs the team that has to implement it.

Writing decisions down helps more than people expect. Michael Nygard's [architecture decision records](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) capture the context, the decision and its consequences in a page or two. When a team disagrees with a standard, a short record of why it exists turns a power struggle into a conversation about facts. And when the facts change, the same record makes it easy to supersede the decision without anyone losing face.

## Make the compliant path the easy path

The most effective technique I know has nothing to do with persuasion. Spotify described its fix for fragmented tooling as the [Golden Path](https://engineering.atspotify.com/2020/08/how-we-use-golden-paths-to-solve-fragmentation-in-our-software-ecosystem), an "opinionated and supported" way to build a service, a website or a data pipeline. Engineers could still take a different route, but they lost the same level of support. Before that, the company had what it called "rumour-driven development," where the only way to learn how to do something was to ask a colleague.

That is the model for leading without authority: do not ban the alternatives, make the preferred path so much cheaper that most teams choose it on their own. When we consolidated 360 data scientists onto one ML platform at USAA, the argument that carried the room was not a policy memo. It was model deployment dropping from eight weeks to five days.

Expect a dip before the payoff. Google's 2024 DORA findings note that a platform engineering initiative [might lead to a temporary decrease in performance](https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report) before improvements appear, and that results depend on user-centered design and developer independence. That dip is when your credibility balance gets tested. Warn people early, and the dip becomes a prediction you got right.

## When influence runs out

Sometimes influence is not enough. A team is about to take on a risk the enterprise should not carry, the conversation has gone nowhere, and the date is close. Architects without authority tend to make one of two mistakes here: they never escalate and quietly absorb the risk, or they escalate everything and become the person leaders learn to route around.

My decision rule is to escalate risks, never preferences. If the disagreement is about style, technology taste or a pattern I would have chosen differently, I let it go and record it. If it is about customer data, resilience, regulatory exposure or a cost the business has not agreed to carry, I escalate, and I say plainly which one it is.

How you escalate matters as much as whether. Tell the team first that you are going to raise it, and why. Bring their argument to the meeting as fairly as your own. Frame the decision as a choice with options and consequences, not a verdict you want rubber-stamped, and accept that a leader may knowingly choose the risk. If they do, write it down as a decision with an owner. You have done your job. Done this way, an escalation can actually add to your credibility, because teams learn that you play fair even when you lose.

## What has worked for me

- **Make the compliant path the easy path.** Reusable patterns and automated checks win more adoption than mandates.
- **Lead through the managers.** Set architecture, roadmap and standards; let the teams own how they deliver.
- **Show, don't tell.** A working prototype changes more minds than a strategy deck. That is why I build a small working reference before I write the standard, instead of only writing about the idea.
- **Measure what changed.** Adoption, review time and delivery metrics keep the conversation about outcomes rather than opinions.
- **Protect the people who adopt early.** The first team on a new standard takes the risk. Make sure they get the credit and the support.

Culture is the multiplier under all of this. DORA's research holds that ["a high-trust, generative culture predicts software delivery and organizational performance"](https://dora.dev/capabilities/generative-organizational-culture/). An architect without authority depends on that trust more than anyone, because information has to flow toward you voluntarily. If teams hide problems from architecture, you will always be designing for an organization that does not exist.

**What to do on Monday morning:**

- List your current architecture standards and mark which ones teams actually follow, then interview two teams about the most ignored one.
- Apply three tests to every standard awaiting publication: adoption cost, how teams will know they comply, and what happens when they cannot.
- Pick one standard and make the compliant path cheaper with a template, pattern or automated check rather than another memo.
- Write down your escalation rule, risks versus preferences, and share it with the delivery leaders you work with most.

The question I keep coming back to, and would ask any architect reading this: which of your current standards would teams still follow if no one were checking?

**Bottom line:** Authority is granted. Influence is earned, through clarity, practical standards and results people can see, and it is spent every time you say no, so spend it carefully.
