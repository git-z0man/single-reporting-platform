"""euvd/build_stats.py and euvd/charts.js on synthetic data (no network)."""
import importlib.util
import json
import os
import re
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
                           "vendor": "Acme", "product": "Box", "cveId": "CVE-2026-1", "firstSeenAt": d("2026-09-15")}],
          "EUVD-2026-2": [], "EUVD-2026-3": [{"cveId": "CVE-2026-3", "firstSeenAt": d("2022-06-23"), "trend": "STEADY"}]}
    eu = lambda date, origin: {"kevSource": {"code": "EUKEV"}, "dateAdded": d(date), "originSource": origin, "vendorProject": "Acme", "product": "Box", "cveId": "CVE"}
    ci = lambda date: {"kevSource": {"code": "CISA"}, "dateAdded": d(date)}
    kev_entries = {"EUVD-2026-1": [eu("2026-09-18", "NCSC-NL"), ci("2026-09-20")], "EUVD-2026-2": [eu("2026-09-12", "cnw")]}
    cisa = {"CVE-2026-1": {"cveID": "CVE-2026-1", "dateAdded": "2026-09-20", "dueDate": "2026-09-23", "forensicTriage": "Yes",
                           "knownRansomwareCampaignUse": "Known", "cwes": ["CWE-78"]},
            "CVE-2026-3": {"cveID": "CVE-2026-3", "dateAdded": "2025-12-01", "dueDate": "2025-12-22", "knownRansomwareCampaignUse": "Unknown", "cwes": []}}
    months = {s: {m: 5 for m, _, _ in bs.month_windows("2026-10-07")} for s in ["all", "crit"] + [a for a, _ in bs.ASSIGNERS]}
    totals = {a: 10 for a, _ in bs.ASSIGNERS + bs.GLOBAL}
    detail = {"CERTVDE": [dict(item(9, "2026-01-01", "2026-01-01"), id="EUVD-2026-9", exploitedSince=None)],
              "CERT-PL": [dict(item(8, "2026-01-01", "2025-03-01", vendor="Pol"), id="EUVD-2026-8", exploitedSince=None)],
              "INCIBE": [], "CIRCL": [dict(item(1, "2026-09-20", "2026-09-01"), id="EUVD-2026-1")]}
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
        self.assertEqual(S["ft_windows"], [[3, 1]])                       # the triage mark goes with the 3-day window
        self.assertEqual(S["ft_hp"]["marked"], [1, [120]])                # marked, added since the directive, seen by sensors
        self.assertEqual(S["ft_hp"]["plain"], [0, []])                    # CVE-2026-3 predates the directive, CVE-2026-2 is not CISA
        self.assertEqual(S["gen"]["detail"]["n"], 1)
        self.assertEqual([(v["assigner"], v["n"], v["exploited"]) for v in S["gen"]["details"]],
                         [("CERTVDE", 1, 0), ("CERT-PL", 1, 0), ("INCIBE", 0, 0), ("CIRCL", 1, 1)])
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
        self.assertEqual(lines[0]["hp"], {"EUVD-2026-1": [120, 4, "U", 5.0]})
        self.assertEqual(lines[0]["hp_uptick"], 1)
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
        self.assertEqual(html.count('class="p"'), 26)
        self.assertEqual(html.count('<h2 class="g"'), 6)
        titles = re.findall(r'<h2><span class="tag">[^<]*</span>\d+\. (.*?)</h2>', html)
        self.assertEqual(len(titles), 26)
        self.assertEqual(len(set(titles)), 26, "a panel appears twice")
        for i in range(1, 7):
            self.assertIn(f'href="#g{i}"', html)
            self.assertIn(f'id="g{i}"', html)
        self.assertIn('aria-label="Breadcrumb"', html)


def hist_line(date, hp):
    return json.dumps({"date": date, "exploited": 1, "euvd_total": 1, "hp_seen": 1, "hp_connections": 1, "hp": hp})


class Honeypot(unittest.TestCase):
    def test_old_and_new_history_lines_read_alike(self):
        text = "\n".join([hist_line("2026-10-08", {"EUVD-1": 50}), hist_line("2026-10-07", {"EUVD-1": 40}),
                          hist_line("2026-10-09", {"EUVD-1": [60, 30, "U", 2.0]})])
        days = bs.hp_days(text)
        self.assertEqual([d for d, _ in days], ["2026-10-07", "2026-10-08", "2026-10-09"])
        self.assertEqual(days[0][1]["EUVD-1"], (40, None, "", None))
        self.assertEqual(days[2][1]["EUVD-1"], (60, 30, "U", 2.0))

    def test_broad_surge_needs_ratio_against_own_level_and_addresses_and_is_new_once(self):
        D = lambda *v: dict(zip(["A", "B"], v))
        days = [(f"2026-10-0{n}", D((100, 30, "S", 10.0), (500, 30, "S", 10.0))) for n in (5, 6, 7, 8)]
        days.append(("2026-10-09", D((1000, 30, "U", 10.0), (5000, 5, "U", 10.0))))
        s = bs.hp_surges(days, {})
        self.assertEqual([(r["id"], r["kinds"], r["base"], r["ratio"], r["new"]) for r in s],
                         [("A", ["broad"], 100, 10.0, True)])                                    # B: too few addresses
        days.append(("2026-10-10", D((1000, 40, "S", 10.0), (10, 2, "S", 10.0))))
        self.assertEqual([(r["id"], r["new"]) for r in bs.hp_surges(days, {})], [("A", False)])
        days.append(("2026-10-11", D((900, 40, "S", 10.0), (10, 2, "S", 10.0))))               # 9x its level: no longer broad,
        self.assertEqual([(r["id"], r["kinds"], r["new"]) for r in bs.hp_surges(days, {})],    # but held three days
                         [("A", ["persistent"], True)])

    def test_steady_entry_far_above_the_euvd_average_is_no_surge(self):
        # NetScaler on 2026-10-10..13: thousands of connections a day against an avg30d of 25-28.
        days = [(f"2026-10-0{n}", {"A": (6000 + 100 * n, 50, "U", 27.0)}) for n in range(1, 8)]
        self.assertEqual(bs.hp_surges(days, {}), [])

    def test_no_surge_without_enough_recorded_days(self):
        days = [(f"2026-10-0{n}", {"A": (10, 30, "S", 1.0)}) for n in (6, 7, 8)]
        days.append(("2026-10-09", {"A": (5000, 300, "U", 1.0)}))
        self.assertIsNone(bs.own_base(days, "A", 3))
        self.assertEqual(bs.hp_surges(days, {}), [])

    def test_persistent_surge_needs_a_level_held_three_days(self):
        days = [(f"2026-10-0{n}", {"A": (20, 12, "S", 10.0), "B": (2, 2, "U", 1.0)}) for n in (3, 4, 5, 6)]
        for n in (7, 8):
            days.append((f"2026-10-0{n}", {"A": (150, 12, "S", 10.0), "B": (2, 2, "U", 1.0)}))
        self.assertEqual(bs.hp_surges(days, {}), [])
        days.append(("2026-10-09", {"A": (150, 12, "S", 10.0), "B": (2, 2, "U", 1.0)}))
        s = bs.hp_surges(days, {})
        self.assertEqual([(r["id"], r["kinds"], r["new"]) for r in s], [("A", ["persistent"], True)])   # B: UPTICK alone is not enough
        self.assertEqual((s[0]["base"], s[0]["base_days"], s[0]["ratio"]), (20, 4, 7.5))              # the level before the run
        days.append(("2026-10-10", {"A": (150, 5, "S", 10.0)}))                                        # too few sources today
        self.assertEqual(bs.hp_surges(days, {}), [])
        heat = bs.hp_heat(days, [])
        self.assertEqual((heat["n"], heat["rows"][0]["id"], heat["rows"][0]["days"]), (1, "A", 3))
        self.assertEqual(heat["rows"][0]["cells"][4], [7.5, "S"])                                  # 150 against a level of 20

    def test_first_sighting_on_the_sensors_first_day_is_not_a_lead(self):
        S = bs.compute(data(), "2026-10-07")
        L = S["hp_lead"]
        self.assertEqual((L["n"], L["start"], L["censored"]), (2, "2022-06-23", 1))
        self.assertEqual(dict(L["buckets"])["1-30 days before"], 1)                               # seen 15 Sep, flagged 20 Sep
        self.assertEqual([(r["id"], r["lead"], r["censored"]) for r in L["recent"]], [("EUVD-2026-1", 5, False)])

    @unittest.skipUnless(shutil.which("node") and os.path.isdir("/opt/node22/lib/node_modules/playwright"), "node/Playwright not available")
    def test_old_stats_json_with_one_profile_still_draws(self):
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root)
        os.makedirs(os.path.join(root, "euvd"))
        S = bs.compute(data(), "2026-10-07")
        S["gen"].pop("details")
        S["history"], S["hp_surges"], S["hp_heat"] = [], [], {"days": [], "rows": [], "n": 0}
        json.dump(S, open(os.path.join(root, "euvd", "stats.json"), "w"))
        self.assertEqual(bs.main(["--root", root, "--render-only"]), 0)
        html = open(os.path.join(root, "euvd", "stats.html"), encoding="utf-8").read()
        self.assertNotIn("could not be drawn", html)
        self.assertEqual(html.count('class="p"'), 22)

    def test_pages_have_breadcrumbs_and_relative_links_resolve(self):
        import enrich
        for page in (bs.PAGE, enrich.PAGE):
            self.assertIn('aria-label="Breadcrumb"', page)
            self.assertIn('<header class="bar"><nav class="crumbs"', page)                      # the breadcrumb stays visible
            self.assertRegex(page, r'\.bar\{position:-webkit-sticky;position:sticky;top:0')
            for href in re.findall(r'href="([^"#:]+)(?:#[^"]*)?"', page):
                self.assertTrue(os.path.exists(os.path.join(REPO, "euvd", href)), href)


if __name__ == "__main__":
    unittest.main()
