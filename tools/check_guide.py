#!/usr/bin/env python3
"""Check index.html against what ENISA's pages said when guide-sync/ last looked.

Read-only. Exit 0 = no drift, 1 = drift, 2 = input error.

What it compares: FAQ titles *and answer text*, Glossary field names, text and
per-stage status, every count/version/date the guide states (these live in
<span data-sync="..."> markers), plus link, anchor and tag hygiene. The baselines
are a light cross-check only; their text is annotated prose and is not a source.

--online also re-fetches ENISA (does guide-sync/ still match?) and hashes the
Manual PDF against the baseline. Offline, the whole check is reproducible.
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guide_lib as g  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
CHIP_CLASS = {"Required": "mandatory", "Optional": "optional", "Carried over": "carried",
              "n/a": "na", "If available": "conditional"}

CARD = re.compile(r'<details class="faq field" id="(f-[^"]+)">(.*?)</details>', re.S)
FREF = re.compile(r'<td class="c-field">((?:(?!</td>).)*?)<a class="fieldref" href="#(f-[^"]+)" '
                  r'title="([^"]*)">([^<]*)</a>', re.S)
FAQ_ITEM = re.compile(r'<details class="faq">\s*<summary><span class="faq-qwrap"><span class="faq-num">Q(\d+)</span>'
                      r'<span>(.*?)</span></span>.*?</summary>\s*<div class="faq-body">(.*?)</div>\s*</details>', re.S)
MARKER = re.compile(r'<span data-sync="([a-z-]+)">(.*?)</span>', re.S)
STOP = {"the", "of", "a", "an", "and", "or", "to", "in", "on", "for", "that", "is", "be", "about", "by"}


def fmt_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d}&nbsp;{MONTHS[m - 1]}&nbsp;{y}"


def expected_markers(faq, gl):
    return {
        "faq-count": str(len(faq["questions"])),
        "faq-asof": fmt_date(faq["fetched"]),
        "glossary-count": str(len(gl["fields"])),
        "glossary-version": gl["version"],
        "glossary-asof": fmt_date(gl["fetched"]),
        "footer-asof": fmt_date(max(faq["fetched"], gl["fetched"])),
    }


# The guide appends the character limits it observed on the running form to a
# field's format line ("Free text · max 255 characters"). They are not ENISA's
# wording and the guide says so, so the comparison with the Glossary ignores them.
LIMIT = re.compile(r"\s*(?:&middot;|\u00b7)\s*max\.?[^<\u00b7]*?characters\s*$")


def strip_limit(s):
    return LIMIT.sub("", s)


def parse_cards(h):
    cards = {}
    for m in CARD.finditer(h):
        body = m.group(2)
        head = re.search(r'<span class="faq-num">([^<]*)</span><span>(.*?)</span></span>', body, re.S)
        chips = re.findall(r'<span class="chip ([a-z]+)">([^<]*)</span>', body.split("</summary>")[0])
        part = lambda k: (re.search(r'data-k="%s"[^>]*>(.*?)</(?:span|dd|p)>' % k, body, re.S) or [None, ""])[1]
        cards[m.group(1)] = {"num": head.group(1) if head else "", "name": g.squash(html.unescape(re.sub(r"<[^>]+>", "", head.group(2)))) if head else "",
                             "chips": [t for _, t in chips], "fmt": part("fmt"), "means": part("means"),
                             "how": part("how"), "ex": part("ex")}
    return cards


def parse_faq_items(h):
    sec = re.search(r'<section id="faq".*?</section>', h, re.S)
    out = {}
    for m in FAQ_ITEM.finditer(sec.group(0) if sec else ""):
        body = re.sub(r'<p class="guide-note">.*?</p>', "", m.group(3), flags=re.S)
        out[int(m.group(1))] = {"title": g.squash(html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))), "body": body}
    return out


def tokens(s):
    out = []
    for w in g.words(g.strip_footnote_marks(s)):
        if w in STOP:
            continue
        out.append(w[:-1] if len(w) > 3 and w.endswith("s") else w)
    return set(out)


def same_field(a, b):
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return False
    return ta <= tb or tb <= ta or len(ta & tb) / len(ta | tb) >= 0.6


def check(root, guide="index.html", ref=None, online=False):
    findings = []
    add = lambda sev, code, msg: findings.append((sev, code, msg))
    with open(os.path.join(root, guide), encoding="utf-8") as fh:
        h = fh.read()

    def baseline(name):
        if ref:
            r = subprocess.run(["git", "-C", root, "show", f"{ref}:{name}"], capture_output=True, text=True)
            if r.returncode:
                raise SystemExit(f"error: cannot read {name} at {ref}")
            return r.stdout
        with open(os.path.join(root, name), encoding="utf-8") as fh:
            return fh.read()

    faq = g.load_json(os.path.join(root, "guide-sync", "faq.json"))
    gl = g.load_json(os.path.join(root, "guide-sync", "glossary.json"))
    if not faq or not gl:
        raise SystemExit("error: guide-sync/faq.json or glossary.json missing - run tools/fetch_enisa.py")

    # 1. field cross-references -------------------------------------------------
    cards = parse_cards(h)
    total = len(re.findall(r'class="fieldref"', h))
    refs = FREF.findall(h)
    if len(refs) != total:
        add("hard", "REF-PARSE", f"{total} fieldref anchors, {len(refs)} parsed: checker out of date")
    seen = set()
    for row, target, title, badge in refs:
        label = g.squash(html.unescape(re.sub(r"<[^>]+>", "", row)))
        if (target, label) in seen:
            continue
        seen.add((target, label))
        if target not in cards:
            add("hard", "REF-DEAD", f"#{target} does not exist (link text: {label[:55]})")
        elif not same_field(label, cards[target]["name"]):
            add("hard", "REF-WRONG", f"#{target} is '{cards[target]['name'][:40]}' but the link says '{label[:40]}'")
        if g.squash(badge) != target[2:] or target[2:] not in title:
            add("hard", "REF-LABEL", f"badge '{badge}' / title '{title}' disagree with #{target}")

    # 2. link hygiene -----------------------------------------------------------
    for m in re.finditer(r'href="([^"]*)"', h):
        if m.group(1).count("(") != m.group(1).count(")"):
            add("hard", "HREF-PAREN", f"unbalanced parentheses in href: {m.group(1)[:90]}")
    for m in re.finditer(r"</a>(\d+%?\d*\))", h):
        add("hard", "HREF-ORPHAN", f"'{m.group(1)}' stranded right after a link")
    fm_faq = g.frontmatter(baseline("enisa-srp-faq-baseline.md"))
    old = {g.first_url(fm_faq.get(k, "")).rstrip("/") for k in ("old_url", "old_faq_url")} - {""}
    for m in re.finditer(r'href="([^"]*)"', h):
        if m.group(1).rstrip("/") in old:
            add("hard", "URL-STALE", f"link to a moved page's old address: {m.group(1)}")

    # 3. tag balance ------------------------------------------------------------
    for tag in ("details", "summary", "table", "ul", "li"):
        o, c = len(re.findall(rf"<{tag}\b", h)), len(re.findall(rf"</{tag}>", h))
        if o != c:
            add("hard", "TAGS", f"<{tag}> opened {o}, closed {c}")

    # 4. FAQ vs extract (titles AND answers) ------------------------------------
    items = parse_faq_items(h)
    ex = {q["n"]: q for q in faq["questions"]}
    miss, extra = sorted(set(ex) - set(items)), sorted(set(items) - set(ex))
    if miss:
        add("hard", "FAQ-MISSING", "in ENISA's FAQ, not in the guide: " + ", ".join(f"Q{n}" for n in miss))
    if extra:
        add("hard", "FAQ-EXTRA", "in the guide, not in ENISA's FAQ: " + ", ".join(f"Q{n}" for n in extra))
    for n in sorted(set(ex) & set(items)):
        if g.words(ex[n]["title"]) != g.words(items[n]["title"]):
            add("hard", "FAQ-TITLE", f"Q{n}: guide '{items[n]['title'][:50]}' vs ENISA '{ex[n]['title'][:50]}'")
        if g.words(ex[n]["html"]) != g.words(items[n]["body"]):
            add("hard", "FAQ-BODY", f"Q{n}: answer text differs from ENISA's")
        if g.hrefs(ex[n]["html"]) != g.hrefs(items[n]["body"]):
            add("hard", "FAQ-LINKS", f"Q{n}: link targets differ from ENISA's")

    # 5. Glossary vs extract ----------------------------------------------------
    fx = {f["nr"]: f for f in gl["fields"]}
    gids = {i[2:] for i in cards if i != "f-prereq"}
    if set(fx) - gids:
        add("hard", "GL-MISSING", "Glossary fields without a card: " + ", ".join(sorted(set(fx) - gids)))
    if gids - set(fx):
        add("hard", "GL-EXTRA", "cards without a Glossary field: " + ", ".join(sorted(gids - set(fx))))
    for nr in sorted(set(fx) & gids):
        f, c = fx[nr], cards["f-" + nr]
        if g.words(g.strip_footnote_marks(f["name"])) != g.words(g.strip_footnote_marks(c["name"])):
            add("hard", "GL-NAME", f"{nr}: card '{c['name'][:40]}' vs Glossary '{f['name'][:40]}'")
        if c["chips"] != [f["ew"], f["h72"], f["fr"]]:
            add("hard", "GL-STAGES", f"{nr}: card {c['chips']} vs Glossary {[f['ew'], f['h72'], f['fr']]}")
        for k, key in (("means", "means"), ("how", "how"), ("ex", "example"), ("fmt", "format")):
            have = strip_limit(c[k]) if k == "fmt" else c[k]
            if g.words(f[key]) != g.words(have):
                add("hard", "GL-TEXT", f"{nr}: '{key}' text differs from the Glossary")

    # 6. markers: every count, version and date the guide states ----------------
    want = expected_markers(faq, gl)
    found = {}
    for k, v in MARKER.findall(h):
        found.setdefault(k, []).append(v)
        if k not in want:
            add("hard", "MARKER-UNKNOWN", f"data-sync='{k}' is not a known marker")
        elif v != want[k]:
            add("hard", "MARKER-STALE", f"data-sync='{k}' says '{v}', should be '{want[k]}'")
    for k in want:
        if k not in found:
            add("hard", "MARKER-MISSING", f"no data-sync='{k}' marker in the guide")
    bare = MARKER.sub("§", h)
    for m in re.finditer(r"\b(\d+)(?:&nbsp;|\s)+(fields|questions)\b", re.sub(r"<[^>]+>", " ", bare)):
        add("hard", "UNMARKED-COUNT", f"'{m.group(0)}' is stated outside a data-sync marker")
    if re.search(r"field numbers follow ENISA.s FAQ.16", g.page_text(h)):
        add("hard", "STALE-NUMBERING", "a section hint still says field numbers follow FAQ 16")

    # 7. cross-check with the monitors' baselines (advisory) --------------------
    n_bl = len(re.findall(r"^### Q\d+\. ", baseline("enisa-srp-faq-baseline.md"), re.M))
    if n_bl != len(faq["questions"]):
        add("warn", "BASELINE-FAQ", f"baseline has {n_bl} questions, guide-sync has {len(faq['questions'])}")
    ver = re.search(r'"?(\d+\.\d+)', g.frontmatter(baseline("enisa-srp-glossary-baseline.md")).get("page_version", ""))
    if ver and ver.group(1) != gl["version"]:
        add("warn", "BASELINE-GLOSSARY", f"baseline says Glossary v{ver.group(1)}, guide-sync has v{gl['version']}")

    # 8. online -----------------------------------------------------------------
    if online:
        r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "fetch_enisa.py"), "--root", root, "--dry-run"],
                           capture_output=True, text=True)
        if r.returncode == 1:
            add("hard", "EXTRACT-STALE", "ENISA's pages have changed since guide-sync/ was written: " + r.stdout.strip()[:160])
        elif r.returncode == 2:
            add("warn", "ONLINE-ERROR", "could not re-fetch ENISA: " + r.stderr.strip()[:160])
    return findings


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--guide", default="index.html")
    ap.add_argument("--ref", default=None, help="read baselines from this git ref instead of the working tree")
    ap.add_argument("--online", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        findings = check(a.root, a.guide, a.ref, a.online)
    except SystemExit as e:
        print(e, file=sys.stderr)
        return 2
    hard = [f for f in findings if f[0] == "hard"]
    if a.json:
        print(json.dumps([{"severity": s, "code": c, "message": m} for s, c, m in findings], indent=1))
    else:
        print(f"guide: {a.guide} | findings: {len(hard)} hard, {len(findings) - len(hard)} advisory")
        for sev, code, msg in findings:
            print(f"  [{code}] {msg}" + ("" if sev == "hard" else "  (advisory)"))
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
