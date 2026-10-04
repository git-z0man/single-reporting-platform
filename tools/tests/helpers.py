"""Builders for the tests: a small guide made with the same renderers sync_guide uses."""
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
sys.path.insert(0, TOOLS)
import check_guide as cg  # noqa: E402,F401
import guide_lib as g  # noqa: E402,F401
import sync_guide as sg  # noqa: E402,F401

FIXTURES = os.path.join(HERE, "fixtures")


def fx(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return fh.read()


def field(nr, name, applies="Both", ew="Optional", h72="Optional", fr="Optional",
          means="Means it.", how="Do it.", example="Example", fmt="Free text"):
    return {"nr": nr, "name": name, "applies": applies, "means": means, "how": how,
            "example": example, "format": fmt, "ew": ew, "h72": h72, "fr": fr}


def question(n, title, html=None):
    return {"n": n, "title": title, "html": html or f"<p>Answer to question {n}.</p>"}


def extracts():
    faq = {"schema": 1, "source": "x", "fetched": "2026-10-04", "stamp": "Updated: 03 October 2026",
           "questions": [question(1, "What is it?"), question(2, "Who reports?",
                                                              '<p>Severe incidents are reported by <a href="https://example.eu/a" target="_blank" rel="noopener">the AR</a>.</p>'),
                         question(3, "When?")]}
    gl = {"schema": 1, "source": "x", "fetched": "2026-10-04", "version": "1.4", "last_update": "01 October 2026",
          "fields": [field("1", "Notification type", fmt="Select one", ew="Required", h72="Carried over", fr="Carried over"),
                     field("2", "Title", ew="Required", h72="Carried over", fr="Carried over"),
                     field("v19", "CVE ID", "AEV"), field("v26", "Date aware", "AEV", ew="Required"),
                     field("v27", "Malicious actor", "AEV"),
                     field("i31", "Suspected unlawful", "SI")]}
    return faq, gl


PREREQ = ('          <details class="faq field" id="f-prereq">\n'
          '            <summary><span class="faq-qwrap"><span class="faq-num">v27a</span><span>Prerequisites</span></span>'
          '<span class="field-chips"><span class="fchip"><b>EW</b><span class="chip na">n/a</span></span>'
          '<span class="fchip"><b>72&hairsp;h</b><span class="chip na">n/a</span></span>'
          '<span class="fchip"><b>FR</b><span class="chip na">n/a</span></span></span><span class="faq-chev">+</span></summary>\n'
          '            <div class="faq-body"><p>Not in the Glossary.</p></div>\n          </details>\n')


def guide_for(faq, gl, own_note=True):
    """A guide that is exactly in sync with (faq, gl)."""
    cards = {"": "", "v": "", "i": ""}
    for f in gl["fields"]:
        key = {"Both": "", "AEV": "v", "SI": "i"}[f["applies"]]
        cards[key] += sg.render_card(f)
        if f["nr"] == "v27":
            cards[key] += PREREQ
    faqs = "".join(sg.render_faq(q) for q in faq["questions"])
    m = cg.expected_markers(faq, gl)
    S = lambda k: f'<span data-sync="{k}">{m[k]}</span>'
    return f'''<!doctype html><html><body>
<section id="fields" class="phase divider">
  <p class="intro">This is the whole form: all {S("glossary-count")} fields ENISA itemises, version&nbsp;{S("glossary-version")}, as it stood on {S("glossary-asof")}.</p>
  <div id="fieldcards">
    <div class="seclabel"><span class="seclabel-text">Common fields</span></div>
    <p class="fieldgroup-sub">Both.</p>
        <div class="faq-wrap">
{cards[""]}        </div>
    <div class="seclabel"><span class="seclabel-text">Actively exploited vulnerability</span></div>
        <div class="faq-wrap">
{cards["v"]}        </div>
    <div class="seclabel"><span class="seclabel-text">Severe incident</span></div>
        <div class="faq-wrap">
{cards["i"]}        </div>
  </div>
</section>
<section id="faq" class="phase divider">
  <p class="intro">all {S("faq-count")} questions as they stood on {S("faq-asof")}.</p>
        <div class="faq-wrap">
{faqs}        </div>
</section>
<footer>changed {S("footer-asof")}</footer>
</body></html>
'''


BASELINE_FAQ = ("---\nurl: https://example.eu/new/srp\nold_url: https://example.eu/old/srp (moved)\n"
                "faq_url: https://example.eu/new/srp/faq\nold_faq_url: https://example.eu/old/srp/faq (moved)\n---\n"
                "### Q1. What is it?\n### Q2. Who reports?\n### Q3. When?\n")
BASELINE_GL = '---\nurl: https://example.eu/gl\npage_version: "1.4 (footer)"\n---\n'


def make_root(faq, gl, guide=None):
    """A temporary repository root with guide, extracts and baselines."""
    root = tempfile.mkdtemp(prefix="guide-test-")
    os.makedirs(os.path.join(root, "guide-sync"))
    with open(os.path.join(root, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(guide if guide is not None else guide_for(faq, gl))
    g.dump_json(os.path.join(root, "guide-sync", "faq.json"), faq)
    g.dump_json(os.path.join(root, "guide-sync", "glossary.json"), gl)
    for n, t in (("enisa-srp-faq-baseline.md", BASELINE_FAQ), ("enisa-srp-glossary-baseline.md", BASELINE_GL)):
        with open(os.path.join(root, n), "w", encoding="utf-8") as fh:
            fh.write(t)
    return root


def git(root, *a):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True, check=True).stdout


def git_init(root):
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.email", "t@example.eu")
    git(root, "config", "user.name", "t")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    git(root, "branch", "-f", "origin/main", "HEAD")  # a ref named like the real base


def write_json(root, name, data):
    g.dump_json(os.path.join(root, "guide-sync", name), data)


def read(root, name="index.html"):
    with open(os.path.join(root, name), encoding="utf-8") as fh:
        return fh.read()


def write(root, text, name="index.html"):
    with open(os.path.join(root, name), "w", encoding="utf-8") as fh:
        fh.write(text)


def deep(x):
    return copy.deepcopy(x)
