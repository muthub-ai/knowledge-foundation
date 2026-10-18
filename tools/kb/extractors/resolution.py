"""Entity resolution for the semantic layer: one node per thing, whatever the notes call it.

Extraction finds "MCP" in one note and "Model Context Protocol" in another, "coding agent" here and "coding agents"
there. Three passes merge them, each conservative on its own:

1. Semantica's EntityResolver (fuzzy string similarity) for spelling and plural variants.
2. An acronym rule: an all-capitals label merges with the label whose initials spell it ("MCP" and "Model Context
   Protocol"), never with a label that merely contains it ("MCP server" stays separate).
3. Optionally, one model call over the whole entity list that groups names for the same thing. Its answer is checked:
   only labels that exist are merged, and a group may not join a broader term to a narrower one by containment.

The merged entity keeps the most specific spelled-out name as its label and every other name as an alias.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from typing import Any

from . import Entity

_STOP = {"of", "and", "the", "for", "a", "an", "to", "in", "on", "with", "by", "&"}


class _UnionFind:
    def __init__(self, keys: Iterable[str]) -> None:
        self.parent = {k: k for k in keys}

    def find(self, k: str) -> str:
        while self.parent[k] != k:
            self.parent[k] = self.parent[self.parent[k]]
            k = self.parent[k]
        return k

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def _norm(label: str) -> str:
    # Case, hyphens, slashes and spacing never make two things different: "Architecture-as-Code" = "architecture as code".
    return " ".join(re.sub(r"[-_/]+", " ", label.casefold()).split())


def initials(label: str) -> str:
    words = [w for w in re.split(r"[\s\-/]+", label) if w and w.casefold() not in _STOP]
    return "".join(w[0] for w in words).upper()


def is_acronym(label: str) -> bool:
    return bool(re.fullmatch(r"[A-Z][A-Z0-9]{1,6}s?", label.strip()))


def acronym_pairs(labels: list[str]) -> list[tuple[str, str]]:
    """(acronym, long form) pairs: "MCP" and "Model Context Protocol". The long form must have as many significant
    words as the acronym has letters, so "MCP" never pairs with "MCP server" or with an unrelated three-word phrase
    whose initials happen to match only after dropping words."""
    out = []
    longs = [label for label in labels if not is_acronym(label) and len(label.split()) >= 2]
    for a in (label for label in labels if is_acronym(label)):
        letters = a.rstrip("s") if a.endswith("s") and a[:-1].isupper() else a
        for long in longs:
            if initials(long) == letters and len([w for w in long.split() if w.casefold() not in _STOP]) == len(letters):
                out.append((a, long))
    return out


def _contains(broad: str, narrow: str) -> bool:
    """True when one label is the other plus qualifying words ("agents" in "coding agents"): a narrower thing."""
    b, n = _norm(broad).split(), _norm(narrow).split()
    return len(b) < len(n) and all(w in n for w in b)


def _canonical(group: list[Entity]) -> Entity:
    # The spelled-out name wins over an acronym; then the most mentioned; then the longest; then alphabetical.
    def key(e: Entity) -> tuple[int, int, int, str]:
        return (0 if is_acronym(e.label) else 1, len(e.mentioned_in), len(e.label), e.label)
    return max(group, key=key)


def resolve(
    entities: list[Entity],
    *,
    fuzzy: Callable[[list[dict[str, Any]]], list[dict[str, Any]]] | None = None,
    alias_groups: Callable[[list[str]], list[list[str]]] | None = None,
    log: Callable[[str], None] | None = None,
) -> list[Entity]:
    """Merge entities that name the same thing. `fuzzy` is Semantica's EntityResolver.resolve_entities (injectable);
    `alias_groups` is the optional model pass. Returns new Entity objects with `aliases` filled in."""
    by_key: dict[str, Entity] = {}
    merges: list[str] = []
    for e in entities:  # same name up to case and punctuation: one entity from the start
        k = _norm(e.label)
        if k in by_key:
            first = by_key[k]
            first.mentioned_in += [m for m in e.mentioned_in if m not in first.mentioned_in]
            first.aliases = sorted(set(first.aliases) | {e.label} - {first.label})
            merges.append(f"{first.label} = {e.label} (spelling)")
        else:
            by_key[k] = Entity(e.label, e.type, list(e.mentioned_in), list(e.aliases))
    uf = _UnionFind(by_key)

    def join(a: str, b: str, why: str) -> None:
        ka, kb = _norm(a), _norm(b)
        if ka in by_key and kb in by_key and uf.find(ka) != uf.find(kb):
            uf.union(ka, kb)
            merges.append(f"{by_key[ka].label} = {by_key[kb].label} ({why})")

    if fuzzy is not None:
        items = [{"id": k, "name": e.label, "type": e.type} for k, e in by_key.items()]
        try:
            for merged in fuzzy(items):
                ids = merged.get("merged_from") or []
                for other in ids[1:]:
                    join(ids[0], other, "fuzzy")
        except Exception as e:  # resolution is an improvement, never a reason to lose the layer
            if log:
                log(f"fuzzy resolution skipped ({type(e).__name__}: {e})")

    for a, long in acronym_pairs([e.label for e in by_key.values()]):
        join(a, long, "acronym")

    if alias_groups is not None:
        try:
            groups = alias_groups(sorted(e.label for e in by_key.values()))
        except Exception as e:
            groups = []
            if log:
                log(f"model alias pass skipped ({type(e).__name__}: {e})")
        for g in groups:
            names = [n for n in g if _norm(n) in by_key]
            for other in names[1:]:
                # A broader and a narrower term are related, not the same thing: never merged by the model pass.
                if _contains(names[0], other) or _contains(other, names[0]):
                    continue
                join(names[0], other, "model")

    groups_by_root: dict[str, list[Entity]] = {}
    for k, e in by_key.items():
        groups_by_root.setdefault(uf.find(k), []).append(e)
    out = []
    for group in groups_by_root.values():
        head = _canonical(group)
        mentioned: list[str] = []
        for e in sorted(group, key=lambda e: e.label):
            mentioned += [m for m in e.mentioned_in if m not in mentioned]
        aliases = sorted({e.label for e in group if e.label != head.label} | {a for e in group for a in e.aliases if a != head.label})
        out.append(Entity(label=head.label, type=head.type, mentioned_in=mentioned, aliases=aliases))
    if log and merges:
        log(f"resolution: {len(entities)} names -> {len(out)} entities; " + "; ".join(merges[:25]))
    return sorted(out, key=lambda e: e.label.lower())


__all__ = ["resolve", "acronym_pairs", "initials", "is_acronym"]
