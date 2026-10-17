---
type: Source
title: Governance belongs in the catalog
resource: https://muthub.org/writing/unified-governance-in-the-catalog.md
hash: sha256:d2ad63593bd92d1cd7ad50e217b5e3a1c7071c5933cbb2e1bbbef3dcb3b70af8
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2025-04-14'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Governance belongs in the catalog

Published 2025-04-14. Adapted from my LinkedIn post of April 12, 2025.

**Governance that lives in the catalog travels with the data; governance that lives in a policy document does not.** Unified catalogs now bring technical and business metadata, data products, a knowledge engine that infers relationships between entities, and semantic search into one place, built on open table formats like [Apache Iceberg](https://iceberg.apache.org/).

For human analysts, that is a convenience. For agents, it is the difference between guessing at tables and understanding meaning. An agent asked about customer churn will happily query whichever table has "customer" in its name unless something tells it which dataset is certified, what the columns mean and who owns the definition. The catalog is where that context should live.

In large regulated enterprises I have worked in, the hardest governance problems were rarely about access control. They were about meaning: two teams using the same term for different things, and nobody able to say which version a report used. Putting business definitions and lineage next to the technical metadata is how you start to fix that, and open formats keep you from being locked into one vendor's view of your own data.

If your agents cannot read your catalog, they are working from rumor.
