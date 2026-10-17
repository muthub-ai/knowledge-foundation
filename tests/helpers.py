"""Build small OKF bundles in a temporary folder for tests."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from kb import okf  # noqa: E402


def note_fm(**over: Any) -> dict[str, Any]:
    fm: dict[str, Any] = {
        "type": "Note",
        "id": "n1",
        "title": "Curated overlay",
        "description": "A context layer that stays small, owned and retrieval-first.",
        "tags": ["context-engineering"],
        "generated": {"by": "llmwiki2/0.5.0", "at": "2026-10-10T10:00:00Z"},
        "sources": [{"id": "s1", "resource": "/raw/2026-src.md", "title": "Not another data lake"}],
        "kind": "Concept",
        "status": "draft",
        "stale_after": "2027-04-10T00:00:00Z",
        "classification": "public",
    }
    fm.update(over)
    return fm


def raw_fm(**over: Any) -> dict[str, Any]:
    fm: dict[str, Any] = {
        "type": "Source",
        "title": "Not another data lake",
        "resource": "https://muthub.org/writing/not-another-data-lake.md",
        "published_at": "2026-07-21",
        "origin_kind": "own-essay",
        "license_note": "Own work",
    }
    fm.update(over)
    return fm


class Bundle:
    """A temporary bundle with one theme folder, one raw copy and one note unless told otherwise."""

    def __init__(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "wiki"
        (self.root / "raw").mkdir(parents=True)
        (self.root / "context-engineering").mkdir()
        (self.root / "index.md").write_text("---\nokf_version: '0.2'\n---\n\n# Index\n", encoding="utf-8")
        (self.root / "log.md").write_text("# Wiki log\n", encoding="utf-8")

    def write(self, rel: str, fm: dict[str, Any], body: str = "# Overview\n\nText.[^s1]\n\n[^s1]: Source.\n") -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(okf.serialize(fm, body), encoding="utf-8")
        return path

    def standard(self) -> "Bundle":
        self.write("raw/2026-src.md", raw_fm(), "# Not another data lake\n\nFull text.\n")
        self.write("context-engineering/curated-overlay.md", note_fm())
        return self

    def cleanup(self) -> None:
        self._tmp.cleanup()
