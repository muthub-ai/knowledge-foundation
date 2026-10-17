"""Confidential-terms guardrail. The list itself is private: it comes from the CONFIDENTIAL_TERMS environment
variable (a GitHub secret) or a git-ignored .confidential-terms.txt, one term per line, # for comments, and a
`case:` prefix for exact-case matching. Matching is whole-word and case-insensitive otherwise.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from .validate import Problem

SCAN_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt"}


def load_terms(repo: Path) -> list[str]:
    text = os.environ.get("CONFIDENTIAL_TERMS", "")
    f = repo / ".confidential-terms.txt"
    if f.exists():
        text += "\n" + f.read_text(encoding="utf-8")
    return [t.strip() for t in text.replace("|", "\n").splitlines() if t.strip() and not t.strip().startswith("#")]


def _pattern(term: str) -> re.Pattern[str]:
    if term.startswith("case:"):
        return re.compile(r"(?<![A-Za-z0-9])" + re.escape(term[5:]) + r"(?![A-Za-z0-9])")
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])", re.IGNORECASE)


def scan(paths: list[Path], terms: list[str], root: Path) -> list[Problem]:
    patterns = [(t, _pattern(t)) for t in terms]
    problems = []
    for base in paths:
        files = [base] if base.is_file() else sorted(p for p in base.rglob("*") if p.is_file())
        for f in files:
            if f.suffix not in SCAN_SUFFIXES or any(part.startswith(".") for part in f.relative_to(root).parts):
                continue
            text = f.read_text(encoding="utf-8", errors="replace")
            for term, rx in patterns:
                for m in rx.finditer(text):
                    line = text.count("\n", 0, m.start()) + 1
                    # Never echo the term itself into CI logs: report its position in the list only.
                    problems.append(Problem("blocklist", f"{f.relative_to(root).as_posix()}:{line}", f"confidential term #{terms.index(term) + 1}"))
    return problems
