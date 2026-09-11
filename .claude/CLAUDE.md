# ghostwriters

Public-domain classics, ghostwritten by other dead authors.

The repo holds a set of source books and a set of author voices. The product is
the cross product: every source retold in every voice. Claude Code does the
retelling, one chapter at a time, driven by a voice file that describes the
prose as concrete rules and never names the author it imitates — and judged by
a reader, not by the rules. A chapter is right when somebody who knows the
author's books would take a page of it for the author's own.

The current state is loaded with this file rather than read on demand:

@../memory/where-we-are.md

## Layout

```
sources/<slug>/book.yaml         title, author, year, gutenberg_id, pd_status, notes
sources/<slug>/chapters/NN.md    one file per chapter, original text verbatim
voices/<slug>.md                 style rules; frontmatter name, tagline, era, do_not_name, human_read
voices/_template.md              the shape a voice file must have
touchstones/<slug>.md            verbatim passages a draft is read against; pd_us: true
.claude/agents/reader.md         the reader: touchstones plus a draft, nothing else
out/<source>/<voice>/NN.md       per-chapter drafts while a cell is in progress
out/<source>/<voice>.md          the finished retelling, assembled
memory/                          what a session needs that the code does not say
scripts/                         fetch.py, grid.py, check.py, tests/
```

## Scripts

Stdlib-only Python 3. No build step, no dependencies.

```bash
python3 scripts/fetch.py <gutenberg_id> <slug>   # -> sources/<slug>/
python3 scripts/fetch.py 67098 pooh --dry-run    # report the split, write nothing
python3 scripts/grid.py                          # the source x voice matrix
python3 scripts/check.py                         # the gate; exit 1 on any problem
python3 -m unittest discover -s scripts/tests -t .
```

`fetch.py` cuts the Gutenberg header and footer and splits on chapter headings.
If a book's headings are a form it does not know, add the form to `CHAPTER_RE`
and `is_subtitle` — do not hand-edit the chapters it produces.

`grid.py` reports; it never gates. A cell is `done`, `N/M`, or `.`.

`check.py` gates. It fails when a voice file or a retelling contains the name in
`do_not_name`, when anything under `out/` belongs to a source whose
`pd_status.us` is not `true`, when a draft's H1 differs from its source
chapter's, when a book is assembled before every chapter has a draft, when a
voice's frontmatter is incomplete, when a voice has no `touchstones/<slug>.md`
or its touchstones do not declare `pd_us: true`, or when a cell holds a second
draft and the voice's `human_read` does not list the source. It says nothing
about style: that is judgment, and it belongs to the reader. A `Stop` hook runs
it at the end of every turn; a `PreToolUse` hook refuses edits under `sources/`
and `touchstones/`.

## The slash command

`/retell <source> <voice> [chapter | --assemble]` — retells one chapter into
`out/<source>/<voice>/NN.md`, has the `reader` agent read it against
`touchstones/<voice>.md`, rewrites what the reader quoted, has it read once
more, and only then runs the voice file's two lists: Prohibitions, fixed on
sight, and Questions, which send a passage back for a reread and are never
edited toward. The first draft of a cell then waits for a person to read it.
`--assemble` builds `out/<source>/<voice>.md` once every chapter has a draft.

## Four hard rules

1. **Sources are verbatim and never edited.** `sources/` is the record of what
   the book says. A typo in it is the book's typo. Fix the extractor, not the text.
2. **`pd_status.us` must be `true` before anything is generated from a source.**
   `fetch.py` writes that field as a default, not as a finding. Check it by hand.
   No cell is started against a source whose US status is unconfirmed.
3. **Voice files never name the author.** The name goes in `do_not_name` in the
   frontmatter, once, so the rule can check itself: grep the body for that
   string. Rules about sentences move prose; "write like X" does not.
4. **The reader outranks the rules.** The rules are how a draft reaches the
   sound; the numbers describe where the corpus sits, in ranges, and mark
   passages worth rereading. Never write or edit a sentence to move a count.
   Where a rule and the reading disagree, the reading wins and the voice file
   is what gets corrected.

`.claude/rules/prose.md` carries the rules that apply while writing under `out/`.
The other rules there are written without this project's nouns so they can be
copied into another repo unchanged; `memory/` and `.claude/hooks/` travel the
same way.
