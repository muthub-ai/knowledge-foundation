---
type: Source
title: 'From MLOps to AI engineering: what industrializing ML still teaches us'
resource: https://muthub.org/writing/from-mlops-to-ai-engineering.md
hash: sha256:5f8a3cb0e3f5f32b1104c93b9c12777598e34e777caebe10070ff8f8b436820a
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2024-11-19'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# From MLOps to AI engineering: what industrializing ML still teaches us

Published 2024-11-19. Adapted from my Medium article "The Rise of MLOps" (2021) and my LinkedIn post of November 14, 2024.

**A trained model is the start of the work, and the discipline that gets it safely into production matters more than the model itself.** In 2021 I wrote that MLOps was not a buzzword but a necessary discipline. Without a systematic approach, machine learning projects stall at proof of concept, or degrade quietly as live data drifts away from the data the model learned from.

Three years later, generative AI has widened the scope, the first agentic systems are widening it again, and much of the industry is rediscovering those lessons under new names. I think the discipline now deserves a broader name, AI engineering, but the core ideas have changed less than the marketing suggests.

## Why ML was never just software

The clearest statement of the problem is still [Hidden Technical Debt in Machine Learning Systems](https://proceedings.neurips.cc/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf), the 2015 NeurIPS paper by D. Sculley and colleagues at Google. Its famous diagram shows the model code as a small box surrounded by data collection, feature extraction, configuration, serving and monitoring. The paper names risks every platform team eventually meets: entanglement, hidden feedback loops, undeclared consumers and data dependencies. Its shorthand, *Changing Anything Changes Everything*, is the best one-line description of ML in production I know.

Three differences from ordinary software drove everything we built:

- **More than code.** Software lifecycles center on code. Machine learning also depends on data and models, which are harder to version and harder to diff.
- **Experimental by nature.** Development is a series of experiments that must be tracked to be reproducible.
- **Never finished.** After deployment, models need monitoring for drift and periodic retraining as well as bug fixes.

## The lifecycle we industrialized

The lifecycle itself is familiar: data ingestion and preparation, feature engineering, training and tuning, evaluation against held-out data, deployment in the mode the use case needs (batch or real-time), then continuous monitoring with automated retraining when performance drops. In regulated industries you add lineage and audit trails across data, code and model artifacts.

At USAA we consolidated 360 data scientists onto one ML platform and cut model deployment from 8 weeks to 5 days. People assume the gain came from automation. Automation helped, but in my view the bigger shift was that model risk teams could validate models on the same platform data scientists built them on, using the same lineage and evidence. Validation stopped being a separate project that reassembled the facts afterwards. When evidence is a by-product of the pipeline, review gets faster and better at the same time.

## What carries over to generative AI

Teams adopting foundation models sometimes conclude that MLOps no longer applies because they do not train the model. I disagree. You may not own the weights, but you own almost everything else: prompts, retrieval corpora, tool definitions, guardrails, evaluation sets and the routing logic between models. Each is a versioned artifact that changes behavior, and each needs the lineage we built for features and models.

The practical shift is that evaluation becomes the regression suite. In classical ML, a held-out dataset told you whether a retrained model was safe to promote. For generative systems the equivalent is a curated set of questions, expected behaviors and adversarial prompts, run automatically on every change to a prompt, a corpus or a model version. Teams that skip this are deploying on instinct. Teams that build it find that model upgrades, which used to be nerve-wracking, become routine.

Sculley's risks map almost one to one. Data dependencies become the document corpus behind retrieval, which drifts every time someone edits a policy page. Undeclared consumers become LLM applications and agents wired to your APIs through function calling. Hidden feedback loops appear when AI-generated content flows back into the knowledge base the next answer draws from. And drift now includes a provider updating a model version underneath you, which can change behavior without a single line of your code changing.

## What does not carry over

The analogy has limits, and teams that miss them get hurt. The first is determinism. A classical model given the same input returns the same score. A generative system can answer the same question differently on consecutive runs, so a single pass of your evaluation set proves less than it seems. The [τ-bench paper](https://arxiv.org/abs/2406.12045), published in June 2024, makes the point well: it proposes a pass^k metric that asks whether an agent succeeds on every one of k repeated trials, not just once, and reports that even state-of-the-art function-calling agents failed most of its tasks and were inconsistent across runs. For a customer-facing system in a bank, succeeding every time is the measure that matters.

The second is grading. Held-out data came with labels. Many generative outputs have no single right answer, so teams use one model to grade another. That is workable, and [research on LLM-as-a-judge](https://arxiv.org/abs/2306.05685) found strong models agreeing with human preferences about as often as humans agree with each other, while also documenting position and verbosity biases. But the grader is now a model in production too, and it needs the same calibration against human experts that we demanded of any other model before we trusted its scores, plus an explicit way to say it does not know.

The third is cost. A classical model's inference cost was close to fixed. An agent that decides how many steps to take can make the same task many times more expensive on a bad day, so cost per task belongs on the monitoring dashboard next to accuracy and drift. Model risk teams that treat these three as footnotes will approve systems whose behavior they have only sampled once.

## From MLOps to AI engineering

That is why I see AI engineering as one discipline that unifies DataOps, MLOps and DevOps pipelines across hybrid, multi-cloud and edge delivery, and across streaming and batch operations. Splitting them is what produces the gaps: a data team that changes a source without knowing which agent depends on it, or an application team that ships a prompt change without the evaluations an ML team would insist on.

The research points the same way. [DORA's 2024 report](https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report) found that a 25% increase in AI adoption was associated with better documentation and code quality, but also with an estimated 7.2% reduction in delivery stability. My reading is that AI speeds up change without supplying the discipline to absorb it, and that discipline lives in the pipelines and the data underneath them. That is a DataOps finding as much as an AI one. When we moved hundreds of data scientists onto one governed platform, the hardest conversations were rarely about tools. They were about who owned a feature definition when three models depended on it.

Responsible design has to run through the whole lifecycle rather than being added at the end. The [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework), released in January 2023, organizes the work as govern, map, measure and manage, and NIST added a Generative AI Profile in July 2024. The value of a framework like this is less the vocabulary than the expectation that risk work happens continuously, alongside the build.

The cost of skipping this is already visible. In July 2024, [Gartner predicted that at least 30% of generative AI projects will be abandoned after proof of concept by the end of 2025](https://www.gartner.com/en/newsroom/press-releases/2024-07-29-gartner-predicts-30-percent-of-generative-ai-projects-will-be-abandoned-after-proof-of-concept-by-end-of-2025), citing poor data quality, inadequate risk controls, escalating costs or unclear business value. Those are the same reasons ML projects stalled at proof of concept a decade ago. The technology changed. The failure pattern did not.

## The head start nobody talks about

**What to do on Monday morning:**

- Inventory the prompts, retrieval corpora and tool definitions behind your most important generative use case and put each under version control.
- Build an evaluation set of fifty real questions for that use case and run it automatically on every prompt or model change.
- Add cost per task and a provider model-version alert to the monitoring dashboard of each production generative AI application.
- Give your model risk team access to evaluation results on the same platform where builders see them.

Firms that built real MLOps platforms have an advantage they may not recognize. Lineage, evaluation, monitoring and shared evidence with risk partners are exactly what generative and agentic systems need, and those capabilities take years to build and earn trust. Firms that skipped that work are about to pay for it twice, once for the models they already run and again for the agents they are about to deploy. If a provider changed the model under your most important AI use case tonight, how quickly would you know?

**Bottom line:** The lessons of MLOps still hold for generative and agentic AI: industrialize the path to production, measure what happens after launch, and give risk teams the same evidence the builders have.
