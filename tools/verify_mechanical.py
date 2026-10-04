#!/usr/bin/env python3
"""Is this change to index.html purely mechanical?

    python3 tools/verify_mechanical.py origin/main

Recomputes sync_guide on BASE's index.html using the guide-sync/ extracts and
baselines in the working tree, and requires the result to equal the working
tree's index.html *byte for byte*. Any hand edit - by a person or a model -
makes the two differ, so a change that passes can only be what sync_guide
would have produced anyway. Judgment items also disqualify it.

This is the gate a Routine runs before merging its own pull request.

Exit: 0 mechanical and eligible, 1 not eligible (reason printed), 2 error.
"""
import argparse
import difflib
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guide_lib as g  # noqa: E402
import sync_guide as sg  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("base", nargs="?", default="origin/main")
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--guide", default="index.html")
    a = ap.parse_args(argv)
    r = subprocess.run(["git", "-C", a.root, "show", f"{a.base}:{a.guide}"], capture_output=True, text=True)
    if r.returncode:
        print(f"error: cannot read {a.guide} at {a.base}: {r.stderr.strip()}", file=sys.stderr)
        return 2
    base_text = r.stdout
    try:
        with open(os.path.join(a.root, a.guide), encoding="utf-8") as fh:
            head_text = fh.read()
        faq = g.load_json(os.path.join(a.root, "guide-sync", "faq.json"))
        gl = g.load_json(os.path.join(a.root, "guide-sync", "glossary.json"))
        if not faq or not gl:
            raise OSError("guide-sync/faq.json or glossary.json missing")
        expected, rep = sg.sync(base_text, faq, gl, sg.moved_urls(a.root), include_judgment=False)
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if head_text == base_text:
        print("index.html unchanged: nothing to verify")
        return 0
    if rep["judgment"]:
        print("NOT ELIGIBLE: judgment items are pending:")
        for it in rep["judgment"]:
            print(f"  {it['class']} {it['target']}: {it['detail']}")
        return 1
    if head_text != expected:
        print("NOT ELIGIBLE: index.html is not what sync_guide produces from the base and the extracts.")
        diff = list(difflib.unified_diff(expected.split("\n"), head_text.split("\n"),
                                         "sync_guide(base)", "working tree", lineterm="", n=0))
        for ln in diff[:12]:
            print("  " + ln[:200])
        if len(diff) > 12:
            print(f"  ... {len(diff) - 12} more diff lines")
        return 1
    if rep["changed_lines"] > sg.MAX_LINES:
        print(f"NOT ELIGIBLE: {rep['changed_lines']} changed lines exceed the {sg.MAX_LINES}-line limit for a mechanical change")
        return 1
    print(f"mechanical: matches sync_guide exactly ({rep['changed_lines']} changed lines, "
          f"{len(rep['mechanical'])} edit(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
