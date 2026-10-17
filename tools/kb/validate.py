"""Structural rules for the bundle. Deterministic, no model calls. Complements `llmwiki2 check`.

Rules:
  schema        notes match page.schema.json, raw copies match source.schema.json
  folders       top-level folders are the configured themes (plus raw/); depth is capped
  kind          `kind` is one of the configured kinds
  footnotes     every [^id] in a note has a matching sources[].id, and every source id resolves
  sources       a source pointing into the bundle points at an existing raw copy
  links         every relative Markdown link in a note points at an existing document
  relations     every relation targets an existing note
  canonical     canonical_essay points at the canonical site
  public        every note is classification: public
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import jsonschema

from . import okf
from .config import Config


@dataclass(frozen=True)
class Problem:
    rule: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"[{self.rule}] {self.path}: {self.message}"


def _schema_problems(validator: jsonschema.Draft7Validator, doc: okf.Doc) -> list[Problem]:
    return [
        Problem("schema", doc.rel, f"{'/'.join(str(p) for p in e.absolute_path) or '(root)'}: {e.message}")
        for e in sorted(validator.iter_errors(doc.frontmatter), key=lambda e: list(e.absolute_path))
    ]


def validate(bundle: Path, cfg: Config) -> list[Problem]:
    problems: list[Problem] = []
    page_v = jsonschema.Draft7Validator(cfg.schema("page"), format_checker=jsonschema.FormatChecker())
    source_v = jsonschema.Draft7Validator(cfg.schema("source"), format_checker=jsonschema.FormatChecker())
    themes = set(cfg.themes)
    max_depth = int(cfg.data.get("max_folder_depth", 3))
    canonical = cfg.data["canonical_site"].rstrip("/") + "/"

    try:
        docs = list(okf.documents(bundle))
    except okf.OKFError as e:
        return [Problem("parse", str(bundle), str(e))]
    existing = {d.rel for d in docs}

    for child in sorted(bundle.iterdir()) if bundle.is_dir() else []:
        if child.is_dir() and not child.name.startswith(".") and child.name != okf.RAW and child.name not in themes:
            problems.append(Problem("folders", child.name, "top-level folder is not a configured theme; move its notes into a theme"))
        if child.is_file() and child.suffix == ".md" and child.name not in (okf.INDEX, okf.LOG):
            problems.append(Problem("folders", child.name, "notes may not sit at the bundle root"))

    for doc in docs:
        fm = doc.frontmatter
        if doc.is_raw:
            problems += _schema_problems(source_v, doc)
            continue
        problems += _schema_problems(page_v, doc)
        depth = doc.rel.count("/")
        if depth > max_depth:
            problems.append(Problem("folders", doc.rel, f"deeper than {max_depth} folders"))
        if fm.get("kind") and fm["kind"] not in cfg.kinds:
            problems.append(Problem("kind", doc.rel, f"unknown kind {fm['kind']!r}"))
        if fm.get("classification") not in (None, "public"):
            problems.append(Problem("public", doc.rel, "only public knowledge may enter the wiki"))

        sources = fm.get("sources") if isinstance(fm.get("sources"), list) else []
        ids = {str(s.get("id")) for s in sources if isinstance(s, dict)}
        for ref in sorted(set(okf.FOOTNOTE_REF.findall(doc.body))):
            if ref not in ids:
                problems.append(Problem("footnotes", doc.rel, f"footnote [^{ref}] has no matching source id"))
        for s in sources:
            res = str(s.get("resource", "")) if isinstance(s, dict) else ""
            if res.startswith("/") and res.lstrip("/") not in existing:
                problems.append(Problem("sources", doc.rel, f"source {s.get('id')} points at missing {res}"))

        for link in sorted(set(okf.MD_LINK.findall(doc.body))):
            if "://" not in link and okf.resolve_link(bundle, doc.rel, link) not in existing:
                problems.append(Problem("links", doc.rel, f"link to missing {link}"))

        for rel in fm.get("relations") or []:
            if not isinstance(rel, dict):  # the schema check reports the shape; don't crash on it here
                continue
            target = okf.resolve_link(bundle, doc.rel, str(rel.get("target", "")))
            if target not in existing:
                problems.append(Problem("relations", doc.rel, f"{rel.get('type')} targets missing {rel.get('target')}"))

        ce = fm.get("canonical_essay")
        if ce and not str(ce).startswith(canonical):
            problems.append(Problem("canonical", doc.rel, f"canonical_essay must be on {canonical}"))
    return problems
