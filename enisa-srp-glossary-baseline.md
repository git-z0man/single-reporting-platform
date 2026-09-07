---
source: ENISA — CRA SRP Glossary
url: https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary
page_version: 1.1, last update per page footer: 05/09/2026
retrieved: 2026-09-07 (fetched 05:06 UTC)
purpose: Full-detail baseline of the CRA SRP Glossary page — the authoritative field-by-field
  reference for the SRP reporting template (meaning, how to complete, example, expected format,
  and per-stage status for every field). The compact field-name/status table cross-referenced
  from `enisa-srp-faq-baseline.md` (Q16 and the "CRA SRP Glossary" section there) is a trimmed
  summary of this file; this file is the one to diff against for wording-level changes to any
  field's description, example, or format, and is the historical record now that the live page
  is not reliably available (see status below).
status: >-
  Live page returned HTTP 403 as of the 2026-09-07 15:56 UTC re-check, a few hours after this
  content was captured. At the same check, the main SRP page, the FAQ page, the CSIRT-list page,
  and all three guidance subpages were still HTTP 200 — so this looks specific to the Glossary
  page (ENISA editing or temporarily unpublishing it) rather than a site-wide outage. Re-verify
  on every future check; update this line with whatever is found.
last_check: 2026-09-07
last_change: 2026-09-07
note: One block per field, grouped Common / AEV / SI as on the live page, to keep diffs readable.
  Update `retrieved`, `page_version`, `status`, and field content whenever a change or a
  reachability transition (403 <-> 200, or a genuinely new page version) is confirmed.
---

# CRA SRP Glossary — full-detail baseline

## Change log (2026-09-07 initial capture)

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

## Common fields

### 1. Notification type (Vulnerability/Incident)
Applies to: Both
- Meaning: Indicates whether the notification concerns an actively exploited vulnerability (AEV) or a severe incident (SI) having an impact on the security of a product with digital elements.
- How to complete: Select Actively Exploited Vulnerability when reporting an AEV. Select Severe Incident when reporting a SI having an impact on the security of a product with digital elements.
- Example: Vulnerability
- Format: Select one: Vulnerability or Incident
- Status (EW / 72h / FR): Required / copied-or-updated / copied-or-updated

### 2. Title
Applies to: Both
- Meaning: Short human-readable name for the notification.
- How to complete: Enter a short, specific title that allows users to recognise the affected product and the reported issue. Do not include confidential technical detail that is unnecessary for identification (max. 255 characters).
- Example: Active exploitation affecting Product X version 4.2.
- Format: Plain text; concise title
- Status: Required / copied-or-updated / copied-or-updated

### 3. Summary
Applies to: Both
- Meaning: Concise overview of the facts, affected product, and issue being notified.
- How to complete: Provide a concise overview of what happened, the affected product or version, the known impact, and the current mitigation status. Use factual information available at the reporting stage (max. 4000 characters).
- Example: An actively exploited vulnerability affects Product X 4.2. A temporary workaround is available, and a security update is being prepared.
- Format: Short paragraph
- Status: Required / copied-or-updated / copied-or-updated

### 4. Manufacturer name
Applies to: Both
- Meaning: Name of the natural or legal person who develops or manufactures the product with digital elements or has the product with digital elements designed, developed or manufactured, and markets it under its name or trademark, whether for payment, monetisation or free of charge.
- How to complete: No user action is required. The platform creates or updates this value automatically based on what you wrote when you registered to the Platform or added at a later stage. You may review it only to confirm that the displayed information is consistent with the notification history.
- Example: Automatically populated by the platform during the notification submission or free text during manufacturer registration [Name of the company].
- Format: System-generated / read-only
- Status: Required / copied-or-updated / copied-or-updated

### 5. Member States where product available (Concerned CSIRT)
Applies to: Both
- Meaning: Member States in which territory the manufacturer is aware that the affected product has been made available; used to determine concerned CSIRTs.
- How to complete: The Platform will automatically show you CDaC, however, you may select other Member States (MS) where the affected product has been made available, based on the information currently known to the manufacturer. Update the selection if new distribution information becomes available.
- Example: Belgium as your CDaC, automatically populated by the platform and you may add Greece and Italy and MS where the affected product has been made available
- Format: Select one or more Member States
- Status: Required if such information available / copied-or-updated / copied-or-updated

### 6. Product Name
Applies to: Both
- Meaning: Name that identifies the affected product with digital elements.
- How to complete: Enter the official commercial or technical name of the affected product with digital elements. Use the same name that appears in product technical documentation or market information (max. 255 characters).
- Example: Product X
- Format: Official product name
- Status: Required / copied-or-updated / copied-or-updated

### 7. Product version
Applies to: Both
- Meaning: Version, release, build, model, or other revision information required to identify the affected product instance.
- How to complete: Enter every affected version, release, build, model, or firmware revision. Use exact identifiers and clearly state a range when multiple versions are affected (max. 255 characters).
- Example: 4.0 to 4.2.1
- Format: Version or version range
- Status: Required / copied-or-updated / copied-or-updated

### 8. Product Type (Default/Important/Critical)
Applies to: Both
- Meaning: Regulatory category indicating whether the product is default, important, or critical under the CRA classification framework.
- How to complete: Select the CRA regulatory type applicable to the product. Choose Important or Critical only where the product falls within the relevant CRA category (Annexes III and IV); otherwise select Default.
- Example: Important
- Format: Select one: Default, Important, Critical
- Status: Optional / copied-or-updated / copied-or-updated

### 9. Product Class
Applies to: Both
- Meaning: For an important product, the applicable Class I or Class II category used for conformity-assessment treatment.
- How to complete: For an important product, select the applicable CRA class. Leave the field empty when the product is not classified as an important product or when no class applies.
- Example: Class II
- Format: Select one configured class
- Status: Optional / copied-or-updated / copied-or-updated

### 10. Product Category
Applies to: Both
- Meaning: The applicable CRA product category, normally selected from the relevant category list in CRA Annexes III or IV.
- How to complete: You may select the category that best matches the affected product under the applicable CRA category list. Use the product's core functionality, not only its commercial name.
- Example: Choose between: Hardware devices with Security Boxes; Smart meter gateways within smart metering systems and other devices for advanced security purposes, including secure cryptoprocessing devices; or Smartcards or similar devices, including secure elements.
- Format: Select one configured category
- Status: Optional / copied-or-updated / copied-or-updated

### 11. End of support indicator
Applies to: Both
- Meaning: Indicates whether the product with digital elements has a user interface or similar technical means allowing direct interaction with its users and the manufacturer should make use of such features to inform users that their product with digital elements has reached the end of the support period.
- How to complete: You may select one: Yes when the product with digital elements has reached the end of the support period or No when is doesn't. *("is doesn't" is a typo on the live page, reproduced verbatim.)*
- Example: Yes
- Format: Select one: Yes or No
- Status: Optional / copied-or-updated / copied-or-updated

### 12. Component name
Applies to: Both
- Meaning: Name of the software or hardware component in which the vulnerability or incident is located or observed.
- How to complete: Enter the name of the affected hardware or software component. You may include the component version when known. Leave empty if the issue cannot be attributed to a component (max. 255 characters).
- Example: Authentication module 3.1
- Format: Component name and optional version
- Status: Optional / copied-or-updated / copied-or-updated

### 13. Mitigating measure expected shortly
Applies to: Both
- Meaning: Indicates whether an effective risk-mitigation measure, such as a security update or user guidance, is expected to become available.
- How to complete: Select Yes only when an effective security update, workaround, or user guidance is expected shortly and the expectation is supported by the remediation plan. Otherwise select No or Unknown.
- Example: Yes
- Format: Select one: Yes, No, Unknown
- Status: Optional / copied-or-updated / copied-or-updated

### 14. User Action able to reduce impact
Applies to: Both
- Meaning: Action that product users can take to prevent, reduce, or contain the impact of the vulnerability or incident.
- How to complete: You may describe the immediate action a user can take to reduce the likelihood or impact of exploitation or the incident. Provide clear, practical instructions and identify any limitation or prerequisite (max. 4000 characters).
- Example: Disable the affected interface until the security update is installed.
- Format: Action-oriented text
- Status: Optional / copied-or-updated / copied-or-updated

### 15. Considered sensitivity of information
Applies to: Both
- Meaning: Manufacturer's assessment of how sensitive the notified information is, to inform secure handling and dissemination decisions.
- How to complete: You may describe why any submitted information requires restricted handling. Identify the sensitive element and the potential consequence of premature or wider disclosure. Do not use a generic confidentiality statement (max. 255 characters).
- Example: The technical details reveal an unpatched exploitation path that is not yet publicly known.
- Format: Concise justification
- Status: Optional / Required if such information available / copied-or-updated

### 16. Corrective or mitigating measures taken
Applies to: Both
- Meaning: Actions already implemented by the manufacturer or other responsible party to correct the issue or reduce its risk or impact.
- How to complete: List the actions already taken to correct the issue or to reduce the risk. You may include containment, configuration changes, update withdrawal, credential rotation, monitoring, or other completed measures, with dates where useful (max. 2000 characters).
- Example: Disabled the affected service; revoked exposed credentials; increased monitoring.
- Format: Bulleted list or structured text
- Status: Optional / Required / Required

### 17. Corrective or mitigating measures users can take
Applies to: Both
- Meaning: Instructions or actions users can apply to reduce exposure or impact, including workarounds, configuration changes, patches, or isolation measures.
- How to complete: Provide step-oriented guidance that users can apply. Prioritise the effective fix, then state temporary workarounds and any operational impact. Clearly identify actions that are no longer recommended (max. 4000 characters).
- Example: Install version 4.2.2. Until installation, restrict management-interface access to trusted networks.
- Format: Action-oriented text
- Status: Optional / Required / Required

### 18. Attack vector
Applies to: Both
- Meaning: Description or structured classification of the path or means by which exploitation or compromise can occur.
- How to complete: Describe how the vulnerability may be exploited or how the incident reached the affected product. State the relevant interface, access path, protocol, or user interaction. Avoid unsupported assumptions (max. 255 characters).
- Example: Remote network access through an exposed API.
- Format: Short, structured description or configured classification
- Status: Optional / Optional / Optional

## Actively Exploited Vulnerability (AEV) fields

### v19. CVE ID
Applies to: AEV
- Meaning: CVE Identifier (CVE ID) assigned to the publicly disclosed vulnerability under the Common Vulnerabilities and Exposures (CVE) Program.
- How to complete: You may enter the official CVE ID only if one has been assigned by the competent CNA. Copy the ID exactly as published. Leave the field empty if no ID exists (max. 255 characters).
- Example: CVE-2026-12345
- Format: CVE identifier
- Status: Optional / copied-or-updated / copied-or-updated

### v20. EUVD ID
Applies to: AEV
- Meaning: Identifier of the vulnerability record in the European Vulnerability Database (EUVD).
- How to complete: You may enter the official EUVD ID if one has been assigned by ENISA. Copy the ID exactly as published. Leave the field empty if no ID exists (max. 255 characters).
- Example: EUVD-2026-12345
- Format: EUVD identifier
- Status: Optional / copied-or-updated / copied-or-updated

### v21. General information
Applies to: AEV
- Meaning: High-level description of the vulnerability and, where known, how exploitation works, without requiring the full final technical analysis.
- How to complete: Describe the vulnerability at a high level and explain how the known exploit operates. Include the affected function, required access, and observed exploitation behaviour. Do not include unverified attribution (max. 4000 characters).
- Example: An authentication bypass in the management interface allows a remote actor with network access to execute privileged actions.
- Format: Structured narrative
- Status: Optional / Required / copied-or-updated

### v22. Date when corrective or mitigating measure has been available
Applies to: AEV
- Meaning: Date and time when the mitigating measure has been available.
- How to complete: Enter the date and time when the mitigating measure has been available.
- Example: 2026-09-02 09:15 UTC
- Format: Date and time
- Status: Optional / Optional / Required

### v23. Full description of the severity of the vulnerability
Applies to: AEV
- Meaning: Complete description of the vulnerability, including at least its severity.
- How to complete: Provide the completed technical description of the vulnerability, including the assessed severity rating, classification, rationale for the assessment and other relevant factors or criteria supporting the assigned severity level (max. 4000 characters).
- Example: Authentication validation is missing in endpoint X... Severity: High... Affected versions: 4.0–4.2.1...
- Format: Detailed structured narrative
- Status: Optional / Optional / Required

### v24. Full description of the impact of the vulnerability
Applies to: AEV
- Meaning: Complete description of the vulnerability, including at least its impact.
- How to complete: Provide the completed technical description of the vulnerability, including the potential or actual impact of the vulnerability, the affected systems, components, data, users or services, as applicable (max. 4000 characters).
- Example: Authentication validation is missing in endpoint X... Impact: High... Affected versions: 4.0–4.2.1...
- Format: Detailed structured narrative
- Status: Optional / Optional / Required

### v25. Date/time when you become aware of the Actively Exploited Vulnerability [1]
Applies to: AEV
- Meaning: Date and time when the manufacturer or another relevant party first detected the vulnerability.
- How to complete: Enter the date and time when the vulnerability was first detected. If the exact time is unknown, enter the best supported estimate and identify it as estimated in the vulnerability description.
- Example: 2026-08-24 09:15 UTC
- Format: Date and time
- Status: Required / copied-or-updated / copied-or-updated

### v26. Malicious actor that has exploited/is exploiting the vulnerability
Applies to: AEV
- Meaning: Available information about the actor that exploited or is exploiting the vulnerability, without requiring attribution where information is unavailable.
- How to complete: You may enter confirmed information about the malicious actor or observed activity. If attribution is unconfirmed, describe the observed indicators and state that attribution is unknown (max. 100 characters).
- Example: Unknown actor; observed infrastructure includes the indicators listed in Reference REF-2026-18.
- Format: Free text
- Status: Optional / Optional / Required if such information available

### v27. Particular Exceptional Circumstances (PEC)
Applies to: AEV
- Meaning: Selection indicating that one or more legally specified circumstances in the third subparagraph of Article 16(2) of CRA justify withholding the full 72-hour AEV notification from simultaneous access by ENISA and/or delaying wider dissemination.
- How to complete: You may select the applicable exceptional circumstance only when the corresponding legal condition is met.
- Format: Select applicable PEC option(s)
- Status (EW / 72h / FR): N/A / Optional / N/A

### v28. PEC Delay Reason
Applies to: AEV
- Meaning / how to complete: You may select one of the three legally specified circumstances justifying withholding the full 72-hour AEV notification from simultaneous access by ENISA and/or delaying wider dissemination. Support the selection with specific facts in PEC Delay Reason and indicate the requested dissemination delay. You may select at least one of the three options:
  - the notified vulnerability has been actively exploited by a malicious actor and, according to the information available, it has been exploited in no other Member State than the one of the CSIRT designated as coordinator to which the manufacturer has notified the vulnerability; or
  - that any immediate further dissemination of the notified vulnerability would likely result in the supply of information the disclosure of which would be contrary to the essential interests of that Member State; or
  - that the notified vulnerability poses an imminent high cybersecurity risk stemming from the further dissemination.
- Format: Select applicable check box
- Status (EW / 72h / FR): N/A / Optional / N/A

### v29. Please provide further information
Applies to: AEV
- Meaning: Description of anything that should be helpful for CSIRT Designated as Coordinator (CDaC) taking their decision.
- How to complete: You may provide additional information(s).
- Example: We consider it very important for national security.
- Format: Free text
- Status: Optional / Optional / copied-or-updated

## Severe Incident (SI) fields

### i30. Incident is suspected of unlawful or malicious acts
Applies to: SI
- Meaning: Boolean indication of whether available evidence suggests the incident resulted from unlawful or malicious activity.
- How to complete: Select Yes when available evidence indicates intentional unlawful or malicious activity. Select No when the event is assessed as non-malicious. Select Unknown while the cause remains unresolved.
- Example: Yes
- Format: Select one: Yes, No, Unknown
- Status: Required / copied-or-updated / copied-or-updated

### i31. General information about nature of incident
Applies to: SI
- Meaning: High-level account of what happened, how the incident manifested, and the affected security properties or functions.
- How to complete: Describe what occurred, the affected product functions or security properties, and the currently known scope. Focus on confirmed facts available at the 72-hour stage (max. 4000 characters).
- Example: Malicious code executed through the update service and affected the integrity of locally stored configuration data.
- Format: Structured narrative
- Status: Optional / Required / copied-or-updated

### i32. Applied or ongoing mitigation measures
Applies to: SI
- Meaning: Actions that have been taken by the manufacturer or other responsible party or are still ongoing to correct the issue or reduce its risk or impact.
- How to complete: List the actions already applied or ongoing to correct the issue or reduce risk. Include containment, configuration changes, update withdrawal, credential rotation, monitoring, or other completed measures, with dates where useful (max. 4000 characters).
- Example: Disabled the affected service; revoked exposed credentials; increased monitoring.
- Format: Structured narrative
- Status: Optional / Optional / Required

### i33. Detailed description of the Severity of the incident
Applies to: SI
- Meaning: Complete the detailed description of the severity of the incident.
- How to complete: Provide the completed description of the severity of the incident. Include the sequence of events, affected products and functions, severity, scope, evidence, root cause, response measures, and recovery status (max. 4000 characters).
- Example: Low – limited impact, no significant disruption to operation.
- Format: Structured narrative
- Status: Optional / Optional / Required

### i34. Detailed description of the Impact of the incident
Applies to: SI
- Meaning: Complete the detailed description of the impact of the incident.
- How to complete: Provide the completed description of the impact of the incident, including the impact on the product, data, functions, users, or connected systems (max. 4000 characters).
- Example: Minimal – no material impact of operations, users or data.
- Format: Structured narrative
- Status: Optional / Optional / Required

### i35. Type of Threat or root cause likely to have triggered incident
Applies to: SI
- Meaning: Most likely threat category, initiating event, weakness, failure, or root cause that triggered the incident.
- How to complete: State the most likely threat type and root cause supported by the investigation. Explain the evidence briefly and mark the conclusion as preliminary when analysis is incomplete (max. 255 characters).
- Example: Supply-chain compromise caused by an unauthorised modification to the update package.
- Format: Classification plus short explanation
- Status: Optional / Optional / Required

### i36. Date/time when you become aware of the incident [2]
Applies to: SI
- Meaning: Date and time when the manufacturer or another relevant party became aware of the incident.
- How to complete: Enter the date and time you become aware of the incident. If the exact time is unknown, enter the best supported estimate and identify it as estimated in the incident description.
- Example: 2026-08-24 09:15 UTC
- Format: Date and time
- Status: Required / copied-or-updated / copied-or-updated

### i37. Date/time incident occurred
Applies to: SI
- Meaning: Known or estimated date and time when the incident began or took place.
- How to complete: Enter the date and time when the incident began or occurred. If the exact time is unknown, enter the best supported estimate and identify it as estimated in the incident description.
- Example: 2026-08-24 09:15 UTC
- Format: Date and time
- Status: Optional / Optional / Optional

### i38. Initial assessment of the incident
Applies to: SI
- Meaning: Preliminary analysis of the incident's severity, scope, likely impact, affected functions or data, and immediate implications.
- How to complete: Provide the preliminary assessment of severity, scope, affected security properties, products or users, and likely impact. Clearly distinguish confirmed findings from matters still under investigation (max. 4000 characters).
- Example: Confirmed impact is limited to integrity of configuration data on three product instances; broader exposure remains under investigation.
- Format: Structured narrative
- Status: Optional / Required / copied-or-updated

## Footnotes (from the live page)

- [1] This field will be available in the next release of the Platform. (attached to field v25)
- [2] In the current release this field is named: "Date/time the incident was detected". (attached to field i36)

## Check log

- 2026-09-07: Initial capture. Fetched raw HTML of the Glossary page at 05:06 UTC (as part of the
  ENISA SRP FAQ baseline-check routine's run that day, which discovered the page via updated site
  navigation) and recorded full field-by-field content here for the first time. A later same-day
  re-check (15:56 UTC) found the live page returning HTTP 403 while the rest of the tracked SRP
  pages remained reachable; this file reflects the 05:06 UTC capture, the last known-good state.
  The next check should first confirm whether the page is back (200) or still down (403/other),
  update `status` in the frontmatter accordingly, and — if reachable — diff the live content
  against the 38 fields captured here.
