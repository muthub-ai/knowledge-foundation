"""Build the published graph from the bundle (ADR 009).

Deterministic backbone, no model calls: notes, themes and sources are nodes; typed relations, links, folder
membership and sources are edges. The semantic layer (an extractor behind the adapter interface) adds entities the
notes mention. Positions and communities are computed here so the browser only draws.

Outputs: graph.json (schemas/graph.schema.json), graph.graphml (Gephi and networkx), report.md.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import jsonschema
import networkx as nx

from . import okf
from .config import Config
from .extractors import Extraction, Extractor, ExtractorUnavailable, NoteText

SCHEMA_VERSION = "1.0"


def page_url(rel: str) -> str:
    """Site URL of a note: the bundle path without .md (the site builder uses the same rule)."""
    return "/" + re.sub(r"\.md$", "", rel)


def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]
    # A label with no ASCII letters or digits still gets its own id, not a shared "entity".
    return s or "entity-" + hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]


def _day(ts: Any) -> str:
    text = str(ts or "")
    return text[:10] if re.match(r"\d{4}-\d{2}-\d{2}", text) else "1970-01-01"


def _opt_day(ts: Any) -> str:
    """A date when there is one, else "" (unlike _day, which gives sorting-safe 1970 for a missing timestamp)."""
    text = str(ts or "")
    return text[:10] if re.match(r"\d{4}-\d{2}-\d{2}", text) else ""


def _human_verified(fm: dict[str, Any]) -> str:
    """Day of the latest human verification; "" when no human has reviewed the note yet."""
    return max((_opt_day(v.get("at")) for v in okf.verifications(fm) if str(v.get("by", "")).startswith("human:")), default="")


def _source_date(fm: dict[str, Any], raws: dict[str, Any]) -> str:
    """Earliest publication day among the note's dated sources; "" when none is dated."""
    days = []
    for s in fm.get("sources") or []:
        res = str(s.get("resource", "")) if isinstance(s, dict) else ""
        raw = raws.get(res.lstrip("/")) if res.startswith("/") else None
        d = _opt_day(raw.frontmatter.get("published_at")) if raw is not None else ""
        if d:
            days.append(d)
    return min(days, default="")


def build(bundle: Path, cfg: Config, extractor: Extractor | None = None, *, revision: str = "") -> tuple[dict[str, Any], str]:
    G = nx.DiGraph()
    notes = list(okf.notes(bundle))
    raws = {d.rel: d for d in okf.raws(bundle)}
    note_ids = {n.rel for n in notes}
    aliases: dict[str, str] = {}

    for theme, desc in cfg.themes.items():
        if (bundle / theme).is_dir():
            G.add_node(f"theme:{theme}", type="Theme", label=cfg.theme_label(theme), url=f"/{theme}",
                       summary=desc[:300], trust="human-reviewed", status="stable", updated=_day(None), tags=[])

    for n in notes:
        fm = n.frontmatter
        G.add_node(n.rel, type=str(fm.get("kind") or "Concept"), label=str(fm.get("title") or n.rel), url=page_url(n.rel),
                   summary=str(fm.get("description") or "")[:300], trust=okf.trust_tier(fm), status=str(fm.get("status") or "draft"),
                   updated=_day((fm.get("generated") or {}).get("at") if isinstance(fm.get("generated"), dict) else None),
                   tags=[str(t) for t in fm.get("tags") or []], canonical=str(fm.get("canonical_essay") or ""),
                   verified=_human_verified(fm), stale_after=_opt_day(fm.get("stale_after")), source_date=_source_date(fm, raws))
        aliases[str(fm.get("title") or "").lower()] = n.rel
        for a in fm.get("aliases") or []:
            aliases[str(a).lower()] = n.rel

    def edge(s: str, t: str, typ: str, origin: str, evidence: str) -> None:
        if s == t or not G.has_node(s) or not G.has_node(t):
            return
        if G.has_edge(s, t) and G.edges[s, t]["origin"] == "frontmatter":
            return  # a typed relation wins over an untyped duplicate
        G.add_edge(s, t, type=typ, origin=origin, evidence=evidence, weight=1.0)

    for n in notes:
        fm = n.frontmatter
        top = n.top_folder
        if top and G.has_node(f"theme:{top}"):
            edge(n.rel, f"theme:{top}", "in_folder", "folder", n.rel)
        for link in okf.MD_LINK.findall(n.body):
            target = okf.resolve_link(bundle, n.rel, link)
            if target in note_ids:
                edge(n.rel, target, "links_to", "link", n.rel)
        for s in fm.get("sources") or []:
            res = str(s.get("resource", "")) if isinstance(s, dict) else ""
            raw = raws.get(res.lstrip("/")) if res.startswith("/") else None
            if raw is None:
                continue
            if not G.has_node(raw.rel):
                rfm = raw.frontmatter
                ext = str(rfm.get("resource") or "")
                G.add_node(raw.rel, type="Source", label=str(rfm.get("title") or raw.rel), url=ext if ext.startswith("http") else page_url(raw.rel),
                           summary=f"Published {rfm.get('published_at', 'n.d.')}"[:300], trust="human-reviewed" if str(rfm.get("origin_kind", "")).startswith("own") else "unverified",
                           status="stable", updated=_day(rfm.get("published_at")), tags=[])
            edge(n.rel, raw.rel, "draws_on", "source", str(s.get("id")))
        for r in fm.get("relations") or []:
            if not isinstance(r, dict):
                continue
            target = okf.resolve_link(bundle, n.rel, str(r.get("target", "")))
            if target in note_ids:
                if G.has_edge(n.rel, target):
                    G.remove_edge(n.rel, target)
                edge(n.rel, target, str(r.get("type")), "frontmatter", n.rel)

    report_lines: list[str] = []
    extraction = Extraction()
    if extractor is not None:
        texts = [NoteText(n.rel, str(n.frontmatter.get("title") or ""), n.body) for n in notes]
        try:
            extraction = extractor.extract(texts)
        except ExtractorUnavailable as e:
            report_lines.append(f"- Semantic layer skipped: {e}. The deterministic graph was published.")
        for ent in extraction.entities:
            target = aliases.get(ent.label.lower()) or f"ext:{_slug(ent.label)}"
            if not G.has_node(target):
                G.add_node(target, type=ent.type, label=ent.label, url="", summary=f"Mentioned in {len(ent.mentioned_in)} note(s); no note yet",
                           trust="machine-confirmed", status="draft", tags=[],
                           # The newest mentioning note's date, not today's: graph.json stays the same between builds.
                           updated=max((G.nodes[m]["updated"] for m in ent.mentioned_in if m in G), default=_day(None)))
            for nid in ent.mentioned_in:
                if not G.has_edge(nid, target):
                    edge(nid, target, "mentions", "extracted", f"ext:{extraction.extractor}")
        report_lines += [f"- Extractor note: {m}" for m in extraction.notes]

    G.remove_nodes_from([n for n, d in G.nodes(data=True) if d["type"] == "Theme" and G.degree(n) == 0])  # empty themes
    U = G.to_undirected()
    pos = nx.spring_layout(U, seed=42, k=2.5 / max(len(U), 1) ** 0.5, iterations=300) if len(U) else {}
    communities = nx.community.louvain_communities(U, seed=42) if len(U) else []
    community_of = {node: i for i, group in enumerate(sorted(communities, key=len, reverse=True)) for node in group}

    nodes = []
    for node, data in G.nodes(data=True):
        x, y = pos.get(node, (0.0, 0.0))
        nodes.append({"id": node, **{k: data[k] for k in ("type", "label", "url", "summary", "trust", "status", "updated", "tags")},
                      **{k: data[k] for k in ("canonical", "verified", "stale_after", "source_date") if data.get(k)},
                      "degree": int(U.degree(node)), "community": int(community_of.get(node, 0)),
                      "x": round(float(x) * 1000, 2), "y": round(float(y) * 1000, 2)})
    edges = [{"source": s, "target": t, **{k: d[k] for k in ("type", "origin", "evidence", "weight")}} for s, t, d in G.edges(data=True)]

    node_types = sorted({n["type"] for n in nodes})
    graph = {
        "version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_revision": revision,
        "ontology": {
            "node_types": [{"id": t, "label": t, "description": f"{t} node"} for t in node_types],
            "edge_types": [{"id": e["id"], "label": e["label"], "description": e["description"]} for e in cfg.edge_types],
        },
        "nodes": sorted(nodes, key=lambda n: n["id"]),
        "edges": sorted(edges, key=lambda e: (e["source"], e["target"])),
    }
    jsonschema.validate(graph, cfg.schema("graph"))

    by_type: dict[str, int] = {}
    for n in nodes:
        by_type[n["type"]] = by_type.get(n["type"], 0) + 1
    orphans = [n["id"] for n in nodes if n["degree"] == 0]
    central = sorted((n for n in nodes if not n["id"].startswith(("theme:", "raw/"))), key=lambda n: -n["degree"])[:10]
    report = "\n".join([
        "# Graph report", "",
        f"Revision {revision or 'working tree'}; {len(nodes)} nodes, {len(edges)} edges, {len(communities)} communities.", "",
        "## Nodes by type", "", *[f"- {t}: {c}" for t, c in sorted(by_type.items())], "",
        "## Most connected notes", "", *[f"- {n['label']} ({n['degree']})" for n in central], "",
        "## Orphans", "", *([f"- {o}" for o in orphans] or ["- none"]), "",
        "## Semantic layer", "", f"- Extractor: {extraction.extractor}", f"- Entities: {len(extraction.entities)}", *report_lines, "",
    ])
    return graph, report


def write_outputs(graph: dict[str, Any], report: str, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / "graph.json").write_text(json.dumps(graph, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (out / "report.md").write_text(report, encoding="utf-8")
    G = nx.DiGraph()
    for n in graph["nodes"]:
        G.add_node(n["id"], **{k: (", ".join(v) if isinstance(v, list) else v) for k, v in n.items() if k != "id"})
    for e in graph["edges"]:
        G.add_edge(e["source"], e["target"], **{k: v for k, v in e.items() if k not in ("source", "target")})
    nx.write_graphml(G, out / "graph.graphml")
