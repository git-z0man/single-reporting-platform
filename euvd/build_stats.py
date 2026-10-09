#!/usr/bin/env python3
"""Build the EUVD statistics page: euvd/stats.json, euvd/history.jsonl, euvd/stats.html.

    python3 euvd/build_stats.py [--full] [--no-prerender] [--today YYYY-MM-DD]

Reads the EUVD API (documented and undocumented endpoints, see euvd/API.md), the CISA
KEV catalogue, and the previous euvd/stats.json. Monthly counts for the whole EUVD are
cached in stats.json: a daily run only recounts the current and the previous month
(--full recounts all). Every run appends or replaces today's line in history.jsonl, the
only place where values the EUVD keeps no history of (honeypot counts, set sizes) are
recorded over time.

Honeypot surges: from that history it marks surges, an entry attacked far above its own
30-day level by many sources ("broad"), or flagged UPTICK by the EUVD on several recorded
days in a row ("persistent"). The EUVD's own UPTICK flag compares one day with the 7-day
average and fires for dozens of entries a day; a surge is the stricter signal the monitor
reports. New surges are printed, one per line, after the summary.

The page is rendered by euvd/charts.js from the data embedded in it. When node and
Playwright are available, euvd/prerender.js draws the charts into the file so it also
reads in viewers that run no JavaScript; otherwise the page draws them in the browser.

Exit: 0 written, 2 failed (nothing written). A failed fetch is never a content change.
"""
import argparse
import collections
import datetime as dt
import json
import os
import shutil
import statistics
import subprocess
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_exploited as ce  # noqa: E402
import enrich  # noqa: E402

ROOT = os.path.dirname(HERE)
SEARCH = "https://euvdservices.enisa.europa.eu/api/search?"
KEV_DUMP = "https://euvdservices.enisa.europa.eu/api/kev/dump"
GO_LIVE = ce.GO_LIVE
MONTHS_BACK = 24
# European assigners counted month by month: (EUVD assigner value, display name)
ASSIGNERS = [("CERTVDE", "CERT@VDE (DE)"), ("CERT-PL", "CERT Polska (PL)"), ("INCIBE", "INCIBE-CERT (ES)"),
             ("CIRCL", "CIRCL (LU)"), ("ENISA", "ENISA (EU)"), ("NCSC-NL", "NCSC-NL (NL)"), ("NCSC-FI", "NCSC-FI (FI)"),
             ("SK-CERT", "SK-CERT (SK)"), ("siemens", "Siemens (DE)"), ("schneider", "Schneider Electric (FR)"),
             ("ABB", "ABB (CH/SE)"), ("Bosch", "Bosch (DE)"), ("Nozomi", "Nozomi Networks")]
# Global assigners for scale in the ranking: (assigner value, display name)
GLOBAL = [("mitre", "MITRE"), ("GitHub_M", "GitHub"), ("Patchstack", "Patchstack"), ("VulDB", "VulDB"),
          ("microsoft", "Microsoft"), ("redhat", "Red Hat"), ("Wordfence", "Wordfence"), ("VulnCheck", "VulnCheck"),
          ("cisco", "Cisco"), ("JPCERT", "JPCERT/CC"), ("Fortinet", "Fortinet")]
DETAIL_ASSIGNER = "CERTVDE"
CWE_NAMES = {"CWE-20": "Improper input validation", "CWE-78": "OS command injection", "CWE-787": "Out-of-bounds write",
             "CWE-416": "Use after free", "CWE-119": "Memory buffer bounds", "CWE-22": "Path traversal",
             "CWE-94": "Code injection", "CWE-502": "Unsafe deserialisation", "CWE-77": "Command injection",
             "CWE-79": "Cross-site scripting", "CWE-89": "SQL injection", "CWE-287": "Improper authentication",
             "CWE-306": "Missing authentication", "CWE-843": "Type confusion", "CWE-862": "Missing authorisation",
             "CWE-918": "Server-side request forgery", "CWE-434": "Unrestricted file upload", "CWE-125": "Out-of-bounds read"}
ORIGIN_NAMES = {"cnw": "CSIRTs Network", "cert.pl": "CERT-PL", "cert-pl": "CERT-PL"}
# Honeypot surges. Starting values, to be calibrated once a few weeks are recorded: on
# 2026-10-09 they would have marked 4 entries, against 51 UPTICK flags.
SURGE_RATIO = 20     # today's connections at least this many times the 30-day average
SURGE_IPS = 25       # ... from at least this many source IPs (fewer: one or a few scanners)
SURGE_DAYS = 3       # UPTICK on this many recorded days in a row
TREND_CODE = {"UPTICK": "U", "STEADY": "S", "DECLINE": "D"}


class StatsError(Exception):
    pass


# ---------- fetching (network) ----------

def search_total(query):
    d = ce.get(SEARCH + query + "&size=1")
    try:
        return int(d["total"])
    except (KeyError, TypeError, ValueError):
        raise StatsError(f"no total for {query}")


def search_all(query, cap=2000):
    first = ce.get(SEARCH + query + "&size=100&page=0")
    total, items = first["total"], {x["id"]: x for x in first["items"]}
    if total > cap:
        raise StatsError(f"{query}: {total} records, more than the cap of {cap}")
    for p in range(1, (total + 99) // 100):
        for x in ce.get(SEARCH + query + f"&size=100&page={p}")["items"]:
            items[x["id"]] = x
    if len(items) != total:
        raise StatsError(f"{query}: expected {total}, got {len(items)}")
    return list(items.values())


def month_windows(today, back=MONTHS_BACK):
    """[(YYYY-MM, first day, last day or today)] for the last `back` months including the current one."""
    t = dt.date.fromisoformat(today)
    first = (t.replace(day=1) - dt.timedelta(days=31 * (back - 1))).replace(day=1)
    out, d = [], first
    while d <= t:
        nxt = (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        out.append((d.strftime("%Y-%m"), d.isoformat(), min(nxt - dt.timedelta(days=1), t).isoformat()))
        d = nxt
    return out[-back:]


def count_months(today, cached, full):
    """{series: {month: count}} for 'all', 'crit' and every European assigner. Months already in the
    cache are kept, except the current and the previous one (still filling up) or all with --full."""
    wins = month_windows(today)
    fresh = {m for m, _, _ in wins[-2:]}
    series = {"all": "", "crit": "&fromScore=9&toScore=10"}
    series.update({a: "&assigner=" + urllib.parse.quote(a) for a, _ in ASSIGNERS})
    out = {}
    for name, extra in series.items():
        old = (cached or {}).get(name, {})
        out[name] = {}
        for m, a, b in wins:
            if not full and m not in fresh and m in old:
                out[name][m] = old[m]
            else:
                out[name][m] = search_total(f"fromDate={a}&toDate={b}{extra}")
    return out


def fetch_everything(today, cached_months, full):
    items = ce.fetch_all()
    if len(items) < ce.MIN_TOTAL:
        raise StatsError(f"only {len(items)} exploited entries; the pipeline looks broken, not the EUVD")
    kev_dump = ce.get(KEV_DUMP)
    if not isinstance(kev_dump, list) or len(kev_dump) < ce.MIN_TOTAL:
        raise StatsError("KEV dump empty or not a list")
    ids = sorted(x["id"] for x in items)
    hp = enrich.honeypot_batch(ids)
    eu_ids = sorted({k["euvdId"] for k in kev_dump if "eukev_kev" in k.get("sources", []) and k.get("euvdId")})
    kev_entries = enrich._batch(enrich.KEV_ENTRIES, "kevEntries", eu_ids, chunk=40)
    cisa = enrich.cisa_catalog()
    months = count_months(today, cached_months, full)
    totals = {a: search_total("assigner=" + urllib.parse.quote(a)) for a, _ in ASSIGNERS + GLOBAL}
    euvd_total = search_total("fromScore=0&toScore=10")
    detail = search_all("assigner=" + urllib.parse.quote(DETAIL_ASSIGNER))
    return dict(items=items, kev_dump=kev_dump, hp=hp, kev_entries=kev_entries, cisa=cisa, months=months,
                totals=totals, euvd_total=euvd_total, detail=detail)


# ---------- computing (pure) ----------

def pday(s):
    return dt.datetime.strptime(s, ce.FMT).date()


def vendor_of(x):
    return ", ".join(v["vendor"]["name"] for v in x.get("enisaIdVendor", [])) or "n/a"


def median(v):
    return statistics.median(v) if v else None


def mean(v):
    return round(statistics.mean(v), 1) if v else None


def kev_class(sources):
    s = set(sources)
    return "both" if {"cisa_kev", "eukev_kev"} <= s else ("eu" if s == {"eukev_kev"} else "cisa")


def eu_cisa_dates(entries):
    """(EU KEV date, CISA date or None, origin, vendor, product) from one entry's kevEntries list."""
    eu = next((e for e in entries if e.get("kevSource", {}).get("code") == "EUKEV"), None)
    ci = next((e for e in entries if e.get("kevSource", {}).get("code") == "CISA"), None)
    if not eu:
        return None
    return (pday(eu["dateAdded"]).isoformat(), pday(ci["dateAdded"]).isoformat() if ci else None,
            norm_origin(eu.get("originSource")), eu.get("vendorProject") or "", (eu.get("product") or "")[:48])


def norm_origin(s):
    s = (s or "unknown").strip()
    return ORIGIN_NAMES.get(s.lower(), s)


def lead_split(rows, cut):
    """Counts of who listed first (EU KEV, same day, CISA) before and from `cut`, with median and mean gap
    in days (positive: EU KEV first)."""
    def part(rs):
        g = [(dt.date.fromisoformat(r["cisa"]) - dt.date.fromisoformat(r["eu"])).days for r in rs]
        return {"n": len(g), "eu_first": sum(v > 0 for v in g), "same": sum(v == 0 for v in g),
                "cisa_first": sum(v < 0 for v in g), "median": median(g), "mean": mean(g)}
    both = [r for r in rows if r["cisa"]]
    return {"cut": cut, "recent": part([r for r in both if r["eu"] >= cut]), "old": part([r for r in both if r["eu"] < cut])}


def compute(data, today):
    T = dt.date.fromisoformat(today)
    go = dt.date.fromisoformat(GO_LIVE)
    items = {x["id"]: x for x in data["items"]}
    S = {"schema": 1, "generated": today, "go_live": GO_LIVE, "total": len(items)}

    # KEV additions per month and per day, from the dump
    month = collections.defaultdict(lambda: collections.Counter())
    daily = collections.defaultdict(lambda: collections.Counter())
    day_from = max(go - dt.timedelta(days=27), T - dt.timedelta(days=60))
    for k in data["kev_dump"]:
        d = dt.date.fromisoformat(k["dateAdded"])
        c = kev_class(k.get("sources", []))
        month[d.strftime("%Y-%m")][c] += 1
        if d >= day_from:
            daily[d.isoformat()][c] += 1
    S["kev_month"] = [[m, month[m]["cisa"], month[m]["both"], month[m]["eu"]] for m in sorted(month)]
    S["kev_day_from"] = day_from.isoformat()
    S["kev_day"] = [[d, daily[d]["cisa"], daily[d]["both"], daily[d]["eu"]] for d in sorted(daily)]

    # time from EUVD publication to flagged, last 12 months
    gaps = [(pday(x["exploitedSince"]) - pday(x["datePublished"])).days for x in items.values()
            if x.get("exploitedSince") and x.get("datePublished") and pday(x["exploitedSince"]) > T - dt.timedelta(days=365)]
    bins = [("before publication", lambda v: v < 0), ("same day", lambda v: v == 0), ("1-7 days", lambda v: 1 <= v <= 7),
            ("8-30", lambda v: 8 <= v <= 30), ("31-90", lambda v: 31 <= v <= 90), ("91-365", lambda v: 91 <= v <= 365),
            ("over a year", lambda v: v > 365)]
    S["tte"] = [[n, sum(1 for v in gaps if f(v))] for n, f in bins]
    S["tte_median"], S["tte_n"] = median(gaps), len(gaps)

    # who is faster, EUVD or KEV, by month of flagging (last 24 months)
    start = (T.replace(day=1) - dt.timedelta(days=31 * 23)).replace(day=1)
    by = collections.defaultdict(list)
    allg, golive = [], []
    for x in items.values():
        if not (x.get("exploitedSince") and x.get("datePublished")):
            continue
        es = pday(x["exploitedSince"])
        g = (es - pday(x["datePublished"])).days
        if es >= start:
            by[es.strftime("%Y-%m")].append(g)
            allg.append(g)
        if es >= go:
            golive.append(g)
    S["speed_month"] = [{"m": m, "n": len(v), "first": sum(g > 0 for g in v), "same": sum(g == 0 for g in v),
                         "kev": sum(g < 0 for g in v), "median": median(v), "mean": mean(v)} for m, v in sorted(by.items())]
    S["speed_all"] = {"from": start.strftime("%Y-%m"), "n": len(allg), "median": median(allg), "mean": mean(allg),
                      "golive_n": len(golive), "golive_median": median(golive), "golive_mean": mean(golive)}

    # honeypot
    hp = data["hp"]
    rows = []
    for i, obs in hp.items():
        for o in obs:
            if o.get("connections1d") is not None:
                rows.append({"id": i, "vendor": o.get("vendor") or "", "product": o.get("product") or "",
                             "d1": o.get("connections1d") or 0, "d7": o.get("avg7d") or 0, "d30": o.get("avg30d") or 0,
                             "d90": o.get("avg90d") or 0, "ips": o.get("uniqueIps1d"), "trend": o.get("trend") or ""})
    rows.sort(key=lambda r: -max(r["d1"], r["d7"]))
    S["honeypot"] = rows[:16]
    S["hp_with"] = sum(1 for v in hp.values() if v)
    S["hp_trend"] = dict(collections.Counter(r["trend"] for r in rows))
    cov = collections.defaultdict(lambda: [0, 0])
    for i, x in items.items():
        if x.get("exploitedSince"):
            y = pday(x["exploitedSince"]).year
            cov[y][1] += 1
            cov[y][0] += bool(hp.get(i))
    S["hp_cov"] = {str(y): v for y, v in sorted(cov.items()) if y >= T.year - 5}
    today_obs = hp_today(hp)
    S["hp_scatter"] = sorted([{"id": i, "cve": cve_of(items.get(i), o), "vendor": o.get("vendor") or "",
                               "product": (o.get("product") or "")[:40], "d1": o.get("connections1d") or 0,
                               "ips": o.get("uniqueIps1d") or 0, "trend": o.get("trend") or ""}
                              for i, o in today_obs.items() if (o.get("connections1d") or 0) > 0], key=lambda r: -r["d1"])
    S["hp_lead"] = hp_lead(hp, items, data["kev_entries"])

    # vendors, last 90 days against the 90 before
    cur, prev = collections.Counter(), collections.Counter()
    for x in items.values():
        if not x.get("exploitedSince"):
            continue
        es = pday(x["exploitedSince"])
        if es > T - dt.timedelta(days=90):
            cur[vendor_of(x)] += 1
        elif es > T - dt.timedelta(days=180):
            prev[vendor_of(x)] += 1
    S["vendors"] = [[v, n, prev.get(v, 0)] for v, n in cur.most_common(10)]

    # severity against EPSS, entries flagged in the last 90 days
    S["scatter"] = [{"id": i, "cvss": float(x["baseScore"]), "epss": float(x["epss"]),
                     "cve": next((a for a in (x.get("aliases") or "").split() if a.startswith("CVE-")), "")}
                    for i, x in items.items() if x.get("exploitedSince") and pday(x["exploitedSince"]) > T - dt.timedelta(days=90)
                    and x.get("baseScore") not in (None, "") and x.get("epss") not in (None, "")]

    # edits per day, last 30 days
    upd = collections.Counter(pday(x["dateUpdated"]).isoformat() for x in items.values()
                              if x.get("dateUpdated") and pday(x["dateUpdated"]) > T - dt.timedelta(days=30))
    S["updates_from"] = (T - dt.timedelta(days=29)).isoformat()
    S["updates"] = [[d, upd[d]] for d in sorted(upd)]

    # EU KEV against CISA, and who reports into the EU KEV
    dumb = []
    for i, es in data["kev_entries"].items():
        r = eu_cisa_dates(es)
        if r:
            dumb.append({"id": i, "cve": next((e.get("cveId") for e in es if e.get("cveId")), ""), "eu": r[0], "cisa": r[1],
                         "origin": r[2], "vendor": r[3], "product": r[4]})
    dumb.sort(key=lambda r: r["eu"], reverse=True)
    S["dumbbell"] = dumb
    S["dumb_from"] = (T - dt.timedelta(days=120)).isoformat()
    S["lead"] = lead_split(dumb, (T - dt.timedelta(days=90)).isoformat())
    S["eu_first_date"] = min((r["eu"] for r in dumb), default=None)
    S["eu_go_gap"] = [r["id"] for r in dumb if GO_LIVE <= r["eu"] <= (go + dt.timedelta(days=9)).isoformat()]
    pre, post = collections.Counter(), collections.Counter()
    for r in dumb:
        (post if r["eu"] >= GO_LIVE else pre)[r["origin"]] += 1
    names = sorted(set(pre) | set(post), key=lambda k: (-(pre[k] + post[k]), k))
    S["origin"] = [[n, pre[n], post[n]] for n in names]
    S["origin_after"] = sorted([[r["eu"], r["id"], r["origin"], r["vendor"], r["product"]] for r in dumb if r["eu"] >= GO_LIVE])

    # CISA catalogue: urgency, ransomware, weakness types
    cisa = list(data["cisa"].values())
    S["cisa_n"] = len(cisa)
    urg = collections.defaultdict(lambda: collections.Counter())
    for v in cisa:
        try:
            a, due = dt.date.fromisoformat(v["dateAdded"]), dt.date.fromisoformat(v["dueDate"])
        except (KeyError, ValueError):
            continue
        if a < start:
            continue
        w = (due - a).days
        urg[a.strftime("%Y-%m")][str(w) if w in (3, 7, 14, 21) else "other"] += 1
        urg[a.strftime("%Y-%m")]["ft"] += v.get("forensicTriage") == "Yes"
    S["urgency"] = [[m, urg[m]["3"], urg[m]["7"], urg[m]["14"], urg[m]["21"], urg[m]["other"], urg[m]["ft"]] for m in sorted(urg)]
    ry = collections.defaultdict(lambda: [0, 0])
    for v in cisa:
        y = (v.get("dateAdded") or "")[:4]
        if y:
            ry[y][1] += 1
            ry[y][0] += v.get("knownRansomwareCampaignUse") == "Known"
    S["ransom"] = [[k, a, b] for k, (a, b) in sorted(ry.items())]
    cw = collections.Counter(w for v in cisa for w in (v.get("cwes") or []))
    S["cwe"] = [[k, CWE_NAMES.get(k, ""), n] for k, n in cw.most_common(8)]

    # the whole EUVD
    mo = data["months"]
    ms = sorted(mo["all"])
    S["gen"] = {"months": ms, "all": [mo["all"][m] for m in ms], "crit": [mo["crit"][m] for m in ms],
                "assigners": [[a, n, [mo[a][m] for m in ms], data["totals"][a]] for a, n in ASSIGNERS],
                "rank": sorted([[n, data["totals"][a], 1] for a, n in ASSIGNERS] + [[n, data["totals"][a], 0] for a, n in GLOBAL],
                               key=lambda r: -r[1]),
                "euvd_total": data["euvd_total"], "detail": detail_profile(data["detail"], DETAIL_ASSIGNER, items)}
    return S


def detail_profile(recs, assigner, exploited):
    years = collections.Counter(pday(x["datePublished"]).year for x in recs if x.get("datePublished"))
    ven = collections.Counter()
    for x in recs:
        for e in x.get("enisaIdVendor", []):
            ven[e["vendor"]["name"].replace("Weidmüller", "Weidmueller")] += 1
    sc = [float(x["baseScore"]) for x in recs if x.get("baseScore") not in (None, "")]
    top = sorted([x for x in recs if x.get("epss") not in (None, "")], key=lambda x: -float(x["epss"]))[:5]
    return {"assigner": assigner, "name": dict(ASSIGNERS).get(assigner, assigner), "n": len(recs),
            "years": [[str(k), v] for k, v in sorted(years.items())], "undated": sum(1 for x in recs if not x.get("datePublished")),
            "vendors": ven.most_common(10),
            "sev": [["Critical (9-10)", sum(s >= 9 for s in sc)], ["High (7-8.9)", sum(7 <= s < 9 for s in sc)],
                    ["Medium (4-6.9)", sum(4 <= s < 7 for s in sc)], ["Low (below 4)", sum(s < 4 for s in sc)],
                    ["No score", len(recs) - len(sc)]],
            "epss_top": [[x["id"], float(x["epss"]), x.get("baseScore"), vendor_of(x)] for x in top],
            "exploited": sum(1 for x in recs if x["id"] in exploited)}


def cve_of(item, obs=None):
    return (obs or {}).get("cveId") or next((a for a in ((item or {}).get("aliases") or "").split() if a.startswith("CVE-")), "")


def hp_today(hp):
    """{id: the observation that carries today's counts} from the honeypot answer."""
    out = {}
    for i, obs in hp.items():
        o = next((o for o in obs if o.get("connections1d") is not None), None)
        if o:
            out[i] = o
    return out


def hp_lead(hp, items, kev_entries):
    """When the sensors first saw an exploited entry, against the day it was flagged. The earliest
    firstSeenAt of all is the start of the sensors' record, not a sighting: entries on that day are
    counted apart ("at or before the start"), never as a lead."""
    first = {}
    for i, obs in hp.items():
        seen = [pday(o["firstSeenAt"]) for o in obs if o.get("firstSeenAt")]
        if seen and i in items and items[i].get("exploitedSince"):
            first[i] = min(seen)
    if not first:
        return {"n": 0, "start": None, "censored": 0, "buckets": [], "recent": []}
    start = min(first.values())
    bins = [("over a year before", lambda v: v > 365), ("31-365 days before", lambda v: 31 <= v <= 365),
            ("1-30 days before", lambda v: 1 <= v <= 30), ("same day", lambda v: v == 0),
            ("1-30 days after", lambda v: -30 <= v <= -1), ("over 30 days after", lambda v: v < -30)]
    gaps, recent = {}, []
    for i, fs in first.items():
        flagged = pday(items[i]["exploitedSince"])
        eu = eu_cisa_dates(kev_entries.get(i, []) or [])
        if fs > start:
            gaps[i] = (flagged - fs).days
        if flagged.isoformat() >= GO_LIVE:
            recent.append({"id": i, "cve": cve_of(items[i]), "vendor": vendor_of(items[i]), "flagged": flagged.isoformat(),
                           "eu": eu[0] if eu else None, "seen": fs.isoformat(), "censored": fs == start,
                           "lead": (flagged - fs).days})
    return {"n": len(first), "start": start.isoformat(), "censored": len(first) - len(gaps),
            "buckets": [[n, sum(1 for v in gaps.values() if f(v))] for n, f in bins],
            "recent": sorted(recent, key=lambda r: r["flagged"], reverse=True)}


def history_line(S, data, today):
    """One line per day: what the EUVD keeps no history of. Per honeypot entry with connections:
    [connections today, unique IPs, trend code U/S/D, 30-day average]."""
    obs = hp_today(data["hp"])
    hp = {i: [o.get("connections1d") or 0, o.get("uniqueIps1d"), TREND_CODE.get(o.get("trend"), ""), o.get("avg30d")]
          for i, o in sorted(obs.items()) if o.get("connections1d")}
    return {"date": today, "euvd_total": data["euvd_total"], "exploited": S["total"], "kev_dump": len(data["kev_dump"]),
            "eu_kev": len(S["dumbbell"]), "hp_seen": S["hp_with"], "hp_connections": sum(v[0] for v in hp.values()),
            "hp_uptick": sum(1 for o in obs.values() if o.get("trend") == "UPTICK"), "hp": hp}


def hp_days(text):
    """[(date, {id: (connections, ips, trend code, 30-day average)})] from history.jsonl, oldest first.
    Lines written before 2026-10-09 hold only the connections; the rest is None or ''."""
    out = []
    for ln in (text or "").splitlines():
        if ln.strip():
            r = json.loads(ln)
            out.append((r["date"], {i: (tuple(v) + (None, "", None))[:4] if isinstance(v, list) else (v, None, "", None)
                                    for i, v in (r.get("hp") or {}).items()}))
    return sorted(out)


def surge_kinds(day_rows, i):
    """Surge kinds of entry i on the last of `day_rows` ([(date, {id: values})], oldest first)."""
    if not day_rows or i not in day_rows[-1][1]:
        return []
    d1, ips, _, avg30 = day_rows[-1][1][i]
    kinds = []
    if avg30 is not None and ips is not None and d1 >= SURGE_RATIO * max(avg30, 1) and ips >= SURGE_IPS:
        kinds.append("broad")
    last = day_rows[-SURGE_DAYS:]
    if len(last) == SURGE_DAYS and all(i in m and m[i][2] == "U" for _, m in last):
        kinds.append("persistent")
    return kinds


def hp_surges(days_all, S):
    """Entries in a surge on the last recorded day; `new` when they were not in one of the same kind the
    recorded day before, so a long surge is reported once per kind."""
    if not days_all:
        return []
    meta = {r["id"]: r for r in S.get("hp_scatter", [])}
    out = []
    for i, (d1, ips, trend, avg30) in sorted(days_all[-1][1].items()):
        kinds = surge_kinds(days_all, i)
        if kinds:
            before = set(surge_kinds(days_all[:-1], i))
            m = meta.get(i, {})
            out.append({"id": i, "cve": m.get("cve", ""), "vendor": m.get("vendor", ""), "product": m.get("product", ""),
                        "kinds": kinds, "d1": d1, "ips": ips, "ratio": round(d1 / max(avg30 or 0, 1), 1),
                        "new": bool(set(kinds) - before)})
    return sorted(out, key=lambda r: -r["d1"])


def hp_heat(days_all, surges, limit=20, span=30):
    """Rows for the persistence heatmap: entries flagged UPTICK, or in a surge, on any of the last `span`
    recorded days; one cell per day, [connections / 30-day average or None, trend code]."""
    days = days_all[-span:]
    flagged = collections.Counter(i for _, m in days for i, v in m.items() if v[2] == "U")
    for s in surges:
        flagged[s["id"]] += 0
    rows = []
    for i in flagged:
        cells = [[round(m[i][0] / max(m[i][3], 1), 1) if i in m and m[i][3] is not None else None, m[i][2] if i in m else ""]
                 for _, m in days]
        rows.append({"id": i, "days": flagged[i], "cells": cells})
    rows.sort(key=lambda r: (-r["days"], -max((c[0] or 0) for c in r["cells"]), r["id"]))
    return {"days": [d for d, _ in days], "rows": rows[:limit], "n": len(rows)}


def merge_history(text, line):
    """history.jsonl with today's line added or replaced, sorted by date."""
    rows = {}
    for ln in (text or "").splitlines():
        if ln.strip():
            r = json.loads(ln)
            rows[r["date"]] = r
    rows[line["date"]] = line
    return "".join(json.dumps(rows[d], separators=(",", ":"), sort_keys=True) + "\n" for d in sorted(rows))


def history_series(text):
    """Small per-day series for the page (no per-entry data)."""
    out = []
    for ln in (text or "").splitlines():
        if ln.strip():
            r = json.loads(ln)
            out.append([r["date"], r["exploited"], r["euvd_total"], r["hp_seen"], r["hp_connections"], r.get("hp_uptick")])
    return out


# ---------- the page ----------

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>EUVD statistics</title>
<style>
:root{--bg:#f6f7f9;--card:#fff;--fg:#1b2230;--mut:#5d6677;--line:#dde1e8;--grid:#e9ecf1;--acc:#1f5fa8;
--cisa:#4b7fb8;--both:#2a9d8f;--eu:#e0a030;--up:#c0463a;--steady:#7d8798;--down:#3f8f5b;--note:#eef3fa}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#12161d;--card:#1a202a;--fg:#e4e8ee;--mut:#98a2b3;--line:#2c3441;--grid:#252c37;--acc:#7db2ee;
--cisa:#6a9fd6;--both:#3cb8a8;--eu:#e9b44c;--up:#e0675b;--steady:#8b95a7;--down:#5bb07a;--note:#1f2937}}
:root[data-theme="dark"]{--bg:#12161d;--card:#1a202a;--fg:#e4e8ee;--mut:#98a2b3;--line:#2c3441;--grid:#252c37;--acc:#7db2ee;
--cisa:#6a9fd6;--both:#3cb8a8;--eu:#e9b44c;--up:#e0675b;--steady:#8b95a7;--down:#5bb07a;--note:#1f2937}
*{box-sizing:border-box}body{margin:0;padding:1.2rem 16px 4rem;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:64rem;margin:0 auto}h1{font-size:1.6rem;margin:.2rem 0 .4rem}h2{font-size:1.15rem;margin:0 0 .2rem}
.lede{color:var(--mut);max-width:48rem}.tag{display:inline-block;font-size:.75rem;letter-spacing:.04em;text-transform:uppercase;color:var(--mut);border:1px solid var(--line);padding:0 .45rem;margin-right:.4rem}
section.p{background:var(--card);border:1px solid var(--line);padding:1rem 1.1rem 1.1rem;margin:1.1rem 0}
.src{font-size:.85rem;color:var(--mut);margin:.1rem 0 .7rem}.see{background:var(--note);border-left:3px solid var(--acc);padding:.5rem .8rem;margin:.8rem 0 0;font-size:.95rem}
.see b.h{display:block;font-size:.8rem;letter-spacing:.04em;text-transform:uppercase;color:var(--acc);margin-bottom:.15rem}
.limit{font-size:.88rem;color:var(--mut);margin:.5rem 0 0}
svg{width:100%;height:auto;display:block;font:11px system-ui,sans-serif}svg text{fill:var(--mut)}svg .t{fill:var(--fg)}
.leg{display:flex;flex-wrap:wrap;gap:.3rem 1rem;font-size:.85rem;color:var(--mut);margin:.3rem 0}.leg i{display:inline-block;width:.8rem;height:.8rem;margin-right:.3rem;vertical-align:-1px}
.scroll{max-height:680px;overflow:auto;border:1px solid var(--line)}
table{border-collapse:collapse;width:100%;font-size:.92rem}th,td{text-align:left;padding:.3rem .5rem;border-bottom:1px solid var(--line);vertical-align:top}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:1rem}@media(max-width:760px){.grid2{grid-template-columns:1fr}}
.tbl{overflow-x:auto}code{font-size:.85em}a{color:var(--acc)}td{font-variant-numeric:tabular-nums}
a:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
.crumbs{font-size:.9rem;color:var(--mut);margin:0 0 .4rem}.crumbs ol{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:.2rem .5rem}
.crumbs li+li::before{content:"›";margin-right:.5rem;color:var(--mut)}.crumbs [aria-current]{color:var(--fg)}
.toc{position:sticky;top:0;z-index:2;background:var(--bg);border-bottom:1px solid var(--line);margin:.8rem -16px 0;padding:0 16px;overflow-x:auto;white-space:nowrap}
.toc a{display:inline-flex;align-items:center;min-height:44px;padding:0 .5rem;text-decoration:none;font-size:.92rem}.toc a:first-child{padding-left:0}
h2.g{font-size:1.35rem;margin:2rem 0 .2rem;scroll-margin-top:3.5rem}.top{font-size:.85rem;margin:.4rem 0 0;text-align:right}
.swipe{display:none;font-size:.8rem;color:var(--mut);margin:.2rem 0}
@media(max-width:700px){.c{overflow-x:auto}.c svg.wide{min-width:800px}.swipe{display:block}h1{font-size:1.35rem}}
</style></head><body><main id="top">
<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="../index.html">SRP guide</a></li><li><a href="../index.html#euvd">EUVD</a></li><li><span aria-current="page">Statistics</span></li></ol></nav>
<h1>EUVD statistics</h1>
<p class="lede">Charts on the EU Vulnerability Database, regenerated every day by the monitor in this repository from the EUVD's own API, the CISA KEV catalogue and Shadowserver honeypot data as served by the EUVD. Data as of <span id="gen"></span>. Every panel says what it shows, where the data comes from and what it cannot show. None of it says how a vulnerability reached ENISA: no source records the reporting route. Raw data: <a href="stats.json">stats.json</a>; the exploited entries one by one: <a href="index.html">index.html</a>; the API: <a href="https://github.com/git-z0man/single-reporting-platform/blob/main/euvd/API.md">API.md</a>.</p>
<p class="lede" id="mode" style="font-size:.85rem"></p>
<nav class="toc" aria-label="Sections"><a href="#g1">The EUVD as a whole</a><a href="#g2">Flagged, and when</a><a href="#g3">EU KEV and the SRP</a><a href="#g4">What is exploited</a><a href="#g5">Honeypot sensors</a><a href="#g6">Monitor record</a><a href="index.html">Exploited entries &rarr;</a></nav>
<div id="panels"></div>
<script id="data" type="application/json">__DATA__</script>
<script>
__CHARTS__
</script></main></body></html>
"""


def render(S, charts_js):
    data = json.dumps(S, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    return PAGE.replace("__DATA__", data).replace("__CHARTS__", charts_js)


def prerender(path):
    """Draw the charts into the file with headless Chromium. Returns True when it worked."""
    node = shutil.which("node")
    if not node:
        return False
    env = dict(os.environ)
    env.setdefault("NODE_PATH", "/opt/node22/lib/node_modules")
    r = subprocess.run([node, os.path.join(HERE, "prerender.js"), path], capture_output=True, text=True, env=env, timeout=180)
    if r.returncode:
        print(f"prerender skipped: {(r.stderr or r.stdout).strip()[:300]}", file=sys.stderr)
        return False
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--today", default=None)
    ap.add_argument("--full", action="store_true", help="recount every month of the whole EUVD")
    ap.add_argument("--no-prerender", action="store_true")
    ap.add_argument("--data-file", help="read the fetched data from this JSON file instead of the network (tests)")
    ap.add_argument("--render-only", action="store_true", help="rebuild stats.html from the stored stats.json; no network")
    a = ap.parse_args(argv)
    today = a.today or dt.datetime.now(dt.timezone.utc).date().isoformat()
    stats_p, hist_p, page_p = (os.path.join(a.root, "euvd", n) for n in ("stats.json", "history.jsonl", "stats.html"))
    if a.render_only:
        S, charts = json.loads(ce.read(stats_p) or "null"), ce.read(os.path.join(HERE, "charts.js"))
        if not S or not charts:
            print("error: stats.json or charts.js missing", file=sys.stderr)
            return 2
        ce.write(page_p, render(S, charts))
        drawn = False if a.no_prerender else prerender(page_p)
        print(f"rendered, {'pre-rendered' if drawn else 'drawn in the browser'}")
        return 0
    try:
        old = json.loads(ce.read(stats_p) or "null")
        cached = (old or {}).get("_months")
        data = json.loads(ce.read(a.data_file)) if a.data_file else fetch_everything(today, cached, a.full)
        S = compute(data, today)
        hist = merge_history(ce.read(hist_p), history_line(S, data, today))
        S["history"] = history_series(hist)
        days_all = hp_days(hist)
        S["hp_surges"] = hp_surges(days_all, S)
        S["hp_heat"] = hp_heat(days_all, S["hp_surges"])
        S["_months"] = data["months"]
        charts = ce.read(os.path.join(HERE, "charts.js"))
        if not charts:
            raise StatsError("euvd/charts.js missing")
    except (StatsError, ce.CheckError, enrich.FetchError, OSError, ValueError, KeyError, TypeError) as e:
        print(f"error: {e!r}", file=sys.stderr)
        return 2
    ce.write(stats_p, json.dumps(S, indent=1, ensure_ascii=False, sort_keys=True) + "\n")
    ce.write(hist_p, hist)
    ce.write(page_p, render(S, charts))
    drawn = False if a.no_prerender else prerender(page_p)
    print(f"stats: {S['total']} exploited, {S['gen']['euvd_total']} EUVD records, {len(S['history'])} history days, "
          f"page {'pre-rendered' if drawn else 'drawn in the browser'}")
    new = [r for r in S["hp_surges"] if r["new"]]
    print(f"honeypot surges, new today: {len(new)} (in a surge: {len(S['hp_surges'])})")
    for r in new:
        print(f"  surge {'+'.join(r['kinds'])}: {r['id']} {r['cve']} {r['vendor']} {r['product']}: {r['d1']} connections "
              f"from {r['ips']} IPs, {r['ratio']}x the 30-day average")
    return 0


if __name__ == "__main__":
    sys.exit(main())
