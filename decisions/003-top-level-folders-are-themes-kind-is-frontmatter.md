# ADR 003: Top-level folders are themes; kind is frontmatter

Status: accepted, October 17, 2026

## Context

CROW routes by subject. Genre folders would ask the classifier a question it was not calibrated for.

## Decision

Seven theme folders from the site taxonomy; `kind` is a frontmatter field set by the curator.

## Consequences

Validation refuses other top-level folders; the curator moves misfiled notes.
