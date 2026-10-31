#!/usr/bin/env python3
"""Verify that every attributed quote is verbatim.

Two checks:

  session  Every "quote" [Sxxx] in a debrief session must appear word for word
           in the brain of the seat it is attributed to, next to the same id.
           python scripts/check_quotes.py session sessions/2026-11-02-froze-in-standup

  brain    Every "quote" [Sxxx] in a brain must appear word for word in the raw
           source it cites (the corpus fetched by /newseat into build/<slug>/).
           python scripts/check_quotes.py brain .claude/skills/rewire/brains/adam-grant --corpus build/adam-grant

Matching ignores case, punctuation, and whitespace; words and their order must
match. Exits 1 if any quote fails, so it can gate a commit or a CI run.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from textnorm import find_quotes, loose, split_sections, word_count

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / ".claude" / "skills" / "rewire"
MAX_QUOTE_WORDS = 25
ID_WINDOW = 400  # characters around a quote in which its source id must appear


@dataclass
class Result:
    file: str
    seat: str
    source_id: str
    quote: str
    status: str  # ok | missing | id-mismatch | no-brain | no-source | too-long
    detail: str = ""


def load_roster(skill_dir: Path = SKILL) -> dict[str, dict]:
    roster = json.loads((skill_dir / "roster.json").read_text(encoding="utf-8"))
    return {s["short"].lower(): s for s in roster["seats"]}


def brain_text(brain_dir: Path) -> str:
    """All markdown in a brain except sources.md (titles there are not quotes)."""
    parts = [p.read_text(encoding="utf-8") for p in sorted(brain_dir.glob("*.md")) if p.name != "sources.md"]
    return "\n".join(parts)


def check_in_text(quote: str, source_id: str, haystack: str) -> str:
    """Return ok, id-mismatch, or missing for one quote against loose text."""
    needle = loose(quote)
    flat = loose(haystack)
    if not needle or needle not in flat:
        return "missing"
    # The quote exists; confirm the same id sits near at least one occurrence.
    id_token = f" {source_id.lower()} "
    padded = f" {flat} "
    start = padded.find(needle)
    while start != -1:
        window = padded[max(0, start - ID_WINDOW): start + len(needle) + ID_WINDOW]
        if id_token in window:
            return "ok"
        start = padded.find(needle, start + 1)
    return "id-mismatch"


def check_session(session_dir: Path, skill_dir: Path = SKILL) -> list[Result]:
    roster = load_roster(skill_dir)
    brains = skill_dir / "brains"
    cache: dict[str, str] = {}

    def brain_for(slug: str) -> str | None:
        if slug not in cache:
            d = brains / slug
            cache[slug] = brain_text(d) if (d / "_hot.md").exists() else ""
        return cache[slug] or None

    results: list[Result] = []
    for md in sorted(session_dir.glob("*.md")):
        for heading, body in split_sections(md.read_text(encoding="utf-8")):
            seat = roster.get(heading.lower())
            for quote, sid in find_quotes(body):
                if seat:
                    candidates = [seat]
                else:
                    # Chair notes, brief, debrief: try every seat whose id prefix fits.
                    want_evidence = sid.startswith("E")
                    candidates = [s for s in roster.values() if (s["kind"] == "evidence") == want_evidence]
                status, used = "no-brain", (seat or {}).get("short", "?")
                for cand in candidates:
                    text = brain_for(cand["slug"])
                    if text is None:
                        continue
                    status, used = check_in_text(quote, sid, text), cand["short"]
                    if status == "ok":
                        break
                results.append(Result(md.name, used, sid, quote, status))
    return results


def check_brain(brain_dir: Path, corpus_dir: Path) -> list[Result]:
    manifest_path = corpus_dir / "sources.json"
    if not manifest_path.exists():
        raise SystemExit(f"No sources.json in {corpus_dir}. Fetch sources first.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = {s["id"]: corpus_dir / s["file"] for s in manifest["sources"] if s.get("file")}
    cache: dict[str, str] = {}

    results: list[Result] = []
    for md in sorted(brain_dir.glob("*.md")):
        if md.name == "sources.md":
            continue
        for quote, sid in find_quotes(md.read_text(encoding="utf-8")):
            path = files.get(sid)
            if path is None or not path.exists():
                results.append(Result(md.name, brain_dir.name, sid, quote, "no-source", "id not in sources.json"))
                continue
            if sid not in cache:
                cache[sid] = loose(path.read_text(encoding="utf-8"))
            if loose(quote) not in cache[sid]:
                results.append(Result(md.name, brain_dir.name, sid, quote, "missing", path.name))
            elif word_count(quote) > MAX_QUOTE_WORDS:
                results.append(Result(md.name, brain_dir.name, sid, quote, "too-long",
                                      f"{word_count(quote)} words; keep quotes under {MAX_QUOTE_WORDS}"))
            else:
                results.append(Result(md.name, brain_dir.name, sid, quote, "ok"))
    return results


def report(results: list[Result], as_json: bool) -> int:
    failed = [r for r in results if r.status != "ok"]
    if as_json:
        print(json.dumps({"checked": len(results), "failed": [asdict(r) for r in failed]}, indent=2))
    else:
        for r in failed:
            short = r.quote if len(r.quote) <= 70 else r.quote[:67] + "..."
            print(f"{r.status.upper():12} {r.file} [{r.seat} {r.source_id}] \"{short}\" {r.detail}".rstrip())
        print(f"{len(results)} quotes checked, {len(results) - len(failed)} ok, {len(failed)} failed.")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="mode", required=True)
    s = sub.add_parser("session", help="check a debrief session against the brains")
    s.add_argument("session_dir", type=Path)
    b = sub.add_parser("brain", help="check a brain against its raw sources")
    b.add_argument("brain_dir", type=Path)
    b.add_argument("--corpus", type=Path, required=True, help="build/<slug> folder with sources.json")
    for p in (s, b):
        p.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)

    if args.mode == "session":
        results = check_session(args.session_dir)
    else:
        results = check_brain(args.brain_dir, args.corpus)
    return report(results, args.json)


if __name__ == "__main__":
    sys.exit(main())
