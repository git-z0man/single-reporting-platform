#!/usr/bin/env python3
"""The EU KEV register: every EU KEV entry, the day this monitor first saw it, and when the EUVD
inserted it.

    python3 euvd/eukev.py [--today D] [--dry-run] [--json]

The daily check (check_exploited.py) runs this as part of its own run; standalone it only reads the
EUVD and rewrites euvd/eukev.json.

The EU KEV's own date (`dateAdded` in /api/kevEntries) is not the day an entry entered the
catalogue: entries have been inserted weeks later with an earlier date (euvd/EU-KEV.md). Two things
recorded here do not depend on that date.

- First seen. `first_seen` is the first check that listed the entry and `first_seen_after` the check
  before it, which did not. Entries present when the register started have no `first_seen_after`.
- The insertion clock. The EUVD numbers its KEV rows in insertion order (`id` in /api/kevEntries),
  and since March 2026 CISA rows arrive day by day in date order. Every CISA row numbered below an EU
  KEV row was inserted before it, and none before CISA added it, so the latest date among them is a
  hard lower bound: `inserted_after`. `inserted_before` is the date of the next CISA row, an upper
  bound only on the assumption that the EUVD imports a CISA entry the day CISA adds it; it stays
  empty for the newest rows. `backdated_days`, from `dateAdded` to `inserted_after`, is a minimum.

What counts as a change: an entry that appears or disappears, and a moved `dateAdded`, origin,
vendor, product, notes, CVE, row number or CISA date. The insertion window is recomputed every run
and never counts on its own.

Exit (standalone): 0 unchanged, 1 changed (written unless --dry-run), 2 the check failed; on 2
nothing is written.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import enrich  # noqa: E402

REGISTER = os.path.join("euvd", "eukev.json")
FMT = "%b %d, %Y, %I:%M:%S %p"
CLOCK_FROM = "2026-03-01"   # CISA rows from here on are in insertion order (euvd/EU-KEV.md)
MIN_DUMP = 1000             # canary: the dump has held 1,700+ entries since 2026-10
MIN_EU = 50                 # canary: the EU KEV has held 73 entries since 2026-10-07
FIELDS = ("cve", "row", "dateAdded", "origin", "vendor", "product", "notes", "cisa")


class RegisterError(Exception):
    pass


def day(s):
    try:
        return dt.datetime.strptime(s, FMT).date().isoformat()
    except (ValueError, TypeError):
        raise RegisterError(f"unparseable date {s!r}")


def norm(x):
    return "".join(c for c in (x or "").lower() if c.isalnum())


def is_eu(sources):
    return any(str(s).lower().startswith("eu") for s in sources or [])


def from_dump(dump):
    """(EU KEV ids, the ids whose kevEntries the clock needs) from /api/kev/dump."""
    if not isinstance(dump, list) or len(dump) < MIN_DUMP:
        raise RegisterError(f"kev/dump has {len(dump) if isinstance(dump, list) else 'no'} entries; the pipeline looks broken")
    eu, clock = set(), set()
    for r in dump:
        try:
            i, d, src = r["euvdId"], r["dateAdded"], r["sources"]
        except (KeyError, TypeError):
            raise RegisterError(f"unexpected kev/dump row {r!r:.120}")
        if not i:
            continue
        if is_eu(src):
            eu.add(i)
            clock.add(i)
        elif (d or "") >= CLOCK_FROM:
            clock.add(i)
    if len(eu) < MIN_EU:
        raise RegisterError(f"only {len(eu)} EU KEV entries in kev/dump; the pipeline looks broken")
    return sorted(eu), sorted(clock)


def rows(recs, eu):
    """({EUVD id: entry} of the EU KEV, [(row, date)] of the CISA rows) from /api/kevEntries/batch."""
    out, clock, cisa = {}, [], {}
    for i, lst in recs.items():
        for e in lst:
            try:
                code, n, d = e["kevSource"]["code"], int(e["id"]), day(e["dateAdded"])
            except (KeyError, TypeError, ValueError):
                raise RegisterError(f"unexpected kevEntries record for {i}: {e!r:.120}")
            if code == "CISA":
                clock.append((n, d))
                cisa[i] = min(cisa.get(i, d), d)
            elif code == "EUKEV":
                out[i] = {"id": i, "cve": e.get("cveId") or "", "row": n, "dateAdded": d,
                          "origin": e.get("originSource") or "", "vendor": e.get("vendorProject") or "",
                          "product": e.get("product") or "", "notes": e.get("notes") or ""}
    missing = sorted(set(eu) - set(out))
    if missing:
        raise RegisterError(f"kev/dump lists EU KEV entries that kevEntries does not: {missing[:5]}")
    for i, e in out.items():
        e["cisa"] = cisa.get(i, "")
    clock.sort()
    for e in out.values():
        before = [d for n, d in clock if n < e["row"]]
        lo = max(before) if before else ""
        later = [d for n, d in clock if n > e["row"] and d >= lo]
        e["inserted_after"], e["inserted_before"] = lo, (later[0] if later else "")
        e["backdated_days"] = max(0, (dt.date.fromisoformat(lo) - dt.date.fromisoformat(e["dateAdded"])).days) if lo else 0
    return out, clock


def update(old, cur, today, prev):
    """(new register, what changed). `prev` is the previous check day, on which new entries were absent."""
    o = {e["id"]: e for e in (old or {}).get("entries", [])}
    entries, new, changed = [], [], []
    for i, e in sorted(cur.items(), key=lambda kv: kv[1]["row"]):
        p = o.get(i)
        e = dict(e)
        if p is None:
            e.update(first_seen=today, first_seen_after=prev if old else "", changes=[])
            if old:
                new.append(i)
        else:
            e.update(first_seen=p["first_seen"], first_seen_after=p.get("first_seen_after", ""),
                     changes=list(p.get("changes", [])))
            for f in FIELDS:
                if p.get(f) != e[f]:
                    e["changes"].append({"day": today, "field": f, "from": p.get(f), "to": e[f]})
                    changed.append({"id": i, "field": f, "from": p.get(f), "to": e[f]})
        entries.append(e)
    removed = sorted(set(o) - set(cur))
    gone = list((old or {}).get("removed", [])) + [{**o[i], "removed": today, "removed_after": prev} for i in removed]
    seen = {norm(x["origin"]) for x in list(o.values()) + (old or {}).get("removed", [])}
    origins = sorted({e["origin"] for e in entries if old and norm(e["origin"]) not in seen})
    reg = {"schema": 1, "started": (old or {}).get("started") or today, "entries": entries, "removed": gone}
    return reg, {"started": old is None, "new": new, "changed": changed, "removed": removed, "new_origins": origins}


def is_change(rd):
    return bool(rd["started"] or rd["new"] or rd["changed"] or rd["removed"])


def summary(reg, rd):
    """What the daily check's --json carries about the register."""
    e = {x["id"]: x for x in reg["entries"]}
    keep = ("id", "cve", "dateAdded", "origin", "vendor", "cisa", "first_seen_after", "inserted_after",
            "inserted_before", "backdated_days")
    return {"eukev_started": rd["started"], "eukev_new": [{k: e[i][k] for k in keep} for i in rd["new"]],
            "eukev_changed": rd["changed"], "eukev_removed": rd["removed"], "eukev_new_origins": rd["new_origins"]}


def days(n):
    return f"{n} day{'s' if n != 1 else ''}" if n else "-"


def render(reg, since, go_live):
    """The register's section of the baseline: counts, then every entry inserted from `since` on or first
    seen by this monitor."""
    es = reg["entries"]
    late = [e for e in es if e["inserted_after"] >= since or e["first_seen_after"]]
    first = min((e["inserted_after"] for e in es if e["inserted_after"]), default="")
    batch = [e for e in es if e["inserted_after"] == first]
    rest = [e for e in es if e["inserted_after"] != first]
    back = [e for e in rest if e["backdated_days"]]
    after = [e for e in es if e["inserted_after"] >= go_live]
    out = ["## EU KEV register", "",
           f"The EUVD lists {len(es)} EU KEV entries (`euvd/eukev.json`, kept since {reg['started']}). The EU KEV's "
           "date is not the day an entry was added. The EUVD numbers its KEV rows in insertion order, and the CISA "
           "rows around an EU KEV row date its insertion: \"Inserted\" runs from the latest CISA date before it "
           "(a hard lower bound) to the next CISA date (an upper bound if the EUVD imports CISA entries the same "
           f"day). By that clock the first {len(batch)} entries arrived together, inserted between {first} and "
           f"{batch[0]['inserted_before'] if batch else ''}; of the {len(rest)} inserted since, {len(back)} carry a "
           f"date at least one day before their insertion, and {len(after)} were inserted on or after the go-live "
           "day. \"First seen here\" is the first check of this monitor that listed the entry, with the previous "
           "check, which did not.", ""]
    if late:
        out += ["| EUVD ID | EU KEV date | Inserted | Back-dated by at least | First seen here | Origin | Vendor | CISA KEV added |",
                "|---|---|---|---|---|---|---|---|"]
        for e in late:
            seen = f"{e['first_seen']} (not on {e['first_seen_after']})" if e["first_seen_after"] else "at register start"
            out.append(f"| [{e['id']}](https://euvd.enisa.europa.eu/enisa/{e['id']}) | {e['dateAdded']} | "
                       f"{e['inserted_after']} to {e['inserted_before'] or 'now'} | "
                       f"{days(e['backdated_days'])} | {seen} | "
                       f"{e['origin']} | {e['vendor']} | {e['cisa'] or '-'} |")
    if reg["removed"]:
        out += ["", "Removed from the EU KEV: " + ", ".join(f"{e['id']} ({e['removed']})" for e in reg["removed"]) + "."]
    return out


def fetch(dump=None):
    """(EU ids, kevEntries for the clock) from the EUVD."""
    eu, clock = from_dump(enrich.kev_dump() if dump is None else dump)
    return eu, enrich.kev_batch(clock)


def last_check(path):
    try:
        with open(path, encoding="utf-8") as fh:
            m = re.search(r"^last_check: *(\S+)", fh.read(), re.M)
    except FileNotFoundError:
        return ""
    return m.group(1) if m else ""


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--today", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    today = a.today or dt.datetime.now(dt.timezone.utc).date().isoformat()
    path = os.path.join(a.root, REGISTER)
    try:
        eu, recs = fetch()
        cur, _ = rows(recs, eu)
        try:
            with open(path, encoding="utf-8") as fh:
                old = json.load(fh)
        except FileNotFoundError:
            old = None
        reg, rd = update(old, cur, today, last_check(os.path.join(a.root, "euvd-exploited-baseline.md")))
    except (RegisterError, enrich.FetchError, OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if reg != old and not a.dry_run:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(reg, indent=1, ensure_ascii=False) + "\n")
    s = summary(reg, rd)
    print(json.dumps(s, indent=1) if a.json else
          f"{len(reg['entries'])} EU KEV entries; new {[x['id'] for x in s['eukev_new']]}, "
          f"changed {s['eukev_changed']}, removed {s['eukev_removed']}, new origins {s['eukev_new_origins']}")
    return 1 if is_change(rd) else 0


if __name__ == "__main__":
    sys.exit(main())
