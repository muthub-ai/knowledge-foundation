# ADR 005: A GitHub App authors automated pull requests and stamp commits

Status: accepted, October 17, 2026

## Context

Events created with GITHUB_TOKEN do not trigger workflows, so checks would never run on bot pull requests.

## Decision

A private GitHub App owned by Muthu provides tokens to the ingest, weekly and approve workflows.

## Consequences

Required checks run on every bot change; Muthu's review is required because the App, not he, is the author.
