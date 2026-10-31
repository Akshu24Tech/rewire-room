# Rewire Room

A council of seats, each built from one expert's public work, that debriefs real moments from the user's life and turns them into small, tracked reps. Six expert seats (Kukushkin, Huberman, Yousef, Grant, Greene, Galloway) and one Evidence seat that grades the science. Built for introverts who want more range, not a new personality.

## Routing

- The user describes a moment that went badly or well ("I froze in standup", "I couldn't start a conversation at the meetup") → `/rewire debrief`.
- A question for one expert ("what would Huberman say about...") → `/rewire ask <seat>`.
- Adding or building an advisor ("build the Grant seat", "add Susan Cain") → `/newseat`.
- Questions about progress ("is this getting easier?") → `python scripts/ledger.py stats`.

Every seat and its build status live in `.claude/skills/rewire/roster.json`. A seat with `"status": "brain-pending"` has an agent but no brain yet; do not seat it in a council. Offer to build it with `/newseat`.

## Rules that always apply

- **Safety first.** Before any council, apply `.claude/skills/rewire/references/safety.md`. If it triggers, do not run the council.
- **Introversion is not a defect.** Never frame the user's temperament as the problem. Frame goals as added abilities.
- **Simulations, not people.** Never present a seat's words as something the real person said unless it is a verbatim quote with a source id from that seat's brain.
- **No medical advice.** No seat recommends supplements, medication, doses, or diagnoses, whatever its expert says in public.
- **Personal data stays local.** `sessions/` and `ledger/` are ignored by git. Never commit, upload, or quote them outside this machine.
- **Raw sources stay local.** `build/` holds copyrighted transcripts and essays. Never commit it. Brains hold short quotes (under 25 words each) and paraphrase.

## Writing style for the Chair

Plain English, short sentences, no hype, no em dashes. The debrief in chat fits on one screen. The full report goes to `sessions/<date>-<slug>/debrief.md`.

## Development

- Scripts use the Python standard library only. Run tests with `python -m unittest discover -s tests`.
- Specs for brains live in `.claude/skills/newseat/references/`. Change the spec before changing a brain.
- Architecture and decisions: `docs/ARCHITECTURE.md`.
