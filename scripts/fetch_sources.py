#!/usr/bin/env python3
"""Fetch a person's public work into a clean text corpus for /newseat.

  python scripts/fetch_sources.py build/adam-grant --list build/adam-grant/urls.txt
  python scripts/fetch_sources.py build/adam-grant --add notes/talk.md --title "Talk" --date 2025-03-01
  python scripts/fetch_sources.py build/adam-grant --sources-md .claude/skills/rewire/brains/adam-grant/sources.md --name "Adam Grant"
  python scripts/fetch_sources.py build/evidence --prefix E --list build/evidence/urls.txt

Each source becomes build/<slug>/corpus/S001-<title>.md and is logged in
build/<slug>/sources.json. YouTube links use yt-dlp captions when yt-dlp is
installed; web pages are converted to plain text. Sources already logged are
skipped, so the command is safe to re-run. Raw sources stay in build/, which git
ignores.

Status per URL: ok, skip (already fetched), thin (under 500 words, often a
paywall or a JavaScript page), fail.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

USER_AGENT = "Mozilla/5.0 (compatible; RewireRoom-fetch/1.0; personal research)"
THIN_WORDS = 500
TIMEOUT = 30
YOUTUBE = re.compile(r"(youtube\.com/watch|youtu\.be/|youtube\.com/live/)")


# ---------- manifest ----------

def load_manifest(build: Path) -> dict:
    path = build / "sources.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"sources": []}


def save_manifest(build: Path, manifest: dict) -> None:
    (build / "sources.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def next_id(manifest: dict, prefix: str) -> str:
    nums = [int(s["id"][1:]) for s in manifest["sources"] if s["id"].startswith(prefix)]
    return f"{prefix}{(max(nums) + 1) if nums else 1:03d}"


def slugify(text: str, limit: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:limit].rstrip("-") or "untitled"


# ---------- text extraction ----------

class _TextExtractor(HTMLParser):
    SKIP = {"script", "style", "noscript", "nav", "footer", "header", "aside", "form", "svg", "button"}
    BLOCK = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "section", "article", "tr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip_depth += 1
        elif tag == "title":
            self._in_title = True
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip_depth:
            self.skip_depth -= 1
        elif tag == "title":
            self._in_title = False
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self.skip_depth:
            self.parts.append(data)


def html_to_text(html: str) -> tuple[str, str]:
    """Return (title, text) from an HTML page."""
    parser = _TextExtractor()
    parser.feed(html)
    raw = "".join(parser.parts)
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in raw.splitlines()]
    text = "\n".join(ln for ln in lines if ln)
    return parser.title.strip(), re.sub(r"\n{3,}", "\n\n", text)


def vtt_to_text(vtt: str) -> str:
    """Flatten WebVTT captions into plain text, dropping timing lines, tags, and
    the rolling duplicates that auto-captions produce."""
    out: list[str] = []
    for line in vtt.splitlines():
        line = line.strip()
        if not line or line == "WEBVTT" or "-->" in line or line.isdigit():
            continue
        if line.startswith(("Kind:", "Language:", "NOTE")):
            continue
        line = re.sub(r"<[^>]+>", "", line).strip()
        if line and (not out or line != out[-1]):
            out.append(line)
    # Auto-captions repeat each line as the next one starts; drop exact repeats.
    deduped = [ln for i, ln in enumerate(out) if i == 0 or ln != out[i - 1]]
    return " ".join(deduped)


# ---------- fetchers ----------

def fetch_web(url: str) -> tuple[str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        ctype = resp.headers.get("Content-Type", "")
        body = resp.read()
    if "pdf" in ctype or url.lower().endswith(".pdf"):
        return fetch_pdf_bytes(body, url)
    charset = "utf-8"
    m = re.search(r"charset=([\w-]+)", ctype)
    if m:
        charset = m.group(1)
    return html_to_text(body.decode(charset, errors="replace"))


def fetch_pdf_bytes(body: bytes, url: str) -> tuple[str, str]:
    if not shutil.which("pdftotext"):
        raise RuntimeError("PDF needs pdftotext (Poppler). Install it, or save the text yourself and use --add.")
    with tempfile.TemporaryDirectory() as tmp:
        pdf = Path(tmp) / "doc.pdf"
        pdf.write_bytes(body)
        subprocess.run(["pdftotext", "-layout", str(pdf), str(pdf.with_suffix(".txt"))], check=True, timeout=120)
        text = pdf.with_suffix(".txt").read_text(encoding="utf-8", errors="replace")
    return Path(url).stem, text


def fetch_youtube(url: str) -> tuple[str, str, str]:
    """Return (title, date, transcript) using yt-dlp captions."""
    if not shutil.which("yt-dlp"):
        raise RuntimeError("YouTube needs yt-dlp. Install it (pip install yt-dlp) or add a transcript with --add.")
    with tempfile.TemporaryDirectory() as tmp:
        meta = subprocess.run(
            ["yt-dlp", "--skip-download", "--print", "%(title)s\t%(upload_date)s", url],
            capture_output=True, text=True, timeout=120, check=True,
        ).stdout.strip().split("\t")
        title = meta[0] if meta else url
        raw_date = meta[1] if len(meta) > 1 else ""
        subprocess.run(
            ["yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs", "--sub-langs", "en.*,en",
             "--sub-format", "vtt", "-o", f"{tmp}/cap.%(ext)s", url],
            capture_output=True, text=True, timeout=180, check=True,
        )
        vtts = sorted(Path(tmp).glob("*.vtt"))
        if not vtts:
            raise RuntimeError("no English captions")
        # Prefer human captions (en.vtt) over auto captions (en-orig, auto) when both exist.
        best = min(vtts, key=lambda p: (len(p.name), p.name))
        text = vtt_to_text(best.read_text(encoding="utf-8", errors="replace"))
    when = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}" if len(raw_date) == 8 else ""
    return title, when, text


# ---------- commands ----------

def save_source(build: Path, manifest: dict, prefix: str, *, url: str, title: str,
                when: str, text: str, kind: str) -> tuple[str, int]:
    sid = next_id(manifest, prefix)
    words = len(text.split())
    rel = f"corpus/{sid}-{slugify(title)}.md"
    path = build / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    header = f"# {title}\n\nSource: {url or 'local'}\nDate: {when or 'unknown'}\nId: {sid}\n\n"
    path.write_text(header + text.strip() + "\n", encoding="utf-8")
    manifest["sources"].append({
        "id": sid, "title": title, "url": url, "date": when, "kind": kind,
        "words": words, "file": rel, "fetched": date.today().isoformat(),
    })
    save_manifest(build, manifest)
    return sid, words


def read_url_list(path: Path) -> list[tuple[str, str]]:
    """Return (group, url) pairs. Lines starting with # set the group."""
    group, items = "", []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            group = line.lstrip("#").strip()
        else:
            items.append((group, line.split()[0]))
    return items


def cmd_list(build: Path, url_file: Path, prefix: str) -> int:
    manifest = load_manifest(build)
    seen = {s["url"] for s in manifest["sources"] if s.get("url")}
    counts = {"ok": 0, "skip": 0, "thin": 0, "fail": 0}
    for group, url in read_url_list(url_file):
        if url in seen:
            counts["skip"] += 1
            print(f"skip  {url}")
            continue
        try:
            if YOUTUBE.search(url):
                title, when, text = fetch_youtube(url)
                kind = "video"
            else:
                title, text = fetch_web(url)
                when, kind = "", "web"
            title = title or url
            sid, words = save_source(build, manifest, prefix, url=url, title=title, when=when, text=text, kind=kind)
            seen.add(url)
            status = "thin" if words < THIN_WORDS else "ok"
            counts[status] += 1
            print(f"{status:<5} {sid} {words:>6} words  {title[:70]}")
        except (urllib.error.URLError, subprocess.SubprocessError, RuntimeError, OSError, ValueError) as exc:
            counts["fail"] += 1
            print(f"fail  {url}  ({exc})")
    print_manifest(manifest, counts)
    return 0


def cmd_add(build: Path, file: Path, title: str, when: str, prefix: str) -> int:
    manifest = load_manifest(build)
    text = file.read_text(encoding="utf-8", errors="replace")
    sid, words = save_source(build, manifest, prefix, url="", title=title, when=when, text=text, kind="local")
    print(f"ok    {sid} {words:>6} words  {title}")
    return 0


def cmd_sources_md(build: Path, out: Path, name: str) -> int:
    manifest = load_manifest(build)
    good = [s for s in manifest["sources"] if s["words"] >= THIN_WORDS]
    total = sum(s["words"] for s in good)
    dates = sorted(s["date"] for s in good if s["date"])
    span = f"{dates[0][:7]} to {dates[-1][:7]}" if dates else "dates unknown"
    lines = [
        f"# {name}: sources", "",
        f"{len(good)} sources, {total:,} words, {span}. Built {date.today().isoformat()}. "
        f"Raw files live in build/ and are not committed.", "",
        "Format: id | title | url | date", "",
    ]
    lines += [f"- {s['id']} | {s['title']} | {s['url'] or 'local'} | {s['date'] or 'unknown'}" for s in good]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(good)} sources).")
    return 0


def print_manifest(manifest: dict, counts: dict) -> None:
    good = [s for s in manifest["sources"] if s["words"] >= THIN_WORDS]
    print(f"\nThis run: {counts['ok']} ok, {counts['thin']} thin, {counts['fail']} failed, {counts['skip']} skipped.")
    print(f"Corpus: {len(good)} usable sources, {sum(s['words'] for s in good):,} words.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("build", type=Path, help="build/<slug> folder")
    parser.add_argument("--prefix", default="S", choices=["S", "E"], help="S for a persona seat, E for the Evidence seat")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", type=Path, help="text file of URLs, one per line, # lines for groups")
    group.add_argument("--add", type=Path, help="a local text or markdown file")
    group.add_argument("--sources-md", type=Path, help="write the brain's sources.md")
    parser.add_argument("--title", help="title for --add")
    parser.add_argument("--date", default="", help="YYYY-MM-DD for --add")
    parser.add_argument("--name", help="person's full name for --sources-md")
    args = parser.parse_args(argv)

    args.build.mkdir(parents=True, exist_ok=True)
    if args.list:
        return cmd_list(args.build, args.list, args.prefix)
    if args.add:
        if not args.title:
            parser.error("--add needs --title")
        return cmd_add(args.build, args.add, args.title, args.date, args.prefix)
    if not args.name:
        parser.error("--sources-md needs --name")
    return cmd_sources_md(args.build, args.sources_md, args.name)


if __name__ == "__main__":
    sys.exit(main())
