# ADR 006: Verification is the owner's approval

Status: accepted, October 17, 2026

## Context

Trust must be a fact about review, not an opinion of the writer.

## Decision

When Muthu approves a pull request, `approve.yml` stamps `verified: {by: human:muthu, at: <approval>}` on the changed notes and promotes drafts to stable.

## Consequences

Trust tiers are derived from `verified` as OKF specifies; no confidence scores are stored.
