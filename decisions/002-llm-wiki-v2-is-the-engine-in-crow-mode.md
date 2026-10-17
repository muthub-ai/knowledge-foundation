# ADR 002: LLM-Wiki-V2 is the engine, in CROW mode

Status: accepted, October 17, 2026

## Context

Classic LLM wikis spend most tokens deciding where things go, and cost grows with the wiki.

## Decision

LLM-Wiki-V2 (llmwiki2 0.5.0, pinned) files and answers; a typed classifier makes the decisions and the LLM writes.

## Consequences

Flat cost per document. Two-author project: pinned, and the OKF bundle lets us switch engines.
