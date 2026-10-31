# Rewire Room

**Turn podcast insight into personality change.**

You watched the Huberman episode. You read Adam Grant. You nodded along to Robert Greene. Then Monday came, you sat quietly in the meeting again, and nothing changed.

Insight does not rewire a brain. Repetition does. Rewire Room is a council of advisors, each built from one expert's public work, that looks at a real moment from your life, works out which layer broke (your story about yourself, your nervous system, your energy, your growth habits, how you read people, or what is at stake), and hands you one small rep to do next time. Then it tracks whether that moment is actually getting easier.

Built for introverts who want more range, not a new personality. Introversion is not the problem being fixed. The goal is to add abilities (speaking up, starting conversations, holding a room) while keeping your temperament.

> **Status: Phase 1 in progress.** The council protocol, seat agents, verification scripts, and brain builder are in place. Seat brains are built with `/newseat` on a machine with web access (see [Build a seat](#build-a-seat)). See [docs/ROADMAP.md](docs/ROADMAP.md).

## The council

Every seat owns one layer of how people change.

| Layer | Seat | The question they own |
|---|---|---|
| Identity and memory | Nikolay Kukushkin | What story about yourself is your brain rehearsing, and how do new experiences rewrite it? |
| Nervous system and state | Andrew Huberman | Is your body in a state where you can perform, and how do you get there before the moment? |
| Attention and energy | Sahar Yousef | Where is your mental and social energy going, and are you budgeting it? |
| Growth and rethinking | Adam Grant | What evidence would change how you see yourself, and are you stretching or hiding? |
| Human nature and mastery | Robert Greene | What do others actually see, and what does your long apprenticeship look like? |
| Real-world stakes | Scott Galloway | What does this do for your career and relationships ten years from now? |
| Research check | The Evidence seat | Does research back this advice, and how strongly? |

The six expert seats are simulations built from public work: talks, podcasts, essays, and books as their authors teach them in public. They are not the people, do not speak for them, and none of them is affiliated with or endorses this project.

The Evidence seat is not a persona. It is built from research reviews and meta-analyses, and its only job is to grade the other seats' claims. When a confident podcast claim has weak evidence behind it, the council says so.

## How it works

```
/rewire debrief  I froze when my team lead asked for ideas in standup.
                 I had one but waited too long, and someone else said it.
```

1. **Safety screen.** If what you describe sounds like more than everyday discomfort, the council does not run. It points you to real support instead.
2. **The brief.** The Chair asks only for what is missing: what happened, what you wanted, what you did, and how uncomfortable it felt (0 to 10).
3. **Round 1, diagnosis.** Three or four seats, picked for this moment, each read the brief through their own layer and propose one rep.
4. **Round 2, cross-examination.** Seats answer each other. The Evidence seat grades every factual claim from Round 1 (strong, mixed, weak, unsupported).
5. **The debrief.** The Chair names the one layer with the most leverage, the single rep for next time, an if-then plan, and what the council disagreed on. The rep goes into your ledger.

A debrief costs about 9 sub-agent runs, not the 21 a full business council takes.

## Modes

| Mode | What it does | Phase |
|---|---|---|
| `debrief` | After a real moment: diagnose the layer that broke, get one rep | 1 |
| `ask <seat>` | One question to one seat | 1 |
| `reps` | A weekly challenge ladder, easiest to hardest | 2 |
| `check-in` | Review the ledger: what is getting easier, what you keep dodging | 2 |
| `prep` | Before a hard moment: state, energy, framing, and one intention | 3 |
| `decide` | A personal decision argued over three rounds | 3 |

## Why you can trust it

Most AI coaches are one agreeable voice that forgets you. Rewire Room checks itself at three levels:

1. **Quotes.** A seat may quote its expert only with a line that appears word for word in its brain, tagged with a source id. `scripts/check_quotes.py` verifies every quote in a session against the brains, and every quote in a brain against the raw sources it was built from.
2. **Claims.** The Evidence seat grades the science behind each piece of advice. Weakly supported advice is labeled, not hidden.
3. **Change.** Every rep is logged with discomfort before and after. `scripts/ledger.py stats` shows whether the same kind of moment is getting easier over weeks. That is the only number that matters.

## Setup

You need [Claude Code](https://claude.com/claude-code) and Python 3.10 or newer. Nothing else for running councils.

```bash
git clone https://github.com/Akshu24Tech/rewire-room.git
cd rewire-room
claude
```

Then type `/rewire debrief` and describe a moment.

## Build a seat

Each seat needs a brain: a folder of markdown files compiled from that person's public work, with every quote traced to a source. Seats ship without brains until they are built.

```
/newseat Adam Grant
```

The builder finds sources, fetches transcripts and essays into `build/` (ignored by git), extracts frameworks, principles, positions, stories, and voice with parallel sub-agents, writes the brain, and runs the quote checker until it passes. It needs web access, so run it in Claude Code on your own machine. Optional but recommended: [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube transcripts.

You can also build a seat for someone not on the list, or for yourself from your own journals and posts.

## Repo layout

| Path | What |
|---|---|
| `.claude/skills/rewire/` | The council: Chair protocol, round prompts, scoring, safety rules, roster, and one brain per seat |
| `.claude/skills/newseat/` | The seat builder and the brain specs |
| `.claude/agents/` | One sub-agent per seat (`seat-<key>.md`) |
| `scripts/` | Quote checker, ledger, and source fetcher (Python standard library only) |
| `tests/` | Tests for the scripts (run in CI on every push) |
| `docs/` | Vision, architecture, roadmap |
| `sessions/` | Your debriefs (ignored by git) |
| `ledger/` | Your reps (ignored by git) |

## Not therapy

Rewire Room is for everyday growth: speaking up, meeting people, building presence. It is not a treatment for social anxiety, depression, or anything else, and it is not a substitute for a professional. If a moment you want to debrief involves panic, persistent dread, or thoughts of harming yourself, please talk to a professional or a local helpline. In India, Tele-MANAS is free at 14416.

## Credits

The council pattern (seats built from public work, a neutral Chair, verified quotes) was inspired by [Roast Room](https://github.com/nateherkai/roast-room) by AI Automation Society, which runs it for business decisions. Rewire Room is a separate implementation for personal growth, with its own protocol, evidence layer, and progress ledger.

MIT licensed. See [LICENSE](LICENSE).
