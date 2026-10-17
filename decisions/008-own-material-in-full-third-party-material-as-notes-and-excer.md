# ADR 008: Own material in full; third-party material as notes and excerpts

Status: accepted, October 17, 2026

## Context

A public repository must not republish other people's work.

## Decision

Captures marked third-party are limited to notes and a short excerpt (2,500 characters); full copies stay in the private folder.

## Consequences

Enforced by tools/librarian/ingest.py and reviewed in every pull request.
