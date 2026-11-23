import contextlib
import io
import json
import os
import unittest

from tools.tests import helpers as H

fe = __import__("fetch_enisa")


def run(root, faq_file, gl_file, *extra):
    return fe.main(["--root", root, "--faq-file", faq_file, "--glossary-file", gl_file, "--today", "2026-10-05", *extra])


class Fetch(unittest.TestCase):
    def setUp(self):
        self.root = H.make_root(*H.extracts())
        os.remove(os.path.join(self.root, "guide-sync", "faq.json"))
        os.remove(os.path.join(self.root, "guide-sync", "glossary.json"))
        self.faq_f = os.path.join(H.FIXTURES, "faq_dl.html")
        self.gl_f = os.path.join(H.FIXTURES, "glossary_table.html")

    def load(self, name):
        with open(os.path.join(self.root, "guide-sync", name), encoding="utf-8") as fh:
            return json.load(fh)

    def test_first_run_writes_and_second_run_changes_nothing(self):
        self.assertEqual(run(self.root, self.faq_f, self.gl_f), 1)
        self.assertEqual(len(self.load("faq.json")["questions"]), 33)
        self.assertEqual(len(self.load("glossary.json")["fields"]), 42)
        before = self.load("faq.json")
        self.assertEqual(run(self.root, self.faq_f, self.gl_f), 0)
        self.assertEqual(self.load("faq.json"), before)

    def test_markup_only_changes_leave_the_stored_entry_alone(self):
        run(self.root, self.faq_f, self.gl_f)
        stored = self.load("faq.json")["questions"][0]["html"]
        with open(self.faq_f, encoding="utf-8") as fh:
            churned = fh.read().replace("<p>The CRA Single Reporting Platform (SRP)", "<p><strong> </strong>The CRA Single Reporting Platform (SRP)", 1)
        alt = os.path.join(self.root, "faq_churned.html")
        with open(alt, "w", encoding="utf-8") as fh:
            fh.write(churned)
        self.assertEqual(run(self.root, alt, self.gl_f), 0)
        self.assertEqual(self.load("faq.json")["questions"][0]["html"], stored)

    def test_a_wording_change_is_written_and_named(self):
        run(self.root, self.faq_f, self.gl_f)
        with open(self.faq_f, encoding="utf-8") as fh:
            changed = fh.read().replace("Under the CRA, manufacturers placing on the EU market", "Under the CRA, all manufacturers", 1)
        alt = os.path.join(self.root, "faq_changed.html")
        with open(alt, "w", encoding="utf-8") as fh:
            fh.write(changed)
        self.assertEqual(run(self.root, alt, self.gl_f), 1)
        self.assertIn("all manufacturers", self.load("faq.json")["questions"][4]["html"])
        self.assertEqual(self.load("faq.json")["fetched"], "2026-10-05")

    def test_dry_run_writes_nothing(self):
        self.assertEqual(run(self.root, self.faq_f, self.gl_f, "--dry-run"), 1)
        self.assertFalse(os.path.exists(os.path.join(self.root, "guide-sync", "faq.json")))

    def test_an_unreadable_page_is_an_error_and_writes_nothing(self):
        bad = os.path.join(self.root, "bad.html")
        with open(bad, "w", encoding="utf-8") as fh:
            fh.write("<html>Service unavailable</html>")
        self.assertEqual(run(self.root, bad, self.gl_f), 2)
        self.assertFalse(os.path.exists(os.path.join(self.root, "guide-sync", "glossary.json")))

    def test_the_faq_stamp_alone_is_not_a_change(self):
        run(self.root, self.faq_f, self.gl_f)
        with open(self.faq_f, encoding="utf-8") as fh:
            alt_text = fh.read().replace("Updated: 03 October 2026", "Updated: 09 October 2026")
        alt = os.path.join(self.root, "faq_stamp.html")
        with open(alt, "w", encoding="utf-8") as fh:
            fh.write(alt_text)
        self.assertEqual(run(self.root, alt, self.gl_f), 0)


class SourceAnomaly(unittest.TestCase):
    """ENISA printed the 36th question as "26." (captured 2026-11-23)."""

    def setUp(self):
        self.root = H.make_root(*H.extracts())
        os.remove(os.path.join(self.root, "guide-sync", "faq.json"))
        os.remove(os.path.join(self.root, "guide-sync", "glossary.json"))
        self.faq_f = os.path.join(H.FIXTURES, "faq_dl_36.html")
        self.gl_f = os.path.join(H.FIXTURES, "glossary_table_1_6.html")

    def load(self, name):
        with open(os.path.join(self.root, "guide-sync", name), encoding="utf-8") as fh:
            return json.load(fh)

    def run_quiet(self, faq_f):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = run(self.root, faq_f, self.gl_f)
        return code, out.getvalue()

    def test_the_duplicate_is_stored_as_q36_and_reported(self):
        code, out = self.run_quiet(self.faq_f)
        self.assertEqual(code, 1)
        faq = self.load("faq.json")
        self.assertEqual([q["n"] for q in faq["questions"]], list(range(1, 37)))
        self.assertEqual([(a["n"], a["source_n"]) for a in faq["source_anomalies"]], [(36, 26)])
        self.assertIn('source anomaly: FAQ: ENISA numbers its question 36 "26."', out)

    def test_it_is_reported_again_on_an_unchanged_run(self):
        self.run_quiet(self.faq_f)
        code, out = self.run_quiet(self.faq_f)
        self.assertEqual(code, 0)
        self.assertIn("source anomaly", out)

    def test_enisa_correcting_the_number_removes_it_and_keeps_q36(self):
        self.run_quiet(self.faq_f)
        q36 = self.load("faq.json")["questions"][35]
        with open(self.faq_f, encoding="utf-8") as fh:
            fixed = fh.read().replace("<dt>26. [NEW] What can do", "<dt>36. [NEW] What can do", 1)
        alt = os.path.join(self.root, "faq_fixed.html")
        with open(alt, "w", encoding="utf-8") as fh:
            fh.write(fixed)
        code, out = self.run_quiet(alt)
        self.assertEqual(code, 1)
        self.assertIn("source anomaly corrected by ENISA", out)
        faq = self.load("faq.json")
        self.assertNotIn("source_anomalies", faq)
        self.assertEqual(faq["questions"][35], q36)
        self.assertEqual(self.run_quiet(alt)[0], 0)

    def test_a_clean_page_writes_no_anomaly_key(self):
        run(self.root, os.path.join(H.FIXTURES, "faq_dl.html"), self.gl_f)
        self.assertNotIn("source_anomalies", self.load("faq.json"))

    def test_the_glossary_now_carries_7a(self):
        self.run_quiet(self.faq_f)
        self.assertIn("7a", [f["nr"] for f in self.load("glossary.json")["fields"]])


if __name__ == "__main__":
    unittest.main()
