---
type: Source
title: From pair programming to fleet management
resource: https://muthub.org/writing/from-pair-programming-to-fleet-management.md
hash: sha256:acbcaacc0db53177d0ee3c6dd02e9501f314e205cd5afd2c4e5b94118341ad8c
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2025-12-15'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# From pair programming to fleet management

Published 2025-12-15. Adapted from my LinkedIn post of December 13, 2025.

**The bottleneck in AI-assisted development is often not the model, it is the cost of switching context.** Every time an engineer stops to set up a task, wait for a result and then reload the problem in their head, the speed gain from the model leaks away. One assistant in a chat pane is still pair programming, and pair programming does not scale past one pair.

Multi-agent orchestration in the editor changes the shape of the work. A local agent handles strategy and quick answers. Background agents work in isolated worktrees on well-scoped tasks. Cloud agents take the heavy lifting, like large refactors or long test runs. Ideally all of them draw on the same repository instructions and context, so nobody has to re-explain the codebase each time.

The useful distinction for leaders is between automation and orchestration. Automation is doing things right: one agent completing one task well. Orchestration is doing the right things: deciding which work goes to which agent, in what order, with what checks before anything merges. The second is an architecture and management problem, and that is where I see most teams underinvesting. The payoff is asynchronous execution. Engineers stop babysitting a single session and start reviewing the output of several, which is a different skill and needs different guardrails.

Build the factory first; the widgets will follow.
