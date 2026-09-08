#!/usr/bin/env python3
"""Substantive diff between two Commission CRA FAQ versions.

PDF text extraction sprays spurious spaces inside words ("expres sed" for
"expressed") and those artefacts differ between two renderings of the *same*
sentence.  A plain `diff` therefore reports dozens of changes that are not
changes at all.  This tool matches sentences with all whitespace removed, so
only genuine wording differences survive, and prints them in readable form.

Works on the canonical text produced by extract_text.py and on the Markdown
renderings the Commission publishes alongside the PDF.

Usage:
    diff_versions.py <old> <new> [--context]

Exit status is 1 when substantive differences were found, 0 when there are
none, so a monitoring run can branch on it.
"""

import difflib
import re
import sys

SENTENCE_SPLIT = re.compile(r"(?<=[.?!:])\s+")
WHITESPACE = re.compile(r"\s+")
SPACE_BEFORE_PUNCT = re.compile(r"\s+([.,;:!?)])")


def load(path: str) -> list:
    """Read a version file and split it into comparable sentences."""
    with open(path, encoding="utf-8") as handle:
        text = handle.read()

    for src, dst in (
        ("’", "'"), ("‘", "'"),
        ("“", '"'), ("”", '"'),
        ("–", "-"), ("—", "-"),
        ("…", "..."), (" ", " "),
    ):
        text = text.replace(src, dst)

    text = WHITESPACE.sub(" ", text)
    # PDF extraction places a spurious space before punctuation inconsistently
    # between renderings of the same sentence (e.g. "period ?," in one version,
    # "period? ," in the next). Left alone, that shifts where SENTENCE_SPLIT
    # breaks the sentence and produces a false "changed" pair. Stripping it
    # before splitting keeps identical wording aligned regardless of which
    # version the spurious space landed in.
    text = SPACE_BEFORE_PUNCT.sub(r"\1", text)
    text = re.sub(r"\.\s*(?:\.\s*){3,}", " ... ", text)
    return [s.strip() for s in SENTENCE_SPLIT.split(text) if s.strip()]


def key(sentence: str) -> str:
    """Matching key: no whitespace, no case -- immune to extraction artefacts."""
    return WHITESPACE.sub("", sentence).lower()


def main(argv):
    if not 3 <= len(argv) <= 4:
        sys.exit(__doc__)

    old, new = load(argv[1]), load(argv[2])
    show_context = "--context" in argv

    matcher = difflib.SequenceMatcher(
        None, [key(s) for s in old], [key(s) for s in new], autojunk=False
    )

    changed = False
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        changed = True
        print(f"\n--- {tag.upper()} (old {i1}:{i2} -> new {j1}:{j2}) ---")
        for sentence in old[i1:i2]:
            print(f"  - {sentence}")
        for sentence in new[j1:j2]:
            print(f"  + {sentence}")
        if show_context and i1 > 0:
            print(f"    context before: {old[i1 - 1][:120]}")

    if not changed:
        print("No substantive differences.")
    return 1 if changed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
