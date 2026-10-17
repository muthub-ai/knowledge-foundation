import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from helpers import Bundle, note_fm, raw_fm

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "librarian"))
import ingest as ing  # noqa: E402

from kb import okf  # noqa: E402

CAPTURE = """---
title: Introducing the Open Knowledge Format
resource: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
published_at: 2026-06-12
origin_kind: third-party-note
license_note: cite and paraphrase only
---
My notes on the format.
"""


class FakeWiki:
    """Stands in for LLM-Wiki-V2: writes a raw copy and a note the way the Librarian does."""

    def __init__(self, bundle: Path):
        self.bundle = bundle

    def ingest(self, text, *, title, resource=None, origin=None):
        b = Bundle.__new__(Bundle)
        b.root = self.bundle
        b.write("raw/20261020-okf.md", {"type": "Source", "title": title, "resource": resource}, text)
        b.write("context-engineering/okf.md", note_fm(id="okf", title=title, sources=[{"id": "s1", "resource": "/raw/20261020-okf.md"}]))
        return SimpleNamespace(action="created", note="/context-engineering/okf.md", folder="/context-engineering", related=[])


class IngestTests(unittest.TestCase):
    def setUp(self):
        self.b = Bundle().standard()
        self.inbox = self.b.root.parent / "inbox"
        self.inbox.mkdir()
        self.cfg = mock.Mock(bundle=self.b.root)

    def tearDown(self):
        self.b.cleanup()

    def test_capture_fields_land_on_the_raw_copy_and_the_capture_moves(self):
        cap = self.inbox / "okf.md"
        cap.write_text(CAPTURE, encoding="utf-8")
        out = ing.ingest(cap, cfg=self.cfg, wiki_factory=FakeWiki)
        self.assertEqual(out["raw"], "raw/20261020-okf.md")
        raw = okf.read(self.b.root / out["raw"], self.b.root).frontmatter
        self.assertEqual((raw["published_at"], raw["origin_kind"]), ("2026-06-12", "third-party-note"))
        self.assertFalse(cap.exists())
        self.assertTrue((self.inbox / "done" / "okf.md").exists())

    def test_full_third_party_text_is_refused(self):
        cap = self.inbox / "long.md"
        cap.write_text(CAPTURE + ("word " * 1000), encoding="utf-8")
        with self.assertRaises(ing.CaptureError):
            ing.ingest(cap, cfg=self.cfg, wiki_factory=FakeWiki)

    def test_capture_without_publication_date_is_refused(self):
        cap = self.inbox / "nodate.md"
        cap.write_text(CAPTURE.replace("published_at: 2026-06-12\n", ""), encoding="utf-8")
        with self.assertRaises(ing.CaptureError):
            ing.read_capture(cap)

    def test_own_material_may_be_long(self):
        cap = self.inbox / "own.md"
        cap.write_text(CAPTURE.replace("third-party-note", "own-post") + ("word " * 1000), encoding="utf-8")
        fm, body = ing.read_capture(cap)
        self.assertEqual(fm["origin_kind"], "own-post")


if __name__ == "__main__":
    unittest.main()
