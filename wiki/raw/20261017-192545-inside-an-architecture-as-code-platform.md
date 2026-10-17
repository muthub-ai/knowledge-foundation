---
type: Source
title: 'Inside an Architecture-as-Code platform: a C4 walkthrough'
resource: https://muthub.org/writing/inside-an-architecture-as-code-platform.md
hash: sha256:02f2da076e64f80dcfae906a7a2fa06d51a2a21198c4b472b135650b7e199ecd
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2026-10-12'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Inside an Architecture-as-Code platform: a C4 walkthrough

Published 2026-06-09, updated 2026-10-12. Based on my public prototype at aac.muthub.org, its source at github.com/muthub-ai/aac, and my LinkedIn post of May 2, 2026.

**The best test of an architecture platform is whether it can describe itself, so I made mine do it.** [aac.muthub.org](https://aac.muthub.org) is a working prototype of an architecture control plane: enterprise architecture held as version-controlled YAML that drives validation, policy, diagrams and an executive scorecard. To write this piece I modeled the platform in its own notation, ran that model through the same JSON Schema and the same five compliance rules it applies to every other system, and drew the diagrams below from it. It passed. The [source is public](https://github.com/muthub-ai/aac) if you want to check my work.

I used Simon Brown's [C4 model](https://c4model.com/) because most engineers already read it fluently: context, containers, components, code. Each level answers a different question for a different reader, and the walkthrough follows that order. The interesting part is less what each box is than why it sits where it does.

## Level 1: three people, one source of truth, and an agent

The context view shows who the platform serves. Enterprise architects author standards, patterns and models and review exceptions. Application engineers design and change systems. Technology leaders read conformance and risk. Around them sit GitHub, which hosts everything, the npm registry, product teams' own repositories, and an AI coding assistant in the engineer's IDE.

The arrow I would point a review board at is the one from the AI assistant into the platform. Two years ago I would have drawn the engineer as the only consumer of architecture standards. Today a large share of design decisions are made, or at least drafted, by an agent in the IDE, and an agent that cannot read your standards will happily invent its own. Treating the agent as a first-class user at Level 1 is the design decision everything else follows from.

## Level 2: one repository, seven containers

Inside the boundary there are seven containers, and six of them are projections of the seventh. The Architecture Repository holds system models, patterns, standards, waivers and the schemas that define them. Everything else reads from it: the governance pipeline on every pull request, the web dashboard at build time, the documentation microsite as generated pages, the CLI through the published schemas, the MCP server through a local clone, and the policy engine as tested Rego.

Three decisions at this level carry most of the weight.

- **The dashboard has no database.** It reads the repository at build time through server components and is rebuilt when main changes. There is nothing at runtime that can drift from Git, which is the property you want from a governance view. The cost is that the dashboard is only as fresh as the last merge, and for architecture that is the right cadence.
- **The CLI validates against published schemas, not local copies.** It fetches them from the repository's public URL with ETag caching and falls back to the cache when offline. A product team's pipeline therefore validates against the same contract the platform publishes, and a schema change reaches every team on its next run without anyone upgrading a package.
- **Waivers live next to the standards they bend.** An exception is a versioned record with its risk, compensating controls, financial impact, approver, remediation plan and expiry date. Once exceptions are data, the scorecard can report exception debt the same way it reports technical debt, and a pipeline can check an expiry date instead of relying on someone's memory.

The scorecard is the payoff for leaders. Conformance, risk posture, remediation velocity and pattern reuse are computed from the artifacts, not assembled for a meeting. The figures on the live site come from a fictional sample portfolio, so ignore the values; the point is that the number is a query and it changes when a pull request merges.

## Level 3: governance as an API for agents

I drew component views for only two containers, and that restraint is deliberate. The C4 site itself says to [create component diagrams only when they add value](https://c4model.com/diagrams/component) and to automate them for long-lived documentation. The platform's own schema stops at containers for the same reason: components change with every refactor, so they belong to the code, not to the model.

The MCP server is the container that earns a Level 3 view, because its internal shape is the governance contract for agents. Built on the open [Model Context Protocol](https://modelcontextprotocol.io/introduction), it separates three kinds of capability. **Resources** are read-only views of the repository: systems, standards, patterns, schemas and, importantly, `aac://waivers/active`, which is meant to give an agent only the exceptions currently in force, so it does not treat a pending or rejected waiver as permission. **Tools** act: validate a document, run the five compliance rules, scaffold a waiver. **Prompts** are guided workflows for designing a new system or requesting an exception.

The distinction matters for risk. Reading a standard is harmless; writing a waiver is a governance act. Keeping them in different MCP primitives means an enterprise can grant an agent the first without the second, and the `scaffold_waiver` tool only drafts a file. The exception still becomes real through a reviewed pull request, the same as one written by a person.

The web container's components show the other half of the design: pure functions for parsing, validation, view filtering, layout and export, wrapped by a thin layer of React. The same parser and layout code also run in the pipeline's diagram build, which is why a diagram in a pull-request comment and the one in the dashboard agree.

## Level 4: draw code only where an invariant lives

C4's guidance on the code level is blunt: [it is optional and usually not recommended](https://c4model.com/diagrams/code), because an IDE can generate it on demand. I agree, with one exception. Draw Level 4 where the design depends on an invariant that is easy to break and hard to see in a diff.

The diagram editor has one. Engineers can edit YAML or drag boxes on a canvas, and each side updates the other. Without a guard that is an infinite loop: the editor updates the graph, the graph rewrites the YAML, the YAML updates the graph. A single field in the store, `syncSource`, records which side started the change, and each update path returns early if the other side owns it. It is three lines of code that the whole feature depends on, and it is exactly the kind of detail a new contributor would remove while tidying up. That is the case for a code diagram.

## A governed change, end to end

The dynamic view is the one I show executives, because it answers the question they actually have: what happens between someone proposing a change and that change being trusted? An engineer, or an agent working through the MCP server, edits the YAML and validates it locally. A pull request starts the pipeline: a lint and test gate, then parallel stages for schema validation, the five compliance rules, OPA policy tests and catalog and diagram generation. The pipeline comments diagram previews on the pull request, an architect reviews a diff with evidence attached, and the merge publishes the microsite and rebuilds the dashboard.

The pull request is the architecture review board now. A person still approves, but they approve a change with test results, not a slide deck. Nygard's case for [small decision records kept with the work](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) applies directly: the reasoning travels with the change.

## What I would change before an enterprise ran it

Modeling the platform in its own notation also exposed its weak spots, and I would rather name them than have a reviewer find them.

- **Validation lives in three places.** The CLI and the MCP server each validate with JSON Schema, and the web app validates with Zod. The five compliance rules exist in the pipeline script and again in the MCP tool. They agree today; nothing guarantees they will tomorrow. The fix is one rules package that the pipeline, the MCP server and the editor all import.
- **Some rules infer intent from free text.** The rule that stops a frontend talking directly to a database decides what counts as a frontend from keywords in tags and technology names. That is fine for a prototype and fragile at scale. An enterprise version needs explicit types in the schema, enforced by the schema.
- **Expiry is recorded, not enforced.** Every waiver carries an expiration date, but today a waiver stops counting only when someone changes its status. The active-waivers resource and the pipeline should compare the date themselves, so a lapsed exception stops granting permission on the day it lapses.
- **Policy lives in two languages.** Structural rules run as TypeScript and infrastructure rules run as Rego in [Open Policy Agent](https://www.openpolicyagent.org/docs). Two engines are defensible, but the boundary should be written down, or teams will add the next rule wherever is convenient.

The organizational gaps matter more than the technical ones. Never import a system catalog wholesale; seed it from the systems that change most and require an owner for every record. Run each new rule in report-only mode before it blocks anything, because a rule that cries wolf in its first month loses its audience for a year. And fund the control plane as a product with a small team and a backlog. Architecture-as-Code maintained as a side project decays into one more stale repository.

**What to do on Monday morning:**

- Ask your architecture team to model one platform they own in C4 YAML and run it through the same checks they apply to product teams.
- Inventory where your architecture rules are enforced today and count how many enforce the **same** rule in different code.
- List every place an AI coding agent can read your standards, and the places where it cannot.
- Pick one rule to run in report-only mode for a month before it blocks a release.

If you run architecture in a regulated enterprise, I would like to know: could your platform pass its own rules?

**Bottom line:** An architecture platform earns trust when it holds itself to its own rules. Model it in its own notation, draw component and code views only where they explain a real decision, and give AI agents the same governed access to standards that people have.
