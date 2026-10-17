---
type: Source
title: 'Spec-driven development for regulated industries: audit the contract, not
  every line'
resource: https://muthub.org/writing/spec-driven-development-for-regulated-industries.md
hash: sha256:2d26c6bba833de6e131e70521e8841d8ab068166cc9bc07436daa2990b415822
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2025-10-21'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Spec-driven development for regulated industries: audit the contract, not every line

Published 2025-10-21. Adapted from my LinkedIn post of October 18, 2025.

**For complex work in regulated industries, prompt-to-code is a non-starter, and the specification has to become the contract the AI must fulfil.** Tools built around this idea have appeared quickly over the past few months, and the enthusiasm is running ahead of the evidence. The risk, unpredictability and lack of verifiability of free-form prompting are not acceptable when an examiner can ask why a system behaves the way it does.

Spec-driven development is the responsible path. The engineer's job shifts from writing boilerplate to designing precise, machine-readable specifications, and the spec becomes the single source of truth. But the idea has been oversold in places, and the regulated version of it looks different from the startup version.

## Why prompt-to-code fails the audit test

A prompt is a conversation. It is not versioned with intent, it is rarely reviewed, and the same prompt can produce different code tomorrow. When something goes wrong in production, the trail from business requirement to running code passes through a chat window nobody kept.

In the large banks I have worked in, the questions after an incident are always the same. What was this supposed to do? Who approved that? What evidence shows it does what was approved? Prompt-to-code has no good answer to any of them. A spec does, if it is written and governed properly.

There is a quieter problem too. Prompts encode decisions that nobody reviewed as decisions. A developer who types "store the customer details" has made a data-retention choice without realizing it. A spec forces those choices into the open, where a privacy or security partner can see and challenge them.

## What changes in the lifecycle

- **Design first.** We define the *what* in a formal spec: decomposed requirements, OpenAPI contracts for APIs, schemas for data, types for functions, and the security and data-handling rules that apply. Precise inputs and outputs constrain the AI to a narrow, testable task.
- **AI implements.** Agents write the *how*: implementation code that must conform to the spec.
- **Humans validate.** Effort moves to validating the spec and the AI's adherence to it, rather than to typing the code.

[GitHub's Spec Kit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit) captures this flow well, with specify, plan and tasks phases and a human checkpoint after each. Its pitch to enterprises is that security and compliance requirements get written into the spec and plan from day one rather than arriving as review comments at the end. I agree with that direction. The toolkit does not enforce those constraints for you, though. It relies on the agent reading them and a human checking the result.

## The honest critique

The most useful analysis I have read is [Birgitta Böckeler's review of Kiro, Spec Kit and Tessl](https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) on martinfowler.com. She separates three levels: *spec-first*, where a spec guides one task; *spec-anchored*, where the spec is kept and evolved with the feature; and *spec-as-source*, where humans edit only the spec and never the code.

Her concerns deserve attention from anyone presenting this to a risk committee. A small bug ballooned into four user stories with 16 acceptance criteria. Spec Kit generated so many verbose markdown files that she wrote she would rather review code. Agents sometimes ignored the spec anyway. Regenerating from the same spec produced different code. And she draws the parallel to model-driven development, which struggled in business applications, warning that we could end up with inflexibility and non-determinism together.

There is a deeper risk underneath her critique. Rich Sutton's [bitter lesson](https://www.incompleteideas.net/IncIdeas/BitterLesson.html) is that general methods which scale with computation beat handcrafted knowledge "by a large margin." Elaborate, opinionated workflows and lengthy spec files that are hard to review are handcrafted rules for AI, and some of today's spec ceremony may age badly as models improve.

## Spec-anchored, not spec-as-source

My position for regulated firms is specific. Aim for spec-anchored and treat spec-as-source as a research bet, not a control strategy. If the same spec yields different code on each run, the spec alone cannot be your evidence of behavior. The tested, reviewed code that actually ships is still what the regulator cares about.

Second, keep the prose small and the formal parts large. Most of the value comes from artifacts machines can check: API contracts, schemas, type signatures, data classification tags, entitlement rules. A thousand words of natural-language requirements is just a longer prompt. The test I use is blunt. If a line in the spec cannot fail a build, it is guidance, not a contract. A fragment like this is more useful to an auditor than pages of user stories, because every line points at something that can pass or fail:

```yaml
feature: payment-status-api
contract: openapi/payment-status.v3.yaml
risk_tier: high
data:
  classification: confidential
  pii_fields: [account_number]
  logging: masked
controls:
  - id: entitlement-check
    test: tests/authz/test_entitlements.py
  - id: no-pii-in-logs
    test: policy/log_masking.rego
```

Third, match ceremony to risk. A copy change on an internal tool does not need a constitution and sixteen acceptance criteria. A change to how customer data is classified does. Tiering the process by risk is how you avoid the overhead Böckeler describes while keeping rigor where examiners will look. In practice, the first spec a team writes for a regulated service takes longer than the code would have. The fifth is faster, because the shared parts (data classes, entitlement patterns, logging rules) become reusable modules that every new spec imports.

## Why spec programs decay

The failure I see most often is not a bad first spec. It is drift. An incident at two in the morning gets fixed in the code, the fix is correct, and nobody updates the spec. Three months later the spec describes a system that no longer exists, and the audit trail it was meant to provide points confidently at the wrong behavior. A drifted spec is worse than none, because people trust it.

Two rules prevent most of this. First, any change to a spec-anchored service that does not reference a spec version fails the pipeline. Emergency fixes are included; they get a short window to amend the spec, not an exemption. Second, each spec has a named owner on the business side as well as in engineering. Engineers can keep contract files accurate, but only someone accountable for the business outcome can say whether a requirement is still the requirement.

The other quiet failure is the spec written after the code to satisfy a process. It is easy to spot: the spec matches the implementation perfectly, accidents included. A spec that never disagreed with the code was never doing any work. When I review a program, I ask to see one spec change that caused code to be rejected. If nobody can show me one, the process is documentation, not control.

## Make conformance mechanical

The business case is simple to state. Velocity, because low-level repetitive coding is automated. Predictability, because a formal contract sharply reduces ambiguity and hallucination. Auditability, because the spec becomes the primary artifact for compliance and security review, and it is far more efficient to audit a spec than thousands of lines of generated code.

There is a condition attached, and it is the point I most want leaders to take away. Auditing the spec instead of the code is only legitimate when conformance between them is checked by machines: contract tests generated from the OpenAPI file, schema validation in the pipeline, policy-as-code for data handling, all tied to the spec version. Without that link you have not reduced the audit burden. You have moved the gap from the code to the space between the spec and the code, where nobody is looking. [DORA's 2025 research](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) adds a practical warning: AI raises change volume, and without strong testing, version control and fast feedback, that volume turns into instability.

**What to do on Monday morning:**

- Choose one high-risk service and mark which lines of its current specification could fail a build today.
- Add a pipeline check that rejects changes to spec-anchored services when the commit does not reference a spec version.
- Name a business owner alongside the engineering owner for each spec on your most examined system.
- Define three risk tiers for spec ceremony and publish which kinds of change fall into each.

Done this way, spec-driven development turns generative AI from a helpful but unreliable assistant into a disciplined engineering tool that a risk partner can reason about. Done carelessly, it produces piles of markdown that look like governance and are not. Which parts of your current specifications could fail a build today?

**Bottom line:** Make the spec the contract, keep it anchored to the code, and let machines prove conformance. That is the balance regulated industries need between innovation and control.
