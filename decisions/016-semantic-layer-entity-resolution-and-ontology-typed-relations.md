# ADR 016: Semantic layer: entity resolution and ontology-typed relations, promoted only by review

Status: accepted, October 18, 2026 (extends ADR 009)

## Context

Semantica's LLM entity extraction works (after the fixes recorded in the README), but raw output repeats things under
several names ("MCP" and "Model Context Protocol"), returns generic words, and says nothing about how notes relate.
A model can propose relations between notes, but a model's relation is not an author's relation.

## Decision

- Extraction is constrained to five entity types (Concept, Standard, Tool, Organization, Practice); people, places,
  dates and amounts are dropped, and an entity is published only if it connects two or more notes or is a named
  standard, tool or organisation.
- Entities are resolved in conservative passes: spelling and plural folding, Semantica's fuzzy `EntityResolver`, an
  acronym rule, and one model pass whose groups are checked (existing names only; never a broader term with a narrower one).
- Typed relations between notes are proposed by the model under the ontology's relation types, only between notes
  that share entities and are not already linked, and kept only when the evidence sentence is found verbatim in the note.
- Proposals are published as `extracted` edges, labelled and hidden by default on the site, and never override an
  authored edge. Nothing is written to a note by the build. `kb propose` writes chosen proposals into frontmatter on a
  branch; the owner accepts them through an ordinary pull request.

## Consequences

The graph shows what a model found without passing it off as authored structure. Model confidence for relations is
currently uniform (0.75), so it does not rank proposals; promotion is editorial. Each release takes a few minutes
longer and costs a few cents of API use. The layer can be switched off with a repository variable.
