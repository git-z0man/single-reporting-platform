"""Tests of THIS repository's current state, not of the tools.

They hold whenever index.html is in sync with guide-sync/. They fail, correctly,
while a judgment item is waiting for a person - so a Routine does not use them
as a gate. Run them by hand: python3 -m unittest tools.tests.repo_state
"""
import os
import unittest

from tools.tests import helpers as H

ROOT = os.path.dirname(H.TOOLS)


class RepoState(unittest.TestCase):
    def test_the_guide_matches_what_enisa_said_when_guide_sync_last_looked(self):
        findings = [f for f in H.cg.check(ROOT) if f[0] == "hard"]
        self.assertEqual(findings, [])

    def test_sync_is_a_fixed_point_on_the_real_guide(self):
        with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as fh:
            h = fh.read()
        faq = H.g.load_json(os.path.join(ROOT, "guide-sync", "faq.json"))
        gl = H.g.load_json(os.path.join(ROOT, "guide-sync", "glossary.json"))
        new, rep = H.sg.sync(h, faq, gl, H.sg.moved_urls(ROOT), False)
        self.assertEqual((new == h, rep["mechanical"], rep["judgment"]), (True, [], []))


if __name__ == "__main__":
    unittest.main()
