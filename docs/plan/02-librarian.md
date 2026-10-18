# 2. The Librarian: a local classifier decides, Claude writes

**Outcome:** dropping a capture in `inbox/` and running `make ingest` files it into the right theme, linked to the
right notes, on a branch.

## Steps

1. **Install LLM-Wiki-V2** (pinned in `requirements.txt`, `llmwiki2`). It runs in CROW mode (ADR 002): a typed
   classifier makes every filing and retrieval decision; the writing model only writes.
2. **Install the local classifier** (ADR 013) following [`docs/local-classifier.md`](../local-classifier.md):
   Ollama 0.35+, the `tev1` model with an 8,192-token context (`tev1-8k`). Ollama refuses an over-long request rather
   than truncating it, so a small context sends decisions back to Claude.
3. **Configure** `.env` from `.env.example`: Claude through Anthropic's OpenAI-compatible endpoint
   (`OKF_LLM_*`), the classifier (`OKF_CLASSIFIER_*`), the prompts directory and the bundle path. Never commit `.env`.
4. **House style** lives in `prompts/` (for the Librarian) and `skills/` plus `AGENTS.md` (for the curator agent):
   plain language, no hype words, no em dashes, every claim footnoted to a dated source.
5. **Daily loop:** copy `inbox/TEMPLATE.md.txt`, fill `title`, `published_at`, `origin_kind`, `license_note`, then
   `git switch -c capture/<topic> && make ingest && make curate`. The curator opens the pull request with a claims table.

## Check it worked

- `llmwiki2 --bundle wiki ask "What is a curated overlay?"`: the token line shows two ledgers, and the classifier line
  shows calls with no cost.
- `make ingest` on a sample capture creates or updates a note and moves the capture to `inbox/done/`.

## Gotchas

- Third-party material: at most a short excerpt (2,500 characters). The rules reject full copies.
- The cloud fallback (`ingest.yml`, run by hand from Actions) has no local classifier, so it runs in classic mode
  (Claude decides and writes). Use it only when away from the Mac.
