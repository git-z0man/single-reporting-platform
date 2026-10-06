"""euvd/check_exploited.py: change detection and the detail page on synthetic answers (no network)."""
import contextlib
import importlib.util
import io
import json
import os
import shutil
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location("check_exploited", os.path.join(REPO, "euvd", "check_exploited.py"))
ce = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ce)

FETCHED = []
REAL_HONEYPOT_BATCH = ce.enrich.honeypot_batch


def item(n, since="Sep 12, 2026, 12:00:00 AM", updated="Sep 13, 2026, 3:00:00 AM", vendor="Acme"):
    return {"id": f"EUVD-2026-{n}", "exploitedSince": since, "datePublished": "Sep 10, 2026, 1:00:00 PM",
            "dateUpdated": updated, "aliases": f"CVE-2026-{n}\n", "assigner": "acme",
            "enisaIdVendor": [{"vendor": {"name": vendor}}]}


def base_items():
    old = [item(i, since="Jan 5, 2025, 12:00:00 AM") for i in range(1, 1001)]   # filler, outside the window
    return old + [item(5001), item(5002, since="Sep 2, 2026, 12:00:00 AM")]


def fake_euvd(i):
    FETCHED.append(("euvd", i))
    return {"id": i, "description": "<script>alert(1)</script> bad", "epss": 1.5, "dataProcessed": "today",
            "references": "https://cert.europa.eu/x https://example.org/y", "aliases": "CVE-2026-1\n",
            "baseScore": 7.5, "baseScoreVersion": "3.1", "exploitedSince": "Sep 12, 2026, 12:00:00 AM",
            "enisaIdProduct": [{"product": {"name": "P", "vendor": {"name": "V"}}, "product_version": "<2"}],
            "enisaIdAdvisory": [{"advisory": {"id": "WID-SEC-1", "source": {"id": 8, "name": "csaf_certbund"},
                                              "description": "cert advisory", "references": "https://wid.cert-bund.de/a"}},
                                {"advisory": {"id": "RHSA-1", "source": {"id": 9, "name": "csaf_redhat"},
                                              "description": "vendor advisory"}}]}


def fake_nvd(cve):
    FETCHED.append(("nvd", cve))
    return {"id": cve, "vulnStatus": "Analyzed", "descriptions": [{"lang": "en", "value": "nvd text"}],
            "metrics": {}, "weaknesses": [], "references": [{"url": "https://cvcn.gov.it/a"}]}


def obs(**kw):
    return {"cveId": "CVE-2026-5001", "source": "shadowserver", "firstSeenAt": "Oct 1, 2026, 3:00:00 AM",
            "lastSeenAt": "Oct 5, 2026, 7:00:00 AM", "connections1d": 4, "uniqueIps1d": 1, "avg7d": 1.0, "avg30d": 0.0,
            "avg90d": 0.0, "vendor": "Acme", "product": "Widget", "vulnClass": "other-software", "trend": "STEADY",
            "isNew": False, **kw}


def kev(code, date):
    return {"id": 1, "cveId": "CVE-x", "kevSource": {"code": code, "displayName": code}, "dateAdded": date + ", 12:00:00 AM"}


class Case(unittest.TestCase):
    def setUp(self):
        FETCHED.clear()
        self.catalog = {"CVE-2026-5001": {"cveID": "CVE-2026-5001", "dateAdded": "2026-09-12", "vulnerabilityName": "N",
                                          "vendorProject": "Acme", "forensicTriage": "No", "futureField": "x"}}
        self.hp, self.ks = {}, {}
        for name, fn in (("euvd_record", fake_euvd), ("nvd_record", fake_nvd), ("cisa_catalog", lambda: self.catalog),
                         ("honeypot_batch", lambda ids: {i: self.hp.get(i, []) for i in ids}),
                         ("kev_batch", lambda ids: {i: self.ks.get(i, []) for i in ids})):
            old = getattr(ce.enrich, name)
            setattr(ce.enrich, name, fn)
            self.addCleanup(setattr, ce.enrich, name, old)
        self.root = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.root, "euvd"))
        shutil.copy(os.path.join(REPO, "euvd-exploited-baseline.md"), os.path.join(self.root, "euvd-exploited-baseline.md"))
        self.addCleanup(shutil.rmtree, self.root)

    def run_check(self, items, kev=None, *extra):
        ip, kp = os.path.join(self.root, "items.json"), os.path.join(self.root, "kev.json")
        json.dump(items, open(ip, "w"))
        json.dump(kev or {}, open(kp, "w"))
        return ce.main(["--root", self.root, "--items-file", ip, "--kev-file", kp, "--today", "2026-10-05", *extra])

    def state(self):
        return json.load(open(os.path.join(self.root, "euvd", "exploited.json")))

    def md(self):
        return open(os.path.join(self.root, "euvd-exploited-baseline.md"), encoding="utf-8").read()

    def page(self):
        return open(os.path.join(self.root, "euvd", "index.html"), encoding="utf-8").read()

    def test_first_run_writes_then_is_quiet(self):
        self.assertEqual(self.run_check(base_items()), 1)
        self.assertEqual([e["id"] for e in self.state()["entries"]], ["EUVD-2026-5002", "EUVD-2026-5001"])
        self.assertIn("EUVD-2026-5001", self.md())
        self.assertIn("last_change: 2026-10-05", self.md())
        self.assertEqual(self.run_check(base_items()), 0)

    def test_new_entry_is_a_change(self):
        self.run_check(base_items())
        self.assertEqual(self.run_check(base_items() + [item(5003)]), 1)
        self.assertIn("EUVD-2026-5003", [e["id"] for e in self.state()["entries"]])

    def test_removed_entry_is_a_change_and_loses_its_detail_file(self):
        self.run_check(base_items())
        self.assertEqual(self.run_check(base_items()[:-1]), 1)
        self.assertNotIn("EUVD-2026-5002", [e["id"] for e in self.state()["entries"]])
        self.assertFalse(os.path.exists(os.path.join(self.root, "euvd", "details", "EUVD-2026-5002.json")))

    def test_update_to_an_entry_is_a_change(self):
        self.run_check(base_items())
        items = base_items()
        items[-1] = item(5002, since="Sep 2, 2026, 12:00:00 AM", updated="Oct 4, 2026, 9:00:00 AM")
        self.assertEqual(self.run_check(items), 1)

    def test_kev_event_pulls_in_an_old_entry(self):
        self.assertEqual(self.run_check(base_items(), {"2026-09-21": ["EUVD-2026-7"]}), 1)
        e = {x["id"]: x for x in self.state()["entries"]}["EUVD-2026-7"]
        self.assertEqual(e["kev"], ["2026-09-21"])

    def test_kev_event_for_unknown_entry_fails(self):
        self.assertEqual(self.run_check(base_items(), {"2026-09-21": ["EUVD-2026-99999"]}), 2)
        self.assertFalse(os.path.exists(os.path.join(self.root, "euvd", "exploited.json")))

    def test_small_answer_is_a_failure_not_a_change(self):
        self.run_check(base_items())
        before = self.md()
        self.assertEqual(self.run_check(base_items()[:50]), 2)
        self.assertEqual(self.md(), before)

    def test_heartbeat_moves_only_last_check(self):
        self.run_check(base_items())
        before = self.md()
        self.assertEqual(ce.main(["--root", self.root, "--items-file", os.path.join(self.root, "items.json"),
                                  "--kev-file", os.path.join(self.root, "kev.json"), "--today", "2026-10-06",
                                  "--heartbeat"]), 0)
        after = self.md()
        self.assertIn("last_check: 2026-10-06", after)
        self.assertEqual(after.replace("last_check: 2026-10-06", "last_check: 2026-10-05"), before)

    def test_dry_run_writes_nothing(self):
        self.assertEqual(self.run_check(base_items(), None, "--dry-run"), 1)
        self.assertFalse(os.path.exists(os.path.join(self.root, "euvd", "exploited.json")))

    def test_baseline_without_markers_fails(self):
        open(os.path.join(self.root, "euvd-exploited-baseline.md"), "w").write("---\nlast_check: x\n---\nno markers\n")
        self.assertEqual(self.run_check(base_items()), 2)

    # --- details from the other sources ---

    def test_details_fetched_once_then_only_when_the_entry_moves(self):
        self.run_check(base_items())
        self.assertEqual([k for k, _ in FETCHED].count("euvd"), 2)
        FETCHED.clear()
        self.run_check(base_items())
        self.assertEqual(FETCHED, [])
        items = base_items()
        items[-1] = item(5002, since="Sep 2, 2026, 12:00:00 AM", updated="Oct 4, 2026, 9:00:00 AM")
        self.run_check(items)
        self.assertEqual(FETCHED, [("euvd", "EUVD-2026-5002"), ("nvd", "CVE-2026-5002")])

    def test_volatile_fields_are_not_a_change(self):
        self.run_check(base_items())
        orig = ce.enrich.euvd_record
        ce.enrich.euvd_record = lambda i: {**fake_euvd(i), "epss": 99.9, "dataProcessed": "tomorrow"}
        self.addCleanup(setattr, ce.enrich, "euvd_record", orig)
        self.assertEqual(self.run_check(base_items(), None, "--refresh"), 0)

    def test_cisa_entry_change_is_a_change(self):
        self.run_check(base_items())
        self.catalog["CVE-2026-5001"] = {**self.catalog["CVE-2026-5001"], "dueDate": "2026-10-03"}
        self.assertEqual(self.run_check(base_items()), 1)

    def test_page_shows_all_sources_and_escapes_text(self):
        self.run_check(base_items())
        page = self.page()
        for needle in ("NIST NVD", "CISA KEV catalogue", "CERT-EU", "CVCN (IT)", "Advisories from CERTs", "cert advisory",
                       "Vendor advisories", "Forensic triage", "futureField",     # new CISA fields still show
                       "not in CISA KEV",                                         # entry 5002 is not in the catalogue
                       "&lt;script&gt;alert(1)&lt;/script&gt;"):
            self.assertIn(needle, page)
        self.assertNotIn("<script>alert(1)", page)

    # --- honeypot sensors ---

    def test_first_honeypot_sighting_is_a_change(self):
        self.run_check(base_items())
        self.hp["EUVD-2026-5001"] = [obs()]
        self.assertEqual(self.run_check(base_items()), 1)
        self.assertEqual({e["id"]: e["honeypot"] for e in self.state()["entries"]}["EUVD-2026-5001"], "2026-10-01")
        self.assertIn("| CVE-2026-5001 | 2026-10-01 |", self.md())
        self.assertIn("seen in honeypot", self.page())
        self.assertIn("Honeypot sensors (Shadowserver, via EUVD)", self.page())

    def test_honeypot_counts_are_not_a_change_but_the_heartbeat_records_them(self):
        self.hp["EUVD-2026-5001"] = [obs()]
        self.run_check(base_items())
        self.hp["EUVD-2026-5001"] = [obs(connections1d=3331, trend="UPTICK", lastSeenAt="Oct 6, 2026, 7:11:51 AM")]
        before = self.md()
        self.assertEqual(self.run_check(base_items(), None, "--heartbeat"), 0)
        self.assertEqual(self.md().replace("last_check: 2026-10-05", "x"), before.replace("last_check: 2026-10-05", "x"))
        det = json.load(open(os.path.join(self.root, "euvd", "details", "EUVD-2026-5001.json")))
        self.assertEqual(det["honeypot"][0]["connections1d"], 3331)
        self.assertIn("3331 connections", self.page())

    def test_honeypot_without_first_seen_fails(self):
        self.hp["EUVD-2026-5001"] = [{"cveId": "CVE-2026-5001"}]
        self.assertEqual(self.run_check(base_items()), 2)
        self.assertFalse(os.path.exists(os.path.join(self.root, "euvd", "exploited.json")))

    def test_incomplete_honeypot_answer_is_a_failed_fetch(self):
        orig = ce.enrich._get
        self.addCleanup(setattr, ce.enrich, "_get", orig)
        ce.enrich._get = lambda url: json.dumps({"EUVD-2026-1": []})
        with self.assertRaises(ce.enrich.FetchError):
            REAL_HONEYPOT_BATCH(["EUVD-2026-1", "EUVD-2026-2"])
        ce.enrich._get = lambda url: json.dumps({"EUVD-2026-1": ["x"]})
        with self.assertRaises(ce.enrich.FetchError):
            REAL_HONEYPOT_BATCH(["EUVD-2026-1"])

    # --- KEV per source and SRP candidates ---

    def test_eu_kev_before_cisa_after_go_live_is_a_candidate(self):
        self.run_check(base_items())
        self.ks["EUVD-2026-5001"] = [kev("EUKEV", "Sep 23, 2026"), kev("CISA", "Sep 25, 2026")]
        self.ks["EUVD-2026-5002"] = [kev("EUKEV", "Sep 22, 2026"), kev("CISA", "Sep 22, 2026")]    # same day: no
        self.assertEqual(self.run_check(base_items(), None, "--json"), 1)
        e = {x["id"]: x for x in self.state()["entries"]}
        self.assertEqual(e["EUVD-2026-5001"]["candidate"], "EU KEV 2 days before CISA")
        self.assertEqual(e["EUVD-2026-5001"]["kev_sources"], {"CISA": "2026-09-25", "EUKEV": "2026-09-23"})
        self.assertEqual(e["EUVD-2026-5002"]["candidate"], "")
        self.assertIn("## SRP candidates (indications, not findings)", self.md())
        self.assertIn("| 2026-09-23 | 2026-09-25 | EU KEV 2 days before CISA | Acme | acme | yes |", self.md())
        self.assertIn("SRP candidate (indication only)", self.page())

    def test_eu_only_counts_but_not_before_go_live(self):
        self.ks["EUVD-2026-5001"] = [kev("EUKEV", "Sep 12, 2026")]
        self.ks["EUVD-2026-5002"] = [kev("EUKEV", "Sep 10, 2026")]
        self.run_check(base_items())
        e = {x["id"]: x for x in self.state()["entries"]}
        self.assertEqual(e["EUVD-2026-5001"]["candidate"], "EU KEV only")
        self.assertEqual(e["EUVD-2026-5002"]["candidate"], "")

    def test_new_candidate_is_reported(self):
        self.run_check(base_items())
        self.ks["EUVD-2026-5001"] = [kev("EUKEV", "Oct 1, 2026")]
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(self.run_check(base_items(), None, "--json"), 1)
        self.assertEqual(json.loads(out.getvalue())["srp_candidates_new"], ["EUVD-2026-5001"])

    def test_vendor_is_assigner(self):
        row = lambda v, a: {"vendor": v, "assigner": a}
        self.assertTrue(ce.vendor_is_assigner(row("Citrix NetScaler", "NetScaler")))
        self.assertTrue(ce.vendor_is_assigner(row("Arista Networks", "Arista")))
        self.assertFalse(ce.vendor_is_assigner(row("Zammad GmbH", "DIVD")))
        self.assertFalse(ce.vendor_is_assigner(row("", "")))

    def test_render_only_needs_no_network(self):
        self.run_check(base_items())
        FETCHED.clear()
        self.assertEqual(ce.main(["--root", self.root, "--render-only"]), 0)
        self.assertEqual(FETCHED, [])


if __name__ == "__main__":
    unittest.main()
