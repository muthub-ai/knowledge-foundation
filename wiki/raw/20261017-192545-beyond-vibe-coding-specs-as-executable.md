---
type: Source
title: 'Beyond vibe coding: specs as executable artifacts'
resource: https://muthub.org/writing/spec-kit-beyond-vibe-coding.md
hash: sha256:37ae66a5e9d3d65501b6712982f5979240ffe2263a7b67722d86bba2a4f0c239
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2025-09-08'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Beyond vibe coding: specs as executable artifacts

Published 2025-09-08. Adapted from my LinkedIn post of September 5, 2025.

**Vibe coding produces code that looks right and quietly misses the point.** Ad-hoc prompting works for a prototype on a Friday afternoon. It falls apart when the output has to meet a business requirement, pass an audit and still make sense to the next engineer six months later.

GitHub's [Spec Kit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) takes a different stance: the specification is a living, executable artifact that guides every step of the build. Work moves through four gated phases (specify, plan, tasks, implement) with validation at each gate. It works with Copilot, Claude Code and Gemini CLI, which matters for enterprises that will not standardize on one assistant.

What I like most is where it puts human effort. Reviewing a spec and a plan is cheaper and more effective than reviewing a 2,000-line diff after the fact. If the intent is wrong, you catch it before a single file changes. In regulated settings that also gives you a trace from requirement to code, which is exactly what reviewers and auditors ask for. The trade-off is discipline. Teams have to write specs they would otherwise skip, and some will find that slow at first. I think that is the right cost to pay.

In AI-assisted delivery, the spec is the product and the code is a build output.
