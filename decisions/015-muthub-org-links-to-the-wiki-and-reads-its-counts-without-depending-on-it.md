# ADR 015: muthub.org links to the wiki and reads its counts, without depending on it

Status: accepted, October 18, 2026 (amends ADR 011)

## Context

ADR 011 kept muthub.org unchanged while the wiki was new and left "a link from muthub.org" as a later decision. With
the wiki live, the essays site should send readers to the graph, and the numbers it shows should be the wiki's own.

## Decision

muthub.org gets a "Graph" link in its header and a Knowledge Foundation band on its home page. The band reads
`https://wiki.muthub.org/graph.json` at build time and then hourly (Next.js ISR), counts notes and connections with the
same rules as the wiki (extracted entities are not notes, machine edges are not connections), and falls back to the
last known figures when the wiki cannot be reached.

## Consequences

muthub.org's build and pages never fail because of the wiki. The counts can lag a new release by up to an hour. The
essays remain canonical on muthub.org; wiki notes link to them.
