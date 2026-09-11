import contextlib, io, os, pathlib, sys, tempfile, unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import check  # noqa: E402

VOICE = """\
---
name: earnest
tagline: Short declaratives, plain nouns
era: 1920s American
do_not_name: Ernest Hemingway
human_read: pooh
---

## Sentences

- Median sentence under 8 words.

## Checklist

1. Is every sentence under 20 words?
"""

# Verbatim passages a draft is read against. No author, no title: the id and
# the anchors are what makes a passage checkable against its original.
TOUCHSTONES = """\
---
voice: earnest
pd_us: true
provenance: Project Gutenberg ebook 61085
---

## 1

<!-- gutenberg 61085 | They shot ... his knees. -->

They shot the six cabinet ministers at half-past six in the morning
against the wall of a hospital.
"""

# A template has placeholder frontmatter, a name that is not its filename, and
# the literal placeholder text in its body. None of that may be reported.
TEMPLATE = """\
---
name: <slug, identical to the filename without .md>
tagline: <under twelve words>
era: <e.g. 1920s American>
do_not_name: <Full Name Of The Author>
---

<!-- Put the author in do_not_name as Full Name Of The Author. -->
"""

BOOK = """\
title: "Winnie-the-Pooh"
author: "A. A. Milne"
year: 1926
gutenberg_id: 67098
pd_status:
  us: {us}
  uk: false
notes: "fetched"
"""

CH1 = "# CHAPTER I: IN WHICH WE ARE INTRODUCED\n\nHere is Edward Bear.\n"
CH2 = "# CHAPTER II: IN WHICH POOH GOES VISITING\n\nEdward Bear went visiting.\n"


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


class CheckTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        write(self.root, "voices/earnest.md", VOICE)
        write(self.root, "voices/_template.md", TEMPLATE)
        write(self.root, "touchstones/earnest.md", TOUCHSTONES)
        write(self.root, "sources/pooh/book.yaml", BOOK.format(us="true"))
        write(self.root, "sources/pooh/chapters/01.md", CH1)
        write(self.root, "sources/pooh/chapters/02.md", CH2)

    def tearDown(self):
        self._tmp.cleanup()

    def problems(self):
        return check.run(self.root)

    def assertProblem(self, fragment):
        found = self.problems()
        self.assertTrue(
            any(fragment in p for p in found), "expected %r in %r" % (fragment, found)
        )

    # voices

    def test_clean_tree_has_no_problems(self):
        self.assertEqual(self.problems(), [])

    def test_voice_body_naming_its_author_fails(self):
        write(self.root, "voices/earnest.md", VOICE + "\nWrite like Hemingway.\n")
        self.assertProblem("voices/earnest.md: names the author")

    def test_author_match_ignores_case(self):
        write(self.root, "voices/earnest.md", VOICE + "\nernest hemingway wrote it.\n")
        self.assertProblem("voices/earnest.md: names the author")

    def test_voice_name_must_match_filename(self):
        write(self.root, "voices/earnest.md", VOICE.replace("name: earnest", "name: ernest"))
        self.assertProblem("voices/earnest.md: name is 'ernest'")

    def test_voice_missing_frontmatter_field_fails(self):
        write(self.root, "voices/earnest.md", VOICE.replace("era: 1920s American\n", ""))
        self.assertProblem("voices/earnest.md: frontmatter lacks era")

    # sources

    def test_source_chapter_must_open_on_h1(self):
        write(self.root, "sources/pooh/chapters/02.md", "CHAPTER II\n\ntext\n")
        self.assertProblem("sources/pooh/chapters/02.md: does not open on an H1")

    def test_source_without_book_yaml_fails(self):
        os.remove(os.path.join(self.root, "sources/pooh/book.yaml"))
        self.assertProblem("sources/pooh/book.yaml: missing")

    # drafts

    def test_clean_draft_passes(self):
        write(self.root, "out/pooh/earnest/01.md", CH1.replace("Here is Edward Bear.", "Edward Bear came down."))
        self.assertEqual(self.problems(), [])

    def test_draft_naming_author_fails(self):
        write(self.root, "out/pooh/earnest/01.md", CH1 + "\nHemingway's bear.\n")
        self.assertProblem("out/pooh/earnest/01.md: names the author")

    def test_output_from_unconfirmed_source_fails(self):
        write(self.root, "sources/pooh/book.yaml", BOOK.format(us="false"))
        write(self.root, "out/pooh/earnest/01.md", CH1)
        self.assertProblem("out/pooh: pd_status.us is not true")

    def test_draft_heading_must_match_source(self):
        write(self.root, "out/pooh/earnest/01.md", "# Chapter One\n\ntext\n")
        self.assertProblem("out/pooh/earnest/01.md: H1 differs from source")

    def test_draft_for_missing_chapter_fails(self):
        write(self.root, "out/pooh/earnest/03.md", "# CHAPTER III\n\ntext\n")
        self.assertProblem("out/pooh/earnest/03.md: no source chapter 03.md")

    def test_draft_for_unknown_voice_fails(self):
        write(self.root, "out/pooh/nobody/01.md", CH1)
        self.assertProblem("out/pooh/nobody: no voice 'nobody'")

    def test_draft_for_unknown_source_fails(self):
        write(self.root, "out/piglet/earnest/01.md", CH1)
        self.assertProblem("out/piglet: no source 'piglet'")

    # touchstones

    def test_voice_without_touchstones_fails(self):
        os.remove(os.path.join(self.root, "touchstones/earnest.md"))
        self.assertProblem("touchstones/earnest.md: missing")

    def test_touchstones_without_pd_us_fails(self):
        write(self.root, "touchstones/earnest.md", TOUCHSTONES.replace("pd_us: true\n", ""))
        self.assertProblem("touchstones/earnest.md: pd_us is not true")

    def test_touchstones_with_pd_us_false_fails(self):
        write(self.root, "touchstones/earnest.md", TOUCHSTONES.replace("pd_us: true", "pd_us: false"))
        self.assertProblem("touchstones/earnest.md: pd_us is not true")

    def test_template_needs_no_touchstones(self):
        self.assertEqual(self.problems(), [])

    # a person reads the first draft of a cell before the rest are written

    def test_one_draft_needs_no_human_read(self):
        write(self.root, "voices/earnest.md", VOICE.replace("human_read: pooh\n", ""))
        write(self.root, "out/pooh/earnest/01.md", CH1)
        self.assertEqual(self.problems(), [])

    def test_second_draft_without_human_read_fails(self):
        write(self.root, "voices/earnest.md", VOICE.replace("human_read: pooh\n", ""))
        write(self.root, "out/pooh/earnest/01.md", CH1)
        write(self.root, "out/pooh/earnest/02.md", CH2)
        self.assertProblem("out/pooh/earnest: 2 drafts, but nothing records a person reading the first")

    def test_second_draft_with_human_read_passes(self):
        write(self.root, "out/pooh/earnest/01.md", CH1)
        write(self.root, "out/pooh/earnest/02.md", CH2)
        self.assertEqual(self.problems(), [])

    def test_human_read_of_another_source_does_not_count(self):
        write(self.root, "voices/earnest.md", VOICE.replace("human_read: pooh", "human_read: piglet"))
        write(self.root, "out/pooh/earnest/01.md", CH1)
        write(self.root, "out/pooh/earnest/02.md", CH2)
        self.assertProblem("out/pooh/earnest: 2 drafts, but nothing records a person reading the first")

    # assembled

    def test_assembled_before_every_chapter_drafted_fails(self):
        write(self.root, "out/pooh/earnest/01.md", CH1)
        write(self.root, "out/pooh/earnest.md", "# Winnie-the-Pooh\n\n" + CH1)
        self.assertProblem("out/pooh/earnest.md: assembled with 1 of 2 chapters drafted")

    def test_assembled_with_every_chapter_passes(self):
        write(self.root, "out/pooh/earnest/01.md", CH1)
        write(self.root, "out/pooh/earnest/02.md", CH2)
        write(self.root, "out/pooh/earnest.md", "# Winnie-the-Pooh\n\n" + CH1 + "\n" + CH2)
        self.assertEqual(self.problems(), [])

    def test_assembled_naming_author_fails(self):
        write(self.root, "out/pooh/earnest/01.md", CH1)
        write(self.root, "out/pooh/earnest/02.md", CH2)
        write(self.root, "out/pooh/earnest.md", "# Winnie-the-Pooh\n\nAfter Hemingway.\n")
        self.assertProblem("out/pooh/earnest.md: names the author")

    # exit code

    def main(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = check.main(["--root", self.root])
        return code, out.getvalue()

    def test_main_exits_zero_and_says_ok_when_clean(self):
        code, out = self.main()
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("ok: 1 voices, 1 sources, 0 drafts, 0 assembled"), out)

    def test_main_exits_one_and_lists_the_problem(self):
        write(self.root, "out/pooh/earnest/01.md", CH1 + "\nHemingway.\n")
        code, out = self.main()
        self.assertEqual(code, 1)
        self.assertIn("out/pooh/earnest/01.md: names the author", out)
        self.assertIn("1 problem\n", out)


if __name__ == "__main__":
    unittest.main()
