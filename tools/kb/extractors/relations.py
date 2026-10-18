"""Ontology-constrained relations between notes, and the model pass of entity resolution.

For each note, a model is shown the note and a short list of candidate notes (the ones that share resolved entities
with it) and asked which of the wiki's own relation types hold from this note to a candidate. It may only use those
types, only name candidates it was given, and must quote the sentence of the note that supports the relation. The
quote is then checked against the note's text: a relation whose evidence is not in the note is dropped. What survives
is published as a machine edge (origin "extracted", typed) and listed as a frontmatter proposal for the owner. Nothing
here writes to a note.

The model is reached through Semantica's provider layer (`create_provider`), so the same key, model and patches serve
entity extraction and relation extraction.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from typing import Any

from . import Entity, NoteRelation, NoteText

# The frontmatter relation types a model may propose (ontology/edge-types.yaml). authored_by is left out: its target is
# a person, and people are not part of the extracted layer.
RELATION_TYPES: dict[str, str] = {
    "builds_on": "the note extends an idea developed in the target",
    "refines": "the note narrows or sharpens the target's idea",
    "applies": "the note puts the target (a standard, pattern or practice) to work",
    "contradicts": "the note disagrees with the target",
    "cites": "the note draws on the target as evidence",
    "part_of": "the note belongs to the target (a series or a larger idea the target lays out)",
    "about": "the note's subject is the target",
    "supersedes": "the note replaces the target",
    "answers": "the note answers the question the target asks",
}
MAX_CANDIDATES = 8
MIN_CONFIDENCE = 0.7
MIN_EVIDENCE = 25

Ask = Callable[[str], Any]   # prompt -> parsed JSON (dict or list)


def _squash(text: str) -> str:
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)          # Markdown links: keep the words
    text = re.sub(r"[*_`>#]+", " ", text)                          # emphasis, code, quotes, headings
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return " ".join(text.casefold().split())


def evidence_in(evidence: str, text: str) -> bool:
    """The quote must be the note's own words: compared after removing Markdown and normalising quotes and spaces."""
    e = _squash(evidence).strip(" .\"'")
    return len(e) >= MIN_EVIDENCE and e in _squash(text)


def candidates(notes: list[NoteText], entities: list[Entity]) -> dict[str, list[str]]:
    """For each note, the other notes that share the most resolved entities with it (at most MAX_CANDIDATES)."""
    ents_of: dict[str, set[str]] = {n.id: set() for n in notes}
    for e in entities:
        for m in e.mentioned_in:
            ents_of.setdefault(m, set()).add(e.label)
    out: dict[str, list[str]] = {}
    for n in notes:
        mine = ents_of.get(n.id, set())
        scored = sorted(((len(mine & ents_of[o.id]), o.id) for o in notes if o.id != n.id and mine & ents_of[o.id]),
                        key=lambda t: (-t[0], t[1]))
        out[n.id] = [oid for _, oid in scored[:MAX_CANDIDATES]]
    return out


def relation_prompt(note: NoteText, cands: list[NoteText]) -> str:
    types = "\n".join(f"- {k}: {v}" for k, v in RELATION_TYPES.items())
    listing = "\n".join(f"- C{i + 1}: {c.title}. {c.description}".strip() for i, c in enumerate(cands))
    return f"""You curate a wiki of essays. Decide which typed relations hold FROM the note below TO the candidate notes.

Allowed relation types (use only these ids):
{types}

Rules:
- Propose a relation only when the note's own text makes it explicit or unmistakable. Sharing a topic is not a relation.
- At most 3 relations. Zero is a good answer.
- "evidence" must be one sentence copied word for word from the note text (not from a candidate), at least 6 words.
- "confidence" is your probability (0 to 1) that a careful human editor would accept the relation.

Return JSON only: {{"relations": [{{"target": "C1", "type": "applies", "evidence": "...", "confidence": 0.8}}]}}

Candidates:
{listing}

Note title: {note.title}
Note text:
{note.text[:6000]}"""


def _parse_relations(raw: Any) -> list[dict[str, Any]]:
    if isinstance(raw, str):
        raw = json.loads(raw)
    items = raw.get("relations", []) if isinstance(raw, dict) else raw
    return [r for r in items or [] if isinstance(r, dict)]


def extract_note_relations(notes: list[NoteText], entities: list[Entity], ask: Ask,
                           log: Callable[[str], None] | None = None) -> list[NoteRelation]:
    by_id = {n.id: n for n in notes}
    cands = candidates(notes, entities)
    out: list[NoteRelation] = []
    dropped = {"type": 0, "target": 0, "evidence": 0, "confidence": 0, "failed": 0}
    for n in notes:
        cs = [by_id[c] for c in cands.get(n.id, [])]
        if not cs:
            continue
        try:
            items = _parse_relations(ask(relation_prompt(n, cs)))
        except Exception as e:  # one note's call failing must not sink the pass
            dropped["failed"] += 1
            if log and dropped["failed"] <= 3:
                log(f"relations for {n.id} failed ({type(e).__name__}: {str(e)[:160]})")
            continue
        seen: set[tuple[str, str]] = set()
        for r in items[:6]:
            if len(seen) >= 3:
                break
            typ = str(r.get("type", "")).strip()
            m = re.fullmatch(r"C(\d+)", str(r.get("target", "")).strip(), re.I)
            idx = int(m.group(1)) - 1 if m else -1
            ev = " ".join(str(r.get("evidence", "")).split())
            try:
                conf = float(r.get("confidence", 0))
            except (TypeError, ValueError):
                conf = 0.0
            if typ not in RELATION_TYPES:
                dropped["type"] += 1
            elif not 0 <= idx < len(cs):
                dropped["target"] += 1
            elif not evidence_in(ev, n.text):
                dropped["evidence"] += 1
            elif conf < MIN_CONFIDENCE:
                dropped["confidence"] += 1
            elif (cs[idx].id, typ) not in seen:
                seen.add((cs[idx].id, typ))
                out.append(NoteRelation(n.id, cs[idx].id, typ, ev, round(conf, 2)))
    if log:
        log(f"typed relations: {len(out)} kept; dropped " + ", ".join(f"{v} {k}" for k, v in dropped.items() if v)
            if any(dropped.values()) else f"typed relations: {len(out)} kept, none dropped")
    return out


def alias_prompt(labels: list[str]) -> str:
    listing = "\n".join(f"- {label}" for label in labels)
    return f"""Below are entity names extracted from a wiki of essays on enterprise AI. Group the names that refer to
exactly the same thing: abbreviations and their expansions, alternative spellings, singular and plural. Do NOT group a
broader term with a narrower one ("agents" and "coding agents" are different), and do not group related but distinct
things. Leave every name that has no synonym out.

Return JSON only: {{"groups": [["Model Context Protocol", "MCP"], ...]}}

Names:
{listing}"""


def alias_groups_with(ask: Ask) -> Callable[[list[str]], list[list[str]]]:
    def run(labels: list[str]) -> list[list[str]]:
        raw = ask(alias_prompt(labels))
        if isinstance(raw, str):
            raw = json.loads(raw)
        groups = raw.get("groups", []) if isinstance(raw, dict) else raw
        return [[str(x) for x in g] for g in groups or [] if isinstance(g, list) and len(g) > 1]
    return run


__all__ = ["RELATION_TYPES", "extract_note_relations", "alias_groups_with", "evidence_in", "candidates"]
