#!/usr/bin/env python3
"""Fetch ENISA's FAQ and Glossary into guide-sync/*.json.

This is the only tool here that touches the network. Everything downstream
(check_guide, sync_guide, verify_mechanical) reads the JSON it writes, so a run
can be re-done later from the repository alone.

A question or field whose *words* have not changed keeps its stored entry, so
ENISA's frequent markup-only edits never produce a diff.

Exit: 0 nothing changed, 1 files written (or would be, with --dry-run), 2 error.
On any error nothing is written.
"""
import argparse
import datetime
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guide_lib as g  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def curl(url):
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        path = tmp.name
    try:
        r = subprocess.run(
            ["curl", "-sS", "--retry", "5", "--retry-delay", "5", "--retry-all-errors",
             "-o", path, "-w", "%{http_code}", url],
            capture_output=True, text=True, timeout=600)
        if r.returncode != 0:
            raise g.ParseError(f"curl failed for {url}: {r.stderr.strip()[:200]}")
        if r.stdout.strip() != "200":
            raise g.ParseError(f"HTTP {r.stdout.strip()} for {url} (a failed fetch, not a content change)")
        with open(path, encoding="utf-8", errors="replace") as fh:
            body = fh.read()
        if len(body) < 20000:
            raise g.ParseError(f"suspiciously small response ({len(body)} bytes) from {url}")
        return body
    finally:
        os.unlink(path)


def baseline_url(root, filename, key):
    with open(os.path.join(root, filename), encoding="utf-8") as fh:
        url = g.first_url(g.frontmatter(fh.read()).get(key, ""))
    if not url:
        raise g.ParseError(f"no {key} in {filename}")
    return url


def merge_faq(old, new):
    keep = {q["n"]: q for q in (old or {}).get("questions", [])}
    out = []
    for q in new["questions"]:
        o = keep.get(q["n"])
        same = o and g.words(o["title"] + " " + o["html"]) == g.words(q["title"] + " " + q["html"])
        out.append(o if same else q)
    return out


_TEXT = ("means", "how", "example", "format")


def same_field(o, f):
    return (o and g.words(g.strip_footnote_marks(o["name"])) == g.words(g.strip_footnote_marks(f["name"]))
            and o["applies"] == f["applies"]
            and all(g.words(o[k]) == g.words(f[k]) for k in _TEXT)
            and (o["ew"], o["h72"], o["fr"]) == (f["ew"], f["h72"], f["fr"]))


def merge_glossary(old, new):
    keep = {f["nr"]: f for f in (old or {}).get("fields", [])}
    return [keep[f["nr"]] if same_field(keep.get(f["nr"]), f) else f for f in new["fields"]]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--out", default=None, help="output dir (default: <root>/guide-sync)")
    ap.add_argument("--faq-file", help="parse this local file instead of fetching")
    ap.add_argument("--glossary-file", help="parse this local file instead of fetching")
    ap.add_argument("--today", default=None, help="date to record (default: today, UTC)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    out = a.out or os.path.join(a.root, "guide-sync")
    today = a.today or datetime.datetime.now(datetime.timezone.utc).date().isoformat()

    try:
        faq_url = baseline_url(a.root, "enisa-srp-faq-baseline.md", "faq_url")
        gl_url = baseline_url(a.root, "enisa-srp-glossary-baseline.md", "url")
        def read(p):
            with open(p, encoding="utf-8", errors="replace") as fh:
                return fh.read()
        faq = g.parse_faq(read(a.faq_file) if a.faq_file else curl(faq_url))
        gl = g.parse_glossary(read(a.glossary_file) if a.glossary_file else curl(gl_url))
    except (g.ParseError, OSError, subprocess.SubprocessError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    faq_path, gl_path = os.path.join(out, "faq.json"), os.path.join(out, "glossary.json")
    old_faq, old_gl = g.load_json(faq_path), g.load_json(gl_path)

    new_faq = {"schema": 1, "source": faq_url, "fetched": today, "stamp": faq["stamp"],
               "questions": merge_faq(old_faq, faq)}
    new_gl = {"schema": 1, "source": gl_url, "fetched": today, "version": gl["version"],
              "last_update": gl["last_update"], "fields": merge_glossary(old_gl, gl)}

    # What counts as a change. The FAQ stamp is ENISA's own and moves without
    # edits, so it does not; the Glossary version is shown in the guide, so it does.
    faq_changed = not old_faq or old_faq.get("questions") != new_faq["questions"]
    gl_changed = (not old_gl or old_gl.get("fields") != new_gl["fields"]
                  or (old_gl.get("version"), old_gl.get("last_update")) != (gl["version"], gl["last_update"]))

    msg = []
    if faq_changed:
        old_n = {q["n"] for q in (old_faq or {}).get("questions", [])}
        msg.append(f"faq.json: {len(new_faq['questions'])} questions"
                   + (f", new: {sorted({q['n'] for q in new_faq['questions']} - old_n)}" if old_faq else ", first write"))
    if gl_changed:
        old_ids = {f["nr"] for f in (old_gl or {}).get("fields", [])}
        msg.append(f"glossary.json: v{gl['version']}, {len(new_gl['fields'])} fields"
                   + (f", new: {sorted({f['nr'] for f in new_gl['fields']} - old_ids)}" if old_gl else ", first write"))
    if not msg:
        print("unchanged: faq.json and glossary.json already match ENISA's pages")
        return 0
    if not a.dry_run:
        os.makedirs(out, exist_ok=True)
        if faq_changed:
            g.dump_json(faq_path, new_faq)
        if gl_changed:
            g.dump_json(gl_path, new_gl)
    print(("would write: " if a.dry_run else "wrote: ") + "; ".join(msg))
    return 1


if __name__ == "__main__":
    sys.exit(main())
