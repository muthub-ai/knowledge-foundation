---
type: Source
title: 'A2A and MCP: complementary, not competing'
resource: https://muthub.org/writing/a2a-and-mcp.md
hash: sha256:2cfaa473f26d26623d1c2dc0ed0002a101350e6c22444e919cd2caeed92cb7ea
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2025-05-01'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# A2A and MCP: complementary, not competing

Published 2025-05-01. Adapted from my LinkedIn posts of April 10 and April 30, 2025.

**MCP and A2A solve different problems, and the debate over which one wins misses that.** Google Cloud Next 2025 brought the Agent2Agent protocol, the Agent Development Kit and MCP support together. Google's own [A2A announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) described it as complementing MCP: MCP gives an agent access to tools and data, while A2A lets agents discover and work with each other.

A2A's modality-agnostic design is the part I find most interesting. Agents can collaborate in whatever form suits the task, including text, audio or video streaming, rather than being forced through a single chat format.

Standards are making AI less of a solo act. Interoperability is what turns individual agents into enterprise systems. But it also raises the governance stakes considerably. When one agent can call tools and also delegate to other agents, you need identity, authorization and audit across both protocols. A permission boundary that holds for a single agent can leak once it starts handing work to others.

If your agents can talk to each other, can you trace who asked whom to do what?
