---
description: Retell one chapter of a source book in a voice, have it read, then run the voice's checklist
argument-hint: <source> <voice> [chapter | --assemble]
---

Retell a chapter of `$1` in the voice `$2`. Third argument: `$3` — a chapter
number (`3`, `03`) to retell that chapter, `--assemble` to build the finished
book, or empty to retell the next chapter that has no draft.

This command has no `allowed-tools` line: a subagent cannot be named in one,
and the reader below is a subagent. Writes are still bounded by the hooks and
by `.claude/settings.json`.

Current state of the grid:

!`python3 scripts/grid.py`

## Before anything else

1. Read `sources/$1/book.yaml`. **If `pd_status.us` is not `true`, stop and say
   so.** Nothing is generated from a source that is not public domain in the US.
2. Read `voices/$2.md` in full. It is the drafting brief. If it does not exist,
   list `voices/` and stop.
3. Check that `touchstones/$2.md` exists. It is what the reader reads against,
   and without it the reader's pass cannot run. If it is missing, stop and say
   so. **Do not read it yourself** — see the reader's pass below.
4. Note the `do_not_name` value from the voice frontmatter. That name must not
   appear in anything you write.

## If `$3` is `--assemble`

Only assemble when every chapter has a draft — `ls sources/$1/chapters/` and
`ls out/$1/$2/` must return the same count. If they do not, say which chapters
are missing and stop.

Concatenate the drafts in numerical order into `out/$1/$2.md`, separated by a
blank line, and open the file with a title page built from `book.yaml`:

```markdown
# <title>

*Retold in the <name> voice.*

After **<title>** (<year>) by <author>, which is in the public domain in the
United States. Retelling © Otto Quill. The original illustrations are not
used and no illustration from any edition is reproduced here.

---
```

Do not name the author the voice imitates on the title page or anywhere else.
Then run `python3 scripts/grid.py` and report the row.

## Otherwise: retell one chapter

**Pick the chapter.** If `$3` is a number, that one. Otherwise the
lowest-numbered file in `sources/$1/chapters/` with no counterpart in
`out/$1/$2/`. If every chapter has a draft, say so and suggest `--assemble`.

**Stop if the first draft is still unread.** If `out/$1/$2/` already holds a
draft and the `human_read` field in `voices/$2.md` does not list `$1`, stop.
Say which chapter is waiting, and that once it has been read, `$1` goes into
`human_read` and the notes go into the voice file. One chapter is read by a
person before the rest of a cell is written, so that what the reader agent
approves has been checked against a reader once. `scripts/check.py` fails on a
second draft without it, so drafting on regardless only breaks the gate.

**Read the source chapter in full** before writing a word of the retelling.

**Retell it.** The rules in `voices/$2.md` are the drafting brief — how a draft
reaches the sound. They are not the target and their numbers are not quotas.
The target is a reader who knows the author's books taking this for the
author's own.

- Keep every scene, in the source's order.
- Keep every named character. A character in the source chapter is in the draft.
- Keep the outcome of every scene: what happens, happens.
- Change only the telling. Do not add a scene, an incident, a joke, an aside,
  or a line of commentary that the source does not have. Do not remove one.
- Keep the source's chapter heading as the H1, verbatim.
- Do not explain, describe, or refer to the style anywhere in the draft.
- Never write a sentence to make a count come out. A sentence cut in two to
  pull a median down is a sentence nobody wrote.

Write it to `out/$1/$2/NN.md`, `NN` zero-padded to match the source filename.

**Then have it read.** Dispatch the `reader` subagent with exactly two lines:

```
Touchstones: touchstones/$2.md
Draft: out/$1/$2/NN.md
```

Give it nothing else — no rules, no account of the voice, no defence of a
choice you made. It carries its own instructions and it must not know what the
brief said. If the `reader` agent is not available, because the session began
before `.claude/agents/reader.md` existed, dispatch a general-purpose subagent
with the body of that file as its prompt, followed by the same two lines.

**Revise what it quoted.** Rewrite those stretches by ear, from what the reader
said the sound was doing. You do not read the touchstones yourself. Do not
reach for a rule to justify a sentence the reader flagged: the reader heard it,
and hearing it is the thing being tested.

Then dispatch the reader once more, on the revision. Fix what you agree with.
**Do not run it a third time.** A proxy read over and over becomes another
metric; what it still flags is reported, not chased, and is for the person who
reads the chapter to settle.

**Then run the voice's checklist.** `voices/$2.md` ends in two lists, and they
are not run the same way:

- **Prohibitions** — fix every hit. These are constructions the corpus has
  effectively none of, so each one is audible to a reader of the books.
- **Questions** — these describe where the corpus sits. A draft outside one is
  a question about that passage, not a fault: reread it. If it reads right it
  stays, and the mismatch goes in the report as a disagreement between the
  voice file and the page. Never edit a sentence to bring a number inside a
  range. The corpus itself sits outside several of these, book by book.

**Report**: the chapter, the source and retold word counts, what the reader
found and what you changed, which prohibitions fired, which questions the
draft sits outside and what you decided for each, and every place the rules and
the reading disagreed. If this was the first draft of the cell, end by asking for
it to be read.
