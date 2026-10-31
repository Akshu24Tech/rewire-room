"""Shared text helpers for Rewire Room scripts. Standard library only."""

from __future__ import annotations

import re
import unicodedata

# A verbatim quote with a source id: "exact words" [S014], "exact words" [S014, 2024],
# or “exact words” [E012]. Anything after the comma is ignored, so an odd year format
# cannot make the checker silently skip a quote.
QUOTE_RE = re.compile(r'["“]([^"“”\n]{6,}?)["”]\s*\[([SE]\d{3,4})(?:,[^\]\n]*)?\]')

_PUNCT_MAP = {
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", "…": "...", " ": " ",
}


def loose(text: str) -> str:
    """Normalize text for verbatim matching.

    Case, punctuation, and whitespace differences are ignored, so a quote copied
    from a transcript still matches after light cleanup. Words and their order
    must match exactly.
    """
    text = unicodedata.normalize("NFKC", text)
    for src, dst in _PUNCT_MAP.items():
        text = text.replace(src, dst)
    text = text.lower().replace("'", "")  # it's -> its, so contractions match either way
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def find_quotes(text: str) -> list[tuple[str, str]]:
    """Return (quote, source_id) pairs in reading order."""
    return [(m.group(1).strip(), m.group(2)) for m in QUOTE_RE.finditer(text)]


def word_count(text: str) -> int:
    return len(loose(text).split())


def split_sections(markdown: str) -> list[tuple[str, str]]:
    """Split markdown into (level-2 heading, body) pairs. Text before the first
    level-2 heading is returned under the heading ""."""
    sections: list[tuple[str, str]] = []
    heading, buf = "", []
    for line in markdown.splitlines():
        if line.startswith("## "):
            sections.append((heading, "\n".join(buf)))
            heading, buf = line[3:].strip(), []
        else:
            buf.append(line)
    sections.append((heading, "\n".join(buf)))
    return sections
