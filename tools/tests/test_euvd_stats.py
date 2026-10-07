"""euvd/build_stats.py and euvd/charts.js on synthetic data (no network)."""
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location("build_stats", os.path.join(REPO, "euvd", "build_stats.py"))
bs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bs)

F = "%b %d, %Y, %I:%M:%S %p"


def d(s):  # "2026-09-20" -> EUVD date string
    import datetime as dt
    return dt.date.fromisoformat(s).strftime("%b %d, %Y, 12:00:00 AM")


def item(n, since, pub, vendor="Acme", score="9.8", epss="1.5"):
    return {"id": f"EUVD-2026-{n}", "exploitedSince": d(since), "datePublished": d(pub), "dateUpdated": d("2026-10-01"),
            "aliases": f"CVE-2026-{n}\n", "baseScore": score, "epss": epss, "enisaIdVendor": [{"vendor": {"name": vendor}}]}


def data():
    items = [item(1, "2026-09-20", "2026-09-01"), item(2, "2026-09-12", "2026-09-12", vendor="</script><b>x"),
             item(3, "2025-12-01", "2024-01-01", vendor="Other", epss="40")]
    kev_dump = [{"cveId": "CVE-2026-1", "euvdId": "EUVD-2026-1", "dateAdded": "2026-09-20", "sources": ["cisa_kev", "eukev_kev"]},
                {"cveId": "CVE-2026-2", "euvdId": "EUVD-2026-2", "dateAdded": "2026-09-12", "sources": ["eukev_kev"]},
                {"cveId": "CVE-2026-3", "euvdId": "EUVD-2026-3", "dateAdded": "2025-12-01", "sources": ["cisa_kev"]}]
    hp = {"EUVD-2026-1": [{"connections1d": 120, "avg7d": 10.0, "avg30d": 5.0, "avg90d": 2.0, "uniqueIps1d": 4, "trend": "UPTICK",
                           "vendor": "Acme", "product": "Box"}], "EUVD-2026-2": [], "EUVD-2026-3": []}
    eu = lambda date, origin: {"kevSource": {"code": "EUKEV"}, "dateAdded": d(date), "originSource": origin, "vendorProject": "Acme", "product": "Box", "cveId": "CVE"}
    ci = lambda date: {"kevSource": {"code": "CISA"}, "dateAdded": d(date)}
    kev_entries = {"EUVD-2026-1": [eu("2026-09-18", "NCSC-NL"), ci("2026-09-20")], "EUVD-2026-2": [eu("2026-09-12", "cnw")]}
    cisa = {"CVE-2026-1": {"cveID": "CVE-2026-1", "dateAdded": "2026-09-20", "dueDate": "2026-09-23", "forensicTriage": "Yes",
                           "knownRansomwareCampaignUse": "Known", "cwes": ["CWE-78"]},
            "CVE-2026-3": {"cveID": "CVE-2026-3", "dateAdded": "2025-12-01", "dueDate": "2025-12-22", "knownRansomwareCampaignUse": "Unknown", "cwes": []}}
    months = {s: {m: 5 for m, _, _ in bs.month_windows("2026-10-07")} for s in ["all", "crit"] + [a for a, _ in bs.ASSIGNERS]}
    totals = {a: 10 for a, _ in bs.ASSIGNERS + bs.GLOBAL}
    detail = [dict(item(9, "2026-01-01", "2026-01-01"), id="EUVD-2026-9", exploitedSince=None)]
    return dict(items=items, kev_dump=kev_dump, hp=hp, kev_entries=kev_entries, cisa=cisa, months=months, totals=totals,
                euvd_total=1000, detail=detail)


class Case(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.root, "euvd"))
        self.addCleanup(shutil.rmtree, self.root)
        self.df = os.path.join(self.root, "data.json")
        json.dump(data(), open(self.df, "w"))

    def run_build(self, today="2026-10-07", *extra):
        return bs.main(["--root", self.root, "--data-file", self.df, "--today", today, "--no-prerender", *extra])

    def read(self, name):
        return open(os.path.join(self.root, "euvd", name), encoding="utf-8").read()

    def test_writes_stats_history_and_page(self):
        self.assertEqual(self.run_build(), 0)
        S = json.loads(self.read("stats.json"))
        self.assertEqual(S["total"], 3)
        self.assertEqual(S["origin_after"][0][2], "CSIRTs Network")       # cnw normalised
        self.assertEqual([r[0] for r in S["origin"]][:2], ["CSIRTs Network", "NCSC-NL"])
        self.assertEqual(S["lead"]["recent"]["eu_first"], 1)               # EU KEV two days before CISA
        self.assertEqual({r[0]: r[1] for r in S["urgency"]}["2026-09"], 1)   # one 3-day window in Sep 2026
        self.assertEqual(S["gen"]["detail"]["n"], 1)
        page = self.read("stats.html")
        self.assertIn('<script id="data" type="application/json">', page)
        self.assertNotIn("</script><b>x", page)                            # embedded JSON cannot close the script
        self.assertIn("EUVD statistics", page)

    def test_history_one_line_per_day(self):
        self.run_build("2026-10-07")
        self.run_build("2026-10-07")
        self.assertEqual(len(self.read("history.jsonl").splitlines()), 1)
        self.run_build("2026-10-08")
        lines = [json.loads(x) for x in self.read("history.jsonl").splitlines()]
        self.assertEqual([x["date"] for x in lines], ["2026-10-07", "2026-10-08"])
        self.assertEqual(lines[0]["hp"], {"EUVD-2026-1": 120})
        self.assertEqual(len(json.loads(self.read("stats.json"))["history"]), 2)

    def test_month_cache_recounts_only_recent_months(self):
        calls = []
        orig = bs.search_total
        bs.search_total = lambda q: calls.append(q) or 7
        self.addCleanup(setattr, bs, "search_total", orig)
        cached = {s: {m: 1 for m, _, _ in bs.month_windows("2026-10-07")} for s in ["all", "crit"] + [a for a, _ in bs.ASSIGNERS]}
        out = bs.count_months("2026-10-07", cached, full=False)
        self.assertEqual(len(calls), 2 * (2 + len(bs.ASSIGNERS)))         # current and previous month only
        self.assertEqual(out["all"]["2026-10"], 7)
        self.assertEqual(out["all"]["2026-01"], 1)

    def test_failed_fetch_writes_nothing(self):
        orig = bs.fetch_everything
        def boom(*a):
            raise bs.StatsError("HTTP 429")
        bs.fetch_everything = boom
        self.addCleanup(setattr, bs, "fetch_everything", orig)
        self.assertEqual(bs.main(["--root", self.root, "--today", "2026-10-07", "--no-prerender"]), 2)
        self.assertFalse(os.path.exists(os.path.join(self.root, "euvd", "stats.json")))

    @unittest.skipUnless(shutil.which("node") and os.path.isdir("/opt/node22/lib/node_modules/playwright"), "node/Playwright not available")
    def test_every_panel_draws_from_sparse_data(self):
        self.run_build()
        page = os.path.join(self.root, "euvd", "stats.html")
        env = dict(os.environ, NODE_PATH="/opt/node22/lib/node_modules")
        r = subprocess.run(["node", os.path.join(REPO, "euvd", "prerender.js"), page], capture_output=True, text=True, env=env, timeout=120)
        self.assertEqual(r.returncode, 0, r.stderr)
        html = open(page, encoding="utf-8").read()
        self.assertNotIn("could not be drawn", html)
        self.assertNotIn("<script", html)
        self.assertEqual(html.count('class="p"'), 19)


if __name__ == "__main__":
    unittest.main()
