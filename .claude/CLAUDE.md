# ghostwriters

Public-domain classics, ghostwritten by other dead authors.

The repo holds a set of source books and a set of author voices. The product is
the cross product: every source retold in every voice. Claude Code does the
retelling, one chapter at a time, driven by a voice file that describes the
prose as concrete rules and never names the author it imitates.

## Layout

```
sources/<slug>/book.yaml         title, author, year, gutenberg_id, pd_status, notes
sources/<slug>/chapters/NN.md    one file per chapter, original text verbatim
voices/<slug>.md                 style rules; frontmatter name, tagline, era, do_not_name
voices/_template.md              the shape a voice file must have
out/<source>/<voice>/NN.md       per-chapter drafts while a cell is in progress
out/<source>/<voice>.md          the finished retelling, assembled
scripts/                         fetch.py, grid.py
```

## Scripts

Stdlib-only Python 3. No build step, no dependencies.

```bash
python3 scripts/fetch.py <gutenberg_id> <slug>   # -> sources/<slug>/
python3 scripts/fetch.py 67098 pooh --dry-run    # report the split, write nothing
python3 scripts/grid.py                          # the source x voice matrix
```

`fetch.py` cuts the Gutenberg header and footer and splits on chapter headings.
If a book's headings are a form it does not know, add the form to `CHAPTER_RE`
and `is_subtitle` — do not hand-edit the chapters it produces.

`grid.py` reports; it never gates. A cell is `done`, `N/M`, or `.`.

## The slash command

`/retell <source> <voice> [chapter | --assemble]` — retells one chapter into
`out/<source>/<voice>/NN.md`, then runs the voice file's own Checklist against
the draft and fixes what it finds. `--assemble` builds `out/<source>/<voice>.md`
once every chapter has a draft.

## Three hard rules

1. **Sources are verbatim and never edited.** `sources/` is the record of what
   the book says. A typo in it is the book's typo. Fix the extractor, not the text.
2. **`pd_status.us` must be `true` before anything is generated from a source.**
   `fetch.py` writes that field as a default, not as a finding. Check it by hand.
   No cell is started against a source whose US status is unconfirmed.
3. **Voice files never name the author.** The name goes in `do_not_name` in the
   frontmatter, once, so the rule can check itself: grep the body for that
   string. Rules about sentences move prose; "write like X" does not.

`.claude/rules/prose.md` carries the rules that apply while writing under `out/`.
