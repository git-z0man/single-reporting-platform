#!/usr/bin/env python3
"""Render a visual side-by-side diff of two Commission CRA FAQ versions.

Produces a self-contained HTML page -- no external CSS, JS, fonts or images --
so it can be committed to the repository and served straight from GitHub Pages.

This is the visual layer that a commercial comparison service would otherwise
provide. It reuses the matching strategy of diff_versions.py: sentences are
aligned on their whitespace-stripped form, because PDF text extraction inserts
spurious spaces inside words ("expres sed") and those artefacts differ between
two renderings of an unchanged sentence. Within a changed pair, a word-level
diff highlights exactly what moved.

Usage:
    render_diff.py <old.txt> <new.txt> <out.html>
        [--old-label "v1.3 (01/07/2026)"] [--new-label "v1.4 (04/09/2026)"]
        [--context N]   sentences of unchanged context around each change (default 2)
        [--full]        include the whole document, not just changed regions
"""

import argparse
import difflib
import glob
import html
import os
import re
import sys
from datetime import date

SENTENCE_SPLIT = re.compile(r"(?<=[.?!:])\s+")
WHITESPACE = re.compile(r"\s+")
SPACE_BEFORE_PUNCT = re.compile(r"\s+([.,;:!?)])")

STYLE = """
:root{
  --bg:#eef1f4; --card:#ffffff; --card-alt:#f5f7f9; --hairline:#e2e7ec;
  --ink:#16191d; --body:#5e666f; --muted:#6b727b; --faint:#8b939c;
  --accent:#16636b; --accent-tint:#eef4f4;
  --chg-bg:#fafbfc; --chg-rule:#d8dee4;
  --del-bg:#fdecec; --del-mark:#f7c9c9; --del-ink:#8a2020;
  --ins-bg:#e9f6ec; --ins-mark:#bfe6c8; --ins-ink:#14612c;
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#14171a; --card:#1c2024; --card-alt:#20252a; --hairline:#2c3238;
    --ink:#e8ecef; --body:#aab3bc; --muted:#98a1aa; --faint:#79828b;
    --accent:#5fb3ba; --accent-tint:#18292b;
    --chg-bg:#1f242a; --chg-rule:#39414a;
    --del-bg:#2e1a1a; --del-mark:#5e2a2a; --del-ink:#f0a9a9;
    --ins-bg:#16281c; --ins-mark:#28532f; --ins-ink:#9adcaa;
  }
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.6 'IBM Plex Sans',system-ui,-apple-system,sans-serif;}
.wrap{max-width:1400px;margin:0 auto;padding:32px 24px 80px}
header{margin-bottom:28px}
h1{font-size:24px;font-weight:600;margin:0 0 6px;letter-spacing:-.01em}
.sub{color:var(--muted);font-size:14px;margin:0 0 18px}
.sub a{color:var(--accent)}
.stats{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 8px;padding:0;list-style:none}
.stats li{background:var(--card);border:1px solid var(--hairline);border-radius:7px;
  padding:7px 13px;font-size:13px;color:var(--body)}
.stats b{color:var(--ink);font-weight:600}
.note{background:var(--accent-tint);border:1px solid var(--hairline);border-radius:8px;
  padding:12px 16px;font-size:13px;color:var(--body);margin:16px 0 0}
.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:13px;color:var(--muted);margin:14px 0 0}
.legend span{display:inline-flex;align-items:center;gap:6px}
.swatch{width:13px;height:13px;border-radius:3px;display:inline-block}
.swatch.del{background:var(--del-mark)} .swatch.ins{background:var(--ins-mark)}
table{width:100%;border-collapse:collapse;margin-top:24px;background:var(--card);
  border:1px solid var(--hairline);border-radius:10px;overflow:hidden;table-layout:fixed}
thead th{background:var(--card-alt);border-bottom:1px solid var(--hairline);
  padding:11px 16px;text-align:left;font-size:13px;font-weight:600;color:var(--body);width:50%}
td{padding:9px 16px;vertical-align:top;border-bottom:1px solid var(--hairline);
  font-size:14px;line-height:1.62;word-wrap:break-word;overflow-wrap:break-word}
tr:last-child td{border-bottom:none}
td.ctx{color:var(--faint);background:transparent}
td.del{background:var(--del-bg);color:var(--del-ink)}
td.ins{background:var(--ins-bg);color:var(--ins-ink)}
td.chg{background:var(--chg-bg);border-left:3px solid var(--chg-rule)}
td.chg.l{border-left-color:var(--del-mark)} td.chg.r{border-left-color:var(--ins-mark)}
td.empty{background:var(--card-alt)}
mark.del{background:var(--del-mark);color:inherit;padding:1px 2px;border-radius:2px;
  text-decoration:line-through;text-decoration-thickness:1px}
mark.ins{background:var(--ins-mark);color:inherit;padding:1px 2px;border-radius:2px}
tr.gap td{background:var(--card-alt);color:var(--faint);font-size:12px;text-align:center;
  padding:5px;letter-spacing:.04em}
footer{margin-top:32px;color:var(--faint);font-size:12px;line-height:1.7}
footer a{color:var(--accent)}
@media (max-width:820px){
  thead{display:none}
  table,tbody,tr,td{display:block;width:100%}
  td.empty{display:none}
  tr{border-bottom:1px solid var(--hairline)}
  td{border-bottom:none}
}
"""


def load(path):
    """Read a version file and split it into comparable sentences."""
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    for src, dst in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
                     ("–", "-"), ("—", "-"), ("…", "..."), (" ", " ")):
        text = text.replace(src, dst)
    text = WHITESPACE.sub(" ", text)
    # See diff_versions.py: PDF extraction inconsistently places a spurious
    # space before punctuation between renderings of the same sentence, which
    # shifts sentence-split points and produces a false "changed" pair.
    text = SPACE_BEFORE_PUNCT.sub(r"\1", text)
    text = re.sub(r"\.\s*(?:\.\s*){3,}", " ... ", text)
    return [s.strip() for s in SENTENCE_SPLIT.split(text) if s.strip()]


def key(sentence):
    """Matching key: no whitespace, no case -- immune to extraction artefacts."""
    return WHITESPACE.sub("", sentence).lower()


def word_diff(old, new):
    """Highlight word-level changes inside a modified sentence pair."""
    old_words = old.split(" ")
    new_words = new.split(" ")
    matcher = difflib.SequenceMatcher(
        None,
        [w.lower().strip(".,;:()") for w in old_words],
        [w.lower().strip(".,;:()") for w in new_words],
        autojunk=False,
    )
    left, right = [], []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        old_run = html.escape(" ".join(old_words[i1:i2]))
        new_run = html.escape(" ".join(new_words[j1:j2]))
        if tag == "equal":
            left.append(old_run)
            right.append(new_run)
        else:
            if old_run:
                left.append(f'<mark class="del">{old_run}</mark>')
            if new_run:
                right.append(f'<mark class="ins">{new_run}</mark>')
    return " ".join(left), " ".join(right)


def build_rows(old, new, context, full):
    """Walk the opcodes and emit (kind, left_html, right_html) rows."""
    matcher = difflib.SequenceMatcher(
        None, [key(s) for s in old], [key(s) for s in new], autojunk=False
    )
    opcodes = matcher.get_opcodes()
    rows = []
    counts = {"insert": 0, "delete": 0, "replace": 0}

    for index, (tag, i1, i2, j1, j2) in enumerate(opcodes):
        if tag == "equal":
            span = i2 - i1
            if full:
                # Emit the whole block once, as leading context; the trailing
                # loop must stay empty or every sentence would appear twice.
                head, tail = span, 0
            else:
                # Keep a little context either side of a change, elide the rest.
                first = index == 0
                last = index == len(opcodes) - 1
                head = 0 if first else min(context, span)
                tail = 0 if last else min(context, span - head)
            for offset in range(head):
                text = html.escape(old[i1 + offset])
                rows.append(("ctx", text, text))
            hidden = span - head - tail
            if hidden > 0 and not full:
                rows.append(("gap", f"{hidden} unchanged sentences", ""))
            for offset in range(span - tail, span):
                text = html.escape(old[i1 + offset])
                rows.append(("ctx", text, text))
            continue

        counts[tag] += 1
        if tag == "replace" and (i2 - i1) == (j2 - j1):
            # Same number of sentences on both sides: pair them up and do a
            # word-level diff, which is far more readable than two blocks.
            for offset in range(i2 - i1):
                left, right = word_diff(old[i1 + offset], new[j1 + offset])
                rows.append(("change", left, right))
        else:
            for sentence in old[i1:i2]:
                rows.append(("del", html.escape(sentence), ""))
            for sentence in new[j1:j2]:
                rows.append(("ins", "", html.escape(sentence)))

    return rows, counts


def render(rows, counts, old_label, new_label, old_count, new_count, full):
    parts = []
    for kind, left, right in rows:
        if kind == "gap":
            parts.append(f'<tr class="gap"><td colspan="2">{left}</td></tr>')
        elif kind == "ctx":
            parts.append(f'<tr><td class="ctx">{left}</td><td class="ctx">{right}</td></tr>')
        elif kind == "change":
            parts.append(f'<tr><td class="chg l">{left}</td><td class="chg r">{right}</td></tr>')
        elif kind == "del":
            parts.append(f'<tr><td class="del">{left}</td><td class="empty"></td></tr>')
        else:
            parts.append(f'<tr><td class="empty"></td><td class="ins">{right}</td></tr>')

    scope = "full document" if full else "changed passages with surrounding context"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CRA FAQ {html.escape(old_label)} → {html.escape(new_label)}</title>
<style>{STYLE}</style></head><body><div class="wrap">
<header>
<h1>FAQs on the Cyber Resilience Act</h1>
<p class="sub">{html.escape(old_label)} &rarr; {html.escape(new_label)} &middot;
generated {date.today().isoformat()} &middot;
<a href="https://digital-strategy.ec.europa.eu/en/library/cyber-resilience-act-implementation-frequently-asked-questions">source</a></p>
<ul class="stats">
<li><b>{counts['replace']}</b> modified</li>
<li><b>{counts['insert']}</b> inserted</li>
<li><b>{counts['delete']}</b> deleted</li>
<li>{old_count} &rarr; {new_count} sentences</li>
</ul>
<div class="legend">
<span><i class="swatch del"></i> removed in {html.escape(new_label)}</span>
<span><i class="swatch ins"></i> added in {html.escape(new_label)}</span>
</div>
<p class="note">Showing {scope}. Sentences are matched with all whitespace
removed, so spurious spaces from PDF text extraction do not show up as
changes. Text is extracted from the published PDFs and normalised for
comparison; it is not a facsimile of the original layout. For the authoritative
wording, read the PDFs themselves.</p>
</header>
<table>
<thead><tr><th>{html.escape(old_label)}</th><th>{html.escape(new_label)}</th></tr></thead>
<tbody>
{chr(10).join(parts)}
</tbody></table>
<footer>
<p>&copy; European Union, 2025. The FAQ is reusable under
<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> per Commission
Decision 2011/833/EU. This comparison is generated from unmodified archived copies.</p>
<p>The FAQ is prepared by Commission services and is not an official position of the
European Commission. This page is not legal advice.</p>
</footer>
</div></body></html>
"""


def write_index(diff_dir):
    """Regenerate the comparison index by globbing the diff directory.

    Called after every render so the index can never go stale: whatever HTML
    comparisons exist on disk are exactly what the index lists.
    """
    pages = sorted(
        (os.path.basename(f) for f in glob.glob(os.path.join(diff_dir, "v*-v*.html"))),
        key=lambda n: [
            [int(part) for part in v.lstrip("v").split(".")]
            for v in n[:-5].split("-")
        ],
    )
    if not pages:
        return

    items = []
    for name in pages:
        old, new = name[:-5].split("-")
        items.append(
            f'<li><a href="{html.escape(name)}">'
            f"<b>{html.escape(old)} &rarr; {html.escape(new)}</b>"
            f"<span>side-by-side comparison</span></a></li>"
        )

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CRA FAQ version comparisons</title>
<style>{STYLE}
ul.idx{{list-style:none;padding:0;margin:24px 0 0;display:grid;gap:10px;
  grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}}
ul.idx a{{display:flex;flex-direction:column;gap:3px;background:var(--card);
  border:1px solid var(--hairline);border-radius:9px;padding:15px 17px;
  text-decoration:none;color:var(--ink)}}
ul.idx a:hover{{border-color:var(--accent)}}
ul.idx span{{color:var(--muted);font-size:13px}}
</style></head><body><div class="wrap">
<header>
<h1>FAQs on the Cyber Resilience Act</h1>
<p class="sub">Version comparisons &middot; generated {date.today().isoformat()} &middot;
<a href="https://digital-strategy.ec.europa.eu/en/library/cyber-resilience-act-implementation-frequently-asked-questions">source</a></p>
<p class="note">Each page shows what changed between two released versions of the
Commission's CRA FAQ, generated from the archived copies in this repository.
Version 1.1 was never captured, so its edits appear inside the v1.0 &rarr; v1.2
comparison.</p>
</header>
<ul class="idx">
{chr(10).join(items)}
</ul>
<footer>
<p>&copy; European Union, 2025. Reusable under
<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> per Commission
Decision 2011/833/EU. Comparisons are generated from unmodified archived copies.</p>
<p>The FAQ is prepared by Commission services and is not an official position of the
European Commission. Not legal advice.</p>
</footer>
</div></body></html>
"""
    with open(os.path.join(diff_dir, "index.html"), "w", encoding="utf-8") as handle:
        handle.write(page)
    print(f"{os.path.join(diff_dir, 'index.html')}: {len(pages)} comparison(s) indexed")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("old")
    parser.add_argument("new")
    parser.add_argument("out")
    parser.add_argument("--old-label", default=None)
    parser.add_argument("--new-label", default=None)
    parser.add_argument("--context", type=int, default=2)
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()

    old, new = load(args.old), load(args.new)
    old_label = args.old_label or args.old.rsplit("/", 1)[-1]
    new_label = args.new_label or args.new.rsplit("/", 1)[-1]

    rows, counts = build_rows(old, new, args.context, args.full)
    page = render(rows, counts, old_label, new_label, len(old), len(new), args.full)

    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write(page)

    write_index(os.path.dirname(args.out) or ".")

    total = counts["replace"] + counts["insert"] + counts["delete"]
    print(f"{args.out}: {total} change block(s) "
          f"({counts['replace']} modified, {counts['insert']} inserted, "
          f"{counts['delete']} deleted), {len(page)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
