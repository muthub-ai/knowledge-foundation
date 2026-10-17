# ADR 009: Deterministic graph backbone; Semantica behind an adapter

Status: accepted, October 17, 2026

## Context

Semantica is powerful but young and changes APIs between minor releases; Markdown is not a first-class input.

## Decision

The graph is built from frontmatter, links, folders and sources by `kb graph`; Semantica runs behind a one-function adapter and is optional.

## Consequences

If Semantica breaks, the deterministic graph still publishes and the report says so. A canary job tests new releases.
