---
type: Source
title: Architecture-as-Code Reference Platform (open prototype)
resource: https://muthub.org/initiatives/aac-reference-platform.md
hash: sha256:f629615e88f4d2020bc9c931596fc60365773821dc0aad2c828033f2211ab15b
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2026-10-16'
origin_kind: own-post
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Architecture-as-Code Reference Platform (open prototype)

Personal project, 2026. Role: Designer and builder.

aac.muthub.org: a public, working prototype of an architecture control plane, with catalogs, OPA policies, waivers, an executive scorecard, a CLI and an MCP server that brings the rules into coding agents. It is modeled in its own notation and passes its own rules.

## Problem

Architecture-as-Code is easy to agree with and hard to picture. Leaders and engineers needed to see what an architecture control plane actually looks like before committing to one.

## Approach

- Modeled systems, patterns, standards and waivers as machine-readable, version-controlled YAML validated by JSON Schema, using the C4 model's vocabulary for systems and containers.
- Built an operational lifecycle (define, build, test, accept, deploy) with automated schema validation, compliance checks and generated diagrams and documentation, gated by pull requests.
- Shipped developer utilities: a CLI (aac init, create, validate), an MCP server for IDEs and AI assistants, an OPA/Rego policy engine, context-driven development with Copilot Spaces and a reference GitHub Actions pipeline.

## Governance

- Executable guardrails with pass/fail results on every pull request: five structural compliance rules plus OPA policies for encryption, API-gateway routing and rightsizing.
- Waivers as first-class records with risk, compensating controls, financial impact, an approver, a remediation plan and an expiry date.
- The platform's own C4 model lives in the repository and passes the same schema and rules it applies to every other system.

## Outcome

- An executive scorecard computed directly from the artifacts: standards conformance, risk posture, technical-debt exposure, remediation velocity, pattern reuse and cloud spend at risk. The live site runs on a fictional sample portfolio.
- A public reference that colleagues and the community can explore, with its source on GitHub and a level-by-level C4 walkthrough below.

## Lesson

A working prototype changes more minds than a strategy deck, and one that passes its own rules changes more still.
