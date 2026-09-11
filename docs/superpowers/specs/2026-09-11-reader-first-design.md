# The reader comes first — design

2026-09-11. Approved in conversation before implementation.

## The ask

The primary effect of a retelling must be prose that a human reader takes for
the voice's author. Meeting a countable rule is a means to that, never the
point.

## Evidence

Read in full: `voices/earnest.md`, `voices/_template.md`,
`.claude/commands/retell.md`, `.claude/rules/prose.md`, `README.md`,
`scripts/check.py`, `.claude/settings.json`, `.claude/hooks/guard-write.sh`,
the 2026-09-07 spec, and the message of commit 90511a1.

The repo as bootstrapped makes the countable rule the target:

| Where | What it says |
|---|---|
| `prose.md:11-13` | the voice file is the only style authority — "not what reads well" |
| `retell.md:56`, `:68-75` | the rules are "the whole of the style brief"; the only quality loop is the checklist, re-run "until it comes back clean" |
| `_template.md:14-19` | every rule must be answerable "without taste entering into it", so every future voice is built out of quotas |
| `README.md:73-75` | "a rule that is not on the checklist is a rule that is not enforced" |
| `earnest.md:144-168` | 7 of 16 checklist items set a per-chapter count or rate |

Three of those budgets are tighter than the corpus they were measured from.
Against the ranges in 90511a1: `-ly` adverbs capped at 5 per 1,000, measured
4.8–5.6; em dashes capped at 1 per 1,000, measured 0.5–2.9; single-sentence
paragraphs set at 35–40%, measured 36–43%. The top of each measured range
fails its own budget, so at least one book of the corpus would fail the
checklist written from it. A corpus average used as a per-chapter ceiling
makes every chapter more uniform than the books are.

Nothing has been drafted — `out/` is empty — so this is a prediction about
what the loop would produce, not an observed failure. It is also the cheapest
moment to change it.

Two things are not the problem. `check.py` gates names, public-domain status,
headings and assembly, and never looks at style. The rules themselves are
good drafting instructions; it is their rank that is wrong.

Inference, not measurement: the checklist's medians and percentages would be
estimated by eye, since `/retell` has no counting tool, so the loop would
optimise the model's guess at a number.

## Decisions

- **The target reader knows the books.** Someone who has read the author's
  1920s fiction would take a page for the author's own. Not the reader who
  knows the reputation, whose recognition is served by heightening the
  signature moves past their corpus rate. This keeps 2026-09-07's decision
  that the count beats the impression: the corpus is what this reader has in
  their ear.
- **A model reads every draft; the owner calibrates it.** A fresh-context
  subagent reads each draft against real corpus passages. The owner reads
  chapter 1 of each cell before chapter 2 is drafted, and those notes go into
  the voice file. A person checks the proxy once per cell instead of once per
  chapter.

## Design

**Touchstones — `touchstones/<voice>.md`.** Six to eight passages from the
corpus books, ~1,500 words, weighted toward dialogue (the Pooh chapters are
mostly talk) and covering an `and` chain, plain description, and a large
moment carried short. Fetched again from Gutenberg — ids 67138, 75201, 61085
and 69683, whose titles are confirmed on fetch — and cut by script, never
transcribed, so punctuation survives exactly. Frontmatter carries `voice`,
`pd_us: true`, and per passage the Gutenberg id with its first and last
words, so any passage can be verified against the original. Verbatim like
`sources/`: `guard-write.sh` gains a `touchstones/*` deny. No extractor is
committed for one voice; when a second voice needs touchstones, promote the
scratch script to `scripts/`.

**The reader — `.claude/agents/reader.md`, tools: Read.** Sees the
touchstones and one draft. Never the voice file, the source chapter, or the
author's name: grounding the judgement in the passages is what makes it the
reader who knows the books rather than the reader who knows the reputation.
Told that the subject matter is not the writer's and that only the telling is
under judgement. Returns the stretches where the draft stops sounding like
the touchstones' writer, worst first, each quoted, each with what it sounds
like instead — the source's own manner, a parody, a rule being obeyed,
generic modern prose. No score: a score is a number to climb.

**`/retell`, reordered.** Draft → reader → rewrite what it quoted, by ear →
reader once more → checklist. What the second pass still flags is reported,
not chased; a proxy optimised against is a metric again. The checklist splits:

- *Prohibitions*, fixed on every hit: tags other than `said`/`asked`, adverbs
  and stage directions in tags, `he realized` and kin, `although`, `however`,
  `therefore`, `moreover`, `having` + participle, rating adjectives in
  narration, the `do_not_name` value, a scene or character added or dropped,
  the draft describing its own style. The corpus has ~none of these, so a
  reader of the books trips on them.
- *Ranges*, looked at and never chased: sentence lengths, `-ly` adverbs,
  named emotions, similes, single-sentence paragraphs, `which`, definite
  articles. A value outside the corpus range sends that stretch back for a
  reread. If it reads right it stays, and the mismatch is reported as a
  defect in the voice file.

After chapter 1 of a new cell, `/retell` stops and asks the owner to read it.

**Voice file and docs.** `earnest.md`'s opening says the numbers describe
where the corpus sits rather than targets to hit; the three budgets the
corpus fails widen to the measured ranges. Rules and the before/after stay —
they are the drafting brief. New frontmatter field `human_read:`, a
comma-separated list of sources whose chapter 1 the owner has read.
`_template.md`, `prose.md`, `README.md` and `.claude/CLAUDE.md` lose "not what
reads well" and "a rule that is not on the checklist is a rule that is not
enforced", and say instead that the reader decides and the rules are how a
draft gets there.

**Gate — `scripts/check.py`.** Two failures added: a voice with no
`touchstones/<voice>.md`, or one whose frontmatter lacks `pd_us: true`; and
any draft past the first chapter in a cell whose source is not listed in that
voice's `human_read`. The owner's read becomes structural rather than
advisory. Style stays out of the gate: judgement remains with `/retell`.

## Testing

Unit tests for both new checks, written first and watched to fail, in the
style of `scripts/tests/test_check.py`: a voice without touchstones, a
touchstones file without `pd_us`, a `02.md` drafted before `human_read` names
the source, and the passing counterparts.

The reader is validated before any cell is run, on three passages: a corpus
passage held out of the touchstones, the heightened parody sample written in
conversation, and Milne's own opening of chapter 1. It must leave the first
alone and flag the other two. If it cannot separate the corpus passage from
the parody it cannot stand in for the reader chosen above, and the design
returns here rather than proceeding.

Then chapter 1 of `winnie-the-pooh` × `earnest`, read by the owner, whose
notes are the first real calibration of both the voice file and the reader.

## Out of scope

A script that counts a draft's ranges: by-eye estimates are tolerable once no
edit is made to move a number, and one gets built if they mislead. Showing
the touchstones to the drafter — the reader stays independent, and lifted
phrasing is the risk; revisit if the reader keeps finding the same slip.
Calibration state in `grid.py`, which reports and never gates.
