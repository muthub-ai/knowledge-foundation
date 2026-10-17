# SPDX-License-Identifier: AGPL-3.0-or-later
# Imports LLM-Wiki-V2 (AGPL-3.0-or-later). See LICENSES/README.md.
"""The whole pipeline, end to end, on a copy of this repository:

capture in inbox/ -> ingest through the real LLM-Wiki-V2 Librarian in CROW mode (scripted local classifier and Claude
stand-ins, no network) -> kb normalize -> kb check -> llmwiki2 check -> owner approval stamp -> graph -> release
bundle -> the website build (when knowledge-foundation-site sits next to this repository).

Plus the ways it must fail: a confidential term, a dangling link, a future date, a bot trying to stamp a review,
a full third-party text, and a capture with no publication date.

Skipped when llmwiki2 is not installed (pip install -r requirements.txt).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
APPROVED_AT = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")  # the approval happens "now": a future stamp fails kb dates
SITE = Path(os.environ.get("KF_SITE_REPO", REPO.parent / "knowledge-foundation-site"))

try:
    from llmw2 import Wiki, WikiConfig  # type: ignore[import-not-found]
    from llmw2.config import ClassifierConfig, LLMConfig  # type: ignore[import-not-found]
    from llmw2.models.classifier import Classifier  # type: ignore[import-not-found]
    from llmw2.models.llm import LLM  # type: ignore[import-not-found]
    from llmw2.models.usage import UsageTracker  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    Wiki = None  # type: ignore[assignment,misc]

CAPTURE = """---
title: Introducing the Open Knowledge Format
resource: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
published_at: 2026-06-12
origin_kind: third-party-note
license_note: cite and paraphrase only
why: The format this wiki is stored in.
---
My notes. Google proposed the Open Knowledge Format: knowledge kept as Markdown files with YAML frontmatter, so people,
agents and search systems read the same source. Each document records its sources and when it was generated and verified.
"""

NOTE_BODY = (
    "# Overview\n\nThe Open Knowledge Format keeps knowledge as Markdown with YAML frontmatter, so people and agents read "
    "the same files.[^s1]\n\n# Why it matters here\n\nIt is the format this wiki is stored in, and it carries provenance "
    "with every note.[^s1]\n"
)


if Wiki is not None:

    class ScriptedClaude(LLM):
        """Answers by prompt type, like Claude would, without the network. Unexpected calls fail the test."""

        def __init__(self, usage: Any) -> None:
            super().__init__(LLMConfig(model="claude-sonnet-5-5"), usage)
            self.ops: list[str] = []

        def chat(self, messages, *, op="", json_mode=False, max_tokens=None):  # noqa: ANN001
            self.ops.append(op)
            self.usage.record("llm", self.model, 100, 10, op=op)
            if op == "librarian/summarize":
                return json.dumps({"title": "Open Knowledge Format", "summary": "Google's format for knowledge as Markdown with provenance.",
                                   "tags": ["context-engineering", "okf"], "body": NOTE_BODY})
            if op == "librarian/name_folder":
                return json.dumps({"name": "standards", "description": "Formats and standards."})
            raise AssertionError(f"unexpected LLM call {op!r}")

    class ScriptedClassifier(Classifier):
        """The local classifier: routes to context-engineering, finds no existing match, relates to one essay."""

        def __init__(self, usage: Any) -> None:
            super().__init__(ClassifierConfig(model="tev1-8k", api_key="local"), usage)
            self.ops: list[str] = []

        def ask(self, state, questions, *, op=""):  # noqa: ANN001
            self.ops.append(op)
            self.usage.record("classifier", self.model, 50, 0, op=op)
            out: dict[str, Any] = {}
            for key, q in questions.items():
                if q["type"] == "choice":
                    opts = list(q["criteria"])
                    pick = next((o for o in ("context-engineering", "Here", "New note") if o in opts), opts[0])
                    out[key] = {"type": "choice", "choice": pick, "probabilities": {pick: 0.92}, "confidence": 0.92}
                else:
                    text = q["instructions"]
                    score = 0.0 if op == "match" else (0.9 if "context" in text.lower() and op == "relate" else 0.05)
                    out[key] = {"type": "noul", "noul": score}
            return out


def run(cmd: list[str], cwd: Path, env: dict[str, str] | None = None, ok: bool = True) -> subprocess.CompletedProcess[str]:
    e = {**os.environ, "PYTHONPATH": str(cwd / "tools") + os.pathsep + os.environ.get("PYTHONPATH", ""), **(env or {})}
    p = subprocess.run(cmd, cwd=cwd, env=e, text=True, capture_output=True, timeout=300)
    if ok and p.returncode != 0:
        raise AssertionError(f"{' '.join(cmd)} failed ({p.returncode}):\n{p.stdout}\n{p.stderr}")
    return p


@unittest.skipIf(Wiki is None, "llmwiki2 is not installed")
class EndToEnd(unittest.TestCase):
    BLOCKED = "Zebracorn Ledger"  # a made-up confidential term for this test only

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.repo = self.tmp / "kf"
        shutil.copytree(REPO, self.repo, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", ".confidential-terms.txt"))
        (self.repo / ".confidential-terms.txt").write_text(f"# test list\n{self.BLOCKED}\n", encoding="utf-8")
        self.bundle = self.repo / "wiki"
        sys.path.insert(0, str(self.repo / "tools"))
        sys.path.insert(0, str(self.repo / "tools" / "librarian"))

    def tearDown(self):
        sys.path[:] = [p for p in sys.path if not p.startswith(str(self.tmp))]
        for m in [m for m in sys.modules if m == "ingest" or m == "kb" or m.startswith("kb.")]:
            del sys.modules[m]
        shutil.rmtree(self.tmp)

    def ingest(self, name: str, text: str) -> tuple[dict[str, Any], Any, Any]:
        import ingest as ing  # the copy under test
        from kb.config import Config

        cap = self.repo / "inbox" / name
        cap.write_text(text, encoding="utf-8")
        tracker = UsageTracker()
        llm, clf = ScriptedClaude(tracker), ScriptedClassifier(tracker)

        def factory(bundle: Path) -> Any:
            return Wiki(WikiConfig(bundle=bundle, mode="crow"), llm=llm, classifier=clf)

        return ing.ingest(cap, cfg=Config(repo=self.repo), wiki_factory=factory), llm, clf

    def kb(self, *args: str, ok: bool = True) -> subprocess.CompletedProcess[str]:
        return run([sys.executable, "-m", "kb", *args], self.repo, ok=ok)

    # -- the happy path -------------------------------------------------------------
    def test_capture_to_published_site(self):
        before = run([sys.executable, "-m", "llmw2", "--bundle", "wiki", "check"], self.repo, ok=False)
        self.assertEqual(before.returncode, 0, before.stdout + before.stderr)

        out, llm, clf = self.ingest("2026-10-20-okf.md", CAPTURE)
        self.assertEqual(out["action"], "created", out)
        note_rel = out["note"].lstrip("/")
        self.assertTrue(note_rel.startswith("context-engineering/"), note_rel)
        self.assertIn("route", clf.ops)  # the local classifier routed
        self.assertEqual(llm.ops.count("librarian/summarize"), 1)  # Claude wrote
        self.assertNotIn("librarian/route", llm.ops)  # and did not route
        self.assertTrue((self.repo / "inbox" / "done" / "2026-10-20-okf.md").exists())

        from kb import okf

        raw = okf.read(self.bundle / out["raw"], self.bundle).frontmatter
        self.assertEqual((raw["published_at"], raw["origin_kind"]), ("2026-06-12", "third-party-note"))

        changed = self.kb("normalize", f"wiki/{note_rel}").stdout
        self.assertIn(note_rel, changed)
        fm = okf.read(self.bundle / note_rel, self.bundle).frontmatter
        self.assertEqual((fm["status"], fm["classification"], fm["kind"]), ("draft", "public", "Concept"))
        self.assertIn("stale_after", fm)
        self.assertNotIn("verified", fm)  # the machine never verifies

        check = self.kb("check", "--require-blocklist")
        self.assertIn("blocklist: 0 problem(s)", check.stdout)
        run([sys.executable, "-m", "llmw2", "--bundle", "wiki", "check"], self.repo)

        # Owner approves the pull request -> stamp
        with self.assertRaises(AssertionError):
            self.kb("stamp", "--by", "llmwiki2/lint", "--at", APPROVED_AT, f"wiki/{note_rel}")
        self.kb("stamp", "--by", "human:muthu", "--at", APPROVED_AT, f"wiki/{note_rel}")
        again = self.kb("stamp", "--by", "human:muthu", "--at", APPROVED_AT, f"wiki/{note_rel}").stdout
        self.assertIn("nothing to stamp", again)  # idempotent
        fm = okf.read(self.bundle / note_rel, self.bundle).frontmatter
        self.assertEqual(fm["verified"], {"by": "human:muthu", "at": APPROVED_AT})
        self.assertEqual(fm["status"], "stable")
        self.kb("check", "--require-blocklist")
        run([sys.executable, "-m", "llmw2", "--bundle", "wiki", "check"], self.repo)

        # Publish: graph + release bundle, exactly as publish.yml does
        self.kb("graph", "--out", "dist", "--revision", "test")
        g = json.loads((self.repo / "dist" / "graph.json").read_text())
        node = next(n for n in g["nodes"] if n["id"] == note_rel)
        self.assertEqual(node["trust"], "human-reviewed")
        self.assertTrue(any(e["source"] == note_rel and e["type"] == "draws_on" and e["target"] == out["raw"] for e in g["edges"]))
        with tarfile.open(self.repo / "dist" / "bundle.tgz", "w:gz") as tar:
            for name in ("wiki", "wiki.config.yaml", "schemas", "ontology"):
                tar.add(self.repo / name, arcname=name)

        if not (SITE / "kfsite").exists():
            self.skipTest("knowledge-foundation-site is not next to this repository")
        release = self.tmp / "release"
        release.mkdir()
        with tarfile.open(self.repo / "dist" / "bundle.tgz") as tar:
            tar.extractall(release, filter="data")
        shutil.copy(self.repo / "dist" / "graph.json", release / "graph.json")
        # The site's own steps: stage the release as Quartz content, then (Quartz itself needs npm, so the site's
        # Quartz stand-in renders it) the finishing step. The real Quartz build is tested in the site's CI.
        content, public = self.tmp / "content", self.tmp / "public"
        run([sys.executable, "tests/build_preview.py", "--bundle", str(release / "wiki"), "--graph", str(release / "graph.json"),
             "--content", str(content), "--public", str(public)], SITE)
        staged = (content / note_rel).read_text()
        self.assertIn("> [!success] Reviewed by Muthu", staged)
        self.assertIn("Last verified " + datetime.strptime(APPROVED_AT[:10], "%Y-%m-%d").strftime("%b %-d, %Y"), staged)
        self.assertIn("[Introducing the Open Knowledge Format](https://cloud.google.com/blog/products/data-analytics/"
                      "how-the-open-knowledge-format-can-improve-data-sharing) · published Jun 12, 2026", staged)
        self.assertFalse((content / out["raw"]).exists())  # source copies are not published
        page = (public / (note_rel.removesuffix(".md") + ".html")).read_text()
        self.assertIn('data-kf="jsonld"', page)
        self.assertIn(note_rel.removesuffix(".md") + ".md", (public / "llms.txt").read_text())
        self.assertIn(note_rel, (public / "graph.json").read_text())

    # -- the ways it must fail -------------------------------------------------------
    def test_confidential_term_fails_the_check_without_printing_it(self):
        self.ingest("leak.md", CAPTURE.replace("My notes.", f"My notes on the {self.BLOCKED}."))
        p = self.kb("check", "--require-blocklist", ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertNotIn(self.BLOCKED, p.stdout + p.stderr)
        self.assertNotIn(self.BLOCKED.lower(), (p.stdout + p.stderr).lower())

    def test_missing_blocklist_fails_when_required(self):
        (self.repo / ".confidential-terms.txt").unlink()
        p = run([sys.executable, "-m", "kb", "check", "--require-blocklist"], self.repo, env={"CONFIDENTIAL_TERMS": ""}, ok=False)
        self.assertNotEqual(p.returncode, 0)

    def test_dangling_link_and_future_date_fail(self):
        out, _, _ = self.ingest("2026-10-20-okf.md", CAPTURE)
        note = self.bundle / out["note"].lstrip("/")
        self.kb("normalize")
        self.kb("validate")  # clean before the damage
        text = note.read_text()
        note.write_text(text.replace("# Overview\n", "# Overview\n\nSee [a note that does not exist](./nope.md).\n", 1))
        p = self.kb("validate", ok=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("nope.md", p.stdout)
        raw = self.bundle / out["raw"]
        raw.write_text(raw.read_text().replace("published_at: '2026-06-12'", "published_at: '2099-01-01'").replace("published_at: 2026-06-12", "published_at: 2099-01-01"))
        p = self.kb("dates", ok=False)
        self.assertNotEqual(p.returncode, 0)

    def test_bad_captures_are_refused_before_any_model_call(self):
        import ingest as ing

        for name, text in (("long.md", CAPTURE + "word " * 1000), ("nodate.md", CAPTURE.replace("published_at: 2026-06-12\n", "")),
                           ("kind.md", CAPTURE.replace("third-party-note", "blog"))):
            with self.subTest(name), self.assertRaises(ing.CaptureError):
                self.ingest(name, text)
            self.assertTrue((self.repo / "inbox" / name).exists())  # left in place for the author to fix

    def test_second_ingest_of_the_same_text_changes_nothing(self):
        self.ingest("a.md", CAPTURE)
        before = {p: p.read_text() for p in self.bundle.rglob("*.md")}
        out, llm, _ = self.ingest("b.md", CAPTURE)
        self.assertEqual(out["action"], "unchanged")
        self.assertEqual(llm.ops, [])
        self.assertEqual(before, {p: p.read_text() for p in self.bundle.rglob("*.md")})


if __name__ == "__main__":
    unittest.main()
