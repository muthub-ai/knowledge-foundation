---
type: Source
title: 'Gating AI investment: eight gates from pilot to production'
resource: https://muthub.org/playbooks/gating-ai-investment.md
hash: sha256:cefcb342869408e61e7a9b4b6b8c3ea733a983d22ceea54448584534cff3a103
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2026-10-16'
origin_kind: own-post
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Gating AI investment: eight gates from pilot to production

Reviewed 2026-10-16.

Most AI budgets in large enterprises are released the way software budgets were in 2005: a business case up front, a status report every month, and a surprise at the end. AI rewards a different pattern. Release money in small amounts against evidence, and stop early when the evidence does not come.

These eight gates are the ones I would hold any AI use case to. Each has a single question and a check you can verify without a slide deck.

## 1. The problem and its baseline

Start with the process as it is today: how long it takes, what it costs, how often it goes wrong. Without a baseline, every pilot looks like a success.

Check: The current process is measured on the metric the use case claims to improve.

## 2. A value hypothesis with a number

State the expected change and what it is worth: hours saved per case, error rate reduced, revenue per offer. Write down the result that would make you stop.

Check: There is a target, a dollar value and a stop threshold, agreed by the business owner.

## 3. Data rights and readiness

Confirm the data exists, is good enough, and is allowed to be used for this purpose. Many promising pilots die here, which is the cheapest place for them to die.

Check: Data owners have approved the use, and a sample has passed a quality check.

## 4. Risk tier and controls

Assign the risk tier and the controls that come with it before building anything, using a shared framework such as the [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework). Controls designed in are cheap; controls bolted on are expensive and late.

Check: The risk tier is recorded, and the required controls are in the backlog.

## 5. Offline evaluation passed

Before real users touch it, the system must meet agreed quality thresholds on a representative test set, including the hard and adversarial cases. [Anthropic's guidance on agent evaluations](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) covers how to build one.

Check: Evaluation results meet the thresholds set at gate two, and they are reproducible.

## 6. Pilot results against the baseline

Run with real users in a limited scope and compare against the baseline, not against expectations. Be wary of reported speed: [METR's randomized study](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) found experienced developers were slower with AI tools while believing they were faster.

Check: Measured pilot results, including cost per task, beat the baseline by the target margin.

## 7. Operational readiness

Production needs an owner on call, monitoring for quality drift, a rollback path and a kill switch. A use case that cannot be turned off safely is not ready to be turned on.

Check: Monitoring, rollback, kill switch and an accountable owner are in place and tested.

## 8. Scale, with a sunset rule

Scale funding in steps tied to the same metrics, and set the condition under which the use case will be retired or rebuilt. [Gartner expects many agentic projects to be cancelled](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027); the ones that survive will be the ones measured honestly.

Check: Each funding step is tied to a metric, and the retirement condition is written down.

Gates feel slow on the first use case and fast on the tenth, because the evidence and the controls are already in place. Which gate does your current portfolio skip most often?
