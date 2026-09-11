# Where we are

A living note, loaded into every session. Update it the turn a decision is
made, not afterwards. Last updated: 2026-09-11.

## The arc

**What this is for:** public-domain classics retold in the voices of other dead
authors, by Claude Code, one chapter at a time, driven by voice files and
judged by whether a reader who knows the author's books would take the telling
for the author's own.

**Where it stands:** bootstrapped 2026-09-07, on the `bootstrap` branch, not yet
merged to `main`. One source (`winnie-the-pooh`, 10 chapters, 22,104 words),
one voice (`earnest`, written from 201,000 measured corpus words), zero cells
started. Nothing under `out/`.

**What moves next:** the reader-first redesign — a model reader grounded in
real corpus passages, the checklist demoted beneath it, a gate on the owner's
read of chapter 1 — designed in conversation 2026-09-11, pending approval.
Then the first cell, `/retell winnie-the-pooh earnest`.

## Decisions in force

- 2026-09-07 — Sources are verbatim; the extractor is fixed, never the text. A
  `PreToolUse` hook refuses edits under `sources/`.
- 2026-09-07 — `pd_status.us` is confirmed by hand before any cell starts.
- 2026-09-07 — A voice file never names its author; the name sits once in
  `do_not_name` so the rule can check itself, and `scripts/check.py` does.
- 2026-09-07 — Voice rules come from measurement, not impression: where the
  popular picture of a style and the counted corpus disagreed, the count won
  (eight corrections to `earnest.md`, commit 90511a1).
- 2026-09-07 — Memory lives in `memory/` under git with auto-memory pointed at
  it and this note loaded by `@` import; `scripts/check.py` is the gate, run by
  a `Stop` hook. Design record in `docs/superpowers/specs/`.
- 2026-09-11 — The target is a reader who knows the author's books taking a
  retelling for the author's own, not a reader who knows the reputation. The
  voice file's rules are the drafter's means and its numbers are corpus ranges
  that send a passage back for rereading, never quotas to edit toward. The
  2026-09-07 measurement decision stands: the corpus is what that reader has
  in their ear.
- 2026-09-11 — A model reader, given real corpus passages and never the rules
  or the name, reads every draft and outranks the checklist. The owner reads
  chapter 1 of each cell before chapter 2 is drafted, and those notes go into
  the voice file.

## Live defects

- `sources/winnie-the-pooh/book.yaml` says `pd_status.us: true`, but that is
  `fetch.py`'s default and nothing in the file records whether it was checked
  by hand. Winnie-the-Pooh (1926) entered the US public domain on 2022-01-01;
  the check is trivial, the record of it is what is missing.

## Parked

Nothing.
