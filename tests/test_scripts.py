"""Tests for the Rewire Room scripts. Run: python -m unittest discover -s tests"""

from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import check_quotes  # noqa: E402
import fetch_sources  # noqa: E402
import ledger  # noqa: E402
from textnorm import find_quotes, loose, split_sections  # noqa: E402


class TextNormTests(unittest.TestCase):
    def test_loose_ignores_case_punctuation_and_curly_quotes(self):
        self.assertEqual(loose("It’s  NOT, the end!"), loose("its not the end"))

    def test_find_quotes_reads_straight_and_curly(self):
        text = 'He said "practice beats insight" [S012] and “slow is smooth” [E004].'
        self.assertEqual(find_quotes(text), [("practice beats insight", "S012"), ("slow is smooth", "E004")])

    def test_find_quotes_skips_quotes_without_ids(self):
        self.assertEqual(find_quotes('a "plain quote here" with no id'), [])

    def test_split_sections(self):
        sections = split_sections("intro\n## Grant\ncard\n## Chair notes\nnotes")
        self.assertEqual([h for h, _ in sections], ["", "Grant", "Chair notes"])


def make_skill(root: Path) -> Path:
    skill = root / "skill"
    (skill / "brains" / "adam-grant").mkdir(parents=True)
    (skill / "brains" / "evidence").mkdir(parents=True)
    roster = {"seats": [
        {"key": "grant", "short": "Grant", "slug": "adam-grant", "kind": "persona"},
        {"key": "evidence", "short": "Evidence", "slug": "evidence", "kind": "evidence"},
        {"key": "greene", "short": "Greene", "slug": "robert-greene", "kind": "persona"},
    ]}
    (skill / "roster.json").write_text(json.dumps(roster))
    (skill / "brains" / "adam-grant" / "_hot.md").write_text(
        "## Rules\n1. **Stretch.** \"Discomfort is a sign of growth, not failure.\" [S014, 2024]\n")
    (skill / "brains" / "adam-grant" / "sources.md").write_text("- S099 | A title that is not a quote |\n")
    (skill / "brains" / "evidence" / "_hot.md").write_text("Exposure works: \"repeated exposure reduces fear\" [E003]\n")
    return skill


class SessionCheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.skill = make_skill(root)
        self.session = root / "session"
        self.session.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def run_check(self, text: str):
        (self.session / "round-1.md").write_text(text)
        return {(r.quote, r.status) for r in check_quotes.check_session(self.session, self.skill)}

    def test_verbatim_quote_passes(self):
        res = self.run_check('## Grant\nAs I put it, "discomfort is a sign of growth not failure" [S014].')
        self.assertEqual(res, {("discomfort is a sign of growth not failure", "ok")})

    def test_invented_quote_fails(self):
        res = self.run_check('## Grant\n"Introverts should just fake it" [S014]')
        self.assertEqual(res, {("Introverts should just fake it", "missing")})

    def test_wrong_source_id_fails(self):
        res = self.run_check('## Grant\n"Discomfort is a sign of growth" [S077]')
        self.assertEqual(res, {("Discomfort is a sign of growth", "id-mismatch")})

    def test_quote_attributed_to_seat_without_brain(self):
        res = self.run_check('## Greene\n"Know your own nature well" [S001]')
        self.assertEqual(res, {("Know your own nature well", "no-brain")})

    def test_chair_notes_quotes_check_against_all_brains(self):
        res = self.run_check('## Chair notes\nThe audit cited "repeated exposure reduces fear" [E003].')
        self.assertEqual(res, {("repeated exposure reduces fear", "ok")})

    def test_cross_seat_quote_fails(self):
        # A Grant line quoted under the Evidence heading is not in the Evidence brain.
        res = self.run_check('## Evidence\n"Discomfort is a sign of growth" [S014]')
        self.assertEqual(res, {("Discomfort is a sign of growth", "missing")})


class BrainCheckTests(unittest.TestCase):
    def test_brain_against_corpus(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build = root / "build"
            (build / "corpus").mkdir(parents=True)
            (build / "corpus" / "S001-talk.md").write_text("Um, so, the thing is: discomfort is a sign of growth, not failure.")
            (build / "sources.json").write_text(json.dumps({"sources": [
                {"id": "S001", "file": "corpus/S001-talk.md", "words": 600}]}))
            brain = root / "brain"
            brain.mkdir()
            long_quote = " ".join(["word"] * 30)
            (build / "corpus" / "S001-talk.md").write_text(
                "Um, so, the thing is: discomfort is a sign of growth, not failure. " + long_quote)
            (brain / "frameworks.md").write_text(
                '"Discomfort is a sign of growth, not failure." [S001]\n'
                '"Made up line about introverts" [S001]\n'
                f'"{long_quote}" [S001]\n'
                '"Some quote" [S009]\n')
            statuses = [r.status for r in check_quotes.check_brain(brain, build)]
            self.assertEqual(statuses, ["ok", "missing", "too-long", "no-source"])


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["REWIRE_LEDGER"] = str(Path(self.tmp.name) / "reps.jsonl")

    def tearDown(self):
        os.environ.pop("REWIRE_LEDGER", None)
        self.tmp.cleanup()

    def run_cli(self, *argv, today=date(2026, 11, 1)):
        out = io.StringIO()
        with redirect_stdout(out):
            code = ledger.main(list(argv), today=today)
        return code, out.getvalue()

    def add(self, before, today, rtype="work-meeting"):
        self.run_cli("add", "--type", rtype, "--situation", "standup", "--layer", "State",
                     "--rep", "Say one idea early", "--before", str(before), today=today)

    def test_add_done_and_ids(self):
        self.add(7, date(2026, 11, 1))
        self.add(6, date(2026, 11, 2))
        code, out = self.run_cli("done", "R002", "--after", "3")
        self.assertEqual(code, 0)
        self.assertIn("6 -> 3", out)
        reps = ledger.current_reps(ledger.read_events(ledger.ledger_path()))
        self.assertEqual([r["status"] for r in reps.values()], ["open", "done"])

    def test_cannot_close_twice(self):
        self.add(5, date(2026, 11, 1))
        self.run_cli("done", "R001", "--after", "2")
        with self.assertRaises(SystemExit):
            self.run_cli("skip", "R001")

    def test_score_range_enforced(self):
        with self.assertRaises(SystemExit):
            self.add(11, date(2026, 11, 1))

    def test_trend_and_stale(self):
        for i, before in enumerate([8, 8, 5, 4]):
            self.add(before, date(2026, 10, 1 + i))
        self.add(6, date(2026, 10, 1), rtype="class")
        reps = list(ledger.current_reps(ledger.read_events(ledger.ledger_path())).values())
        s = ledger.stats(reps, date(2026, 11, 1))
        rows = {r["type"]: r for r in s["by_type"]}
        self.assertTrue(rows["work-meeting"]["trend"].startswith("easier"))
        self.assertEqual(rows["class"]["trend"], "need 4+ done reps")
        self.assertEqual(len(s["stale"]), 5)

    def test_events_are_append_only(self):
        self.add(7, date(2026, 11, 1))
        self.run_cli("done", "R001", "--after", "4")
        lines = ledger.ledger_path().read_text().splitlines()
        self.assertEqual([json.loads(l)["event"] for l in lines], ["add", "done"])


class FetchTests(unittest.TestCase):
    def test_html_to_text_drops_scripts_and_nav(self):
        title, text = fetch_sources.html_to_text(
            "<html><head><title>Essay</title><script>var x=1</script></head>"
            "<body><nav>Menu</nav><p>First idea.</p><p>Second idea.</p><footer>c</footer></body></html>")
        self.assertEqual(title, "Essay")
        self.assertEqual(text, "First idea.\nSecond idea.")

    def test_vtt_to_text_removes_timing_and_rolling_duplicates(self):
        vtt = ("WEBVTT\nKind: captions\n\n00:00:01.000 --> 00:00:02.000\nhello there\n\n"
               "00:00:02.000 --> 00:00:03.000\nhello there\n<c>general</c> idea\n")
        self.assertEqual(fetch_sources.vtt_to_text(vtt), "hello there general idea")

    def test_add_local_and_sources_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            note = root / "talk.md"
            note.write_text("word " * 600)
            build = root / "build"
            with redirect_stdout(io.StringIO()):
                fetch_sources.main([str(build), "--add", str(note), "--title", "My Talk", "--date", "2025-01-02"])
                fetch_sources.main([str(build), "--prefix", "E", "--add", str(note), "--title", "Review"])
                out = root / "sources.md"
                fetch_sources.main([str(build), "--sources-md", str(out), "--name", "Test Person"])
            manifest = json.loads((build / "sources.json").read_text())
            self.assertEqual([s["id"] for s in manifest["sources"]], ["S001", "E001"])
            self.assertTrue((build / "corpus" / "S001-my-talk.md").exists())
            self.assertIn("S001 | My Talk | local | 2025-01-02", out.read_text())


if __name__ == "__main__":
    unittest.main()
