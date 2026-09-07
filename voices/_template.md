---
name: <slug, identical to the filename without .md>
tagline: <under twelve words; describes the prose, never the person>
era: <e.g. 1920s American, late-Victorian English, interwar Anglo-Irish>
do_not_name: <Full Name Of The Author>
---

<!--
  This is the shape a voice file must have. Copy it to voices/<slug>.md and
  replace every angle-bracketed placeholder and every example rule.

  Two things make a voice file work, and both are easy to lose:

  1. Every rule is CHECKABLE. A rule is checkable when a reader with no memory
     of this file can answer yes or no about a sentence without taste entering
     into it. "No dialogue tag but `said`" is checkable. "Muscular" is not.
     Prose moves along exactly the axes a brief makes checkable and stays at
     the house default everywhere else, which is why every section below has
     to be filled in even when the voice feels unremarkable on that axis.

  2. The author is NEVER named in the body. The name lives in do_not_name in
     the frontmatter, once, so that the prohibition carries its own test:
     grep the body for that string and the file fails if it hits. A rule that
     says "write like X" tells a writer to reach for their impression of X;
     rules about sentence length tell them what to do.

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

<Run this against a finished draft before returning it. Each item is a yes/no
question that maps to one rule above, and each is answerable without judgement.
Fix every no. Keep the list under fifteen items -- a checklist nobody finishes
is not a gate.>

1. Is every sentence under <N> words?
2. Does any sentence contain a word ending in `-ly` used as an adverb?
3. Does any dialogue tag other than `said` appear?
4. Does any tag carry an adverb?
5. Is any emotion named directly?
6. Does any sentence explain a character's motive?
7. Does any paragraph end on an abstract noun?
8. Does any banned word from **Words** appear?
9. Is any rationed word over its budget for the chapter's word count?
10. Is the author's name -- the `do_not_name` value -- anywhere in the draft?
11. Does the draft contain a scene, character, or joke absent from the source?
12. Is any named character from the source chapter missing?
13. Does the draft describe or explain its own style?
