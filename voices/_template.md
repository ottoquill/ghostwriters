---
name: <slug, identical to the filename without .md>
tagline: <under twelve words; describes the prose, never the person>
era: <e.g. 1920s American, late-Victorian English, interwar Anglo-Irish>
do_not_name: <Full Name Of The Author>
human_read:
---

<!--
  This is the shape a voice file must have. Copy it to voices/<slug>.md and
  replace every angle-bracketed placeholder and every example rule.

  Four things make a voice file work, and all four are easy to lose:

  1. The file is a BRIEF, not a target. What a retelling aims at is a reader
     who knows the author's books taking a page of it for the author's own.
     Rules are written concretely because a concrete rule moves prose and a
     vague one moves nothing -- "no dialogue tag but `said`" does work that
     "muscular" cannot -- and every section has to be filled in, because prose
     reverts to the house default along any axis the brief leaves silent. But
     a rule is a means. Nothing in this file is the thing being aimed at.

  2. Numbers are RANGES, measured across the corpus's own books, and they
     describe rather than instruct. Where one book runs 0.5 per 1,000 and
     another 2.9, the range is 0.5 to 2.9. An average turned into a per-chapter
     ceiling is stricter than the writer was, and yields chapters more uniform
     than any the writer wrote. A draft outside a range is a passage to reread,
     never a sentence to edit until the count moves.

  3. The author is NEVER named in the body. The name lives in do_not_name in
     the frontmatter, once, so that the prohibition carries its own test:
     grep the body for that string and the file fails if it hits. A rule that
     says "write like X" tells a writer to reach for their impression of X;
     rules about sentence length tell them what to do.

  4. Every voice needs touchstones/<slug>.md: passages cut verbatim by script
     from public-domain texts, declaring pd_us: true, naming no author and no
     title. The reader agent judges a draft against those passages and nothing
     else, and scripts/check.py fails a voice that has none.

  Delete this comment when you fill the file in.
-->

## Sentences

<Length, structure, and where a sentence starts. Give numbers.>

- Median sentence under <N> words. No sentence over <N> words.
- <At least/no more than> <N> in <M> sentences opens on its grammatical subject.
- No semicolons. / Semicolons only between two independent clauses.
- Coordinate with `and`; do not subordinate with `although`, `whereas`, `while`.
- No sentence contains more than <N> commas.

## Words

<Vocabulary, register, and the specific words that are banned or rationed.>

- No adverb ending in `-ly`.
- No word of Latin origin where a shorter Germanic one exists: `use` not `utilise`.
- Banned outright: <list>.
- Rationed to <N> per thousand words: <list>.
- Concrete nouns only in <position>; no abstract noun ends a paragraph.

## Emotion and meaning

<How feeling reaches the page. The commonest failure axis, because it is the
one writers describe rather than specify.>

- Never name an emotion. Give the action or the physical fact instead.
- No sentence explains why a character did something.
- No narrator comment on an event after the event.
- The point of a scene is never stated in the scene.

## Description

<What gets described, how much, and in what order.>

- No more than <N> consecutive sentences of description.
- Describe only what a camera in the scene could record.
- No simile. / Simile only where both terms are physical objects.
- Colour named only when it distinguishes one thing from another.
- No weather at the opening of a chapter.

## Dialogue

<Tags, punctuation, and what speech is allowed to do.>

- No tag but `said`. No adverb on any tag.
- No speech longer than <N> words without an interruption.
- Characters do not answer the question they were asked.
- No dialect spelling. Register is carried by word choice and syntax.

## Rhythm

<How units end and how they follow one another. Paragraph and chapter shape.>

- Paragraphs of <N> to <M> sentences.
- A paragraph does not end on its longest sentence.
- No paragraph ends on an abstract noun.
- The chapter's last sentence is under <N> words and states a fact.
- <N> to <M> single-sentence paragraphs per chapter, no two adjacent.

## Before / after

<A short passage in neutral prose, then the same passage under these rules.
Same scene, same characters, same events. Only the telling changes. Keep both
under 120 words so the difference is legible at a glance.>

**Before**

> <neutral version>

**After**

> <same content, these rules applied>

## Checklist

<Two lists, run against a finished draft after the reader agent has read it and
never in place of that. Keep each under ten items: a checklist nobody finishes
is not a gate.>

### Prohibitions — fix every hit

<Only constructions the corpus effectively lacks, plus the repository's own
rules. If you cannot say that the measurement found approximately none, it is
not a prohibition -- it is a question. A banned construction that turns up in
the corpus is how a voice file ends up stricter than the writer.>

1. Does any dialogue tag other than `said` appear?
2. Does any tag carry an adverb?
3. Does any word banned outright in **Words** appear?
4. Is the author's name -- the `do_not_name` value -- anywhere in the draft?
5. Does the draft contain a scene, character, or joke absent from the source,
   or is any named character from the source chapter missing?
6. Does the draft describe or explain its own style?

### Questions — reread the passage, decide, report

<Ranges and habits. Each asks whether a stretch is worth rereading, and the
answer may be that it reads right and the range is wrong. Say so in the report:
that is how this file gets corrected.>

7. Is the median sentence length near <N> words?
8. Do `-ly` adverbs sit far outside <N> to <M> per 1,000 words?
9. Are emotions named more often than <N> per 1,000 words?
10. Does any paragraph end on an abstract noun where it could have ended on the
    thing itself?
11. Is any rationed word far outside its measured range for this word count?
12. Does any sentence explain a character's reasons to the reader?
