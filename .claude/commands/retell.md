---
description: Retell one chapter of a source book in a voice, then check the draft against the voice's own checklist
argument-hint: <source> <voice> [chapter | --assemble]
allowed-tools: Read, Write, Edit, Glob, Bash(python3 scripts/grid.py:*), Bash(ls:*), Bash(cat:*), Bash(grep:*)
---

Retell a chapter of `$1` in the voice `$2`. Third argument: `$3` — a chapter
number (`3`, `03`) to retell that chapter, `--assemble` to build the finished
book, or empty to retell the next chapter that has no draft.

Current state of the grid:

!`python3 scripts/grid.py`

## Before anything else

1. Read `sources/$1/book.yaml`. **If `pd_status.us` is not `true`, stop and say
   so.** Nothing is generated from a source that is not public domain in the US.
2. Read `voices/$2.md` in full. It is the only style authority for this task.
   If it does not exist, list `voices/` and stop.
3. Note the `do_not_name` value from the voice frontmatter. That name must not
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

**Read the source chapter in full** before writing a word of the retelling.

**Retell it.** The rules in `voices/$2.md` are the whole of the style brief.

- Keep every scene, in the source's order.
- Keep every named character. A character in the source chapter is in the draft.
- Keep the outcome of every scene: what happens, happens.
- Change only the telling. Do not add a scene, an incident, a joke, an aside,
  or a line of commentary that the source does not have. Do not remove one.
- Keep the source's chapter heading as the H1, verbatim.
- Do not explain, describe, or refer to the style anywhere in the draft.

Write it to `out/$1/$2/NN.md`, `NN` zero-padded to match the source filename.

**Then check your own draft.** Read the **Checklist** section of `voices/$2.md`
and answer every item against the file you just wrote, one at a time, quoting
the offending sentence for each `no`. Fix every one and re-run the checklist
until it comes back clean. This is not optional and it is not a summary step —
an unchecked draft is not a draft.

**Report**: the chapter, the source and retold word counts, and every checklist
item that fired and what you changed.
