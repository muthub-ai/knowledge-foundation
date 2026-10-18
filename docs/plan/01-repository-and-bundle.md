# 1. The knowledge repository and its bundle

**Outcome:** a public repository holding an Open Knowledge Format v0.2 bundle that passes its own rules locally.

## Steps

1. **Create the repository** `knowledge-foundation` (public) and clone it.
2. **Lay out the bundle** (ADR 001, 003):
   - `wiki/<theme>/` one folder per theme; `kind` is frontmatter, not a folder.
   - `wiki/raw/` source copies (own material in full; third-party as notes plus a short excerpt, ADR 008).
   - `index.md` and `log.md` in every folder (LLM-Wiki-V2 maintains them).
3. **Write `wiki.config.yaml`**: site name and URL, canonical essays site, themes with routing descriptions, kinds,
   re-verification periods per kind, owner, models.
4. **Add the rules** (`tools/kb/`): JSON Schemas in `schemas/` for notes, source copies and the graph; the date rule
   (ADR 007: a note may not cite a source published after it; dates are never invented); the blocklist checker; the
   evals file (`evals/questions.yaml`, questions with the note that should answer each).
5. **Add the ontology** `ontology/edge-types.yaml`: ten typed relations a curator may write in frontmatter
   (`builds_on`, `refines`, `applies`, `contradicts`, `cites`, `part_of`, `authored_by`, `about`, `supersedes`,
   `answers`) and the derived edge types (`links_to`, `in_folder`, `draws_on`, `mentions`).
6. **Add the blocklist locally**: copy your private term list to `.confidential-terms.txt` (git-ignored). One term per line.
7. **Seed content**: either write notes by hand or run the one-off seed from an existing site
   (`tools/librarian/`), then `python -m kb normalize` to add governance defaults (never `verified`).
8. **Record decisions** in `decisions/` as you go (context, decision, consequences).

## Check it worked

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make check        # validate, dates, blocklist, evals: 0 problems
make test         # unit tests and the end-to-end flow
make graph        # dist/graph.json builds and matches schemas/graph.schema.json
```

## Gotchas

- Keep timestamps as text when reading YAML: PyYAML turns ISO dates into `datetime` objects, which breaks
  round-tripping. The tools use a loader without the timestamp resolver.
- Give each note a stable path; rename with `llmwiki2 move` so links follow.
