"""Entity and relation extractors for the semantic layer of the graph (ADR 009).

Every extractor implements one function, `extract(notes) -> Extraction`. The graph builder never imports an
extraction library directly, so a library that breaks or changes costs one adapter, not the build.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


class ExtractorUnavailable(RuntimeError):
    """The extractor's library or credentials are missing; the build publishes the deterministic graph instead."""


@dataclass
class NoteText:
    id: str          # bundle-relative note path
    title: str
    text: str        # body without frontmatter


@dataclass
class Entity:
    label: str
    type: str                                    # one of the ontology node types, or "Concept"
    mentioned_in: list[str] = field(default_factory=list)


@dataclass
class Relation:
    source: str      # entity label or note id
    target: str
    type: str = "mentions"


@dataclass
class Extraction:
    entities: list[Entity] = field(default_factory=list)
    relations: list[Relation] = field(default_factory=list)
    extractor: str = "none"
    notes: list[str] = field(default_factory=list)   # warnings for the report


class Extractor(Protocol):
    name: str

    def extract(self, notes: list[NoteText]) -> Extraction: ...


def get(name: str) -> Extractor:
    if name == "semantica":
        from .semantica_adapter import SemanticaExtractor

        return SemanticaExtractor()
    if name == "none":
        from .null import NullExtractor

        return NullExtractor()
    raise ValueError(f"unknown extractor {name!r}")
