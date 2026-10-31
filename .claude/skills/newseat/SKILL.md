---
name: newseat
description: Use when the user wants to build or add an advisor seat for Rewire Room, says "/newseat", "build the Grant seat", "add [name] to the council", "make a seat for [name]", wants a seat built from their own journals or posts, or wants the Evidence seat built ("/newseat --evidence"). Finds and fetches the person's public work, extracts frameworks, principles, positions, stories, and voice with parallel sub-agents, writes the brain, verifies every quote against the raw sources, finalizes the seat agent, and marks the seat ready in the roster. Not for running a council (that is /rewire).
argument-hint: "[full name] [--quick | --deep] | --evidence | refresh <key>"
---

# Build a seat

A seat is three things. This skill makes or finishes all three:

1. **A brain**: `.claude/skills/rewire/brains/<slug>/`, compiled from public work, every quote verbatim with a source id.
2. **An agent**: `.claude/agents/seat-<key>.md`. The six expert seats ship with draft agents; this skill rewrites their lens from the finished brain.
3. **A roster entry**: `.claude/skills/rewire/roster.json`, with `"status": "ready"` once the brain passes the checker.

Raw sources go to `build/<slug>/`, which git ignores. Only the brain is committed.

Read before the first run: `references/brain-spec.md`, `references/extract-prompt.md`, `references/writer-prompt.md`. For the Evidence seat, read `references/evidence-spec.md` instead of `brain-spec.md`.

**This needs web access from the shell** (the fetcher downloads pages and YouTube captions). Run it in Claude Code on your own machine. If fetches fail across the board, the environment is blocking the web: say so and stop, rather than building a brain from memory.

## Who can be a seat

- Public figures with a real body of public work: books as they teach them in talks, long interviews where they are the main speaker, their own podcast or channel, essays, lectures.
- The user, or someone who consented, from material the user provides (`--add` in Step 3).
- Not: fictional characters, private people without consent, or anyone with too little material. Under about 15 usable sources or 60,000 words, say so and offer `--quick` with a warning, or a different person.

## Depth

| Flag | Sources | Words | Extraction agents |
|---|---|---|---|
| `--quick` | 12 to 20 | 80k+ | 2 to 3 |
| default | 30 to 50 | 250k+ | 4 to 6 |
| `--deep` | 80+ | 500k+ | 8 to 12, in waves of six |

One 90-minute interview is worth ten 6-minute clips. Prefer depth over count.

## Step 1: Which seat

1. If the person is in `roster.json`, use that entry (key, slug, layer, question) and skip to Step 2. If its status is already `ready`, offer a refresh (Step 3 on, the fetcher skips sources it already has).
2. For a new person, ask in one AskUserQuestion batch (best guess as the first option): the **layer and question** the seat owns (worded like the roster, one layer of change, not overlapping an existing seat without a sharper angle), and the **depth**. Then set `key` (lowercase surname), `slug` (first-last), `short`, and `dimension` (two or three words), add the entry with `"status": "brain-pending"`, and create the agent from `references/agent-template.md`.

## Step 2: Find sources

Use WebSearch to build a source list, best first:

- Long-form interviews and podcasts where the person does most of the talking, including their own show.
- Talks, lectures, and keynotes.
- Their own essays, newsletter, or articles.
- Books as they teach them in public: author talks, book interviews, chapters they posted free. Never fetch pirated or paywalled text.
- Recent material (last two years) so `positions.md` is current, plus a spread of years.

Bias toward material on this seat's layer. A Huberman seat for Rewire Room needs his episodes on stress, fear, focus, and social behavior more than his episodes on training or nutrition.

Skip clips under about 10 minutes, compilations, reaction videos, and anything where someone else does most of the talking. Write `build/<slug>/urls.txt`, one URL per line, `# heading` lines for groups. Aim for the depth target plus 20 percent.

## Step 3: Fetch

```bash
python scripts/fetch_sources.py build/<slug> --list build/<slug>/urls.txt
```

Each source lands in `build/<slug>/corpus/` and is logged in `sources.json`, with a status per URL: `ok`, `skip`, `thin`, `fail`. Replace thin and failed sources (another copy, a transcript page) and re-run until the manifest meets the depth target. For local material: `--add path --title "..." --date YYYY-MM-DD`.

Open two or three corpus files and confirm they are clean text by the right person. Auto-captions with a guest talking most of the time are not this person's corpus.

## Step 4: Extract (map)

Split the sources into batches of about 50,000 words. Spawn one extraction agent per batch, in **one message**, in parallel, foreground: `subagent_type: general-purpose`, `model: sonnet`, with the prompt from `references/extract-prompt.md`. At most six at a time.

Each agent writes `build/<slug>/notes/batch-NN.md`. When all are back, check every note quote against the corpus. Notes are not a brain, so point the checker at the notes folder:

```bash
python scripts/check_quotes.py brain build/<slug>/notes --corpus build/<slug>
```

Fix what it reports: correct a wrong id, delete a quote it cannot find. Notes without a verified quote can stay as paraphrase marked "inferred from S0xx". Too-long quotes get trimmed to the strongest part.

## Step 5: Write the brain (reduce)

Create the brain folder and its `sources.md`:

```bash
python scripts/fetch_sources.py build/<slug> --sources-md .claude/skills/rewire/brains/<slug>/sources.md --name "Full Name"
```

Spawn three writer agents in one message (`general-purpose`, default model) with the prompt from `references/writer-prompt.md`:

- Writer A: `frameworks.md` and `principles.md`.
- Writer B: `positions.md` and `stories.md`.
- Writer C: `voice.md`.

When they are back, write `_hot.md` yourself from the five finished files, per the spec, including "where this lens misfires". Then:

```bash
python scripts/check_quotes.py brain .claude/skills/rewire/brains/<slug> --corpus build/<slug>
```

Fix until it passes with zero failures. Read `_hot.md` once more as the agent will: under 800 words, and it should tell you how this person thinks about this seat's layer, in their words.

## Step 6: Finish the agent

Rewrite the `## Your lens` section of `.claude/agents/seat-<key>.md` from the brain: five questions this person asks of any moment on this layer, each traceable to a framework or principle. Remove the draft comment. Update "How you talk" from `voice.md`, and "How you debate" and "Watch yourself" from "where this lens misfires". Keep the "Never" list as it is; it carries project-wide rules.

## Step 7: Mark ready and test

1. Set the seat's `"status"` to `"ready"` in `roster.json`.
2. Run a single-seat consult on a sample moment ("I went quiet in a group project meeting when someone talked over me") using the consult prompt from `.claude/skills/rewire/references/round-prompts.md`, with `general-purpose` and the fallback line (a new agent file only registers in a new session).
3. Save the answer to `sessions/test-<key>.md` under a `## <Short>` heading and run `python scripts/check_quotes.py session sessions` on it, or check its quotes against the brain by hand. Fix the brain or the agent if the seat invents quotes, gives medical advice, or frames introversion as a defect.

## Step 8: Report

Tell the user, in under 120 words: sources and words used, the date span, checker result, the five lens questions in one line each, the known misfires, and that a new Claude Code session will load the seat as its own agent. Suggest committing the brain, the agent, and `roster.json` (never `build/`).

## The Evidence seat (`--evidence`)

Follow `references/evidence-spec.md`. Same pipeline, three differences: sources are research reviews, meta-analyses, and key studies (open-access versions only); the fetcher runs with `--prefix E`; and the brain is `claims.md` plus `studies.md` instead of the persona files.
