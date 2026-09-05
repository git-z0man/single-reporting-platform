#!/usr/bin/env python3
"""Extract a canonical plain-text rendering of a Commission CRA FAQ PDF.

The output is deterministic and whitespace-normalised so that two versions can
be diffed with tools/diff_versions.py.  It is NOT meant to be a faithful
reproduction of the PDF layout -- it exists purely so that change detection
runs against a stable text form that lives in git.

Requires pypdf.  The system Python in some environments ships a broken
`cryptography` build that pypdf imports; if `import pypdf` fails, create a
throwaway venv:

    python3 -m venv .venv && .venv/bin/pip install pypdf
    .venv/bin/python commission-faq/tools/extract_text.py in.pdf out.txt

Usage:
    extract_text.py <input.pdf> [output.txt]
"""

import re
import sys

# A line that is nothing but a page number: dropped, because page numbering
# shifts whenever a section is added and would otherwise swamp every diff.
PAGE_NUMBER_ONLY = re.compile(r"^\d{1,3}$")


def canonicalise(raw: str) -> str:
    """Normalise extracted PDF text into stable, diffable lines."""
    # Typographic characters vary between PDF producers; fold them.
    for src, dst in (
        ("’", "'"), ("‘", "'"),
        ("“", '"'), ("”", '"'),
        ("–", "-"), ("—", "-"),
        ("…", "..."), (" ", " "),
    ):
        raw = raw.replace(src, dst)

    out = []
    for line in raw.splitlines():
        line = re.sub(r"[ \t]+", " ", line).strip()
        if not line or PAGE_NUMBER_ONLY.match(line):
            continue
        # Table-of-contents dot leaders carry no information and are extracted
        # inconsistently; collapse them to a single marker.
        line = re.sub(r"\.\s*(?:\.\s*){3,}", " ... ", line)
        out.append(line)
    return "\n".join(out) + "\n"


def main(argv):
    if not 2 <= len(argv) <= 3:
        sys.exit(__doc__)

    try:
        from pypdf import PdfReader
    except Exception as exc:  # noqa: BLE001 - report the real cause to the user
        sys.exit(f"cannot import pypdf ({exc}); see the module docstring")

    reader = PdfReader(argv[1])
    raw = "\n".join((page.extract_text() or "") for page in reader.pages)
    text = canonicalise(raw)

    if len(argv) == 3:
        with open(argv[2], "w", encoding="utf-8") as handle:
            handle.write(text)
        print(f"{argv[2]}: {len(reader.pages)} pages, {text.count(chr(10))} lines")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main(sys.argv)
