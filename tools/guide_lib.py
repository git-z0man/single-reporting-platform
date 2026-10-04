"""Shared parsing for the guide tools. Standard library only.

Two kinds of function live here:
  * parsers for ENISA's live pages (FAQ, Glossary) -> small JSON-able dicts;
  * helpers to compare text by its words, so cosmetic markup churn is invisible.

Parsers raise ParseError rather than guess. A tool that guesses at a page it does
not understand writes plausible nonsense into a public guide.
"""
import html
import json
import re


class ParseError(Exception):
    pass


# --------------------------------------------------------------------- text
def words(s):
    """Lower-case alphanumeric words of a string or HTML fragment.

    Quotes, dashes, nbsp, markup and punctuation are ignored on purpose: two
    texts with the same words are the same wording for our purposes.
    """
    s = html.unescape(re.sub(r"<[^>]+>", " ", s)).replace("\xa0", " ")
    s = (s.lower().replace("’", "'").replace("‘", "'")
         .replace("“", '"').replace("”", '"')
         .replace("–", "-").replace("—", "-").replace(" ", ""))
    return re.findall(r"[a-z0-9]+", s)


def hrefs(s):
    """The link targets in an HTML fragment, in order, compared without a trailing slash."""
    return [html.unescape(h).rstrip("/") for h in re.findall(r'href="([^"]*)"', s)]


def squash(s):
    return re.sub(r"\s+", " ", s).strip()


def strip_footnote_marks(s):
    return squash(re.sub(r"\[\d+\]", "", s))


def page_text(raw):
    raw = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", "", raw)
    return squash(html.unescape(re.sub(r"<[^>]+>", " ", raw)).replace("\xa0", " "))


# ---------------------------------------------------------------------- FAQ
_PAIR = re.compile(r"<dt>(\d+)\.\s*(.*?)</dt>\s*<dd>(.*?)</dd>", re.S)


def clean_title(t):
    t = html.unescape(re.sub(r"<[^>]+>", "", t)).replace("\xa0", " ")
    t = re.sub(r"^\s*\[(UPDATED|NEW)\]\s*", "", t)
    return squash(t)


def normalize_answer_html(dd):
    """ENISA answer HTML -> the form the guide stores.

    Changes presentation only: external links open in a new tab, whitespace
    quirks around bold and at paragraph edges go. Wording is never touched.
    """
    s = dd.strip()
    s = re.sub(r'(href="[^"]*?)(?:%20)+"', r'\1"', s)  # a trailing encoded space is never meant
    s = re.sub(r'<a href="(https?://[^"]+)">', r'<a href="\1" target="_blank" rel="noopener">', s)
    s = re.sub(r"<strong>\s*</strong>", " ", s)
    s = re.sub(r"<strong>([^<]*?)\s+</strong>", r"<strong>\1</strong> ", s)
    s = re.sub(r"(?:&nbsp;|\s)+</p>", "</p>", s)
    s = re.sub(r"<p>(?:&nbsp;|\s)+", "<p>", s)
    s = re.sub(r" {2,}", " ", s)
    return "\n".join(ln.strip() for ln in s.split("\n") if ln.strip())


def parse_faq(raw):
    pairs = _PAIR.findall(raw)
    if len(pairs) < 30:
        raise ParseError(f"FAQ: found {len(pairs)} questions, expected at least 30 - page structure changed?")
    qs = []
    for n, t, dd in pairs:
        qs.append({"n": int(n), "title": clean_title(t), "html": normalize_answer_html(dd)})
    nums = [q["n"] for q in qs]
    if nums != list(range(1, len(nums) + 1)):
        raise ParseError(f"FAQ: question numbers are not 1..N in order: {nums}")
    for q in qs:
        if not q["title"] or not words(q["html"]):
            raise ParseError(f"FAQ: Q{q['n']} has an empty title or answer")
    m = re.search(r"Updated:\s*(\d{1,2} [A-Za-z]+ \d{4})", page_text(raw))
    return {"stamp": ("Updated: " + m.group(1)) if m else "", "questions": qs}


# ----------------------------------------------------------------- Glossary
STAGE = {
    "Required": "Required",
    "Optional": "Optional",
    "By default copied from previous step, or updated": "Carried over",
    "N/A": "n/a",
    "Required if such information available": "If available",
}
_NR = re.compile(r"^(\d+|v\d+[a-z]?|i\d+)$")


def cell_text(c):
    """A table cell -> plain text; paragraph breaks become newlines."""
    c = re.sub(r"(?i)</p>\s*<p[^>]*>|<br\s*/?>", "\n", c)
    c = html.unescape(re.sub(r"<[^>]+>", "", c)).replace("\xa0", " ")
    return "\n".join(squash(ln) for ln in c.split("\n") if squash(ln))


def parse_glossary(raw):
    rows = []
    for tr in re.findall(r"(?s)<tr[^>]*>(.*?)</tr>", raw):
        cells = re.findall(r"(?s)<t[dh][^>]*>(.*?)</t[dh]>", tr)
        if len(cells) >= 10:
            rows.append(cells)
    fields = []
    for r in rows:
        nr = re.sub(r"[\s.]+", "", cell_text(r[0]))
        if not _NR.match(nr):
            continue
        stages = []
        for c in r[7:10]:
            s = cell_text(c)
            if s not in STAGE:
                raise ParseError(f"Glossary field {nr}: unknown stage text {s!r}")
            stages.append(STAGE[s])
        fields.append({
            "nr": nr, "name": cell_text(r[1]), "applies": cell_text(r[2]),
            "means": cell_text(r[3]), "how": cell_text(r[4]), "example": cell_text(r[5]),
            "format": cell_text(r[6]), "ew": stages[0], "h72": stages[1], "fr": stages[2],
        })
    if len(fields) < 38:
        raise ParseError(f"Glossary: found {len(fields)} fields, expected at least 38")
    ids = [f["nr"] for f in fields]
    if len(set(ids)) != len(ids):
        raise ParseError("Glossary: duplicate field numbers")
    for f in fields:
        if not f["name"] or not f["means"]:
            raise ParseError(f"Glossary field {f['nr']}: empty name or meaning")
    m = re.search(r"Version\s+(\d+\.\d+)\.?\s+Last update:\s*(\d{1,2} [A-Za-z]+ \d{4})", page_text(raw))
    if not m:
        raise ParseError("Glossary: version/last-update footer not found")
    return {"version": m.group(1), "last_update": m.group(2), "fields": fields}


# ---------------------------------------------------------------- baselines
def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    out = {}
    if m:
        for line in m.group(1).split("\n"):
            k = re.match(r"^([a-z_]+):\s*(.*)$", line)
            if k:
                out[k.group(1)] = k.group(2)
    return out


def first_url(value):
    m = re.search(r"https?://[^\s)`\"]+", value or "")
    return m.group(0) if m else ""


def load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return None


def dump_json(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
