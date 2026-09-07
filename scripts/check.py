#!/usr/bin/env python3
"""
check.py -- the gate. Exit 1 on anything a script can prove wrong.

    python3 scripts/check.py
    python3 scripts/check.py --root .

What it checks:

    voices/<v>.md      frontmatter has name, tagline, era, do_not_name; name is
                       the filename; the body never contains the do_not_name
                       value or its surname. A file starting with _ is a
                       template and is skipped.
    sources/<s>/       book.yaml exists; every chapters/NN.md opens on an H1.
    out/<s>/           the source exists and its pd_status.us is true.
    out/<s>/<v>/NN.md  the voice exists; there is a source chapter NN.md; the
                       H1 is the source's, verbatim; no do_not_name.
    out/<s>/<v>.md     exists only once every chapter has a draft; no
                       do_not_name.

One line per problem, `path: what is wrong`, and exit 1 if there were any.
grid.py reports; this gates. The voice Checklist is judgment and stays with
/retell; this is the part a script can hold. Stdlib only.
"""

import argparse
import os
import re
import sys

MD = ".md"
VOICE_FIELDS = ("name", "tagline", "era", "do_not_name")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def frontmatter(text):
    """Return (fields, body). Fields is {} when there is no frontmatter block."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    fields = {}
    for line in text[4:end].split("\n"):
        m = re.match(r"^([A-Za-z_][\w-]*):[ \t]*(.*?)[ \t]*$", line)
        if m:
            fields[m.group(1)] = m.group(2)
    return fields, text[end + 5:]


def pd_us(path):
    """Return pd_status.us from book.yaml as lower-case text, or None."""
    in_block = False
    for line in read(path).split("\n"):
        if re.match(r"^pd_status:\s*$", line):
            in_block = True
            continue
        if in_block:
            if not line.startswith((" ", "\t")):
                break
            m = re.match(r"^\s+us:\s*(\S+)", line)
            if m:
                return m.group(1).strip("\"'").lower()
    return None


def name_patterns(do_not_name):
    """Regexes that find the author in prose: the full name, then the surname.

    Case-insensitive, anchored at a word start only, so "Hemingway's" and
    "Hemingwayesque" are hits and "earnest" is not "Ernest".
    """
    name = do_not_name.strip().strip("\"'")
    if not name:
        return []
    patterns = [re.compile(r"\b" + re.escape(name), re.I)]
    words = name.split()
    if len(words) > 1:
        patterns.append(re.compile(r"\b" + re.escape(words[-1]), re.I))
    return patterns


def names_author(text, patterns):
    for p in patterns:
        m = p.search(text)
        if m:
            return m.group(0)
    return None


def first_h1(text):
    """The first non-blank line if it is an H1, else None."""
    for line in text.split("\n"):
        if line.strip():
            return line.strip() if line.startswith("# ") else None
    return None


def check_voices(root, problems):
    """Return {slug: patterns} for every real voice, reporting defects."""
    voices = {}
    base = os.path.join(root, "voices")
    if not os.path.isdir(base):
        return voices
    for fn in sorted(os.listdir(base)):
        if not fn.endswith(MD) or fn.startswith("_"):
            continue
        path = "voices/" + fn
        slug = fn[: -len(MD)]
        fields, body = frontmatter(read(os.path.join(base, fn)))
        for field in VOICE_FIELDS:
            if not fields.get(field):
                problems.append("%s: frontmatter lacks %s" % (path, field))
        if fields.get("name") and fields["name"] != slug:
            problems.append(
                "%s: name is '%s', the filename says '%s'" % (path, fields["name"], slug)
            )
        patterns = name_patterns(fields.get("do_not_name", ""))
        hit = names_author(body, patterns)
        if hit:
            problems.append("%s: names the author (%r)" % (path, hit))
        voices[slug] = patterns
    return voices


def check_sources(root, problems):
    """Return {slug: (chapter_files, pd_us)} for every source, reporting defects."""
    sources = {}
    base = os.path.join(root, "sources")
    if not os.path.isdir(base):
        return sources
    for slug in sorted(os.listdir(base)):
        chapters = os.path.join(base, slug, "chapters")
        if not os.path.isdir(chapters):
            continue
        files = sorted(f for f in os.listdir(chapters) if f.endswith(MD))
        for fn in files:
            if first_h1(read(os.path.join(chapters, fn))) is None:
                problems.append("sources/%s/chapters/%s: does not open on an H1" % (slug, fn))
        yaml = os.path.join(base, slug, "book.yaml")
        us = None
        if os.path.isfile(yaml):
            us = pd_us(yaml)
        else:
            problems.append("sources/%s/book.yaml: missing" % slug)
        sources[slug] = (files, us)
    return sources


def check_out(root, voices, sources, problems):
    """Check every draft and assembled book; return (drafts, assembled) counts."""
    drafts = assembled = 0
    base = os.path.join(root, "out")
    if not os.path.isdir(base):
        return drafts, assembled
    for slug in sorted(os.listdir(base)):
        sdir = os.path.join(base, slug)
        if not os.path.isdir(sdir):
            continue
        if slug not in sources:
            problems.append("out/%s: no source '%s'" % (slug, slug))
            continue
        files, us = sources[slug]
        if us != "true":
            problems.append(
                "out/%s: pd_status.us is not true in sources/%s/book.yaml -- "
                "nothing may be generated from it" % (slug, slug)
            )
        for entry in sorted(os.listdir(sdir)):
            epath = os.path.join(sdir, entry)
            if os.path.isdir(epath):
                voice = entry
                vpath = "out/%s/%s" % (slug, voice)
                if voice not in voices:
                    problems.append("%s: no voice '%s'" % (vpath, voice))
                    continue
                for fn in sorted(f for f in os.listdir(epath) if f.endswith(MD)):
                    drafts += 1
                    dpath = "%s/%s" % (vpath, fn)
                    text = read(os.path.join(epath, fn))
                    if fn not in files:
                        problems.append("%s: no source chapter %s" % (dpath, fn))
                    else:
                        want = first_h1(read(os.path.join(root, "sources", slug, "chapters", fn)))
                        have = first_h1(text)
                        if have is None:
                            problems.append("%s: does not open on an H1" % dpath)
                        elif have != want:
                            problems.append(
                                "%s: H1 differs from source (%r, source has %r)" % (dpath, have, want)
                            )
                    hit = names_author(text, voices[voice])
                    if hit:
                        problems.append("%s: names the author (%r)" % (dpath, hit))
            elif entry.endswith(MD):
                assembled += 1
                voice = entry[: -len(MD)]
                apath = "out/%s/%s" % (slug, entry)
                if voice not in voices:
                    problems.append("%s: no voice '%s'" % (apath, voice))
                    continue
                ddir = os.path.join(sdir, voice)
                done = []
                if os.path.isdir(ddir):
                    done = [f for f in os.listdir(ddir) if f in files]
                if len(done) < len(files):
                    problems.append(
                        "%s: assembled with %d of %d chapters drafted"
                        % (apath, len(done), len(files))
                    )
                hit = names_author(read(epath), voices[voice])
                if hit:
                    problems.append("%s: names the author (%r)" % (apath, hit))
    return drafts, assembled


def inspect(root):
    """Return (problems, (voices, sources, drafts, assembled))."""
    problems = []
    voices = check_voices(root, problems)
    sources = check_sources(root, problems)
    drafts, assembled = check_out(root, voices, sources, problems)
    return problems, (len(voices), len(sources), drafts, assembled)


def run(root):
    """Return the list of problems, one `path: what is wrong` line each."""
    return inspect(root)[0]


def main(argv=None):
    p = argparse.ArgumentParser(description="The gate: exit 1 on anything a script can prove wrong.")
    p.add_argument("--root", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    args = p.parse_args(argv)
    root = os.path.normpath(args.root)

    problems, counts = inspect(root)
    for line in problems:
        print(line)
    if problems:
        print("%d problem%s" % (len(problems), "" if len(problems) == 1 else "s"))
        return 1
    print("ok: %d voices, %d sources, %d drafts, %d assembled" % counts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
