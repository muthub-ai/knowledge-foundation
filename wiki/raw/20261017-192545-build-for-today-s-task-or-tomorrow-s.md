---
type: Source
title: Build for today's task or tomorrow's platform?
resource: https://muthub.org/writing/build-for-today-or-tomorrow.md
hash: sha256:4438b7853c633fe4f6646dda3917fe8c03425785c629067b7cb664762e1d9c49
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2025-09-22'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Build for today's task or tomorrow's platform?

Published 2025-09-22. Adapted from my LinkedIn post of September 21, 2025, on McKinsey's agentic AI lessons.

**How much to invest in reusable agents is the oldest architecture question in a new form.** McKinsey's [lessons from a year of agentic AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/one-year-of-agentic-ai-six-lessons-from-the-people-doing-the-work) raise it directly, and it is the same tension every architect knows: build fast, but do not lock in choices that will constrain you later.

Move too fast and you end up with brittle, single-use agents, each with its own prompts, tool wiring and guardrails, none of which can be reused or governed consistently. Move too slow and competitors ship while you are still designing the perfect platform. Neither failure is hypothetical; I have seen both in large enterprises.

My rule of thumb is to standardize the parts that are expensive to change and cheap to share, and let teams move freely on the rest. Identity, tool access, logging, evaluation and policy enforcement belong in a common harness from day one. The agent's specific task logic can stay local and disposable until a pattern repeats two or three times. Then it earns promotion to a shared component. Single-use agents are the new frontier of technical debt, and finding the balance takes architectural judgment, not a framework.

Standardize the harness early; let the agents stay disposable until they prove otherwise.
