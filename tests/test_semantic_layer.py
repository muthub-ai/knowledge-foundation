"""Entity resolution and ontology-constrained relations (the semantic layer, October 2026). No network: the model and
Semantica's resolver are replaced by fakes; the real ones run in the semantica canary jobs."""

import os
import unittest
from unittest import mock

import helpers  # noqa: F401  (puts tools/ on sys.path, like the other tests)

from kb import graph
from kb.config import Config
from kb.extractors import Entity, Extraction, NoteRelation, NoteText
from kb.extractors import relations as rels
from kb.extractors.resolution import acronym_pairs, initials, resolve
from kb.extractors.semantica_adapter import SemanticaExtractor


CFG = Config()


def E(label, *notes, type="Concept", aliases=()):
    return Entity(label=label, type=type, mentioned_in=list(notes), aliases=list(aliases))


class ResolutionTests(unittest.TestCase):
    def test_acronym_joins_its_expansion_not_a_longer_phrase(self):
        self.assertEqual(initials("Model Context Protocol"), "MCP")
        pairs = acronym_pairs(["MCP", "Model Context Protocol", "MCP server", "Managed Cloud Platform team"])
        self.assertEqual(pairs, [("MCP", "Model Context Protocol")])

    def test_merged_entity_keeps_spelled_out_name_aliases_and_all_notes(self):
        out = resolve([E("MCP", "a.md", "b.md", type="Standard"), E("Model Context Protocol", "c.md", type="Standard"),
                       E("MCP server", "a.md", type="Tool")])
        by = {e.label: e for e in out}
        self.assertIn("Model Context Protocol", by)
        self.assertEqual(by["Model Context Protocol"].aliases, ["MCP"])
        self.assertEqual(sorted(by["Model Context Protocol"].mentioned_in), ["a.md", "b.md", "c.md"])
        self.assertIn("MCP server", by)  # a narrower thing stays its own node

    def test_fuzzy_groups_from_semantica_are_applied(self):
        fuzzy = mock.Mock(return_value=[{"id": "coding agents", "merged_from": ["coding agents", "coding agent"]}])
        out = resolve([E("coding agents", "a.md"), E("coding agent", "b.md")], fuzzy=fuzzy)
        self.assertEqual([(e.label, e.aliases) for e in out], [("coding agents", ["coding agent"])])

    def test_model_pass_cannot_merge_broader_with_narrower_or_invent_names(self):
        groups = mock.Mock(return_value=[["agents", "coding agents"], ["OPA", "Open Policy Agent", "Not A Label"]])
        out = resolve([E("agents", "a.md"), E("coding agents", "b.md"), E("OPA", "c.md"), E("Open Policy Agent", "d.md")],
                      alias_groups=groups)
        labels = sorted((e.label for e in out), key=str.lower)
        self.assertEqual(labels, ["agents", "coding agents", "Open Policy Agent"])

    def test_model_pass_cannot_chain_a_narrower_term_into_a_broader_one(self):
        fuzzy = mock.Mock(return_value=[{"id": "agents", "merged_from": ["agents", "agent"]}])
        groups = mock.Mock(return_value=[["AI agent", "agents"], ["AI agent", "AI agents"]])
        out = resolve([E("agents", "a.md"), E("agent", "b.md"), E("AI agent", "c.md"), E("AI agents", "d.md")],
                      fuzzy=fuzzy, alias_groups=groups)
        self.assertEqual(sorted((e.label, tuple(e.aliases)) for e in out), [("AI agents", ("AI agent",)), ("agents", ("agent",))])

    def test_a_failing_pass_is_logged_not_fatal(self):
        notes = []
        out = resolve([E("A thing", "a.md")], fuzzy=mock.Mock(side_effect=RuntimeError("boom")),
                      alias_groups=mock.Mock(side_effect=ValueError("bad json")), log=notes.append)
        self.assertEqual([e.label for e in out], ["A thing"])
        self.assertEqual(len(notes), 2)


NOTE_A = NoteText("governed-ai/a.md", "Registry", "An enterprise MCP registry applies the Model Context Protocol to tool approval. "
                  "It is the control point for every agent.", "How to govern MCP servers.")
NOTE_B = NoteText("governed-ai/b.md", "Adopting MCP", "The Model Context Protocol connects agents to tools.", "Risks of MCP.")
NOTE_C = NoteText("data/c.md", "Lakehouse", "An open lakehouse keeps data in open formats.", "Data platform.")


class RelationTests(unittest.TestCase):
    def setUp(self):
        self.ents = [E("Model Context Protocol", NOTE_A.id, NOTE_B.id), E("open lakehouse", NOTE_C.id)]

    def test_candidates_are_notes_sharing_entities(self):
        c = rels.candidates([NOTE_A, NOTE_B, NOTE_C], self.ents)
        self.assertEqual(c[NOTE_A.id], [NOTE_B.id])
        self.assertEqual(c[NOTE_C.id], [])

    def test_only_verbatim_evidence_known_types_given_targets_and_confident_answers_survive(self):
        answer = {"relations": [
            {"target": "C1", "type": "applies", "evidence": "An enterprise MCP registry applies the Model Context Protocol to tool approval.", "confidence": 0.9},
            {"target": "C1", "type": "builds_on", "evidence": "This sentence is not in the note at all, so it must go.", "confidence": 0.95},
            {"target": "C1", "type": "inspired_by", "evidence": "It is the control point for every agent.", "confidence": 0.9},
            {"target": "C7", "type": "about", "evidence": "It is the control point for every agent.", "confidence": 0.9},
        ]}
        ask = mock.Mock(side_effect=lambda p: answer if "Registry" in p.split("Note title:")[1] else {"relations": []})
        log = []
        out = rels.extract_note_relations([NOTE_A, NOTE_B, NOTE_C], self.ents, ask, log=log.append)
        self.assertEqual([(r.source, r.type, r.target) for r in out], [(NOTE_A.id, "applies", NOTE_B.id)])
        self.assertIn("1 evidence", log[-1])
        self.assertIn("1 type", log[-1])
        self.assertIn("1 target", log[-1])

    def test_low_confidence_is_dropped_and_markdown_does_not_break_evidence(self):
        md = NoteText("x/md.md", "MD", "We **apply** the [Model Context Protocol](https://example.com) to every tool call today.")
        self.assertTrue(rels.evidence_in("We apply the Model Context Protocol to every tool call today.", md.text))
        ask = mock.Mock(return_value={"relations": [{"target": "C1", "type": "applies", "confidence": 0.4,
                                                     "evidence": "We apply the Model Context Protocol to every tool call today."}]})
        ents = [E("Model Context Protocol", md.id, NOTE_B.id)]
        self.assertEqual(rels.extract_note_relations([md, NOTE_B], ents, ask), [])

    def test_prompt_lists_only_ontology_types_and_no_person_relation(self):
        p = rels.relation_prompt(NOTE_A, [NOTE_B])
        for t in ("builds_on", "applies", "contradicts", "supersedes"):
            self.assertIn(f"- {t}:", p)
        self.assertNotIn("authored_by", p)


class AdapterTests(unittest.TestCase):
    def test_people_and_dates_dropped_types_mapped_resolution_and_relations_run(self):
        builder = mock.Mock()
        builder.build.side_effect = [
            {"entities": [{"text": "MCP", "type": "PROTOCOL"}, {"text": "Ada Lovelace", "type": "PERSON"},
                          {"text": "spec-driven development", "type": "METHODOLOGY"}, {"text": "Anthropic", "type": "COMPANY"}]},
            {"entities": [{"text": "Model Context Protocol", "type": "STANDARD"}, {"text": "Last summer", "type": "DATE"},
                          {"text": "Spec-driven development", "type": "METHOD"}, {"text": "code", "type": "CONCEPT"}]},
            {"entities": []},
        ]
        ask = mock.Mock(side_effect=lambda p: {"groups": []} if "Group the names" in p else {"relations": []})
        with mock.patch.dict(os.environ, {"SEMANTICA_NER_METHOD": "llm", "SEMANTICA_RELATIONS": "llm"}):
            out = SemanticaExtractor(builder, resolver=lambda items: [], ask=ask).extract([NOTE_A, NOTE_B, NOTE_C])
        by = {e.label: e for e in out.entities}
        self.assertNotIn("Ada Lovelace", by)
        self.assertNotIn("Last summer", by)
        self.assertEqual(by["Model Context Protocol"].type, "Standard")
        self.assertEqual(by["Model Context Protocol"].aliases, ["MCP"])
        self.assertEqual(by["spec-driven development"].type, "Practice")
        self.assertNotIn("code", by)  # a generic word, not an entity
        self.assertEqual(by["Anthropic"].type, "Organization")
        self.assertEqual(builder.build.call_args.kwargs["entity_types"], ["Concept", "Standard", "Tool", "Organization", "Practice"])
        self.assertTrue(any("typed relations" in n for n in out.notes))

    def test_relations_off_by_default(self):
        builder = mock.Mock(); builder.build.return_value = {"entities": [{"text": "OKF", "type": "STANDARD"}]}
        ask = mock.Mock()
        with mock.patch.dict(os.environ, {"SEMANTICA_NER_METHOD": "pattern"}, clear=False):
            os.environ.pop("SEMANTICA_RELATIONS", None)
            SemanticaExtractor(builder, resolver=lambda items: [], ask=ask).extract([NOTE_A])
        self.assertFalse(any("C1" in str(c) for c in ask.call_args_list))


class GraphTests(unittest.TestCase):
    def test_typed_proposals_become_extracted_edges_and_never_replace_authored_ones(self):
        notes = sorted(p.relative_to(CFG.bundle).as_posix() for p in CFG.bundle.rglob("*.md")
                       if not p.relative_to(CFG.bundle).as_posix().startswith("raw/") and p.name not in ("index.md", "log.md"))
        if len(notes) < 3:
            self.skipTest("bundle too small")
        g0, _ = graph.build(CFG.bundle, CFG)
        linked = next((e["source"], e["target"]) for e in g0["edges"] if e["origin"] in ("link", "frontmatter"))
        ids = {n["id"] for n in g0["nodes"]}
        free = next((a, b) for a in notes for b in notes if a != b and a in ids and b in ids and
                    not any({e["source"], e["target"]} == {a, b} for e in g0["edges"]))

        class Fake:
            name = "fake"

            def extract(self, texts):
                return Extraction(entities=[E("Model Context Protocol", free[0], free[1], type="Standard", aliases=["MCP"])],
                                  note_relations=[NoteRelation(free[0], free[1], "applies", "quoted sentence", 0.9),
                                                  NoteRelation(linked[0], linked[1], "refines", "quoted sentence", 0.9)],
                                  extractor="fake")

        g, report = graph.build(CFG.bundle, CFG, Fake())
        typed = [e for e in g["edges"] if e["origin"] == "extracted" and e["type"] != "mentions"]
        self.assertEqual([(e["source"], e["type"], e["target"]) for e in typed], [(free[0], "applies", free[1])])
        ent = next(n for n in g["nodes"] if n["id"] == "ext:model-context-protocol")
        self.assertEqual(ent["aliases"], ["MCP"])
        self.assertIn("Typed relations proposed: 1 new", report)


if __name__ == "__main__":
    unittest.main()
