---
type: Source
title: 'Architecture that runs: why AI-era governance must be code'
resource: https://muthub.org/writing/architecture-that-runs.md
hash: sha256:8e6e57c59172d9416ae75c7cb89105d17718fe64c049d266f871f0d5161cc1af
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2026-05-12'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Architecture that runs: why AI-era governance must be code

Published 2026-05-12. Adapted from my LinkedIn posts of May 2 and May 10, 2026.

**If AI is writing your code, your architecture has to become something that runs.** We gave engineers assistants that produce code far faster than any review board can read it, and we kept architecture moving at human speed. That mismatch is quietly breaking the software lifecycle.

AI coding agents do not *understand* your enterprise. They optimize for finishing the task in front of them. Without guardrails they produce code that violates policy, integrations that bypass approved patterns, and data flows that should not exist. At scale, that is not productivity. It is automated technical debt, and it arrives later as higher run cost and clogged release pipelines.

## The evidence points the same way

This is not a hypothetical worry. Google's 2024 DORA research found that as AI adoption increased, it was accompanied by [an estimated 1.5% decrease in delivery throughput and a 7.2% reduction in delivery stability](https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report). The same study saw gains in documentation quality, code quality and code review speed. Individuals got faster. The delivery system got shakier.

The [2025 DORA report](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) moved the picture forward without changing its shape: AI adoption now related positively to delivery throughput but still negatively to stability. I agree with the report's explanation. Acceleration exposes weaknesses downstream, and without controls such as automated testing and fast feedback loops, more change means more instability. I would add one control that most enterprises have never automated, which is architectural conformance. We test whether code works. We rarely test whether it belongs.

## Architecture is still treated as documentation

For most of my career, architecture governance has meant documents, diagrams and review boards. Architecture was something you read, not something that runs. That model was slow but survivable when software changed a few times a quarter. It is obsolete now.

Michael Nygard named the root problem in 2011 when he proposed architecture decision records: ["Large documents are never kept up to date."](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) He was describing human teams. An agent that commits dozens of times a day widens the gap between the document and the code faster than any architect can close it.

In the large regulated banks I have worked in, the architecture review board was usually the most experienced room in the building and also one of the slowest steps in delivery. That was nobody's fault. The board was being asked to do by reading what should have been done by execution.

> Architecture is not what you say you'll build; it's what you actually allow into production.

## What changes when architecture is machine-readable

To make the shift concrete, I built a public prototype at [aac.muthub.org](https://aac.muthub.org). Five things change when architecture is machine-readable and version-controlled:

1. **The plan becomes executable.** Architecture lives in structured formats (YAML or JSON with a small vocabulary), not slide diagrams, and becomes a real source of truth with an owner and a history.
2. **Code becomes guided.** AI agents pull approved patterns through a machine-readable context layer, so they generate compliant code by design instead of by luck.
3. **Reviews become deterministic.** Policy-as-code enforces standards in CI/CD and replaces subjective manual review for the questions that have a right answer.
4. **Operations become measurable.** Because the architecture is data, risk exposure, cost and technical debt become queries rather than quarterly slide exercises.
5. **Drift becomes visible, and fixable.** What is running is continuously compared with what was designed, so divergence cannot hide until an audit finds it.

None of these ideas is new on its own. The Thoughtworks Technology Radar put architectural fitness functions in Trial back in 2017, describing a way to ["communicate, validate and preserve architectural characteristics in an automated, continual manner"](https://www.thoughtworks.com/radar/techniques/architectural-fitness-function). What has changed is the audience. The consumer of the rule is now an agent as well as a pipeline.

## Policy without enforcement is a suggestion

The enforcement layer already exists. [Open Policy Agent](https://www.openpolicyagent.org/docs) is built on the idea that it "decouples policy decision-making from policy enforcement." In practice that means the architecture team owns the rule, the platform team owns the gate, and neither has to rewrite the other's code when a standard changes.

The delivery channel matters as much as the rules. The Model Context Protocol gives coding assistants an open, standard way to reach external systems, so an assistant can query the architecture repository and validate its own output before anything is committed. That is how architectural control scales across thousands of developers: governance in the terminal, where the code is written, instead of in a meeting two weeks later.

## Where I disagree with the usual advice

The common advice is to start with policy-as-code gates in CI. I think that is the wrong first move. Gates alone turn the architecture function into a red light that agents hit after the work is done. Every rejection costs a full cycle, and teams quickly learn to route around the gate. Give agents the approved patterns and schemas first, then add the gate to catch what the context missed. Prevention at generation time is far cheaper than rejection at merge time.

The second trade-off is how much to encode. Not every architectural judgment belongs in Rego. My decision rule is simple: if two senior architects would reach the same answer from the same facts, encode it. If they would argue, keep it a human decision and record it as an ADR. Over time the arguments settle and become rules. Programs that try to encode everything on day one stall in policy debates and never ship a single check.

The third is exceptions. A policy engine without a formal waiver process gets switched off within a quarter, usually by someone senior under deadline pressure. Treat every exception as a record with an owner, a risk rating and an expiry date, and the engine stays on.

## One rule, followed end to end

It helps to watch a single rule travel through the whole system. Take a standard most banks already have on paper: every new data store must declare the classification of the data it holds, and anything holding customer data must be encrypted with managed keys.

In the document world, that rule lives in a standards page. An engineer may or may not read it, a reviewer may or may not catch the gap, and an auditor finds the unencrypted bucket eighteen months later. In the executable world, the rule exists once, as data. The agent's context layer serves the approved storage pattern with the classification field already in the template, so the first draft is usually right. The pipeline check rejects any store that has no classification or the wrong key type, and it says exactly which field failed. If a team genuinely cannot comply yet, it files a waiver with an owner and an expiry, and the check honors it until that date.

Notice what the architect did not do: attend a meeting, read a diff or chase a team by email. The architect's work moved upstream into writing the rule well and deciding what counts as an acceptable exception. That is a better use of the most experienced people in the building, and in my experience it is also the part of the job they enjoy most.

## The outer loop is where the next gains are

Last year's gains came from the developer's inner loop: writing, completing and explaining code. This year's will come from automating the outer loop, where review, compliance and release still wait in queues. That is where Architecture-as-Code pays for itself.

I have seen this pattern before. When we consolidated 360 data scientists onto one governed ML platform at USAA, model deployment went from eight weeks to five days. The lesson I took was that the speed came from building the controls into the platform rather than stacking them in front of it. Agents will follow the same rule. The organizations that encode their architecture will let agents move quickly inside it, and the ones that keep it in documents will keep slowing everything down to read.

**What to do on Monday morning:**

- Pick **five** architecture standards where two senior architects would always agree, and assign an owner to rewrite each as a machine-readable rule.
- Choose one standard, such as data classification on new data stores, and run it as a non-blocking pipeline check for one product line to measure violations.
- Expose your approved patterns to coding assistants through one read-only context endpoint before adding any new merge gate.
- Stand up a waiver register where every exception has a named owner, a risk rating and an expiry date, and move existing exceptions into it.

So here is the question I would put to any CIO or chief architect: which of your architecture standards could an AI agent check for itself today, before it writes a line of code?

**Bottom line:** If AI is writing your code, your architecture cannot stay passive. It has to become the system the AI listens to, with rules that run in the agent's context and in the pipeline, and exceptions that are owned and dated.
