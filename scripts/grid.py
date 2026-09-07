#!/usr/bin/env python3
"""
grid.py -- print the source x voice matrix.

    python3 scripts/grid.py
    python3 scripts/grid.py --root .

Rows are sources, columns are voices, and a cell is one retelling:

    done   out/<source>/<voice>.md exists -- the cell is assembled
    N/M    N of M chapters drafted in out/<source>/<voice>/
    .      nothing yet

Voice files whose name begins with an underscore (voices/_template.md) are
templates, not voices, and get no column.

Stdlib only. Always exits 0 -- this reports, it does not gate.
"""

import argparse
import os
import sys

CH_SUFFIX = ".md"


def words(path):
    try:
        with open(path, encoding="utf-8") as f:
            return len(f.read().split())
    except OSError:
        return 0


def plural(n, noun):
    return "%d %s%s" % (n, noun, "" if n == 1 else "s")


def list_sources(root):
    base = os.path.join(root, "sources")
    if not os.path.isdir(base):
        return []
    out = []
    for slug in sorted(os.listdir(base)):
        chapters = os.path.join(base, slug, "chapters")
        if not os.path.isdir(chapters):
            continue
        files = sorted(f for f in os.listdir(chapters) if f.endswith(CH_SUFFIX))
        out.append((slug, files, sum(words(os.path.join(chapters, f)) for f in files)))
    return out


def list_voices(root):
    base = os.path.join(root, "voices")
    if not os.path.isdir(base):
        return []
    return sorted(
        f[: -len(CH_SUFFIX)]
        for f in os.listdir(base)
        if f.endswith(CH_SUFFIX) and not f.startswith("_")
    )


def cell(root, source, voice, chapter_count):
    """Return (label, words_written) for one cell."""
    assembled = os.path.join(root, "out", source, voice + CH_SUFFIX)
    drafts = os.path.join(root, "out", source, voice)
    draft_files = []
    if os.path.isdir(drafts):
        draft_files = sorted(f for f in os.listdir(drafts) if f.endswith(CH_SUFFIX))
    written = sum(words(os.path.join(drafts, f)) for f in draft_files)
    if os.path.isfile(assembled):
        return "done", max(written, words(assembled))
    if draft_files:
        return "%d/%d" % (len(draft_files), chapter_count), written
    return ".", 0


def main():
    p = argparse.ArgumentParser(description="Print the source x voice matrix.")
    p.add_argument("--root", default=os.path.join(os.path.dirname(__file__), ".."))
    args = p.parse_args()
    root = os.path.normpath(args.root)

    sources = list_sources(root)
    voices = list_voices(root)

    if not sources or not voices:
        print("%s, %s -- nothing to grid yet." % (plural(len(sources), "source"), plural(len(voices), "voice")))
        return 0

    rows = []
    done = started = retold = 0
    for slug, files, source_words in sources:
        cells = []
        for voice in voices:
            label, written = cell(root, slug, voice, len(files))
            retold += written
            if label == "done":
                done += 1
                started += 1
            elif label != ".":
                started += 1
            cells.append(label)
        rows.append((slug, len(files), source_words, cells))

    name_w = max([len("source")] + [len(r[0]) for r in rows])
    col_w = [max([len(v)] + [len(r[3][i]) for r in rows]) for i, v in enumerate(voices)]

    header = "%-*s  %3s  %8s  " % (name_w, "source", "ch", "words")
    header += "  ".join("%-*s" % (col_w[i], v) for i, v in enumerate(voices))
    print(header)
    print("-" * len(header.rstrip()))
    for slug, n, source_words, cells in rows:
        line = "%-*s  %3d  %8s  " % (name_w, slug, n, "{:,}".format(source_words))
        line += "  ".join("%-*s" % (col_w[i], c) for i, c in enumerate(cells))
        print(line.rstrip())
    print("-" * len(header.rstrip()))

    total_cells = len(sources) * len(voices)
    source_words = sum(r[2] for r in rows)
    print(
        "%s (%s x %s): %d done, %d started, %d empty"
        % (plural(total_cells, "cell"), plural(len(sources), "source"),
           plural(len(voices), "voice"), done, started - done, total_cells - started)
    )
    print("source words: {:,}   retold words: {:,}".format(source_words, retold))
    return 0


if __name__ == "__main__":
    sys.exit(main())
