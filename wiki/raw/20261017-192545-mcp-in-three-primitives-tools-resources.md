---
type: Source
title: 'MCP in three primitives: tools, resources, prompts'
resource: https://muthub.org/writing/mcp-tools-resources-prompts.md
hash: sha256:bf4c18446c3765b27451fc912641307961951fa81a3e76c4a54681bffb78182a
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2025-06-18'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# MCP in three primitives: tools, resources, prompts

Published 2025-06-18. Adapted from my LinkedIn post of June 17, 2025.

**The Model Context Protocol exists because people got tired of copying and pasting context between applications.** Before MCP, connecting a model to your files, tickets or databases meant manual shuttling or a bespoke integration for every pairing of model and system. That does not scale, and it is a governance headache.

MCP's answer is three primitives. Tools are actions a model can take. Resources are data it can read for context. Prompts are reusable templates that a user can invoke. I like this design because it is small enough to explain to a non-specialist in a minute, which is rare for an integration standard and a good sign it will last.

The bigger story is that it was open source from the start, which let a large community form quickly. That shifted effort away from proprietary connectors and toward model intelligence and workflow, where the real differentiation sits. For an enterprise architect, a common protocol also means one place to apply authentication, logging and policy instead of dozens.

Small, open standards tend to win; the [MCP specification](https://modelcontextprotocol.io/specification/2025-03-26) is a good example of why.
