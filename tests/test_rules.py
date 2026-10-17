import os
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

from helpers import Bundle, note_fm, raw_fm

from kb import blocklist, dates, okf, validate
from kb.config import Config

CFG = Config()


def rules(problems):
    return sorted({p.rule for p in problems})


class OKFTests(unittest.TestCase):
    def test_round_trip_keeps_timestamps_as_text(self):
        text = okf.serialize({"type": "Note", "generated": {"at": "2026-10-10T10:00:00Z"}, "published_at": "2026-07-21"}, "Body")
        fm, body = okf.parse(text)
        self.assertEqual(fm["generated"]["at"], "2026-10-10T10:00:00Z")
        self.assertEqual(fm["published_at"], "2026-07-21")
        self.assertEqual(okf.serialize(fm, body), text)

    def test_trust_tier_is_derived_from_verified(self):
        self.assertEqual(okf.trust_tier({}), "unverified")
        self.assertEqual(okf.trust_tier({"verified": {"by": "process:ci", "at": "x"}}), "machine-confirmed")
        self.assertEqual(okf.trust_tier({"verified": [{"by": "process:ci"}, {"by": "human:muthu"}]}), "human-reviewed")

    def test_unterminated_frontmatter_is_an_error(self):
        with self.assertRaises(okf.OKFError):
            okf.parse("---\ntype: Note\n")

    def test_resolve_link(self):
        self.assertEqual(okf.resolve_link(Path("."), "a/b/c.md", "../d.md"), "a/d.md")
        self.assertEqual(okf.resolve_link(Path("."), "a/b/c.md", "/x/y.md"), "x/y.md")


class ValidateTests(unittest.TestCase):
    def setUp(self):
        self.b = Bundle().standard()

    def tearDown(self):
        self.b.cleanup()

    def test_good_bundle_passes(self):
        self.assertEqual(validate.validate(self.b.root, CFG), [])

    def test_top_level_folder_must_be_a_theme(self):
        self.b.write("customer-policies/refunds.md", note_fm(id="n2", title="Refund policy"))
        self.assertIn("folders", rules(validate.validate(self.b.root, CFG)))

    def test_note_at_root_is_refused(self):
        self.b.write("stray.md", note_fm(id="n3"))
        self.assertIn("folders", rules(validate.validate(self.b.root, CFG)))

    def test_footnote_without_source(self):
        self.b.write("context-engineering/x.md", note_fm(id="n4"), "Claim.[^s9]\n")
        self.assertIn("footnotes", rules(validate.validate(self.b.root, CFG)))

    def test_source_pointing_at_missing_raw(self):
        self.b.write("context-engineering/x.md", note_fm(id="n5", sources=[{"id": "s1", "resource": "/raw/missing.md"}]))
        self.assertIn("sources", rules(validate.validate(self.b.root, CFG)))

    def test_schema_requires_governance_fields(self):
        fm = note_fm(id="n6")
        del fm["classification"]
        self.b.write("context-engineering/x.md", fm)
        self.assertIn("schema", rules(validate.validate(self.b.root, CFG)))

    def test_unknown_kind_and_non_public(self):
        self.b.write("context-engineering/x.md", note_fm(id="n7", kind="Gossip", classification="internal"))
        found = rules(validate.validate(self.b.root, CFG))
        self.assertIn("schema", found)

    def test_relation_to_missing_note(self):
        self.b.write("context-engineering/x.md", note_fm(id="n8", relations=[{"type": "refines", "target": "/context-engineering/nope.md"}]))
        self.assertIn("relations", rules(validate.validate(self.b.root, CFG)))

    def test_link_to_missing_note(self):
        self.b.write("context-engineering/x.md", note_fm(id="n10"), "See [gone](./gone.md) and [web](https://example.com/a.md).\n")
        found = validate.validate(self.b.root, CFG)
        self.assertEqual([p.message for p in found if p.rule == "links"], ["link to missing ./gone.md"])

    def test_canonical_essay_must_be_on_the_site(self):
        self.b.write("context-engineering/x.md", note_fm(id="n9", canonical_essay="https://example.com/x"))
        self.assertIn("canonical", rules(validate.validate(self.b.root, CFG)))

    def test_raw_copy_needs_publication_date_and_licence(self):
        fm = raw_fm()
        del fm["license_note"]
        self.b.write("raw/2026-other.md", fm, "text")
        self.assertIn("schema", rules(validate.validate(self.b.root, CFG)))


class DateTests(unittest.TestCase):
    def setUp(self):
        self.b = Bundle().standard()

    def tearDown(self):
        self.b.cleanup()

    def test_good_dates_pass(self):
        self.assertEqual(dates.check_dates(self.b.root, today=date(2026, 10, 17)), [])

    def test_source_newer_than_note_fails(self):
        self.b.write("raw/2026-src.md", raw_fm(published_at="2026-10-15"), "text")
        problems = dates.check_dates(self.b.root, today=date(2026, 10, 17))
        self.assertTrue(any("after the note was written" in p.message for p in problems))

    def test_future_dates_fail(self):
        self.b.write("raw/2026-src.md", raw_fm(published_at="2027-01-01"), "text")
        self.assertTrue(dates.check_dates(self.b.root, today=date(2026, 10, 17)))

    def test_missing_publication_date_fails(self):
        fm = raw_fm()
        del fm["published_at"]
        self.b.write("raw/2026-src.md", fm, "text")
        self.assertTrue(any("published_at" in p.message for p in dates.check_dates(self.b.root, today=date(2026, 10, 17))))

    def test_stale_after_must_follow_generation(self):
        self.b.write("context-engineering/curated-overlay.md", note_fm(stale_after="2026-01-01T00:00:00Z"))
        self.assertTrue(dates.check_dates(self.b.root, today=date(2026, 10, 17)))

    def test_stale_notes_are_listed(self):
        self.assertEqual(dates.stale_notes(self.b.root, today=date(2027, 5, 1)), ["context-engineering/curated-overlay.md"])


class BlocklistTests(unittest.TestCase):
    def setUp(self):
        self.b = Bundle().standard()

    def tearDown(self):
        self.b.cleanup()

    def test_whole_word_case_insensitive_and_never_echoes_the_term(self):
        self.b.write("context-engineering/x.md", note_fm(id="n10"), "We used Project Zephyr here; zephyrs are fine.\n")
        problems = blocklist.scan([self.b.root], ["project zephyr", "case:ACME"], self.b.root.parent)
        self.assertEqual(len(problems), 1)
        self.assertNotIn("zephyr", str(problems[0]).lower())

    def test_case_prefix_matches_exact_case_only(self):
        self.b.write("context-engineering/x.md", note_fm(id="n11"), "acme is a word; ACME is a name.\n")
        self.assertEqual(len(blocklist.scan([self.b.root], ["case:ACME"], self.b.root.parent)), 1)

    def test_terms_come_from_the_environment(self):
        with mock.patch.dict(os.environ, {"CONFIDENTIAL_TERMS": "one\n# comment\ntwo|three"}):
            self.assertEqual(blocklist.load_terms(Path("/nonexistent")), ["one", "two", "three"])


if __name__ == "__main__":
    unittest.main()
