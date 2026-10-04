"""euvd/check_exploited.py: change detection and the detail page on synthetic answers (no network)."""
import importlib.util
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


class Case(unittest.TestCase):
    def setUp(self):
        FETCHED.clear()
        self.catalog = {"CVE-2026-5001": {"cveID": "CVE-2026-5001", "dateAdded": "2026-09-12", "vulnerabilityName": "N",
                                          "vendorProject": "Acme", "forensicTriage": "No", "futureField": "x"}}
        for name, fn in (("euvd_record", fake_euvd), ("nvd_record", fake_nvd), ("cisa_catalog", lambda: self.catalog)):
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

    def test_render_only_needs_no_network(self):
        self.run_check(base_items())
        FETCHED.clear()
        self.assertEqual(ce.main(["--root", self.root, "--render-only"]), 0)
        self.assertEqual(FETCHED, [])


if __name__ == "__main__":
    unittest.main()
