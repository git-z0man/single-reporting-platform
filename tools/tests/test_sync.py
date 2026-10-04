import re
import unittest

from tools.tests import helpers as H


def run(faq0, gl0, faq1, gl1, include=False, urls=None):
    guide = H.guide_for(faq0, gl0)
    return guide, *H.sg.sync(guide, faq1, gl1, urls or {}, include)


class TypoClass(unittest.TestCase):
    def test_accepts_one_letter_typo(self):
        self.assertTrue(H.sg.is_typo_change("a severe incident".split(), "a sever incident".split()))

    def test_rejects_short_word_swaps_that_change_meaning(self):
        self.assertFalse(H.sg.is_typo_change("report in time".split(), "report on time".split()))

    def test_rejects_a_different_word(self):
        self.assertFalse(H.sg.is_typo_change("involved in the deployment of".split(), "involved in the development of".split()))

    def test_rejects_insertions_and_deletions(self):
        self.assertFalse(H.sg.is_typo_change("report now".split(), "report it now".split()))


class Faq(unittest.TestCase):
    def setUp(self):
        self.faq, self.gl = H.extracts()

    def test_fixed_point(self):
        g, new, rep = run(self.faq, self.gl, self.faq, self.gl)
        self.assertEqual(g, new)
        self.assertEqual((rep["mechanical"], rep["judgment"]), ([], []))

    def test_new_question_is_appended_in_order_and_is_mechanical(self):
        f1 = H.deep(self.faq)
        f1["questions"].append(H.question(4, "Can I withdraw?"))
        g, new, rep = run(self.faq, self.gl, f1, self.gl)
        self.assertEqual([m["class"] for m in rep["mechanical"] if m["class"] != "marker"], ["faq-new"])
        nums = [int(x) for x in re.findall(r'class="faq-num">Q(\d+)<', new)]
        self.assertEqual(nums, [1, 2, 3, 4])
        self.assertIn('data-sync="faq-count">4<', new)

    def test_question_inserted_between_existing_ones(self):
        f0 = H.deep(self.faq)
        f0["questions"] = [q for q in f0["questions"] if q["n"] != 2]
        guide = H.guide_for(f0, self.gl)
        new, rep = H.sg.sync(guide, self.faq, self.gl, {}, False)
        nums = [int(x) for x in re.findall(r'class="faq-num">Q(\d+)<', new)]
        self.assertEqual(nums, [1, 2, 3])

    def test_typo_is_mechanical(self):
        f1 = H.deep(self.faq)
        f1["questions"][1]["html"] = f1["questions"][1]["html"].replace("Severe", "Sever")
        g, new, rep = run(self.faq, self.gl, f1, self.gl)
        self.assertEqual([m["class"] for m in rep["mechanical"]], ["faq-typo"])
        self.assertIn("Sever incidents", new)
        self.assertEqual(rep["judgment"], [])

    def test_rewrite_is_judgment_and_not_applied(self):
        f1 = H.deep(self.faq)
        f1["questions"][0]["html"] = "<p>Something else entirely.</p>"
        g, new, rep = run(self.faq, self.gl, f1, self.gl)
        self.assertEqual(g, new)
        self.assertEqual([j["class"] for j in rep["judgment"]], ["faq-text"])
        self.assertFalse(rep["eligible_for_auto_merge"])

    def test_include_judgment_applies_it_but_is_never_eligible(self):
        f1 = H.deep(self.faq)
        f1["questions"][0]["html"] = "<p>Something else entirely.</p>"
        g, new, rep = run(self.faq, self.gl, f1, self.gl, include=True)
        self.assertIn("Something else entirely", new)
        self.assertTrue(rep["applied_judgment"])
        self.assertFalse(rep["eligible_for_auto_merge"])

    def test_changed_link_target_is_judgment(self):
        f1 = H.deep(self.faq)
        f1["questions"][1]["html"] = f1["questions"][1]["html"].replace("example.eu/a", "example.eu/b")
        g, new, rep = run(self.faq, self.gl, f1, self.gl)
        self.assertEqual(g, new)
        self.assertIn("faq-links", [j["class"] for j in rep["judgment"]])

    def test_removed_question_is_reported_and_never_deleted(self):
        f1 = H.deep(self.faq)
        f1["questions"] = [q for q in f1["questions"] if q["n"] != 3]
        g, new, rep = run(self.faq, self.gl, f1, self.gl, include=True)
        self.assertIn("Q3", [j["target"] for j in rep["judgment"] if j["class"] == "faq-removed"])
        self.assertIn('faq-num">Q3<', new)

    def test_guide_note_survives_a_rewrite(self):
        guide = H.guide_for(self.faq, self.gl).replace(
            "Answer to question 1.</p>", 'Answer to question 1.</p>\n              <p class="guide-note"><em>Ours.</em></p>', 1)
        f1 = H.deep(self.faq)
        f1["questions"][0]["html"] = "<p>Rewritten.</p>"
        new, rep = H.sg.sync(guide, f1, self.gl, {}, True)
        self.assertIn('<p class="guide-note"><em>Ours.</em></p>', new)
        self.assertIn("Rewritten.", new)


class Glossary(unittest.TestCase):
    def setUp(self):
        self.faq, self.gl = H.extracts()

    def ids(self, text):
        return re.findall(r'<details class="faq field" id="f-([^"]+)"', text)

    def test_new_optional_field_is_mechanical_and_ordered(self):
        g1 = H.deep(self.gl)
        g1["fields"] += [H.field("40", "AR Note"), H.field("v26a", "Occurred", "AEV", h72="Required")]
        g1["fields"][-1]["h72"] = "Optional"  # optional-only, so mechanical
        g, new, rep = run(self.faq, self.gl, self.faq, g1)
        self.assertEqual(sorted(m["class"] for m in rep["mechanical"] if m["class"].startswith("gl-")), ["gl-new", "gl-new"])
        ids = self.ids(new)
        self.assertEqual(ids.index("v26a"), ids.index("v26") + 1)
        self.assertEqual(ids.index("40"), ids.index("2") + 1)

    def test_new_required_field_is_judgment_and_not_inserted(self):
        g1 = H.deep(self.gl)
        g1["fields"].append(H.field("v26a", "Occurred", "AEV", ew="Optional", h72="Required", fr="Carried over"))
        g, new, rep = run(self.faq, self.gl, self.faq, g1)
        unmark = lambda s: re.sub(r'data-sync="glossary-count">\d+', 'data-sync="glossary-count">N', s)
        self.assertEqual(unmark(g), unmark(new))  # nothing but the count marker moved
        self.assertNotIn("v26a", self.ids(new))
        self.assertEqual([j["class"] for j in rep["judgment"]], ["gl-new-required"])
        self.assertFalse(rep["eligible_for_auto_merge"])

    def test_stage_change_is_judgment(self):
        g1 = H.deep(self.gl)
        g1["fields"][0]["ew"] = "Optional"
        g, new, rep = run(self.faq, self.gl, self.faq, g1)
        self.assertEqual([j["class"] for j in rep["judgment"]], ["gl-stages"])
        self.assertEqual(g, new)

    def test_text_typo_updates_in_place_and_keeps_limit_suffix_and_notes(self):
        self.gl["fields"][1]["format"] = "Short paragraph"
        guide = H.guide_for(self.faq, self.gl)
        # the guide's own supplements: an observed character limit on field 1, a note box on field 1
        guide = guide.replace('<span data-k="fmt">Select one</span>', '<span data-k="fmt">Select one &middot; max 255 characters</span>', 1)
        guide = guide.replace('<dl class="fdef">', '<div class="faq-amend"><p>OUR NOTE</p></div><dl class="fdef">', 1)
        g1 = H.deep(self.gl)
        g1["fields"][0]["means"] = "Meens it."          # typo-class, field 1
        g1["fields"][0]["format"] = "Select on"          # too short to count as a typo -> judgment
        g1["fields"][1]["format"] = "Short paragrph"    # typo-class, field 2
        new, rep = H.sg.sync(guide, self.faq, g1, {}, False)
        self.assertEqual(sorted(m["class"] for m in rep["mechanical"] if m["class"].startswith("gl-")), ["gl-typo", "gl-typo"])
        self.assertEqual([j["class"] for j in rep["judgment"]], ["gl-text"])
        self.assertIn("Meens it.", new)
        self.assertIn("Short paragrph", new)
        self.assertIn("Select one &middot; max 255 characters", new)   # judgment edit not applied; suffix intact
        self.assertIn("OUR NOTE", new)
        self.assertIn("OWN-NOTE field-1:", new)

    def test_removed_field_is_reported_not_deleted(self):
        g1 = H.deep(self.gl)
        g1["fields"] = [f for f in g1["fields"] if f["nr"] != "v19"]
        g, new, rep = run(self.faq, self.gl, self.faq, g1, include=True)
        self.assertIn("v19", [j["target"] for j in rep["judgment"] if j["class"] == "gl-removed"])
        self.assertIn("v19", self.ids(new))

    def test_prereq_card_is_never_touched_or_reported(self):
        g, new, rep = run(self.faq, self.gl, self.faq, self.gl, include=True)
        self.assertIn("prereq", self.ids(new))
        self.assertNotIn("prereq", [j["target"] for j in rep["judgment"]])


class MarkersUrlsAndLimits(unittest.TestCase):
    def setUp(self):
        self.faq, self.gl = H.extracts()

    def test_markers_follow_the_extracts_and_notes_are_grouped(self):
        g1 = H.deep(self.gl)
        g1["version"], g1["fetched"] = "1.5", "2026-10-09"
        g, new, rep = run(self.faq, self.gl, self.faq, g1)
        self.assertIn('data-sync="glossary-version">1.5<', new)
        self.assertIn("9&nbsp;October&nbsp;2026", new)
        keys = [m["target"] for m in rep["mechanical"]]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertTrue(rep["eligible_for_auto_merge"])

    def test_moved_page_links_are_repointed_mechanically(self):
        guide = H.guide_for(self.faq, self.gl).replace("</footer>", '<a href="https://example.eu/old/srp">x</a> <a href="https://example.eu/old/srp/faq/">y</a> <a href="https://example.eu/old/srp/sub">z</a></footer>')
        urls = {"https://example.eu/old/srp": "https://example.eu/new/srp", "https://example.eu/old/srp/faq": "https://example.eu/new/srp/faq"}
        new, rep = H.sg.sync(guide, self.faq, self.gl, urls, False)
        self.assertIn('href="https://example.eu/new/srp"', new)
        self.assertIn('href="https://example.eu/new/srp/faq"', new)
        self.assertIn('href="https://example.eu/old/srp/sub"', new)  # a subpage under the old prefix is not a moved page

    def test_a_big_change_is_never_eligible(self):
        g1 = H.deep(self.gl)
        g1["fields"] += [H.field(str(100 + i), f"Extra {i}") for i in range(10)]
        g, new, rep = run(self.faq, self.gl, self.faq, g1)
        self.assertGreater(rep["changed_lines"], H.sg.MAX_LINES)
        self.assertFalse(rep["eligible_for_auto_merge"])

    def test_nothing_to_do_is_not_eligible(self):
        g, new, rep = run(self.faq, self.gl, self.faq, self.gl)
        self.assertFalse(rep["eligible_for_auto_merge"])


if __name__ == "__main__":
    unittest.main()
