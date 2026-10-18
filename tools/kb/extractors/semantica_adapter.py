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

import logging
import os
import re
import time
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


def _patch_anthropic_provider() -> None:
    """Semantica 0.7.0 reads `response.content[0].text` from Anthropic. Current Claude models can answer with a
    thinking block first, which has no `.text`, so every call failed and the layer silently fell back to patterns.
    Read the text blocks instead (all of them, joined). Remove once Semantica does this itself."""
    try:
        from semantica.semantic_extract import providers as P  # type: ignore[import-not-found]
    except Exception:
        return
    cls = getattr(P, "AnthropicProvider", None)
    if cls is None or getattr(cls, "_kf_patched", False):
        return

    def text_of(response: Any) -> str:
        parts = [getattr(b, "text", "") for b in getattr(response, "content", []) or [] if getattr(b, "type", "text") == "text"]
        return "".join(parts).strip()

    def create(self: Any, prompt: str, kwargs: dict[str, Any]) -> Any:
        if not self.client:
            raise P.ProcessingError("Anthropic client not initialized. Set ANTHROPIC_API_KEY or pass api_key.")
        args: dict[str, Any] = {"model": kwargs.get("model", self.model), "max_tokens": kwargs.get("max_tokens", 8192),
                                "messages": [{"role": "user", "content": prompt}]}
        for k in ("temperature", "top_p", "top_k", "stop_sequences", "system", "metadata"):
            if k in kwargs:
                args[k] = kwargs[k]
        return self.client.messages.create(**args)

    def generate(self: Any, prompt: str, **kwargs: Any) -> str:
        return text_of(create(self, prompt, kwargs))

    def generate_structured(self: Any, prompt: str, **kwargs: Any) -> Any:
        response = create(self, f"{prompt}\n\nReturn the response as valid JSON only.", kwargs)
        try:
            return self._parse_json(text_of(response))
        except Exception as e:
            raise P.ProcessingError(f"Failed to parse JSON from Anthropic response: {e}") from e

    cls.generate, cls.generate_structured, cls._kf_patched = generate, generate_structured, True


def _load_builder() -> Any:
    try:
        from semantica.kg import GraphBuilder  # type: ignore[import-not-found]
    except Exception as e:  # ImportError, or a broken release raising at import time
        raise ExtractorUnavailable(f"semantica is not importable: {e}") from e
    _patch_anthropic_provider()
    kwargs: dict[str, Any] = {"merge_entities": True, "entity_resolution_strategy": "fuzzy", "resolve_conflicts": True}
    if os.environ.get("SEMANTICA_PROVIDER"):
        kwargs["provider"] = os.environ["SEMANTICA_PROVIDER"]
    if os.environ.get("SEMANTICA_MODEL"):
        kwargs["llm_model"] = os.environ["SEMANTICA_MODEL"]
    try:
        return GraphBuilder(**kwargs)
    except Exception as e:  # e.g. the llm method without an API key: publish the deterministic graph instead
        raise ExtractorUnavailable(f"semantica could not start: {e}") from e


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
        # Semantica's default "fallback" strategy quietly substitutes pattern matching when a method fails (an LLM
        # call that errors looks exactly like a pattern run). "union" keeps only what the requested method found, and
        # the library's warnings are collected so the report says why a method produced nothing.
        extra: dict[str, Any] = {"merge_strategy": "union"} if ner != "pattern" else {}
        warnings = _Warnings()
        logging.getLogger("semantica").addHandler(warnings)
        started, slowest = time.monotonic(), (0.0, "")
        for note in notes:
            headings = _headings(note.text)
            t0 = time.monotonic()
            try:
                kg = builder.build([note.text], extract_relations=True, ner_method=ner, relation_method=rel, **extra)
            except Exception as e:  # one bad note must not sink the build
                out.notes.append(f"{note.id}: extraction failed ({type(e).__name__}: {e})")
                continue
            finally:
                took = time.monotonic() - t0
                slowest = max(slowest, (took, note.id))
                print(f"semantica {ner}: {note.id} in {took:.1f}s", flush=True)
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
        logging.getLogger("semantica").removeHandler(warnings)
        out.notes.append(f"{ner} pass: {len(notes)} notes in {time.monotonic() - started:.0f}s, slowest {slowest[1]} at {slowest[0]:.0f}s")
        out.notes.extend(f"semantica warned: {w}" for w in warnings.seen[:5])
        out.entities = sorted(by_label.values(), key=lambda e: e.label.lower())
        return out


class _Warnings(logging.Handler):
    """Distinct warning and error messages Semantica logged during a build (its method failures are only logged)."""

    def __init__(self) -> None:
        super().__init__(level=logging.WARNING)
        self.seen: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        text = " ".join(record.getMessage().split())[:300]
        if text not in self.seen:
            self.seen.append(text)
