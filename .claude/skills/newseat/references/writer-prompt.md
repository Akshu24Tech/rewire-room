# Writer prompt (reduce step)

Three writers, spawned together, `general-purpose`, default model. Each writes only its own files. Fill the brackets.

```
REWIRE ROOM SEAT BUILD: WRITER [A | B | C]

Repo root: [absolute path]
Person: [full name]
Seat layer: [layer]
The question this seat owns: [question]

Read:
- .claude/skills/newseat/references/brain-spec.md (the layout, budgets, and rules; follow them exactly)
- every file in build/<slug>/notes/ (verified notes from all sources)
- build/<slug>/corpus/ only when you need a quote's context

Write, into .claude/skills/rewire/brains/<slug>/:
- Writer A: frameworks.md and principles.md
- Writer B: positions.md and stories.md
- Writer C: voice.md

How to write:
1. Merge duplicates across batches. A framework that appears in twelve sources is one entry with a count of twelve.
2. Order by importance to the seat's layer, then by how often the person returns to it.
3. Copy quotes exactly as they appear in the notes, with the source id and year. Do not create new quotes, shorten them mid-sentence, or fix their grammar. If you need a different quote, copy it exactly from the corpus file and keep it under 25 words.
4. Everything else is paraphrase with source ids.
5. Stay within the budgets in the spec. Cut the least useful material, not the sources.
6. No supplements, compounds, medication, or dosing. No em dashes.

Reply with one line per file: name, word count, number of quotes.
```
