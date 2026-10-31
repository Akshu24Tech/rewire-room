# Debrief template

Write `debrief.md` in exactly this shape. Plain English, short sentences, no em dashes. Quote a seat only verbatim from its card; quote an expert only with a checked source id.

```markdown
# Debrief: <one-line moment>

YYYY-MM-DD · Seats: <Short names> · Evidence: checked | not checked · Confidence: high | medium | low

## The layer that broke: <layer> (<seat>)

<Two or three sentences: what happened on this layer, in the user's own situation, and why the council put it first.>

Layer scores: <dimension n · dimension n · ...>

## Your rep

**<The rep, one sentence.>**

If-then: When <cue>, I will <rep>.

Why this rep: <one or two sentences, with the seat and the framework or source id behind it>. <Evidence label if WEAK or not checked.>

## What the council saw

- **<Seat>**: <their diagnosis in one line, faithful to the card>. (<framework, source id>)
- ...

## Where they disagreed

<The main crux in two or three lines: who said what, who moved, how it resolved.>

**Minority view** (<seat>): <one line>. For this to be right: <the condition>.

## Evidence notes

<Each claim graded WEAK, UNSUPPORTED, or NOT IN BRAIN that touched the advice, in one line each, or "No weak claims behind the rep.">

## After the moment

Rate your discomfort before and after (0 to 10) and tell Claude how it went:
`python scripts/ledger.py done <id> --after <n> --note "..."`

---
Seats are simulations built from each expert's public work. They are not the people and do not speak for them. This is not therapy or medical advice.
```

## The chat version (under 180 words)

```
**Layer that broke:** <layer>. <one line why>
**Your rep:** <rep>
**If-then:** When <cue>, I will <rep>.
<Evidence warning, if any, in one line.>
**Worth knowing:** <the disagreement or minority view in one line>
Full debrief: sessions/<folder>/debrief.md · Logged as rep <id>.
Tell me how it went after your next <situation> so I can log it.
```
