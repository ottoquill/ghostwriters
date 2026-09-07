---
description: Style authority and prohibitions for generated retellings
paths: ["out/**/*.md"]
---

# Writing under out/

Everything under `out/` is a retelling of a source book in one voice. While
writing one:

- **The active voice file is the only style authority.** `voices/<voice>.md`
  decides sentence length, vocabulary, dialogue, rhythm. Nothing else does —
  not the source's own style, not your default register, not what reads well.
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
