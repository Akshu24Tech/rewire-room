# Brain spec (expert seats)

A brain is what a seat knows. It is read by an agent under a tight budget (the hot sheet every time, up to three other files per round), so it must be dense, organized for decisions, and honest about its limits.

Folder: `.claude/skills/rewire/brains/<slug>/`

| File | Budget | Holds |
|---|---|---|
| `_hot.md` | under 800 words | The seat in one page. Always read first. |
| `frameworks.md` | 1,500 to 3,000 words | Named models and tools, most central to the layer first |
| `principles.md` | 800 to 1,500 words | Rules of thumb the person repeats |
| `positions.md` | 1,000 to 2,000 words | Stances on specific questions, with dates, including changes of mind |
| `stories.md` | 500 to 1,200 words | The personal and historical stories they use as proof |
| `voice.md` | 300 to 600 words | How they talk: rhythm, phrases, habits, what they never say |
| `sources.md` | generated | Every source id with title, URL, date. Written by the fetcher. |

## Rules for every file

1. **Quotes are verbatim** and written `"exact words" [S014, 2024]`. Under 25 words each. Copy them from the verified notes, never from memory.
2. **Every claim has a source.** Paraphrase cites `(S014)` or `(S014, S031)`. A synthesis across sources cites `(inferred from S014, S031)`.
3. **Layer first.** Material on this seat's layer comes first and gets the most space. Material off the layer is kept only when the person ties it to the layer.
4. **No medical protocols.** Leave out supplements, compounds, medication, and dosing even when the person teaches them. Behavioral tools stay.
5. **Short quotes, mostly paraphrase.** A brain is notes about public work, not a copy of it. No passage longer than two quoted sentences from one source in a row.
6. **No em dashes.**
7. **Scope honestly.** If the person has said little about a topic, the brain says so instead of stretching.

## `_hot.md`

```markdown
# <Name> seat: hot sheet

**Layer:** <layer>. **Question this seat owns:** <question>

Built from <n> public sources, <years>. Simulated advisor, not the person.

## Worldview in three sentences
...each sentence cited.

## The rules they decide by (6 to 8)
1. **<Rule in plain words>.** "<verbatim quote>" [S014, 2024]

## The frameworks they reach for first (4 to 5)
1. **<Name>:** what it is, in one line (S0xx).

## How they read a moment on this layer
A short paragraph: what they look at first, what they ask, what they recommend first, in their order.

## Signature questions
- ... (S0xx)

## Voice cheat sheet
- 4 or 5 bullets from voice.md.

## Where this lens misfires
- 4 to 6 bullets: situations where this person's advice overreaches, contradicts better evidence, does not fit an introvert, or does not fit the user's context. Name which other seat covers the gap.
```

## `frameworks.md` entries

```markdown
## <n>. <Framework name>

- **What it is:** one or two lines.
- **Parts or steps:** ...
- **When to use it:** the kind of moment.
- **How to apply it to a debrief:** what it says about a moment that went wrong, and what rep it suggests.
- **Quote:** "<verbatim>" [S0xx, year]
- **Sources:** <count> (S0xx, S0xx, ...)
```

## `positions.md` entries

One heading per question the user might face ("Should introverts fake extroversion?", "Is it better to prepare or improvise?"). Each: the stance in one line, the reasoning, a quote, the sources and dates. If the stance changed over time, say from what to what and when.
