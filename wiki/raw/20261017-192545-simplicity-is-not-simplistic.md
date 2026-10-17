---
type: Source
title: Simplicity is not simplistic
resource: https://muthub.org/writing/simplicity-in-architecture.md
hash: sha256:0be6f8dd5034c68a3c508515068bf61d028413d399e9695ffe8469e09e41cda5
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2024-11-08'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Simplicity is not simplistic

Published 2024-11-08. Adapted from my LinkedIn post of November 7, 2024, and Medium.

**Simple architecture is the hardest kind to produce, which is why there is so little of it.** By simplicity I mean designs that are easy to communicate, build and maintain: a deliberate reduction to the essential components. That is very different from simplistic, which skips the hard thinking and leaves the complexity for someone else to find later.

Making a design look effortless takes considerable work. You have to understand the problem well enough to know what can be left out, and then defend those omissions when someone asks for one more layer, one more service or one more configuration option. Every component you add is a component someone will have to explain, secure and operate for years.

My test is whether an engineer who joins next year can sketch the system on a whiteboard after a one-hour walkthrough. If they cannot, the design will slowly be rewritten by people working around parts they do not understand. Complexity rarely arrives in one big decision; it accumulates through many small ones that each seemed reasonable. The payoff is reliability and ease of operation, and both matter more every year a system runs.

If you cannot explain it simply, you probably cannot run it reliably.
