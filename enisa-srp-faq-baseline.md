---
source: ENISA — Single Reporting Platform (SRP)
url: https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp
old_url: https://www.enisa.europa.eu/topics/product-security-and-certification/single-reporting-platform-srp (now redirects to `url` above, first seen 2026-08-31)
faq_url: https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/frequently-asked-questions
glossary_url: https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2
csirt_list_url: https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/list-of-csirts-designated-as-coordinators
guidance_urls:
  - https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-guidance-ar-user-registration
  - https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-guidance-ar-notification-submission-and-update
  - https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-guidance-ar-interface-functions
  - https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-guidance-particular-exceptional-circumstances-pec
retrieved: 2026-09-10
guidance_retrieved: 2026-09-10
glossary_retrieved: 2026-09-10
csirt_list_retrieved: 2026-09-10
purpose: Baseline snapshot for change detection. Future runs diff the live page(s) — main/FAQ page, the new Glossary and CSIRT-list subpages, and the four guidance subpages listed in `guidance_urls` — against this file.
note: One logical block per FAQ entry / per guidance subpage to keep diffs readable. Update `retrieved` (or the other `*_retrieved` dates) and content when a change is confirmed. The Glossary and CSIRT-list pages are captured in summary/table form (field names and per-stage status, not every descriptive sentence) to keep this file diffable — see the "Scope note" under each of those sections. `guidance_urls[3]` (the PEC guidance page) was added 2026-09-08 14:10 UTC, discovered via the main page's "Content" navigation — it is not yet listed as a card in the main page's own "User guidance" section, unlike the other three. None of the four guidance-page date stamps is a reliable change signal, in either direction — AR User Registration and AR Notification Submission and Update have each had their stamp move only once since first capture despite being edited more often than that; PEC went weeks with no stamp at all before gaining one on 2026-09-09; and AR Interface Functions was rewritten twice on 2026-09-09 (21:07 and 22:12 UTC) with the stamp reading "09/09/2026" both times — so even a stamp that has just moved is no guarantee against a same-day second edit. Diff the text on every check, not the date.
last_check: 2026-09-10
last_change: 2026-09-10
---

# ENISA Single Reporting Platform (SRP) — FAQ Baseline

## Change log

Newest first. One entry per check that found something; runs that find nothing changed leave no entry.

### 2026-09-10 01:08 UTC (vs. 2026-09-10 00:10 UTC)

All eight pages returned HTTP 200. One long-tracked FAQ typo was fixed; nothing else moved.

**Fixed**

- **Q26** (FAQ): the "72-hour **Sever** Incident Notification" typo (present since at least 2026-09-07) is fixed → "72-hour **Severe** Incident Notification". Purely the missing "e" — no counter logic, deadline, or obligation affected.

**Unchanged**

Main page (still 6 items in Content nav, no Glossary/9th entry; no PEC card in "User guidance"). FAQ (Q1–Q30, same tags, Q16 table, "Updated: 09 September 2026" — unmoved despite this fix). CSIRT list (27 countries, "contacts of EU CSIRTs...", "Updated: 04/09/2026"). AR User Registration (stamp "09/09/2026"). AR Notification Submission and Update (stamp "03 September 2026"). AR Interface Functions (stamp "09/09/2026"). PEC guidance (stamp "09 September 2026"). Glossary (all 38 fields re-verified, footer still "version 1.1, last update: 05/09/2026").

### 2026-09-10 00:10 UTC (vs. 2026-09-09 23:11 UTC)

All eight pages returned HTTP 200. One cosmetic wording change on a single guidance page; nothing else moved.

**Editorial**

- **AR User Registration** intro sentence: "This page provides information on the **Assigned Representatives** (AR) user registration in the SRP." → "...the **Assigned Representative** (AR) user registration...", singular. The page's own "Last updated: 09 September 2026" stamp did not move. The main page's "User guidance" card blurb describing this same page still reads the plural "Assigned Representatives" — a new (very small) internal inconsistency between the two, not present before today. No precondition, deadline, obligation, or field affected.

**Unchanged**

Main page (still 6 items in Content nav, no Glossary/9th entry; no PEC card in "User guidance"). FAQ (Q1–Q30, same tags, Q16 table, "Updated: 09 September 2026"). CSIRT list (27 countries, "contacts of EU CSIRTs...", "Updated: 04/09/2026"). AR Notification Submission and Update (stamp "03 September 2026"). AR Interface Functions (stamp "09/09/2026"). PEC guidance (stamp "09 September 2026") — re-verified word-for-word identical, including the "Particularly"/"Particular" internal inconsistency. Glossary (all 38 fields re-verified, footer still "version 1.1, last update: 05/09/2026").

### 2026-09-09 23:11 UTC (vs. 2026-09-09 22:12 UTC)

All eight pages returned HTTP 200. Only the FAQ and CSIRT-list pages changed; the four guidance pages, the main page and the Glossary are all unchanged from the 22:12 UTC check.

**Changed**

- **Q9** (FAQ): "**Validation** takes place in parallel..." → "**Verification** takes place in parallel...", the same sentence still ending "...while validation is pending" — a new internal inconsistency, and the continuation of the validation→verification rewording already logged at 12:19 UTC, which missed this sentence.
- **Q16 intro** (FAQ): the long-tracked "it explains **that** the field means" typo is fixed → "it explains **what** the field means".
- **Q16 table, field 22** (FAQ): "Corrective or mitigating measures that **user** can take" typo fixed → "...that **users** can take".
- **Q16 table, fields v28/v29** (FAQ): "**Full** description of the severity/impact of the vulnerability" → "**Detailed** description of the severity/impact of the vulnerability". This now matches the SI fields' wording (i38/i39) but creates a **new** FAQ/Glossary mismatch: the Glossary's own v23/v24 rows for these same two fields still read "Full description..." — not touched today.
- **CSIRT list page note**: "This list provides the contacts **to the** CSIRTs Designated as Coordinators..." → "...contacts **of EU** CSIRTs Designated as Coordinators...". Flagged with a provenance caveat in the baseline text itself: every check since first capture (2026-09-07) recorded this page as "unchanged" without re-quoting the sentence, so whether this wording changed today or was simply never re-verified word-for-word before now cannot be determined from this run alone.

**Watch**

- FAQ Q16 and the Glossary now disagree on v28/v29's field name ("Detailed" vs. "Full") — previously in sync.

**Unchanged**

Main page (still 6 items in Content nav, no Glossary/9th entry; no PEC card in "User guidance"). AR User Registration (stamp "09/09/2026"). AR Notification Submission and Update (stamp "03 September 2026"). AR Interface Functions (stamp "09/09/2026", unmoved). PEC guidance (stamp "09 September 2026"). Glossary (all 38 fields re-verified, footer still "version 1.1, last update: 05/09/2026").

### 2026-09-09 22:12 UTC (vs. 2026-09-09 21:07 UTC)

All eight pages returned HTTP 200. Three of the four guidance pages were rewritten again — the fourth, PEC, gained its first-ever date stamp — and one long-tracked bug and one long-tracked numeric inconsistency were both fixed in the same pass.

**Changed**

- **AR Notification Submission and Update** was rewritten into the same second-person "Follow these steps…" style already used by the other two guidance pages (numbered steps, added screenshots), and its page date moved for the first time since tracking began: "3/08/2026" → **"03 September 2026"**. Substance, statuses and the "Particularly **Exception** Circumstances" (missing "-al") typo are all unchanged.
- **AR User Registration** reworded again, stamp "08/09/2026" → **"09 September 2026"**. The long-tracked "manufacturer **adress**" typo is fixed → "address". The self-contradictory "These fields cannot be edited but are retrieved from EU Login and cannot be edited in the SRP" is fixed → "These fields are retrieved from EU Login and cannot be edited in the SRP." The Secondary-AR invitation precondition is reworded from "The Primary AR is a validated user" to **"The feature to invite a Secondary AR is available only to a 'Verified' Primary AR"**, now matching Q9's own "Verified" term. New defect: the Primary AR flow's confirm-details step now lists only "First Name, Last Name, Email", dropping "Legal name" — the Secondary AR flow still lists all four.
- **AR Interface Functions** reworded a second time today, still dated "09/09/2026" (unchanged from the 21:07 UTC rewrite — a date stamp that has just moved is no guard against a same-day second edit). Two real fixes: the long-standing invitation-recipient bug is resolved — the expected result now correctly reads **"The SRP sends an email invitation to the Secondary AR"** (was "An email is sent to the Primary AR, which instructs the Secondary AR…"); and the Unverified-AR notification cap is corrected from **10 to 20**, reconciling it with Q9's own number. Also: "Invite Secondary AR" gained a new precondition (the Primary AR's own association must be "Verified"); the "Remove Association" button is renamed **"Delete Association"**; the Dashboard gained a third access route ("selecting a Notification Alert, where available"); the named "Action Required" filter tab is now only "the appropriate tab" (name dropped); and a new grammar defect appeared — "request to the Primary AR role" (a word is missing).
- **PEC guidance** gained a **"Last updated: 09 September 2026"** stamp — its first ever, after weeks with none. New defect: three body instances now read "**Particular** Exceptional Circumstances (PEC)" (dropped "-ly"), while the opening sentence still reads "**Particularly** Exceptional Circumstances (PEC)" — the page's own defined term is now spelled two ways on itself.

**Watch**

- AR User Registration's two flows now disagree on which personal-detail fields are shown for confirmation (Primary: 3 fields; Secondary: 4, including Legal name).
- None of the four guidance-page date stamps is a reliable change signal, in either direction: two moved only once despite repeated edits, one went weeks with none before suddenly gaining one, and one was edited twice in a day without moving at all the second time.

**Editorial**

- Numerous wording/structure changes across all three rewritten guidance pages (explicit Pre-conditions/Steps headings, added screenshots, tense and phrasing shifts) not itemised individually.

**Unchanged**

Main page (still no Glossary entry in Content navigation, no PEC card in "User guidance"), FAQ (Q1–Q30, same tags, Q16 table, "Updated: 09 September 2026"), CSIRT list (27 countries, same links, "Updated: 04/09/2026"), Glossary (all 38 fields re-verified row by row in `enisa-srp-glossary-baseline.md`, footer still "version 1.1, last update: 05/09/2026").

### 2026-09-09 21:07 UTC (vs. 2026-09-09 12:19 UTC)

Two guidance pages were rewritten again; nothing else moved. All eight pages returned HTTP 200.

**Changed**

- **AR Interface Functions guidance re-dated**: "Last updated: 07/09/2026" → **"09/09/2026"**. The rewrite fixes three typos this baseline had flagged since the 07/09 rewrite — "**Yo** can access the Dashboard" → "You can access the Dashboard"; the duplicated section title "Add an Association with an Additional Manufacturer **Association** through Settings" → "…Additional Manufacturer through Settings"; and both stray double full stops ("…request to become a Primary AR.." and "…based on your selections..") are now single. It also changes the wording of the still-unresolved invitation-flow inconsistency: "An email is sent to the Primary AR, **who** instructs the Secondary AR to complete registration" → "…**which** instructs the Secondary AR…" — the substance (email still goes to the Primary AR, still inconsistent with AR User Registration's own description of the Secondary AR clicking a link from their own email) is unchanged. The Delete AR–Manufacturer Association expected result was also recast from passive to active voice ("the AR Association is removed and its status updated to 'Deleted'" → "The system removes the AR Association, and its status is updated to 'Deleted'"), no meaning change.
- **PEC guidance reworded again**, still with no "Last updated" date stamp. The apostrophe typo is fixed: "This section explains to **the AR's**" → "This section explains to **ARs**". The long-standing **"PEC Delay Reson" typo is fixed** → "PEC Delay Reason" (and "options" narrows to singular "option"). "whether particularly exceptional circumstances, or PEC, apply" → "whether **Particularly Exceptional Circumstances (PEC)** apply" (capitalised, parenthetical form). Several smaller wording shifts throughout: "only applicable when" → "applicable only when"; "manufacturer/open-source software steward (hereinafter 'Reporter')" → "manufacturer or open-source software steward (hereinafter **the** 'Reporter')"; "72hrs report template" → "72-hour report template"; "sharing the notification manually" → "manually sharing the notification"; "provide justification which can help…to decide" → "provide **a** justification **that** can help…decide"; "AR users can access the Dashboard" → "AR users can access the **SRP** Dashboard". No deadline, obligation, legal cross-reference, or the PEC scope itself (still AEV 72-hour notifications only) changed.

**Unchanged**

Main page (still no Glossary entry in Content navigation, no PEC card in "User guidance"), FAQ (Q1–Q30, same tags, Q16 table), CSIRT list (27 countries, same links, "Updated: 04/09/2026"), Glossary (all 38 fields re-verified row by row in `enisa-srp-glossary-baseline.md`, footer still "version 1.1, last update: 05/09/2026"), AR User Registration ("Last updated: 08/09/2026") and AR Notification Submission and Update (3/08/2026) byte for byte.

### 2026-09-09 12:19 UTC (vs. 2026-09-08 23:11 UTC)

FAQ page date moved to "Updated: 09 September 2026". Q9 was rewritten with new AR-role detail, including a new precondition for inviting a Secondary AR; Q8 silently lost its "[UPDATED]" tag. Two guidance subpages (AR User Registration, PEC) were also reworded, neither with its own date stamp moving. All eight pages returned HTTP 200.

**Changed**

- **Q9** retitled from "How is the platform accessible and how does the registration process work?" to "**How do I access and register on the SRP, and what are the roles of Primary and Secondary ARs?**" (still tagged [UPDATED]). New content: "A Primary AR must first have a validated AR–manufacturer association, displayed as '**Verified**', before inviting Secondary ARs." — this formalises, on the FAQ page itself, the precondition ("The Primary AR is a validated user") that until now only appeared in the AR User Registration guidance's Secondary-AR preconditions, closing the "Watch" item opened 2026-09-08 21:06 UTC about whether it is enforced anywhere else. Also new: a paragraph on notification-access scope — "The Primary AR can access all notifications associated with the manufacturer, whereas a Secondary AR can access only the notifications they submitted themselves. A Secondary AR does not have the same administrative permissions as the Primary AR but may claim the Primary AR role, subject to review and approval by the designated CSIRT." — and a pointer to "Settings > Association Management" for checking role/association status. The 20-notification non-validated limit is restated with "validation" reworded to "verification": "ARs whose manufacturer association has not yet been verified may submit up to 20 notifications for that manufacturer before verification becomes mandatory." No numeric limit changed (still one Primary AR, up to 20 Secondary ARs, up to 20 notifications).
- **AR User Registration guidance — General Notes rewritten**, but the page's own "Last updated: 08/09/2026" stamp did **not** move. The EU-Login sentence gained a new closing clause: "Further information on EU Login is available through the official EU Login guidance at: https://trusted-digital-identity.europa.eu/index_en" (previously just "— see [link]"). The validation-timing sentence was split and expanded: "...takes place after registration (described below) and is not a prerequisite for submitting a notification. Validation takes place after the first access to the platform, in parallel with the reporting process, and will not affect the ability to submit notifications through the SRP. Specific validation procedures may vary between CSIRTs and remain the responsibility of the relevant CSIRT." No precondition, deadline or numeric limit changed. New wording defect: "ARs **that have** already an EU Login account with no MFA enabled" (was "ARs **who already have** an EU Login account…") — grammatically worse than before, reproduced verbatim.
- **PEC guidance page reworded throughout**, still carrying no "Last updated" date at all. Nearly every sentence was rephrased into a flowing-paragraph style (the descriptive "Flagging a submission" / "Effect" structure this file used to summarise it no longer corresponds to distinct headings on the live page — it never had real `<h3>` headings, but the wording under each heading changed): "(the page calls this the 'Reporter')" → "(hereinafter 'Reporter')"; the closing clause "— not for a Severe Incident" is no longer present (the scope itself is unchanged — the page still only ever describes AEV 72-hour notifications); "whether PEC applies" → "whether particularly exceptional circumstances, or PEC, apply"; "The full notification is not simultaneously made available to ENISA in this scenario — only limited information…" split into two sentences. Substance, the "PEC Delay **Reson**" typo, and the Art. 16(2) cross-references are all unchanged.

**Watch**

- Two of the three page-level "Last updated" stamps in this baseline (AR User Registration, PEC) are now known to lag real edits, the same pattern already flagged for the Glossary's "Version 1.1" footer. Do not treat an unmoved stamp on any of these pages as proof nothing changed — diff the text.

**Editorial**

- **Q8 lost its "[UPDATED]" tag** (was tagged since at least 2026-09-08; now reads plain "8. How does the Single Reporting Platform operate?", confirmed by raw-HTML tag count: 4 "[UPDATED]" occurrences on the live page now, not 5). Text itself unchanged. Recorded here since this baseline explicitly tracks per-question tags.

**Unchanged**

Main page (including the six-item Content navigation, still no Glossary entry and no PEC card in "User guidance"), CSIRT list (27 countries, same links, "Updated: 04/09/2026"), Glossary (38 fields, footer unchanged, re-verified row by row in `enisa-srp-glossary-baseline.md`), Q1–Q7, Q10–Q30 other than the Q8 tag loss, the Q16 table (43 fields, same values), AR Notification Submission and Update (3/08/2026) and AR Interface Functions (07/09/2026) byte for byte.

### 2026-09-08 23:11 UTC (vs. 2026-09-08 21:06 UTC)

All eight pages returned HTTP 200; nothing on ENISA's side changed. Two small gaps in this baseline's own capture of two guidance pages were closed on this pass — both pre-existing on the live pages, not new edits.

**Fixed (this baseline, not the page)**

- The PEC guidance page's opening sentence reads "This section explains to the **AR's** how and when to apply..." on the live page (apostrophe present, confirmed in the raw HTML as a single unbroken text node); this file had recorded it as "the ARs" (no apostrophe). Corrected to match. Whether ENISA's apostrophe is new since the page's 2026-09-08 14:10 UTC discovery, or was simply not transcribed precisely at the time, could not be determined from this run alone — treated as pre-existing page text either way and reproduced verbatim, not counted against `last_change`.
- The AR Notification Submission and Update page's live text reads "Particularly **Exception** Circumstances (PEC)" (missing "-al") in all three places the phrase occurs in its "Expected results" paragraph; this file had normalised it to "Particularly Exceptional Circumstances" in its own summary. Corrected to quote the page's typo verbatim, consistent with how other typos on these pages are already reproduced rather than silently fixed.

**Unchanged**

Main page, FAQ (Q1–Q30, same tags, Q16 table), CSIRT list (27 countries, "Updated: 04/09/2026"), Glossary (38 fields, Version 1.1 footer, re-verified row by row in `enisa-srp-glossary-baseline.md`), AR User Registration ("Last updated: 08/09/2026") and AR Interface Functions ("Last updated: 07/09/2026") byte for byte; PEC and AR Notification Submission and Update otherwise unchanged apart from the two capture corrections above.

### 2026-09-08 21:06 UTC (vs. 2026-09-08 14:10 UTC)

The AR User Registration guidance page was rewritten a second time in 24 hours, now "Last updated: 08/09/2026" (was 07/09/2026): the placeholder launch URL is filled in, and two new preconditions appear — an explicit MFA requirement, and, for Secondary AR registration, that the Primary AR already be a validated user. All other pages returned HTTP 200 and were re-verified unchanged.

**Changed**

- **AR User Registration** rewritten again, "Last updated: 08/09/2026" (was 07/09/2026). The registration URL is no longer a placeholder: "Open the SRP website (https://portal.cra-srp.enisa.europa.eu)" replaces "(URL to be provided at launch)". Both registration flows now state an explicit precondition "You have an active EU Login account with MFA enabled" (previously only implied via a linked reference). A new note ties CDaC selection to "Article 14(7) of the CRA". The Primary AR's expected result now states explicitly: "The AR may start submitting notifications while validation of the AR–manufacturer association is pending."

**New**

- **Secondary AR registration gains a fourth precondition**: "The Primary AR is a validated user." Not stated anywhere else on these pages — AR Interface Functions' own "Invite Secondary AR" preconditions still ask only for the "AR User Primary" role, not validated status. Worth checking on a future run whether this is enforced or a documentation slip.

**Watch**

- The 07/09 rewrite's wording "an email invitation from SRP triggered by the Primary AR" is gone; the page now reads "a valid SRP email invitation initiated by a Primary AR" — closer to the pre-07/09 phrasing. The invitation-recipient inconsistency with AR Interface Functions (flagged 2026-09-08 04:10 UTC: "An email is sent to the Primary AR, who instructs the Secondary AR...") is untouched either way.

**Editorial**

- New redundant sentence in the Secondary AR steps: "These fields cannot be edited but are retrieved from EU Login and cannot be edited in the SRP." (repeats "cannot be edited" twice). One wording shift in the Primary AR flow: "the SRP will return an error" → "the SRP will display an error". "manufacturer adress" typo still present.

**Unchanged**

Main page, FAQ (Q1–Q30, same tags, Q16 table), CSIRT list (27 countries, "Updated: 04/09/2026"), Glossary (38 fields, Version 1.1 footer, re-verified row by row in `enisa-srp-glossary-baseline.md`), AR Notification Submission and Update (3/08/2026), AR Interface Functions (07/09/2026), and PEC guidance, byte for byte.

### 2026-09-08 14:10 UTC (vs. 2026-09-08 12:18 UTC)

A new page appeared in the "Content" subtopics navigation on the main SRP page and every subpage: **"CRA SRP guidance - Particular Exceptional Circumstances (PEC)"**. All seven previously-tracked pages returned HTTP 200 and were re-verified unchanged; this is a scope-widening discovery, not a content edit to any of them.

**New**

- **CRA SRP guidance - Particular Exceptional Circumstances (PEC)** (`.../cra-srp-guidance-particular-exceptional-circumstances-pec`, HTTP 200), a fourth guidance subpage explaining how an AR flags a submission under PEC: in the 72-hour report template, toggle the "Particular Exceptional Circumstances (PEC)" indicator, which reveals the "PEC Delay Reson" options and an optional justification field for the CDaC. Ties directly to a reporting obligation already covered elsewhere (Q21, the Glossary's v27/v28 fields): PEC may be invoked only under the third subparagraph of Art. 16(2) of the CRA, and doing so sets the dissemination status to "72h Submitted under PEC". No new deadline or field beyond what the Glossary already records — this page documents the UI steps, not new substance. Full content captured below and in the new `guidance_urls[3]`. Not yet listed as a card in the main page's own "User guidance" section, only reachable via the Content navigation, the same way the Glossary and CSIRT list were first found on 2026-09-07.

**Editorial**

- Typo reproduced verbatim: "PEC Delay **Reson**" (for "Reason"), in the sentence "the PEC Delay Reson options will be displayed."

**Watch**

- This widens what the routine tracks (seven pages → eight). Per `CLAUDE.md`, the scheduled prompt itself must be updated to match — done in this same commit at `routines/enisa-srp-pages-monitor.md` — and the live Routine's stored prompt needs a human to apply the same change in the Routines UI (trigger `trig_015C8QiJhXwkxPkDdoMbkHeD`). Because this change touches a file other than the two baselines, this PR is left open rather than auto-merged, per `CLAUDE.md`.

**Unchanged**

Q1–Q30 and the closing note, byte for byte. CSIRT list (27 countries, "Updated: 04/09/2026"). Glossary (38 fields, Version 1.1 footer, unchanged — re-verified row by row in `enisa-srp-glossary-baseline.md`). All three previously-tracked guidance subpages (same "Last updated" dates, same typos) and the main page's own content, apart from the new navigation entry.

### 2026-09-08 12:18 UTC (vs. 2026-09-08 09:10 UTC)

No substantive change; four more Q16 field names lost their capital letters. All seven pages returned HTTP 200.

**Editorial**

Q16 table fields 12–15 (Product Version/Type/Class/Category) are now lowercase "version/type/class/category" — the same capitalisation shift already seen on fields 11 and 19 in this morning's 09:10 UTC check; no status value in the table moved.

**Unchanged**

Q1–Q30 and the closing note, byte for byte. CSIRT list (27 countries, "Updated: 04/09/2026"). Glossary (38 fields, Version 1.1 footer, unchanged — re-verified row by row in `enisa-srp-glossary-baseline.md`). All three guidance subpages (same "Last updated" dates, same typos) and the main page, including the eight now-working Glossary links.

### 2026-09-08 09:10 UTC (vs. 2026-09-08 04:10 UTC)

FAQ page dated forward to "08 September 2026": a new Q30 was added for people who are not manufacturers, and Q27 was reworded with sharper legal citations. All seven pages returned HTTP 200.

**New**

- **Q30** "I am not a manufacturer. How can I report a vulnerability or security issue?" *(tagged [NEW])*: non-manufacturers are told to contact their national CSIRT directly, since the platform currently supports only mandatory manufacturer notifications under Art. 14; ENISA warns such a submission "might be marked as 'invalid' in the SRP" (the page's own sentence, missing its closing full stop, reproduced verbatim). Count 29 → 30.

**Changed**

- **Q27** (now tagged [UPDATED]) rewritten with more precise article citations: "Art. 15 of the CRA" → "Art. 15(1) and (2) of the CRA"; both AEV and SI notifications are now anchored to "Art. 14(3)" specifically (was the general "Articles 14 and 24"); a new sentence states that the open-source software steward obligation under Art. 24(3) applies from 11 December 2027 per Art. 71(2) — a date already known from Q5/Q29 but not previously stated inside Q27 itself.

**Fixed**

- Q16 table row **i39** now reads lowercase "i39." — the capitalised "I39." inconsistency flagged since 2026-09-07 is gone.

**Editorial**

Two Q16 field-name capitalisation shifts (field 11 "Product Name" → "Product name", field 19 "User Action" → "User action"); no status value in the table moved.

**Unchanged**

Q1–Q26, Q28, Q29 and the closing note, byte for byte. CSIRT list (27 countries, "Updated: 04/09/2026"). Glossary (38 fields, Version 1.1 footer, re-verified separately in `enisa-srp-glossary-baseline.md`). All three guidance subpages, including the two "Last updated: 07/09/2026" pages from this morning's rewrite.

### 2026-09-08 04:10 UTC (vs. 2026-09-07 evening)

No FAQ wording change. Two of the three guidance subpages were rewritten, and the FAQ's broken Glossary links now work. All seven tracked pages returned HTTP 200.

**Changed**

- **AR User Registration** and **AR Interface Functions** rewritten, both now "Last updated: 07/09/2026" (were 3/08 and 14/08). A wording and structure pass into "Purpose: Follow these steps to …" narrative. Checked field by field: no deadline, obligation, status name or limit moved — the 20/20/10 figures and the 7-day invitation expiry all stand. Full text below.
- AR User Registration now names the sender of the invitation: "an email invitation from **SRP triggered by** the Primary AR" (was "from the Primary AR").
- **AR Notification Submission and Update** is untouched, still 3/08/2026 and still in the older phrasing.

**Fixed**

- All eight "SRP Glossary" links in the FAQ answers (Q8, Q11 ×3, Q15, Q16 ×2, Q17) now point at `.../cra-srp-glossary2` and resolve. The broken-link defect tracked since 2026-09-07 is closed and no longer flagged.

**Watch**

- **Two ENISA pages now describe two different invitation flows.** AR Interface Functions says the email goes to the *Primary* AR, "who instructs the Secondary AR to complete registration"; AR User Registration still has the Secondary AR clicking a link in their own email. Reads like a slip from the rewrite, but it concerns the registration path — watch it.
- **The Glossary is no longer listed in the "Content" navigation** on any page. It is still linked from the Get Started card and reachable, so nothing is removed from this baseline. Note it if it reappears.

**Editorial**

Three new typos and two stray double full stops across the two rewritten pages, plus "additional **I**nformation" gaining a capital — all reproduced verbatim in the guidance text below.

**Unchanged**

FAQ page ("Updated: 07 September 2026", Q1–Q29) and its Q16 table, byte for byte. Glossary (Version 1.1, 38 fields). CSIRT list ("Updated: 04/09/2026", 27 countries).

### 2026-09-07 evening (vs. the same morning)

Second FAQ pass in five days, and the platform address is published. Page date "Updated: 04 September 2026" → **"07 September 2026"**; all seven pages HTTP 200.

**New**

- **The production URL.** Q9 no longer says the address will follow: "The SRP will be available at https://portal.cra-srp.enisa.europa.eu". First time ENISA names the host — it is one of the 29 already tracked by the SRP domain reachability routine.
- **Q28 "How do I connect to the CRA Single Reporting Platform?"** — the URL, the "Assigned Representative" choice on the landing screen, available from 11 September 2026.
- **Q29 "When do the reporting obligations start?"** — Art. 14 for manufacturers from 11 September 2026, Art. 24(3) for open-source software stewards from 11 December 2027 per Art. 71(2).
- **Q24 gains a first sentence**: "At launch, the platform will be available in **English only**."
- **Q22 names the pre-launch testers** for the first time — national CSIRTs, the CRA Expert Group, selected manufacturers — and states that **no further testing is foreseen before go-live**.

**Changed**

- **Q8: ENISA corrects its own article reference.** Choosing the CSIRT moves from **Article 15(7)** to **Art. 14(7)**; 15(7) does not concern that choice. The answer also points to "User Manuals", a document set not linked anywhere else on these pages.
- **Q18: a new consequence.** "If the wrong CDaC is selected, the notification **may be invalidated and will need to be resubmitted** to the correct CDaC." The identification duty is now put on the manufacturer up front.
- **Q4**: the unfilled placeholder "Art 14 and **24(x)**" is resolved — Art. 24(3), applying 11 December 2027 per Art. 71(2). Voluntary reporting under Art. 15 "will not be available at launch".
- **Q9**: the sentence duplicated verbatim last week is de-duplicated. The one-Primary / 20-Secondary / 20-notifications figures are unchanged.
- **Q26** retitled and rewritten; substance unchanged — the 72-hour counter still runs 48 hours from the Early Warning rather than from awareness, so a notification can show as overdue early.
- **Q16 table**: 43 fields, same numbering, none added or removed. The status legend moved out of its own line and into every cell.
- **Q14**: the doubled "inin" recorded that morning is fixed. Q5 and Q7 make the 11 December 2027 steward date explicit; Q19 corrects "as per Article (14)" to "Art. 14".

**Watch**

- **The eight Glossary links in the FAQ answers are broken**: they point at `.../cra-srp-glossary`, which returns 403. The page moved to `.../cra-srp-glossary2` and the main page's link was updated; the FAQ's were not. Reproduced as they stand.
- **Q21 changes the PEC term** — "In **particularly** exceptional circumstances" → "In **particular** exceptional circumstances" — while the question's own title still says "particularly". The Glossary says "Particular Exceptional Circumstances".
- **`I39.`** is still capitalised in the Q16 table where every other SI row uses a lowercase prefix.

**Editorial**

"Article" is now written "Art." almost throughout, and "24hrs / 72hrs / final report" became "24-hour Early Warning / 72-hour Notification / Final Report", alongside a handful of capitalisation shifts. Three new errors, verbatim below: "72-hour **Sever** Incident Notification" (Q26), "measures that **user** can take" (Q16 field 22), "it explains **that** the field means" (Q16 intro).

**Unchanged**

The three guidance subpages (3/08, 3/08, 14/08/2026) and the CSIRT list ("Updated: 04/09/2026", 27 countries), word for word. The main page apart from its Glossary link, which now points at `.../cra-srp-glossary2`. No new page in the navigation.

### 2026-09-07 morning (vs. 2026-08-31)

The largest change since monitoring began: the FAQ rewritten end to end, and two new pages found through the site navigation. Page date "Updated: 03 August 2026" → **"04 September 2026"**.

**New**

- **CRA SRP Glossary** (Version 1.1, 05/09/2026) — the authoritative field-by-field reference: meaning, how to complete, example, format and per-stage status. Its numbering does **not** match the FAQ's Q16 table: 18 common fields (the five automated ones are not itemised), v19–v29 for AEV, i30–i38 for SI. Full detail in `enisa-srp-glossary-baseline.md`.
- **List of CSIRTs Designated as Coordinators** ("Updated: 04/09/2026") — contact links for the coordinator in each of the 27 Member States. Section below.
- **Three numbered questions**: Q24 languages, Q25 platform unavailable, Q26 counters. A fourth appears **without a number** at the end, tagged [NEW]: "Can I report vulnerabilities even if they are not actively exploited?" — reproduced as-is. Count 23 → 27.
- **A closing note** carrying the helpdesk address `cra-srp-helpdesk[@]enisa.europa.eu` — **moved here from the main page**, where it no longer appears.
- Main page gains a **"Get Started"** heading grouping the Factsheet, the FAQ and a new Glossary card; the "Content" navigation gains both new pages.

**Changed**

- **Every question reworded or expanded.** Q9 is the substantive one: MFA required for EU Login, **one Primary AR and up to 20 Secondary ARs**, and **up to 20 notifications before validation becomes mandatory** — all three numbers new.
- **Q16 restructured and expanded**: common fields 12 → 23, AEV 14 → 11 (two new PEC fields), SI 13 → 9. Total 39 → **43**. The answer now defers to the Glossary and reproduces only the abbreviated table.
- **Q4** gains a go-live scope statement: at launch only mandatory reporting "fulfilling Art 14 and 24(x)", no voluntary reporting under Art. 15.
- The intro no longer refers to "question 10" by number; it links the Commission's "FAQs on the CRA Implementation" directly.

**Watch**

- **Q19 changed but carries no "[UPDATED]" tag**, unlike every other question — an ENISA tagging inconsistency. Its Market Surveillance bullet moved from "Receive disseminated information" to "Receive information from the CSIRT Designated as Coordinator".
- **A sentence is duplicated verbatim in Q9**: "No additional corporate entity authentication mechanism is currently used by the SRP." twice, back to back.

**Editorial**

Two typos reproduced as they stand: "inin particular section 5.4" in Q14, and "manufacturer adress" on the AR User Registration page. On the main page the Factsheet's inline "here" is no longer a hyperlink and the download button points straight at the PDF — same document.

**Unchanged**

The three guidance subpages in substance and date (3/08, 3/08, 14/08/2026), apart from the typo above and a new parenthetical "(please check the URL above)" in the registration pre-conditions.

## Intro

The Cyber Resilience Act (CRA) introduces the Single Reporting Platform (SRP) for cybersecurity incident reporting in the EU Digital Single Market.

The Single Reporting Platform (SRP) shall become a technical tool for the reporting of actively exploited vulnerabilities and incidents impacting products with digital elements in the EU Digital Single Market.

Under the [Cyber Resilience Act](https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng) (CRA), manufacturers of products with digital elements are mandated to report actively exploited vulnerabilities and severe incidents having an impact on the security of the products.

As of 11 September 2026 onwards, the SRP will be used by CSIRTs and manufacturers for mandatory reporting and could be used by any natural/legal persons for voluntary reporting.

Throughout 2025 and 2026, ENISA is taking the necessary steps to support the successful implementation of the platform.

Overall, the CRA brings transparency to the vulnerability disclosure processes and strengthens how EU CSIRTs can mitigate risks stemming from vulnerabilities.

### CRA Single Reporting Platform Factsheet

ENISA has published a factsheet on the CRA Single Reporting Platform. It can be downloaded here, currently in English. ("Download the SRP factsheet" button links directly to `/sites/default/files/2026-07/ENISA_CRA_SRP_Factsheet_v1.0_0.pdf`; the inline "here" text is no longer itself a hyperlink, unlike the previous check.)

### Get Started (new section heading on the main page)

Groups three resource cards: the Factsheet (above), "Frequently asked questions" (→ `faq_url`), and the new "CRA SRP Glossary" ("Consult the fields to be filled in during each stage of notification, their meaning and format" → `glossary_url`).

## FAQ entries

Source: dedicated FAQ subpage (see `faq_url` above). Page-level note: "Updated: 09 September 2026". Intro text on the FAQ page: "All you need to know about the CRA Single Reporting Platform" (subtitle) — "This page provides answers to frequently asked questions about the Cyber Resilience Act Single Reporting Platform (CRA SRP), including its purpose, reporting process, registration and use. The FAQs are updated regularly to reflect the latest available information and guidance as the CRA SRP is implemented. For broader guidance on the interpretation and implementation of the CRA, please also consult the European Commission's "FAQs on the CRA Implementation"."

30 entries (still 30). Q9, Q18, Q22 and Q27 carry an "[UPDATED]" tag on the live page, and Q28, Q29 and Q30 a "[NEW]" tag — but the untagged text changed as well, in earlier checks: see the change log above. **Q8 lost its "[UPDATED]" tag on 2026-09-09** (was tagged since at least 2026-09-08); its text is otherwise unchanged. The per-question tags are recorded in each heading below where present.

**Glossary links fixed 2026-09-08**: all eight "SRP Glossary" links in the answers below now point to `.../cra-srp-glossary2` (see `glossary_url`) and resolve normally. Until this check they pointed at the dead `.../cra-srp-glossary` path (HTTP 403) since at least 2026-09-07; see the change log.

### Q1. What is the Cyber Resilience Act’s Single Reporting Platform (CRA SRP)?

The CRA Single Reporting Platform (SRP) is an online tool for manufacturers and open-source software stewards to meet their obligation to report actively exploited vulnerabilities and severe incidents having an impact on the security of products with digital elements under the Cyber Resilience Act (CRA). Designed to simplify EU reporting obligations, the SRP enables manufacturers and open-source software stewards to report only once, rather than having to notify multiple national authorities individually. The platform incorporates security measures to protect confidentiality.

Manufacturers and open-source software stewards submit notifications electronically through the SRP and select the relevant CSIRT designated as coordinator. In general, the national CSIRT to which the notification should be submitted is primarily determined by the manufacturer’s main location of establishment, in accordance with Art. 14(7) of the CRA.

Once submitted, the notification is simultaneously made available to ENISA, while the CSIRT initially receiving it disseminates the information to other relevant CSIRTs in Member States where the product is also available, and to market surveillance authorities as needed. CSIRTs designated as coordinators may also share some information with their respective market surveillance authorities to enable them to fulfil their enforcement obligations.

### Q2. What is the legal basis for the CRA SRP?

The legal basis for the operation of the SRP is the [Cyber Resilience Act](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847) (CRA), which states in Art. 16(1): For the purposes of the notifications referred to in Art. 14(1) and (3) and Art. 15(1) and (2) and in order to simplify the reporting obligations of manufacturers, a single reporting platform shall be established by ENISA. The day-to-day operations of that single reporting platform shall be managed and maintained by ENISA. The architecture of the single reporting platform shall allow Member States and ENISA to put in place their own electronic notification end-points.

Articles 14-17 of the CRA provide the relevant framework for the reporting and dissemination of notifications. Additionally, in December 2025, the European Commission published a [Delegated Regulation](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=PI_COM:C(2025)8407) specifying the conditions under which the dissemination of notifications may be delayed.

### Q3. Who is responsible for establishing and managing the platform?

ENISA is responsible for establishing the CRA SRP and for managing and maintaining its day-to-day operations. ENISA must also ensure the platform's security and implement appropriate technical and organizational measures to protect the information submitted.

### Q4. When will the Single Reporting Platform be operational?

The platform is scheduled to be operational from 11 September 2026, coinciding with the date on which the CRA reporting obligations under Art.14 become applicable.

At launch, the platform will support only mandatory reporting of actively exploited vulnerabilities and severe incidents under Art. 14 of the CRA. The corresponding reporting obligations for open-source software stewards under Art. 24(3) will apply from 11 December 2027, in accordance with Art. 71(2) of the CRA.

Voluntary reporting under Art. 15 will not be available at launch and will be introduced in a future phase of the platform.

### Q5. What must be reported via the platform?

Under the CRA, manufacturers are required to notify two specific types of events:

- Actively Exploited Vulnerabilities: vulnerabilities in products with digital elements for which there is reliable evidence that they have been exploited by a malicious actor;

- Severe Incidents: incidents having a severe impact on the security of a product with digital elements (e.g., compromising its availability, authenticity, integrity, or confidentiality). The criteria for severity are set out in Art. 14(5).

Open-source software stewards will also be subject to reporting obligations, starting from 11 December 2027, to the extent that they are involved in the deployment of products with digital elements, in accordance with Art. 24(3) of CRA.

### Q6. What else can be reported in the platform?

In a future phase, the SRP will also offer functionality for voluntary notifications.

Any natural or legal person may voluntarily notify:

- Vulnerabilities contained in a product with digital elements;

- Cyber threats that could affect the risk profile of a product with digital elements;

- Incidents having an impact on the security of a product with digital elements;

- Near misses that could have resulted in an incident.

### Q7. What are the deadlines for reporting?

The reporting process starts when a manufacturer or open-source steward becomes aware of an actively exploitation vulnerability or severe incident.

‘Actively exploited vulnerability’ means a vulnerability for which there is reliable evidence that a malicious actor has exploited it in a system without permission of the system owner (CRA definition).

‘Incident having an impact on the security of the product with digital elements’ means an incident that negatively affects (or is capable of negatively affecting) the ability of a product with digital elements to protect the availability, authenticity, integrity or confidentiality of data or functions (CRA definition).

Manufacturers and, once applicable, open-source software stewards must adhere to the following reporting deadlines:

- Early Warning: Without undue delay and in any case within 24 hours of becoming aware of the actively exploited vulnerability or severe incident;

- Actively Exploited Vulnerability/Severe Incident Notification: Without undue delay and in any case within 72 hours of becoming aware, providing general information and an initial assessment;

- Final Report:

- For actively exploited vulnerabilities : No later than 14 days after a corrective measure (e.g., patch) becomes available.

- For severe incidents : Within 1 month after the 72-hour notification.

### Q8. How does the Single Reporting Platform operate? *(no tag on the live page since 2026-09-09; was tagged [UPDATED])*

Manufacturers and open-source software stewards submit notifications electronically through the SRP and select the relevant CSIRT designated as coordinator. Manufacturers and, once applicable, open-source software stewards are responsible for identifying the relevant CSIRT designated as coordinator in accordance with Art. 14(7) of the CRA and submitting their notification accordingly.

Only one notification is required for any given actively exploited vulnerability (AEV) or severe incident (SI), even when a manufacturer has multiple branches or subsidiaries in the EU and/or its parent company is headquartered outside the EU. It is the manufacturer’s responsibility to coordinate internally across its corporate structure and ensure that the required notification is submitted through the SRP.

Once submitted, the notification is simultaneously made available to ENISA, while the CSIRT acting as coordinator disseminates the information without delay to other relevant CSIRTs in Member States where the product is also available. National CSIRTs also share some information with their respective market surveillance authorities to enable them to fulfil their enforcement obligations. Under exceptional circumstances, dissemination of information may be delayed in accordance with Art. 16(2) of the CRA. More detailed information on delayed dissemination is provided in FAQ 21. The platform incorporates security measures to protect confidentiality.

Information on the reporting workflow, the mandatory and optional fields and how to complete them is available in the [SRP Glossary](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2), User Manuals and the regularly updated ENISA guidance materials.

### Q9. How do I access and register on the SRP, and what are the roles of Primary and Secondary ARs? *(retitled 2026-09-09; tagged [UPDATED] on the live page; was "How is the platform accessible and how does the registration process work?")*

The SRP is available at: [https://portal.cra-srp.enisa.europa.eu](https://portal.cra-srp.enisa.europa.eu).

Assigned Representatives (ARs) of manufacturers and, once applicable, open-source software stewards must have an EU Login account with multi-factor authentication (MFA) enabled and use it to register on the SRP. An EU Login account can be created in advance at the following link: [https://ecas.ec.europa.eu/cas/login](https://ecas.ec.europa.eu/cas/login). No additional corporate entity authentication mechanism is currently used by the SRP.

EU Login accounts are personal, and MFA is required to access the platform. Therefore, ARs submitting notifications should use their own EU Login accounts.

A Primary AR can register directly on the SRP by selecting the relevant CSIRT Designated as Coordinator (CDaC), providing the required manufacturer information, and creating the initial association with the manufacturer. A Secondary AR can register on the SRP and be associated with a manufacturer after receiving an invitation from the Primary AR and confirming the pre-filled manufacturer information.

There can be only one Primary AR per manufacturer and up to 20 Secondary ARs. The Primary AR is the main administrative representative for the manufacturer in the SRP and has additional administrative permissions, including managing the manufacturer association and inviting or removing Secondary ARs. **A Primary AR must first have a validated AR–manufacturer association, displayed as "Verified", before inviting Secondary ARs.** *(new 2026-09-09 — formalises on the FAQ page the precondition previously stated only in the AR User Registration guidance's Secondary-AR preconditions, "The Primary AR is a validated user".)* Both Primary and Secondary ARs can submit and update notifications for the manufacturer, subject to their respective access permissions.

**The Primary AR can access all notifications associated with the manufacturer, whereas a Secondary AR can access only the notifications they submitted themselves.** *(new 2026-09-09)* A Secondary AR does not have the same administrative permissions as the Primary AR but may claim the Primary AR role, subject to review and approval by the designated CSIRT.

**ARs can check their current role and manufacturer association status under Settings > Association Management.** *(new 2026-09-09)*

The AR–manufacturer association is validated by the designated CSIRT. The specific validation procedure and processing time may vary between CSIRTs and remain the responsibility of the relevant CSIRT.

Verification takes place in parallel with the reporting process and does not prevent an AR from submitting notifications while validation is pending. *(reworded 2026-09-09 23:11 UTC: "Validation" → "Verification" — only the sentence's first word changed, so it now contradicts itself by ending in "validation is pending"; continues the validation→verification rewording already logged for the neighbouring sentence at 2026-09-09 12:19 UTC, which missed this one.)*

ARs whose manufacturer association has not yet been verified may submit up to 20 notifications for that manufacturer before verification becomes mandatory. *(reworded 2026-09-09 from "Non-validated ARs may submit up to 20 notifications for one manufacturer before validation becomes mandatory" — "validation"/"validated" → "verification"/"verified"; the 20-notification limit itself is unchanged.)*

To limit the validation workload for designated CSIRTs, manufacturers and, once applicable, open-source software stewards are advised to register and initiate the validation process only when they need to submit a notification. Provided that the AR already has an active EU Login account, registration on the SRP takes just a few minutes.

More information on registration, AR roles, and use of the platform is available in the regularly updated ENISA guidance materials.

### Q10. Where can I get further information on the application of the CRA?

To ensure smooth implementation of the CRA, the European Commission has set up [a web page about the reporting obligations](https://digital-strategy.ec.europa.eu/en/policies/cra-reporting), which includes the document “[FAQs on the CRA Implementation](https://ec.europa.eu/newsroom/dae/redirection/document/122331)”. Section 5 provides more details on the reporting obligations under the CRA.

On 27 July 2026, the European Commission also published its [Guidance to support timely Cyber Resilience Act implementation](https://digital-strategy.ec.europa.eu/en/library/commission-publishes-new-guidance-support-timely-cyber-resilience-act-implementation). In particular, Section 9.1 provides detailed guidance on the reporting obligations of manufacturers and open-source software stewards.

ENISA has also published guidance and supporting documents on the use of the CRA SRP, which are available on the main [CRA SRP](https://www.enisa.europa.eu/cra-srp) page and are updated as necessary.

### Q11. How is the term “actively exploited vulnerability” and “severe incidents” interpreted and reported in practice?

The European Commission provides further guidance on the interpretation of actively exploited vulnerabilities (AEVs) and severe incidents (SIs) in Section 5 of its “[FAQs on the CRA Implementation](https://ec.europa.eu/newsroom/dae/redirection/document/122331)”, including in subsection 5.1 – How can a manufacturer become aware of an actively exploited vulnerability or a severe incident? .

For the purposes of reporting through the SRP, an AR must select whether the notification concerns an AEV or a SI having a severe impact on the security of a product with digital elements. The reporting fields then adapt to the selected notification type. The [SRP Glossary](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2) provides practical guidance on the information to be supplied for each type of notification. For AEVs, this includes – where applicable/available – information such as the CVE ID, EUVD ID, general information about the vulnerability and exploitation, severity and impact, malicious actor, general nature of the exploit, and Particular Exceptional Circumstances (PEC). For SIs, the relevant fields include information on the nature of the incident, applied or ongoing mitigation measures, severity and impact, and the threat or root cause likely to have triggered the incident.

Please note that not all the fields are required. Some fields may not be required in the 24-hour Early Warning but become required in the 72-hour Notification or in the Final Report. Refer to the [SRP Glossary](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2) for additional information.

For further details on the legal interpretation of these concepts, please refer to the European Commission’s guidance; for practical guidance on completing the relevant SRP fields, please consult the [SRP Glossary](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2).

### Q12. Do I need to report actively exploited vulnerabilities or severe incidents for products placed on the market before the entry into force of the CRA?

Please refer to the European Commission’s “[FAQs on the CRA Implementation](https://ec.europa.eu/newsroom/dae/redirection/document/122331)”, in particular subsection 5.3 on the reporting obligations under Art. 14, which will apply from 11 September 2026 to all products with digital elements falling within the scope of the CRA, including products that were placed on the market before 11 December 2027.

### Q13. Do I need to report vulnerabilities whose active exploitation occurred before the CRA reporting obligations apply?

The manufacturer’s obligation to report actively exploited vulnerabilities is triggered when the manufacturer becomes aware of them. According to the European Commission’s “[FAQs on the CRA Implementation](https://ec.europa.eu/newsroom/dae/redirection/document/122331)” a manufacturer is not required to retrospectively report an actively exploited vulnerability where it was already aware of the active exploitation before 11 September 2026 (subsections 5.1 & 5.3). However, where the manufacturer becomes aware of the active exploitation after that date, the reporting obligation applies, including where the underlying vulnerability existed or was previously known.

### Q14. If an actively exploited vulnerability in my product originates from a third-party component, am I still required to notify it?

Please refer to the [European Commission’s FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/122331), in particular Section 5.4 on the reporting obligations for actively exploited vulnerability contained in a third-party component.

### Q15. Can the notification workflow be automated for a large number of notifications from one manufacturer?

Organisations may automate their internal reporting workflows and integrate CRA reporting requirements into their own systems and databases. However, no Application Programming Interface (API) will be provided at the initial release of the SRP, so notifications must be submitted through the platform interface. API functionality may be considered in a future phase of the SRP.

Detailed information on the data fields to be completed at each reporting stage is available in FAQ 16 and the [SRP Glossary](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2).

### Q16. What are the data fields to be filled in the reporting template?

The [SRP Glossary](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2) and table provide detailed guidance on all fields available in the platform for both actively exploited vulnerabilities and severe incidents. For each field, it explains what the field means *(typo fixed 2026-09-09 23:11 UTC: was "that" where "what" was meant, since 2026-09-07)*, how it may be completed, the expected format, and at which reporting stage it applies. The Glossary also indicates whether each field is required (stemming directly from CRA obligations or identified by logical consequence), optional , mandatory if the information is available , or carried forward from a previous reporting stage.
Please consult the [SRP Glossary](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2) for the complete and most up-to-date field-by-field guidance.

**Common fields**
1. Notification type (Vulnerability/Incident): Required / copied-or-updated / copied-or-updated
2. Notification level (24hrs/72hrs/Final): Required / Required / Required
3. Reporting time - 24hrs: Automated / Automated / Automated
4. Reporting time - 72hrs: Automated / Automated / Automated
5. Reporting time - Final: Automated / Automated / Automated
6. Reporter: Automated / Automated / Automated
7. Title: Required / copied-or-updated / copied-or-updated
8. Summary: Required / copied-or-updated / copied-or-updated
9. Manufacturer name: Required / copied-or-updated / copied-or-updated
10. Member States where product is available (concerned CSIRT): Required-if-available / copied-or-updated / copied-or-updated
11. Product name *(live page now reads "name", was "Name", new on 2026-09-08)*: Required / copied-or-updated / copied-or-updated
12. Product version *(live page now reads "version", was "Version", new on 2026-09-08)*: Required / copied-or-updated / copied-or-updated
13. Product type (Default/Important/Critical) *(live page now reads "type", was "Type", new on 2026-09-08)*: Optional / copied-or-updated / copied-or-updated
14. Product class *(live page now reads "class", was "Class", new on 2026-09-08)*: Optional / copied-or-updated / copied-or-updated
15. Product category *(live page now reads "category", was "Category", new on 2026-09-08)*: Optional / copied-or-updated / copied-or-updated
16. End of support indicator: Optional / copied-or-updated / copied-or-updated
17. Component name: Optional / copied-or-updated / copied-or-updated
18. Mitigating measure expected shortly: Optional / copied-or-updated / copied-or-updated
19. User action able to reduce impact *(live page now reads "action", was "Action", new on 2026-09-08)*: Optional / copied-or-updated / copied-or-updated
20. Considered sensitivity of information: Optional / Required-if-available / copied-or-updated
21. Corrective or mitigating measures taken: Optional / Required / Required
22. Corrective or mitigating measures that users can take *(typo fixed 2026-09-09 23:11 UTC: was "user", now "users")*: Optional / Required / Required
23. Attack vector: Optional / Optional / Optional

**Actively Exploited Vulnerability (AEV)**
v24. CVE ID: Optional / copied-or-updated / copied-or-updated
v25. EUVD ID: Optional / copied-or-updated / copied-or-updated
v26. General information: Optional / Required / copied-or-updated
v27. Date when corrective or mitigating measure has been available: Optional / Optional / Required
v28. Detailed description of the severity of the vulnerability *(live page now reads "Detailed", was "Full", new 2026-09-09 23:11 UTC — the Glossary's own v23 row for this field still reads "Full", a new FAQ/Glossary mismatch)*: Optional / Optional / Required
v29. Detailed description of the impact of the vulnerability *(live page now reads "Detailed", was "Full", new 2026-09-09 23:11 UTC — the Glossary's own v24 row for this field still reads "Full", a new FAQ/Glossary mismatch)*: Optional / Optional / Required
v30. Date/time when you become aware of the Actively Exploited Vulnerability: Required / copied-or-updated / copied-or-updated
v31. Malicious actor that has exploited / is exploiting the vulnerability: Optional / Optional / Required-if-available
v32. Particular Exceptional Circumstances (PEC): N/A / Optional / N/A
v33. PEC Delay Reason: N/A / Optional / N/A
v34. Please provide further information: Optional / Optional / copied-or-updated

**Severe Incidents (SI)**
i35. Incident is suspected of unlawful or malicious acts: Required / copied-or-updated / copied-or-updated
i36. General information about nature of incident: Optional / Required / copied-or-updated
i37. Applied and ongoing mitigation measures: Optional / Optional / Required
i38. Detailed description of the Severity of the incident: Optional / Optional / Required
i39. Detailed description of the Impact of the incident *(live page now reads lowercase "i39.", fixed 2026-09-08; was capitalised "I39." since at least 2026-09-07)*: Optional / Optional / Required
i40. Type of threat or root cause that is likely to have triggered the incident: Optional / Optional / Required
i41. Date/time when you become aware of the incident: Required / copied-or-updated / copied-or-updated
i42. Date/time when the incident occurred: Optional / Optional / Optional
i43. Initial assessment of the incident: Optional / Required / copied-or-updated

### Q17. What guidance material is available for the relevant parties?

ENISA recognises the need to ensure that manufacturers, open-source software stewards, Assigned Representatives and other relevant reporting teams have clear and practical information to prepare for and use the CRA SRP. ENISA has published a range of supporting materials, including the SRP Factsheet, FAQs, and SRP Glossary. Additional operational materials, including a user manual and tutorial videos, will be published at the launch of the platform. These materials will be updated and expanded as necessary.

The [SRP Glossary](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2) provides detailed field-by-field guidance, including what each field means, how it may be completed, the expected format, and at which reporting stage it applies.

### Q18. How do I know which national CSIRT I should report to through the CRA SRP? *(tagged [UPDATED] on the live page)*

Manufacturers and, once applicable, open-source software stewards are responsible for identifying the correct CSIRT designated as coordinator (CDaC) in accordance with Art. 14(7) of the CRA and selecting it when submitting a notification through the SRP. If the wrong CDaC is selected, the notification may be invalidated and will need to be resubmitted to the correct CDaC.

In general, you should report to the CDaC in the Member State of your main establishment in the EU. Under the CRA, the main establishment is the place where decisions related to the cybersecurity of your products with digital elements are predominantly taken.

If this cannot be determined, use the Member State where your establishment with the highest number of employees in the EU is located.

If you do not have a main establishment in the EU, determine the relevant Member State using the following order, based on the information available:

- the Member State where your authorised representative acts on your behalf for the highest number of products with digital elements;

- if this does not apply, the Member State where the importer places the highest number of your products with digital elements on the market;

- if this does not apply, the Member State where the distributor makes the highest number of your products with digital elements available on the market;

- if none of the above applies, the Member State with the highest number of users of your products with digital elements.

You should then select the corresponding CDaC when submitting your notification through the SRP.

### Q19. What are the responsibilities of key entities involved with the CRA SRP?

- Manufacturers : Submit timely notifications and comply with the other obligations established by the CRA, as per Art. 14;

- Open-source software stewards : Submit timely notifications to the extent that they are involved with products with digital elements, as per Art. 24(3);

- ENISA : Manages the platform, processes reports, prepares biennial trend reports (first due within 24 months of the reporting obligations starting), operates a helpdesk (especially for SMEs), and discloses fixed vulnerabilities to the European Vulnerability Database (EUVD);

- CSIRTs Designated as Coordinators : Receive and assess reports, decide on dissemination delays, inform market surveillance authorities and the public, if necessary, and provide helpdesk support alongside ENISA;

- European Commission : Adopts delegated and implementing acts (e.g., for delay criteria and report formats), evaluates the platform's effectiveness, and supports coordination of enforcement activities;

- Market Surveillance Authorities : Receive information from the CSIRT designated as coordinator and enforce compliance, such as through investigations or corrective actions.

### Q20. Who receives the reports submitted through the platform?

As a general rule, when a manufacturer submits a notification through the CRA SRP, it is simultaneously made available to:

- The CSIRT (Computer Security Incident Response Team) designated as coordinator in the relevant Member State; and

- ENISA (unless particularly exceptional circumstances apply).

The CSIRT designated as coordinator that initially receives the notification is then responsible for disseminating it without delay to other relevant CSIRTs across the EU via the platform.

### Q21. Can the dissemination of a report be delayed or withheld? What are the particularly exceptional circumstances?

Yes. In particular exceptional circumstances (PEC) , the receiving CSIRT may delay or withhold the dissemination of a notification to other Member States, including at the request of the manufacturer or open-source software steward.

The European Commission adopted a [Delegated Act](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=PI_COM:C(2025)8407%20) on 11 December 2025 to further specify the terms and conditions for applying these grounds.

During the first 72-hour window, you should assess, where applicable, whether PEC applies. PEC may be invoked only where at least one of the conditions under Art. 16(2) of the CRA is met. It is intended for exceptional situations in which the dissemination of information may need to be delayed to avoid security-related risks.

Where PEC is invoked in the 72-hour Notification, ENISA will not receive the full content of the notification immediately. This applies only where the manufacturer actively marks that at least one of the conditions listed in points (a) to (c) of Art. 16(2) applies. In such a case, ENISA receives only partial information until the receiving CSIRT makes the full notification available.

### Q22. How does the platform ensure security? *(tagged [UPDATED] on the live page)*

ENISA is legally required to take appropriate technical and organisational measures to manage risks to the platform's security and must notify the CSIRTs Network and the European Commission of any security incidents affecting the platform itself.

Before launch, the platform underwent several user, security and technical testing exercises with selected stakeholders, including national CSIRTs, the CRA Expert Group, selected manufacturers and other users. Their feedback helped strengthen the platform’s functionality, security and usability. ENISA does not currently foresee additional testing before go-live.

The platform will also be periodically reviewed and re-tested as necessary after launch.

### Q23. How was the CSIRTs Network involved?

As provided for in Art. 16 of the CRA, ENISA has engaged the CSIRTs Network in the development and testing of the CRA SRP. Various CSIRTs participated in user, security and technical testing, providing valuable feedback on the functioning of the platform.

### Q24. In which languages will the SRP be available?

At launch, the platform will be available in English only.

ENISA will progressively translate the Factsheet and other supporting materials into all EU languages. This availability of additional language versions of the platform itself will be reviewed in the next phase of the project.

### Q25. What should I do if the SRP is temporarily unavailable?

Manufacturers must fulfil their reporting obligations by submitting notifications through the Single Reporting Platform (SRP), in accordance with Article 14(7). If the SRP is temporarily unavailable, manufacturers should wait until it becomes available again and then submit the required notification.

If, in the meantime, manufacturers consider that immediate communication is necessary before the SRP is restored, they may contact their designated CSIRT directly. Please note, however, that even where the CSIRT has been contacted directly, the notification must still be submitted through the SRP once it is available again in accordance with the CRA.

The same applies to open-source software stewards.

### Q26. How are the 72-hour and Final Report counters calculated?

To help Assigned Representatives (ARs) of manufacturers and, once applicable, open-source software stewards prioritise and keep track of their reporting obligations, the platform implements a number of counters.

The counters for the 72-hour Notification and Final Report are used as a reference for sending reminder emails and displaying alerts that a report may be overdue.

These counters are intended to provide visibility but do not replace the responsibility of manufacturers and open-source software stewards to comply with the obligations laid down in CRA, including the requirement to report upon becoming aware, without undue delay and in any event within the timelines set out in Art. 14.

- 72-hour counter : In the current release, the 72-hour counter displays a due date/time 48hrs after submission of the 24-hour Early Warning. As a result, in some cases, a notification may be displayed as overdue before 72 hours have elapsed since the manufacturer or open-source software steward became aware of the event. This logic will be updated in a future release to calculate the deadline using the "Date/Time when you became aware of the incident/actively exploited vulnerability" field for both AEVs and SIs.

- Final Report : The Final Report deadline is calculated differently for AEVs and SIs, reflecting the different requirements under Art. 14. For AEVs, no counter is currently implemented, as the Final Report deadline depends on the date and time when a corrective or mitigating measure becomes available. For SIs, the counter displays a due date one month after submission of the 72-hour Severe Incident Notification *(typo fixed 2026-09-10 01:08 UTC — was "Sever Incident Notification" since at least 2026-09-07)*.

### Q27. Can I report vulnerabilities even if they are not actively exploited? *(tagged [UPDATED] on the live page since 2026-09-08; previously untagged)*

The platform has not yet implemented the voluntary reporting functionality provided for under Art. 15(1) and (2) of the CRA. As such, only mandatory notifications concerning actively exploited vulnerabilities (AEVs) under Art. 14(3) and severe incidents (SIs) having an impact on the security of products with digital elements under Art. 14(3) can currently be submitted through the SRP.

The corresponding reporting obligations for open-source software stewards, set out in Art. 24(3) of the CRA, will apply from 11 December 2027, in accordance with Art. 71(2).

The platform will be enhanced at a later stage to support voluntary reporting under Art.15.

### Q28. How do I connect to the CRA Single Reporting Platform? *(tagged [NEW] on the live page)*

The SRP will be available at [https://portal.cra-srp.enisa.europa.eu](https://portal.cra-srp.enisa.europa.eu).

From there, select "Assigned Representative" and log in using your EU Login account.

The portal will be available from 11 September 2026.

### Q29. When do the reporting obligations start? *(tagged [NEW] on the live page)*

The CRA reporting obligations under Art. 14 apply to manufacturers of products with digital elements from 11 September 2026.

In accordance with Art. 71(2) of the CRA, the reporting obligations for open-source software stewards under Art. 24(3) apply from 11 December 2027.

Mandatory notifications must be submitted through the CRA Single Reporting Platform. See FAQ 25 for information on what to do if the platform is temporarily unavailable.

### Q30. I am not a manufacturer. How can I report a vulnerability or security issue? *(new question, tagged [NEW] on the live page, added 2026-09-08)*

The current version of the platform supports only mandatory notifications submitted by manufacturers under Art. 14 of the CRA. If you are not a manufacturer and would like to report a vulnerability or other security issue, please contact the relevant national CSIRT directly. Your submission might be marked as 'invalid' in the SRP *(sentence ends without a full stop on the live page, reproduced verbatim)*.

### Closing note (end of FAQ page)

"Did you not find the answer to your question above? For matters not covered in the FAQs, nor in the available supporting materials, please contact: cra-srp-helpdesk[@]enisa.europa.eu" — reworded on 2026-09-07 (was "You did not find above the answer to your question? For matters not covered by this FAQ, nor by available guidance pages, …"), and "available supporting materials" is now a link.


## Guidance documents (User guidance section, on the main SRP page)

- "CRA SRP - AR User registration" — Updated: 3/08/2026. "This page provides information on the Assigned Representatives (AR) user registration in the SRP. It is intended for AR users (Primary and Secondary)."
- "CRA SRP - AR Notification submission and update" — Updated: 3/08/2026. "This page provides information on the Assigned Representatives (AR) submission and update of notifications in the SRP. It is intended for AR users (Primary and Secondary)."
- "CRA SRP - AR Interface functions" — Updated: 14/08/2026. "This page explains the AR's interface of the SRP for various functions that can be performed."

**Stale as of 2026-09-08**: this main-page card list still shows the pre-rewrite dates (3/08/2026, 14/08/2026) for the AR User Registration and AR Interface Functions cards, even though those two subpages themselves now say "Last updated: 07/09/2026" (see the "Guidance subpages — full content baseline" section and the change log). The main page's own card text was not refreshed to match; reproduced here as it stands, not corrected.

The support-contact line previously listed here (cra-srp-helpdesk[@]enisa.europa.eu) has moved to the bottom of the FAQ page — see "Closing note" above.

## CRA SRP Glossary (new page, `glossary_url`)

Version 1.1, last update: 05/09/2026 — **the page footer still says this on 2026-09-07, although the page content was edited that day** (see the change log in `enisa-srp-glossary-baseline.md`): the version stamp is not a reliable change signal for this page. The authoritative field-by-field reference for the reporting template: for each field it gives the meaning, how to complete it, a worked example, the expected format, and its per-stage status (Early Warning 24h / 72h / Final Report). Its own field numbering differs from the FAQ's Q16 table — it does not itemize the 5 automated/system common fields (Notification level, the three Reporting-time fields, Reporter) that Q16 lists explicitly, so its common-field numbering runs 1–18 instead of 1–23; the AEV and SI fields (same substance as Q16's v24–v34 and i35–i43) are renumbered v19–v29 and i30–i38 respectively.

**Scope note**: only field names, applies-to (Both/AEV/SI), and per-stage status are captured below, not the full descriptive text (meaning/how-to-complete/example/format) for each field — that level of detail lives in the dedicated **`enisa-srp-glossary-baseline.md`** file (added 2026-09-07, when the live Glossary page began returning HTTP 403 on its original path — it had moved, see `glossary_url`), which is the full-detail historical record and the one to diff against for wording-level changes. A future check should re-verify field names, counts, and statuses against this list, and flag if the page's own numbering or the field set changes.

Common fields (1–18, "Both" AEV/SI): 1 Notification type, 2 Title, 3 Summary, 4 Manufacturer name, 5 Member States where product available (Concerned CSIRT), 6 Product Name, 7 Product version, 8 Product Type (Default/Important/Critical), 9 Product Class, 10 Product Category, 11 End of support indicator, 12 Component name, 13 Mitigating measure expected shortly, 14 User Action able to reduce impact, 15 Considered sensitivity of information, 16 Corrective or mitigating measures taken, 17 Corrective or mitigating measures users can take, 18 Attack vector.

AEV fields (v19–v29): v19 CVE ID, v20 EUVD ID, v21 General information, v22 Date when corrective or mitigating measure has been available, v23 Full description of the severity of the vulnerability, v24 Full description of the impact of the vulnerability, v25 Date/time when you become aware of the Actively Exploited Vulnerability [1], v26 Malicious actor that has exploited/is exploiting the vulnerability, v27 Particular Exceptional Circumstances (PEC), v28 PEC Delay Reason, v29 Please provide further information.

SI fields (i30–i38): i30 Incident is suspected of unlawful or malicious acts, i31 General information about nature of incident, i32 Applied or ongoing mitigation measures, i33 Detailed description of the Severity of the incident, i34 Detailed description of the Impact of the incident, i35 Type of Threat or root cause likely to have triggered incident, i36 Date/time when you become aware of the incident [2], i37 Date/time incident occurred, i38 Initial assessment of the incident.

Footnotes on the page: [1] "This field will be available in the next release of the Platform." [2] "In the current release this field is named: 'Date/time the incident was detected'."

## List of CSIRTs Designated as Coordinators (new page, `csirt_list_url`)

"Updated: 04/09/2026". Page note: "This list provides the contacts of EU CSIRTs Designated as Coordinators, in the meaning of the Cyber Resilience Act (CRA)." *(reads "of EU" 2026-09-09 23:11 UTC; this file had recorded "to the" since first capture on 2026-09-07, but no intervening check re-quoted the sentence — only ever noting "27 countries, same links, Updated stamp" — so it is not certain this wording changed today rather than being missed earlier.)* One entry per EU Member State (27 total), each with one or more contact links:

- Austria: https://www.cert.at/de/ueber-uns/kontakt/ ; https://www.cert.at/en/about-us/contact/
- Belgium: https://ccb.belgium.be/contacts
- Bulgaria: https://www.govcert.bg/en/contact-us/
- Croatia: https://www.cert.hr/en/home-page/
- Cyprus: https://www.csirt.cy/en/contact-us
- Czechia: https://nukib.gov.cz/cs/kontakty/
- Denmark: https://www.fe-ddis.dk/da/arbejdsomrade-a/Cybertruslen/
- Estonia: https://www.ria.ee/en/cyber-security/handling-cyber-incidents-cert-ee
- Finland: https://www.kyberturvallisuuskeskus.fi/en/contact-us/contact
- France: https://www.cert.ssi.gouv.fr/contact-us/
- Germany: https://www.bsi.bund.de/CERT-Bund/ ; https://www.bsi.bund.de/EN/CERT-Bund/
- Greece: https://cyber.gov.gr/el-csirt/
- Hungary: https://ncsc.gov.hu
- Ireland: https://www.ncsc.gov.ie/cra/
- Italy: https://www.acn.gov.it/portale/csirt-italia/chi-siamo
- Latvia: https://cert.lv/uploads/par-mums/RFC_2350_CERT-LV_21072025.pdf
- Lithuania: https://www.nksc.lt/kontaktai.html
- Luxembourg: https://www.circl.lu/pub/coordinated-vulnerability-disclosure/
- Malta: http://www.mita.gov.mt
- Netherlands: https://www.ncsc.nl/contact
- Poland: https://cert.pl/en/cvd/
- Portugal: https://www.cncs.gov.pt/pt/certpt/rfc-2350
- Romania: https://www.dnsc.ro/contact
- Slovakia: http://www.sk-cert.sk
- Slovenia: https://www.cert.si/en/about-si-cert/
- Spain: for incidents — https://www.incibe.es/incibe-cert/incidentes/respuesta-incidentes and https://www.incibe.es/en/incibe-cert/incidents/incident-handling ; for vulnerability coordination — https://www.incibe.es/incibe-cert/alerta-temprana/vulnerabilidades/asignacion-publicacion-cve and https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/cve-assignment-publication
- Sweden: https://cert.se/rapportera/

## Guidance subpages — full content baseline

The four guidance documents above are separate subpages (URLs in `guidance_urls` in the frontmatter). The first three carry a disclaimer of the form "The information on this page is provided according to our current best knowledge and may be subject to change. Please ensure [that] you consult the latest available guidance before applying these instructions." (the "that" is present on two of the three — AR User Registration and AR Notification Submission and Update — and absent on AR Interface Functions; a pre-existing wording difference, not a detected change). The fourth, PEC, carries the same disclaimer without "that", plus an additional access-precondition note not present on the other three (see below). All four have now been rewritten into a second-person "Follow these steps…" style with numbered steps and screenshots (AR Notification Submission and Update was the last to receive this treatment, on 2026-09-09 22:12 UTC). **As of 2026-09-09 22:12 UTC**: AR User Registration shows "Last updated: 09/09/2026"; AR Notification Submission and Update shows "Last updated: 03 September 2026" (its first move since 2026-09-02); AR Interface Functions shows "Last updated: 09/09/2026" (unmoved since 21:07 UTC despite a further same-day rewrite); PEC shows "Last updated: 09 September 2026" — its first date stamp ever, gained this run. None of the four stamps is a reliable change signal; diff the text on every check.

### Guidance: CRA SRP - AR User registration
URL: see `guidance_urls`. Page note: "Last updated: 09/09/2026" *(unmoved since the 2026-09-09 22:12 UTC rewrite, despite the wording change below).*

This page provides information on the Assigned Representative (AR) user registration in the SRP. It is intended for AR users (Primary and Secondary). *(singular "Representative", new 2026-09-10 00:10 UTC — was "Representatives"; the main page's own "User guidance" card blurb for this page still reads "Representatives", plural, so the two now disagree.)*

**General Notes** (unchanged this pass): AR users authenticate through EU Login when registering on the SRP. Authentication steps carried out within EU Login are not described here. Further information on EU Login is available through the official EU Login guidance at: https://trusted-digital-identity.europa.eu/index_en. An EU Login account with multi-factor authentication (MFA) is needed in order to access the platform. ARs that have already an EU Login account with no MFA enabled should enable MFA before their first access to the platform *(grammar as on the live page — "ARs that have already", reproduced verbatim; was "ARs who already have")*. Validation by the CSIRT Designated as Coordinator (CDaC) of whether an AR is authorised to submit notifications on behalf of a specific manufacturer takes place after registration (described below) and is not a prerequisite for submitting a notification. Validation takes place after the first access to the platform, in parallel with the reporting process, and will not affect the ability to submit notifications through the SRP. Specific validation procedures may vary between CSIRTs and remain the responsibility of the relevant CSIRT. Manufacturers and open-source stewards are advised to register and initiate the validation process only when they need to submit a specific notification, rather than registering pre-emptively.

**Register as a Primary AR & associate with a manufacturer** *(section retitled in the 2026-09-09 22:12 UTC rewrite; was "Registration as Primary Assigned Representative & AR Association with a Manufacturer via 'Registration Flow'")*
Follow this procedure to register on the SRP as a Primary Assigned Representative (Primary AR) and create an association with a manufacturer.
- Pre-conditions: You are not already registered as an SRP user; you have an active EU Login account with MFA enabled.
- Steps: Open the SRP website (https://portal.cra-srp.enisa.europa.eu), select your AR role, and click "Continue" *(the parenthetical UI hint — "hovering over the 'i' icon shows information about each role" — is gone in this rewrite)* → select the CSIRT Designated as Coordinator (CDaC) from the drop-down menu and click "Continue" (note: "The manufacturer is responsible for identifying the correct CDaC in accordance with Article 14(7) of the CRA.") → authenticate through EU Login → read and accept the legal agreement → review and confirm your pre-filled personal details **(First Name, Last Name, Email)**, then click "Continue" ("These fields are retrieved from EU Login and cannot be edited in the SRP.") → enter the manufacturer details (manufacturer name, manufacturer **address** *(the long-tracked "adress" typo is fixed in this rewrite)*, additional information) and click "Continue". Exceptions: "If required manufacturer information is missing, such as Manufacturer Name, the SRP displays an error and the 'Continue' button remains disabled." *(reworded from "If you omit mandatory manufacturer details (manufacturer name, additional Information), the SRP will display an error…" — drops "additional Information" as a named required field, now gives one example only.)*
- Expected result: "Registration is completed and the user account becomes 'Active' with the 'AR Primary User' role. The manufacturer entity is created in the SRP based on the information provided, and the AR-manufacturer association is submitted for validation by the CSIRT. The system sends a confirmation email to the user. The AR may start submitting notifications while validation of the AR–manufacturer association is pending." *(unchanged in substance; "Your registration" → "Registration".)*

**Watch**: this flow's personal-details list now reads (First Name, Last Name, Email) — three fields, no longer four. The Secondary AR flow below still lists a fourth field, "Legal name", for the same confirm-details step. Whether this is deliberate (Legal name applies only to Secondary AR) or a new capture gap in ENISA's own rewrite cannot be told from this run alone.

**Registration as a Secondary AR via Invitation** *(retitled from "Registration via Invitation (Secondary AR)")*
Follow this procedure to register on the SRP as a Secondary AR using an email invitation sent by the Primary AR.
- Pre-conditions: You are not already registered as an SRP user; you have an active EU Login account with MFA enabled; you have received a valid SRP email invitation initiated by a Primary AR; and **"The feature to invite a Secondary AR is available only to a 'Verified' Primary AR."** *(reworded in this rewrite from "The Primary AR is a validated user" — now uses the same "Verified" term as Q9 and AR Interface Functions' own "Invite Secondary AR" precondition, closing the terminology gap flagged since 2026-09-08 21:06 UTC.)*
- Steps: "Click the link in the email invitation. You will be prompted to authenticate through EU Login, which completes the authentication successfully." Exceptions: "If the invitation link has expired because more than 7 days have passed since the SRP sent the invitation, you will be redirected to a page displaying an error message." *(causal "because" replaces the parenthetical, no meaning change)* → Review and confirm the accuracy of your pre-filled personal details (First Name, Last Name, Email, Legal name) and click "Continue". **"These fields are retrieved from EU Login and cannot be edited in the SRP."** *(the previously-tracked redundant/self-contradictory phrasing — "These fields cannot be edited but are retrieved from EU Login and cannot be edited in the SRP" — is fixed in this rewrite.)* → Review and confirm the accuracy of the pre-filled manufacturer details for the manufacturer associated with the Primary AR who initiated the invitation and click "Accept invitation".
- Expected result: "Registration is completed and you become a Secondary AR for the relevant manufacturer. Your system role is displayed as 'AR Backup User' and your status is set to 'Active'. If registration is not completed within 7 days of the invitation being sent, the invitation expires and the user status becomes 'Invitation Expired' in the SRP." *(reworded; same substance — still 7 days, same role/status names.)*

### Guidance: CRA SRP - AR Notification submission and update
URL: see `guidance_urls`. Page note: "Last updated: 03 September 2026" *(moved for the first time since 2026-09-02, in the 2026-09-09 22:12 UTC rewrite that also restyled the page — see change log; was "3/08/2026")*.

This page provides information on the Assigned Representatives (AR) submission and update of notifications in the SRP. It is intended for AR users (Primary and Secondary/Backup).

*Rewritten into the second-person "Follow these steps…" style already used on the other guidance pages, with numbered steps and screenshots. Substance below is unchanged from the prior capture except where noted.*

**Submit a New Notification**
Purpose: Follow these steps to submit a new notification for an Actively Exploited Vulnerability (AEV) or a Severe Incident (SI), to inform the relevant users of the CSIRT Designated as Coordinator (CDaC) so they can review, disseminate and further process it. Pre-conditions: user status "Active", logged in, Dashboard opened.

- *Submit an Early Warning*: Click "Submit new notification" (auto-created, pre-filled with user type AR) → fill mandatory/optional fields under the Early Warning tab → select an existing manufacturer (approved or pending validation) or add a new one → submit or save as draft → optionally fill Additional Notes → notification listed on the Dashboard. Exception: omitting mandatory data returns an error naming the missing data.
- *Submit a 72-hour Notification*: Pre-conditions: status "Active", logged in, Dashboard open, an Early Warning already submitted. Steps: click an existing notification on the Dashboard → fill mandatory/optional fields under the 72-hour Notification tab → submit or save as draft → notification listed on the Dashboard, subject to CSIRT validation. Exception: omitting mandatory data returns an error.
- *Submit a Final Report*: Pre-conditions: status "Active", logged in, Dashboard open, an Early Warning and a 72-hour Notification already submitted. Steps: click an existing notification → fill mandatory/optional fields under the Final Report tab → submit the Final Report or save as draft. Exception: omitting mandatory data returns an error.
- *Expected results*: Draft — saved notification state becomes "Draft", visible only to the author. Early Warning — stored and accessible to the CDaC and ENISA; email/alert sent to the CDaC, to the submitter and all other ARs of the selected manufacturer, and automatically to ENISA; state becomes "Early Warning"; other concerned CSIRTs receive it only after manual dissemination by the CDaC. 72-hour Notification — state becomes "72h Submitted" (or "72h Submitted under PEC" if a notification is "subject to Particularly **Exception** Circumstances (PEC)" *(typo still present on the live page after the rewrite — "Exceptional" missing its "-al", reproduced verbatim; occurs three times in this section)*); email/alert sent to the CDaC, submitter, other ARs, and to ENISA automatically only when PEC has not been invoked; other CSIRTs receive it only after manual CDaC dissemination. Final Report — state becomes "FR Submitted" (sub-state "Final Report"); ENISA receives it automatically only when Particularly Exception Circumstances has not been invoked; other CSIRTs receive it only after manual CDaC dissemination.

**Update an Existing Notification**
Purpose: Follow these steps to update an existing notification for an AEV or SI. Pre-conditions: status "Active" and logged in; a notification has been previously submitted or saved as draft; notification is not closed (closed notifications cannot be updated); the Final Report is not submitted (the notification becomes non-editable after Final Report submission). Steps: open a notification and update the necessary fields under the Notification tab → click "Update" to save. Exception: omitting mandatory data on "Update" returns an error. The SRP automatically notifies the CDaC via alert and email, and automatically notifies ENISA and any concerned CSIRTs that previously received the notification through dissemination, via alert and email.

### Guidance: CRA SRP - AR Interface functions
URL: see `guidance_urls`. Page note: "Last updated: 09/09/2026" *(unchanged from the 21:07 UTC rewrite, even though the page was rewritten a second time today — see change log; the stamp does not move on every edit)*.

This section explains the AR interface of the SRP for various functions that can be performed. Note: AR users can access the Dashboard only after successfully logging in and while their SRP user status is "Active", subject to applicable role and association restrictions.

- **View Personal and Update Manufacturer Details through Settings**: Pre-conditions: status "Active", logged in. Steps: open the Dashboard, click your profile name → profile drop-down opens → click Settings → view personal details or update manufacturer details using the same steps as the registration flow (now split into separate "Personal details"/"Manufacturer details" screenshots).
- **Invite Secondary AR (Primary AR only)**: Purpose: as Primary AR, invite a Secondary AR for the same manufacturer. Pre-conditions: status "Active", logged in; you hold the Primary AR role for the relevant manufacturer; and **"Your AR-manufacturer association has been validated by the CSIRT Designated as Coordinator (CDaC) and is displayed as 'Verified'."** *(new precondition in this rewrite — previously only the role was required; the "invitee's email not already registered" precondition from the prior capture is no longer listed.)* Steps: in Settings, select the option to add a Secondary AR ("Invite Backup") for the manufacturer you represent (note repeats the verified-association precondition) → enter the email address the prospective Secondary AR uses to register on EU Login and click "Send Invitation". Expected result: **"The SRP sends an email invitation to the Secondary AR. A new user record is created in the SRP with the specified email address and corresponding manufacturer details. The user role is assigned once the registration is completed."** *(Fixes the long-tracked bug: the email invitation is now correctly said to go to the Secondary AR, not the Primary AR — was "An email is sent to the Primary AR, which instructs the Secondary AR to complete registration." The "Pending Invitation" status name is no longer mentioned.)*
- **Add Additional Manufacturer Association via Settings** *(retitled from "Add an Association with an Additional Manufacturer through Settings")*: Pre-conditions: status "Active", logged in. Steps: Dashboard → profile menu → Settings → "Association Management" → "Add Manufacturer" → enter required details for the new manufacturer → "Save". A pop-up confirms creation. Exceptions: "If required manufacturer details are missing, such as Manufacturer Name, the SRP displays an error and the 'Continue' or 'Save Edit' button remains disabled." *(adds the "Save Edit" button case; drops the two-item enumeration for a single example, same pattern as the User Registration rewrite.)* Expected result: the manufacturer record and the AR association are created with status "Unverified"; a request to verify goes to the CDaC for validation; a confirmation email is sent. **"As an 'Unverified' AR, you can submit up to 20 notifications."** *(Corrected from "only up to 10 notifications" — reconciles this page's own number with Q9's "up to 20 notifications" limit, which this page had disagreed with since first capture.)*
- **Claim Primary AR Role as a Secondary AR**: Purpose: "Follow these steps, as a Secondary AR, to request to the Primary AR role for a manufacturer." *(new grammar defect in this rewrite — a word appears to be missing, e.g. "to become"; was "…to request to become a Primary AR.")* Pre-conditions: you are a Secondary AR associated with the relevant manufacturer; status "Active", logged in. Steps: Dashboard → profile menu → Settings → select the option to claim the Primary AR role for the relevant manufacturer. A pop-up confirms the request. Expected result: "The request is created and submitted to the designated CDaC for review and approval. **The Secondary AR remains in the existing role until the request is approved.**" *(closing sentence new — states explicitly what was previously only implied.)*
- **Delete AR – Manufacturer Association**: Purpose: manage the association between AR users and manufacturers, including removal of your own association or, where applicable, a Secondary AR's. Pre-conditions: status "Active", logged in; valid EU Login account able to authenticate; the AR–manufacturer association has been "Verified". Steps: open the AR Association Management page (a Primary AR can remove their own association or a Secondary AR's for the manufacturer; a Secondary AR can remove only their own) → click **"Delete Association"** and confirm the action. *(Button renamed from "Remove Association" in this rewrite.)* Expected result: "The system removes the selected AR association, and its status is updated to 'Deleted'." *(unchanged in substance.)*
- **Dashboard**: Purpose: use the Dashboard to view accessible notifications, search, sort and filter records, and open notification details. "You can access the Dashboard by:" opening it directly via a valid URL after login; accessing the Dashboard URL while logged in; or **"selecting a Notification Alert, where available."** *(third access route, new in this rewrite — was just "opening it directly via a valid URL, or clicking on the Dashboard button".)* Pre-condition: status "Active", logged in.
  - *View the Dashboard*: "A Primary AR can access all notifications associated with their manufacturer, whereas a Secondary AR can only access notifications they submitted and drafts they created. Secondary ARs cannot view notifications submitted by another AR associated with the same manufacturer." *(reworded with explicit Primary/Secondary role split, echoing Q9's own wording; substance unchanged from the prior "only your own draft notifications are shown" capture.)*
  - *Search, Sort & Filter Notifications*: Pre-conditions: status "Active", logged in, at least one notification previously submitted/saved as draft. Search by Notification ID, Manufacturer, or Title. Sort by Title (alphabetical) or Last Update (chronological). Filter via "All filters" by Member States where the product with digital elements is available and Type of submission. **"You can select the appropriate tab to focus on notifications with a pending action label."** *(the named "Action Required" tab is no longer named — a specific UI label has been generalised away.)* "Clear all filters" removes all applied filters. Exception: no matching results found → the system informs you no notifications match the search criteria. Expected result: "The results are filtered and/or sorted based on your selections."
  - *View Notification Details*: click a notification to view its details. Expected result: "you can view the notification details." *(new explicit expected-result line, not previously stated.)*
- **View Alerts**: Purpose: review alerts generated by the system. Pre-conditions: registered as a user in the SRP; valid EU Login account able to authenticate. Steps: open the Alerts tab. Alerts are triggered by an action requiring AR attention; **"blue"** = unread *(was "light blue")*, turns grey ("read") once opened; red alerts appear only for exceptional/critical actions (e.g., a designated CSIRT has invalidated a submission). Expected result: the selected alert is marked "Read" and its details can be reviewed.

### Guidance: CRA SRP guidance - Particular Exceptional Circumstances (PEC)
URL: see `guidance_urls[3]`. First captured 2026-09-08 14:10 UTC, discovered via the site's own "Content" navigation (not yet listed as a card in the main page's "User guidance" section). **Page note: "Last updated: 09 September 2026"** — its first date stamp ever, gained in the 2026-09-09 22:12 UTC check, after weeks (and two rewordings on 2026-09-09 alone, at 12:19 and 21:07 UTC) with no date at all.

This section explains to ARs how and when to apply one of the three cases of Particularly Exceptional Circumstances (PEC), as described in the third subparagraph of Article 16(2) of the CRA — this opening sentence still spells the term "Particularly". Disclaimer: "The information on this page is provided according to our current best knowledge and may be subject to change. Please ensure you consult the latest available guidance and related legislation, before applying these instructions." Note: "AR users can access the SRP Dashboard only after successfully logging in and while their SRP user status is 'Active', subject to applicable role and association restrictions."

*No `<h3>`/`<h4>` headings on the live page at any point — this file's own "Flagging a submission" / "Effect" labels below are this baseline's summarising labels, not page headings, and are kept only to structure the diff.*

Particular Exceptional Circumstances (PEC) are applicable only when a manufacturer or open-source software steward (hereinafter the "Reporter") submits a 72-hour Notification of an Actively Exploited Vulnerability (AEV). *(New defect in the 2026-09-09 22:12 UTC rewrite: this instance and the two below now read "**Particular** Exceptional Circumstances", dropping "-ly" — but the opening sentence above still reads "**Particularly** Exceptional Circumstances", so the page is now internally inconsistent about the spelling of its own defined term.)* During the first 72-hour window, the Reporter should assess, where applicable, whether Particular Exceptional Circumstances (PEC) apply.

- **Flagging a submission**: In order to flag a submission under PEC, in the 72-hour report template, scroll down and toggle the Particular Exceptional Circumstances (PEC) indicator. PEC can be invoked only where at least one of the conditions under the third subparagraph of Article 16(2) of the CRA applies. By toggling the indicator, the PEC Delay Reason option will be displayed. An optional field is also available to provide a justification that can help the CSIRT Designated as Coordinator (CDaC) decide whether to accept the submission under PEC.
- **Effect**: PEC is intended for exceptional situations in which the dissemination of information may need to be delayed to avoid security-related risks. If PEC is invoked in the 72-hour Notification, the dissemination status becomes "72h Submitted under PEC". The CDaC remains responsible for deciding whether dissemination is necessary and possible, and for manually sharing the notification with other concerned CSIRTs and the full notification with ENISA. In this scenario, the full notification is not simultaneously made available to ENISA. Only limited information in accordance with Article 16(2) is made available to ENISA.

All previously-tracked fixes (the "the AR's" apostrophe, the "PEC Delay Reson" typo, "SRP" before "Dashboard") remain in place from the 21:07 UTC rewrite; unchanged this pass except as noted above.

Cross-reference: this matches Q21's summary on the FAQ page and the Glossary's v27 (Particular Exceptional Circumstances (PEC)) and v28 (PEC Delay Reason) fields — no deadline, obligation or field name here contradicts either. Note that the Glossary's own v27 field name has always read "**Particular** Exceptional Circumstances (PEC)", not "Particularly" — so the three body instances changed in the 2026-09-09 22:12 UTC rewrite now match the Glossary's spelling, and it is the guidance page's own still-unmoved opening sentence ("Particularly Exceptional Circumstances") that is the odd one out.

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
- 2026-09-02: monitoring scope extended at user request to include the three guidance subpages themselves (previously only their title/date were tracked from the summary list on the main page), listed in `guidance_urls`. Fetched raw HTML of all three and captured full content as a new baseline section ("Guidance subpages — full content baseline"), dated `guidance_retrieved: 2026-09-02`. Their "Last updated" dates on this pass (3/08/2026, 3/08/2026, 14/08/2026) match what was already known from the summary list, so this is a first full-content capture, not a detected change. FAQ/main page content itself was not re-checked in this pass (still as of 2026-08-31); the next check should diff both the FAQ/main page and all three guidance subpages against this file.
- 2026-09-07: checked (fetched raw HTML directly for the main page, the FAQ page, both re-verified guidance subpages, and — newly discovered via the site's own updated navigation — two brand-new subpages, the "CRA SRP Glossary" and the "List of CSIRTs Designated as Coordinators"). **Major overhaul**: FAQ page-level date bumped to "Updated: 04 September 2026"; every FAQ answer reworded/expanded and tagged [UPDATED] (except Q19, whose text changed without the tag); FAQ entry count grew from 23 to 27 (three new numbered questions Q24–Q26 plus one new unnumbered entry, all tagged [NEW]); Q16's data-field table grew from 39 to 43 fields and now defers to the new Glossary page as the authoritative source; a new helpdesk-contact closing note was added to the bottom of the FAQ page (the equivalent line was removed from the main page's "User guidance" footer). The two new subpages (Glossary — version 1.1, last update 05/09/2026; CSIRT list — Updated 04/09/2026) are now tracked going forward (`glossary_url`, `csirt_list_url` added to frontmatter) and captured in summary/table form. Guidance subpages verified unchanged in substance/dates, with one cosmetic typo spotted ("manufacturer adress"). See the "Change log (2026-09-07 check...)" section above for full detail. File updated accordingly.
- 2026-09-07 (evening, second check that day): FAQ page "Updated: 07 September 2026". **Production URL published** (`https://portal.cra-srp.enisa.europa.eu`, Q9 and new Q28). Two questions added (Q28, Q29), the previously unnumbered entry now numbered Q27; count 27 → 29. Q8's CSIRT-choice article reference corrected by ENISA from Art. 15(7) to Art. 14(7); Q18 now states that selecting the wrong CDaC may invalidate a notification. Q22 names the pre-launch testing participants and rules out further testing before go-live; Q24 states English-only at launch. Glossary edited the same day without a version bump (see `enisa-srp-glossary-baseline.md`); its eight links from the FAQ page are broken (403, old path). Guidance subpages, CSIRT list and main page otherwise unchanged. See the change log at the top of this file.
- 2026-09-08: checked (fetched raw HTML directly for all seven tracked pages — main page, FAQ, CSIRT list, all three guidance subpages, and the Glossary at its current `cra-srp-glossary2` address — with retry backoff; all seven returned HTTP 200 and were confirmed as real page bodies, not error documents). Word-for-word diff against this baseline found **no substantive change on any page**: FAQ still "Updated: 07 September 2026", still Q1–Q29 with the same tags, wording, and Q16 field table (43 fields, same values); CSIRT list still 27 countries, same links, "Updated: 04/09/2026"; the three guidance subpages unchanged (same "Last updated" dates, same procedures, same typos); main page unchanged, its Glossary resource card still points to `cra-srp-glossary2`, and the eight broken Glossary links inside the FAQ answers are still unrepaired. One navigation nuance noted for future checks: the site's own "Content" subtopics list (shown in the left-hand sidebar on the main page and every subpage) currently lists only five items — FAQ and the three guidance pages, plus the CSIRT list — and does not include "CRA SRP Glossary", even though the 2026-09-07 discovery run recorded it there. The Glossary page itself is unaffected (still reachable, still linked via the "Get Started" resource card on the main page and via the FAQ's own links), so this is not treated as a reachability or content change, only flagged in case the omission from that list persists or widens on a future check. See `enisa-srp-glossary-baseline.md` for the same day's Glossary check, which found one likely pre-existing transcription artifact in the baseline table (not an ENISA change) and corrected it. `last_check` updated to 2026-09-08; `last_change` left at 2026-09-07 since nothing on this page changed.
- 2026-09-08 (04:10 UTC, second check that day): checked all seven pages again with retry backoff; all HTTP 200 and confirmed as real bodies. FAQ page, Q16 table, main page, CSIRT list, and the Glossary are all still unchanged from the morning's baseline (Glossary re-verified separately in `enisa-srp-glossary-baseline.md`, still no change). Two real changes found: (1) all eight previously-broken "SRP Glossary" links inside the FAQ answers now resolve — ENISA repointed them from the dead `.../cra-srp-glossary` path to `.../cra-srp-glossary2`; updated the hrefs in this file to match and dropped the stale "Broken links" note. (2) The AR User Registration and AR Interface Functions guidance pages were both rewritten in a second-person "Follow these steps to …" style and now show "Last updated: 07/09/2026" (previously 3/08/2026 and 14/08/2026); the AR Notification Submission and Update page is untouched (still 3/08/2026). No deadline, obligation, status name, or numeric limit changed in the rewrite, but it introduced two new typos ("Yo can access the Dashboard", a duplicated "Manufacturer Association" section title), two new stray double full stops, and one wording change worth watching — the "Invite Secondary AR" expected result now says the invitation email goes to the Primary AR rather than the Secondary AR, which reads like an unintended slip rather than a process change. The main page's own "User guidance" summary cards were not refreshed to match the two rewritten subpages' new dates — noted as a stale-but-harmless discrepancy, not corrected. See the change log at the top of this file for full detail and exact quotes. `last_check` and `last_change` both updated to 2026-09-08.
- 2026-09-08 (09:10 UTC, third check that day): checked all seven pages again with retry backoff; all HTTP 200 and confirmed as real bodies. CSIRT list, Glossary (re-verified separately in `enisa-srp-glossary-baseline.md`), and all three guidance subpages unchanged from the 04:10 UTC baseline. The FAQ page moved again: page-level date bumped to "Updated: 08 September 2026"; a new **Q30** was added ("I am not a manufacturer. How can I report a vulnerability or security issue?", tagged [NEW], count 29 → 30) directing non-manufacturers to their national CSIRT and warning that such a submission "might be marked as 'invalid' in the SRP"; **Q27** gained an [UPDATED] tag and was rewritten with sharper article citations (Art. 15(1) and (2), Art. 14(3) for both AEV and SI) plus a new sentence on the open-source steward timeline (Art. 24(3), 11 December 2027, per Art. 71(2)). The Q16 table's long-flagged "I39." capitalisation inconsistency was fixed to lowercase "i39."; two more field-name capitalisations shifted to lowercase (field 11 "Product name", field 19 "User action") with no status value moved. See the change log at the top of this file for full detail and exact quotes. `last_check` and `last_change` both updated to 2026-09-08 (already today's date from the 04:10 UTC check).
- 2026-09-08 (12:18 UTC, fourth check that day): checked all seven pages again with retry backoff; all HTTP 200 and confirmed as real bodies. No substantive change anywhere: FAQ still Q1–Q30 with the same tags and wording, CSIRT list, Glossary (re-verified separately, still unchanged) and all three guidance subpages unchanged from the 09:10 UTC baseline. One more editorial capitalisation shift in the Q16 table, continuing the pattern from the 09:10 UTC check: fields 12–15 (Product Version/Type/Class/Category) are now lowercase "version/type/class/category"; no status value moved. `last_check` and `last_change` both left at 2026-09-08 (already today's date).
- 2026-09-08 (14:10 UTC, fifth check that day): checked all seven previously-tracked pages again with retry backoff; all HTTP 200, confirmed as real bodies, and byte-for-byte unchanged from the 12:18 UTC baseline (FAQ Q1–Q30, CSIRT list, Glossary re-verified separately in `enisa-srp-glossary-baseline.md`, all three original guidance subpages). Walking the main page's "Content" navigation, as the routine's instructions require, turned up an eighth page not in either baseline: **"CRA SRP guidance - Particular Exceptional Circumstances (PEC)"** (`.../cra-srp-guidance-particular-exceptional-circumstances-pec`, HTTP 200), explaining how an AR flags a 72-hour AEV notification under PEC per Art. 16(2) of the CRA. Added as `guidance_urls[3]` and captured in full under "Guidance subpages — full content baseline"; see the change log at the top of this file for the substance and the one typo found ("PEC Delay Reson"). This widens the routine's scope from seven pages to eight, so `routines/enisa-srp-pages-monitor.md` was updated in this same commit per `CLAUDE.md`, and the live Routine (trigger `trig_015C8QiJhXwkxPkDdoMbkHeD`) still needs the same update applied by a human in the Routines UI — this PR is therefore left open rather than auto-merged, since it touches a file besides the two baselines. `last_check` left at 2026-09-08 (already today's date); `last_change` left at 2026-09-08 (already bumped by the 09:10 UTC check) even though this run's own finding — the new page — is itself a change, because `last_change` tracks content edits to the seven originally-tracked pages, not the discovery of an eighth.
- 2026-09-08 (21:06 UTC, sixth check that day): checked all eight tracked pages (the URL list read from both baselines' frontmatter, per the routine's own instructions, now includes the PEC guidance page) with retry backoff; all HTTP 200, confirmed as real bodies. Main page, FAQ (still Q1–Q30, same tags and Q16 table), CSIRT list, Glossary (re-verified separately in `enisa-srp-glossary-baseline.md`), AR Notification Submission and Update, AR Interface Functions, and PEC guidance were all byte-for-byte unchanged from the 14:10 UTC baseline. AR User Registration was rewritten a second time in 24 hours: page date "Last updated: 07/09/2026" → **"08/09/2026"**. The launch-URL placeholder is now filled in with the production address; both registration flows gained an explicit MFA precondition; Secondary AR registration gained a new precondition ("The Primary AR is a validated user") not stated anywhere else on these pages; the Primary AR flow's expected result now explicitly confirms notification submission is not blocked by pending validation; one new redundant sentence and one minor wording shift ("return" → "display" an error) were introduced. See the change log at the top of this file for full detail and exact quotes. `last_check` and `last_change` both left at 2026-09-08 (already today's date).
- 2026-09-08 (23:11 UTC, seventh check that day): checked all eight tracked pages again with retry backoff; all HTTP 200, confirmed as real bodies (raw HTML parsed with a fresh word-for-word text extraction rather than relying on the previous check's own summary). No ENISA content changed: main page, FAQ (Q1–Q30, same tags, Q16 table), CSIRT list (27 countries, same links, "Updated: 04/09/2026"), Glossary (re-verified separately in `enisa-srp-glossary-baseline.md`, unchanged), AR User Registration and AR Interface Functions all byte for byte unchanged from the 21:06 UTC baseline. The more literal extraction did turn up two small gaps in this file's own capture of the PEC and AR Notification Submission and Update pages — an apostrophe in "the AR's" on the PEC page, and "Particularly Exception Circumstances" (missing "-al") on the Notification/Update page — both present on the live pages but recorded loosely in this baseline; corrected here as capture fixes, not counted as ENISA changes, since it could not be determined whether either wording is new. See the change log at the top of this file. `last_check` and `last_change` both left at 2026-09-08 (already today's date).
- 2026-09-09 (12:19 UTC): checked all eight tracked pages (URL list read from both baselines' frontmatter) with retry backoff; all HTTP 200, confirmed as real page bodies (title tags and known content markers checked, not just the exit code). Three real changes: (1) the FAQ page date moved to "Updated: 09 September 2026", Q9 was substantially rewritten with new AR-role/permission detail including a new explicit precondition for inviting a Secondary AR, and Q8 silently lost its "[UPDATED]" tag; (2) the AR User Registration guidance's "General Notes" section was reworded (expanded EU-Login pointer, restructured validation-timing sentence, one new grammar defect) without its own "Last updated: 08/09/2026" stamp moving; (3) the PEC guidance page was reworded throughout in flowing-paragraph style, also without gaining a date stamp — substance, typo ("Reson") and legal cross-references all unchanged on both. Main page, CSIRT list (27 countries, "Updated: 04/09/2026"), Glossary (all 38 fields re-verified row by row in `enisa-srp-glossary-baseline.md`, unchanged), AR Notification Submission and Update, and AR Interface Functions all byte for byte unchanged. See the change log at the top of this file for full detail and exact quotes. `last_check` and `last_change` both updated to 2026-09-09.
- 2026-09-09 (21:07 UTC): checked all eight tracked pages again with retry backoff; all HTTP 200, confirmed as real page bodies. Two real changes, both guidance pages: (1) AR Interface Functions was rewritten a second time, page date "07/09/2026" → **"09/09/2026"**, fixing three typos this baseline had tracked since the 07/09 rewrite ("Yo" → "You", the duplicated "Association" section title, two stray double full stops) and changing "who instructs" to "which instructs" in the still-unresolved Invite-Secondary-AR wording; (2) the PEC guidance page was reworded again (still no date stamp), fixing the long-tracked "the AR's" apostrophe and the "PEC Delay **Reson**" typo, and capitalising/reformatting several PEC references — no deadline, obligation, legal cross-reference, or scope changed on either page. Main page, FAQ (Q1–Q30, same tags, Q16 table), CSIRT list (27 countries, "Updated: 04/09/2026"), Glossary (all 38 fields re-verified row by row in `enisa-srp-glossary-baseline.md`, unchanged), AR User Registration, and AR Notification Submission and Update all byte for byte unchanged. See the change log at the top of this file for full detail and exact quotes. `last_check` and `last_change` both updated to 2026-09-09 (already today's date from the 12:19 UTC check).
- 2026-09-09 (22:12 UTC): checked all eight tracked pages again with retry backoff; all HTTP 200, confirmed as real page bodies. Four real changes, all guidance pages: (1) AR Notification Submission and Update was finally rewritten into the second-person "Follow these steps…" style (screenshots, numbered steps) already used by the other guidance pages, and its date stamp moved for the first time since 2026-09-02 ("3/08/2026" → "03 September 2026"); substance unchanged. (2) AR User Registration reworded again ("08/09/2026" → "09/09/2026"): the long-tracked "manufacturer adress" typo and the self-contradictory EU-Login field note are both fixed; the Secondary-AR invitation precondition now uses the "Verified" term already used by Q9; a new field-list inconsistency appeared between the Primary and Secondary AR flows (see change log). (3) AR Interface Functions was rewritten a second time today without its stamp moving again: this fixed the long-standing Invite-Secondary-AR email-recipient bug and the 10-vs-20 Unverified-AR notification-limit mismatch with Q9, but renamed a button, dropped a named filter-tab label, and introduced one new grammar defect. (4) PEC guidance gained its first-ever "Last updated" date stamp, but three body instances of its own defined term were changed from "Particularly" to "Particular" Exceptional Circumstances while the opening sentence still reads "Particularly" — a new internal inconsistency (though the Glossary's own v27 field name has always read "Particular", so this partially reconciles the two). Main page, FAQ (Q1–Q30, same tags, Q16 table, "Updated: 09 September 2026"), CSIRT list (27 countries, "Updated: 04/09/2026"), and Glossary (all 38 fields re-verified row by row in `enisa-srp-glossary-baseline.md`, unchanged) all byte for byte unchanged. See the change log at the top of this file for full detail and exact quotes. `last_check` and `last_change` both updated to 2026-09-09 (already today's date).
- 2026-09-09 (23:11 UTC): checked all eight tracked pages again with retry backoff (extracted with a fresh raw-HTML text pass, not a prior summary); all HTTP 200, confirmed as real page bodies. Only the FAQ and CSIRT-list pages changed this time — see the change log at the top of this file for the Q9/Q16/CSIRT wording detail. The four guidance pages, the main page and the Glossary were all byte-for-byte unchanged from the 22:12 UTC baseline. `last_check` and `last_change` both updated to 2026-09-09 (already today's date).
- 2026-09-10 (00:10 UTC): first check of the day (yesterday's date was still in `last_check` on `main`). Checked all eight tracked pages with retry backoff; all HTTP 200, confirmed as real page bodies via title-tag and known-content checks, not just exit code. One cosmetic change found: the AR User Registration guidance page's own intro sentence now reads "Assigned Representative" (singular), was "Assigned Representatives" (plural) — its "Last updated: 09/09/2026" stamp did not move, and the main page's own "User guidance" card blurb for this page still uses the plural, so the two now disagree. No precondition, deadline, obligation, field, or numeric limit affected. Main page, FAQ (Q1–Q30, same tags, Q16 table), CSIRT list (27 countries, "Updated: 04/09/2026"), AR Notification Submission and Update, AR Interface Functions, PEC guidance, and the Glossary (re-verified separately in `enisa-srp-glossary-baseline.md`) all otherwise byte-for-byte unchanged from the 23:11 UTC baseline. See the change log at the top of this file for detail. `last_check` and `last_change` both updated to 2026-09-10.
- 2026-09-10 (01:08 UTC): checked all eight tracked pages again with retry backoff; all HTTP 200, confirmed as real page bodies (raw HTML parsed with a fresh word-for-word text extraction, not a prior summary). One real change: the long-tracked "72-hour Sever Incident Notification" typo in Q26 (present since at least 2026-09-07) is fixed to "Severe" — no deadline, counter logic, or obligation affected, and the page's own "Updated: 09 September 2026" stamp did not move. Main page (still 6-item Content nav, no Glossary/9th entry, no PEC card), CSIRT list (27 countries, "Updated: 04/09/2026"), all four guidance subpages (same stamps, same typos, byte for byte), and the Glossary (all 38 fields re-verified row by row in `enisa-srp-glossary-baseline.md`, footer unchanged) otherwise unchanged from the 00:10 UTC baseline. See the change log at the top of this file for detail. `last_check` and `last_change` both already 2026-09-10.
