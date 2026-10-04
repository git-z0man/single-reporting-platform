import os
import subprocess
import sys
import unittest

from tools.tests import helpers as H

TOOLS = H.TOOLS


def py(script, *args, cwd=None):
    r = subprocess.run([sys.executable, os.path.join(TOOLS, script), *args], capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout + r.stderr


class VerifyMechanical(unittest.TestCase):
    def setUp(self):
        self.faq, self.gl = H.extracts()
        self.root = H.make_root(self.faq, self.gl)
        H.git_init(self.root)

    def advance(self, faq=None, gl=None, apply=True):
        """Pretend ENISA changed, the extracts were refreshed, and sync ran."""
        faq, gl = faq or self.faq, gl or self.gl
        H.write_json(self.root, "faq.json", faq)
        H.write_json(self.root, "glossary.json", gl)
        if apply:
            new, _ = H.sg.sync(H.read(self.root), faq, gl, {}, False)
            H.write(self.root, new)

    def verify(self):
        return py("verify_mechanical.py", "origin/main", "--root", self.root)

    def test_unchanged_guide(self):
        self.assertEqual(self.verify()[0], 0)

    def test_a_pure_sync_result_is_eligible(self):
        f1 = H.deep(self.faq)
        f1["questions"].append(H.question(4, "Can I withdraw?"))
        self.advance(faq=f1)
        code, out = self.verify()
        self.assertEqual(code, 0, out)
        self.assertIn("matches sync_guide exactly", out)

    def test_one_hand_edited_word_disqualifies_it(self):
        f1 = H.deep(self.faq)
        f1["questions"].append(H.question(4, "Can I withdraw?"))
        self.advance(faq=f1)
        H.write(self.root, H.read(self.root).replace("Answer to question 4.", "Answer to question 4, edited."))
        code, out = self.verify()
        self.assertEqual(code, 1)
        self.assertIn("not what sync_guide produces", out)
        self.assertIn("edited", out)

    def test_a_change_with_pending_judgment_is_not_eligible(self):
        f1 = H.deep(self.faq)
        f1["questions"][0]["html"] = "<p>Rewritten completely.</p>"
        f1["questions"].append(H.question(4, "Can I withdraw?"))
        self.advance(faq=f1)
        code, out = self.verify()
        self.assertEqual(code, 1)
        self.assertIn("judgment items are pending", out)

    def test_judgment_edits_made_by_hand_or_with_the_flag_are_not_eligible(self):
        f1 = H.deep(self.faq)
        f1["questions"][0]["html"] = "<p>Rewritten completely.</p>"
        self.advance(faq=f1, apply=False)
        new, _ = H.sg.sync(H.read(self.root), self.faq, self.gl, {}, False)  # base-equivalent
        applied, _ = H.sg.sync(H.read(self.root), f1, self.gl, {}, True)
        H.write(self.root, applied)
        self.assertEqual(self.verify()[0], 1)

    def test_a_missing_base_ref_is_an_error(self):
        self.assertEqual(py("verify_mechanical.py", "no-such-ref", "--root", self.root)[0], 2)


class ScopeGuard(unittest.TestCase):
    def setUp(self):
        self.root = H.make_root(*H.extracts())
        H.git_init(self.root)

    def guard(self, *scope):
        return py("scope_guard.py", *scope, "--root", self.root)

    def test_nothing_changed(self):
        code, out = self.guard("index.html")
        self.assertEqual((code, "nothing changed" in out), (0, True))

    def test_changes_inside_the_scope(self):
        H.write(self.root, "x" + H.read(self.root))
        H.write_json(self.root, "faq.json", H.extracts()[0] | {"fetched": "2026-10-09"})
        self.assertEqual(self.guard("index.html", "guide-sync/")[0], 0)

    def test_a_file_outside_the_scope_fails_and_is_named(self):
        H.write(self.root, "changed", "CLAUDE.md")
        code, out = self.guard("index.html", "guide-sync/")
        self.assertEqual(code, 1)
        self.assertIn("CLAUDE.md", out)

    def test_untracked_files_count(self):
        os.makedirs(os.path.join(self.root, "routines"))
        H.write(self.root, "x", "routines/new.md")
        self.assertEqual(self.guard("index.html", "guide-sync/")[0], 1)

    def test_a_prefix_is_not_a_substring_match(self):
        H.write(self.root, "x", "guide-sync-evil.json")
        self.assertEqual(self.guard("guide-sync/")[0], 1)


if __name__ == "__main__":
    unittest.main()
