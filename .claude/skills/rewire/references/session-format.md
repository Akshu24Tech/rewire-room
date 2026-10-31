# Session format

Every debrief writes a folder `sessions/YYYY-MM-DD-<slug>/` (slug: three to five words from the moment, lowercase, hyphens). These files are personal data and stay on the user's machine (`sessions/` is ignored by git).

| File | Written by | When |
|---|---|---|
| `brief.md` | Chair | Step 3 |
| `round-1.md` | Chair (cards verbatim) | Step 4 |
| `round-2.md` | Chair (cards verbatim) | Step 5 |
| `evidence.md` | Chair (audit verbatim) | Step 5, if the Evidence seat sat |
| `debrief.md` | Chair | Step 6 |

## brief.md

```markdown
# Brief: <one-line moment>

Date: YYYY-MM-DD · Type: <situation type> · Mode: debrief

## The moment
...
## What I wanted
...
## What I did
...
## Discomfort
Before n/10 · During n/10 · After n/10
## Context
...
## Next similar moment
...
## History
<earlier reps of this type from the ledger, or "None yet">

## Council
| Seat | Layer | Weight | Why |
|---|---|---|---|
```

## Round files

One `## <Short>` heading per card, using the seat's `short` name from `roster.json` exactly (the quote checker uses it to find the seat's brain). Cards are pasted verbatim under their heading. The Chair's section is `## Chair notes`, always last.

## Quotes

A verbatim line from a brain is written `"exact words" [S014]` (persona seats) or `"exact words" [E012]` (Evidence seat). Straight or curly quotes both work. The checker verifies every such quote under a seat heading against that seat's brain, and every such quote in `debrief.md` against all brains. Anything else in quotation marks is not treated as a source quote, so never put an expert's supposed words in quotes without a source id.
