import json
import unittest
from unittest import mock

import jsonschema
from helpers import Bundle, note_fm

from kb import graph, governance, okf
from kb.config import Config
from kb.extractors import Entity, Extraction, ExtractorUnavailable, NoteText
from kb.extractors.semantica_adapter import SemanticaExtractor

CFG = Config()


class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.b = Bundle().standard()

    def tearDown(self):
        self.b.cleanup()

    def test_normalize_adds_defaults_without_overwriting(self):
        fm = note_fm()
        for k in ("kind", "status", "stale_after", "classification"):
            del fm[k]
        fm["kind"] = "Pattern"
        self.b.write("context-engineering/curated-overlay.md", fm)
        changed = governance.normalize(self.b.root, CFG)
        self.assertEqual(changed, ["context-engineering/curated-overlay.md"])
        out = okf.read(self.b.root / changed[0], self.b.root).frontmatter
        self.assertEqual(out["kind"], "Pattern")
        self.assertEqual(out["status"], "draft")
        self.assertEqual(out["classification"], "public")
        self.assertEqual(out["stale_after"], "2027-04-10T00:00:00Z")  # Pattern: default 6 months
        self.assertNotIn("verified", out)
        self.assertEqual(governance.normalize(self.b.root, CFG), [])  # idempotent

    def test_stamp_is_human_only_idempotent_and_promotes_drafts(self):
        rel = "context-engineering/curated-overlay.md"
        with self.assertRaises(ValueError):
            governance.stamp(self.b.root, [rel], by="process:ci", at="2026-10-17T12:00:00Z")
        self.assertEqual(governance.stamp(self.b.root, [rel, "raw/2026-src.md", "index.md"], by="human:muthu", at="2026-10-17T12:00:00Z"), [rel])
        self.assertEqual(governance.stamp(self.b.root, [rel], by="human:muthu", at="2026-10-17T12:00:00Z"), [])
        fm = okf.read(self.b.root / rel, self.b.root).frontmatter
        self.assertEqual(okf.trust_tier(fm), "human-reviewed")
        self.assertEqual(fm["status"], "stable")
        governance.stamp(self.b.root, [rel], by="human:muthu", at="2026-12-01T09:00:00Z")
        self.assertEqual(len(okf.verifications(okf.read(self.b.root / rel, self.b.root).frontmatter)), 2)


class FakeExtractor:
    name = "fake"

    def __init__(self, extraction=None, fail=False):
        self.extraction, self.fail = extraction, fail

    def extract(self, notes):
        if self.fail:
            raise ExtractorUnavailable("not installed")
        return self.extraction


class GraphTests(unittest.TestCase):
    def setUp(self):
        self.b = Bundle().standard()
        self.b.write("context-engineering/context-layer.md", note_fm(id="n2", title="Context layer", aliases=["knowledge layer"],
                     relations=[{"type": "refines", "target": "/context-engineering/curated-overlay.md"}]),
                     "See [the overlay](curated-overlay.md).[^s1]\n\n[^s1]: Source.\n")

    def tearDown(self):
        self.b.cleanup()

    def test_graph_matches_the_published_contract(self):
        g, report = graph.build(self.b.root, CFG)
        jsonschema.validate(g, CFG.schema("graph"))
        ids = {n["id"] for n in g["nodes"]}
        self.assertIn("theme:context-engineering", ids)
        self.assertNotIn("theme:reference", ids)  # empty themes are left out
        origins = {e["origin"] for e in g["edges"]}
        self.assertEqual(origins, {"folder", "source", "frontmatter"})
        self.assertIn("Graph report", report)

    def test_typed_relation_wins_over_a_plain_link(self):
        g, _ = graph.build(self.b.root, CFG)
        e = [e for e in g["edges"] if e["source"] == "context-engineering/context-layer.md" and e["target"] == "context-engineering/curated-overlay.md"]
        self.assertEqual([(x["type"], x["origin"]) for x in e], [("refines", "frontmatter")])

    def test_extracted_entities_merge_by_alias_or_become_ext_nodes(self):
        ex = Extraction(entities=[Entity("Knowledge layer", "Concept", ["context-engineering/curated-overlay.md"]),
                                  Entity("OKF", "Standard", ["context-engineering/curated-overlay.md"])], extractor="fake")
        g, report = graph.build(self.b.root, CFG, FakeExtractor(ex))
        ids = {n["id"] for n in g["nodes"]}
        self.assertIn("ext:okf", ids)
        mentions = {(e["source"], e["target"]) for e in g["edges"] if e["origin"] == "extracted"}
        self.assertIn(("context-engineering/curated-overlay.md", "ext:okf"), mentions)
        self.assertNotIn("ext:knowledge-layer", ids)  # merged into the note that carries the alias
        self.assertIn("Entities: 2", report)

    def test_unavailable_extractor_still_publishes_the_deterministic_graph(self):
        g, report = graph.build(self.b.root, CFG, FakeExtractor(fail=True))
        self.assertTrue(g["nodes"])
        self.assertIn("Semantic layer skipped", report)

    def test_outputs_are_written(self):
        import tempfile
        from pathlib import Path

        g, report = graph.build(self.b.root, CFG)
        with tempfile.TemporaryDirectory() as d:
            graph.write_outputs(g, report, Path(d))
            self.assertEqual(json.loads((Path(d) / "graph.json").read_text())["version"], "1.0")
            self.assertTrue((Path(d) / "graph.graphml").read_text().startswith("<?xml"))


class SemanticaAdapterTests(unittest.TestCase):
    """Semantica itself is faked: these tests pin the adapter's contract with GraphBuilder.build()."""

    def test_entities_keep_their_note_and_relations_are_read(self):
        builder = mock.Mock()
        builder.build.return_value = {"entities": [{"text": "Model Context Protocol", "type": "PRODUCT"}, {"name": "Anthropic", "type": "ORG"}],
                                      "relationships": [{"source": "Anthropic", "target": "Model Context Protocol", "type": "created"}]}
        out = SemanticaExtractor(builder).extract([NoteText("a/x.md", "X", "text"), NoteText("a/y.md", "Y", "text")])
        labels = {e.label: e for e in out.entities}
        self.assertEqual(labels["Anthropic"].type, "Organization")
        self.assertEqual(labels["Model Context Protocol"].type, "Tool")
        self.assertEqual(labels["Anthropic"].mentioned_in, ["a/x.md", "a/y.md"])
        self.assertEqual(out.relations[0].type, "created")
        kwargs = builder.build.call_args.kwargs
        self.assertEqual(kwargs["ner_method"], "ml")
        self.assertTrue(kwargs["extract_relations"])

    def test_one_failing_note_is_reported_not_fatal(self):
        builder = mock.Mock()
        builder.build.side_effect = [RuntimeError("boom"), {"entities": [{"text": "OKF", "type": "STANDARD"}]}]
        out = SemanticaExtractor(builder).extract([NoteText("a/x.md", "X", "t"), NoteText("a/y.md", "Y", "t")])
        self.assertEqual([e.label for e in out.entities], ["OKF"])
        self.assertTrue(any("a/x.md" in n for n in out.notes))

    def test_dates_numbers_and_headings_are_not_entities(self):
        builder = mock.Mock()
        builder.build.return_value = {"entities": [{"text": t, "type": "MISC"} for t in
                                                   ("2025", "Q3 2026", "Overview", "Why gates matter", "40%", "OKF")]}
        out = SemanticaExtractor(builder).extract([NoteText("a/x.md", "X", "# Overview\n\nBody.\n\n## Why gates matter\n")])
        self.assertEqual([e.label for e in out.entities], ["OKF"])

    def test_missing_library_raises_unavailable(self):
        with mock.patch.dict("sys.modules", {"semantica": None, "semantica.kg": None}):
            with self.assertRaises(ExtractorUnavailable):
                SemanticaExtractor().extract([NoteText("a/x.md", "X", "t")])


class RepositoryBundleTests(unittest.TestCase):
    """The committed bundle itself must pass the rules (what CI enforces on every pull request)."""

    def test_committed_bundle_is_valid(self):
        from kb import dates, validate

        if not CFG.bundle.exists():
            self.skipTest("no bundle yet")
        self.assertEqual([str(p) for p in validate.validate(CFG.bundle, CFG)], [])
        self.assertEqual([str(p) for p in dates.check_dates(CFG.bundle)], [])

    def test_committed_bundle_builds_a_valid_graph(self):
        if not CFG.bundle.exists():
            self.skipTest("no bundle yet")
        g, _ = graph.build(CFG.bundle, CFG)
        self.assertGreater(len(g["nodes"]), 10)


if __name__ == "__main__":
    unittest.main()
