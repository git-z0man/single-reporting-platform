---
source: ENISA — Single Reporting Platform (SRP)
url: https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp
old_url: https://www.enisa.europa.eu/topics/product-security-and-certification/single-reporting-platform-srp (now redirects to `url` above, first seen 2026-08-31)
faq_url: https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/frequently-asked-questions
retrieved: 2026-08-31
purpose: Baseline snapshot for change detection. Future runs diff the live page(s) against this file.
note: One logical block per FAQ entry to keep diffs readable. Update `retrieved` and content when a change is confirmed.
last_check: 2026-08-31
last_change: 2026-08-31
---

# ENISA Single Reporting Platform (SRP) — FAQ Baseline

## Change log (2026-08-31 check, vs. 2026-08-24 baseline)

No questions added, deleted, or reordered — still Q1–Q23. Three questions had their answer text changed (Q1, Q6, Q17); everything else (intro, Q2–Q5, Q7–Q16 incl. the data-field table, Q18–Q23, guidance documents, factsheet) verified unchanged via raw-HTML word-for-word diff.

- **Main page URL changed**: the main SRP page's canonical URL moved from `.../topics/product-security-and-certification/single-reporting-platform-srp` to `.../topics/product-security/single-reporting-platform-srp` (now recorded as `url` above; old URL kept as `old_url` since it still resolves via a redirect). This aligns the main page's URL with the FAQ subpage's URL, which already used the `product-security` (not `product-security-and-certification`) path segment. Breadcrumb now reads Topics → Product Security → Single Reporting Platform (SRP).
- **Q1 answer reworded**: substance unchanged, but restructured into two shorter paragraphs and shifted from future tense ("CRA SRP will be...") to present tense ("The CRA SRP is an online tool..."). No new facts, obligations, or figures.
- **Q6 answer changed**: the specific trigger date for voluntary-reporting functionality was removed — "This functionality will be enabled in the CRA SRP after 11 September 2026" is now "In the future, the platform will also offer functionality for voluntary reporting. This functionality will be enabled in the next phase of the CRA SRP." (no longer tied to a specific date).
- **Q17 answer changed**: "Other material, including short videos, will be published closer to the launch of the Platform." is now "Other material, including a PDF manual tutorial videos, will be published closer to the launch of the Platform." (adds a PDF manual to the planned material; likely a missing "and" on ENISA's side, reproduced verbatim here).
- Page-level "Updated: 03 August 2026" note is unchanged despite the above wording edits — ENISA did not bump the displayed update date for this pass.
- Minor cosmetic-only items, not treated as substantive: Q18 has a stray typo "Iist" for "list" (reproduced verbatim, not corrected); the Q16 data-field table's i22 row (the two "severity" sub-bullets under i21) is confirmed via raw HTML to be its own explicit table row with blank A/X/O values — same effective meaning as before, just more finely broken out in the markup.

## Change log (2026-08-24 check, vs. 2026-08-03 baseline)

Significant structural change: **the FAQ moved off the main SRP page onto its own dedicated subpage**, `.../single-reporting-platform-srp/frequently-asked-questions` (now recorded as `faq_url` above). The main SRP page now shows only a "Frequently asked questions" summary card with a "View all FAQs" link, not the full Q&A content inline. Bookmarks/anchors pointing at FAQ content on the old main-page URL no longer resolve to that content.

Other changes:

- **New guidance document added**: "CRA SRP - AR Interface functions" (Updated: 14/08/2026) — "explains the AR's interface of the SRP for various functions that can be performed." This is a third guidance document alongside the previous two.
- **Updated dates on the two existing guidance documents**: "CRA SRP - AR User registration" and "CRA SRP - AR Notification submission and update" both now show "Updated: 3/08/2026" (previously 31/07/2026). No means to verify their internal content changed, only the stated update date.
- **FAQ page now carries a single page-level "Updated: 03 August 2026" note** instead of the previous per-question "[Updated 31 July 2026]" tags on Q9, Q10, and Q17 (those tags have been removed; the questions themselves are otherwise unchanged in substance — see below).
- **Main-page intro paragraph reworded**: added a new lead sentence ("The Cyber Resilience Act (CRA) introduces the Single Reporting Platform (SRP) for cybersecurity incident reporting in the EU Digital Single Market."); the standalone closing line "Further information: Regulation (EU) 2024/2847 (EUR-Lex)" was removed and replaced with an inline hyperlink on "Cyber Resilience Act" within the body text (still linking to the same EUR-Lex regulation, eur-lex.europa.eu/eli/reg/2024/2847/oj/eng).
- **All 23 FAQ questions (Q1–Q23) received a light copyediting pass** during the move to the new subpage — minor wording, punctuation, and phrasing tweaks throughout (e.g. "must ensure" → "must also ensure", straight quotes → curly quotes, added clarifying phrases like "under the Cyber Resilience Act" in Q1 and "allowing for the manufacturer to identify the national CSIRT to report to" in Q18). No question was added, deleted, reordered, or renumbered, and none of these edits change any obligation, deadline, date, or scope — verified word-for-word against the 2026-08-03 baseline for substantive differences.
- **Q16 data-field table**: all 39 field entries (12 common + 14 vulnerability + 13 incident) and their X/C/A/O/I values verified identical to the 2026-08-03 baseline. Only cosmetic change: the legend order on the new page lists "A - automated..." first instead of "X - obligatory" first.
- Guidance-documents section on the main page ("User guidance") verified present with the same descriptive text pattern for each document, now covering three documents (see below).

## Intro

The Cyber Resilience Act (CRA) introduces the Single Reporting Platform (SRP) for cybersecurity incident reporting in the EU Digital Single Market.

The Single Reporting Platform (SRP) shall become a technical tool for the reporting of actively exploited vulnerabilities and incidents impacting products with digital elements in the EU Digital Single Market.

Under the [Cyber Resilience Act](https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng) (CRA), manufacturers of products with digital elements are mandated to report actively exploited vulnerabilities and severe incidents having an impact on the security of the products.

As of 11 September 2026 onwards, the SRP will be used by CSIRTs and manufacturers for mandatory reporting and could be used by any natural/legal persons for voluntary reporting.

Throughout 2025 and 2026, ENISA is taking the necessary steps to support the successful implementation of the platform.

Overall, the CRA brings transparency to the vulnerability disclosure processes and strengthens how EU CSIRTs can mitigate risks stemming from vulnerabilities.

### CRA Single Reporting Platform Factsheet

ENISA has published a factsheet on the CRA Single Reporting Platform. It can be downloaded here (https://www.enisa.europa.eu/media/57221), currently in English.

## FAQ entries

Source: dedicated FAQ subpage (see `faq_url` above). Page-level note: "Updated: 03 August 2026". Intro text on the FAQ page: "This is a collection of frequently asked questions on Cyber Resilience Act Single Reporting Platform (CRA SRP). Document is intended for publication on ENISA website and is updated regularly during the implementation of CRA SRP. Please note that the European Commission also provides guidance on the implementation of the CRA, please consult the question 10 of this FAQ for the references."

### Q1. What is the Cyber Resilience Act's Single Reporting Platform (CRA SRP)?
The CRA Single Reporting Platform (SRP) is an online tool for manufacturers and open-source software stewards to meet their obligation to report actively exploited vulnerabilities and severe incidents having an impact on the security of products with digital elements under the Cyber Resilience Act (CRA). Designed to simplify EU reporting obligations, the SRP enables manufacturers to report only once, rather than having to notify multiple national authorities individually. The platform incorporates security measures to protect confidentiality.

Manufacturers and open-source software stewards submit notifications electronically through the SRP and select the relevant CSIRT designated as coordinator. In general, the national CSIRT to which the notification should be submitted is primarily determined by the main location of establishment, in accordance with Article 14(7) of the CRA. Once submitted, the notification is simultaneously made available to ENISA, while the CSIRT initially receiving it disseminates the information to other relevant CSIRTs in Member States where the product is also available, and to market surveillance authorities as needed.

### Q2. What is the legal basis for CRA SRP?
The legal basis for the operation of the SRP is the Cyber Resilience Act (CRA), which states in Article 16(1): For the purposes of the notifications referred to in Article 14(1) and (3) and Article 15(1) and (2) and in order to simplify the reporting obligations of manufacturers, a single reporting platform shall be established by ENISA. The day-to-day operations of that single reporting platform shall be managed and maintained by ENISA. The architecture of the single reporting platform shall allow Member States and ENISA to put in place their own electronic notification end-points.

Articles 14-17 of the CRA provide the details of the ecosystem for reporting of vulnerabilities. Additionally, in December 2025 the European Commission published a Delegated Regulation specifying the conditions for delaying the dissemination of notifications.

### Q3. Who is responsible for establishing and managing the platform?
ENISA is tasked with establishing, managing, and maintaining the day-to-day operations of the CRA SRP. ENISA must also ensure the platform's security and implement appropriate technical and organizational measures to protect the information submitted.

### Q4. When will the Single Reporting Platform be operational?
The platform is scheduled to be operational by 11 September 2026. This coincides with the date when the mandatory reporting obligations for manufacturers officially enter into application (art.14 of Cyber Resilience Act). A testing period is expected to take place before this date.

### Q5. What must be reported via the platform?
Under CRA, manufacturers will be obliged to notify two specific types of occurrences:
- Actively Exploited Vulnerabilities: Vulnerabilities in products with digital elements for which there is reliable evidence that they have been exploited by a malicious actor;
- Severe Incidents: Incidents that have a severe impact on the security of the product with digital elements (e.g., compromising availability, authenticity, integrity, or confidentiality); the criteria for severity are defined in Article 14(5).

Open-source software stewards are subject to reporting obligations to the extent that they are involved with products with digital elements, as per Article 24(3) of CRA.

### Q6. What else can be reported in the platform?
In the future, the platform will also offer functionality for voluntary reporting. This functionality will be enabled in the next phase of the CRA SRP.

Any natural or legal person may notify on a voluntary basis:
- Vulnerabilities contained in a product with digital elements;
- Cyber threats that could affect the risk profile of a product with digital elements;
- Incidents having an impact on the security of a product;
- Near misses that could have resulted in an incident.

### Q7. What are the deadlines for reporting?
Reporting process starts at the moment manufacturer becomes aware of active exploitation of vulnerability or incident.

'Actively exploited vulnerability' means a vulnerability for which there is reliable evidence that a malicious actor has exploited it in a system without permission of the system owner (CRA definition).

'Incident having an impact on the security of the product with digital elements' means an incident that negatively affects or is capable of negatively affecting the ability of a product with digital elements to protect the availability, authenticity, integrity or confidentiality of data or functions (CRA definition).

The manufacturers and open-source software stewards must adhere to specific deadlines:
- Early Warning: Without undue delay and in any case within 24 hours of becoming aware of the vulnerability or incident;
- Vulnerability/Incident Notification: Without undue delay and in any case within 72 hours of becoming aware, providing general information and an initial assessment;
- Final Report:
  - For vulnerabilities: No later than 14 days after a corrective measure (e.g., patch) is available.
  - For severe incidents: Within 1 month after the initial notification.

### Q8. How does the Single Reporting Platform operate?
Manufacturers submit notifications electronically through the platform, which automatically routes them to the designated CSIRT coordinator (based on the manufacturer's main establishment) and ENISA simultaneously. The CSIRT then disseminates the information without delay to other relevant CSIRTs in Member States where the product is available, and to market surveillance authorities as needed. For sensitive reports, dissemination may be delayed on security grounds. More detailed information on the delayed dissemination process is provided in [Q21]. The platform incorporates security measures to protect confidentiality.

### Q9. How will the platform be accessible and how will the registration process work?
The SRP platform will be accessible through a dedicated public URL, which will be communicated and published in due course on this page before the platform goes live.

Manufacturers and open-source stewards representatives (AR), will be required to register using an EU Login account, which can be created in advance at the following link: https://ecas.ec.europa.eu/cas/login.

The validation that a representative can submit a report on behalf of a specific manufacturer will subsequently be performed by the CSIRT designated as coordinator. This validation will take place after the first access to the platform, in parallel with the reporting process, and will not affect the manufacturer's or open-source steward's ability to submit notifications through the platform.

The specific validation procedure may vary between CSIRTs and will remain the responsibility of the relevant CSIRT. To avoid significantly increasing the validation workload of designated CSIRTs, manufacturers and open-source stewards are advised to register and initiate the validation process only when they need to submit a specific notification.

More information can be found in the regularly updated guidance documents, to which we provide links at the bottom of this page.

### Q10. Where can I get further information on the application of the CRA?
To ensure smooth implementation of the CRA, the European Commission has set up a web page about the reporting obligations, including a document "FAQs on the CRA Implementation", which specifies in section 5 more details related to the reporting obligations under this Regulation.

On the 27th July 2026 the European Commission has published the Guidance to support timely Cyber Resilience Act implementation. In particular, the point 9.1 of the Guidance document explains in detail reporting obligations of manufacturers and open-source software stewards.

Also in July 2026 ENISA published guidance documents, available at the bottom of this page.

### Q11. How is the term "actively exploited vulnerability" interpreted in practice?
The European Commission explains this term in its subsection 5.1 of its "FAQs on the CRA Implementation" – How can a manufacturer become aware of an actively exploited vulnerability or a severe incident?, alongside with other information related to the legal interpretation of CRA.

### Q12. Do I need to report a vulnerability discovered in products made available before the entry into force of the CRA?
Please refer to the European Commission's "FAQs on the CRA Implementation", in particular for this context to the subsection 5.3 – Does a manufacturer need to report actively exploited vulnerabilities or severe incidents for products placed on the market before the CRA applies?

### Q13. Do I need to report vulnerabilities that have been actively exploited before the CRA applies?
The manufacturer's obligation to report actively exploited vulnerabilities applies once the manufacturer becomes aware of them. The European's Commission draft guidance provides further explanations on when a manufacturer is regarded to have become aware (section 9.1). The obligation does not extend to reporting of vulnerabilities the active exploitation of which the manufacturer was already aware before the CRA reporting obligation applies.

### Q14. If a vulnerability in my product has its source in a third-party component, am I still obliged to notify it?
Please refer to the European Commission's FAQ in section 5.4 - If an actively exploited vulnerability is contained in a third-party component, are all manufacturers integrating that component required to notify it?

### Q15. Can the notification workflow be automated for large number of notifications from one manufacturer?
Organisations might automate reporting workflows and integrate reporting requirements into their systems and databases, however no Application Programming Interfaces will be provided at this stage. The relevant data fields for reporting can be found in the next section of this FAQ (Q16).

### Q16. What are the data fields to be filled in the reporting template?
The table below explains the fields that will be obligatory (stemming directly from CRA or identified by logical consequence) or optional at each stage of reporting.

Legend: A — automated (not visible for the submitter); X — obligatory; C — by default copied from previous step, or updated; O — optional; I — obligatory if such information available.

Common fields (24h / 72h / Final):
1. Notification type (Vulnerability/Incident): X / C / C
2. Notification level (24h/72h/Final): X / X / X
3. Reporting time - 24h: A / A / A
4. Reporting time - 72h: A / A / A
5. Reporting time - Final: A / A / A
6. Reporter: A / A / A
7. Name of manufacturer or open-source software steward: X / C / C
8. Product: X / C / C
9. Product Type (Default/Important/Critical): O / C / C
10. Product Category (If Product Type other than Default - CRA Annex III/IV): O / C / C
11. Member States where product available: I / C / C
12. Title: X / C / C

Vulnerability fields:
v13. CVE ID: O / C / C
v14. EUVD ID: O / C / C
v15. General information, in particular: O / X / C
v16. a. General nature of the vulnerability: O / X / C
v17. b. General nature of the exploit: O / X / C
v18. Corrective or mitigating measures taken: O / X / C
v19. Corrective or mitigating measures that users can take: O / X / C
v20. Considered sensitivity of information: O / I / C
v21. Date when corrective or mitigating measure has been available: O / O / X
v22. Full description of the vulnerability, incl.: O / O / X
v23. a. Severity of the vulnerability: O / O / X
v24. b. Impact of the vulnerability: O / O / X
v25. Malicious actor that has exploited / is exploiting the vulnerability: O / O / I
v26. Details about the security update / corrective measures available: O / O / X

Incident fields:
i13. Incident is suspected by unlawful or malicious acts: X / C / C
i14. General information, about the nature of the incident: O / X / C
i15. Date and time when the incident was detected: O / X / C
i16. Date and time when the incident occurred: O / X / C
i17. Initial assessment of the incident: O / X / C
i18. Corrective or mitigating measures taken: O / X / C
i19. Corrective or mitigating measures that users can take: O / X / C
i20. Considered sensitivity of information: O / I / C
Detailed description of the incident, incl.: O / O / X
i21. a. Severity of the incident, where:
  1) it negatively affects or is capable of negatively affecting the ability of a product with digital elements to protect the availability, authenticity, integrity or confidentiality of sensitive or important data or functions; or
  2) it has led or is capable of leading to the introduction or execution of malicious code in a product with digital elements or in the network and information systems of a user of the product with digital elements: O / O / X
i23. b. Impact of the incident: O / O / X
i24. Type of threat or root cause that is likely to have triggered the incident: O / O / X
i25. Applied and ongoing mitigation measures: O / O / X

### Q17. Will any trainings be provided for the relevant parties?
Yes. ENISA recognises the need to ensure that all relevant contributors and reporting teams have sufficient time to prepare ahead of the CRA reporting obligations becoming applicable. Guidance instructions and a fact sheet have been published by ENISA in July 2026 and are successively expanded and updated. Other material, including a PDF manual tutorial videos, will be published closer to the launch of the Platform. To support training and preparation efforts, ENISA also foresees to hold a webinar two weeks before the entry into service of the SRP.

### Q18. How do I know what is the national CSIRT to which I should report through the CRA SRP?
The national CSIRT to which you should report through the SRP is essentially determined by your main location of establishment (or of the establishment of your authorised representative, if you are not established in the EU). The CRA Art.14(7) provides detailed information allowing for the manufacturer to identify the national CSIRT to report to.

Additional information (list of national CSIRTs designated as coordinators) will be provided by ENISA at the later stage.

### Q19. What are the responsibilities of key entities involved with the CRA SRP?
- Manufacturers: Submit timely notifications and comply with the other obligations established by the CRA;
- Open-source software stewards: Submit timely notifications to the extent that they are involved with products with digital elements, as per Article 24(3);
- ENISA: Manages the platform, processes reports, prepares biennial trend reports (first due within 24 months of the reporting obligations starting), operates a helpdesk (especially for SMEs), and discloses fixed vulnerabilities to the European Vulnerability Database;
- CSIRTs Designated as Coordinators: Receive and assess reports, decide on dissemination delays, inform market surveillance authorities and the public if necessary, and provide helpdesk support alongside ENISA;
- European Commission: Adopts delegated and implementing acts (e.g., for delay criteria and report formats), evaluates the platform's effectiveness, and supports coordination of enforcement activities;
- Market Surveillance Authorities: Receive disseminated information and enforce compliance, such as through investigations or corrective actions.

### Q20. Who receives the reports submitted to the platform?
As a general rule, when a manufacturer submits a report to the CRA SRP, it is simultaneously notified to:
- The CSIRT (Computer Security Incident Response Team) designated as the coordinator in the Member State where the manufacturer is established.
- ENISA (unless particularly exceptional circumstances apply).

The CSIRT designated as coordinator that initially receives the notification is then responsible for disseminating it without delay to other relevant CSIRTs across the EU via the platform.

### Q21. Can the dissemination of a report be delayed or withheld?
Yes. In exceptional circumstances, the receiving CSIRT may decide to delay or withhold the dissemination of a notification to other Member States. This is strictly limited to cases where immediate dissemination is justified on security related grounds (e.g., if spreading the information would pose an even greater security risk).

The European Commission adopted a delegated act on 11 December 2025 to further specify the terms and conditions for applying these grounds.

In particularly exceptional circumstances, ENISA will not receive the full content of the 72-hour notification. This is only the case where, in the 72-hour notification, the manufacturer actively marks that at least one of the conditions listed in points (a) to (c) of Article 16(2) applies. In such case, ENISA only receives partial information, until the receiving CSIRT discloses the full notification.

### Q22. How does the platform ensure security?
ENISA is legally required to take appropriate measures to manage risks to the platform's security and must notify the CSIRTs Network and the Commission of any security incidents affecting the platform itself.

Before its launch, the platform will be subject to user and security testing, to ensure its reliability. It will be also periodically re-checked.

### Q23. How is the CSIRTs network involved?
As provided in CRA Article 16, ENISA is engaging the CSIRTs Network in development and future testing of the CRA SRP.

## Guidance documents (User guidance section, on the main SRP page)

- "CRA SRP - AR User registration" — Updated: 3/08/2026. "This page provides information on the Assigned Representatives (AR) user registration in the SRP. It is intended for AR users (Primary and Secondary)."
- "CRA SRP - AR Notification submission and update" — Updated: 3/08/2026. "This page provides information on the Assigned Representatives (AR) submission and update of notifications in the SRP. It is intended for AR users (Primary and Secondary)."
- "CRA SRP - AR Interface functions" — Updated: 14/08/2026 — **[New, first seen 2026-08-24]**. "This page explains the AR's interface of the SRP for various functions that can be performed."

Support contact listed on the main page: cra-srp-helpdesk[@]enisa.europa.eu

## Check log

- 2026-06-19: baseline established (10 Q&A entries added in prior sync; see git history).
- 2026-06-23: checked — minor wording/cross-reference additions found in intro and Q1, Q8, Q10, Q13, Q15, Q16 (no questions added or removed). File updated accordingly.
- 2026-06-24: checked — no changes detected (still Q1–Q23, same intro and data-field table). File unchanged except this log entry.
- 2026-06-25: checked — no changes detected (still Q1–Q23, same intro and Q16 data-field table values). File unchanged except this log entry.
- 2026-06-25: file dropped from this repo as part of public-release sanitisation (internal change-detection only; full version maintained privately). See commit 2eb8a20.
- 2026-07-20: file recreated in this repo at explicit user request. Checked — page shows "Updated: 17 July 2026"; live page flags Q9 and Q17 as "[Updated]". Q9 rewritten with full registration/EU Login process detail (previously a placeholder pending June 2026 manuals); Q17 updated from "available within June" to "published in July," now naming short videos and a fact sheet. No questions added or removed (still Q1–Q23). Q16 data-field table values verified unchanged.
- 2026-08-01: checked — page now shows "Updated: 31 July 2026" (no more per-question "[Updated]" tags on the live page itself). Still Q1–Q23, no questions added or removed. Three entries changed: Q9 (added closing pointer to guidance documents), Q10 (draft Communication → final "Guidance to support timely Cyber Resilience Act implementation" published 27 July 2026), Q17 (training materials now published, not just promised; added webinar "two weeks before" launch detail). New guidance-documents list added at bottom of page ("CRA SRP - AR User registration" and "CRA SRP - AR Notification submission and update", both dated 31/07/2026). Intro, Q1, Q8, and Q16 data-field table verified unchanged. File updated accordingly.
- 2026-08-03: checked (fetched raw HTML directly, not just the summarizing fetch tool, to allow a full word-for-word diff) — still "Updated: 31 July 2026", still Q1–Q23, no questions added/removed/changed, Q16 data-field table and bottom guidance-documents list verified unchanged. One new item found: a "CRA Single Reporting Platform Factsheet" section with a direct download link (https://www.enisa.europa.eu/media/57221) now appears between the intro and the FAQ heading — previously the factsheet was only mentioned in Q17's text with no dedicated link. File updated accordingly.
- 2026-08-24: checked (fetched raw HTML directly for both the main SRP page and, after discovering it, the new dedicated FAQ subpage, for a full word-for-word diff). Major structural change: the FAQ content moved off the main page onto its own subpage (`faq_url`), which now shows "Updated: 03 August 2026" and a single page-level update note instead of per-question "[Updated]" tags. All 23 questions received a copyediting pass (wording/punctuation only, no substantive changes to dates, deadlines, or obligations) and Q16's 39-entry data-field table was verified value-for-value unchanged. New third guidance document added ("CRA SRP - AR Interface functions", updated 14/08/2026); the two existing guidance documents now show "Updated: 3/08/2026" (previously 31/07/2026). Main-page intro paragraph reworded (new lead sentence added; standalone EUR-Lex reference line replaced with an inline link). Factsheet section and its download link unchanged. File updated accordingly.
- 2026-08-31: checked (fetched raw HTML directly for both the main SRP page and the FAQ subpage, for a full word-for-word diff; old main-page URL was found to now 301/meta-redirect to a new URL, so both were fetched). Still Q1–Q23, no questions added/removed/reordered. Main page's canonical URL changed from `.../topics/product-security-and-certification/single-reporting-platform-srp` to `.../topics/product-security/single-reporting-platform-srp` (old URL now redirects; recorded as `old_url`). Three answers changed in substance/wording: Q1 (reworded to present tense, same substance), Q6 (removed the specific "after 11 September 2026" trigger date for voluntary reporting, now "next phase of the CRA SRP"), Q17 (training material description changed from "short videos" to "a PDF manual tutorial videos"). Page-level "Updated: 03 August 2026" note was not bumped despite these edits. Intro, Q2–Q5, Q7–Q16 (incl. data-field table values), Q18–Q23, and guidance-documents section verified unchanged. File updated accordingly.
