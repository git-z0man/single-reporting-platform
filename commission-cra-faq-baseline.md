---
source: European Commission (DG CNECT) — Cyber Resilience Act implementation
factpage_url: https://digital-strategy.ec.europa.eu/en/factpages/cyber-resilience-act-implementation
faq_page_url: https://digital-strategy.ec.europa.eu/en/library/cyber-resilience-act-implementation-frequently-asked-questions
faq_pdf_url: https://ec.europa.eu/newsroom/dae/redirection/document/122331
faq_markdown_url: https://ec.europa.eu/newsroom/dae/redirection/document/123307
current_version: "1.4"
current_version_date: 2026-09-04
archive: commission-faq/versions/ (PDF + Markdown per version, manifest.json)
canonical_text: commission-faq/text/ (diffable plain text per version)
retrieved: 2026-09-05
factpage_retrieved: 2026-09-05
purpose: Baseline snapshot for change detection on the Commission's CRA FAQ and its implementation factpage. Future runs compare the live document against the archived version and record the delta here.
note: Unlike the ENISA baseline, the FAQ content is not inlined here — it is a 66-page document. The archive under `commission-faq/versions/` holds each released version verbatim; this page carries the version history, the substantive deltas, and the comparison links.
last_check: 2026-09-05
last_change: 2026-09-04
---

# Commission CRA FAQ — Version Baseline

The Commission publishes *FAQs on the Cyber Resilience Act* as a versioned
"living document". It carries its own version table on page 1, which is the
authoritative signal for a new release — the landing page's "Last update"
date also moves for edits that do not change the document.

Both a PDF and a Markdown rendering are published. The Markdown is the better
diff source and is archived alongside the PDF whenever it is available.

## Current state

| | |
|---|---|
| Current version | **1.4** (04/09/2026) |
| Stated change | Addition of FAQ 5.5 |
| Pages | 66 |
| PDF | [document/122331](https://ec.europa.eu/newsroom/dae/redirection/document/122331) — `sha256:43cd3da1…06b54a` |
| Markdown | [document/123307](https://ec.europa.eu/newsroom/dae/redirection/document/123307) — `sha256:beb9b79a…9dbc9` |
| Last check | 2026-09-05 |
| Last change | 2026-09-04 |

## Version history

Version and date as stated in the document's own version table. "Stated
change" is the Commission's own one-line description; "actually changed" is
what a diff of the archived versions shows.

| Version | Date | Stated change | Archived | Actually changed |
|---|---|---|---|---|
| 1.0 | 03/12/2025 | New | ✅ PDF | — (baseline) |
| 1.1 | 17/12/2025 | Copyright notice; minor formatting issues | ❌ not held | folded into the 1.0 → 1.2 diff |
| 1.2 | 16/01/2026 | Minor correction of 6.2 | ✅ PDF | CC BY 4.0 reuse notice added; **NANDO number removed from the module B+C step in 6.2** |
| 1.3 | 01/07/2026 | Deletion of subsection 4.6 | ✅ PDF | subsection 4.6 incl. 4.6.1 deleted in full |
| 1.4 | 04/09/2026 | Addition of FAQ 5.5 | ✅ PDF + Markdown | FAQ 5.5 added; Article 26 guidance sentence updated |

v1.1 was never captured. Its edits are not lost — they appear inside the
1.0 → 1.2 diff — but they cannot be attributed to 1.1 versus 1.2 separately.

## Change log

### v1.3 → v1.4 (released 04/09/2026, detected 2026-09-05)

**New: FAQ 5.5 — "Are open-source software stewards subject to reporting
obligations under the CRA?"** (section 5, Reporting obligations, p. 55).
Directly relevant to this repository's subject matter. Full text:

> Article 24(3) of the CRA establishes that reporting obligations laid down
> in Article 14, paragraphs (1), (3) and (8), apply to open-source software
> stewards under certain circumstances. In accordance with Article 71(2) of
> the CRA, Article 24(3) shall apply from 11 December 2027.

Note the date: steward reporting obligations start **11 December 2027**, not
11 September 2026. The 2026 date applies to manufacturers under Article 14.

**Changed: the Article 26 guidance sentence in the preamble.**

- was: "The Commission is also working on guidance pursuant to Article 26 of the CRA, to be adopted in the coming months."
- now: "The Commission has also adopted guidance pursuant to Article 26 of the CRA."

The sentence now hyperlinks to the guidance published on 27 July 2026. This
reflects adoption having happened, not a change of substance.

**Consequential only:** the version table gained its 1.4 row, the table of
contents gained the 5.5 entry, and page numbering from p. 55 onwards shifted
by one. No other question was added, deleted, reordered, or reworded.

### v1.2 → v1.3 (released 01/07/2026, recorded retroactively 2026-09-05)

Subsection **4.6 "Other manufacturer's obligations"** and its only entry
**4.6.1 "Can a third-country manufacturer directly place products on the
Union market?"** were deleted in full. The deleted entry set out the
Article 4(1)–(2) of Regulation (EU) 2019/1020 requirement for a
Union-established economic operator (manufacturer, importer, authorised
representative, or fulfilment service provider). Nothing replaced it in the
FAQ; page numbering shifted accordingly. No other substantive edit.

### v1.0 → v1.2 (released 16/01/2026, recorded retroactively 2026-09-05)

Covers both the 1.1 and 1.2 releases, since v1.1 is not archived.

- **Copyright/reuse notice added** to page 1: Commission Decision 2011/833/EU
  and the CC BY 4.0 licence terms. This is the "copyright notice" item.
- **Section 6.2 (module B+C) corrected** — this is the "minor correction of
  6.2", and it is more than cosmetic: the step
  "it affixes the CE marking (…) **together with the NANDO number of the
  notified body**, draw up and sign a declaration of conformity"
  lost the NANDO-number requirement, leaving
  "it affixes the CE marking (…), draw up and sign a declaration of
  conformity". Anyone who took the earlier wording as guidance on CE marking
  content should re-read 6.2 in v1.2 or later.
- Page numbering shifted by one across the table of contents.

## Factpage baseline

`https://digital-strategy.ec.europa.eu/en/factpages/cyber-resilience-act-implementation`
— last update stated **27 July 2026**, retrieved 2026-09-05. This page is
watched for changes to the implementation timeline; the milestones as of this
baseline:

| Date | Milestone |
|---|---|
| 28 Nov 2025 | Implementing act on technical descriptions ([32025R2392](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32025R2392)) |
| 11 Dec 2025 | Delegated act on CSIRT notifications ([32026R0881](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32026R0881)) |
| 11 Jun 2026 | Conformity assessment bodies notification entry |
| 27 Jul 2026 | First Commission guidance (Article 26) |
| Q3 2026 | First standardisation deliverables |
| 11 Sep 2026 | Entry into application of reporting obligations |
| Q4 2026 | EUCC presumption of conformity delegated act |
| 11 Dec 2026 | Sufficient CABs designated |
| 30 Oct 2027 | Additional standardisation deliverables |
| 11 Dec 2027 | Full CRA application |

## Visual comparisons (Draftable)

Textual diffs of the archived versions are produced locally by
`commission-faq/tools/diff_versions.py` and are what the change log above is
built from. Draftable adds a *visual*, document-aware comparison — the
rendered side-by-side view that a naive text diff cannot give.

**Not yet available.** `api.draftable.com` is denied by this environment's
network egress policy (HTTP 403 on CONNECT), so no comparison has been
created. See `commission-faq/README.md` for what needs to be unblocked. Once
it is, this table is filled in by the monitoring routine:

| Comparison | Identifier | Viewer |
|---|---|---|
| v1.0 → v1.2 | `cra-faq-v1.0-v1.2` | pending |
| v1.2 → v1.3 | `cra-faq-v1.2-v1.3` | pending |
| v1.3 → v1.4 | `cra-faq-v1.3-v1.4` | pending |

## Provenance

The FAQ is © European Union, 2025, reusable under CC BY 4.0 per Commission
Decision 2011/833/EU. Archived copies are unmodified. The v1.0, v1.2 and v1.3
PDFs were supplied from a local archive; v1.4 was downloaded from the
Commission's newsroom endpoint on 2026-09-05 and verified byte-identical
(`sha256:43cd3da1…06b54a`) to the locally held copy.

The document is prepared by Commission services and is expressly *not* an
official position of the European Commission. Nothing here is legal advice.
