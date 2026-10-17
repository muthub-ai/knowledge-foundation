---
type: Source
title: 'An AI operating model for a bank: ten decisions to make before the twentieth
  use case'
resource: https://muthub.org/playbooks/ai-operating-model-for-a-bank.md
hash: sha256:ab74ec11f6698c642c7fa3f1b5cca902510342d0459280a58a5a369bd37f5914
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2026-10-16'
origin_kind: own-post
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# An AI operating model for a bank: ten decisions to make before the twentieth use case

Reviewed 2026-10-16.

The first three AI use cases in a bank rarely fail for technical reasons. They succeed on the energy of a few people. The trouble starts around the tenth and twentieth, when every team builds its own gateway, its own evaluation and its own approval path, and nobody can say what the portfolio is worth.

An operating model is the set of decisions that stops that from happening. These are the ten I would want settled before a bank scales, written so a CIO, a chief risk officer and a head of AI can agree on them in one meeting.

## 1. Name one accountable leader and a federated model

Put one executive in charge of the AI portfolio, platform and standards, and let lines of business own their use cases and outcomes. A pure central team becomes a bottleneck; pure federation produces twenty platforms. Hub and spoke is boring and it works.

Check: One person can answer for the whole portfolio, and every use case has a named business owner.

## 2. Run a portfolio, not a pile of pilots

Every use case enters through one intake with a problem statement, a baseline, a value hypothesis and kill criteria. Review the portfolio quarterly and stop work that is not earning its place. [Gartner expects over 40% of agentic AI projects to be cancelled by the end of 2027](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027); a bank should cancel its own, early and on purpose.

Check: There is one list of AI use cases, each with a baseline, a target and a stop rule.

## 3. Build the platform before the twentieth use case

The gateway, evaluation harness, curated context, observability and identity for agents should be shared services. Teams buy or build models; the platform supplies the controls. This is where the model-is-a-tool, harness-is-the-strategy idea becomes an org chart.

Check: New use cases reuse the platform's gateway, evaluation and logging instead of building their own.

## 4. Tier use cases by risk and set controls by tier

An internal drafting assistant, a customer-facing chatbot and a model that influences a credit decision are not the same risk. Define three or four tiers with proportionate controls, in the spirit of the [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework), so low-risk work moves fast and high-risk work gets the scrutiny it needs.

Check: Every use case has a risk tier, and the tier decides its controls and approvers.

## 5. Bring model risk in at design, not at launch

Second-line reviewers who first see a system the week before go-live can only say no. Give them a seat in design reviews and a standard evidence pack, so validation becomes a check of known evidence rather than an archaeology project.

Check: Model risk reviewers see each high-tier use case at design, with a standard evidence pack.

## 6. Treat evaluation as a product

Each use case needs a test set, regression evaluations that run on every change, and sampled human review in production. [Anthropic's guidance on agent evaluations](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) is a practical starting point. If you cannot measure quality, you cannot defend it to a regulator or improve it.

Check: No use case reaches production without an evaluation suite that runs automatically.

## 7. Give knowledge an owner

Agents are only as good as the context they are allowed to read. Policies, procedures and architecture decisions need owners, review dates and retirement rules. [Anthropic describes context as a finite resource](https://anthropic.com/engineering/effective-context-engineering-for-ai-agents); in a bank it is also a control surface.

Check: Every knowledge source an agent reads has an owner and a review date.

## 8. Plan for the bad day

Prompt injection, data leakage and confident wrong answers will happen. Red-team each tier against the [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/), keep a kill switch per use case, and rehearse the incident path with operations and communications before the first public launch.

Check: Every production use case has a kill switch, an incident runbook and a rehearsal date.

## 9. Invest in fluency, not only tools

Executives need enough fluency to ask the right questions; engineers need new review habits; risk partners need to read evaluation results. Training is cheap compared with a program that stalls because the people approving it do not trust what they are approving.

Check: Leaders, engineers and risk partners each have a role-specific AI curriculum.

## 10. Measure outcomes and cost per task

Report value in the terms the business already uses: cycle time, quality, losses avoided, revenue, plus cost per task. Usage counts are vanity. [DORA's research](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) shows AI amplifies the system it lands in, so measure the system, not the tool.

Check: The portfolio report shows outcomes and unit cost for each use case every quarter.

None of these decisions is technical, and that is the point: the technology is the easy part. Which of the ten has your bank not made yet?
