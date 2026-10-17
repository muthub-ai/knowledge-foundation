# SPDX-License-Identifier: AGPL-3.0-or-later
# This script imports LLM-Wiki-V2 (AGPL-3.0-or-later), so it is licensed the same way. See LICENSES/README.md.
"""Seed the wiki from muthub.org without any model call.

Every essay, note, playbook and initiative on the site is the author's own published work, so each is kept in full
as a raw copy (OKF type Source) and summarized as one note in its theme folder, written through LLM-Wiki-V2's own
store so the bundle is exactly what the Librarian would maintain. Related pieces are joined with See-also links,
series parts with `builds_on` relations. Later sources go through `llmwiki2 ingest` (CROW) as usual.

Input: a JSON dump of the site's content folder (see tools/librarian/dump-site-content.js).
Usage: PYTHONPATH=tools python tools/librarian/seed_from_site.py site-content.json --initiatives-date 2026-10-17
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from llmw2.bundle.store import WikiStore  # type: ignore[import-not-found]
from llmw2.bundle.tree import Folder  # type: ignore[import-not-found]

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kb import okf  # noqa: E402
from kb.config import Config  # noqa: E402
from kb.governance import _add_months  # noqa: E402

ACTOR = "seed-import/1.0"
SITE = "https://muthub.org"

# Where pieces without a theme on the site belong. Reviewed by hand; move a note with `llmwiki2 move` to change it.
THEME_OF = {
    # notes
    "living-documentation-trust-gap": "context-engineering",
    "from-pair-programming-to-fleet-management": "ai-native-sdlc",
    "ai-is-an-amplifier": "leading-ai-change",
    "spec-kit-beyond-vibe-coding": "ai-native-sdlc",
    "closing-the-loop": "ai-native-sdlc",
    "agent-design-is-still-hard": "ai-native-sdlc",
    "bigquery-data-engineering-agent": "data-ai-platforms",
    "technical-debt-is-an-architectural-liability": "leading-ai-change",
    "mcp-tools-resources-prompts": "governed-ai",
    "mcp-connector-messages-api": "governed-ai",
    "the-mcp-spec-grows-up": "governed-ai",
    "a2a-and-mcp": "governed-ai",
    "ai-generated-assertions": "ai-native-sdlc",
    "build-for-today-or-tomorrow": "leading-ai-change",
    "unified-governance-in-the-catalog": "data-ai-platforms",
    "rethinking-oltp-for-agents": "data-ai-platforms",
    "audit-your-year-with-ai": "leading-ai-change",
    "simplicity-in-architecture": "leading-ai-change",
    # initiatives
    "ai-augmented-sdlc": "ai-native-sdlc",
    "architecture-as-code": "governed-ai",
    "aac-reference-platform": "governed-ai",
    "enterprise-genai-architecture": "governed-ai",
    "multi-cloud-ai-strategy": "leading-ai-change",
    "controlled-data-movement-archetype": "data-ai-platforms",
    "unified-ml-platform": "data-ai-platforms",
    "data-analytics-platform-usaa": "data-ai-platforms",
    "enterprise-iam-oracle": "governed-ai",
    "middleware-platforms-bunge": "data-ai-platforms",
    # playbooks
    "governing-coding-agents": "ai-native-sdlc",
    "ai-operating-model-for-a-bank": "leading-ai-change",
    "gating-ai-investment": "leading-ai-change",
}


def blocks_to_markdown(blocks: list[dict[str, Any]]) -> str:
    out: list[str] = []
    for b in blocks:
        t = b.get("type")
        if t == "p":
            out.append(b["text"])
        elif t == "h2":
            out.append(f"## {b['text']}")
        elif t in ("ul", "monday"):
            if t == "monday":
                out.append("**What to do on Monday morning:**")
            out.append("\n".join(f"- {i}" for i in b["items"]))
        elif t == "ol":
            out.append("\n".join(f"{n}. {i}" for n, i in enumerate(b["items"], 1)))
        elif t == "quote":
            out.append(f"> {b['text']}")
        elif t == "code":
            out.append(f"```{b.get('lang', '')}\n{b['text']}\n```")
        elif t == "bottomLine":
            out.append(f"**Bottom line:** {b['text']}")
        elif t == "figure":
            continue  # diagrams live on the site
    return "\n\n".join(out)


def first_paragraphs(blocks: list[dict[str, Any]], n: int = 2) -> list[str]:
    return [b["text"] for b in blocks if b.get("type") == "p"][:n]


def essay_note_body(e: dict[str, Any], url: str, kind_word: str) -> str:
    heads = [b["text"] for b in e["body"] if b.get("type") == "h2"]
    bottom = next((b["text"] for b in e["body"] if b.get("type") == "bottomLine"), "")
    lines = ["# Overview", "", f"{e['summary']}[^s1]", ""]
    if heads:
        lines += ["# What it covers", "", *[f"- {h}" for h in heads], ""]
    if bottom:
        lines += ["# Bottom line", "", bottom, ""]
    lines += ["# Read the original", "", f"The full {kind_word} is on muthub.org: [{e['title']}]({url}).", ""]
    lines += [f"[^s1]: {e['title']}, muthub.org, {e.get('updated') or e.get('published')}."]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("content", type=Path)
    ap.add_argument("--initiatives-date", required=True, help="date the initiative pages were last revised (git log of content/initiatives.ts)")
    args = ap.parse_args()
    cfg = Config()
    data = json.loads(args.content.read_text(encoding="utf-8"))
    store = WikiStore(cfg.bundle, actor=ACTOR)
    store.init()
    root = store.load()
    folders: dict[str, Folder] = {}
    for name, desc in cfg.themes.items():
        folders[name], _ = store.create_folder(root, name, desc)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    by_slug: dict[str, Any] = {}

    def add(piece: dict[str, Any], *, kind: str, theme: str, url: str, md_url: str, published: str, raw_text: str, body: str, tags: list[str]) -> None:
        raw_rel = store.save_raw(raw_text, title=piece["title"], resource=md_url)
        raw = okf.read(cfg.bundle / raw_rel.lstrip("/"), cfg.bundle)
        raw.frontmatter.update({"published_at": published, "origin_kind": "own-essay" if kind == "Essay" else "own-post",
                                "license_note": "Own work by the author; reproduced in full", "author": cfg.owner_actor})
        okf.write(raw)
        note = store.write_note(folders[theme], title=piece["title"], summary=piece["summary"], body=body,
                                tags=tags, source={"resource": raw_rel, "title": piece["title"]})
        doc = okf.read(note.path, cfg.bundle)
        doc.frontmatter.update({"kind": kind, "status": "draft", "stale_after": _add_months(now, cfg.stale_months(kind)),
                                "classification": "public", "owner": cfg.owner_actor, "canonical_essay": url})
        okf.write(doc)
        note.frontmatter = doc.frontmatter
        by_slug[piece["slug"]] = note

    for e in data["essays"] + data["notes"]:
        if e.get("status") not in (None, "published"):
            continue
        theme = e.get("theme") or THEME_OF[e["slug"]]
        url = f"{SITE}/writing/{e['slug']}"
        raw_text = "\n\n".join([f"# {e['title']}", f"Published {e['published']}" + (f", updated {e['updated']}" if e.get("updated") else "") + f". {e.get('source', '')}".rstrip(), blocks_to_markdown(e["body"])])
        add(e, kind="Essay", theme=theme, url=url, md_url=url + ".md", published=e.get("updated") or e["published"], raw_text=raw_text,
            body=essay_note_body(e, url, "essay" if e in data["essays"] else "note"), tags=[theme])

    for pb in data["playbooks"]:
        url = f"{SITE}/playbooks/{pb['slug']}"
        raw_text = "\n\n".join([f"# {pb['title']}", f"Reviewed {pb['reviewed']}.", *pb["intro"],
                                *[f"## {i + 1}. {it['title']}\n\n{it['text']}\n\nCheck: {it['check']}" for i, it in enumerate(pb["items"])], pb["closing"]])
        body = "\n".join(["# Overview", "", f"{pb['summary']}[^s1]", "", "# Points", "", *[f"{i + 1}. {it['title']}" for i, it in enumerate(pb["items"])], "",
                          "# Read the original", "", f"The playbook and its self-assessment are on muthub.org: [{pb['title']}]({url}).", "",
                          f"[^s1]: {pb['title']}, muthub.org, reviewed {pb['reviewed']}."])
        add(pb, kind="Playbook", theme=THEME_OF[pb["slug"]], url=url, md_url=url + ".md", published=pb["reviewed"], raw_text=raw_text, body=body, tags=["playbook"])

    for it in data["initiatives"]:
        url = f"{SITE}/initiatives/{it['slug']}"
        sections = [(k.capitalize(), it.get(k)) for k in ("problem", "approach", "governance", "outcome", "lesson")]
        raw_text = "\n\n".join([f"# {it['title']}", f"{it.get('organization', '')}, {it.get('period', '')}. Role: {it.get('role', '')}.", it["summary"],
                                *[f"## {name}\n\n" + ("\n".join(f"- {x}" for x in v) if isinstance(v, list) else str(v)) for name, v in sections if v]])
        body = "\n".join(["# Overview", "", f"{it['summary']}[^s1]", "", f"Organization: {it.get('organization', '')}. Period: {it.get('period', '')}.", "",
                          "# Read the original", "", f"The case study is on muthub.org: [{it['title']}]({url}).", "",
                          f"[^s1]: {it['title']}, muthub.org case study, revised {args.initiatives_date}."])
        add(it, kind="Initiative", theme=THEME_OF[it["slug"]], url=url, md_url=url + ".md", published=args.initiatives_date, raw_text=raw_text, body=body, tags=["initiative"])

    # See-also links from the site's own cross-references.
    for e in data["essays"]:
        for r in e.get("related") or []:
            if e["slug"] in by_slug and r in by_slug:
                store.link(by_slug[e["slug"]], by_slug[r])
    for it in data["initiatives"]:
        for r in it.get("relatedWriting") or []:
            slug = r if isinstance(r, str) else r.get("slug")
            if it["slug"] in by_slug and slug in by_slug:
                store.link(by_slug[it["slug"]], by_slug[slug])

    # Series parts build on the previous part (typed relation).
    series = sorted((e for e in data["essays"] if e.get("series")), key=lambda e: e["series"].get("part", 0) if isinstance(e["series"], dict) else 0)
    for prev, cur in zip(series, series[1:]):
        doc = okf.read(by_slug[cur["slug"]].path, cfg.bundle)
        rels = doc.frontmatter.setdefault("relations", [])
        rels.append({"type": "builds_on", "target": "/" + by_slug[prev["slug"]].rel})
        okf.write(doc)

    store.append_log("Seeded", f"{len(by_slug)} notes from muthub.org (essays, notes, playbooks, initiatives), no model calls", None, None)
    print(f"seeded {len(by_slug)} notes into {cfg.bundle}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
