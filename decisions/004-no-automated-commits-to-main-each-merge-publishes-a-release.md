# ADR 004: No automated commits to main; each merge publishes a release

Status: accepted, October 17, 2026

## Context

Branch protection forbids pushes to main, and bots writing to main weaken review.

## Decision

`publish.yml` builds the graph and creates a versioned GitHub Release; the site builds from the latest release.

## Consequences

main changes only by Muthu's merge. Releases are immutable, versioned outside data.
