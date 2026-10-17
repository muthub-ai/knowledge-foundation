# Lint (weekly)

1. Deterministic first: `python -m kb check`, `python -m kb stale`, `llmwiki2 --bundle wiki check`,
   `python -m kb graph --out dist` (read `dist/report.md`: orphans, most connected notes).
2. Judgment, on a sample of at most 15 notes changed in the last 30 days plus 5 at random:
   - contradictions between notes on the same subject (record both sides; add a `contradicts` relation)
   - claims not supported by their source
   - notes past `stale_after`: propose re-verification against the source, or deprecation
   - orphans worth linking; maps that miss new notes
3. Mechanical fixes (broken links, missing aliases, index drift) go in one pull request. Judgments go in one issue,
   titled "Weekly lint YYYY-MM-DD", with a checklist Muthu can tick.
4. Never rewrite a note's argument in a lint pass.
