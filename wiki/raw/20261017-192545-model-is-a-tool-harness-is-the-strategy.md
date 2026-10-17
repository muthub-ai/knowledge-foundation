---
type: Source
title: Model is a tool, harness is the strategy
resource: https://muthub.org/writing/model-is-a-tool-harness-is-the-strategy.md
hash: sha256:538f21af6b7d4c6d9c64202a9bc6773f8005e9671804e82331ff5bb5f25b5fb9
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2026-05-26'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Model is a tool, harness is the strategy

Published 2026-05-26. Adapted from my LinkedIn post of May 23, 2026.

**The best time to stop a bad commit is before it is written, not after it is deployed.** That one idea is the whole case for harness engineering, and it is why I think most enterprise AI programs are spending their attention in the wrong place.

Enterprise teams are handing AI agents the keys to production codebases. It is the equivalent of putting a teenager in a high-performance sports car with no dual brakes and no driving instructor. The car is impressive. The outcome depends almost entirely on what surrounds it.

To scale agentic AI safely in the software lifecycle, we need to shift attention from model selection to the harness: the context, constraints and checks that surround the model. A good harness does more than monitor an agent. It governs it, with two mechanisms that should be deterministic wherever possible.

## The industry is converging on the same vocabulary

This is no longer a niche view. Birgitta Böckeler at Thoughtworks wrote in February 2026 that a harness is the ["tooling and practices" that keep AI agents in check](https://www.martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html), and she frames its elements as *guides* and *sensors*, each either computational or inferential. That maps closely to how I have been describing it: guardrails that shape what the agent does, and sensors that catch what it got wrong.

Anthropic's engineering team arrived at similar conclusions from the builder's side. In their write-up on [harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), the agent works on one feature at a time against a JSON feature list where every item starts as failing, and the prompt states, "It is unacceptable to remove or edit tests." They also report that the model often marked features complete without verifying them end to end. Read that twice. The model was capable. Without a sensor, it was also overconfident.

## Guardrails: the lanes on the road

Before an agent writes a single line, the harness constrains it. It decides which tools the agent can call, which data it can see, which patterns it must follow and which standards apply. With Architecture-as-Code, those constraints come from a machine-readable source rather than a wiki page the agent never reads.

The OWASP guidance on [excessive agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) is the best checklist I know for this layer. It traces the risk to three root causes (excessive functionality, excessive permissions and excessive autonomy) and recommends enforcing authorization in downstream systems "rather than relying on an LLM to decide" whether an action is allowed. That last point is the one teams skip. A prompt that says "never touch production data" is a request. A credential that cannot reach production data is a guardrail.

## Sensors: the automated brakes

When an agent does make a mistake, sensors react immediately. Linters, type checkers, schema validators, policy checks and tests catch the error, reject the change and hand the failure back so the agent can correct itself. Human engineers should not spend their attention debugging an agent's basic failures.

Here is where I part ways with some of the current enthusiasm. It is tempting to use a second model as the sensor for the first: an LLM reviewer judging LLM output. That has a place for questions of style and design intent. For anything with a right answer (does this call an unapproved service, does this table hold customer data, does this test still pass) use a deterministic check. An inferential sensor that is right most of the time is a second source of error when it matters. Anthropic's own [guide to building agents](https://www.anthropic.com/engineering/building-effective-agents) warns that autonomy brings "the potential for compounding errors" and recommends sandboxed testing with appropriate guardrails. Stacking probabilistic judges does not remove that risk. Deterministic sensors bound it.

> Model is a tool. Harness is the strategy.

## Why the model is the least durable part

Models change every few months, and the right model for a task today will not be the right one next year. The context you give agents, the policies they must satisfy and the checks they must pass are what stay. Separate what the model infers from what the system actually permits, and a model upgrade never breaks your controls.

This has a budget implication many leaders miss. Money spent on a model evaluation depreciates on the vendor's release cycle. Money spent on the harness compounds: every new standard, test and policy improves every agent and every future model. When I review an AI program, I ask what share of the effort goes into the harness versus model selection and prompt tuning. In the programs that struggle, the harness share is usually small.

## How harnesses fail

Harnesses fail in predictable ways, and almost none of them involve the model getting dumber. The first is the agent that can edit its own sensors. If an agent can modify the test, loosen the lint rule or add an ignore comment, a determined optimizer will eventually do exactly that to make the build go green. That is why the instruction in Anthropic's harness about never removing or editing tests matters so much, and why I would not rely on the instruction alone. Sensor configuration should sit outside the agent's write permissions, and any change to it should need a human approval.

The second is the flaky sensor. A check that fails randomly teaches agents and engineers the same lesson: retry until it passes. Within weeks nobody treats a failure as information. One flaky check can do more damage to a harness than a missing one, so I quarantine unreliable checks quickly rather than leave them running.

The third is the harness that is too tight. When every change trips a dozen rules, developers stop using the agent or quietly turn the harness off for their repository. The fix is to measure both directions: how often sensors catch real problems, and how often they block work that was fine.

## Who owns the harness

In large regulated enterprises, the instinct is to let each team configure its own agent. That produces hundreds of slightly different harnesses, each with its own gaps. Böckeler's memo points at a better model, harness templates that share common guides and sensors across an organization. I would go further and treat the harness as a platform product, with an owner, a backlog, tests of its own and a release process.

The platform team owns the shared guardrails and sensors. Product teams add local rules on top and can tighten them but not loosen them. Risk and architecture define the policies as code. Everyone gets the same baseline, and an auditor can inspect one harness instead of hundreds.

The most useful early metric is the sensor rejection rate by rule. When one rule rejects agent output constantly, either the agent lacks context about that standard or the standard is unclear. Both are fixable, and both are invisible if you only measure how much code the agents produce.

## Building the track first

A practical order of work: first restrict what agents can reach, then give them the approved patterns and standards as context, then add deterministic checks to the pipeline, and only then widen their autonomy. Each step earns the right to the next. Teams that start with autonomy and add controls later spend months cleaning up what the agent already merged.

**What to do on Monday morning:**

- Inventory the tools, credentials and data every coding agent in your organization can reach today, and remove anything that exceeds its current task.
- Move test files, lint configuration and policy rules outside agent write permissions so any change to a sensor requires human approval.
- Start reporting sensor rejection rate by rule for agent-generated changes, and review the top three offending rules with their owners.
- Assign a single platform owner for shared agent guardrails and sensors, with a backlog that product teams can submit rules to.

Code fast, verify hard, and keep the humans in the loop. Where in your delivery pipeline would a deterministic sensor have caught the last serious mistake an agent made?

**Bottom line:** Most teams are racing to deploy agents. The teams that win are building the track first: guardrails from machine-readable standards, deterministic sensors in the pipeline, and a harness owned as a platform that outlives any single model.
