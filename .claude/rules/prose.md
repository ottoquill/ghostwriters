---
description: Style authority and prohibitions for generated retellings
paths: ["out/**/*.md"]
---

# Writing under out/

Everything under `out/` is a retelling of a source book in one voice. While
writing one:

- **The target is a reader.** A retelling is right when someone who knows the
  author's books would take a page of it for the author's own. That is settled
  by ear — by the reader agent, and then by a person — never by counting.
- **The voice file is how a draft gets there, not what it aims at.**
  `voices/<voice>.md` decides sentence length, vocabulary, dialogue and rhythm,
  and nothing else does: not the source's own style, not your default register.
  Its rules are means and its numbers describe where the corpus sits. No
  sentence is ever written or edited to move a count.
- **Where a rule and the reading disagree, the reading wins.** Rewrite what the
  reader flagged. Keep a sentence that reads right and sits outside a range,
  and report the disagreement: it is a defect in the voice file, and the voice
  file is what gets corrected.
- **Never name the author the voice imitates.** The name is in the voice file's
  `do_not_name` frontmatter field so you can check for it. It does not belong
  in the prose, a heading, a title page, or a note.
- **Never describe or explain the style in the output.** No preface, no
  afterword, no line about how the telling has changed. The reader gets the
  story; the method stays in `voices/`.
- **Add nothing the source does not have.** No scene, no character, no
  incident, no joke, no aside, no commentary. Every named character and every
  scene in the source chapter survives into the retelling, in the source's
  order, with the same outcome. Only the telling changes.
