---
source: ENISA — Single Reporting Platform (SRP)
url: https://www.enisa.europa.eu/topics/product-security-and-certification/single-reporting-platform-srp
retrieved: 2026-08-03
purpose: Baseline snapshot for change detection. Future runs diff the live page against this file.
note: One logical block per FAQ entry to keep diffs readable. Update `retrieved` and content when a change is confirmed.
last_check: 2026-08-03
last_change: 2026-08-03
---

# ENISA Single Reporting Platform (SRP) — FAQ Baseline

## Change log (2026-08-03 check, vs. 2026-08-01 baseline)

No FAQ questions were added, deleted, or changed (still Q1–Q23, same "Updated: 31 July 2026" note, same data-field table values, same guidance-documents list). One change found outside the FAQ:

- **New: "CRA Single Reporting Platform Factsheet" section** — added between the intro paragraphs and the "Frequently Asked Questions" heading. Reads: "ENISA has published a factsheet on the CRA Single Reporting Platform. It can be downloaded here, currently in English." Links to https://www.enisa.europa.eu/media/57221. This factsheet was previously only referenced in text (Q17: "Guidance instructions and a fact sheet have been published...") with no dedicated section or direct download link on the page.

All 23 FAQ entries, the Q16 data-field table, and the guidance-documents list at the bottom were verified word-for-word unchanged from the 2026-08-01 baseline.

## Change log (2026-08-01 check, vs. 2026-07-20 baseline)

The live page now carries an "Updated: 31 July 2026" note (previously "17 July 2026"). No FAQ questions were added or deleted (still Q1–Q23), and the page no longer marks individual questions with an "[Updated]" tag (the 17 July version did). Three existing entries were **changed**, and a **new section** (guidance documents list) was added:

- **Q9** ("How will the platform be accessible and how will the registration process work?") — one sentence added at the end: now points readers to "the regularly updated guidance documents, to which we provide links at the bottom of this page." Rest of the answer is unchanged.
- **Q10** ("Where can I get further information on the application of the CRA?") — updated. Previously said the Commission had published a *draft* Communication (section 9.1 on reporting obligations) and that "a final version ... will be adopted shortly." Now states the Commission published the final **"Guidance to support timely Cyber Resilience Act implementation"** on **27 July 2026** (point 9.1 covers reporting obligations), and notes ENISA also published its own guidance documents in July 2026, linked at the bottom of the page.
- **Q17** ("Will any trainings be provided for the relevant parties?") — updated from future/promised tense to actual: guidance instructions and a fact sheet **have been published** by ENISA in July 2026 (and are being successively expanded/updated); short videos will follow closer to platform launch; ENISA now also states it foresees holding a **webinar two weeks before** the SRP enters into service.
- **New: guidance documents section** — the page now lists downloadable guidance documents at the bottom, referenced from Q9/Q10/Q17: "CRA SRP - AR User registration" (Updated 31/07/2026) and "CRA SRP - AR Notification submission and update" (Updated 31/07/2026).

Intro text, Q1, Q8, and Q16's data-field table (field list, and X/C/O/I/A requirement values for all common/vulnerability/incident fields) verified unchanged.

## Intro

The Single Reporting Platform (SRP) provided for in the Cyber Resilience Act (CRA) shall become a technical tool to use for the reporting of actively exploited vulnerabilities and incidents impacting products with digital elements operating in the EU Digital Single Market.

The SRP will be used by CSIRTs and manufacturers for mandatory reporting and could be used by any natural/legal persons for voluntary reporting.

The CRA mandates manufacturers of products with digital elements to report actively exploited vulnerabilities and severe incidents having an impact on the security of the product as of 11 September 2026 onwards using the Single Reporting Platform. Throughout 2025 and 2026, ENISA is undertaking a number of necessary steps to support the successful implementation of the platform.

The CRA brings transparency to the vulnerability disclosure processes and strengthens how EU CSIRTs can mitigate risks stemming from vulnerabilities.

Further information: Regulation (EU) 2024/2847 (EUR-Lex).

### CRA Single Reporting Platform Factsheet [New, first seen 2026-08-03]

ENISA has published a factsheet on the CRA Single Reporting Platform. It can be downloaded here (https://www.enisa.europa.eu/media/57221), currently in English.

This FAQ collection on the CRA SRP is intended for publication on the ENISA website and is updated during implementation. See also the European Commission's CRA reporting page (digital-strategy.ec.europa.eu/en/policies/cra-reporting) and, in particular, the FAQ document linked there (ec.europa.eu/newsroom/dae/redirection/document/122331).

## FAQ entries

### Q1. What is the Cyber Resilience Act's Single Reporting Platform (CRA SRP)?
CRA SRP will be a centralized electronic system designed to simplify reporting obligations for manufacturers and open-source software stewards. It will serve as a "single entry point," allowing manufacturers to report actively exploited vulnerabilities and severe incidents only once, rather than notifying multiple national authorities individually.

Manufacturers will submit notifications electronically, selecting the CSIRT designated as coordinator (based on the manufacturer's main establishment location per CRA Article 14(7)) and ENISA simultaneously. The CSIRT will then disseminate information without delay to other relevant CSIRTs in Member States where the product is available, and to market surveillance authorities as needed. The platform will incorporate security measures to protect confidentiality.

### Q2. What is the legal basis for CRA SRP?
The legal basis is the Cyber Resilience Act (CRA), Article 16(1): "For the purposes of the notifications referred to in Article 14(1) and (3) and Article 15(1) and (2) and in order to simplify the reporting obligations of manufacturers, a single reporting platform shall be established by ENISA. The day-to-day operations of that single reporting platform shall be managed and maintained by ENISA."

The architecture of the single reporting platform shall allow Member States and ENISA to put in place their own electronic notification end-points.

Articles 14–17 of the CRA provide details of the ecosystem for reporting vulnerabilities. In December 2025, the European Commission published a Delegated Regulation specifying conditions for delaying dissemination of notifications.

### Q3. Who is responsible for establishing and managing the platform?
ENISA is tasked with establishing, managing, and maintaining the day-to-day operations of the CRA SRP. ENISA must ensure the platform's security and implement appropriate technical and organizational measures to protect submitted information.

### Q4. When will the Single Reporting Platform be operational?
The platform is scheduled to be operational by 11 September 2026. This coincides with when mandatory reporting obligations for manufacturers officially enter into application (Article 14 of the Cyber Resilience Act). A testing period is expected before this date.

### Q5. What must be reported via the platform?
Under CRA, manufacturers will be obliged to notify two specific types of occurrences:
- Actively Exploited Vulnerabilities: vulnerabilities in products with digital elements for which there is reliable evidence they have been exploited by a malicious actor.
- Severe Incidents: incidents that have a severe impact on the security of the product with digital elements (compromising availability, authenticity, integrity, or confidentiality); criteria for severity are defined in Article 14(5).

Open-source software stewards are subject to reporting obligations to the extent they are involved with products with digital elements, as per Article 24(3) of CRA.

### Q6. What else can be reported in the platform?
The platform will offer functionality for voluntary reporting after 11 September 2026. Any natural or legal person may voluntarily notify:
- Vulnerabilities contained in a product with digital elements
- Cyber threats that could affect the risk profile of a product with digital elements
- Incidents having an impact on the security of a product
- Near misses that could have resulted in an incident

### Q7. What are the deadlines for reporting?
The reporting process starts when a manufacturer becomes aware of active exploitation of a vulnerability or incident.

"Actively exploited vulnerability" means a vulnerability for which there is reliable evidence that a malicious actor has exploited it in a system without permission of the system owner (CRA definition).

"Incident having an impact on the security of the product with digital elements" means an incident that negatively affects or is capable of negatively affecting the ability of a product with digital elements to protect the availability, authenticity, integrity or confidentiality of data or functions (CRA definition).

Manufacturers and open-source software stewards must adhere to specific deadlines:
- Early Warning: without undue delay and in any case within 24 hours of becoming aware.
- Vulnerability/Incident Notification: without undue delay and in any case within 72 hours of becoming aware, providing general information and an initial assessment.
- Final Report:
  - For vulnerabilities: no later than 14 days after a corrective measure (e.g., patch) is available.
  - For severe incidents: within 1 month after the initial notification.

### Q8. How does the Single Reporting Platform operate?
Manufacturers submit notifications electronically through the platform, which automatically routes them to the designated CSIRT coordinator (based on manufacturer's main establishment) and ENISA simultaneously. The CSIRT then disseminates information without delay to other relevant CSIRTs in Member States where the product is available, and to market surveillance authorities as needed. For sensitive reports, dissemination may be delayed on security grounds — see Q21 for more detail on the delayed dissemination process. The platform incorporates security measures to protect confidentiality.

### Q9. How will the platform be accessible and how will the registration process work? [Updated 31 July 2026]
The SRP platform will be accessible through a dedicated public URL, which will be communicated and published in due course on this page before the platform goes live.

Manufacturers and open-source stewards representatives (AR), will be required to register using an EU Login account, which can be created in advance at the following link: ecas.ec.europa.eu/cas/login.

The validation that a representative can submit a report on behalf of a specific manufacturer will subsequently be performed by the CSIRT designated as coordinator. This validation will take place after the first access to the platform, in parallel with the reporting process, and will not affect the manufacturer's or open-source steward's ability to submit notifications through the platform.

The specific validation procedure may vary between CSIRTs and will remain the responsibility of the relevant CSIRT. To avoid significantly increasing the validation workload of designated CSIRTs, manufacturers and open-source stewards are advised to register and initiate the validation process only when they need to submit a specific notification.

More information can be found in the regularly updated guidance documents, to which we provide links at the bottom of this page.

### Q10. Where can I get further information on the application of the CRA? [Updated 31 July 2026]
To ensure smooth implementation of the CRA, the European Commission has set up a web page about the reporting obligations, including a document "FAQs on the CRA Implementation," which specifies in section 5 more details related to the reporting obligations under this Regulation.

On the 27th July 2026 the European Commission published the "Guidance to support timely Cyber Resilience Act implementation." In particular, point 9.1 of the Guidance document explains in detail the reporting obligations of manufacturers and open-source software stewards.

Also in July 2026, ENISA published guidance documents, available at the bottom of this page.

### Q11. How is the term "actively exploited vulnerability" interpreted in practice?
The European Commission explains this term in subsection 5.1 of its "FAQs on the CRA Implementation" alongside other information related to the legal interpretation of CRA.

### Q12. Do I need to report a vulnerability discovered in products made available before the entry into force of the CRA?
Refer to the European Commission's "FAQs on the CRA Implementation," particularly subsection 5.3 — "Does a manufacturer need to report actively exploited vulnerabilities or severe incidents for products placed on the market before the CRA applies?"

### Q13. Do I need to report vulnerabilities that have been actively exploited before the CRA applies?
The manufacturer's obligation to report actively exploited vulnerabilities applies once they become aware of them. The European Commission's draft guidance provides further explanations on when a manufacturer is regarded to have become aware (section 9.1). The obligation does not extend to reporting vulnerabilities of which the manufacturer was already aware before the CRA reporting obligation applies.

### Q14. If a vulnerability in my product has its source in a third-party component, am I still obliged to notify it?
Refer to the European Commission's FAQ in section 5.4 — "If an actively exploited vulnerability is contained in a third-party component, are all manufacturers integrating that component required to notify it?"

### Q15. Can the notification workflow be automated for large numbers of notifications from one manufacturer?
Organisations might automate reporting workflows and integrate reporting requirements into their systems and databases; however, no Application Programming Interfaces will be provided at this stage. The relevant data fields for reporting can be found in Q16.

### Q16. What are the data fields to be filled in the reporting template?
Fields are classified as:
- X — obligatory
- C — by default copied from previous step, or updated
- A — automated (not visible for the submitter)
- O — optional
- I — obligatory if such information is available

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
v15. General information: O / X / C
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
i14. General information about the nature of the incident: O / X / C
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

### Q17. Will any trainings be provided for the relevant parties? [Updated 31 July 2026]
Yes. ENISA recognises the need to ensure that all relevant contributors and reporting teams have sufficient time to prepare ahead of the CRA reporting obligations becoming applicable. Guidance instructions and a fact sheet have been published by ENISA in July 2026 and are successively expanded and updated. Other material, including short videos, will be published closer to the launch of the Platform. To support training and preparation efforts, ENISA also foresees to hold a webinar two weeks before the entry into service of the SRP.

### Q18. How do I know what is the national CSIRT to which I should report through the CRA SRP?
The national CSIRT to which you should report is essentially determined by your main location of establishment (or of the establishment of your authorised representative, if you are not established in the EU). CRA Article 14(7) provides detailed information. Additional information (list of national CSIRTs designated as coordinators) will be provided by ENISA at a later stage.

### Q19. What are the responsibilities of key entities involved with the CRA SRP?
- Manufacturers: submit timely notifications and comply with other obligations established by the CRA.
- Open-source software stewards: submit timely notifications to the extent involved with products with digital elements, as per Article 24(3).
- ENISA: manages the platform, processes reports, prepares biennial trend reports (first due within 24 months of reporting obligations starting), operates a helpdesk (especially for SMEs), and discloses fixed vulnerabilities to the European Vulnerability Database.
- CSIRTs Designated as Coordinators: receive and assess reports, decide on dissemination delays, inform market surveillance authorities and the public if necessary, and provide helpdesk support alongside ENISA.
- European Commission: adopts delegated and implementing acts (e.g., for delay criteria and report formats), evaluates the platform's effectiveness, and supports coordination of enforcement activities.
- Market Surveillance Authorities: receive disseminated information and enforce compliance, such as through investigations or corrective actions.

### Q20. Who receives the reports submitted to the platform?
As a general rule, when a manufacturer submits a report to the CRA SRP, it is simultaneously notified to:
- The CSIRT designated as the coordinator in the Member State where the manufacturer is established.
- ENISA (unless particularly exceptional circumstances apply).

The CSIRT designated as coordinator that initially receives the notification is then responsible for disseminating it without delay to other relevant CSIRTs across the EU via the platform.

### Q21. Can the dissemination of a report be delayed or withheld?
Yes. In exceptional circumstances, the receiving CSIRT may decide to delay or withhold the dissemination of a notification to other Member States. This is strictly limited to cases where immediate dissemination is justified on security related grounds (if spreading information would pose an even greater security risk).

The European Commission adopted a delegated act on 11 December 2025 to further specify the terms and conditions for applying these grounds.

In particularly exceptional circumstances, ENISA will not receive the full content of the 72-hour notification. This is only the case where, in the 72-hour notification, the manufacturer actively marks that at least one of the conditions listed in points (a) to (c) of Article 16(2) applies. In such case, ENISA only receives partial information, until the receiving CSIRT discloses the full notification.

### Q22. How does the platform ensure security?
ENISA is legally required to take appropriate measures to manage risks to the platform's security and must notify the CSIRTs Network and the Commission of any security incidents affecting the platform itself. Before its launch, the platform will be subject to user and security testing, to ensure its reliability. It will also be periodically re-checked.

### Q23. How is the CSIRTs network involved?
As provided in CRA Article 16, ENISA is engaging the CSIRTs Network in development and future testing of the CRA SRP.

## Guidance documents [New 31 July 2026]

Linked at the bottom of the page (referenced from Q9, Q10, Q17):

- "CRA SRP - AR User registration" — Updated: 31/07/2026
- "CRA SRP - AR Notification submission and update" — Updated: 31/07/2026

## Check log

- 2026-06-19: baseline established (10 Q&A entries added in prior sync; see git history).
- 2026-06-23: checked — minor wording/cross-reference additions found in intro and Q1, Q8, Q10, Q13, Q15, Q16 (no questions added or removed). File updated accordingly.
- 2026-06-24: checked — no changes detected (still Q1–Q23, same intro and data-field table). File unchanged except this log entry.
- 2026-06-25: checked — no changes detected (still Q1–Q23, same intro and Q16 data-field table values). File unchanged except this log entry.
- 2026-06-25: file dropped from this repo as part of public-release sanitisation (internal change-detection only; full version maintained privately). See commit 2eb8a20.
- 2026-07-20: file recreated in this repo at explicit user request. Checked — page shows "Updated: 17 July 2026"; live page flags Q9 and Q17 as "[Updated]". Q9 rewritten with full registration/EU Login process detail (previously a placeholder pending June 2026 manuals); Q17 updated from "available within June" to "published in July," now naming short videos and a fact sheet. No questions added or removed (still Q1–Q23). Q16 data-field table values verified unchanged.
- 2026-08-01: checked — page now shows "Updated: 31 July 2026" (no more per-question "[Updated]" tags on the live page itself). Still Q1–Q23, no questions added or removed. Three entries changed: Q9 (added closing pointer to guidance documents), Q10 (draft Communication → final "Guidance to support timely Cyber Resilience Act implementation" published 27 July 2026), Q17 (training materials now published, not just promised; added webinar "two weeks before" launch detail). New guidance-documents list added at bottom of page ("CRA SRP - AR User registration" and "CRA SRP - AR Notification submission and update", both dated 31/07/2026). Intro, Q1, Q8, and Q16 data-field table verified unchanged. File updated accordingly.
- 2026-08-03: checked (fetched raw HTML directly, not just the summarizing fetch tool, to allow a full word-for-word diff) — still "Updated: 31 July 2026", still Q1–Q23, no questions added/removed/changed, Q16 data-field table and bottom guidance-documents list verified unchanged. One new item found: a "CRA Single Reporting Platform Factsheet" section with a direct download link (https://www.enisa.europa.eu/media/57221) now appears between the intro and the FAQ heading — previously the factsheet was only mentioned in Q17's text with no dedicated link. File updated accordingly.
