from __future__ import annotations

from . import Extraction, NoteText


class NullExtractor:
    name = "none"

    def extract(self, notes: list[NoteText]) -> Extraction:
        return Extraction(extractor=self.name)
