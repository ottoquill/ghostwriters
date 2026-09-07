#!/usr/bin/env python3
"""
fetch.py -- turn a Project Gutenberg ebook id into a source book under sources/.

    python3 scripts/fetch.py 67098 winnie-the-pooh
    python3 scripts/fetch.py 67098 winnie-the-pooh --uk-pd
    python3 scripts/fetch.py 67098 winnie-the-pooh --dry-run

It downloads the plain-text UTF-8 edition, cuts the Project Gutenberg header and
footer, splits the remainder on chapter headings, and writes

    sources/<slug>/book.yaml
    sources/<slug>/chapters/NN.md      one file per chapter, heading as an H1

Chapter text is written verbatim. The only changes made to it are the removal of
trailing whitespace, the collapsing of runs of blank lines, the removal of
bracketed transcriber's notes, and -- in the final chapter only -- the removal of
a trailing centred printer's colophon. Nothing is reflowed and no word is changed.

Headings recognised (the line must stand alone, preceded by a blank line):

    CHAPTER I            CHAPTER 1          Chapter One
    CHAPTER I: IN WHICH ...                 CHAPTER XIV.--THE SIEGE
    CHAPTER I                               ... followed by an all-capitals
    IN WHICH POOH GOES VISITING                 subtitle block, which is folded
    AND GETS INTO A TIGHT PLACE                 into the heading.

pd_status is NOT determined by this script. It is written as a default -- US
true, UK false -- and must be checked by hand before anything is generated from
the source. See .claude/CLAUDE.md.

Stdlib only. Python 3.8+.
"""

import argparse
import os
import re
import sys
import urllib.error
import urllib.request

UA = "ghostwriters-fetch/1.0 (+https://github.com/ottoquill/ghostwriters)"

# Tried in order. The first is the canonical redirect; the others are the cache
# layouts Gutenberg has used over the years, for ids the redirect does not cover.
URL_TEMPLATES = [
    "https://www.gutenberg.org/ebooks/{id}.txt.utf-8",
    "https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt",
    "https://www.gutenberg.org/files/{id}/{id}-0.txt",
    "https://www.gutenberg.org/files/{id}/{id}.txt",
]

START_RE = re.compile(r"^\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*$", re.M)
END_RE = re.compile(r"^\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*$", re.M)

NUMBER_WORDS = {
    w: i + 1
    for i, w in enumerate(
        "one two three four five six seven eight nine ten eleven twelve "
        "thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty "
        "twentyone twentytwo twentythree twentyfour twentyfive".split()
    )
}
ROMAN_VALUES = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100, "d": 500, "m": 1000}

CHAPTER_RE = re.compile(
    r"^[ \t]*(?P<kw>CHAPTER|Chapter|CHAP\.|Chap\.)[ \t]+"
    r"(?P<num>[A-Za-z0-9]+(?:[ \t]*-[ \t]*[A-Za-z]+)?)"
    r"[ \t]*(?P<sep>[:.–—-]{0,3})[ \t]*"
    r"(?P<rest>.*?)[ \t]*$"
)

TRANSCRIBER_RE = re.compile(r"\[\s*Transcriber'?s? Note.*?\]", re.S | re.I)


def roman_to_int(s):
    """Return the value of a roman numeral, or None if s is not one."""
    s = s.lower()
    if not s or any(c not in ROMAN_VALUES for c in s):
        return None
    total, prev = 0, 0
    for c in reversed(s):
        v = ROMAN_VALUES[c]
        total += v if v >= prev else -v
        prev = max(prev, v)
    return total or None


def parse_number(token):
    """Return the integer a chapter-number token denotes, or None."""
    t = token.strip().rstrip(".")
    if not t:
        return None
    if t.isdigit():
        return int(t)
    word = re.sub(r"[^a-z]", "", t.lower())
    if word in NUMBER_WORDS:
        return NUMBER_WORDS[word]
    return roman_to_int(t)


def download(book_id):
    last = None
    for template in URL_TEMPLATES:
        url = template.format(id=book_id)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                raw = r.read()
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            last = "%s: %s" % (url, e)
            continue
        return url, raw.decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "\n")
    raise SystemExit("fetch failed for ebook %s (last: %s)" % (book_id, last))


def read_metadata(text):
    """Pull Title/Author/year out of the Gutenberg header block."""
    head = text[: text.find("*** START") + 1] or text[:6000]
    meta = {}
    for field in ("Title", "Author", "Illustrator", "Release date", "Original publication"):
        m = re.search(r"^%s:[ \t]*(.+)$" % re.escape(field), head, re.M)
        if m:
            meta[field] = m.group(1).strip()
    year = None
    for field in ("Original publication", "Release date"):
        if field in meta:
            years = re.findall(r"\b(1[0-9]{3}|20[0-9]{2})\b", meta[field])
            if years:
                year = int(years[-1])
                break
    meta["year"] = year
    return meta


def strip_wrapper(text):
    """Cut everything outside the START/END markers.

    Gutenberg repeats the START marker after the licence blurb, so the last one
    wins; the first END marker wins.
    """
    starts = list(START_RE.finditer(text))
    body = text[starts[-1].end():] if starts else text
    end = END_RE.search(body)
    if end:
        body = body[: end.start()]
    return body


def tidy(block, last_chapter=False):
    block = TRANSCRIBER_RE.sub("", block)
    lines = [ln.rstrip() for ln in block.split("\n")]
    if last_chapter:
        # Drop a trailing centred colophon ("Printed in Canada / by ...").
        while lines and not lines[-1]:
            lines.pop()
        tail = []
        while lines and lines[-1] and len(lines[-1]) - len(lines[-1].lstrip()) >= 12:
            tail.append(lines.pop())
        if tail:
            while lines and not lines[-1]:
                lines.pop()
    out, blanks = [], 0
    for ln in lines:
        if ln:
            blanks = 0
            out.append(ln)
        else:
            blanks += 1
            if blanks <= 1:
                out.append("")
    return "\n".join(out).strip("\n")


def is_subtitle(text):
    """Is this all-capitals block a chapter subtitle rather than the first line of prose?

    A subtitle is set in capitals, runs to at least two words, and does not close
    like a sentence. The last test is what keeps a chapter opening on a short
    shouted line ("A.", "NO!") from being swallowed into the heading.
    """
    if len(text) < 8 or len(text.split()) < 2:
        return False
    if text != text.upper() or not re.search(r"[A-Z]", text):
        return False
    return text[-1] not in '.!?"\u201d'


def find_headings(lines):
    """Return [(line_index, heading_text, consumed_through_index), ...]."""
    found = []
    for i, line in enumerate(lines):
        if i and lines[i - 1].strip():
            continue  # a heading stands alone, after a blank line
        m = CHAPTER_RE.match(line)
        if not m or parse_number(m.group("num")) is None:
            continue
        num_token = m.group("num").strip()
        rest = m.group("rest").strip()
        consumed = i
        if not rest:
            # Look ahead past blank lines for an all-capitals subtitle block.
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            run = []
            k = j
            while k < len(lines) and lines[k].strip():
                run.append(lines[k].strip())
                k += 1
            joined = re.sub(r"\s+", " ", " ".join(run))
            if is_subtitle(joined):
                rest = joined
                consumed = k - 1
        heading = "%s %s" % (m.group("kw").rstrip("."), num_token)
        if rest:
            heading = "%s: %s" % (heading, rest)
        found.append((i, heading, consumed))
    return found


def split_chapters(body):
    lines = body.split("\n")
    heads = find_headings(lines)
    chapters = []
    for n, (start, heading, consumed) in enumerate(heads):
        stop = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        text = tidy("\n".join(lines[consumed + 1: stop]), last_chapter=(n == len(heads) - 1))
        chapters.append((heading, text))
    return chapters


def yaml_str(value):
    if value is None:
        return "null"
    s = str(value)
    return '"%s"' % s.replace("\\", "\\\\").replace('"', '\\"')


def write_book_yaml(path, slug, meta, book_id, url, chapter_count, uk_pd):
    lines = [
        "# Written by scripts/fetch.py. pd_status is a DEFAULT, not a finding --",
        "# check it by hand before generating anything from this source.",
        "title: %s" % yaml_str(meta.get("Title") or slug),
        "author: %s" % yaml_str(meta.get("Author")),
        "year: %s" % (meta["year"] if meta.get("year") else "null"),
        "gutenberg_id: %d" % book_id,
        "pd_status:",
        "  us: true",
        "  uk: %s" % ("true" if uk_pd else "false"),
        "notes: %s"
        % yaml_str(
            "%d chapters, fetched from %s. Distributed by Project Gutenberg, "
            "which publishes only works in the US public domain. UK status "
            "defaults to false and must be confirmed against the author's death "
            "date before any UK-facing use." % (chapter_count, url)
        ),
    ]
    if meta.get("Illustrator"):
        lines.insert(4, "illustrator: %s" % yaml_str(meta["Illustrator"]))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    p = argparse.ArgumentParser(description="Fetch a Gutenberg ebook into sources/<slug>/.")
    p.add_argument("gutenberg_id", type=int)
    p.add_argument("slug")
    p.add_argument("--root", default=".", help="repository root (default: .)")
    p.add_argument("--uk-pd", action="store_true", help="record pd_status.uk as true")
    p.add_argument("--dry-run", action="store_true", help="report chapters, write nothing")
    args = p.parse_args()

    url, text = download(args.gutenberg_id)
    meta = read_metadata(text)
    chapters = split_chapters(strip_wrapper(text))

    if not chapters:
        raise SystemExit(
            "no chapter headings found in %s -- add the heading form to CHAPTER_RE" % url
        )

    print("%s -- %s (%s)" % (meta.get("Title", "?"), meta.get("Author", "?"), meta.get("year", "?")))
    for i, (heading, body) in enumerate(chapters, 1):
        print("  %02d  %-6d words  %s" % (i, len(body.split()), heading[:70]))

    if args.dry_run:
        print("%d chapters (dry run, nothing written)" % len(chapters))
        return

    base = os.path.join(args.root, "sources", args.slug)
    os.makedirs(os.path.join(base, "chapters"), exist_ok=True)
    for i, (heading, body) in enumerate(chapters, 1):
        with open(os.path.join(base, "chapters", "%02d.md" % i), "w", encoding="utf-8") as f:
            f.write("# %s\n\n%s\n" % (heading, body))
    write_book_yaml(
        os.path.join(base, "book.yaml"), args.slug, meta, args.gutenberg_id, url,
        len(chapters), args.uk_pd,
    )
    print("%d chapters -> %s" % (len(chapters), os.path.join(base, "chapters")))


if __name__ == "__main__":
    sys.exit(main())
