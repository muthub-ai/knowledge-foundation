"""Command line for the wiki's governance tools.

  python -m kb check [--require-blocklist]     validate + dates + blocklist (what CI runs on every pull request)
  python -m kb validate | dates | blocklist
  python -m kb normalize [PATH ...]            add governance defaults to notes (curator, on a branch)
  python -m kb stamp --by human:muthu --at TS PATH ...   add the approval verification (approve workflow)
  python -m kb graph --out dist [--extractor semantica|none] [--revision SHA]
  python -m kb stale                           notes past stale_after
  python -m kb evals [--live]                  evaluation set (offline structure check, or live right-note rate)

Run from the repository root with PYTHONPATH=tools.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import blocklist, dates, evals, governance, graph, validate
from .config import Config
from .extractors import get as get_extractor


def _report(problems: list, label: str) -> int:
    for p in problems:
        print(p)
    print(f"{label}: {len(problems)} problem(s)")
    return 1 if problems else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="kb")
    ap.add_argument("--bundle", type=Path, help="bundle folder (default from wiki.config.yaml)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--require-blocklist", action="store_true", help="fail when no confidential terms are configured")
    sub.add_parser("validate")
    sub.add_parser("dates")
    b = sub.add_parser("blocklist")
    b.add_argument("--require-blocklist", action="store_true")
    n = sub.add_parser("normalize")
    n.add_argument("paths", nargs="*")
    s = sub.add_parser("stamp")
    s.add_argument("--by", required=True)
    s.add_argument("--at", required=True)
    s.add_argument("paths", nargs="+")
    g = sub.add_parser("graph")
    g.add_argument("--out", type=Path, required=True)
    g.add_argument("--extractor", default="none")
    g.add_argument("--revision", default="")
    sub.add_parser("stale")
    e = sub.add_parser("evals")
    e.add_argument("--live", action="store_true", help="ask LLM-Wiki-V2 (needs the models; run on the Mac)")
    args = ap.parse_args(argv)

    cfg = Config()
    bundle = args.bundle or cfg.bundle

    def run_blocklist(require: bool) -> int:
        terms = blocklist.load_terms(cfg.repo)
        if not terms:
            print("blocklist: no confidential terms configured" + (" (required)" if require else " (skipped)"))
            return 1 if require else 0
        targets = [p for p in (bundle, cfg.repo / "inbox") if p.exists()]
        return _report(blocklist.scan(targets, terms, cfg.repo), "blocklist")

    if args.cmd == "validate":
        return _report(validate.validate(bundle, cfg), "validate")
    if args.cmd == "dates":
        return _report(dates.check_dates(bundle), "dates")
    if args.cmd == "blocklist":
        return run_blocklist(args.require_blocklist)
    if args.cmd == "check":
        rc = _report(validate.validate(bundle, cfg), "validate")
        rc |= _report(dates.check_dates(bundle), "dates")
        rc |= run_blocklist(args.require_blocklist)
        rc |= _report(evals.check(cfg.repo, bundle), "evals")
        return rc
    if args.cmd == "normalize":
        changed = governance.normalize(bundle, cfg, paths=[p.removeprefix(f"{bundle.name}/") for p in args.paths] or None)
        print("\n".join(changed) or "nothing to normalize")
        return 0
    if args.cmd == "stamp":
        done = governance.stamp(bundle, [p.removeprefix(f"{bundle.name}/") for p in args.paths], by=args.by, at=args.at)
        print("\n".join(done) or "nothing to stamp")
        return 0
    if args.cmd == "graph":
        g_, report = graph.build(bundle, cfg, get_extractor(args.extractor), revision=args.revision)
        graph.write_outputs(g_, report, args.out)
        print(report)
        return 0
    if args.cmd == "evals":
        if args.live:
            evals.live(cfg.repo, bundle)
            return 0
        return _report(evals.check(cfg.repo, bundle), "evals")
    if args.cmd == "stale":
        rels = dates.stale_notes(bundle)
        print("\n".join(rels) or "no stale notes")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
