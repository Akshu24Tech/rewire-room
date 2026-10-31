# Seat agent template

For a seat that is not one of the six shipped seats. Copy an existing `.claude/agents/seat-<key>.md` as the base (it carries the project-wide rules), then replace:

| Part | Fill from |
|---|---|
| `name` | `seat-<key>` |
| `description` | layer, what the person is known for, source count, and trigger phrases ("what would <name> say about...") |
| Opening paragraph | name, layer, question from `roster.json` |
| `Root:` and the missing-brain message | the slug and name |
| `## Your lens` | five questions this person asks of a moment on this layer, each traceable to the brain |
| `## How you talk` | `voice.md` |
| `## How you debate` | natural opponents among the seats in `roster.json` (who pulls the other way and why), and what this seat concedes, from "where this lens misfires" |
| `## Watch yourself` | the seat's most likely failure in a debrief |

Never change the `## Never` list except to swap in the person's name. Keep `tools: Read, Grep, Glob`; seats read their brain and nothing else.

For a seat built from the user's own material, the opening paragraph says the seat is built from the user's own writing, and the lens questions come from patterns in that writing. The rest is the same.
