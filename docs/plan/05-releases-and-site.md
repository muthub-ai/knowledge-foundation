# 5. Releases and the website

**Outcome:** every merge to `main` produces a versioned release, and the wiki site rebuilds from it within minutes.

## Steps

1. **Release on merge** (`publish.yml`): build the graph, `tar czf dist/bundle.tgz wiki wiki.config.yaml schemas
   ontology`, create release `kf-YYYY.MM.DD-N` with `bundle.tgz`, `graph.json`, `graph.graphml`, `report.md`.
   Nothing in this workflow pushes to `main` (ADR 004).
2. **Build the site repository** following
   [knowledge-foundation-site/docs/plan](https://github.com/muthub-ai/knowledge-foundation-site/tree/main/docs/plan).
   It downloads the latest release (or `KF_RELEASE`) and never imports code from this repository.
3. **Deploy hook:** in the wiki's Vercel project, Settings → Git → Deploy Hooks, create a hook for `main`; save its URL
   as the `VERCEL_DEPLOY_HOOK` secret here. `publish.yml` calls it after the release exists.
4. **Essays site link** (ADR 015): muthub.org reads `https://<wiki>/graph.json` hourly for its counts, with a fallback.

## Check it worked

- Merge a small change: a new release appears, and a new production deployment of the wiki starts seconds later.
- `https://<wiki>/graph.json` has `source_revision` equal to the merge commit.

## Gotchas

- If the site deploys before the release exists (e.g. both repositories merged at once), redeploy the site after
  `publish` finishes, or rely on the hook from the next release.
- Release asset downloads work through the REST API (`Accept: application/octet-stream`) even where Actions artifacts
  and logs are not reachable.
