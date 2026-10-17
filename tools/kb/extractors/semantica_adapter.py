"""Semantica behind the extractor interface.

Semantica (MIT, semantica-agi/semantica) treats Markdown as plain text and flattens files before extraction, so
this adapter walks notes one at a time and keeps the note id on every entity itself. Settings come from the
environment so CI can choose the method without code changes:

  SEMANTICA_NER_METHOD        ml (local spaCy, default), llm, pattern
  SEMANTICA_RELATION_METHOD   pattern (default), llm, dependency
  SEMANTICA_PROVIDER          openai, anthropic, gemini, ollama, litellm ... (only for the llm methods)
  SEMANTICA_MODEL             model name for the provider

The import is lazy: without Semantica installed the adapter raises ExtractorUnavailable and the build publishes the
deterministic graph. Pinned in requirements-graph.txt; a breaking release fails the adapter test, not production.
"""

from __future__ import annotations

import os
import re
from typing import Any

from . import Entity, Extraction, ExtractorUnavailable, NoteText, Relation

_TYPE_MAP = {
    "PERSON": "Person", "PER": "Person",
    "ORG": "Organization", "ORGANIZATION": "Organization", "COMPANY": "Organization",
    "PRODUCT": "Tool", "SOFTWARE": "Tool", "TOOL": "Tool", "TECHNOLOGY": "Tool",
    "STANDARD": "Standard", "LAW": "Standard", "PROTOCOL": "Standard",
}


# Things Semantica's pattern and ml extractors report as entities that are not entities in a wiki of essays: years and
# other numbers, the section headings every note has, and the note's own headings (found by the canary, October 2026).
_NOT_ENTITIES = {"overview", "read the original", "sources", "source", "see also", "summary", "introduction", "conclusion",
                 "notes", "note", "contents", "references", "background", "context", "key points", "takeaways"}
_NUMBERISH = re.compile(r"[\d\s.,:/%$-]+|(q[1-4]|fy|h[12])\s*\d{2,4}", re.I)


def _headings(text: str) -> set[str]:
    return {m.group(1).strip().lower() for m in re.finditer(r"^#{1,6}\s+(.+?)\s*#*$", text, flags=re.M)}


def _is_entity(label: str, note: NoteText, headings: set[str]) -> bool:
    # Pattern matching also returns spans that run from a heading into the next paragraph: an entity is one short line.
    if "\n" in label or len(label) > 60 or len(label.split()) > 6:
        return False
    low = label.lower()
    return (len(label) >= 3 and low != note.title.lower() and low not in _NOT_ENTITIES and low not in headings
            and not _NUMBERISH.fullmatch(label))


def _load_builder() -> Any:
    try:
        from semantica.kg import GraphBuilder  # type: ignore[import-not-found]
    except Exception as e:  # ImportError, or a broken release raising at import time
        raise ExtractorUnavailable(f"semantica is not importable: {e}") from e
    kwargs: dict[str, Any] = {"merge_entities": True, "entity_resolution_strategy": "fuzzy", "resolve_conflicts": True}
    if os.environ.get("SEMANTICA_PROVIDER"):
        kwargs["provider"] = os.environ["SEMANTICA_PROVIDER"]
    if os.environ.get("SEMANTICA_MODEL"):
        kwargs["llm_model"] = os.environ["SEMANTICA_MODEL"]
    return GraphBuilder(**kwargs)


def _label(e: Any) -> str:
    if isinstance(e, dict):
        return str(e.get("text") or e.get("name") or e.get("label") or e.get("id") or "").strip()
    return str(getattr(e, "text", None) or getattr(e, "name", None) or getattr(e, "label", "") or "").strip()


def _etype(e: Any) -> str:
    raw = (e.get("type") or e.get("label_type") or e.get("entity_type")) if isinstance(e, dict) else getattr(e, "type", None)
    return _TYPE_MAP.get(str(raw or "").upper(), "Concept")


def _rel_ends(r: Any) -> tuple[str, str, str]:
    get = (lambda k: r.get(k)) if isinstance(r, dict) else (lambda k: getattr(r, k, None))
    src, tgt = get("source") or get("subject"), get("target") or get("object")
    return _label(src) if not isinstance(src, str) else src, _label(tgt) if not isinstance(tgt, str) else tgt, str(get("type") or get("predicate") or "mentions")


class SemanticaExtractor:
    name = "semantica"

    def __init__(self, builder: Any | None = None) -> None:
        self._builder = builder  # injectable for tests

    def extract(self, notes: list[NoteText]) -> Extraction:
        builder = self._builder or _load_builder()
        ner = os.environ.get("SEMANTICA_NER_METHOD", "ml")
        rel = os.environ.get("SEMANTICA_RELATION_METHOD", "pattern")
        out = Extraction(extractor=f"semantica:{ner}/{rel}")
        by_label: dict[str, Entity] = {}
        for note in notes:
            headings = _headings(note.text)
            try:
                kg = builder.build([note.text], extract_relations=True, ner_method=ner, relation_method=rel)
            except Exception as e:  # one bad note must not sink the build
                out.notes.append(f"{note.id}: extraction failed ({type(e).__name__}: {e})")
                continue
            for e in (kg or {}).get("entities", []) or []:
                label = _label(e)
                if not _is_entity(label, note, headings):
                    continue
                ent = by_label.setdefault(label.lower(), Entity(label=label, type=_etype(e)))
                if note.id not in ent.mentioned_in:
                    ent.mentioned_in.append(note.id)
            for r in (kg or {}).get("relationships", []) or []:
                s, t, typ = _rel_ends(r)
                if s and t and s.lower() != t.lower():
                    out.relations.append(Relation(source=s, target=t, type="mentions" if typ == "mentions" else typ))
        out.entities = sorted(by_label.values(), key=lambda e: e.label.lower())
        return out
