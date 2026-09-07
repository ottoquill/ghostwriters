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
not the model but the voice file. A voice is written down as rules that can be
checked — a median sentence length, a ban on any dialogue tag but `said`, a
prohibition on naming an emotion — because prose only moves along the axes a
brief makes checkable and reverts to the house average everywhere else. A voice
file never names the author it imitates. The name sits once in the frontmatter,
in a field called `do_not_name`, so the prohibition carries its own test; the
rules in the body have to do the work on their own. Telling a model to write
like somebody gets you the model's impression of that somebody. Telling it that
no sentence may exceed fourteen words gets you fourteen-word sentences.

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

Two things to get right. Every rule must be answerable yes or no by a reader
with no memory of the file — "no adverb ending in `-ly`" is a rule, "lyrical" is
not, and a section left vague is a section along which the prose will not move.
And the author's name goes in the `do_not_name` frontmatter field and nowhere
else, so the file can be checked against itself with `grep`.

The Checklist at the bottom is the gate. `/retell` runs it against its own draft
and fixes what it finds before returning, so a rule that is not on the checklist
is a rule that is not enforced.

## Running a cell

```
/retell winnie-the-pooh earnest        # the next chapter with no draft
/retell winnie-the-pooh earnest 3      # chapter 3 specifically
/retell winnie-the-pooh earnest --assemble
```

Drafts land in `out/<source>/<voice>/NN.md`. Once every chapter has one,
`--assemble` concatenates them into `out/<source>/<voice>.md` behind a title
page crediting the source, its year, and its public-domain status. No original
illustration is reproduced, from any edition, anywhere in this repository.

## Licences

Three sets of terms, kept apart:

- [`LICENSE`](LICENSE) — MIT, covering `scripts/`, `.claude/`, and this README.
- [`LICENSE-OUTPUT`](LICENSE-OUTPUT) — `sources/` is public domain in the United
  States; `out/` is copyright Otto Quill, all rights reserved.
