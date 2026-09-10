---
source: ENISA — CRA SRP Glossary
url: https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2
old_url: https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary (returns HTTP 403 since at least 2026-09-07; superseded, see status)
page_version: "1.3 (page footer: last update 10/09/2026)"
retrieved: 2026-09-10 (fetched 22:13 UTC)
purpose: Full-detail baseline of the CRA SRP Glossary page — the authoritative field-by-field
  reference for the SRP reporting template (meaning, how to complete, example, expected format,
  and per-stage status for every field). The compact field-name/status table cross-referenced
  from `enisa-srp-faq-baseline.md` (Q16 and the "CRA SRP Glossary" section there) is a trimmed
  summary of this file; this file is the one to diff against for wording-level changes to any
  field's description, example, or format. The live page has already moved once (see
  `old_url` and status), so this file is also the stable reference when the URL shifts.
status: >-
  Resolved. The page was MOVED, not withdrawn: it now lives at `.../cra-srp-glossary2`
  and returns HTTP 200. Its content was then edited the same evening while the footer
  kept saying Version 1.1, 05/09/2026 — treat the version stamp as unreliable and diff
  the rows. Note that the FAQ page's eight links to the Glossary still point at the old
  path and are therefore broken (403). The old
  `.../cra-srp-glossary` path still returns HTTP 403 and is recorded as `old_url`.
  The earlier reading on this line — that ENISA might have unpublished the page —
  was wrong; a 403 on one path while every neighbouring page stayed up is equally
  consistent with a move, and that is what happened. Re-verify the URL on
  every future check, not just the status code. On 2026-09-10 (13:11 UTC) the page's
  own version stamp moved for the first time since it correlated with content
  (1.2 → 1.3) and this time the correlation was large: 38 fields → 39, a new AEV
  field inserted as v23 cascading every later field's number up by one, and roughly
  a dozen wording/status fixes across the page. See the change log.
last_check: 2026-09-10
last_change: 2026-09-10
note: >-
  One row per field, one table per group (Common / AEV / SI), matching the live page's own
  column order — Nr. | Field | Applies to | Meaning | How to complete | Example | Format |
  EW 24h | 72h | Final Report — so a change to a single field shows up as a single-row diff.
  Update `retrieved`, `page_version`, `status`, and table rows whenever a change or a
  reachability transition (403 <-> 200, or a genuinely new page version) is confirmed. Cell
  text has line breaks and multi-item lists flattened to `<br>`-separated fragments so each
  field stays one table row.
---

# CRA SRP Glossary — full-detail baseline

## Change log

### 2026-09-10 22:13 UTC (vs. 2026-09-10 19:07 UTC)

Page still returns HTTP 200 at `cra-srp-glossary2`, fetched alongside all nine other tracked SRP pages in the same run (one of which — FAQ Q17 gaining a closing sentence — changed this time; see `enisa-srp-faq-baseline.md`). The Glossary itself was unaffected: all 39 fields re-verified row by row against the raw `<table>` structure, footer still "Version 1.3. Last update: 10 September 2026". `retrieved` updated; `last_check` and `last_change` unchanged (already 2026-09-10).

### 2026-09-10 19:07 UTC (vs. 2026-09-10 17:13 UTC)

Page still returns HTTP 200 at `cra-srp-glossary2`, fetched alongside all nine other tracked SRP pages in the same run (the only real change this run was on the main page's "User Guidance" card dates; see `enisa-srp-faq-baseline.md`). The Glossary itself was unaffected: all 39 fields re-verified row by row against the raw `<table>` structure, footer still "Version 1.3. Last update: 10 September 2026". `retrieved` updated; `last_check` and `last_change` unchanged (already 2026-09-10).

### 2026-09-10 17:13 UTC (vs. 2026-09-10 15:10 UTC)

Page still returns HTTP 200 at `cra-srp-glossary2`, footer unchanged ("Version 1.3. Last update: 10 September 2026"), field count unchanged (39). One field's wording changed without the stamp moving — the same pattern already established for this page.

**Changed**

- **Field 5, Member States where product available (Concerned CSIRT)**: three word-level edits to the How-to-complete text in the same sentence — "show **you** CDaC" → "show **your** CDaC" (grammar fix); "you may select" → "you may **also** select" (word inserted); "has been made available" → "is available" (tense simplified). Meaning, Example, Format and per-stage statuses are all unchanged.

**Unchanged**

All other 38 rows and both footnotes re-verified cell by cell against the raw `<table>` structure, including every previously tracked defect (v27's doubled full stop, v30's missing space in "(CDaC)taking", field 10's double-space typo, v28's empty Example, v29's three-item grounds list, field 11's "it doesn't" fix holding). No field added, removed, or renumbered.

### 2026-09-10 15:10 UTC (vs. 2026-09-10 14:07 UTC)

Page still returns HTTP 200 at `cra-srp-glossary2`, fetched alongside all nine other tracked SRP pages in the same run (one of which — the main page's AR User Manual download card `href`, previously malformed — was fixed this time; see `enisa-srp-faq-baseline.md`). The Glossary itself was unaffected: all 39 fields re-verified row by row against the raw `<table>` structure, footer still "Version 1.3. Last update: 10 September 2026". `retrieved` updated; `last_check` and `last_change` unchanged (already 2026-09-10).

### 2026-09-10 14:07 UTC (vs. 2026-09-10 13:11 UTC)

Page still returns HTTP 200 at `cra-srp-glossary2`, fetched alongside all nine other tracked SRP pages in the same run (two of which — a main-page card blurb first fully quoted, and the Terms and Conditions link losing a trailing space — changed cosmetically this time; see `enisa-srp-faq-baseline.md`). The Glossary itself was unaffected: all 39 fields re-verified row by row, footer still "Version 1.3. Last update: 10 September 2026". `retrieved` updated; `last_check` and `last_change` unchanged (already 2026-09-10).

### 2026-09-10 13:11 UTC (vs. 2026-09-10 12:17 UTC)

The footer moved for only the second time since tracking began — "version 1.2, last update: 09/09/2026" → "Version 1.3. Last update: 10 September 2026" — and this is by far the largest correlated content change recorded: 38 fields → 39, and roughly a dozen fields changed wording or per-stage status. Numbering cascades from the new field onward: former v23–v29 are now v24–v30, and every SI field shifts up by one (former i30–i38 are now i31–i39).

**New**

- **v23, "Details about the security update/corrective measure available"** (AEV): Meaning "Information on available corrective measures and security updates." How to complete "You may add the available corrective measures and security updates. For example, security patches or software updates (max. 2000 characters)". Example "Security patches". Format "Detailed structured narrative". Status Optional/Optional/Required. Inserted between the old v22 and v23, causing the cascade above.
- **i31 (was i30)** gained a character limit not previously stated: How to complete now ends "...Select Unknown while the cause remains unresolved (max. 255 characters)."

**Fixed**

- **Field 11, End of support indicator** — the long-tracked contradiction is gone. Meaning was "Indicates whether the product... has a user interface or similar technical means... to inform users..."; now reads simply "Indicates whether the product with digital elements has reached the end of the support period." The "is doesn't" typo is also fixed, to "it doesn't" (and "Yes"/"No" are now quoted in the instruction).
- **i37 (was i36)**: Meaning "another relevant become aware" → "another relevant entity becomes aware" — the broken-grammar defect tracked since 2026-09-07 is resolved. How to complete "you become aware" → "you became aware" (tense). Field name gained "(UTC time)".
- **i38 (was i37)**: How to complete "the incident was began or occurred" → "the incident began or occurred" — the other broken-grammar defect tracked since 2026-09-07 is resolved. Field name gained "(UTC time)".
- **v29 (was v28), PEC Delay Reason**: Meaning "select one of the three of the legally specified circumstances" → "select at least one of the three legally specified circumstances" — resolves the "one" vs "at least one" inconsistency against its own How-to-complete text, tracked since 2026-09-07.
- **i33 (was i32)**: Meaning "taken... or are still ongoing" → "taken... and are still ongoing" — now matches the field name's "and" (the field name was fixed on 2026-09-10 05:10 UTC; the Meaning cell had not been touched until now).

**Changed**

- **Field 13**: Format "Select one: Yes, No, Unknown" → "Select one: "Yes" or "No"" — the Unknown option is dropped, from both the format and the how-to-complete text ("Otherwise select No or Unknown" → "Otherwise select "No""; "select Yes **only** when" also loses "only"). A selectable value removed from a live data field.
- **Field 5**: EW24h status "Required if such information available" → "Required".
- **Field 15**: 72h status "Required if such information available" → "Optional".
- **Fields 16 and 17**: 72h status "Required" → "Optional" (both).
- **Field 18**: EW24h status "Optional" → "N/A".
- **i37 (was i36)**: 72h status "copied-or-updated" → "Required".
- **i38 (was i37)**: 72h status "Optional" → "Required".
- **Field 8**: name "(Default/Important/Critical)" → "(Default/Important Product with Digital Elements/Critical Product with Digital Elements)"; Example "Important" → "Important Product with Digital Elements".
- **Field 9**: Meaning "for an important product" → "for an Important Product with Digital Elements", matching field 8's expanded terminology.
- **v24/v25 (was v23/v24)**: Meaning now specifies "the actively exploited vulnerability" (was just "the vulnerability").
- **v30 (was v29)**: How to complete "You may provide additional information(s)." → "You may provide additional information (max. 800 characters)." — a character limit is now stated where none was before.
- **Footnote [2]** (now attached to i37): "Date/time the incident was detected" → "Date and time when the incident was detected (UTC time)".

**Editorial**

Renumbering-only relabelling across v24–v30 and i32–i39; capitalisation-only field-name changes ("Product Class"→"Product class", "Product Category"→"Product category"); i32 (was i31) name gained a comma ("General information about nature" → "General information, about the nature"); several "Date/time" → "Date and time" wording swaps alongside the fixes above; a new double-space typo in field 10's Example ("cryptoprocessing  devices"); minor phrasing softening in fields 10 and 14 ("Use" → "You may use", "Provide" → "You may provide").

**Watch**

- The v27 (was v26) malicious-actor field's doubled full stop, and the v28 (was v27) PEC field's wording, remain exactly as before — not swept up in this otherwise large edit.
- v24/v25 (was v23/v24) still read "Full description..." against the FAQ's own "Detailed description..." wording for the same fields — that mismatch persists through the renumbering.

**Unchanged**

Field-level content not listed above; both footnote attachments' underlying fields (v26 and i37 respectively) otherwise unchanged.

### 2026-09-10 12:17 UTC (vs. 2026-09-10 10:12 UTC)

Page still returns HTTP 200 at `cra-srp-glossary2`, fetched alongside all seven other originally-tracked SRP pages in the same run — most of which did change this time (FAQ Q9 reverted, a new Q31, refreshed main-page guidance cards, CSIRT list link/stamp changes, an AR Notification Submission stamp move, and two brand-new pages discovered via the Content navigation; see `enisa-srp-faq-baseline.md`). The Glossary itself was unaffected: all 38 fields re-verified row by row, footer still "version 1.2, last update: 09/09/2026". `retrieved` updated; `last_check` and `last_change` unchanged.

### 2026-09-10 10:12 UTC (vs. 2026-09-10 07:11 UTC)

Page still returns HTTP 200 at `cra-srp-glossary2`, fetched alongside all nine other tracked SRP pages in the same run (four of which changed — Q9, a new FAQ entry, the CSIRT list, and the main page's navigation/User Guidance section; two brand-new pages were also discovered — see `enisa-srp-faq-baseline.md`). All 38 fields re-verified row by row: no field name, meaning, how-to-complete text, example, format, or per-stage status moved. Footer still verbatim lowercase "version 1.2, last update: 09/09/2026".

**Unchanged**

All 38 rows, including every previously tracked defect: field 11's contradictory meaning and its "is doesn't" typo, v26's doubled full stop, v29's missing space in "(CDaC)taking", i36's and i37's broken grammar, v28's three grounds and its "one" vs "at least one" inconsistency, and v23/v24 still reading "Full description..." against the FAQ's "Detailed". Both footnotes unchanged.

### 2026-09-10 07:11 UTC (vs. 2026-09-10 05:10 UTC)

Three field names changed, none of the wording, statuses, or the footer stamp. Still 38 fields, same numbering, no field added or removed. The footer still reads "version 1.2, last update: 09/09/2026" — unmoved despite a real content edit, the same lagging-stamp pattern already seen at every prior edit of this page.

**Changed**

- **Field 17**: "Corrective or mitigating measures **users** can take" → "Corrective or mitigating measures **that users** can take". This now matches the FAQ's own field 22 wording exactly (`enisa-srp-faq-baseline.md`, which has read "that users can take" since 2026-09-09 23:11 UTC) — a mismatch that existed but was never previously flagged, since the two tables use different field numbering and this specific pair was not among the ones spot-checked earlier.
- **Field i35**: "Type of Threat or root cause **likely** to have triggered incident" → "Type of Threat or root cause **that is likely** to have triggered incident". Brings the wording closer to the FAQ's own i40 ("Type of threat or root cause that is likely to have triggered **the** incident") but does not fully match it — the FAQ still has "the incident" where the Glossary now has only "incident", and capitalises "Threat" where the FAQ does not.
- **Field i37**: "Date/time incident occurred" → "Date/time **when the** incident occurred". This now matches the FAQ's own i42 field name exactly, word for word — again a previously-unflagged mismatch between the two tables' independent numbering.

**Unchanged**

All other 35 rows, every meaning/how-to-complete/example/format cell for the three changed rows, and every previously tracked defect: field 11's contradictory meaning and its "is doesn't" typo, v26's doubled full stop, v29's missing space in "(CDaC)taking", i36's broken grammar, i37's own "the incident was began" grammar defect (untouched by the field-name change above), v28's three grounds and its "one" vs "at least one" inconsistency, and v23/v24 still reading "Full description..." against the FAQ's "Detailed". Both footnotes unchanged.

### 2026-09-10 05:10 UTC (vs. 2026-09-10 02:08 UTC)

The footer version stamp moved for the first time since tracking began — "version 1.1, last update: 05/09/2026" → "version 1.2, last update: 09/09/2026" — and this time it actually correlates with content: two field names changed. Still 38 fields, same numbering, no field added or removed.

**Changed**

- **Field 7**: "Product **version**" → "Product **Version**" (capitalisation only, no meaning/example/format change).
- **Field i32**: "Applied **or** ongoing mitigation measures" → "Applied **and** ongoing mitigation measures". This resolves the long-tracked FAQ/Glossary mismatch: the FAQ's own Q16 table has read "Applied **and** ongoing mitigation measures" (its i37) since first capture, while the Glossary said "or" — the two now agree.

**Unchanged**

All other 36 rows, including every previously tracked defect: field 11's contradictory meaning and its "is doesn't" typo, v26's doubled full stop, v29's missing space in "(CDaC)taking", i36's and i37's broken grammar, v28's three grounds and its "one" vs "at least one" inconsistency, and v23/v24 still reading "Full description..." against the FAQ's "Detailed" (a mismatch that this run's i32 fix did not touch). Both footnotes unchanged.

### 2026-09-10 02:08 UTC (vs. 2026-09-10 01:08 UTC)

Page still returns HTTP 200 at `cra-srp-glossary2`, fetched alongside all seven other tracked SRP pages in the same run (three of which changed their "Last updated" stamp format only — CSIRT list, AR User Registration, AR Interface Functions; see `enisa-srp-faq-baseline.md`). All 38 fields re-verified row by row: no field name, meaning, how-to-complete text, example, format, or per-stage status moved. Footer still verbatim lowercase "version 1.1, last update: 05/09/2026".

**Unchanged**

All 38 rows, including every previously tracked defect: field 11's contradictory meaning and its "is doesn't" typo, v26's doubled full stop, v29's missing space in "(CDaC)taking", i36's and i37's broken grammar, v28's three grounds and its "one" vs "at least one" inconsistency, and i32's "or" against the FAQ's "and". Both footnotes unchanged.

### 2026-09-10 01:08 UTC (vs. 2026-09-10 00:10 UTC)

Page still returns HTTP 200 at `cra-srp-glossary2`, fetched alongside all seven other tracked SRP pages in the same run (one of which — the FAQ's long-tracked "Sever Incident Notification" typo in Q26 — was fixed this time; see `enisa-srp-faq-baseline.md`). All 38 fields re-verified row by row: no field name, meaning, how-to-complete text, example, format, or per-stage status moved. Footer still verbatim lowercase "version 1.1, last update: 05/09/2026".

**Unchanged**

All 38 rows, including every previously tracked defect: field 11's contradictory meaning and its "is doesn't" typo, v26's doubled full stop, v29's missing space in "(CDaC)taking", i36's and i37's broken grammar, v28's three grounds and its "one" vs "at least one" inconsistency, and i32's "or" against the FAQ's "and". Both footnotes unchanged.

### 2026-09-10 00:10 UTC (vs. 2026-09-09 23:11 UTC)

Page still returns HTTP 200 at `cra-srp-glossary2`, fetched alongside all seven other tracked SRP pages in the same run (one of which — AR User Registration, a cosmetic wording change — did change this time; see `enisa-srp-faq-baseline.md`). All 38 fields re-verified row by row: no field name, meaning, how-to-complete text, example, format, or per-stage status moved. Footer still verbatim lowercase "version 1.1, last update: 05/09/2026".

**Unchanged**

All 38 rows, including every previously tracked defect: field 11's contradictory meaning and its "is doesn't" typo, v26's doubled full stop, v29's missing space in "(CDaC)taking", i36's and i37's broken grammar, v28's three grounds and its "one" vs "at least one" inconsistency, and i32's "or" against the FAQ's "and". Both footnotes unchanged.

### 2026-09-09 22:12 UTC (vs. 2026-09-09 21:07 UTC)

Page still returns HTTP 200 at `cra-srp-glossary2`, fetched alongside all seven other tracked SRP pages in the same run (four of which did change this time — see `enisa-srp-faq-baseline.md`). All 38 fields re-verified row by row: no field name, meaning, how-to-complete text, example, format, or per-stage status moved. Footer still verbatim lowercase "version 1.1, last update: 05/09/2026". Noted for cross-reference: the PEC guidance subpage changed three of its own body instances of "Particularly Exceptional Circumstances" to "Particular Exceptional Circumstances" this run — this table's v27 field name has always read "Particular Exceptional Circumstances (PEC)", so the guidance page's wording now matches this file rather than diverging from it further.

**Unchanged**

All 38 rows, including every previously tracked defect: field 11's contradictory meaning and its "is doesn't" typo, v26's doubled full stop, v29's missing space in "(CDaC)taking", i36's and i37's broken grammar, v28's three grounds and its "one" vs "at least one" inconsistency, and i32's "or" against the FAQ's "and". Both footnotes unchanged.

### 2026-09-09 21:07 UTC (vs. 2026-09-09 12:19 UTC)

Page still returns HTTP 200 at `cra-srp-glossary2`, fetched alongside all seven other tracked SRP pages in the same run (two of which did change this time — see `enisa-srp-faq-baseline.md`). All 38 fields re-verified row by row: no field name, meaning, how-to-complete text, example, format, or per-stage status moved. Footer still verbatim lowercase "version 1.1, last update: 05/09/2026".

**Unchanged**

All 38 rows, including every previously tracked defect: field 11's contradictory meaning and its "is doesn't" typo, v26's doubled full stop, v29's missing space in "(CDaC)taking", i36's and i37's broken grammar, v28's three grounds and its "one" vs "at least one" inconsistency, and i32's "or" against the FAQ's "and". Both footnotes unchanged.

### 2026-09-09 12:19 UTC (vs. 2026-09-09 03:09 UTC)

Page still returns HTTP 200 at `cra-srp-glossary2`, fetched alongside all seven other tracked SRP pages in the same run (three of which did change — see `enisa-srp-faq-baseline.md`). All 38 fields re-verified row by row: no field name, meaning, how-to-complete text, example, format, or per-stage status moved. Footer still verbatim lowercase "version 1.1, last update: 05/09/2026".

**Unchanged**

All 38 rows, including every previously tracked defect: field 11's contradictory meaning and its "is doesn't" typo, v26's doubled full stop, v29's missing space in "(CDaC)taking", i36's and i37's broken grammar, v28's three grounds and its "one" vs "at least one" inconsistency, and i32's "or" against the FAQ's "and". Both footnotes unchanged.

### 2026-09-09 03:09 UTC (vs. 2026-09-08 00:14 UTC)

Page still returns HTTP 200 at `cra-srp-glossary2`. All 38 fields re-verified row by row: no field name, meaning, how-to-complete text, example, format, or per-stage status moved. One correction to this record, not to ENISA's page.

**Fixed (this baseline, not the page)**

- The footer's raw HTML (`<em>version 1.1, last update: 05/09/2026</em>`) is verbatim **lowercase** "version", where this file's own prose has written it as "Version 1.1" throughout. Whether ENISA's capitalisation changed or this file simply never checked the byte-level case before could not be determined from this run alone — treated as pre-existing either way and not counted against `last_change`.

**Unchanged**

All 38 rows, including every previously tracked defect: field 11's contradictory meaning and its "is doesn't" typo, v26's doubled full stop, v29's missing space in "(CDaC)taking", i36's and i37's broken grammar, v28's three grounds and its "one" vs "at least one" inconsistency, and i32's "or" against the FAQ's "and". Both footnotes unchanged.

### 2026-09-08 00:14 UTC (vs. 2026-09-07 22:0x)

Page unchanged. One correction to this record, not to ENISA's page.

**Fixed (this baseline, not the page)**

- The v28 PEC Delay Reason row's Example cell was missing the second of its three grounds and showed a stray "N/A" in its place. The live page puts the three grounds in three table rows under one `rowspan`; an earlier capture picked up an adjacent status cell instead of the middle row's text. Restored to the full three-item list — ENISA's page has always read that way.

**Unchanged**

All 38 rows diffed row by row: no wording, numbering or status moved, and every tracked defect is still present exactly as recorded — field 11's contradictory meaning and its "is doesn't" typo, v26's doubled full stop, v29's missing space, i36's and i37's broken grammar, v28's "one" against "at least one", and i32's "or" against the FAQ's "and". Footer still Version 1.1, 05/09/2026.

### 2026-09-07 22:0x UTC (vs. the same evening's capture)

Content edited **without a version bump** — the footer still says Version 1.1, 05/09/2026. On this page the version stamp is not a change signal; diff the rows. 38 fields, same numbering, no field name changed; 29 of the 38 rows differ.

**Changed**

- **"How to complete" is now illustration, not instruction.** 29 rows had their completion sentence reworded from an imperative into "For example, …" — "Enter a short, specific title…" became "For example, enter a short, specific title…". Nothing else in those sentences moved. It reads as a deliberate pass to stop the examples being taken as requirements, and it weakens every completion instruction on the page in the same way.
- **v28 PEC Delay Reason**, the one substantive row: the Meaning is now garbled ("You may select one of the three of the legally specified circumstances…"), and the numbered list that carried the three grounds is flattened into prose. How to complete gained "You may select at least one of the three options." The grounds themselves are unchanged — third subparagraph of Art. 16(2) CRA.

**Watch**

- **v28 now says both "one of the three" and "at least one of the three".**
- **Field 11 is untouched** by this pass and the one before it: its Meaning still describes whether the product has a user interface for informing users, while its instruction, format and example ask Yes/No about the support period — and "or No when is doesn't" is still there.
- i32's "Applied **or** ongoing mitigation measures" still stands against the FAQ's "Applied **and** ongoing".

**Editorial**

Four new defects, each reproduced verbatim in the tables below: v26 a doubled full stop, v29 a missing space in "(CDaC)taking", i36 "another relevant become aware" (was "another relevant party became aware"), i37 "the incident was began".

**Unchanged**

The two footnotes.

### 2026-09-07 evening — the page moved

**Fixed**

- **Diagnosis corrected.** The Glossary moved from `.../cra-srp-glossary` to `.../cra-srp-glossary2`: the old path returns 403, the new one 200. It had been recorded here as possibly unpublished. A 403 on one page while its neighbours stay up reads like an unpublication — it was a move. The rule now sits in the frontmatter: check where a page went before concluding it is gone.

**Unchanged**

38 fields, identical numbering, no name changed at the time of the move — including field 11's contradiction and its "when is doesn't" typo. Version 1.1, 05/09/2026.

### 2026-09-07 — this file rebuilt as tables

Repository-side housekeeping, not an ENISA change. Both items were introduced by this file's first commit the same day.

- **Rebuilt as three markdown tables**, one row per field, replacing the prose blocks — easier to scan, and diffable row by row against the live page's own table.
- **Invalid YAML frontmatter fixed**: `page_version: 1.1, last update per page footer: 05/09/2026` carried an unquoted colon-space, which GitHub's renderer and any strict parser reject outright. Quoted.

### 2026-09-07 05:06 UTC — initial capture

First full-detail capture. Found by the FAQ routine's run that morning, when the FAQ overhaul added links to two previously untracked pages. Written from the 05:06 UTC fetch: hours later the page returned 403 — it had moved, see above — and could not be re-fetched at write time. `enisa-srp-faq-baseline.md` holds only a trimmed field-name/status summary of the same page.


## Page metadata

- Version: 1.3 (moved from 1.2 on 2026-09-10 13:11 UTC)
- Page's own "last update" footer: 10 September 2026 (moved from 09/09/2026 on 2026-09-10 13:11 UTC)
- Columns on the live page, per field: Nr. | Field | Applies to AEV or SI | What this field means | How you may complete it | Example | Expected format | Early Warning (EW) 24h | 72h | Final Report (FR)
- Field count: 39 (was 38 before 2026-09-10 13:11 UTC) — 18 Common, 12 AEV (v19–v30), 9 SI (i31–i39)

## Common fields (Both AEV and SI)

| Nr. | Field | Applies to | Meaning | How to complete | Example | Format | EW 24h | 72h | Final Report |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Notification type (Vulnerability/Incident) | Both | Indicates whether the notification concerns an actively exploited vulnerability (AEV) or a severe incident (SI) having an impact on the security of a product with digital elements. | Select Actively Exploited Vulnerability when reporting an AEV. Select Severe Incident when reporting a SI having an impact on the security of a product with digital elements. | Vulnerability | Select one: Vulnerability or Incident | Required | copied-or-updated | copied-or-updated |
| 2 | Title | Both | Short human-readable name for the notification. | For example, enter a short, specific title that allows users to recognise the affected product and the reported issue. Do not include confidential technical detail that is unnecessary for identification (max. 255 characters). | Active exploitation affecting Product X version 4.2. | Plain text; concise title | Required | copied-or-updated | copied-or-updated |
| 3 | Summary | Both | Concise overview of the facts, affected product, and issue being notified. | For example, provide a concise overview of what happened, the affected product or version, the known impact, and the current mitigation status. Use factual information available at the reporting stage (max. 4000 characters). | An actively exploited vulnerability affects Product X 4.2. A temporary workaround is available, and a security update is being prepared. | Short paragraph | Required | copied-or-updated | copied-or-updated |
| 4 | Manufacturer name | Both | Name of the natural or legal person who develops or manufactures the product with digital elements or has the product with digital elements designed, developed or manufactured, and markets it under its name or trademark, whether for payment, monetisation or free of charge. | No user action is required. The platform creates or updates this value automatically based on what you wrote when you registered to the Platform or added at a later stage. You may review it only to confirm that the displayed information is consistent with the notification history. | Automatically populated by the platform during the notification submission or free text during manufacturer registration [Name of the company]. | System-generated / read-only | Required | copied-or-updated | copied-or-updated |
| 5 | Member States where product available (Concerned CSIRT) | Both | Member States in which territory the manufacturer is aware that the affected product has been made available; used to determine concerned CSIRTs. | The Platform will automatically show your CDaC, however, you may also select other Member States (MS) where the affected product is available *(three word-level edits 2026-09-10 17:13 UTC: "show you CDaC" → "show your CDaC"; "you may select" → "you may also select"; "has been made available" → "is available"; no meaning/status change)*, based on the information currently known to the manufacturer. Update the selection if new distribution information becomes available. | Belgium as your CDaC, automatically populated by the platform and you may add Greece and Italy and MS where the affected product has been made available | Select one or more Member States | Required *(was "Required if such information available" until 2026-09-10 13:11 UTC)* | copied-or-updated | copied-or-updated |
| 6 | Product Name | Both | Name that identifies the affected product with digital elements. | For example, enter the official commercial or technical name of the affected product with digital elements. Use the same name that appears in product technical documentation or market information (max. 255 characters). | Product X | Official product name | Required | copied-or-updated | copied-or-updated |
| 7 | Product Version | Both | Version, release, build, model, or other revision information required to identify the affected product instance. | For example, enter every affected version, release, build, model, or firmware revision. Use exact identifiers and clearly state a range when multiple versions are affected (max. 255 characters). | 4.0 to 4.2.1 | Version or version range | Required | copied-or-updated | copied-or-updated |
| 8 | Product Type (Default/Important Product with Digital Elements/Critical Product with Digital Elements) *(names expanded 2026-09-10 13:11 UTC; was "(Default/Important/Critical)")* | Both | Regulatory category indicating whether the product is default, important, or critical under the CRA classification framework. | For example, select the CRA regulatory type applicable to the product. Choose Important or Critical only where the product falls within the relevant CRA category (Annexes III and IV); otherwise select Default. | Important Product with Digital Elements *(was "Important" until 2026-09-10 13:11 UTC)* | Select one: Default, Important, Critical | Optional | copied-or-updated | copied-or-updated |
| 9 | Product class *(lowercase "class" since 2026-09-10 13:11 UTC; was "Product Class")* | Both | For an Important Product with Digital Elements *(wording expanded 2026-09-10 13:11 UTC; was "an important product")*, the applicable Class I or Class II category used for conformity-assessment treatment. | For example, for an important product, select the applicable CRA class. Leave the field empty when the product is not classified as an important product or when no class applies. | Class II | Select one configured Class | Optional | copied-or-updated | copied-or-updated |
| 10 | Product category *(lowercase "category" since 2026-09-10 13:11 UTC; was "Product Category")* | Both | The applicable CRA product category, normally selected from the relevant category list, as mentioned in the CRA Annexes III or IV. | You may select the category that best matches the affected product under the applicable CRA category list. You may use the product’s core functionality, not only its commercial name. | Choose between: Hardware devices with Security Boxes; Smart meter gateways within smart metering systems and other devices for advanced security purposes, including secure cryptoprocessing  devices *(new double-space typo, since 2026-09-10 13:11 UTC)*; or Smartcards or similar devices, including secure elements. | Select one configured category | Optional | copied-or-updated | copied-or-updated |
| 11 | End of support indicator | Both | Indicates whether the product with digital elements has reached the end of the support period. *(rewritten 2026-09-10 13:11 UTC — the long-tracked contradictory Meaning, describing a user-interface indicator instead of this field's actual Yes/No content, is gone.)* | You may select one: "Yes" when the product with digital elements has reached the end of the support period or "No" when it doesn’t. *(the "is doesn't" typo fixed to "it doesn't" 2026-09-10 13:11 UTC)* | Yes | Select one: Yes or No | Optional | copied-or-updated | copied-or-updated |
| 12 | Component name | Both | Name of the software or hardware component in which the vulnerability or incident is located or observed. | For example, enter the name of the affected hardware or software component. You may include the component version when known. Leave empty if the issue cannot be attributed to a component (max. 255 characters). | Authentication module 3.1 | Component name and optional version | Optional | copied-or-updated | copied-or-updated |
| 13 | Mitigating measure expected shortly | Both | Indicates whether an effective risk-mitigation measure, such as a security update or user guidance, is expected to become available. | For example, select "Yes" when an effective security update, workaround, or user guidance is expected shortly and the expectation is supported by a remediation plan. Otherwise select "No". *(reworded 2026-09-10 13:11 UTC — dropped "only" and the Unknown option; was "select Yes only when... Otherwise select No or Unknown.")* | Yes | Select one: "Yes" or "No" *(Unknown option dropped 2026-09-10 13:11 UTC; was "Yes, No, Unknown")* | Optional | copied-or-updated | copied-or-updated |
| 14 | User Action able to reduce impact | Both | Action that product users can take to prevent, reduce, or contain the impact of the actively exploited vulnerability or severe incident. *(reworded 2026-09-10 13:11 UTC; was "the vulnerability or incident")* | You may describe the immediate action a user can take to reduce the likelihood or impact of the vulnerability exploited or the incident. You may provide clear, practical instructions and identify any limitation or prerequisite (max. 4000 characters). | Disable the affected interface until the security update is installed. | Action-oriented text | Optional | copied-or-updated | copied-or-updated |
| 15 | Considered sensitivity of information | Both | Manufacturer's assessment of how sensitive the notified information is to inform secure handling and dissemination decisions. *(comma before "to inform" dropped 2026-09-10 13:11 UTC)* | You may describe why any submitted information requires restricted handling. Identify the sensitive element and the potential consequence of premature or wider disclosure. Do not use a generic confidentiality statement (max. 255 characters). | The technical details reveal an unpatched exploitation path that is not yet publicly known. | Concise justification | Optional | Optional *(was "Required if such information available" until 2026-09-10 13:11 UTC)* | copied-or-updated |
| 16 | Corrective or mitigating measures taken | Both | Actions already implemented by the manufacturer or other responsible party to correct the issue or reduce its risk or impact. | For example, list the actions already taken to correct the issue or to reduce the risk. You may include containment, configuration changes, update withdrawal, credential rotation, monitoring, or other completed measures, with dates where useful. (max. 2000 characters). | Disabled the affected service; revoked exposed credentials; increased monitoring. | Bulleted list or structured text | Optional | Optional *(was "Required" until 2026-09-10 13:11 UTC)* | Required |
| 17 | Corrective or mitigating measures that users can take | Both | Instructions or actions users can apply to reduce exposure or impact, including workarounds, configuration changes, patches, or isolation measures. | For example, provide step-oriented guidance that users can apply. Prioritise the effective fix, then state temporary workarounds and any operational impact. Clearly identify actions that are no longer recommended (max. 4000 characters). | Install version 4.2.2. Until installation, restrict management-interface access to trusted networks. | Action-oriented text | Optional | Optional *(was "Required" until 2026-09-10 13:11 UTC)* | Required |
| 18 | Attack vector | Both | Description or structured classification of the path or means by which exploitation or compromise can occur. | For example, describe how the vulnerability may be exploited or how the incident reached the affected product. State the relevant interface, access path, protocol, or user interaction. Avoid unsupported assumptions (max. 255 characters). | Remote network access through an exposed API. | Short, structured description or configured classification | N/A *(was "Optional" until 2026-09-10 13:11 UTC)* | Optional | Optional |

## Actively Exploited Vulnerability (AEV) fields

| Nr. | Field | Applies to | Meaning | How to complete | Example | Format | EW 24h | 72h | Final Report |
|---|---|---|---|---|---|---|---|---|---|
| v19 | CVE ID | AEV | CVE Identifier (CVE ID) assigned to the publicly disclosed vulnerability under the Common Vulnerabilities and Exposures (CVE) Program. | You may enter the official CVE ID only if one has been assigned by the competent CNA. Copy the ID exactly as published. Leave the field empty if no ID exists (max. 255 characters). | CVE-2026-12345 | CVE identifier | Optional | copied-or-updated | copied-or-updated |
| v20 | EUVD ID | AEV | Identifier of the vulnerability record in the European Vulnerability Database (EUVD). | You may enter the official EUVD ID if one has been assigned by ENISA. Copy the ID exactly as published. Leave the field empty if no ID exists (max. 255 characters). | EUVD-2026-12345 | EUVD identifier | Optional | copied-or-updated | copied-or-updated |
| v21 | General information | AEV | High-level description of the vulnerability and, where known, how exploitation works, without requiring the full final technical analysis. | For example, describe the vulnerability at a high level and explain how the known exploit operates. Include the affected function, required access, and observed exploitation behaviour. Do not include unverified attribution (max. 4000 characters). | An authentication bypass in the management interface allows a remote actor with network access to execute privileged actions. | Structured narrative | Optional | Required | copied-or-updated |
| v22 | Date when corrective or mitigating measure has been available | AEV | Date and time when the mitigating measure has been available. | For example, enter the date and time when the mitigating measure has been available. | 2026-09-02 09:15 UTC | Date and time | Optional | Optional | Required |
| v23 | Details about the security update/corrective measure available *(new field, since 2026-09-10 13:11 UTC)* | AEV | Information on available corrective measures and security updates. | You may add the available corrective measures and security updates. For example, security patches or software updates (max. 2000 characters). | Security patches | Detailed structured narrative | Optional | Optional | Required |
| v24 | Full description of the Severity of the vulnerability *(was "v23"; capitalisation of "Severity" and renumbering since 2026-09-10 13:11 UTC)* | AEV | Complete description of the actively exploited vulnerability, including at least its severity. *(reworded 2026-09-10 13:11 UTC; was "the vulnerability")* | For example, provide the completed technical description of the vulnerability. Including the assessed severity rating, classification, rationale for the assessment and other relevant factors or criteria supporting the assigned severity level (max. 4000 characters). | Authentication validation is missing in endpoint X... Severity: High... Affected versions: 4.0–4.2.1... | Detailed structured narrative | Optional | Optional | Required |
| v25 | Full description of the Impact of the vulnerability *(was "v24"; capitalisation of "Impact" and renumbering since 2026-09-10 13:11 UTC)* | AEV | Complete description of the actively exploited vulnerability, including at least its impact. *(reworded 2026-09-10 13:11 UTC; was "the vulnerability")* | For example, provide the completed technical description of the vulnerability. Including the potential or actual impact of the vulnerability, the affected systems, components, data, users or services, as applicable (max. 4000 characters). | Authentication validation is missing in endpoint X... Impact: High... Affected versions: 4.0–4.2.1... | Detailed structured narrative | Optional | Optional | Required |
| v26 | Date and time when you become aware of the Actively Exploited Vulnerability [1] *(was "v25", "Date/time"; renumbered and reworded since 2026-09-10 13:11 UTC)* | AEV | Date and time when the manufacturer or another relevant party first detected the vulnerability. | For example, enter the date and time when the vulnerability was first detected. If the exact time is unknown, enter the best supported estimate and identify it as estimated in the vulnerability description. | 2026-08-24 09:15 UTC | Date and time | Required | copied-or-updated | copied-or-updated |
| v27 | Malicious actor that has exploited/is exploiting the vulnerability *(was "v26"; renumbering only, since 2026-09-10 13:11 UTC)* | AEV | Available information about the actor that exploited or is exploiting the vulnerability, without requiring attribution where information is unavailable. | You may enter confirmed information about the malicious actor or observed activity. If attribution is unconfirmed, describe the observed indicators and state that attribution is unknown (max. 100 characters).. | Unknown actor; observed infrastructure includes the indicators listed in Reference REF-2026-18. | Free text | Optional | Optional | Required if such information available |
| v28 | Particular Exceptional Circumstances (PEC) *(was "v27"; renumbering only, since 2026-09-10 13:11 UTC)* | AEV | Selection indicating that one or more legally specified circumstances in the third subparagraph of Article 16 (2) of CRA justify withholding the full 72-hour AEV notification from simultaneous access by ENISA and/or delaying wider dissemination. | You may select the applicable exceptional circumstance only when the corresponding legal condition is met. | — | Select applicable PEC option(s) | N/A | Optional | N/A |
| v29 | PEC Delay Reason *(was "v28"; renumbering since 2026-09-10 13:11 UTC)* | AEV | You may select at least one of the three legally specified circumstances justifying withholding the full 72-hour AEV notification from simultaneous access by ENISA and/or delaying wider dissemination. *(Meaning fixed 2026-09-10 13:11 UTC; was "one of the three of the" — now matches this row's own How-to-complete, resolving the tracked inconsistency)* | Support the selection with specific facts in PEC Delay Reason and indicate the requested dissemination delay. You may select at least one of the three options. | You may choose: the notified vulnerability has been actively exploited by a malicious actor and, according to the information available, it has been exploited in no other Member State than the one of the CSIRT designated as coordinator to which the manufacturer has notified the vulnerability; or<br>that any immediate further dissemination of the notified vulnerability would likely result in the supply of information the disclosure of which would be contrary to the essential interests of that Member State; or<br>that the notified vulnerability poses an imminent high cybersecurity risk stemming from the further dissemination; | Select applicable check box | N/A | Optional | N/A |
| v30 | Please provide further information *(was "v29"; renumbering since 2026-09-10 13:11 UTC)* | AEV | Description of anything that should be helpful for CSIRT Designated as Coordinator (CDaC)taking *(missing space on the live page, since 2026-09-07)* their decision. | You may provide additional information (max. 800 characters). *(character limit added 2026-09-10 13:11 UTC; was "You may provide additional information(s)." with no stated limit)* | We consider it very important for national security. | Free text | Optional | Optional | copied-or-updated |

## Severe Incident (SI) fields

| Nr. | Field | Applies to | Meaning | How to complete | Example | Format | EW 24h | 72h | Final Report |
|---|---|---|---|---|---|---|---|---|---|
| i31 | Incident is suspected of unlawful or malicious acts *(was "i30"; renumbering since 2026-09-10 13:11 UTC)* | SI | Boolean indication of whether available evidence suggests the incident resulted from unlawful or malicious activity. | For example, select Yes when available evidence indicates intentional unlawful or malicious activity. Select No when the event is assessed as non-malicious. Select Unknown while the cause remains unresolved (max. 255 characters). *(character limit added 2026-09-10 13:11 UTC; not previously stated)* | Yes | Select one: Yes, No, Unknown | Required | copied-or-updated | copied-or-updated |
| i32 | General information, about the nature of the incident *(was "i31", "General information about nature of incident"; comma added and renumbered since 2026-09-10 13:11 UTC)* | SI | High-level account of what happened, how the incident manifested, and the affected security properties or functions. | For example, describe what occurred, the affected product functions or security properties, and the currently known scope. Focus on confirmed facts available at the 72-hour stage (max. 4000 characters). | Malicious code executed through the update service and affected the integrity of locally stored configuration data. | Structured narrative | Optional | Required | copied-or-updated |
| i33 | Applied and ongoing mitigation measures *(was "i32"; renumbering since 2026-09-10 13:11 UTC)* | SI | Actions that have been taken by the manufacturer or other responsible party and are still ongoing to correct the issue or reduce its risk or impact. *(Meaning fixed 2026-09-10 13:11 UTC; was "...or are still ongoing" — now matches the field name's "and")* | For example, list the actions already applied or ongoing to correct the issue or reduce risk. Include containment, configuration changes, update withdrawal, credential rotation, monitoring, or other completed measures, with dates where useful (max. 4000 characters). | Disabled the affected service; revoked exposed credentials; increased monitoring. | Structured narrative | Optional | Optional | Required |
| i34 | Detailed description of the Severity of the incident *(was "i33"; renumbering only, since 2026-09-10 13:11 UTC)* | SI | Complete the detailed description of the severity of the incident. | For example, provide the completed description of the severity of the incident. Include the sequence of events, affected products and functions, severity, scope, evidence, root cause, response measures, and recovery status (max. 4000 characters). | Low – limited impact, no significant disruption to operation. | Structured narrative | Optional | Optional | Required |
| i35 | Detailed description of the Impact of the incident *(was "i34"; renumbering only, since 2026-09-10 13:11 UTC)* | SI | Complete the detailed description of the impact of the incident. | For example, provide the completed description of the impact of the incident, including the impact on the product, data, functions, users, or connected systems (max. 4000 characters). | Minimal – no material impact of operations, users or data. | Structured narrative | Optional | Optional | Required |
| i36 | Type of Threat or root cause that is likely to have triggered incident *(was "i35"; renumbering only, since 2026-09-10 13:11 UTC)* | SI | Most likely threat category, initiating event, weakness, failure, or root cause that triggered the incident. | For example, state the most likely threat type and root cause supported by the investigation. Explain the evidence briefly and mark the conclusion as preliminary when analysis is incomplete (max. 255 characters). | Supply-chain compromise caused by an unauthorised modification to the update package. | Classification plus short explanation | Optional | Optional | Required |
| i37 | Date and time when you become aware of the incident (UTC time) [2] *(was "i36", "Date/time when you become aware..."; renumbered and reworded since 2026-09-10 13:11 UTC)* | SI | Date and time when the manufacturer or another relevant entity becomes aware of the incident. *(broken grammar fixed 2026-09-10 13:11 UTC; was "another relevant become aware")* | For example, enter the date and time you became aware of the incident. *(tense fixed 2026-09-10 13:11 UTC; was "you become aware")* If the exact time is unknown, enter the best supported estimate and identify it as estimated in the incident description. | 2026-08-24 09:15 UTC | Date and time | Required | Required *(was "copied-or-updated" until 2026-09-10 13:11 UTC)* | copied-or-updated |
| i38 | Date and time when the incident occurred (UTC time) *(was "i37", "Date/time when the incident occurred"; renumbered and reworded since 2026-09-10 13:11 UTC)* | SI | Known or estimated date and time when the incident began or took place. | For example, enter the date and time when the incident began or occurred. *(broken grammar fixed 2026-09-10 13:11 UTC; was "the incident was began or occurred")* If the exact time is unknown, enter the best supported estimate and identify it as estimated in the incident description. | 2026-08-24 09:15 UTC | Date and time | Optional | Required *(was "Optional" until 2026-09-10 13:11 UTC)* | Optional |
| i39 | Initial assessment of the incident *(was "i38"; renumbering only, since 2026-09-10 13:11 UTC)* | SI | Preliminary analysis of the incident's severity, scope, likely impact, affected functions or data, and immediate implications. | For example, provide the preliminary assessment of severity, scope, affected security properties, products or users, and likely impact. Clearly distinguish confirmed findings from matters still under investigation (max. 4000 characters). | Confirmed impact is limited to integrity of configuration data on three product instances; broader exposure remains under investigation. | Structured narrative | Optional | Required | copied-or-updated |

## Footnotes (from the live page)

- [1] This field will be available in the next release of the Platform. (attached to field v26, was v25 before the 2026-09-10 13:11 UTC renumbering)
- [2] In the current release this field is named: "Date and time when the incident was detected (UTC time)". *(reworded 2026-09-10 13:11 UTC; was "Date/time the incident was detected")* (attached to field i37, was i36 before the renumbering)

## Check log

- 2026-09-07: Initial capture. Fetched raw HTML of the Glossary page at 05:06 UTC (as part of the
  ENISA SRP FAQ baseline-check routine's run that day, which discovered the page via updated site
  navigation) and recorded full field-by-field content here for the first time, as prose blocks.
- 2026-09-07 (same day, follow-up): rebuilt the field content as maintained markdown tables (one
  table per group, one row per field) at the user's request, and fixed an invalid-YAML frontmatter
  bug from the initial commit (`page_version` had an unquoted colon inside a plain scalar, which
  broke GitHub's frontmatter renderer — "mapping values are not allowed in this context"). A
  same-day re-check (15:56 UTC) had found the live page returning HTTP 403 while the rest of the
  tracked SRP pages remained reachable; this file still reflects the 05:06 UTC capture, the last
  known-good state. The next check should first confirm whether the page is back (200) or still
  down (403/other), update `status` in the frontmatter accordingly, and — if reachable — diff the
  live tables row-by-row against the 38 fields captured here.

- 2026-09-07 (second check): page fetched at its new address, HTTP 200. Content edited without a version bump — footer still reads "Version 1.1, last update: 05/09/2026". 29 of 38 rows reworded ("How to complete" recast as "For example, …"), v28 PEC Delay Reason substantively changed and internally inconsistent, four new typos, field 11 still contradictory. Tables above updated; see the change log.

- 2026-09-08: page fetched at `cra-srp-glossary2`, HTTP 200. All 38 fields re-verified row-by-row against this baseline — no change anywhere, footer still "Version 1.1, last update: 05/09/2026". Corrected a likely capture artifact in v28's Example cell (a stray "N/A" standing in for the second of three PEC grounds, traced to the live page's own 3-row rowspan table structure); see the change log entry at the top. `last_check` and `retrieved` updated to today; `last_change` left at 2026-09-07 since ENISA's content did not change.

- 2026-09-09 (03:09 UTC): page fetched at `cra-srp-glossary2`, HTTP 200, alongside all seven other tracked SRP pages in the same run (all HTTP 200, all re-verified unchanged — see `enisa-srp-faq-baseline.md`). All 38 fields re-verified row-by-row — no field, meaning, example, format or status moved. One capture correction: the footer's raw HTML is verbatim lowercase "version 1.1, last update: 05/09/2026", where this file had written "Version 1.1" throughout; corrected as a baseline-fidelity fix, not counted as an ENISA change since it could not be determined whether the case was ever verified byte-for-byte before. See the change log entry at the top. `last_check` (already bumped to today by the day's earlier heartbeat run) and `retrieved` updated; `last_change` left at 2026-09-07.
- 2026-09-09 (12:19 UTC): page fetched at `cra-srp-glossary2`, HTTP 200, alongside all seven other tracked SRP pages in the same run — three of those seven did change this time (FAQ Q9 and its Q8 tag, AR User Registration's General Notes, and the PEC guidance page; see `enisa-srp-faq-baseline.md`). The Glossary itself was unaffected: all 38 fields re-verified row-by-row, footer unchanged. `retrieved` updated; `last_check` and `last_change` unchanged (already today's date / 2026-09-07 respectively).
- 2026-09-09 (21:07 UTC): page fetched at `cra-srp-glossary2`, HTTP 200, alongside all seven other tracked SRP pages in the same run — two of those seven changed this time (AR Interface Functions and the PEC guidance page, both rewritten again; see `enisa-srp-faq-baseline.md`). The Glossary itself was unaffected: all 38 fields re-verified row-by-row, footer still "version 1.1, last update: 05/09/2026". `retrieved` updated; `last_check` and `last_change` unchanged (already today's date / 2026-09-07 respectively).
- 2026-09-09 (22:12 UTC): page fetched at `cra-srp-glossary2`, HTTP 200, alongside all seven other tracked SRP pages in the same run — four of those seven changed this time (AR Notification Submission and Update, AR User Registration, AR Interface Functions, and the PEC guidance page; see `enisa-srp-faq-baseline.md`). The Glossary itself was unaffected: all 38 fields re-verified row-by-row, footer unchanged. `retrieved` updated; `last_check` and `last_change` unchanged.
- 2026-09-09 (23:11 UTC): page fetched at `cra-srp-glossary2`, HTTP 200, alongside all seven other tracked SRP pages in the same run — the FAQ and CSIRT-list pages changed this time (see `enisa-srp-faq-baseline.md`). The Glossary itself was unaffected: all 38 fields re-verified row-by-row, footer unchanged. `retrieved` updated; `last_check` and `last_change` unchanged.
- 2026-09-10 (00:10 UTC): first check of the day. Page fetched at `cra-srp-glossary2`, HTTP 200, alongside all seven other tracked SRP pages in the same run — one of those seven changed this time, a cosmetic wording tweak on the AR User Registration guidance page (see `enisa-srp-faq-baseline.md`). The Glossary itself was unaffected: all 38 fields re-verified row-by-row, footer still "version 1.1, last update: 05/09/2026". `retrieved` and `last_check` updated to 2026-09-10; `last_change` left at 2026-09-07 since ENISA's Glossary content itself did not change.
- 2026-09-10 (01:08 UTC): page fetched at `cra-srp-glossary2`, HTTP 200, alongside all seven other tracked SRP pages in the same run — the FAQ changed this time (Q26's "Sever" → "Severe" typo fixed; see `enisa-srp-faq-baseline.md`). The Glossary itself was unaffected: all 38 fields re-verified row-by-row, footer unchanged. `retrieved` updated; `last_check` and `last_change` unchanged.
- 2026-09-10 (02:08 UTC): page fetched at `cra-srp-glossary2`, HTTP 200, alongside all seven other tracked SRP pages in the same run — three of those seven changed date-stamp format only this time (see `enisa-srp-faq-baseline.md`). The Glossary itself was unaffected: all 38 fields re-verified row-by-row, footer unchanged. `retrieved` updated; `last_check` and `last_change` unchanged.
- 2026-09-10 (05:10 UTC): page fetched at `cra-srp-glossary2`, HTTP 200, alongside all seven other tracked SRP pages in the same run — all seven other pages unchanged this run (see `enisa-srp-faq-baseline.md`). The Glossary itself moved for the first time since 2026-09-07: footer version bumped "1.1, last update: 05/09/2026" → "1.2, last update: 09/09/2026", and two field names changed accordingly — field 7 "Product version" → "Product Version", and field i32 "Applied or ongoing mitigation measures" → "Applied and ongoing mitigation measures" (the latter resolves the long-tracked FAQ/Glossary "or"/"and" mismatch). All other 36 rows and both footnotes re-verified unchanged, including every previously tracked defect. `retrieved`, `last_check`, and `last_change` all updated to 2026-09-10; `page_version` and the page-metadata section updated. See the change log entry at the top for detail.
- 2026-09-10 (07:11 UTC): page fetched at `cra-srp-glossary2`, HTTP 200, alongside all seven other tracked SRP pages in the same run — all seven other pages unchanged this run (see `enisa-srp-faq-baseline.md`). Three field names changed: field 17 "Corrective or mitigating measures users can take" → "...that users can take" (now matches the FAQ's own field 22 exactly); field i35 "Type of Threat or root cause likely to have triggered incident" → "...that is likely to have triggered incident" (closer to, but not identical with, the FAQ's i40); field i37 "Date/time incident occurred" → "Date/time when the incident occurred" (now matches the FAQ's own i42 exactly). The footer stamp did not move — still "version 1.2, last update: 09/09/2026" — the same lagging-stamp pattern seen at every previous edit of this page. All other 35 rows, every other cell of the three changed rows, and both footnotes re-verified unchanged. `retrieved` updated to 2026-09-10 (07:11 UTC); `last_check` and `last_change` were already 2026-09-10 from the earlier run today and needed no further update. See the change log entry at the top for detail.
- 2026-09-10 (09:09 UTC): page fetched at `cra-srp-glossary2`, HTTP 200, alongside all seven other tracked SRP pages in the same run — only the FAQ's Q9 changed this time (regressed to a placeholder URL sentence; see `enisa-srp-faq-baseline.md`). The Glossary itself was unaffected: all 38 fields re-verified row-by-row, footer unchanged. `retrieved` updated; `last_check` and `last_change` unchanged.
- 2026-09-10 (10:12 UTC): page fetched at `cra-srp-glossary2`, HTTP 200, alongside all nine other tracked SRP pages in the same run (two of them newly discovered this run — see `enisa-srp-faq-baseline.md`). Four of those nine other pages changed this time (Q9 reverted, a new FAQ entry, the CSIRT list's Croatia/Malta links, and the main page's navigation/User Guidance section). The Glossary itself was unaffected: all 38 fields re-verified row-by-row, footer still "version 1.2, last update: 09/09/2026". `retrieved` updated; `last_check` and `last_change` unchanged.
- 2026-09-10 (12:17 UTC): page fetched at `cra-srp-glossary2`, HTTP 200, alongside all seven other originally-tracked SRP pages in the same run — most of those seven changed this time, and two brand-new pages (AR User Manual, Terms and Conditions) were discovered via the main page's Content navigation; see `enisa-srp-faq-baseline.md`. The Glossary itself was unaffected: all 38 fields re-verified row by row, footer still "version 1.2, last update: 09/09/2026". `retrieved` updated to 2026-09-10 (12:17 UTC); `last_check` and `last_change` already 2026-09-10, no further update needed.
- 2026-09-10 (13:11 UTC): page fetched at `cra-srp-glossary2`, HTTP 200, alongside all nine other tracked SRP pages in the same run (one of which, AR User Registration guidance, also changed — see `enisa-srp-faq-baseline.md`). The Glossary itself changed substantially for the first time since 2026-09-07: footer version bumped "1.2, last update: 09/09/2026" → "1.3, last update: 10 September 2026"; field count 38 → 39 with a new AEV field (v23) inserted, cascading v23–v29 to v24–v30 and i30–i38 to i31–i39; several long-tracked defects fixed (field 11's contradictory Meaning, i37/i38's broken grammar, v29's "one"/"at least one" inconsistency, i33's "or"/"and" mismatch); several per-stage status values changed (fields 5, 15, 16, 17, 18, and the renumbered i37/i38); field 13 lost its "Unknown" selectable option; two character limits were added (i31, v30) where none existed before. All row content re-verified field by field against the live page's raw table structure. `retrieved`, `last_check`, and `last_change` all updated to 2026-09-10 (13:11 UTC). See the change log entry at the top for full detail.
- 2026-09-10 (14:07 UTC): page fetched at `cra-srp-glossary2`, HTTP 200, alongside all nine other tracked SRP pages in the same run (two of which changed cosmetically this time — a main-page FAQ-card blurb quoted in full for the first time, and the Terms and Conditions link losing a trailing space; see `enisa-srp-faq-baseline.md`). The Glossary itself was unaffected: all 39 fields re-verified row by row, footer still "Version 1.3. Last update: 10 September 2026". `retrieved` updated; `last_check` and `last_change` unchanged.
- 2026-09-10 (15:10 UTC): page fetched at `cra-srp-glossary2`, HTTP 200, alongside all nine other tracked SRP pages in the same run (one of which changed cosmetically this time — the main page's AR User Manual download card `href`, malformed since first capture, was fixed; see `enisa-srp-faq-baseline.md`). The Glossary itself was unaffected: all 39 fields re-verified row by row against the raw table structure, footer still "Version 1.3. Last update: 10 September 2026". `retrieved` updated; `last_check` and `last_change` unchanged.
- 2026-09-10 (22:13 UTC): page fetched at `cra-srp-glossary2`, HTTP 200, alongside all nine other tracked SRP pages in the same run (one of which changed this time — FAQ Q17 gained a closing sentence; two editorial first-time transcriptions also noted on the main page; see `enisa-srp-faq-baseline.md`). The Glossary itself was unaffected: all 39 fields re-verified row by row against the raw table structure, footer still "Version 1.3. Last update: 10 September 2026". `retrieved` updated; `last_check` and `last_change` unchanged.
