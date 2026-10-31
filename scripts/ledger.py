#!/usr/bin/env python3
"""The rep ledger: what you practiced, and whether it is getting easier.

Every debrief logs one rep. After the real moment, you mark it done with your
discomfort afterwards. Stats show, per situation type, whether discomfort is
dropping over time and which reps you keep skipping.

  python scripts/ledger.py add --type work-meeting --situation "Froze in standup" \\
      --layer "Nervous system and state" --rep "Say one idea in the first five minutes" --before 7
  python scripts/ledger.py done R003 --after 4 --note "Said it, voice shook, nobody cared"
  python scripts/ledger.py skip R004 --note "Meeting got cancelled"
  python scripts/ledger.py list [--type work-meeting] [--open]
  python scripts/ledger.py stats

The ledger is a JSON Lines file at ledger/reps.jsonl (ignored by git). One line
per event, never rewritten, so the history is an audit trail. A rep's current
state is its latest event.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import mean

REPO = Path(__file__).resolve().parent.parent
DEFAULT_LEDGER = REPO / "ledger" / "reps.jsonl"
STALE_DAYS = 14
TYPES = ["class", "work-meeting", "interview", "presentation", "one-on-one",
         "social-group", "new-people", "online", "conflict", "other"]


def ledger_path() -> Path:
    return Path(os.environ.get("REWIRE_LEDGER", DEFAULT_LEDGER))


def read_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    events = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{n}: not valid JSON ({exc.msg}). Fix or remove that line.")
    return events


def append_event(path: Path, event: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def current_reps(events: list[dict]) -> dict[str, dict]:
    """Fold events into the current state of each rep, in creation order."""
    reps: dict[str, dict] = {}
    for ev in events:
        rid = ev["id"]
        if ev["event"] == "add":
            reps[rid] = {**ev, "status": "open"}
        elif rid in reps:
            if ev["event"] == "done":
                reps[rid].update(status="done", after=ev["after"], done_on=ev["date"], note=ev.get("note", ""))
            elif ev["event"] == "skip":
                reps[rid].update(status="skipped", done_on=ev["date"], note=ev.get("note", ""))
    return reps


def next_id(reps: dict[str, dict]) -> str:
    nums = [int(r[1:]) for r in reps if r[1:].isdigit()]
    return f"R{(max(nums) + 1) if nums else 1:03d}"


def score(value: int) -> int:
    if not 0 <= value <= 10:
        raise SystemExit("Discomfort is a number from 0 to 10.")
    return value


def cmd_add(args, path: Path, today: date) -> int:
    reps = current_reps(read_events(path))
    rid = next_id(reps)
    event = {
        "event": "add", "id": rid, "date": today.isoformat(), "type": args.type,
        "situation": args.situation, "layer": args.layer, "rep": args.rep,
        "before": score(args.before), "session": args.session or "",
    }
    append_event(path, event)
    print(f"Logged {rid}: {args.rep}")
    return 0


def cmd_close(args, path: Path, today: date, kind: str) -> int:
    reps = current_reps(read_events(path))
    rep = reps.get(args.id)
    if rep is None:
        raise SystemExit(f"No rep {args.id}. Run `ledger.py list` to see ids.")
    if rep["status"] != "open":
        raise SystemExit(f"{args.id} is already {rep['status']}.")
    event = {"event": kind, "id": args.id, "date": today.isoformat(), "note": args.note or ""}
    if kind == "done":
        event["after"] = score(args.after)
    append_event(path, event)
    if kind == "done":
        print(f"{args.id} done. Discomfort {rep['before']} -> {event['after']}.")
    else:
        print(f"{args.id} skipped.")
    return 0


def cmd_list(args, path: Path, today: date) -> int:
    reps = current_reps(read_events(path)).values()
    if args.type:
        reps = [r for r in reps if r["type"] == args.type]
    if args.open:
        reps = [r for r in reps if r["status"] == "open"]
    reps = list(reps)
    if not reps:
        print("No reps yet." if not args.type and not args.open else "No matching reps.")
        return 0
    for r in reps:
        after = f" -> {r['after']}" if r["status"] == "done" else ""
        print(f"{r['id']}  {r['date']}  {r['type']:<13} {r['status']:<8} {r['before']}{after:<5}  {r['rep']}")
    return 0


def trend(values: list[int]) -> str:
    """Compare the first half of a series with the second half."""
    if len(values) < 4:
        return "need 4+ done reps"
    half = len(values) // 2
    first, last = mean(values[:half]), mean(values[-half:])
    delta = last - first
    if delta <= -1:
        return f"easier ({first:.1f} -> {last:.1f})"
    if delta >= 1:
        return f"harder ({first:.1f} -> {last:.1f})"
    return f"flat ({first:.1f} -> {last:.1f})"


def stats(reps: list[dict], today: date) -> dict:
    by_type: dict[str, list[dict]] = {}
    for r in reps:
        by_type.setdefault(r["type"], []).append(r)
    rows = []
    for rtype, items in sorted(by_type.items()):
        done = [r for r in items if r["status"] == "done"]
        rows.append({
            "type": rtype,
            "reps": len(items),
            "done": len(done),
            "skipped": sum(r["status"] == "skipped" for r in items),
            "avg_before": round(mean(r["before"] for r in items), 1),
            "avg_after": round(mean(r["after"] for r in done), 1) if done else None,
            # The before score of each rep, in order: how hard the moment felt going in.
            "trend": trend([r["before"] for r in sorted(items, key=lambda r: (r["date"], r["id"]))]),
        })
    cutoff = today - timedelta(days=STALE_DAYS)
    stale = [r for r in reps if r["status"] == "open"
             and datetime.strptime(r["date"], "%Y-%m-%d").date() <= cutoff]
    done_all = [r for r in reps if r["status"] == "done"]
    return {
        "total": len(reps),
        "done": len(done_all),
        "completion": round(len(done_all) / len(reps), 2) if reps else 0.0,
        "avg_drop_in_moment": round(mean(r["before"] - r["after"] for r in done_all), 1) if done_all else None,
        "by_type": rows,
        "stale": [{"id": r["id"], "date": r["date"], "rep": r["rep"]} for r in stale],
    }


def cmd_stats(args, path: Path, today: date) -> int:
    reps = list(current_reps(read_events(path)).values())
    if not reps:
        print("No reps yet. Run a debrief first.")
        return 0
    s = stats(reps, today)
    if args.json:
        print(json.dumps(s, indent=2))
        return 0
    print(f"{s['total']} reps, {s['done']} done ({s['completion']:.0%}).")
    if s["avg_drop_in_moment"] is not None:
        print(f"Average drop in discomfort from before to after a done rep: {s['avg_drop_in_moment']}")
    print()
    print(f"{'type':<14}{'reps':>5}{'done':>6}{'skip':>6}{'before':>8}{'after':>7}  trend (before scores over time)")
    for row in s["by_type"]:
        after = "-" if row["avg_after"] is None else row["avg_after"]
        print(f"{row['type']:<14}{row['reps']:>5}{row['done']:>6}{row['skipped']:>6}"
              f"{row['avg_before']:>8}{after:>7}  {row['trend']}")
    if s["stale"]:
        print(f"\nOpen for {STALE_DAYS}+ days (do it, or skip it with a note):")
        for r in s["stale"]:
            print(f"  {r['id']}  {r['date']}  {r['rep']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="log a new rep from a debrief")
    a.add_argument("--type", required=True, choices=TYPES)
    a.add_argument("--situation", required=True)
    a.add_argument("--layer", required=True)
    a.add_argument("--rep", required=True)
    a.add_argument("--before", type=int, required=True, help="discomfort in the original moment, 0 to 10")
    a.add_argument("--session", help="session folder the rep came from")

    d = sub.add_parser("done", help="mark a rep done after the real moment")
    d.add_argument("id")
    d.add_argument("--after", type=int, required=True, help="discomfort doing the rep, 0 to 10")
    d.add_argument("--note")

    k = sub.add_parser("skip", help="close a rep you will not do, with a reason")
    k.add_argument("id")
    k.add_argument("--note")

    ls = sub.add_parser("list", help="list reps")
    ls.add_argument("--type", choices=TYPES)
    ls.add_argument("--open", action="store_true", help="only reps not yet done or skipped")

    st = sub.add_parser("stats", help="progress per situation type")
    st.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None, today: date | None = None) -> int:
    args = build_parser().parse_args(argv)
    today = today or date.today()
    path = ledger_path()
    if args.cmd == "add":
        return cmd_add(args, path, today)
    if args.cmd in ("done", "skip"):
        return cmd_close(args, path, today, args.cmd)
    if args.cmd == "list":
        return cmd_list(args, path, today)
    return cmd_stats(args, path, today)


if __name__ == "__main__":
    sys.exit(main())
