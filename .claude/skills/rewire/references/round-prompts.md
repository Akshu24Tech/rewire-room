# Round prompts

Paste these into each seat's Agent call and fill the brackets. Give the absolute repo root once at the top; every other path is relative to it. Seats read the brief and earlier rounds from the session folder, so cards stay verbatim without being pasted into prompts.

Agent type: `seat-<key>`. If that type is not registered in this session (agent files load at session start), use `general-purpose` and put this line first: `Read .claude/agents/seat-<key>.md and follow it as your instructions for this whole task. Only read files; do not write anything.`

**Quote format.** Verbatim lines from a brain are written as `"exact words" [S014]`. A framework or idea used without quoting is cited as `(Framework name, S014)`. The quote checker reads the first form only.

---

## Round 1: diagnosis

```
REWIRE ROOM, ROUND 1 OF 2: DIAGNOSIS

Repo root: [absolute path]. You hold the [SHORT] seat ([layer]). Read your brain's _hot.md, then at most three more brain files that fit this moment.

Read the brief: [session folder]/brief.md
Your weight on this moment: [w]/3 ([one-line reason]).

Answer in your seat's voice, first person, plain text, under 300 words, in exactly this shape:

SEAT: [SHORT] ([layer])
LAYER SCORE: n/5   (how well your layer held up in this moment, using the anchors below)
PRIMARY LAYER: mine | [another seat's layer]   (where you think the most leverage is)
CONFIDENCE: low | medium | high

WHAT BROKE: one sentence, on your layer.
WHY:
1. reason, naming the framework or principle and its source id
2. ...
THE REP: one action for the next similar moment. Observable, under ten minutes, possible this week.
IF-THEN: When [cue in the moment], I will [the rep].
CLAIMS: each factual claim about the brain, body, or behavior your reasons rely on, one per line, plainly worded. "None" if your reasons are only frameworks and judgment.
QUESTION FOR YOU: the one thing you would ask the user.

LAYER SCORE anchors:
1 = this layer clearly caused the freeze or the miss
2 = it made things noticeably worse
3 = neutral, or helped and hurt equally
4 = it mostly held and helped
5 = it was a clear strength in this moment

Rules: argue from your layer first, at full strength; the Chair balances the council, not you. Introversion is not the problem; never frame the user's temperament as a defect. No supplements, medication, doses, or diagnoses. Quote only lines that appear word for word in your brain, as "exact words" [Sxxx].
```

---

## Round 2: cross-exam

```
REWIRE ROOM, ROUND 2 OF 2: CROSS-EXAM

Repo root: [absolute path]. You hold the [SHORT] seat. Read your _hot.md again and at most two more brain files if you need them to answer the others.

Read: [session folder]/brief.md and [session folder]/round-1.md (every card and the Chair notes).

THE CRUXES THE CHAIR SEES
1. [crux]: [seats on each side]. [If this seat is on one side, the argument it must answer.]
2. ...

Answer in your seat's voice, under 250 words, in exactly this shape:

SEAT: [SHORT]
I DISAGREE MOST WITH: [seat]. Their point in one line, then your rebuttal from your frameworks.
I CONCEDE: the strongest point against you and what it changes. "Nothing" only if you can say why it fails.
ON THE CRUXES: one or two lines each.
PRIMARY LAYER: mine | [another seat's layer]
LAYER SCORE: n/5
MOVED: no | yes, from X to Y, because ...
BEST REP ON THE TABLE: yours or another seat's, in one line, and why it beats the rest.

Rules: engage the strongest version of the other cards. Move only for a better argument, never to be agreeable. If everyone agrees with you, attack the weakest part of your own case.
```

---

## Evidence audit (runs alongside Round 2)

```
REWIRE ROOM, EVIDENCE AUDIT

Repo root: [absolute path]. You hold the Evidence seat. Read your brain's _hot.md and claims.md, then any studies.md entries you need.

Read: [session folder]/brief.md and [session folder]/round-1.md.

THE CLAIMS
C1 ([seat]): [claim]
C2 ([seat]): [claim]
...

For each claim, one line, in exactly this shape:

C1: STRONG | MIXED | WEAK | UNSUPPORTED | NOT IN BRAIN. One-sentence reason. [E012, E031]

Then:
REPS AT RISK: any proposed rep whose whole rationale rests on a claim graded WEAK or UNSUPPORTED, by seat.
SAFER FRAMING: for each rep at risk, how to keep the rep while dropping the weak mechanism, in one line.

Rules: grade only from your brain. A claim your brain does not cover is NOT IN BRAIN, never a guess. Cite evidence ids for every graded claim. You do not argue for or against any rep beyond this audit.
```

---

## Single-seat consult

```
REWIRE ROOM, SINGLE-SEAT CONSULT

Repo root: [absolute path]. You hold the [SHORT] seat. Read your brain's _hot.md, then at most four more brain files that fit the question.

THE QUESTION
[question, plus any context]

Answer in your seat's voice, first person, under 400 words: your view, the reasoning with named frameworks and source ids, one rep the user could do this week, and the question you would ask back. Do not narrate your expert in the third person. Same rules as the council: no medical advice, temperament is not a defect, verbatim quotes only. End with "Sources:" and the source ids you used.
```
