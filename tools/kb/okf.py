"""Read and write OKF v0.2 documents and walk a bundle. Standard library and PyYAML only.

A document is a YAML frontmatter block between `---` lines, a blank line, then a Markdown body. Timestamps are
kept as the text written (YAML 1.1 would turn them into datetimes and rewrite them on save), matching the way
LLM-Wiki-V2 reads and writes the same files, so a round trip never changes a byte it did not mean to.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

import yaml

INDEX = "index.md"
LOG = "log.md"
RAW = "raw"


class OKFError(ValueError):
    pass


class _Loader(yaml.SafeLoader):
    pass


_Loader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


@dataclass
class Doc:
    path: Path
    rel: str  # bundle-relative, posix, no leading slash
    frontmatter: dict[str, Any] = field(default_factory=dict)
    body: str = ""

    @property
    def is_raw(self) -> bool:
        return self.rel.startswith(f"{RAW}/")

    @property
    def top_folder(self) -> str:
        return self.rel.split("/", 1)[0] if "/" in self.rel else ""

    @property
    def bundle_path(self) -> str:
        return "/" + self.rel


def parse(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise OKFError("unterminated frontmatter")
    try:
        fm = yaml.load("\n".join(lines[1:end]), Loader=_Loader) or {}
    except yaml.YAMLError as e:
        raise OKFError(f"invalid YAML in frontmatter: {e}") from e
    if not isinstance(fm, dict):
        raise OKFError("frontmatter is not a mapping")
    return fm, "\n".join(lines[end + 1 :]).removeprefix("\n")


def serialize(frontmatter: dict[str, Any], body: str) -> str:
    fm = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).rstrip()
    body = body if body.endswith("\n") else body + "\n"
    return f"---\n{fm}\n---\n\n{body}"


def read(path: Path, root: Path) -> Doc:
    fm, body = parse(path.read_text(encoding="utf-8"))
    return Doc(path, path.relative_to(root).as_posix(), fm, body)


def write(doc: Doc) -> None:
    doc.path.write_text(serialize(doc.frontmatter, doc.body), encoding="utf-8")


def documents(root: Path) -> Iterator[Doc]:
    """Every concept document in the bundle (not index.md, log.md or hidden folders), sorted by path."""
    for path in sorted(root.rglob("*.md")):
        rel_parts = path.relative_to(root).parts
        if any(p.startswith(".") for p in rel_parts) or path.name in (INDEX, LOG):
            continue
        yield read(path, root)


def notes(root: Path) -> Iterator[Doc]:
    return (d for d in documents(root) if not d.is_raw)


def raws(root: Path) -> Iterator[Doc]:
    return (d for d in documents(root) if d.is_raw)


FOOTNOTE_REF = re.compile(r"\[\^([A-Za-z0-9_-]+)\](?!:)")
MD_LINK = re.compile(r"\]\(([^)\s#]+\.md)(?:#[^)]*)?\)")


def resolve_link(root: Path, from_rel: str, link: str) -> str:
    """Bundle-relative path a Markdown link points to (links may be bundle-absolute or relative)."""
    if link.startswith("/"):
        return link.lstrip("/")
    base = Path(from_rel).parent
    parts: list[str] = []
    for part in (base / link).parts:
        if part == "..":
            if parts:
                parts.pop()
        elif part != ".":
            parts.append(part)
    return "/".join(parts)


def verifications(fm: dict[str, Any]) -> list[dict[str, Any]]:
    """OKF: `verified` may be one mapping or a list; consumers treat a mapping as a one-element list."""
    v = fm.get("verified")
    if isinstance(v, dict):
        return [v]
    if isinstance(v, list):
        return [x for x in v if isinstance(x, dict)]
    return []


def trust_tier(fm: dict[str, Any]) -> str:
    """OKF v0.2 section 5.3: derived from `verified`, never stored."""
    vs = verifications(fm)
    if not vs:
        return "unverified"
    if any(str(x.get("by", "")).startswith("human:") for x in vs):
        return "human-reviewed"
    return "machine-confirmed"
