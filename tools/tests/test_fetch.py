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


if __name__ == "__main__":
    unittest.main()
