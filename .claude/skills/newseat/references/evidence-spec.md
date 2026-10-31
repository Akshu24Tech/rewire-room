# Evidence brain spec

The Evidence seat grades claims. Its brain is a map from claims to the research behind them, not a person's views.

Folder: `.claude/skills/rewire/brains/evidence/`

| File | Budget | Holds |
|---|---|---|
| `_hot.md` | under 800 words | The grading rules, the topics covered, and the strongest and weakest findings |
| `claims.md` | 2,000 to 5,000 words | One entry per claim the expert seats are likely to make, graded |
| `studies.md` | as needed | One entry per review or study, with what it found and its limits |
| `sources.md` | generated | Every evidence id with title, URL, date |

## Sources

Fetch with `python scripts/fetch_sources.py build/evidence --prefix E --list build/evidence/urls.txt`.

- Prefer, in order: meta-analyses and systematic reviews; large preregistered studies; replications; well-designed single studies.
- Open-access versions only (PubMed Central, preprint servers, author copies). Never paywalled text.
- Record failed replications and null results. They are as important as positive findings.

## Starting topics (Phase 1)

Cover what the debrief seats will lean on most:

1. Exposure and approach behavior for social fear in non-clinical adults.
2. Implementation intentions (if-then plans) and behavior change.
3. Arousal reappraisal ("this is excitement, not threat") before performance.
4. Breathing techniques and acute stress (including physiological sighing).
5. Volitional personality change (can people change traits on purpose, and how).
6. Introversion, extraverted behavior, and wellbeing (the costs and benefits of acting extraverted).
7. Memory reconsolidation and spaced practice in humans.
8. Attention, task switching, and mental fatigue.
9. The spotlight effect and the liking gap (overestimating how much others notice and judge us).

## `claims.md` entries

```markdown
## <Claim, worded the way a seat would say it>

- **Grade:** STRONG | MIXED | WEAK | UNSUPPORTED
- **What the research shows:** two or three lines, plain English (E0xx, E0xx).
- **Where it overreaches:** the common inflated version of the claim, and its grade.
- **Key line:** "<verbatim from a source, under 25 words>" [E0xx]
- **Sources:** E0xx, E0xx
```

## `studies.md` entries

```markdown
## E0xx: <short title> (<first author>, <year>)

- **Type:** meta-analysis | systematic review | RCT | replication | observational
- **Sample:** size and population.
- **Finding:** one or two lines, with effect size if reported.
- **Limits:** one line.
```

## Rules

- Grade from the sources only. If the sources do not settle a claim, say MIXED or leave it out.
- Separate what was found in the lab from what was found in everyday life.
- Never cite a study that is not in `sources.md`.
- No em dashes.
