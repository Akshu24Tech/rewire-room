# Architecture

Rewire Room runs inside Claude Code. There is no server and no database. The council is a skill (markdown instructions) that spawns sub-agents, and every artifact is a plain file you can read, diff, and verify.

## Components

```
                ┌────────────────────────────────────────────┐
  user  ──────► │  Chair  (.claude/skills/rewire-room)       │
                │  safety screen → brief → rounds → debrief  │
                └──────┬──────────────────────────┬──────────┘
                       │ spawns in parallel       │ writes
                       ▼                          ▼
        ┌─────────────────────────┐     sessions/<date>-<slug>/
        │ Seat agents             │       brief.md
        │ .claude/agents/seat-*.md│       round-1.md, round-2.md
        │   reads its own brain ──┼──►    evidence.md
        └─────────────────────────┘       debrief.md
                       │                          │
                       ▼                          ▼
        brains/<slug>/  (markdown,         ledger/reps.jsonl
        every quote with a source id)      (scripts/ledger.py)
                       ▲
                       │ built by
        /newseat  →  build/<slug>/ (raw sources, git-ignored)
```

| Component | Path | Role |
|---|---|---|
| Chair skill | `.claude/skills/rewire-room/SKILL.md` | Runs the protocol. Never argues a side. |
| Roster | `.claude/skills/rewire-room/roster.json` | Every seat, its layer, question, and build status |
| Seat agents | `.claude/agents/seat-<key>.md` | One sub-agent per seat; reads only its own brain |
| Brains | `.claude/skills/rewire-room/brains/<slug>/` | What a seat knows, compiled from public work |
| Seat builder | `.claude/skills/newseat/` | Finds sources, extracts, writes and verifies a brain |
| Quote checker | `scripts/check_quotes.py` | Session quotes against brains; brain quotes against raw sources |
| Ledger | `scripts/ledger.py`, `ledger/reps.jsonl` | Reps, discomfort before and after, trends |
| Fetcher | `scripts/fetch_sources.py` | URLs and local files into a clean text corpus |

## The debrief protocol

| Step | Who | Output |
|---|---|---|
| 0. Safety screen | Chair | Stop and refer, or continue |
| 1. Brief | Chair, with the user | `brief.md` |
| 2. Pick seats | Chair (user confirms) | 3 or 4 expert seats plus Evidence |
| 3. Round 1, diagnosis | Expert seats, in parallel | `round-1.md` (one card per seat) |
| 4. Round 2, cross-exam | Expert seats in parallel, Evidence seat alongside | `round-2.md`, `evidence.md` |
| 5. Debrief | Chair | `debrief.md`, one ledger entry |
| 6. Verify | `check_quotes.py` | Unverified quotes removed |

Cost: 4 expert seats × 2 rounds + 1 Evidence run = 9 sub-agent runs.

## Design decisions

**Two rounds, not three.** Roast Room runs three rounds because business decisions are expensive and one-way. A debrief produces a small, reversible rep you test within a week. The ledger is the third round: reality votes.

**Anchored 1 to 5 scores, not 0 to 10.** LLM scores on a 0 to 10 scale look precise and are not; councils converge on the same number. Each layer is scored on a 1 to 5 scale where every level has a written anchor (see `references/scoring.md`), so a score means something specific and two seats can disagree about which anchor fits.

**The Evidence seat audits; it does not debate.** If it argued like the others, it would become one more opinion. Instead it grades every factual claim the expert seats rely on, and the Chair down-ranks reps that rest on weak claims. Seats must list the claims they rely on in a `CLAIMS` field so the audit has a target.

**Seats read only their own brain.** A seat never browses the web or reads other brains. What it knows is fixed, inspectable, and verifiable. Context from other seats arrives only through the round files.

**Personal data never leaves the machine.** Sessions and the ledger are ignored by git. Brains, which hold short quotes and paraphrase of public work, are the only seat data committed. Raw sources stay in `build/`.

**Standard library only.** The scripts run anywhere Python 3.10 runs, with no install step. `yt-dlp` and `pdftotext` are optional speedups for the fetcher.

**Markdown over code for the protocol.** The Chair's protocol is a skill, not a Python orchestrator, so anyone can read and change how the council works without touching code. Deterministic jobs (quote checking, ledger math) are code, because those must give the same answer every time.
