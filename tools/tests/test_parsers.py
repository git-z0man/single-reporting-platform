import unittest

from tools.tests import helpers as H

g = H.g


class RealPages(unittest.TestCase):
    """The captures are real ENISA pages. If ENISA restructures them, this is what fails."""

    def test_faq(self):
        faq = g.parse_faq(H.fx("faq_dl.html"))
        self.assertEqual(len(faq["questions"]), 33)
        self.assertEqual(faq["stamp"], "Updated: 03 October 2026")
        self.assertEqual([q["n"] for q in faq["questions"]], list(range(1, 34)))
        q5 = faq["questions"][4]
        self.assertEqual(q5["title"], "What must be reported via the platform?")  # the [UPDATED] tag is not part of the title
        self.assertIn("placing on the EU market", q5["html"])

    def test_glossary(self):
        gl = g.parse_glossary(H.fx("glossary_table.html"))
        self.assertEqual((gl["version"], gl["last_update"], len(gl["fields"])), ("1.4", "01 October 2026", 42))
        by = {f["nr"]: f for f in gl["fields"]}
        self.assertEqual((by["v26a"]["ew"], by["v26a"]["h72"], by["v26a"]["fr"]), ("Optional", "Required", "Carried over"))
        self.assertEqual(by["40"]["name"], "AR Note")
        self.assertEqual(by["v28"]["how"].count("\n"), 3)  # the three legal conditions are kept as lines
        self.assertEqual(by["v28"]["example"], "")

    def test_glossary_1_6_stage_wordings(self):
        gl = g.parse_glossary(H.fx("glossary_table_1_6.html"))
        self.assertEqual((gl["version"], gl["last_update"], len(gl["fields"])), ("1.6", "21 October 2026", 42))
        st = {f["nr"]: (f["ew"], f["h72"], f["fr"]) for f in gl["fields"]}
        self.assertEqual(st["v22"], ("Optional after v17", "Optional after v17", "Required"))  # with and without the space
        self.assertEqual(st["v26"], ("Required", "n/a", "n/a"))  # "Mandatory"
        self.assertEqual(st["v26a"], ("Optional", "Carried over", "n/a"))  # "By default copied from previous step"
        self.assertEqual(st["v29"][1], "Optional if PEC")
        self.assertEqual(st["v30"], ("n/a", "Optional if PEC", "n/a"))
        labels = {s for t in st.values() for s in t}
        self.assertLessEqual(labels, set(H.cg.CHIP_CLASS))  # every label can be rendered

    def test_answer_normalisation_changes_presentation_not_wording(self):
        html = g.parse_faq(H.fx("faq_dl.html"))["questions"][30]["html"]  # Q31 has links
        self.assertIn('target="_blank" rel="noopener"', html)
        self.assertNotIn("&nbsp;</p>", html)


class Normaliser(unittest.TestCase):
    def test_trailing_encoded_space_in_a_link_goes_but_one_inside_a_path_stays(self):
        s = g.normalize_answer_html('<p><a href="https://x.eu/a/C(2025)8407%20">t</a> <a href="https://x.eu/CRA%20SRP.pdf">p</a></p>')
        self.assertIn('C(2025)8407"', s)
        self.assertIn("CRA%20SRP.pdf", s)

    def test_bold_whitespace_quirks(self):
        s = g.normalize_answer_html("<p>is <strong>required </strong>(stemming) and<strong> </strong>of</p>")
        self.assertIn("<strong>required</strong> (stemming)", s)
        self.assertNotIn("<strong> </strong>", s)

    def test_words_ignore_markup_quotes_and_case(self):
        self.assertEqual(g.words("<p>It’s &ldquo;Fine&rdquo;&nbsp;now</p>"), g.words("it's \"fine\" now"))


class Failure(unittest.TestCase):
    def test_a_page_it_does_not_understand_is_an_error_not_a_guess(self):
        with self.assertRaises(g.ParseError):
            g.parse_faq("<html><body>maintenance</body></html>")
        with self.assertRaises(g.ParseError):
            g.parse_glossary("<table><tr><td>x</td></tr></table>")

    def test_unknown_stage_text_stops_the_parse(self):
        raw = H.fx("glossary_table.html").replace("Optional", "Sometimes", 3)
        with self.assertRaises(g.ParseError):
            g.parse_glossary(raw)

    def test_non_contiguous_question_numbers_stop_the_parse(self):
        with self.assertRaises(g.ParseError):
            g.parse_faq(H.fx("faq_dl.html").replace("<dt>7. ", "<dt>70. ", 1))


CSIRT_BASELINE = """---
x: y
---

## List of CSIRTs Designated as Coordinators (new page, `csirt_list_url`)

Some prose about the page.

- Austria: https://www.cert.at/de/ueber-uns/kontakt/ and https://www.cert.at/en/about-us/contact/
- Malta: https://www.mita.gov.mt *(protocol only, changed 2026-09-10 from `http://www.mita.gov.mt`)*
- Spain: for incidents \u2014 https://www.incibe.es/incibe-cert/incidentes/respuesta-incidentes ; for vulnerability coordination \u2014 https://www.incibe.es/incibe-cert/alerta-temprana/vulnerabilidades/asignacion-publicacion-cve

## Next section

- Not a country: https://example.eu/ignored
"""


class CsirtList(unittest.TestCase):
    """The list ENISA edits without moving its stamp. See tools/check_csirt_list.py."""

    def test_real_page_parses_into_27_countries(self):
        live = H.ccl.from_html(H.fx("csirt_list.html"))
        self.assertEqual(len(live), 27)
        self.assertEqual(live["Sweden"], ["https://cert.se/rapportera"])

    def test_annotation_in_the_baseline_is_not_a_current_link(self):
        base = H.ccl.from_baseline(CSIRT_BASELINE)
        self.assertEqual(base["Malta"], ["https://www.mita.gov.mt"])      # not the quoted http:// one
        self.assertEqual(len(base), 3)                                   # the next section is not read

    def test_a_removed_link_is_reported_against_its_country(self):
        base = H.ccl.from_baseline(CSIRT_BASELINE)
        live = H.deep(base)
        live["Spain"] = [u for u in live["Spain"] if "incidentes" not in u]
        d = H.ccl.diff(live, base)
        self.assertEqual(len(d), 1)
        self.assertIn("~ Spain", d[0])
        self.assertIn("removed https://www.incibe.es/incibe-cert/incidentes/respuesta-incidentes", d[0])
        self.assertEqual(H.ccl.diff(base, base), [])

    def test_markup_that_no_longer_parses_is_an_error_not_a_silent_pass(self):
        import tempfile, os
        d = tempfile.mkdtemp()
        page, base = os.path.join(d, "p.html"), os.path.join(d, "b.md")
        open(page, "w").write("<html><body><p>Moved.</p></body></html>")
        open(base, "w").write(CSIRT_BASELINE)
        self.assertEqual(H.ccl.main([page, base]), 2)
        open(page, "w").write(H.fx("csirt_list.html"))
        open(base, "w").write("---\nno section here\n---\n")
        self.assertEqual(H.ccl.main([page, base]), 2)


if __name__ == "__main__":
    unittest.main()
