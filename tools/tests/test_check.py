import re
import unittest

from tools.tests import helpers as H


def codes(root):
    return sorted({c for s, c, m in H.cg.check(root) if s == "hard"})


class Check(unittest.TestCase):
    def setUp(self):
        self.faq, self.gl = H.extracts()
        self.root = H.make_root(self.faq, self.gl)
        self.guide = H.read(self.root)

    def with_guide(self, text):
        H.write(self.root, text)
        return codes(self.root)

    def test_a_consistent_guide_has_no_findings(self):
        self.assertEqual(codes(self.root), [])

    def test_changed_answer_text(self):
        self.assertEqual(self.with_guide(self.guide.replace("Answer to question 1.", "Another answer.")), ["FAQ-BODY"])

    def test_changed_link_target(self):
        self.assertEqual(self.with_guide(self.guide.replace("example.eu/a", "example.eu/b")), ["FAQ-LINKS"])

    def test_stale_marker_and_unmarked_count(self):
        t = self.guide.replace('data-sync="faq-count">3<', 'data-sync="faq-count">4<')
        self.assertEqual(self.with_guide(t), ["MARKER-STALE"])
        t = self.guide.replace("This is the whole form:", "There are 39 fields here. This is the whole form:")
        self.assertEqual(self.with_guide(t), ["UNMARKED-COUNT"])

    def test_missing_marker(self):
        t = re.sub(r'<span data-sync="footer-asof">.*?</span>', "", self.guide)
        self.assertEqual(self.with_guide(t), ["MARKER-MISSING"])

    def test_dead_and_wrong_field_links(self):
        row = '<table><tr><td class="c-field">Title<a class="fieldref" href="#f-%s" title="Open field %s in the reference">%s</a></td></tr></table>'
        self.assertEqual(self.with_guide(self.guide + row % ("99", "99", "99")), ["REF-DEAD"])
        self.assertEqual(self.with_guide(self.guide + row % ("v19", "v19", "v19")), ["REF-WRONG"])
        self.assertEqual(self.with_guide(self.guide + row % ("2", "2", "9")), ["REF-LABEL"])
        self.assertEqual(self.with_guide(self.guide + row % ("2", "2", "2")), [])

    def test_truncated_href_and_orphan_text(self):
        t = self.guide.replace("</footer>", '<a href="https://eur-lex.eu/?uri=C(2025">Regulation</a>8407)</footer>')
        self.assertEqual(self.with_guide(t), ["HREF-ORPHAN", "HREF-PAREN"])

    def test_unbalanced_tags(self):
        self.assertIn("TAGS", self.with_guide(self.guide.replace("</details>", "", 1)))  # two cards fuse, so GL-MISSING follows

    def test_card_stage_and_text_drift(self):
        t = self.guide.replace('<span class="chip mandatory">Required</span></span><span class="fchip"><b>72', '<span class="chip optional">Optional</span></span><span class="fchip"><b>72', 1)
        self.assertEqual(self.with_guide(t), ["GL-STAGES"])
        self.assertEqual(self.with_guide(self.guide.replace('data-k="means">Means it.', 'data-k="means">Else.', 1)), ["GL-TEXT"])

    def test_the_guides_own_character_limit_is_not_drift(self):
        t = self.guide.replace('<span data-k="fmt">Free text</span>', '<span data-k="fmt">Free text &middot; max 4&nbsp;000 characters</span>', 1)
        self.assertEqual(self.with_guide(t), [])

    def test_missing_and_extra_cards_and_questions(self):
        t = re.sub(r'          <details class="faq field" id="f-i31">.*?</details>\n', "", self.guide, flags=re.S)
        self.assertEqual(self.with_guide(t), ["GL-MISSING"])
        t = self.guide + sg_card("zz")
        self.assertEqual(self.with_guide(t), ["GL-EXTRA"])
        t = re.sub(r'          <details class="faq">\s*<summary><span class="faq-qwrap"><span class="faq-num">Q3<.*?</details>\n', "", self.guide, flags=re.S)
        self.assertEqual(self.with_guide(t), ["FAQ-MISSING"])

    def test_old_address_of_a_moved_page(self):
        t = self.guide.replace("</footer>", '<a href="https://example.eu/old/srp">x</a></footer>')
        self.assertEqual(self.with_guide(t), ["URL-STALE"])

    def test_the_guide_notes_are_not_compared(self):
        t = self.guide.replace("Answer to question 1.</p>", 'Answer to question 1.</p><p class="guide-note"><em>ours</em></p>', 1)
        self.assertEqual(self.with_guide(t), [])


def sg_card(nr):
    return H.sg.render_card(H.field(nr, "Ghost"))


if __name__ == "__main__":
    unittest.main()
