"""Semantica behind the extractor interface.

Semantica (MIT, semantica-agi/semantica) treats Markdown as plain text and flattens files before extraction, so
this adapter walks notes one at a time and keeps the note id on every entity itself. Settings come from the
environment so CI can choose the method without code changes:

  SEMANTICA_NER_METHOD        ml (local spaCy, default), llm, pattern
  SEMANTICA_RELATION_METHOD   pattern (default), llm, dependency
  SEMANTICA_PROVIDER          openai, anthropic, gemini, ollama, litellm ... (only for the llm methods)
  SEMANTICA_MODEL             model name for the provider
  SEMANTICA_RELATIONS         llm: also propose typed relations between notes and run the model pass of entity
                              resolution (off by default; needs the llm provider settings)

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
from . import relations as rels
from .resolution import resolve

# The five entity types of the extracted layer (Muthu, October 18, 2026). The model is asked for exactly these; what
# it returns anyway is mapped onto them, and people, places, dates and amounts are dropped.
ENTITY_TYPES = ["Concept", "Standard", "Tool", "Organization", "Practice"]
_TYPE_MAP = {
    "CONCEPT": "Concept", "IDEA": "Concept", "TECHNOLOGY": "Concept", "FIELD": "Concept", "TOPIC": "Concept",
    "STANDARD": "Standard", "PROTOCOL": "Standard", "SPECIFICATION": "Standard", "SPEC": "Standard", "FORMAT": "Standard",
    "LAW": "Standard", "REGULATION": "Standard", "FRAMEWORK": "Standard",
    "TOOL": "Tool", "PRODUCT": "Tool", "SOFTWARE": "Tool", "PLATFORM": "Tool", "SERVICE": "Tool", "LIBRARY": "Tool",
    "LANGUAGE": "Tool", "MODEL": "Tool",
    "ORG": "Organization", "ORGANIZATION": "Organization", "ORGANISATION": "Organization", "COMPANY": "Organization",
    "INSTITUTION": "Organization", "VENDOR": "Organization",
    "PRACTICE": "Practice", "METHOD": "Practice", "METHODOLOGY": "Practice", "PATTERN": "Practice", "PROCESS": "Practice",
    "TECHNIQUE": "Practice", "APPROACH": "Practice",
}
_EXCLUDED_TYPES = {"PERSON", "PER", "PEOPLE", "GPE", "LOC", "LOCATION", "PLACE", "DATE", "TIME", "EVENT", "MONEY",
                   "QUANTITY", "PERCENT", "CARDINAL", "ORDINAL", "NORP", "FAC", "ROLE", "TITLE", "JOB_TITLE"}


# Things Semantica's pattern and ml extractors report as entities that are not entities in a wiki of essays: years and
# other numbers, the section headings every note has, and the note's own headings (found by the canary, October 2026).
_NOT_ENTITIES = {"overview", "read the original", "sources", "source", "see also", "summary", "introduction", "conclusion",
                 "notes", "note", "contents", "references", "background", "context", "key points", "takeaways"}
_NUMBERISH = re.compile(r"[\d\s.,:/%$-]+|(q[1-4]|fy|h[12])\s*\d{2,4}", re.I)
# Not knowledge, however often the model returns them: dates and date ranges, durations and quantities ("3 years",
# "25B+ records a day"), version numbers, bare month names, and host names (every note cites muthub.org).
_MONTHS = "january|february|march|april|may|june|july|august|september|october|november|december"
_NOISE = re.compile(
    rf"({_MONTHS})(\s+\d{{4}})?|\d{{4}}\s*[–-]\s*(\d{{4}}|present)|\d[\d.,]*\s*[a-z+%]*\s+(years?|months?|weeks?|days?|hours?|minutes?|seconds?)\b.*"
    rf"|\d[\d.,]*[kmbt]?\+?\s+\w+(\s+(a|per)\s+\w+)?|v?\d+(\.\d+)+|[a-z0-9-]+(\.[a-z0-9-]+)*\.(org|com|net|io|ai|dev|app)(/\S*)?",
    re.I,
)


def _headings(text: str) -> set[str]:
    return {m.group(1).strip().lower() for m in re.finditer(r"^#{1,6}\s+(.+?)\s*#*$", text, flags=re.M)}


# Generic words the model returns as "concepts" when asked for typed entities (canary, October 18, 2026). A wiki
# entity is a named thing or a term of art, not an everyday noun.
_GENERIC = {"code", "systems", "system", "standards", "tests", "test", "production", "knowledge", "enterprise", "prompts",
            "resources", "schemas", "tools", "tool", "platform", "models", "model", "data", "teams", "use cases", "decisions",
            "controls", "policy", "reviews", "incidents", "tickets", "commits", "chat", "calendar", "editors", "clarity",
            "fluency", "influence", "authority", "maturity", "autonomy", "security", "simplicity", "analytics", "application",
            "compute", "metadata", "portfolio", "licenses", "license costs", "rewrite", "paydown", "pilots", "lifecycle",
            "reinforcement", "personal growth", "firefighting", "distill", "bank", "architecture", "documentation"}
_PHRASE = re.compile(r"(the|a|an|our|my|your|how|why|what|when)\s+\S+\s+\S+.*", re.I)


def _is_entity(label: str, note: NoteText, headings: set[str], titles: frozenset[str] = frozenset()) -> bool:
    # Pattern matching also returns spans that run from a heading into the next paragraph: an entity is one short line.
    if "\n" in label or len(label) > 60 or len(label.split()) > 6 or "://" in label:
        return False
    low = label.lower()
    return (len(label) >= 3 and low != note.title.lower() and low not in _NOT_ENTITIES and low not in headings
            and low not in _GENERIC and low not in titles and not _PHRASE.fullmatch(label)
            and not _NUMBERISH.fullmatch(label) and not _NOISE.fullmatch(label))


def _titles(notes: list[NoteText]) -> frozenset[str]:
    """Every note's title, and the part before its colon: a note named as an entity is the note, not an entity."""
    out = set()
    for n in notes:
        t = n.title.strip().lower()
        out |= {t, t.split(":")[0].strip()}
    return frozenset(x for x in out if x)


def _keep(e: Entity) -> bool:
    """Publish an entity that connects notes (two or more), or a named standard, tool or organisation (capitalised)
    even when one note mentions it. A one-off generic concept adds a dot, not knowledge."""
    from .resolution import is_acronym
    return (len(e.mentioned_in) >= 2 or is_acronym(e.label)
            or (e.type in ("Standard", "Tool", "Organization") and any(c.isupper() for c in e.label)))


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


def _raw_type(e: Any) -> str:
    raw = (e.get("type") or e.get("label_type") or e.get("entity_type")) if isinstance(e, dict) else getattr(e, "type", None)
    return re.sub(r"[\s/-]+", "_", str(raw or "").strip().upper())


def _etype(e: Any) -> str:
    raw = _raw_type(e)
    return _TYPE_MAP.get(raw) or _TYPE_MAP.get(raw.split("_")[0]) or "Concept"


def _rel_ends(r: Any) -> tuple[str, str, str]:
    get = (lambda k: r.get(k)) if isinstance(r, dict) else (lambda k: getattr(r, k, None))
    src, tgt = get("source") or get("subject"), get("target") or get("object")
    return _label(src) if not isinstance(src, str) else src, _label(tgt) if not isinstance(tgt, str) else tgt, str(get("type") or get("predicate") or "mentions")


class SemanticaExtractor:
    name = "semantica"

    def __init__(self, builder: Any | None = None, resolver: Any | None = None, ask: rels.Ask | None = None) -> None:
        self._builder = builder    # all three injectable for tests
        self._resolver = resolver  # Semantica's EntityResolver.resolve_entities
        self._ask = ask            # prompt -> parsed JSON, through Semantica's provider
        self.known_pairs: set[frozenset[str]] = set()  # note pairs the author already connected (set by kb graph)

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
        if ner == "llm":
            extra["entity_types"] = ENTITY_TYPES
        titles = _titles(notes)
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
                if not _is_entity(label, note, headings, titles) or _raw_type(e) in _EXCLUDED_TYPES:
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
        log = out.notes.append
        want_relations = os.environ.get("SEMANTICA_RELATIONS", "") == "llm"
        ask = self._ask or (_provider_ask() if want_relations else None)
        resolved = resolve(list(by_label.values()), fuzzy=self._resolver or _fuzzy_resolver(),
                           alias_groups=rels.alias_groups_with(ask) if ask else None, log=log)
        out.entities = [e for e in resolved if _keep(e)]
        log(f"kept {len(out.entities)} of {len(resolved)} resolved entities (two or more notes, or a named standard, tool or organisation)")
        if want_relations and ask:
            t0 = time.monotonic()
            out.note_relations = rels.extract_note_relations(notes, out.entities, ask, log=log, known=self.known_pairs)
            log(f"relation pass: {time.monotonic() - t0:.0f}s")
        return out


def _fuzzy_resolver() -> Any:
    try:
        from semantica.kg import EntityResolver  # type: ignore[import-not-found]
        return EntityResolver(strategy="fuzzy", similarity_threshold=0.88).resolve_entities
    except Exception:
        return None


def _provider_ask() -> rels.Ask | None:
    """Semantica's own provider layer, so relation extraction uses the same key, model and patches as entities."""
    try:
        from semantica.semantic_extract.providers import create_provider  # type: ignore[import-not-found]
    except Exception:
        return None
    _patch_anthropic_provider()
    name = os.environ.get("SEMANTICA_PROVIDER", "anthropic")
    kwargs: dict[str, Any] = {"api_key": os.environ.get(f"{name.upper()}_API_KEY")}
    if os.environ.get("SEMANTICA_MODEL"):
        kwargs["model"] = os.environ["SEMANTICA_MODEL"]
    provider = create_provider(name, use_pool=False, **kwargs)

    def ask(prompt: str) -> Any:
        return provider.generate_structured(prompt, max_tokens=4000)
    return ask


class _Warnings(logging.Handler):
    """Distinct warning and error messages Semantica logged during a build (its method failures are only logged)."""

    def __init__(self) -> None:
        super().__init__(level=logging.WARNING)
        self.seen: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        text = " ".join(record.getMessage().split())[:300]
        if text not in self.seen:
            self.seen.append(text)
