# The local classifier

CROW mode asks a typed classifier for every filing and retrieval decision; Claude only writes. The classifier runs
on your Mac, so no decision leaves the machine and it costs nothing per call.

## Set up once

1. Install Ollama 0.35 or later (it serves the System One API at `/systemone`): https://ollama.com/download
2. Pull the classifier model and give it a context of 8,192 tokens. Ollama refuses a longer request instead of
   cutting it, so a small context sends decisions back to Claude:

   ```
   ollama pull tev1:4b
   printf 'FROM tev1:4b\nPARAMETER num_ctx 8192\n' > Modelfile
   ollama create tev1-8k -f Modelfile
   ```

3. Copy `.env.example` to `.env` and paste your Anthropic API key.
4. Check it: `llmwiki2 --bundle wiki ask "What is a curated overlay?"`. The token line after the answer shows two
   ledgers; the classifier line should show calls with no cost.

Alternative server: Laya (`LAYA_PORT=8001 laya-serve`, then `OKF_CLASSIFIER_BASE_URL=http://127.0.0.1:8001/v1`).

## Thresholds

A custom classifier starts from LLM-Wiki-V2's Laya threshold preset. Phase 0 measures them on twenty of your
documents (right-note rate, fallback rate from `llmwiki2 health`) and records the values in ADR 013.

## In CI

GitHub runners have no local classifier. The `ingest` workflow therefore runs in classic mode (Claude decides and
writes) and is a fallback for when you are away from the Mac. Ingest normally runs on the Mac.
