# Knowledge Foundation

Muthu Bommiah's public working knowledge on governed AI, context engineering and AI-native software delivery. It is a
Git repository holding an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format) v0.2 bundle (`wiki/`),
kept by [LLM-Wiki-V2](https://github.com/crow-hq/llm-wiki-v2) and reviewed by Muthu. It is published at
**wiki.muthub.org** by the separate `knowledge-foundation-site` repository. muthub.org stays the home of the essays and
does not depend on any of this (ADR 011).

```
capture (inbox/) ─► Librarian: the local classifier decides, Claude writes ─► branch + pull request
      ─► CI: kb check, llmwiki2 check, graph, end-to-end tests ─► Muthu approves ─► stamp "verified: human:muthu"
      ─► merge ─► release kf-YYYY.MM.DD-N (bundle.tgz, graph.json) ─► Vercel rebuilds wiki.muthub.org
```

Nothing is committed to `main` by a bot, and nothing is marked reviewed until Muthu approves the pull request (ADR 004, 006).

## Repository map

| Path | What it is |
| --- | --- |
| `wiki/` | The OKF bundle: theme folders, notes, `raw/` source copies, `index.md` and `log.md` in every folder |
| `wiki.config.yaml` | Name, site, themes and their routing descriptions, kinds, re-verification periods, models |
| `inbox/` | Capture notes waiting to be ingested (`TEMPLATE.md.txt`); processed ones move to `inbox/done/` |
| `tools/kb/` | Governance tools: validate, dates, confidential terms, normalize, stamp, graph, evals |
| `tools/librarian/` | Ingest a capture through LLM-Wiki-V2; the one-off seed from muthub.org |
| `ontology/`, `schemas/` | Edge types; JSON Schemas for notes, source copies and the graph |
| `skills/`, `prompts/` | The curator's instructions (Claude Code) and house style for the Librarian |
| `evals/questions.yaml` | 20 questions with the note that should answer each |
| `decisions/` | Architecture decision records 001 to 014 |
| `tests/` | Unit tests and the end-to-end flow test |

## Set up on the Mac (once)

```bash
cd ~/knowledge-foundation
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt                 # llmwiki2 0.5.0, jsonschema, PyYAML, networkx
cp .env.example .env                            # then put your Anthropic API key in OKF_LLM_API_KEY
cp <your private term list> .confidential-terms.txt   # git-ignored, never committed
```

The local classifier: install Ollama 0.35 or later and follow `docs/local-classifier.md` (it builds `tev1-8k`, the
classifier with an 8k context). Claude does the writing through the API; the classifier only decides where a note goes,
whether it matches an existing note and what it relates to, so routing costs nothing and stays on the Mac.

Check everything works:

```bash
make test        # unit tests and the end-to-end flow (scripted models, no network)
make check       # the same rules CI runs on every pull request
```

## Daily use

1. Drop a capture in `inbox/` (copy `inbox/TEMPLATE.md.txt`). It needs `title`, `published_at`, `origin_kind` and
   `license_note`. Your own material can be complete; third-party material is your notes plus at most a short excerpt
   (2,500 characters), never the full text.
2. `git switch -c capture/okf && make ingest` files it. `make curate` asks Claude Code to tidy, link and check the
   result and open the pull request.
3. Read the pull request. Approving it stamps `verified: human:muthu` on the changed notes; merging publishes.

`make stale` lists notes past their re-check date. The weekly workflow (Monday) opens a "Weekly lint" issue with the
lint, consolidation and stale-note findings, and a pull request when there are mechanical fixes (made on its own
`curate/` branch); it is capped at $5 of API use per run.

## Set up GitHub (once)

1. Create the public repository `muthub-ai/knowledge-foundation` and push `main`.
2. Create a GitHub App (Settings → Developer settings → GitHub Apps → New), name it `knowledge-foundation-bot`:
   no webhook; repository permissions **Contents: read and write**, **Pull requests: read and write**,
   **Issues: read and write**. Install it on this repository only. Pull requests and commits made with the App's token
   trigger the test workflows, which the built-in `GITHUB_TOKEN` cannot do (ADR 005).
3. Repository settings → Secrets and variables → Actions:

   | Kind | Name | Value |
   | --- | --- | --- |
   | Secret | `ANTHROPIC_API_KEY` | For the weekly curator and the classic-mode ingest fallback |
   | Secret | `CONFIDENTIAL_TERMS` | The blocklist, terms separated by `\|`. The checker never prints a matched term |
   | Secret | `KF_APP_PRIVATE_KEY` | The App's private key (.pem contents) |
   | Secret | `VERCEL_DEPLOY_HOOK` | The site project's deploy hook URL (below) |
   | Variable | `KF_APP_ID` | The App's ID |
   | Variable | `GRAPH_EXTRACTOR` | `none` (default) or `semantica` to add machine-extracted entities (see below) |

4. Branch protection on `main`: require a pull request and the checks **unit tests** and **bundle rules**. Require
   **1 approving review** once pull requests come from the App: GitHub does not let you approve a pull request opened
   under your own account, and the approve workflow stamps notes only when you approve. Leave "Dismiss stale pull
   request approvals" off (the stamp commit would dismiss your approval), turn on "Require review from Code Owners"
   (`.github/CODEOWNERS`), block force pushes, and include administrators. Because stale approvals stay, check
   that nothing was pushed after your approval before you merge; the approve workflow stamps only the exact commit
   you approved, and stamps nothing if the branch has moved on. This protection is what keeps automated work off `main`; set it before enabling the ingest and
   weekly workflows.

## The graph

`kb graph` (run by CI and by the publish workflow) writes `graph.json`, `graph.graphml` and `report.md`. The backbone is
deterministic: declared relations, links in the text, theme membership and sources (ADR 009). A note that summarises one
of Muthu's essays carries its `canonical_essay` into `graph.json` as `canonical`, and the website sends readers there
first. The website lays the graph out itself (themes on a ring, notes orbiting their theme), so the `x`/`y` here are
only a fallback for other tools.

**The semantic layer (Semantica)** is optional and off by default (`GRAPH_EXTRACTOR=none`). It runs behind a
one-function adapter (`tools/kb/extractors/semantica_adapter.py`) and adds machine-found entities as `mentions` edges.
The `semantica canary` jobs in `tests.yml` run it against the real library on every pull request and report what it
found (in the job's annotations). What they showed in October 2026, on the 51 seeded notes:

- It runs, on every note, with no failures.
- The `pattern` and `ml` methods give the same result: without a spaCy model installed, `ml` falls back to patterns.
- Unfiltered, the quality is low: 56 "entities", led by years and section headings. The adapter now drops numbers,
  dates, headings and spans that run across lines, which leaves 19 entities and 43 mention edges. Most are real
  (The Model Context Protocol, Open Knowledge Format, Google Cloud), but some are still fragments ("In June",
  "Enterprise Generative"), so the layer stays off. The canary lists every entity it keeps, so you can judge.
- Worth trying next: the `llm` method (`SEMANTICA_NER_METHOD=llm`, provider Anthropic, `claude-haiku-5-5`), which needs
  `ANTHROPIC_API_KEY`. Turn the layer on (`GRAPH_EXTRACTOR=semantica`) only after the canary's entity list looks useful.

## The website

`muthub-ai/knowledge-foundation-site` builds wiki.muthub.org from each release; its README covers the Vercel project
(created October 17, 2026; the domain is verified). One step remains: save the project's deploy hook here as
`VERCEL_DEPLOY_HOOK`, so each release rebuilds the site.

## Licences

Code: MIT (`LICENSE`), except `tools/librarian/` and `tests/test_flow.py`, which import LLM-Wiki-V2 and are
AGPL-3.0-or-later (`LICENSES/README.md`). Notes: CC BY 4.0 (`CONTENT-LICENSE`).
