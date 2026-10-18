# 6. Operations

## Daily and weekly

| When | What | How |
|---|---|---|
| New source | Capture, file, curate, review, merge | `make ingest`, `make curate`, then the pull request |
| After a release | Glance at `report.md`: entity count, resolution merges, relations kept, failures | the release page |
| Weekly (automatic) | Lint, consolidation, stale notes | the "Weekly lint" issue and its fixes pull request |
| Monthly | Promote good machine suggestions | `python -m kb propose --graph graph.json`, curate, pull request |
| Before a re-check date | Re-verify stale notes | `make stale` |

## Switches

| Variable | Values | Effect |
|---|---|---|
| `GRAPH_EXTRACTOR` | `semantica` (default), `none` | `none` publishes the deterministic graph only |
| `SEMANTICA_NER_METHOD` | `llm` (default), `ml`, `pattern` | entity extraction method |
| `SEMANTICA_RELATIONS` | `llm` (default), empty | typed relation suggestions and the model alias pass |

## Failure modes

| Symptom | Likely cause | Action |
|---|---|---|
| Release has `Semantic layer skipped` | Library failed to import or start (key, credit, network) | The deterministic graph still published; read the reason in `report.md`; fix the key or credit |
| `typed relations: 0 kept; dropped N evidence` | Model paraphrased instead of quoting | Check the prompt; never relax the verbatim check |
| Entity count jumps or collapses between releases | Model behaviour changed | Compare the canary annotations on a pull request; pin or adjust filters |
| Wiki shows old data | Deploy hook missing or site built before the release | Redeploy the wiki project from `main` |
| Required check never reports | Job renamed or skipped by a job-level `if:` | Restore the job name; move conditions to steps |
| Approval did not stamp `verified` | Reviewer was not the owner, or commits were pushed after approval | Approve the latest commit as the owner |

## Rollback

- **Content:** revert the merge on `main`; the next release supersedes the bad one.
- **Semantic layer only:** set `GRAPH_EXTRACTOR=none` and re-run `publish` (or merge anything).
- **Site:** promote the previous production deployment in Vercel, or redeploy an older commit of the site repository.

## Cost

| Item | Typical |
|---|---|
| Semantic layer per release (Haiku, ~51 notes: entities ~150 s, relations ~190 s) | a few cents |
| Weekly curator | capped at $5 per run |
| Local classifier | free (runs on the Mac) |
| Vercel, GitHub | free tiers |
