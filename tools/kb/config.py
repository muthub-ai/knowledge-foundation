"""Repository configuration: wiki.config.yaml, the ontology and the schemas."""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any

import yaml

REPO = Path(__file__).resolve().parents[2]


@dataclass
class Config:
    repo: Path = REPO

    @cached_property
    def data(self) -> dict[str, Any]:
        return yaml.safe_load((self.repo / "wiki.config.yaml").read_text(encoding="utf-8"))

    @property
    def bundle(self) -> Path:
        return self.repo / self.data["bundle"]

    @property
    def themes(self) -> dict[str, str]:
        return dict(self.data["themes"])

    def theme_label(self, theme: str) -> str:
        return str((self.data.get("theme_labels") or {}).get(theme) or theme.replace("-", " ").capitalize())

    @property
    def kinds(self) -> list[str]:
        return list(self.data["kinds"])

    @property
    def owner_actor(self) -> str:
        return self.data["author"]["actor"]

    def stale_months(self, kind: str) -> int:
        table = self.data["stale_after_months"]
        return int(table.get(kind, table["default"]))

    @cached_property
    def edge_types(self) -> list[dict[str, str]]:
        return yaml.safe_load((self.repo / "ontology" / "edge-types.yaml").read_text(encoding="utf-8"))

    def schema(self, name: str) -> dict[str, Any]:
        return json.loads((self.repo / "schemas" / f"{name}.schema.json").read_text(encoding="utf-8"))
