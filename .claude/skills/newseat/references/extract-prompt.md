# Extraction prompt (map step)

One agent per batch of about 50,000 words. `subagent_type: general-purpose`, `model: sonnet`. Fill the brackets.

```
REWIRE ROOM SEAT BUILD: EXTRACTION, BATCH [NN] OF [TOTAL]

Repo root: [absolute path]
Person: [full name]
Seat layer: [layer]
The question this seat owns: [question]

Read every file in this batch completely:
[S001: build/<slug>/corpus/S001-....md]
[S002: ...]

Write your notes to: build/<slug>/notes/batch-[NN].md

Pull out what this person teaches, with the most attention on the seat's layer. For each item, record the source id and, where the person says it well, ONE verbatim quote under 25 words copied character for character from the file, written as "exact words" [S0xx, year]. Never fix grammar inside a quote. Never quote anyone but this person.

Use exactly these sections:

## Frameworks
Named models, tools, or step-by-step methods. Name, what it is, the steps, when they use it, quote, source ids.

## Principles
Rules they repeat. Rule in plain words, quote, source ids.

## Positions
Their stance on specific questions (preparing vs improvising, faking it, introversion, feedback, discomfort, fear, routines). Stance, reasoning, quote, source id with date. Note any change of mind.

## Stories
Personal or historical stories they use as proof. Two or three lines each, what the story is used to prove, source id.

## Voice
How they talk: sentence rhythm, recurring phrases, how they open and close, how they handle disagreement. Five to ten observations, each with a short example quote and source id.

## Misfires
Places where their advice overreaches, contradicts itself, depends on their own unusual situation, or would not fit a quiet, introverted student or early-career professional. Source ids.

## Off-layer
One line per major topic they discuss that is outside this seat's layer, so the writers know it exists. No detail.

Rules:
- Leave out supplements, compounds, medication, and dosing entirely, even when the person teaches them.
- If a source is mostly another speaker, say so in one line at the top of your notes and extract only what this person says.
- Paraphrase everything that is not a quote. Mark syntheses "inferred from S0xx, S0xx".
- No em dashes.
- When done, reply with one line: the batch number, sources read, and counts per section.
```
