# SPDX-License-Identifier: AGPL-3.0-or-later
# This script imports LLM-Wiki-V2 (AGPL-3.0-or-later), so it is licensed the same way. See LICENSES/README.md.
"""Ingest one capture note from inbox/ through LLM-Wiki-V2, then record the governance fields it does not write.

A capture note is Markdown with frontmatter:

    ---
    title: Introducing the Open Knowledge Format
    resource: https://cloud.google.com/blog/...
    published_at: 2026-06-12
    origin_kind: third-party-note        # own-essay | own-post | own-talk | own-repo | third-party-note | third-party-excerpt
    license_note: cite and paraphrase only
    why: The format the wiki is stored in.
    ---
    Your notes, and at most a short excerpt for third-party material.

The Librarian files it (CROW: the local classifier decides, Claude writes), keeps the text as a raw copy, and this
script then writes published_at, origin_kind and license_note onto that raw copy and moves the capture to
inbox/done/. Run on a branch; the curator then opens the pull request.

Usage: PYTHONPATH=tools python tools/librarian/ingest.py inbox/2026-10-20-okf.md
Models come from the environment (see .env.example): OKF_LLM_* for Claude, OKF_CLASSIFIER_* for the local classifier.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kb import okf  # noqa: E402
from kb.config import Config  # noqa: E402

THIRD_PARTY_MAX_CHARS = 2500  # notes plus a short excerpt; full third-party texts stay in the private folder
REQUIRED = ("title", "published_at", "origin_kind", "license_note")
KINDS = ("own-essay", "own-post", "own-talk", "own-repo", "third-party-note", "third-party-excerpt")


class CaptureError(ValueError):
    pass


def read_capture(path: Path) -> tuple[dict[str, Any], str]:
    fm, body = okf.parse(path.read_text(encoding="utf-8"))
    missing = [k for k in REQUIRED if not fm.get(k)]
    if missing:
        raise CaptureError(f"{path}: capture is missing {', '.join(missing)}")
    if fm["origin_kind"] not in KINDS:
        raise CaptureError(f"{path}: origin_kind must be one of {', '.join(KINDS)}")
    if str(fm["origin_kind"]).startswith("third-party") and len(body) > THIRD_PARTY_MAX_CHARS:
        raise CaptureError(f"{path}: third-party captures hold notes and a short excerpt (at most {THIRD_PARTY_MAX_CHARS} characters), not the full text")
    if not body.strip():
        raise CaptureError(f"{path}: capture has no text")
    return fm, body


def record_raw_fields(bundle: Path, note_rel: str, fm: dict[str, Any]) -> str | None:
    """Write the capture's governance fields onto the raw copy the note's newest source points at."""
    note = okf.read(bundle / note_rel.lstrip("/"), bundle)
    sources = [s for s in note.frontmatter.get("sources") or [] if isinstance(s, dict) and str(s.get("resource", "")).startswith("/raw/")]
    if not sources:
        return None
    raw_rel = str(sources[-1]["resource"]).lstrip("/")
    raw = okf.read(bundle / raw_rel, bundle)
    for k in ("published_at", "origin_kind", "license_note"):
        raw.frontmatter[k] = str(fm[k])
    if fm.get("author"):
        raw.frontmatter["author"] = fm["author"]
    okf.write(raw)
    return raw_rel


def capture_origin(fm: dict[str, Any]) -> Any:
    """The capture's identity for LLM-Wiki-V2's origin index: re-ingesting the same text from the same place is a no-op,
    and a changed text from the same place updates the note it fed."""
    try:
        from llmw2.bundle.origin import Origin  # type: ignore[import-not-found]
    except ImportError:  # tests with a stand-in wiki
        return None
    key = str(fm.get("resource") or "") or "title:" + str(fm["title"]).strip().lower()
    return Origin("capture", "", key, link=fm.get("resource"), modified=str(fm["published_at"]))


def default_wiki(bundle: Path) -> Any:
    from llmw2 import Wiki  # type: ignore[import-not-found]

    return Wiki.from_env(bundle=str(bundle))


def ingest(capture: Path, *, cfg: Config | None = None, wiki_factory: Callable[[Path], Any] = default_wiki) -> dict[str, Any]:
    cfg = cfg or Config()
    fm, body = read_capture(capture)
    wiki = wiki_factory(cfg.bundle)
    result = wiki.ingest(body, title=str(fm["title"]), resource=fm.get("resource"), origin=capture_origin(fm))
    done = capture.parent / "done"
    done.mkdir(exist_ok=True)
    if result.action == "unchanged":  # the same text from the same place is already filed
        shutil.move(str(capture), done / capture.name)
        return {"action": "unchanged", "note": result.note}
    raw_rel = record_raw_fields(cfg.bundle, result.note, fm)
    shutil.move(str(capture), done / capture.name)
    return {"action": result.action, "note": result.note, "raw": raw_rel, "folder": result.folder, "related": list(result.related)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("captures", nargs="+", type=Path)
    args = ap.parse_args()
    rc = 0
    for c in args.captures:
        try:
            print(ingest(c))
        except CaptureError as e:
            print(f"refused: {e}", file=sys.stderr)
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
