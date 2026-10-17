---
type: Source
title: The MCP spec grows up
resource: https://muthub.org/writing/the-mcp-spec-grows-up.md
hash: sha256:548e696c7b751a8390bf101a150e0c14ff07c530fe112b25bb77b3c66cef067c
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2025-04-01'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# The MCP spec grows up

Published 2025-04-01. Adapted from my LinkedIn posts of March 29 and 30, 2025.

**The March 2025 MCP update was the release that made enterprise adoption plausible.** The [protocol changelog](https://modelcontextprotocol.io/specification/2025-03-26/changelog) lists four major changes: an authorization framework based on OAuth 2.1, a streamable HTTP transport replacing the older HTTP plus server-sent events approach, JSON-RPC batching, and tool annotations that describe tool behavior, such as whether a tool is read-only or destructive.

Authorization was the one I cared about most. Without a standard way to establish who is calling a tool and with what rights, no serious security team would let MCP near production data. Tool annotations matter too, because a policy engine can treat a destructive tool very differently from a read-only one.

The ecosystem moved the same week. OpenAI added MCP support to its Agents SDK, and Microsoft's new Playwright MCP server let agents use web pages through accessibility snapshots rather than screenshots, which is faster and far more reliable. When a direct competitor adopts a protocol that Anthropic created, it is clear to me that MCP will become the default way agents connect to tools.

Standards become real when security teams can say yes to them.
