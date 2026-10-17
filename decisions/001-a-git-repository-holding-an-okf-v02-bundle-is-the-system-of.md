# ADR 001: A Git repository holding an OKF v0.2 bundle is the system of record

Status: accepted, October 17, 2026

## Context

The wiki must outlive any tool and be readable by people, agents and other engines.

## Decision

`wiki/` is an Open Knowledge Format v0.2 bundle in Git; every change is a commit and arrives by pull request.

## Consequences

Any OKF tool can read it (OpenWiki, the llmwiki compiler, Knowledge Catalog). No database to run.
