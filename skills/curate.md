# Curate (after every ingest)

Input: the branch the Librarian just wrote, usually one new or merged note and one raw copy.

1. `git diff --stat main` to see what changed. Read each changed note and its raw copy.
2. Check the raw copy has `published_at`, `origin_kind` and `license_note`. If not, take them from the capture in
   `inbox/done/`. If the capture has no publication date, stop and ask in the PR.
3. Check the folder. If the note sits outside the theme folders, or in the wrong theme, `llmwiki2 --bundle wiki move`.
4. Set `kind`. Add `relations` where a typed edge is clear (refines, contradicts, builds_on, applies, supersedes...).
   Add `aliases` for other names. Add `canonical_essay` for notes about Muthu's essays.
5. Read the body against the source. Remove anything the source does not say. Keep names, numbers and dates exact.
6. Run `PYTHONPATH=tools python -m kb normalize`, `python -m kb check`, `llmwiki2 --bundle wiki check`. Fix what fails.
7. Append a line to `wiki/log.md` under today's date: `* **Curation**: <what you did> [Note](path)`.
8. Commit, push the branch, open the pull request with this body:

   ```
   ## What changed
   ## Claims table
   | Claim | Source id | Source date |
   ## Checks
   kb check: pass | llmwiki2 check: pass
   ## Questions for Muthu
   ```
