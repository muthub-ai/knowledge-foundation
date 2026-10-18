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
    description: str = ""


@dataclass
class Entity:
    label: str
    type: str                                    # Concept, Standard, Tool, Organization or Practice
    mentioned_in: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)  # other names merged into this one by entity resolution


@dataclass
class Relation:
    source: str      # entity label or note id
    target: str
    type: str = "mentions"


@dataclass
class NoteRelation:
    """A typed relation between two notes, proposed by a model under the wiki's ontology. Never written to a note by
    the build: it is published as a machine edge and offered to the owner as a frontmatter proposal."""
    source: str      # note id
    target: str      # note id
    type: str        # one of the frontmatter relation types in ontology/edge-types.yaml
    evidence: str    # a sentence quoted verbatim from the source note
    confidence: float = 0.0


@dataclass
class Extraction:
    entities: list[Entity] = field(default_factory=list)
    relations: list[Relation] = field(default_factory=list)
    note_relations: list[NoteRelation] = field(default_factory=list)
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
