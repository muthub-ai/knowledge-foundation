# 4. The graph and the semantic layer

**Outcome:** `graph.json` (the only contract with the website) built from a deterministic backbone, plus a labelled
semantic layer from Semantica: resolved entities and ontology-typed relation suggestions, with a canary that proves
the model actually ran.

## The contract

`schemas/graph.schema.json`: nodes (`id`, `type`, `label`, `url`, `summary`, `trust`, `updated`, optional
`canonical`, `verified`, `stale_after`, `source_date`, `aliases`) and edges (`source`, `target`, `type`, `origin` one of
`frontmatter | link | folder | source | extracted`, `evidence`, `weight`). The site treats `ext:` nodes as entities and
`extracted` edges as machine-made.

## Steps

1. **Deterministic backbone** (`tools/kb/graph.py`, ADR 009): theme membership, Markdown links, frontmatter
   `relations`, and sources with their publication dates. No model involved; this layer always builds.
2. **Semantica behind an adapter** (`tools/kb/extractors/semantica_adapter.py`): one function,
   `extract(notes) -> Extraction`. Pin the library (`requirements-graph.txt`, `semantica[llm-anthropic]==0.7.0`).
   The adapter:
   - asks for the `union` merge strategy, so a failed LLM call returns nothing instead of a silent pattern-matching fallback;
   - copies the library's warnings and the pass timing into `report.md`;
   - constrains extraction to five entity types and filters generic words, dates, durations, versions, host names and
     other notes' titles;
   - patches Semantica 0.7.0's Anthropic provider, which reads `response.content[0].text` and fails when the reply
     starts with a thinking block.
3. **Entity resolution** (`tools/kb/extractors/resolution.py`, ADR 016): spelling and plural folding, Semantica's fuzzy
   `EntityResolver`, an acronym rule, and one checked model pass; merged entities keep aliases.
4. **Typed relations** (`tools/kb/extractors/relations.py`): per note, the model sees the notes that share entities
   with it (minus pairs already linked) and may propose only the ontology's relation types; a proposal is kept only if
   its type is allowed, its target was offered, confidence ≥ 0.7 and the evidence sentence is found verbatim in the note.
5. **Promotion by review:** `python -m kb propose --graph dist/graph.json` writes suggestions into frontmatter on a
   branch; curate the diff and open a pull request.
6. **Canary** (`tests.yml`, job `semantica-canary`): a matrix of `pattern`, `ml`, `llm`; prints the extractor report,
   the resolved entities with aliases and every proposed relation (TSV) as check annotations. The `llm` job has a
   50-minute budget.
7. **Turn it on for releases** (`publish.yml` defaults to `GRAPH_EXTRACTOR=semantica`, `SEMANTICA_NER_METHOD=llm`,
   `SEMANTICA_RELATIONS=llm`, provider Anthropic, model `claude-haiku-5-5`).

## Check it worked

- The canary's annotation shows `Extractor: semantica:llm/pattern`, a nonzero entity count, a `resolution:` line with
  merges such as `MCP = Model Context Protocol`, `typed relations: N kept`, and `Notes whose extraction failed: 0`.
- A release's `report.md` has the same lines; `graph.json` has `ext:` nodes with `aliases` and typed `extracted` edges.

## Gotchas we hit (each one looked like success)

| Symptom | Cause | Fix |
|---|---|---|
| LLM run returned exactly the pattern run's entities | Semantica's default `fallback` strategy substitutes patterns when a method fails | `merge_strategy="union"`, warnings copied into the report |
| 400: key not scoped to a workspace | Account-level Anthropic key | Create the key inside a Console workspace |
| 400: credit balance too low | API credit is separate from a Claude subscription | Add prepaid credit in the Console |
| Job cancelled at 15 minutes, no report | Every call retrying three times | Per-note timing in the report; longer budget for the `llm` job |
| `'ThinkingBlock' object has no attribute 'text'` | Provider reads `content[0]` | Adapter joins the reply's text blocks |
| 285 "entities", many generic | Asking for typed entities makes the model list every noun | Generic and phrase filters; publish only entities that connect notes or are named |
| Uniform 0.75 relation confidence | Haiku's self-rated confidence carries no signal | Labelled as unreviewed, hidden by default; promotion is editorial |
