"""Date rule (ADR 007): every raw copy has a publication date, nothing is dated in the future, and no note cites a
source published after the note was written. Notes are living pages: citing a newer source is fine once the note is
rewritten, because `generated.at` moves with the rewrite.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path

from . import okf
from .validate import Problem


def _day(value: object) -> date | None:
    if value is None:
        return None
    text = str(value).strip()
    try:
        if len(text) == 10:
            return date.fromisoformat(text)
        return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(timezone.utc).date()
    except ValueError:
        return None


def check_dates(bundle: Path, today: date | None = None) -> list[Problem]:
    today = today or datetime.now(timezone.utc).date()
    problems: list[Problem] = []
    raws = {d.rel: d for d in okf.raws(bundle)}
    for d in raws.values():
        pub = _day(d.frontmatter.get("published_at"))
        if pub is None:
            problems.append(Problem("dates", d.rel, "raw copy has no valid published_at"))
        elif pub > today:
            problems.append(Problem("dates", d.rel, f"published_at {pub} is in the future"))
    for n in okf.notes(bundle):
        fm = n.frontmatter
        written = _day((fm.get("generated") or {}).get("at") if isinstance(fm.get("generated"), dict) else None)
        if written is None:
            problems.append(Problem("dates", n.rel, "note has no valid generated.at"))
            continue
        if written > today:
            problems.append(Problem("dates", n.rel, f"generated.at {written} is in the future"))
        stale = _day(fm.get("stale_after"))
        if stale is not None and stale <= written:
            problems.append(Problem("dates", n.rel, "stale_after must be after generated.at"))
        for v in okf.verifications(fm):
            vd = _day(v.get("at"))
            if vd is None or vd > today:
                problems.append(Problem("dates", n.rel, f"verified.at {v.get('at')!r} is missing or in the future"))
        for s in fm.get("sources") or []:
            res = str(s.get("resource", "")) if isinstance(s, dict) else ""
            raw = raws.get(res.lstrip("/")) if res.startswith("/") else None
            pub = _day(raw.frontmatter.get("published_at")) if raw else None
            if pub and pub > written:
                problems.append(Problem("dates", n.rel, f"cites {res} published {pub}, after the note was written ({written})"))
    return problems


def stale_notes(bundle: Path, today: date | None = None) -> list[str]:
    today = today or datetime.now(timezone.utc).date()
    out = []
    for n in okf.notes(bundle):
        s = _day(n.frontmatter.get("stale_after"))
        if s is not None and s <= today and n.frontmatter.get("status") != "deprecated":
            out.append(n.rel)
    return out
