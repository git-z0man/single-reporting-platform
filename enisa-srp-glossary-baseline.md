---
source: ENISA — CRA SRP Glossary
url: https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2
old_url: https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary (returns HTTP 403 since at least 2026-09-07; superseded, see status)
page_version: "1.1 (page footer: last update 05/09/2026)"
retrieved: 2026-09-07 (fetched 22:02 UTC)
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
  consistent with a move, and that is what happened. Content verified identical
  after the move: 38 fields, same numbering, no name changed. Re-verify the URL on
  every future check, not just the status code.
last_check: 2026-09-07
last_change: 2026-09-07
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

### 2026-09-07 (22:0x UTC) — content edited without a version bump

The page still shows **Version 1.1, last update 05/09/2026** in its footer, but its content
changed on 2026-09-07. **The version stamp on this page is not a reliable change signal** —
diff the rows, not the header. Field count, numbering and every field name are unchanged
(38 fields: 18 common, v19–v29, i30–i38). 29 of the 38 rows differ.

**The systematic change: "How to complete" is now phrased as illustration, not instruction.**
29 rows had their completion instruction reworded from an imperative to "For example, …" —
"Enter a short, specific title…" became "For example, enter a short, specific title…",
"Provide a concise overview…" became "For example, provide…", and so on. Nothing else in
those sentences moved. It reads as a deliberate pass to stop the examples being taken as
requirements, and it weakens every completion instruction on the page in the same way.

**Substantive change in one row: v28 PEC Delay Reason.**

- Meaning was "One of the legally specified circumstances justifying withholding…"; it now
  reads "**You may select one of the three of** the legally specified circumstances
  justifying withholding…" — garbled, and the numbered list "1. … 2. … 3." that carried the
  three grounds has been flattened into prose separated by "or".
- How to complete gained a sentence: "**You may select at least one of the three options.**"
  Together with the Meaning's "one of the three", the page now says both *one* and *at least
  one*. The three grounds themselves are unchanged (third subparagraph of Art. 16(2) CRA).

**Four new defects, all reproduced verbatim in the tables below:**

| Field | Defect |
|---|---|
| v26 | "(max. 255 characters).**.**" — doubled full stop |
| v29 | "CSIRT Designated as Coordinator (CDaC)**taking** their decision" — missing space |
| i36 | "the manufacturer or another relevant **become aware**" — was "another relevant party became aware" |
| i37 | "the date and time when the incident **was began** or occurred" |

**Field 11 "End of support indicator" is unchanged, including both of its problems**: the
Meaning still describes whether the product has a user interface for informing users, while
How to complete / Example / Format still ask a Yes/No question about whether the support
period has ended; and the typo "or No when is doesn't" is still there. Two edit passes have
now gone over this page without touching it.

Also unchanged: the two footnotes, and i32's "Applied or ongoing mitigation measures" against
the FAQ's "Applied and ongoing" — the and/or discrepancy between the two ENISA sources stands.

### 2026-09-07 (evening) — page moved, content unchanged at the time of the move

The Glossary moved from `.../cra-srp-glossary` to `.../cra-srp-glossary2`. The old
path returns HTTP 403; the new one returns 200 with Version 1.1 and the same
05/09/2026 date. Compared field by field against this baseline: **38 fields, identical
numbering, no name changed** — including field 11, whose stated meaning still
contradicts its own completion instructions, and the "when is doesn't" typo in that
same row.

This corrects the diagnosis recorded on 2026-09-07. A 403 on a single page while its
neighbours stay up reads like an unpublication, and that is how it was written down.
It was a move. The lesson is in the frontmatter: check where a page went before
concluding it is gone.


### 2026-09-07 — rebuilt as maintained tables; fixed invalid YAML frontmatter
This file's first commit (same day) used one prose block per field. Two issues found and fixed
in this pass, both introduced in that first commit:
- **Invalid YAML frontmatter**: `page_version: 1.1, last update per page footer: 05/09/2026`
  contained an unquoted `: ` (colon-space) inside a plain scalar value, which GitHub's YAML
  frontmatter renderer (and any strict parser, confirmed with PyYAML) rejects outright —
  "mapping values are not allowed in this context". Fixed by quoting the value.
- **Rebuilt as tables** (this request): content converted from prose blocks to the three
  markdown tables below, at the user's request, so the file is easier to scan and — going
  forward — easier to maintain as a straight per-row diff against the live page's own table.

### 2026-09-07 — initial capture
First full-detail capture of this page. It was discovered via the ENISA SRP FAQ baseline-check
routine's 2026-09-07 run (the FAQ page overhaul that day added links to a previously-untracked
"CRA SRP Glossary" page and a "List of CSIRTs Designated as Coordinators" page). The Glossary was
fetched as raw HTML at 05:06 UTC and captured here in full; `enisa-srp-faq-baseline.md` from the
same run only holds a compact field-name/status summary of it, trimmed for size.

Hours later the same day, a re-check found the live Glossary page returning HTTP 403 (see
`status` in the frontmatter) while every other tracked SRP page remained reachable. This file was
written from the 05:06 UTC capture — i.e. from the last known-good fetch — since the page could
not be re-fetched at write time.

Field counts at capture: 18 common fields (numbered 1–18), 11 Actively Exploited Vulnerability
(AEV) fields (v19–v29), 9 Severe Incident (SI) fields (i30–i38) — 38 fields total. Note this
numbering is the Glossary's own and differs from the FAQ's Q16 table, which additionally
itemizes 5 automated/system common fields (Notification level, the three Reporting-time fields,
Reporter) that the Glossary does not number explicitly; see `enisa-srp-faq-baseline.md` for that
cross-reference.

## Page metadata

- Version: 1.1
- Page's own "last update" footer: 05/09/2026
- Columns on the live page, per field: Nr. | Field | Applies to AEV or SI | What this field means | How you may complete it | Example | Expected format | Early Warning (EW) 24h | 72h | Final Report (FR)

## Common fields (Both AEV and SI)

| Nr. | Field | Applies to | Meaning | How to complete | Example | Format | EW 24h | 72h | Final Report |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Notification type (Vulnerability/Incident) | Both | Indicates whether the notification concerns an actively exploited vulnerability (AEV) or a severe incident (SI) having an impact on the security of a product with digital elements. | Select Actively Exploited Vulnerability when reporting an AEV. Select Severe Incident when reporting a SI having an impact on the security of a product with digital elements. | Vulnerability | Select one: Vulnerability or Incident | Required | copied-or-updated | copied-or-updated |
| 2 | Title | Both | Short human-readable name for the notification. | For example, enter a short, specific title that allows users to recognise the affected product and the reported issue. Do not include confidential technical detail that is unnecessary for identification (max. 255 characters). | Active exploitation affecting Product X version 4.2. | Plain text; concise title | Required | copied-or-updated | copied-or-updated |
| 3 | Summary | Both | Concise overview of the facts, affected product, and issue being notified. | For example, provide a concise overview of what happened, the affected product or version, the known impact, and the current mitigation status. Use factual information available at the reporting stage (max. 4000 characters). | An actively exploited vulnerability affects Product X 4.2. A temporary workaround is available, and a security update is being prepared. | Short paragraph | Required | copied-or-updated | copied-or-updated |
| 4 | Manufacturer name | Both | Name of the natural or legal person who develops or manufactures the product with digital elements or has the product with digital elements designed, developed or manufactured, and markets it under its name or trademark, whether for payment, monetisation or free of charge. | No user action is required. The platform creates or updates this value automatically based on what you wrote when you registered to the Platform or added at a later stage. You may review it only to confirm that the displayed information is consistent with the notification history. | Automatically populated by the platform during the notification submission or free text during manufacturer registration [Name of the company]. | System-generated / read-only | Required | copied-or-updated | copied-or-updated |
| 5 | Member States where product available (Concerned CSIRT) | Both | Member States in which territory the manufacturer is aware that the affected product has been made available; used to determine concerned CSIRTs. | The Platform will automatically show you CDaC, however, you may select other Member States (MS) where the affected product has been made available, based on the information currently known to the manufacturer. Update the selection if new distribution information becomes available. | Belgium as your CDaC, automatically populated by the platform and you may add Greece and Italy and MS where the affected product has been made available | Select one or more Member States | Required if such information available | copied-or-updated | copied-or-updated |
| 6 | Product Name | Both | Name that identifies the affected product with digital elements. | For example, enter the official commercial or technical name of the affected product with digital elements. Use the same name that appears in product technical documentation or market information (max. 255 characters). | Product X | Official product name | Required | copied-or-updated | copied-or-updated |
| 7 | Product version | Both | Version, release, build, model, or other revision information required to identify the affected product instance. | For example, enter every affected version, release, build, model, or firmware revision. Use exact identifiers and clearly state a range when multiple versions are affected (max. 255 characters). | 4.0 to 4.2.1 | Version or version range | Required | copied-or-updated | copied-or-updated |
| 8 | Product Type (Default/Important/Critical) | Both | Regulatory category indicating whether the product is default, important, or critical under the CRA classification framework. | For example, select the CRA regulatory type applicable to the product. Choose Important or Critical only where the product falls within the relevant CRA category (Annexes III and IV); otherwise select Default. | Important | Select one: Default, Important, Critical | Optional | copied-or-updated | copied-or-updated |
| 9 | Product Class | Both | For an important product, the applicable Class I or Class II category used for conformity-assessment treatment. | For example, for an important product, select the applicable CRA class. Leave the field empty when the product is not classified as an important product or when no class applies. | Class II | Select one configured class | Optional | copied-or-updated | copied-or-updated |
| 10 | Product Category | Both | The applicable CRA product category, normally selected from the relevant category list in CRA Annexes III or IV. | You may select the category that best matches the affected product under the applicable CRA category list. Use the product’s core functionality, not only its commercial name. | Choose between: Hardware devices with Security Boxes; Smart meter gateways within smart metering systems and other devices for advanced security purposes, including secure cryptoprocessing devices; or Smartcards or similar devices, including secure elements. | Select one configured category | Optional | copied-or-updated | copied-or-updated |
| 11 | End of support indicator | Both | Indicates whether the product with digital elements has a user interface or similar technical means allowing direct interaction with its users and the manufacturer should make use of such features to inform users that their product with digital elements has reached the end of the support period. | You may select one: Yes when the product with digital elements has reached the end of the support period or No when is doesn’t. *(typo on the live page, reproduced verbatim; and note that this row's Meaning describes a different concept — see the change log)* | Yes | Select one: Yes or No | Optional | copied-or-updated | copied-or-updated |
| 12 | Component name | Both | Name of the software or hardware component in which the vulnerability or incident is located or observed. | For example, enter the name of the affected hardware or software component. You may include the component version when known. Leave empty if the issue cannot be attributed to a component (max. 255 characters). | Authentication module 3.1 | Component name and optional version | Optional | copied-or-updated | copied-or-updated |
| 13 | Mitigating measure expected shortly | Both | Indicates whether an effective risk-mitigation measure, such as a security update or user guidance, is expected to become available. | For example, select Yes only when an effective security update, workaround, or user guidance is expected shortly and the expectation is supported by the remediation plan. Otherwise select No or Unknown. | Yes | Select one: Yes, No, Unknown | Optional | copied-or-updated | copied-or-updated |
| 14 | User Action able to reduce impact | Both | Action that product users can take to prevent, reduce, or contain the impact of the vulnerability or incident. | You may describe the immediate action a user can take to reduce the likelihood or impact of exploitation or the incident. Provide clear, practical instructions and identify any limitation or prerequisite (max. 4000 characters). | Disable the affected interface until the security update is installed. | Action-oriented text | Optional | copied-or-updated | copied-or-updated |
| 15 | Considered sensitivity of information | Both | Manufacturer's assessment of how sensitive the notified information is, to inform secure handling and dissemination decisions. | You may describe why any submitted information requires restricted handling. Identify the sensitive element and the potential consequence of premature or wider disclosure. Do not use a generic confidentiality statement (max. 255 characters). | The technical details reveal an unpatched exploitation path that is not yet publicly known. | Concise justification | Optional | Required if such information available | copied-or-updated |
| 16 | Corrective or mitigating measures taken | Both | Actions already implemented by the manufacturer or other responsible party to correct the issue or reduce its risk or impact. | For example, list the actions already taken to correct the issue or to reduce the risk. You may include containment, configuration changes, update withdrawal, credential rotation, monitoring, or other completed measures, with dates where useful. (max. 2000 characters). | Disabled the affected service; revoked exposed credentials; increased monitoring. | Bulleted list or structured text | Optional | Required | Required |
| 17 | Corrective or mitigating measures users can take | Both | Instructions or actions users can apply to reduce exposure or impact, including workarounds, configuration changes, patches, or isolation measures. | For example, provide step-oriented guidance that users can apply. Prioritise the effective fix, then state temporary workarounds and any operational impact. Clearly identify actions that are no longer recommended (max. 4000 characters). | Install version 4.2.2. Until installation, restrict management-interface access to trusted networks. | Action-oriented text | Optional | Required | Required |
| 18 | Attack vector | Both | Description or structured classification of the path or means by which exploitation or compromise can occur. | For example, describe how the vulnerability may be exploited or how the incident reached the affected product. State the relevant interface, access path, protocol, or user interaction. Avoid unsupported assumptions (max. 255 characters). | Remote network access through an exposed API. | Short, structured description or configured classification | Optional | Optional | Optional |

## Actively Exploited Vulnerability (AEV) fields

| Nr. | Field | Applies to | Meaning | How to complete | Example | Format | EW 24h | 72h | Final Report |
|---|---|---|---|---|---|---|---|---|---|
| v19 | CVE ID | AEV | CVE Identifier (CVE ID) assigned to the publicly disclosed vulnerability under the Common Vulnerabilities and Exposures (CVE) Program. | You may enter the official CVE ID only if one has been assigned by the competent CNA. Copy the ID exactly as published. Leave the field empty if no ID exists (max. 255 characters). | CVE-2026-12345 | CVE identifier | Optional | copied-or-updated | copied-or-updated |
| v20 | EUVD ID | AEV | Identifier of the vulnerability record in the European Vulnerability Database (EUVD). | You may enter the official EUVD ID if one has been assigned by ENISA. Copy the ID exactly as published. Leave the field empty if no ID exists (max. 255 characters). | EUVD-2026-12345 | EUVD identifier | Optional | copied-or-updated | copied-or-updated |
| v21 | General information | AEV | High-level description of the vulnerability and, where known, how exploitation works, without requiring the full final technical analysis. | For example, describe the vulnerability at a high level and explain how the known exploit operates. Include the affected function, required access, and observed exploitation behaviour. Do not include unverified attribution (max. 4000 characters). | An authentication bypass in the management interface allows a remote actor with network access to execute privileged actions. | Structured narrative | Optional | Required | copied-or-updated |
| v22 | Date when corrective or mitigating measure has been available | AEV | Date and time when the mitigating measure has been available. | For example, enter the date and time when the mitigating measure has been available. | 2026-09-02 09:15 UTC | Date and time | Optional | Optional | Required |
| v23 | Full description of the severity of the vulnerability | AEV | Complete description of the vulnerability, including at least its severity. | For example, provide the completed technical description of the vulnerability. Including the assessed severity rating, classification, rationale for the assessment and other relevant factors or criteria supporting the assigned severity level (max. 4000 characters). | Authentication validation is missing in endpoint X... Severity: High... Affected versions: 4.0–4.2.1... | Detailed structured narrative | Optional | Optional | Required |
| v24 | Full description of the impact of the vulnerability | AEV | Complete description of the vulnerability, including at least its impact. | For example, provide the completed technical description of the vulnerability. Including the potential or actual impact of the vulnerability, the affected systems, components, data, users or services, as applicable (max. 4000 characters). | Authentication validation is missing in endpoint X... Impact: High... Affected versions: 4.0–4.2.1... | Detailed structured narrative | Optional | Optional | Required |
| v25 | Date/time when you become aware of the Actively Exploited Vulnerability [1] | AEV | Date and time when the manufacturer or another relevant party first detected the vulnerability. | For example, enter the date and time when the vulnerability was first detected. If the exact time is unknown, enter the best supported estimate and identify it as estimated in the vulnerability description. | 2026-08-24 09:15 UTC | Date and time | Required | copied-or-updated | copied-or-updated |
| v26 | Malicious actor that has exploited/is exploiting the vulnerability | AEV | Available information about the actor that exploited or is exploiting the vulnerability, without requiring attribution where information is unavailable. | You may enter confirmed information about the malicious actor or observed activity. If attribution is unconfirmed, describe the observed indicators and state that attribution is unknown (max. 100 characters).. | Unknown actor; observed infrastructure includes the indicators listed in Reference REF-2026-18. | Free text | Optional | Optional | Required if such information available |
| v27 | Particular Exceptional Circumstances (PEC) | AEV | Selection indicating that one or more legally specified circumstances in the third subparagraph of Article 16 (2) of CRA justify withholding the full 72-hour AEV notification from simultaneous access by ENISA and/or delaying wider dissemination. | You may select the applicable exceptional circumstance only when the corresponding legal condition is met. | — | Select applicable PEC option(s) | N/A | Optional | N/A |
| v28 | PEC Delay Reason | AEV | You may select one of the three of the legally specified circumstances justifying withholding the full 72-hour AEV notification from simultaneous access by ENISA and/or delaying wider dissemination. | Support the selection with specific facts in PEC Delay Reason and indicate the requested dissemination delay. You may select at least one of the three options. | You may choose: the notified vulnerability has been actively exploited by a malicious actor and, according to the information available, it has been exploited in no other Member State than the one of the CSIRT designated as coordinator to which the manufacturer has notified the vulnerability; or<br>N/A<br>that any immediate further dissemination of the notified vulnerability would likely result in the supply of information the disclosure of which would be contrary to the essential interests of that Member State; or | Select applicable check box | N/A | Optional | N/A |
| v29 | Please provide further information | AEV | Description of anything that should be helpful for CSIRT Designated as Coordinator (CDaC)taking *(missing space on the live page, new on 2026-09-07)* their decision. | You may provide additional information(s). | We consider it very important for national security. | Free text | Optional | Optional | copied-or-updated |

## Severe Incident (SI) fields

| Nr. | Field | Applies to | Meaning | How to complete | Example | Format | EW 24h | 72h | Final Report |
|---|---|---|---|---|---|---|---|---|---|
| i30 | Incident is suspected of unlawful or malicious acts | SI | Boolean indication of whether available evidence suggests the incident resulted from unlawful or malicious activity. | For example, select Yes when available evidence indicates intentional unlawful or malicious activity. Select No when the event is assessed as non-malicious. Select Unknown while the cause remains unresolved. | Yes | Select one: Yes, No, Unknown | Required | copied-or-updated | copied-or-updated |
| i31 | General information about nature of incident | SI | High-level account of what happened, how the incident manifested, and the affected security properties or functions. | For example, describe what occurred, the affected product functions or security properties, and the currently known scope. Focus on confirmed facts available at the 72-hour stage (max. 4000 characters). | Malicious code executed through the update service and affected the integrity of locally stored configuration data. | Structured narrative | Optional | Required | copied-or-updated |
| i32 | Applied or ongoing mitigation measures | SI | Actions that have been taken by the manufacturer or other responsible party or are still ongoing to correct the issue or reduce its risk or impact. | For example, list the actions already applied or ongoing to correct the issue or reduce risk. Include containment, configuration changes, update withdrawal, credential rotation, monitoring, or other completed measures, with dates where useful (max. 4000 characters). | Disabled the affected service; revoked exposed credentials; increased monitoring. | Structured narrative | Optional | Optional | Required |
| i33 | Detailed description of the Severity of the incident | SI | Complete the detailed description of the severity of the incident. | For example, provide the completed description of the severity of the incident. Include the sequence of events, affected products and functions, severity, scope, evidence, root cause, response measures, and recovery status (max. 4000 characters). | Low – limited impact, no significant disruption to operation. | Structured narrative | Optional | Optional | Required |
| i34 | Detailed description of the Impact of the incident | SI | Complete the detailed description of the impact of the incident. | For example, provide the completed description of the impact of the incident, including the impact on the product, data, functions, users, or connected systems (max. 4000 characters). | Minimal – no material impact of operations, users or data. | Structured narrative | Optional | Optional | Required |
| i35 | Type of Threat or root cause likely to have triggered incident | SI | Most likely threat category, initiating event, weakness, failure, or root cause that triggered the incident. | For example, state the most likely threat type and root cause supported by the investigation. Explain the evidence briefly and mark the conclusion as preliminary when analysis is incomplete (max. 255 characters). | Supply-chain compromise caused by an unauthorised modification to the update package. | Classification plus short explanation | Optional | Optional | Required |
| i36 | Date/time when you become aware of the incident [2] | SI | Date and time when the manufacturer or another relevant become aware of the incident. *(broken grammar on the live page, new on 2026-09-07; was "another relevant party became aware")* | For example, enter the date and time you become aware of the incident. If the exact time is unknown, enter the best supported estimate and identify it as estimated in the incident description. | 2026-08-24 09:15 UTC | Date and time | Required | copied-or-updated | copied-or-updated |
| i37 | Date/time incident occurred | SI | Known or estimated date and time when the incident began or took place. | For example, enter the date and time when the incident was began or occurred. *(broken grammar on the live page, new on 2026-09-07; was "when the incident began or occurred")* If the exact time is unknown, enter the best supported estimate and identify it as estimated in the incident description. | 2026-08-24 09:15 UTC | Date and time | Optional | Optional | Optional |
| i38 | Initial assessment of the incident | SI | Preliminary analysis of the incident's severity, scope, likely impact, affected functions or data, and immediate implications. | For example, provide the preliminary assessment of severity, scope, affected security properties, products or users, and likely impact. Clearly distinguish confirmed findings from matters still under investigation (max. 4000 characters). | Confirmed impact is limited to integrity of configuration data on three product instances; broader exposure remains under investigation. | Structured narrative | Optional | Required | copied-or-updated |

## Footnotes (from the live page)

- [1] This field will be available in the next release of the Platform. (attached to field v25)
- [2] In the current release this field is named: "Date/time the incident was detected". (attached to field i36)

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
