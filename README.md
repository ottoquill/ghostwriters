# ghostwriters

Public-domain classics, ghostwritten by other dead authors.

## The premise

The repo holds two sets: source books that have fallen into the public domain,
and voices distilled from authors who wrote in some other register entirely.
The product is the cross product. Every source is retold in every voice, one
chapter at a time, and each cell of the grid is a whole short book — the same
scenes, the same characters, the same things happening in the same order, told
by somebody who would never have told them that way.

The retelling is done by Claude Code, and the thing that makes a cell work is
not the model but the voice file. A voice is written down as rules concrete
enough to move prose — a median sentence length, a ban on any dialogue tag but
`said`, a ration on naming an emotion — because prose only moves along the axes
a brief makes concrete and reverts to the house average everywhere else. A
voice file never names the author it imitates. The name sits once in the
frontmatter, in a field called `do_not_name`, so the prohibition carries its
own test; the rules in the body have to do the work on their own. Telling a
model to write like somebody gets you the model's impression of that somebody.
Telling it that no sentence may exceed fourteen words gets you fourteen-word
sentences.

Fourteen-word sentences are not the point, though, and the rest of the design
exists to keep them from becoming it. A chapter is right when a reader who
knows the author's books would take a page of it for the author's own, and
nothing else is right. So every draft is read: first by an agent that sees a
page and a half of real passages from those books and the draft, and nothing
else — no rules, no checklist, no author's name — and quotes back every stretch
where the draft stops sounding like the same hand; then by a person, once per
cell, before the remaining chapters are written. The numbers in a voice file
are measured ranges that say where the corpus sits. They mark passages worth
rereading. No sentence is ever edited to move one, and the corpus itself falls
outside several of them, book by book.

In the line of Proust's *L'Affaire Lemoine*, Queneau's *Exercises in Style*,
Hemingway's *The Torrents of Spring*, Frederick Crews's *The Pooh Perplex*, and
Angus Croll's *If Hemingway Wrote JavaScript*.

## The grid

```
source            ch     words  earnest
---------------------------------------
winnie-the-pooh   10    22,104  .
---------------------------------------
1 cell (1 source x 1 voice): 0 done, 0 started, 1 empty
source words: 22,104   retold words: 0
```

`python3 scripts/grid.py`. A cell is `done` when `out/<source>/<voice>.md`
exists, `N/M` when N of M chapters are drafted, `.` when nothing is written.

## Adding a source

```bash
python3 scripts/fetch.py 67098 winnie-the-pooh --dry-run   # check the split
python3 scripts/fetch.py 67098 winnie-the-pooh             # write it
```

That writes `sources/<slug>/book.yaml` and `sources/<slug>/chapters/NN.md`, one
file per chapter, with the chapter heading as an H1.

Then **open `book.yaml` and confirm `pd_status.us`**. `fetch.py` writes it as a
default, not as a finding. Nothing is generated from a source whose US
public-domain status has not been checked by hand.

If `fetch.py` gets the chapter split wrong, fix `CHAPTER_RE` or `is_subtitle` in
the script and run it again. Do not hand-edit the chapters. `sources/` is the
record of what the book says, verbatim, including its typos.

## Adding a voice

Copy [`voices/_template.md`](voices/_template.md) to `voices/<slug>.md` and fill
in every section: Sentences, Words, Emotion and meaning, Description, Dialogue,
Rhythm, Before / after, Checklist.

Three things to get right. Every rule must be answerable yes or no by a reader
with no memory of the file — "no adverb ending in `-ly`" is a rule, "lyrical" is
not, and a section left vague is a section along which the prose will not move.
Every number must be a range measured across the corpus's own books, not an
average turned into a ceiling: a voice file stricter than the writer produces
chapters more uniform than any the writer wrote. And the author's name goes in
the `do_not_name` frontmatter field and nowhere else, so the file can be checked
against itself with `grep`.

Every voice also needs `touchstones/<slug>.md`: passages cut verbatim by script
from the author's own public-domain books, naming neither author nor title.
That file is the ear the drafts are judged against, and `check.py` fails a voice
that has none.

The Checklist at the bottom is two lists. **Prohibitions** are fixed on sight,
and hold only what the measurement found the corpus effectively lacks.
**Questions** are ranges and habits: a draft outside one gets reread, and if it
reads right it stays and the voice file is what gets corrected. Neither list
outranks the reader.

## Running a cell

```
/retell winnie-the-pooh earnest        # the next chapter with no draft
/retell winnie-the-pooh earnest 3      # chapter 3 specifically
/retell winnie-the-pooh earnest --assemble
```

Drafts land in `out/<source>/<voice>/NN.md`. Each one is read by the `reader`
agent, revised where the reader says the sound goes wrong, read once more, and
only then run against the voice's two lists. What the second reading still
flags is reported rather than chased: a proxy consulted over and over is a
metric again.

The first draft of a cell stops there and waits to be read by a person. Once it
has been, the source goes into the voice file's `human_read` field and the notes
go into the rules; `check.py` fails a cell that holds a second draft before
that. Once every chapter has one, `--assemble` concatenates them into
`out/<source>/<voice>.md` behind a title page crediting the source, its year,
and its public-domain status. No original illustration is reproduced, from any
edition, anywhere in this repository.

## The check

```
python3 scripts/check.py
```

Exit 1 on anything a script can prove wrong: a voice file or a retelling that
contains the name in `do_not_name`; output from a source whose `pd_status.us` is
not `true`; a draft whose chapter heading is not its source's, verbatim; a book
assembled before every chapter has a draft; a voice file missing a frontmatter
field; a voice with no touchstones, or touchstones that do not declare
`pd_us: true`; a cell holding a second draft when nothing records a person
having read the first. A `Stop` hook runs it at the end of every Claude Code
turn, so a session cannot end with the repo in a state the check rejects.

Style is deliberately absent from that list. Whether a chapter sounds like the
author is judgment, and it stays with the reader agent, the voice's two lists,
and the person who reads the first chapter of a cell. What a script holds is
everything else.

## Working with Claude Code

`memory/` is what a session needs that the code does not say. `where-we-are.md`
is loaded into every session — the arc, the decisions in force, the live
defects, dated — and `MEMORY.md` indexes the smaller notes. The auto-memory
system is pointed at this directory, so what one session learns is committed
for the next. The rules under `.claude/rules/` are written without this
project's nouns; `memory/`, `.claude/hooks/` and those rules can be copied into
another repo as they are.

## Licences

Three sets of terms, kept apart:

- [`LICENSE`](LICENSE) — MIT, covering `scripts/`, `.claude/`, and this README.
- [`LICENSE-OUTPUT`](LICENSE-OUTPUT) — `sources/` is public domain in the United
  States; `out/` is copyright Otto Quill, all rights reserved.
