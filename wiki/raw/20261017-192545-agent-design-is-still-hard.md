---
type: Source
title: Agent design is still hard
resource: https://muthub.org/writing/agent-design-is-still-hard.md
hash: sha256:b9588a4afd8548e46f6f801066a64c358ccf7ce2a84e855b35925031646b5f8e
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2025-11-25'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Agent design is still hard

Published 2025-11-25. Adapted from my LinkedIn post of November 24, 2025, on Armin Ronacher's essay.

**Agent design is still hard, and higher-level SDKs do not make the hard parts go away.** Armin Ronacher's essay [Agent Design Is Still Hard](https://lucumr.pocoo.org/2025/11/21/agents-are-hard/) captures what many builders are finding: subtle differences between models and tool behaviors force teams to build their own abstractions anyway.

His lessons match what I see in enterprise builds. Explicit cache management gives predictability and cost control, even if it feels like extra work at first. Feeding reinforcement back after each tool call (reminding the agent of its goal, reporting status, suggesting a fix after a failure) improves reliability. Sub-agents isolate failures so one bad iteration does not poison the whole context. A shared, file-system-like state lets tools pass work to each other instead of hitting dead ends. And steering the final output turns out harder than anyone expects.

My takeaway for architects is that the loop is the easy part. The real design work is in orchestration, resilience and control: where state lives, how failures are contained and who decides when the agent is done. That is ordinary distributed-systems thinking applied to a new kind of component, and teams that treat it that way ship more reliable agents.

If your agent framework hides these choices from you, who is making them?
