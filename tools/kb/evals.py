"""Evaluation set checks.

Offline (CI): every question is non-empty and every expected note exists.
Live (on the Mac, needs the models): ask each question through LLM-Wiki-V2 and report how often an expected note is
among the notes cited, the "right note" rate the CROW paper measures.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

from .validate import Problem


def load(repo: Path) -> list[dict]:
    return yaml.safe_load((repo / "evals" / "questions.yaml").read_text(encoding="utf-8")) or []


def check(repo: Path, bundle: Path) -> list[Problem]:
    problems = []
    for i, item in enumerate(load(repo), 1):
        if not str(item.get("q", "")).strip():
            problems.append(Problem("evals", f"question {i}", "empty question"))
        for rel in item.get("expect") or []:
            if not (bundle / rel).exists():
                problems.append(Problem("evals", f"question {i}", f"expected note {rel} does not exist"))
        if not item.get("expect"):
            problems.append(Problem("evals", f"question {i}", "no expected notes"))
    return problems


def live(repo: Path, bundle: Path) -> float:
    items = load(repo)
    hits = 0
    for item in items:
        out = subprocess.run(["llmwiki2", "--bundle", str(bundle), "ask", item["q"]], capture_output=True, text=True, timeout=600).stdout
        hit = any(rel in out for rel in item["expect"])
        hits += hit
        print(f"{'HIT ' if hit else 'MISS'} {item['q']}")
    rate = hits / len(items) if items else 0.0
    print(f"right-note rate: {hits}/{len(items)} = {rate:.0%}")
    return rate
