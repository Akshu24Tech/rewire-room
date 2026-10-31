# Example sessions

These are worked examples, not real sessions. Your own sessions are written to
`sessions/` and stay on your machine (git ignores everything here except this
`examples/` folder).

## 2026-10-31-example-froze-in-standup

A full debrief, start to finish, on a common introvert moment: having an idea in
a meeting and waiting too long to say it. It shows every part of the loop:

| File | What it shows |
|---|---|
| `brief.md` | The moment, the discomfort scores, and the three seats picked for it |
| `round-1.md` | Each seat's diagnosis from its own layer, plus the Chair's cruxes and the claims list |
| `round-2.md` | The seats cross-examining and converging on a sequence (steady the body, then speak) |
| `evidence.md` | The Evidence seat grading the science behind the advice |
| `debrief.md` | The one rep, the if-then plan, and the evidence caveat |
| `example-reps.jsonl` | The rep logged to a ledger, then marked done at a lower discomfort |

Two things in this example are worth seeing:

1. **The Evidence seat earns its seat.** It graded the headline mechanisms
   (a single sigh resetting arousal, one rough sentence rewriting a memory) as
   *weak* or *not covered* by its research corpus. The rep survives as a cheap
   experiment, but the tidy brain-science story behind it does not. The council
   checks itself.
2. **The quote checker caught a real error.** In Round 2 the Kukushkin seat
   conceded a point by quoting a Huberman source. `check_quotes.py` flagged it as
   not being in the Kukushkin brain, and the Chair de-quoted it. See the note at
   the bottom of `round-2.md`.

Run `python scripts/check_quotes.py session sessions/examples/2026-10-31-example-froze-in-standup`
to see the check pass (12 quotes, all verbatim).
