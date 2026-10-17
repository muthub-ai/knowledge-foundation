# ADR 012: Public knowledge only

Status: accepted, October 17, 2026

## Context

The wiki is public and the author works in a regulated enterprise.

## Decision

The confidential-terms list runs in CI from a secret; AGENTS.md and the house-style prompt forbid internal material.

## Consequences

The list is never committed and the checker never prints the term it found.
