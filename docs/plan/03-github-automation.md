# 3. GitHub automation: bots propose, the owner approves

**Outcome:** automated work arrives only as pull requests; required checks gate every merge; approving a pull request
stamps `verified` on the notes it changed; merging publishes.

## Steps

1. **Create a GitHub App** (Settings → Developer settings → GitHub Apps → New), e.g. `knowledge-foundation-bot`
   (ADR 005). No webhook. Repository permissions: **Contents: read and write**, **Pull requests: read and write**,
   **Issues: read and write**. Install it on this repository only. Commits and pull requests made with the App's token
   trigger workflows, which the built-in `GITHUB_TOKEN` cannot do.
2. **Secrets and variables** (repository → Settings → Secrets and variables → Actions):

   | Kind | Name | Value |
   | --- | --- | --- |
   | Secret | `ANTHROPIC_API_KEY` | Workspace-scoped Anthropic key (semantic layer, weekly curator, cloud ingest fallback) |
   | Secret | `CONFIDENTIAL_TERMS` | The blocklist, terms separated by `\|`. The checker never prints a matched term |
   | Secret | `KF_APP_PRIVATE_KEY` | The App's private key (`.pem` contents) |
   | Secret | `VERCEL_DEPLOY_HOOK` | The wiki project's deploy hook URL (step 5 of plan 05) |
   | Variable | `KF_APP_ID` | The App's ID |
   | Variable | `GRAPH_EXTRACTOR` | optional override: `semantica` (default on release) or `none` |
   | Variable | `SEMANTICA_NER_METHOD`, `SEMANTICA_RELATIONS` | optional overrides: `llm` (default) |

   Secret names allow only letters, digits and underscores, and must not start with `GITHUB_`.
3. **Workflows** (`.github/workflows/`):

   | Workflow | Trigger | Does |
   |---|---|---|
   | `tests.yml` | every pull request and push to `main` | **unit tests** and **bundle rules** (required), plus the advisory Semantica canaries |
   | `approve.yml` | owner approves a pull request | stamps `verified: human:<owner>` on changed notes, with the App's token, on the exact approved commit |
   | `publish.yml` | push to `main` | builds the graph (with the semantic layer), cuts release `kf-YYYY.MM.DD-N`, calls the deploy hook |
   | `weekly.yml` | Mondays | deterministic checks, then the curator's lint and consolidation; issue plus a fixes pull request; capped spend |
   | `ingest.yml` | manual | cloud fallback ingest in classic mode |

   `.github/ci-run.sh` copies the tail of a failing step into a check annotation, so failures are readable from the
   Checks API even when logs are not.
4. **Branch protection on `main`:** require a pull request, required checks **unit tests** and **bundle rules**, block
   force pushes, include administrators. Leave "Dismiss stale approvals" off (the stamp commit would dismiss the
   approval). Turn on "Require review from Code Owners" (`.github/CODEOWNERS`) once pull requests come from the App:
   GitHub does not let you approve a pull request opened under your own account.
5. **Dependabot** (`.github/dependabot.yml`) for pip and Actions; Dependabot pull requests run the same checks.

## Check it worked

- Open a trivial pull request: both required checks run and pass; the canaries report entities in their annotations.
- Approve an App-authored pull request: a stamp commit appears on the branch, and the checks run again on it.
- Merge: `publish` creates a release with `bundle.tgz`, `graph.json`, `graph.graphml`, `report.md`.

## Gotchas

- Required checks are matched by **job name**; renaming a job silently un-requires it.
- An `if:` on a whole job skips it, and a skipped required check counts as passing. Guard steps, not jobs, when the
  check must run.
- The approve workflow only stamps when the reviewer is the repository owner, and only the commit that was approved.
