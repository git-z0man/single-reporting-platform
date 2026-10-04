#!/usr/bin/env python3
"""Bring index.html in line with guide-sync/*.json.

A pure function of repository files: no network, no clock. That is what lets
verify_mechanical.py recompute an edit later and demand byte equality.

Edits come in two kinds.

  mechanical  Safe to auto-merge. Counts, versions and dates in data-sync
              markers; link repoints for pages ENISA moved; new FAQ questions
              appended verbatim; typo-class word changes; new Glossary cards
              whose every stage is Optional or n/a.

  judgment    Reported, and only applied with --include-judgment. Anything that
              could change what a person filing a notification must do: a
              rewritten FAQ answer, a changed stage, a new Required field (the
              phase tables must change too), a changed link target, a removed
              question or field.

Whatever the guide says about itself - callouts, "From practice" notes, OWN-NOTE
placeholders, the Note on ENISA's text boxes - is never touched.

Exit: 0 nothing to do, 1 edits made, 3 nothing edited but judgment items wait,
2 error.
"""
import argparse
import difflib
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_guide as cg  # noqa: E402
import guide_lib as g  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_LINES = 60  # a bigger diff than this is never "mechanical"

CHIP_CLASS = cg.CHIP_CLASS
esc = lambda s: html.escape(s, quote=False)


# ------------------------------------------------------------------ rendering
def text_html(s):
    return "<br>".join(esc(line) for line in s.split("\n"))


def chips_html(f):
    one = lambda lab, v: f'<span class="fchip"><b>{lab}</b><span class="chip {CHIP_CLASS[v]}">{v}</span></span>'
    return ('<span class="field-chips">' + one("EW", f["ew"]) + one("72&hairsp;h", f["h72"])
            + one("FR", f["fr"]) + "</span>")


def render_card(f):
    ex = (f'              <figure class="field-example"><span class="fdef-label">ENISA’s example</span>'
          f'<p data-k="ex">{text_html(f["example"])}</p></figure>\n') if f["example"] else ""
    return (
        f'          <details class="faq field" id="f-{f["nr"]}">\n'
        f'            <summary><span class="faq-qwrap"><span class="faq-num">{f["nr"]}</span><span>{esc(f["name"])}</span></span>'
        f'{chips_html(f)}<span class="faq-chev">+</span></summary>\n'
        f'            <div class="faq-body">\n'
        f'              <p class="field-format"><span class="fdef-label">Format</span><span data-k="fmt">{text_html(f["format"])}</span></p>\n'
        f'              <dl class="fdef">\n'
        f'                <dt>What it means</dt><dd data-k="means">{text_html(f["means"])}</dd>\n'
        f'                <dt>How to complete it</dt><dd data-k="how">{text_html(f["how"])}</dd>\n'
        f'              </dl>\n{ex}'
        f'              <!-- OWN-NOTE field-{f["nr"]}: your own practical note here, as <p class="ownnote">…</p> -->\n'
        f'              <p class="field-src"><span class="field-gl">Glossary {f["nr"]}</span> &middot; applies to {esc(f["applies"])}</p>\n'
        f'            </div>\n'
        f'          </details>\n')


def indent_answer(body):
    out = []
    for ln in body.split("\n"):
        out.append(("                " if ln.startswith("<li>") else "              ") + ln)
    return "\n".join(out)


def render_faq(q, keep=""):
    return (
        f'          <details class="faq">\n'
        f'            <summary><span class="faq-qwrap"><span class="faq-num">Q{q["n"]}</span><span>{esc(q["title"])}</span></span>'
        f'<span class="faq-chev">+</span></summary>\n'
        f'            <div class="faq-body">\n{indent_answer(q["html"])}\n{keep}'
        f'            </div>\n'
        f'          </details>\n')


# --------------------------------------------------------------- classification
def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def is_typo_change(a, b):
    """True if the word lists differ only by same-length, near-identical words."""
    if a == b:
        return True
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        if tag != "replace" or i2 - i1 != j2 - j1:
            return False
        for x, y in zip(a[i1:i2], b[j1:j2]):
            if min(len(x), len(y)) < 5 or lev(x, y) > 2:
                return False
    return True


# ------------------------------------------------------------------ the sync
class Sync:
    def __init__(self, h, faq, gl, urls, include_judgment):
        self.h, self.faq, self.gl, self.urls = h, faq, gl, urls
        self.include = include_judgment
        self.mech, self.judg, self.applied_judgment = [], [], False

    def note(self, cls, target, detail, mechanical):
        (self.mech if mechanical else self.judg).append({"class": cls, "target": target, "detail": detail})

    def apply_ok(self, mechanical):
        if mechanical:
            return True
        if self.include:
            self.applied_judgment = True
            return True
        return False

    # ---- FAQ ----
    def faq_blocks(self):
        sec = re.search(r'<section id="faq".*?</section>', self.h, re.S)
        base = sec.start() if sec else 0
        pat = re.compile(r'          <details class="faq">\s*<summary><span class="faq-qwrap"><span class="faq-num">Q(\d+)</span>.*?</details>\n', re.S)
        return [(int(m.group(1)), base + m.start(), base + m.end(), m.group(0))
                for m in pat.finditer(sec.group(0) if sec else "")]

    def sync_faq(self):
        for q in sorted(self.faq["questions"], key=lambda x: x["n"]):
            blocks = {n: (s, e, t) for n, s, e, t in self.faq_blocks()}
            if q["n"] not in blocks:
                before = [b for b in blocks if b < q["n"]]
                if before:
                    pos = blocks[max(before)][1]
                else:
                    m = re.search(r'<div class="faq-wrap">\n', self.h[self.h.find('<section id="faq"'):])
                    pos = self.h.find('<section id="faq"') + m.end() if m else None
                if pos is None:
                    self.note("faq-new", f"Q{q['n']}", "no place to insert it - guide structure changed", False)
                    continue
                self.h = self.h[:pos] + render_faq(q) + self.h[pos:]
                self.note("faq-new", f"Q{q['n']}", q["title"][:70], True)
                continue
            s, e, old = blocks[q["n"]]
            m = re.search(r'<span class="faq-num">Q\d+</span><span>(.*?)</span></span>.*?<div class="faq-body">(.*?)</div>\s*</details>', old, re.S)
            old_title = g.squash(html.unescape(re.sub(r"<[^>]+>", "", m.group(1))))
            guide_note = "".join(x + "\n" for x in re.findall(r'              <p class="guide-note">.*?</p>', m.group(2), re.S))
            body = re.sub(r'<p class="guide-note">.*?</p>', "", m.group(2), flags=re.S)
            a = g.words(old_title) + g.words(body)
            b = g.words(q["title"]) + g.words(q["html"])
            links_changed = g.hrefs(body) != g.hrefs(q["html"])
            if a == b and not links_changed:
                continue
            if links_changed:
                self.note("faq-links", f"Q{q['n']}", "link targets differ from ENISA's", False)
                mech = False
            elif is_typo_change(a, b):
                mech = True
            else:
                mech = False
            if not links_changed:
                self.note("faq-typo" if mech else "faq-text", f"Q{q['n']}",
                          "typo-class correction" if mech else "answer or title wording changed", mech)
            if self.apply_ok(mech):
                self.h = self.h[:s] + render_faq(q, guide_note) + self.h[e:]
        known = {q["n"] for q in self.faq["questions"]}
        for n, _, _, _ in self.faq_blocks():
            if n not in known:
                self.note("faq-removed", f"Q{n}", "in the guide, no longer on ENISA's page", False)

    # ---- Glossary cards ----
    def card_span(self, nr):
        m = re.search(r'          <details class="faq field" id="f-%s">.*?</details>\n' % re.escape(nr), self.h, re.S)
        return (m.start(), m.end(), m.group(0)) if m else None

    @staticmethod
    def sort_key(nr):
        m = re.match(r"^([vi]?)(\d+)([a-z]?)$", nr)
        return (m.group(1), int(m.group(2)), m.group(3))

    def insert_card(self, f):
        """Insert in numeric order inside the group that matches 'applies'."""
        group = {"Both": "", "AEV": "v", "SI": "i"}.get(f["applies"])
        if group is None:
            return False
        key = self.sort_key(f["nr"])
        cards = [(m.group(1)[2:], m.start(), m.end()) for m in
                 re.finditer(r'          <details class="faq field" id="(f-[^"]+)">.*?</details>\n', self.h, re.S)]
        same = [(nr, s, e) for nr, s, e in cards if nr != "prereq" and self.sort_key(nr)[0] == group]
        if not same:
            return False
        later = [c for c in same if self.sort_key(c[0]) > key]
        pos = later[0][1] if later else same[-1][2]
        self.h = self.h[:pos] + render_card(f) + self.h[pos:]
        return True

    def set_part(self, block, key, inner):
        pat = {"fmt": r'(<span data-k="fmt">)(.*?)(</span>)', "means": r'(<dd data-k="means">)(.*?)(</dd>)',
               "how": r'(<dd data-k="how">)(.*?)(</dd>)', "ex": r'(<p data-k="ex">)(.*?)(</p>)'}[key]
        return re.sub(pat, lambda m: m.group(1) + inner + m.group(3), block, count=1, flags=re.S)

    def sync_glossary(self):
        fields = self.gl["fields"]
        for f in fields:
            span = self.card_span(f["nr"])
            if not span:
                optional_only = all(v in ("Optional", "n/a") for v in (f["ew"], f["h72"], f["fr"]))
                if optional_only:
                    ok = self.insert_card(f)
                    self.note("gl-new", f["nr"], f["name"][:70], ok)
                else:
                    stages = "/".join((f["ew"], f["h72"], f["fr"]))
                    self.note("gl-new-required", f["nr"],
                              f"{f['name'][:60]} ({stages}): a card AND the phase tables need a human", False)
                    if self.include:
                        self.applied_judgment = self.insert_card(f) or self.applied_judgment
                continue
            s, e, blk = span
            c = cg.parse_cards(blk)["f-" + f["nr"]]
            new_blk, mech_all, parts = blk, True, []
            if c["chips"] != [f["ew"], f["h72"], f["fr"]]:
                self.note("gl-stages", f["nr"], f"stages {c['chips']} -> {[f['ew'], f['h72'], f['fr']]}", False)
                if self.apply_ok(False):
                    new_blk = re.sub(r'<span class="field-chips">(?:<span class="fchip">.*?</span></span>){3}</span>',
                                     lambda m: chips_html(f), new_blk, count=1, flags=re.S)
            for key, k2, val in (("fmt", "fmt", f["format"]), ("means", "means", f["means"]),
                                 ("how", "how", f["how"]), ("ex", "ex", f["example"])):
                have = cg.strip_limit(c[k2]) if key == "fmt" else c[k2]
                if g.words(have) == g.words(val):
                    continue
                typo = is_typo_change(g.words(have), g.words(val))
                self.note("gl-typo" if typo else "gl-text", f["nr"], f"'{key}' wording changed", typo)
                if self.apply_ok(typo):
                    inner = text_html(val)
                    if key == "fmt":
                        suffix = cg.LIMIT.search(c["fmt"])
                        inner += suffix.group(0) if suffix else ""
                    new_blk = self.set_part(new_blk, key, inner)
            old_name = g.strip_footnote_marks(c["name"])
            if g.words(old_name) != g.words(g.strip_footnote_marks(f["name"])):
                typo = is_typo_change(g.words(old_name), g.words(g.strip_footnote_marks(f["name"])))
                self.note("gl-name", f["nr"], "field name changed", typo)
                if self.apply_ok(typo):
                    new_blk = re.sub(r'(<span class="faq-num">[^<]*</span><span>)(.*?)(</span></span>)',
                                     lambda m: m.group(1) + esc(f["name"]) + m.group(3), new_blk, count=1, flags=re.S)
            if new_blk != blk:
                self.h = self.h[:s] + new_blk + self.h[e:]
        known = {f["nr"] for f in fields}
        for m in re.finditer(r'<details class="faq field" id="f-([^"]+)">', self.h):
            if m.group(1) not in known and m.group(1) != "prereq":
                self.note("gl-removed", m.group(1), "card exists, field gone from ENISA's Glossary", False)

    # ---- links and markers ----
    def sync_urls(self):
        for old, new in self.urls.items():
            pat = re.compile(r'href="%s/?"' % re.escape(old))
            n = len(pat.findall(self.h))
            if n:
                self.h = pat.sub(f'href="{new}"', self.h)
                self.note("url", old.rsplit("/", 1)[-1], f"{n} link(s) repointed to {new}", True)

    def sync_markers(self):
        want = cg.expected_markers(self.faq, self.gl)

        seen = {}

        def fix(m):
            k, v = m.group(1), m.group(2)
            if k in want and v != want[k]:
                old, n = seen.get(k, (v, 0))
                seen[k] = (old, n + 1)
                return f'<span data-sync="{k}">{want[k]}</span>'
            return m.group(0)
        self.h = cg.MARKER.sub(fix, self.h)
        for k, (old, n) in seen.items():
            self.note("marker", k, f"'{old}' -> '{want[k]}'" + (f" ({n} places)" if n > 1 else ""), True)

    def run(self):
        self.sync_faq()
        self.sync_glossary()
        self.sync_urls()
        self.sync_markers()
        return self.h


def moved_urls(root):
    out = {}
    path = os.path.join(root, "enisa-srp-faq-baseline.md")
    with open(path, encoding="utf-8") as fh:
        fm = g.frontmatter(fh.read())
    for old_k, new_k in (("old_url", "url"), ("old_faq_url", "faq_url")):
        old, new = g.first_url(fm.get(old_k, "")).rstrip("/"), g.first_url(fm.get(new_k, "")).rstrip("/")
        if old and new and old != new:
            out[old] = new
    return out


def sync(h, faq, gl, urls, include_judgment=False):
    s = Sync(h, faq, gl, urls, include_judgment)
    new = s.run()
    changed = sum(1 for ln in difflib.unified_diff(h.split("\n"), new.split("\n"), lineterm="", n=0)
                  if ln[:1] in "+-" and ln[:3] not in ("+++", "---"))
    report = {
        "mechanical": s.mech, "judgment": s.judg, "applied_judgment": s.applied_judgment,
        "changed_lines": changed,
        "eligible_for_auto_merge": bool(new != h and not s.judg and not s.applied_judgment and changed <= MAX_LINES),
    }
    return new, report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--guide", default="index.html")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--include-judgment", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        path = os.path.join(a.root, a.guide)
        with open(path, encoding="utf-8") as fh:
            h = fh.read()
        faq = g.load_json(os.path.join(a.root, "guide-sync", "faq.json"))
        gl = g.load_json(os.path.join(a.root, "guide-sync", "glossary.json"))
        if not faq or not gl:
            raise OSError("guide-sync/faq.json or glossary.json missing - run tools/fetch_enisa.py")
        new, rep = sync(h, faq, gl, moved_urls(a.root), a.include_judgment)
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if new != h and not a.dry_run:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new)
    if a.json:
        print(json.dumps(rep, indent=1, ensure_ascii=False))
    else:
        print(f"{'would change' if a.dry_run else 'changed'} {rep['changed_lines']} line(s); "
              f"{len(rep['mechanical'])} mechanical, {len(rep['judgment'])} judgment; "
              f"auto-merge eligible: {rep['eligible_for_auto_merge']}")
        for kind in ("mechanical", "judgment"):
            for it in rep[kind]:
                print(f"  [{kind[:4]}:{it['class']}] {it['target']}: {it['detail']}")
    if new != h:
        return 1
    return 3 if rep["judgment"] else 0


if __name__ == "__main__":
    sys.exit(main())
