"""Governance fields that LLM-Wiki-V2 does not write.

normalize   adds missing defaults on a branch: kind, status, stale_after, classification, owner (never `verified`)
stamp       adds `verified: {by: human:<owner>, at: <approval time>}` to the notes a pull request changed; runs
            only when the owner approves the review (ADR 006)
"""

from __future__ import annotations

import calendar
from datetime import datetime, timezone
from pathlib import Path

from . import okf
from .config import Config


def _add_months(ts: str, months: int) -> str:
    d = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)
    m = d.month - 1 + months
    y, m = d.year + m // 12, m % 12 + 1
    day = min(d.day, calendar.monthrange(y, m)[1])
    return d.replace(year=y, month=m, day=day, hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize(bundle: Path, cfg: Config, *, paths: list[str] | None = None) -> list[str]:
    """Fill governance defaults; returns the notes changed. Existing values are never overwritten."""
    changed = []
    wanted = set(paths) if paths else None
    for n in okf.notes(bundle):
        if wanted is not None and n.rel not in wanted:
            continue
        fm = dict(n.frontmatter)
        before = dict(fm)
        fm.setdefault("kind", cfg.data.get("default_kind", "Concept"))
        fm.setdefault("status", "draft")
        fm.setdefault("classification", "public")
        fm.setdefault("owner", cfg.owner_actor)
        gen = fm.get("generated") if isinstance(fm.get("generated"), dict) else {}
        if "stale_after" not in fm and gen.get("at"):
            fm["stale_after"] = _add_months(str(gen["at"]), cfg.stale_months(str(fm["kind"])))
        if fm != before:
            n.frontmatter = fm
            okf.write(n)
            changed.append(n.rel)
    return changed


def stamp(bundle: Path, rels: list[str], *, by: str, at: str) -> list[str]:
    """Append a verification event to each listed note (idempotent for the same actor and time)."""
    if not by.startswith("human:"):
        raise ValueError("only a human actor may stamp a review verification")
    done = []
    for rel in rels:
        path = bundle / rel
        if not path.exists() or path.name in (okf.INDEX, okf.LOG) or rel.startswith(f"{okf.RAW}/"):
            continue
        doc = okf.read(path, bundle)
        events = okf.verifications(doc.frontmatter)
        if any(e.get("by") == by and str(e.get("at")) == at for e in events):
            continue
        events.append({"by": by, "at": at})
        doc.frontmatter["verified"] = events[0] if len(events) == 1 else events
        if doc.frontmatter.get("status") == "draft":
            doc.frontmatter["status"] = "stable"
        okf.write(doc)
        done.append(rel)
    return done
