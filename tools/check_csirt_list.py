#!/usr/bin/env python3
"""Diff ENISA's "List of CSIRTs Designated as Coordinators" against the baseline.

    python3 tools/check_csirt_list.py <fetched.html> [enisa-srp-faq-baseline.md]

The page carries the country -> CSIRT-designated-as-coordinator mapping. ENISA edits it
without moving its "Last updated" stamp: on 2026-10-18 Spain's two incident-handling links
were removed under an unchanged stamp of 10 September 2026, and the ENISA pages monitor
reported "unchanged" for ten daily runs afterwards, because nothing compared the list
itself. This does that comparison, so the monitor no longer has to eyeball it.

It reads a file and never fetches: tools/fetch_enisa.py stays the only tool here that
touches the network.

Exit: 0 the lists agree, 1 they differ (the delta is printed, per country), 2 the input
could not be parsed — which is itself a finding, because it means the page's shape moved.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTION = "## List of CSIRTs Designated as Coordinators"
ROW = re.compile(r"<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>", re.S | re.I)
HREF = re.compile(r'href="([^"]+)"', re.I)
URL = re.compile(r"https?://[^\s<>)`*]+")


def from_html(text):
    """{country: [url, ...]} from the page's one-row-per-country table."""
    out = {}
    for name, cell in ROW.findall(text):
        country = html.unescape(re.sub(r"<[^>]+>", "", name)).strip()
        if country:
            out[country] = [html.unescape(u).rstrip("/") for u in HREF.findall(cell)]
    return out


def from_baseline(text):
    """{country: [url, ...]} from the baseline's section, ignoring *(…)* annotations,
    which quote earlier values and would otherwise count as current links."""
    body = text.split(SECTION, 1)[-1].split("\n## ", 1)[0]
    out = {}
    for line in body.splitlines():
        m = re.match(r"-\s+([^:]+):\s*(.+)", line)
        if m:
            out[m.group(1).strip()] = [u.rstrip("/") for u in URL.findall(re.sub(r"\*\(.*?\)\*", "", m.group(2)))]
    return out


def diff(live, base):
    lines = []
    for c in sorted(set(live) | set(base)):
        if c not in base:
            lines.append(f"  + {c} (new country): " + ", ".join(live[c]))
        elif c not in live:
            lines.append(f"  - {c} (gone): " + ", ".join(base[c]))
        elif set(live[c]) != set(base[c]):
            gone, added = sorted(set(base[c]) - set(live[c])), sorted(set(live[c]) - set(base[c]))
            lines.append(f"  ~ {c}:" + "".join(f"\n      removed {u}" for u in gone)
                         + "".join(f"\n      added   {u}" for u in added))
    return lines


def main(argv=None):
    a = (argv if argv is not None else sys.argv[1:])
    if not a:
        print(__doc__.strip().splitlines()[2].strip(), file=sys.stderr)
        return 2
    page, baseline = a[0], (a[1] if len(a) > 1 else os.path.join(ROOT, "enisa-srp-faq-baseline.md"))
    live = from_html(open(page, errors="replace").read())
    base = from_baseline(open(baseline, errors="replace").read())
    if not live:
        print("error: no country rows in the page; its markup moved", file=sys.stderr)
        return 2
    if not base:
        print(f"error: no country list under '{SECTION}' in {baseline}", file=sys.stderr)
        return 2
    d = diff(live, base)
    if not d:
        print(f"unchanged: {len(live)} countries, same links as the baseline")
        return 0
    print(f"changed: {len(d)} of {len(set(live) | set(base))} countries differ from the baseline")
    print("\n".join(d))
    return 1


if __name__ == "__main__":
    sys.exit(main())
