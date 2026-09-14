# CRA Single Reporting Platform — observed defects and gaps

A list of errors, contradictions and apparent omissions found in the public
ENISA Single Reporting Platform (SRP) pages, compiled so that they can be
passed to ENISA for correction.

**Checked against**: all eight SRP pages plus the CSIRT list, fetched
**9 September 2026, 16:08 UTC** — i.e. after ENISA's edits earlier that day.

**Verified in the running platform**: **13 September 2026**, by a registered
Assigned Representative with an account on the live SRP, who reported what the
form shows. That is the source of **section G**, and the only part of this
document that could see the form rather than the published pages. No
credential, session or account detail is reproduced anywhere here.

**Status re-checked**: **10 September 2026, 07:13 UTC** and again at
**11:52 UTC**, each time against a fresh fetch of every page. ENISA edited the
pages eight more times before the first re-check and rewrote the main page,
extended the FAQ and published two new documents — an **AR User Manual** (PDF,
55 pages, "Version: 1.1") and a **Terms and Conditions** page — before the
second. Each
finding below now carries a status, and a fixed one names the time the change
was first seen. Findings are never deleted — a fixed one stays listed, marked
**fixed**, so the record of what was wrong survives the correction.

| Status | Meaning |
|---|---|
| **fixed** · *timestamp* | the quoted text is gone from the live page; the timestamp is the monitor run that first recorded it |
| **partly** · *timestamp* | ENISA changed something here, but the finding is not resolved |
| **open** | still present on 10 September 2026, 11:52 UTC |

| Page | Short name used below | Own version stamp |
|---|---|---|
| [Single Reporting Platform (main)](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp) | Main | — |
| [Frequently Asked Questions](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/frequently-asked-questions) | FAQ | Updated: 10 September 2026 (was 09 September; Q31 added) |
| [CRA SRP Glossary](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2) | Glossary | version 1.2, last update: 09/09/2026 (was 1.1 / 05/09/2026 on 9 September) |
| [Guidance — AR User registration](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-guidance-ar-user-registration) | Registration | Last updated: 09 September 2026 (was 08/09/2026) |
| [Guidance — AR Notification submission and update](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-guidance-ar-notification-submission-and-update) | Submission | Last updated: 09 September 2026 (was 3/08/2026, then 03 September 2026) |
| [Guidance — AR Interface functions](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-guidance-ar-interface-functions) | Interface | Last updated: 09 September 2026 (was 07/09/2026) |
| [Guidance — Particular Exceptional Circumstances (PEC)](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-guidance-particular-exceptional-circumstances-pec) | PEC | Last updated: 09 September 2026 (had none on 9 September — see D7) |
| [List of CSIRTs Designated as Coordinators](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/list-of-csirts-designated-as-coordinators) | CSIRT list | Last updated: 10 September 2026 (was "Updated: 04/09/2026") |
| [AR User Manual](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-ar-user-manual) *(new, seen 10 September 11:52 UTC)* | Manual | PDF "Version: 1.1"; document history lists only v1.0 of 09/09/2026 — see F11 |

Every item below was verified against the 9 September fetch when first written,
and again against the 10 September fetch for its status. A few findings come from screenshots published on the guidance pages
rather than from the page text; these are marked *(screenshot)* — no account,
login or form submission was used to obtain anything in this report.

Findings are numbered so that individual points can be referenced in a reply.

---

## A. Typos and wording

Text quoted verbatim as it stood on 9 September.

| # | Page | Where | Text on 9 September | Suggested correction | Status |
|---|---|---|---|---|---|
| A1 | Glossary | Field 11 "End of support indicator", instruction column | "…has reached the end of the support period or No when is **doesn't**." | "…or No when it doesn't." | **open** |
| A2 | Glossary | Field v26, instruction column | "…state that attribution is unknown (max. 100 characters)**..**" | Single full stop. | **open** |
| A3 | Glossary | Field v29, instruction column | "…CSIRT Designated as Coordinator **(CDaC)taking** their decision." | Insert a space: "(CDaC) taking". | **open** |
| A4 | Glossary | Field i36, meaning column | "Date and time when the manufacturer or **another relevant become aware** of the incident." | "…or another relevant entity became aware…" | **open** |
| A5 | Glossary | Field i37, example column | "…enter the date and time when the incident **was began** or occurred." | "…when the incident began or occurred." | **open** |
| A6 | FAQ | Q26, Final Report paragraph | "…one month after submission of the 72-hour **Sever** Incident Notification." | "Severe". | **fixed** · 2026-09-10 01:08 UTC — now "Severe" |
| A7 | FAQ | Q16, introductory paragraph | "For each field, **it explains that the field means**, how it may be completed…" | "…it explains what the field means…" | **fixed** · 2026-09-09 23:11 UTC — now "what the field means" |
| A8 | FAQ | Q16 table, field 22 | "Corrective or mitigating measures that **user** can take" | "…that users can take" (the Glossary uses the plural). | **fixed** · 2026-09-09 23:11 UTC — now "that users can take" |
| A9 | PEC | Body text | "By toggling the indicator, the PEC Delay **Reson** options will be displayed." | "Reason" — the Glossary (v28) spells it correctly. | **fixed** · 2026-09-09 21:07 UTC — now "PEC Delay Reason" |
| A10 | PEC | Screenshot of the PEC block *(screenshot)* | "…would be contrary to the essential **intrests** of that Member State" | "interests". This is in the application UI, not only in the guidance. | **open** — a UI screenshot, not testable from page text; unchanged as far as can be seen |
| A11 | Interface | "Access the Dashboard" step | "**Yo** can access the Dashboard by:" | "You". | **fixed** · 2026-09-09 21:07 UTC |
| A12 | Interface | Section heading | "Add an **Association** with an Additional Manufacturer **Association** through Settings" | "Association" appears twice; drop the second. | **fixed** · 2026-09-09 21:07 UTC — heading now "Add Additional Manufacturer Association via Settings" |
| A13 | Registration | Manufacturer details step | "Enter the manufacturer details (manufacturer name, manufacturer **adress**, additional information)" | "address" — see D4: the field is absent from the live form, so the guidance text is wrong on both counts. | **fixed** · 2026-09-09 22:12 UTC — now "address"; the field itself is still missing, see D4 |
| A14 | Registration | Invitation registration, personal details step | "These fields **cannot be edited** but are retrieved from EU Login and **cannot be edited** in the SRP." | The clause is duplicated within one sentence. | **fixed** · 2026-09-09 22:12 UTC — now "These fields are retrieved from EU Login and cannot be edited in the SRP." |
| A15 | Submission | Expected results, 72-hour Notification and Final Report | "…subject to **Particularly Exception** Circumstances (PEC)…" (twice) | "Particular Exceptional Circumstances" — "Exception" is not a valid form. See also C2. | **open** — three occurrences now, after the Submission page was rewritten on 9 September 22:12 UTC |
| A16 | Submission | Pre-conditions, three occurrences | "you are **logged in into** the SRP" | "logged in to the SRP". | **open** — still three occurrences |
| A17 | AR User Manual | §1.4 "How to Use the Manual" (p. 7) | "Section 5 presents other functionalities available on the platform, including reminders and alerts. Section 6 provides FAQs…" | There is no standalone Section 5 — reminders/alerts is §4.9, and the FAQ section's own divider page is titled "SECTION 5", not 6. | **open** — the manual's own table of contents (p. 3-4) agrees with the divider pages, not with §1.4's description |

---

## B. Contradictions

These are cases where two statements cannot both be followed. They matter more
than the typos: a reporter acting on one of them acts wrongly.

### B1 — Glossary field 11: the meaning column describes a different field

**Status: fixed** · *2026-09-10 13:11 UTC* — rewritten with the Glossary's v1.2 → v1.3 move. The meaning column now reads "Indicates whether the product with digital elements has reached the end of the support period", describing this field's actual Yes/No content instead of a user-interface indicator. The "is doesn't" typo went with it.

Field 11 is named **"End of support indicator"**. Its instruction, format and
example columns are consistent with that ("You may select one: Yes … or No",
"Select one: Yes or No", example "Yes"). Its *meaning* column is not:

> "Indicates whether the product with digital elements **has a user interface
> or similar technical means allowing direct interaction with its users** and
> the manufacturer should make use of such features to inform users that their
> product with digital elements has reached the end of the support period."

That describes a user-interface capability, not an end-of-support state. A
reader trying to decide what "Yes" means here gets two different answers.

### B2 — Glossary field v28: "one" versus "at least one" versus the form

**Status: fixed** · *2026-09-10 13:11 UTC* — "select one of the three of the legally specified circumstances" became "select at least one of the three legally specified circumstances", matching the field's own completion instruction. Note the field is **now numbered v29**: the same Glossary release inserted a new AEV field as v23 and shifted every later number up by one.

Three statements about the same PEC field disagree:

- Meaning column: "You may select **one of the three of** the legally specified
  circumstances…" — also garbled; "the three of" is not a phrase.
- Instruction column: "You may select **at least one** of the three options."
- The form itself *(screenshot)*: three independent **check boxes**, i.e.
  multiple selection is possible.

Article 16(2) third subparagraph does not require the grounds to be exclusive,
so the instruction column and the form appear correct and the meaning column
wrong — but the page should say so unambiguously.

### B3 — "Applied and ongoing" versus "Applied or ongoing"

**Status: fixed · 2026-09-10 05:10 UTC** — the Glossary's i32 now reads "Applied **and** ongoing mitigation measures", in the same edit that bumped the Glossary to version 1.2. FAQ and Glossary agree.

The same field is named two ways:

- FAQ, Q16 table: "**Applied and ongoing** mitigation measures"
- Glossary, field i32: "**Applied or ongoing** mitigation measures"

"And" and "or" are not interchangeable here: one reading requires measures to
be both already applied and still running, the other accepts either.

### B4 — Who receives the invitation email for a Secondary AR

**Status: fixed · 2026-09-09 22:12 UTC** — Interface now reads "The SRP sends an email invitation to the Secondary AR." Both pages describe the same flow.

- Interface, "Invite Secondary AR", expected result: "An email is sent to **the
  Primary AR, who instructs the Secondary AR** to complete registration."
- Registration, "Registration via Invitation (Secondary AR)", pre-conditions:
  "**You have received a valid SRP email invitation** initiated by a Primary
  AR"; and step 1: "Click the link in the email invitation."

One page has the invitation going to the inviter, the other to the invitee.
Since the link expires after 7 days, a Secondary AR who waits for an email that
was in fact sent to their Primary AR can lose the invitation.

### B5 — How many notifications before the association is verified

**Status: fixed · 2026-09-09 22:12 UTC** — Interface now says 20, matching Q9.

- FAQ, Q9: "ARs whose manufacturer association has not yet been verified may
  submit up to **20 notifications** for that manufacturer before verification
  becomes mandatory."
- Interface, "Add a manufacturer", expected result: "As unverified AR you can
  submit only up to **10 notifications**."

### B6 — "Legal name" is described as non-editable but is editable

**Status: fixed · 2026-09-10** — moot: ENISA confirmed on 10 September that the Legal name field has been dropped, so there is no longer an editable field described as non-editable. What remains is the stale Secondary-flow text and screenshot on the guidance page, tracked as F13.

Registration states that the pre-filled personal details "(First Name, Last
Name, Email, Legal name) … are retrieved from EU Login and cannot be edited in
the SRP". In the published screenshot of that step *(screenshot)*, First Name,
Last Name and Email are greyed out, while **Legal name is an editable input
field**. Either the text or the form is wrong.

---

## C. Inconsistent naming

Not errors in themselves, but the SRP is a legal reporting tool and users match
guidance to form labels word by word.

| # | Variants in use | Where | Suggestion | Status |
|---|---|---|---|---|
| C1 | "Full description of the severity/impact" (AEV) vs. "Detailed description of the Severity/Impact" (SI) | Glossary fields v23 and i33; FAQ Q16 table | Same content, two names and two capitalisations. Pick one. | **partly** · 2026-09-09 23:11 UTC — the FAQ renamed v28/v29 to "Detailed", so the FAQ is now consistent with itself; but the Glossary's v23/v24 still read "Full", so the two documents now disagree where they used to agree |
| C2 | "Particular Exceptional Circumstances" / "Particularly Exceptional Circumstances" / "Particularly Exception Circumstances" | PEC page uses the first and second within a few lines of each other; Submission uses the third | The CRA itself has no defined term here; choose one form and use it everywhere, including the UI label. | **open** — the PEC page now reads "Particular" seven times and "Particularly" once (22:12 UTC rewrite); Submission still has "Exception" |
| C3 | "Particular Exceptional Circumstances**(PEC)**" — no space before the bracket *(screenshot)* | The toggle label in the notification form | Insert a space, to match every guidance page. | **open** — UI label, not testable from page text |
| C4 | "validation" vs. "verification" of the AR–manufacturer association | FAQ Q9 uses both in one paragraph ("validation … before **verification** becomes mandatory"); Registration uses "validation"; Interface uses "Unverified" as the status | One term for the act, matching the status name shown in the platform. | **open** — Q9 now reads "Verification takes place … while validation is pending" (23:11 UTC): both words in one sentence. The new AR User Manual leans the other way: "validation" 12 times, "verification" once |
| C5 | Date formats: "3/08/2026", "07/09/2026", "08/09/2026", "09 September 2026", "05/09/2026", "04/09/2026" | Guidance pages, FAQ, Glossary, CSIRT list | Mixed unpadded numeric, padded numeric and long form. Numeric DD/MM is ambiguous to non-European readers; the FAQ's "09 September 2026" is unambiguous. | **partly** · 2026-09-09 22:12 / 2026-09-10 02:08 UTC — six pages now spell the month out; the main-page cards moved to "Updated: 9 September 2026" in the 10 September main-page rewrite (seen 11:52 UTC); only the Glossary footer still reads "09/09/2026" |

---

## D. Apparently missing

### D1 — No Glossary entry for "Legal name"

**Status: fixed · 2026-09-10** — resolved by removal, and **confirmed by ENISA on 10 September**: the field has been dropped from the platform. Evidence before the confirmation: the AR User Manual's own screenshots of the personal-details step (Primary and invitation flows alike) show **three fields — First Name, Last Name, Email** — and its text lists the same three. The field appears to have been dropped from the platform. The guidance page's screenshot and its Secondary-AR text still show it, so the web page is now the stale one (F13).

The registration form asks for **"Legal name (for legal entities)"** and
Registration mentions it, but the Glossary has no entry for it (0 occurrences).
An AR registering as a natural person has nothing telling them whether to leave
it empty.

### D2 — No Glossary entry for "Additional Information", which is mandatory

**Status: partly** · *the mandatory half settled 2026-09-13 in the running platform* — the field is **not** required. The live *Manufacturer Details* dialog shows **Name** carrying a *Required* badge and **Additional Information** carrying none, with the placeholder "Additional information (max 255 characters)". That closes the question the AR User Manual and the guidance page disagreed on (F13): the manual, which called it optional, was right, and the guidance page's "Required field" screenshot documents a build that is no longer running.

What remains open is the documentation half: the term still appears nowhere in the Glossary or the FAQ, and nothing states what belongs in the field — which matters because this is the information the CSIRT uses to decide whether to verify the association. A 255-character limit is now known, from the placeholder, and is documented nowhere either.

The Manufacturer Details step of AR registration has a field
**"Additional Information"**, which ENISA's guidance-page screenshot marks
**"Required field"** *(screenshot)*. The term does not appear in the Glossary
or the FAQ at all. As built, the field is optional and capped at 255
characters, and no published source says either.

### D3 — The 800-character limit on the PEC justification is not documented

**Status: open** — the limit appears in neither the Glossary nor the PEC page on 10 September, nor in the AR User Manual (0 hits for "800").

The PEC justification box is labelled "Provide further information (max 800
characters)" *(screenshot)*. Neither the Glossary (field v29) nor the PEC page
states the limit. Compare field v26, where the Glossary does give the limit
("max. 100 characters"). A reporter drafting a justification offline has no way
to know it will be truncated or rejected.

### D4 — Registration describes a manufacturer address field that does not exist

**Status: open** · *re-verified 2026-09-13 in the running platform* — the field is **not** in the form. The live *Manufacturer Details* dialog offers **Name** (Required), **CSIRT Designated as Coordinator** (read-only, pre-filled) and **Additional Information** (no Required badge), and nothing else.

**Withdrawn:** this entry previously reported, on the strength of a statement made to us on 10 September, that ENISA would restore the address field, and was marked *partly* on that basis. Two days after go-live the field has not appeared and there is no present indication that it will, so the claim is withdrawn rather than left standing — the guidance text is the side that is wrong. Anyone who acted on the earlier note should disregard it. (The typo in the same sentence was fixed separately, A13.)

Registration: "Enter the manufacturer details (manufacturer name, manufacturer
adress, additional information)". The published screenshot of that very step
*(screenshot)* shows only **Name**, **CSIRT Designated as Coordinator**
(read-only) and **Additional Information**. There is no address field. Either
the guidance is stale or the field was dropped.

### D5 — No screenshots of the 72-hour and Final Report forms

**Status: partly · 2026-09-10 11:52 UTC** — the guidance page is unchanged (still one Dashboard image per section), but the new **AR User Manual** documents both steps, §4.7.3 "Submit 72-hour Notification" and §4.7.4 "Submit Final Report", with two or three screenshots per page. The gap is closed in the manual, not on the page a reader reaches from the navigation.

Submission illustrates the Early Warning flow with six screenshots, one per
step. The "Submit a 72-hour Notification" and "Submit a Final Report" sections
each have a single screenshot — of the Dashboard step that opens the
notification — and none of the tabs where the reporting actually happens. These
are the two submissions with statutory deadlines and, for AEVs, the ones where
PEC applies.

### D6 — The PEC page is missing from the main page's guidance cards

**Status: fixed · 2026-09-10 11:52 UTC** — the main page was rewritten on 10 September; the "User Guidance" block now carries a PEC entry with its own blurb. (Seen on this check's own fetch; the monitor's 09:09 run predates the rewrite.)

The SRP main page has a "User guidance" block with a card for each guidance
page: AR User registration, AR Notification submission and update, AR Interface
functions. The **PEC guidance page has no card** — it appears only in the
"Content" navigation list. A user browsing the main page will not find it.

### D7 — The PEC page carries no "last updated" stamp

**Status: fixed · 2026-09-09 22:12 UTC** — the page now carries "Last updated: 09 September 2026".

Every other guidance page ends with "Last updated: …". The PEC page has none,
although its content was edited on 9 September 2026. There is no way to tell
which version one is reading.

### D8 — The Glossary is missing from the "Content" navigation

**Status: open** — the Content list grew to eight entries on 10 September (AR User Manual and Terms and Conditions added); the Glossary is still not among them.

The "Content" list repeated on the FAQ and guidance pages has six entries: FAQ,
the three AR guidance pages, the PEC page and the CSIRT list. The **Glossary is
not among them**, although it is the reference document for every field on
those pages. It is linked from the main page only, so a user reading the
guidance has to navigate back to find it.

---

## E. Page management

### E1 — The old Glossary URL returns 403 with no redirect

**Status: open** — re-checked 10 September 2026, 11:52 UTC: HTTP 403, no `Location` header. Note that ENISA already operates a redirecting short address — the AR User Manual cites `https://www.enisa.europa.eu/cra-srp-glossary`, which answers 301 to `…/cra-srp-glossary2` — so the mechanism exists; the old path just isn't wired to it.

The Glossary moved from
`…/single-reporting-platform-srp/cra-srp-glossary` to
`…/cra-srp-glossary2`. Re-checked 9 September 2026, 16:31 UTC: the old path
returns **HTTP 403** and sends no `Location` header. A 403 (rather than 404 or
a 301 to the new address) reads as "you may not see this page" rather than
"this page moved", which is what it actually is. Any bookmark, external link or
citation of the old address is now dead. A redirect to `…2` would fix all of
them at once.

### E2 — Glossary content changed without the version stamp moving

**Status: partly · 2026-09-10 05:10 UTC** — the footer moved for the first time, to "version 1.2, last update: 09/09/2026", together with a real content change (B3). Two hours later, at 07:11 UTC, three field names changed (17, i35, i37) and the stamp did not move. The pattern therefore persists.

The Glossary footer has read "version 1.1, last update: 05/09/2026" continuously
while its content was edited on the evening of 7 September 2026. The version
number and date are therefore not a reliable indicator of whether a reader has
the current field definitions — which matters for a document that defines
mandatory reporting fields.

---

## The five that matter most

1. **B4** — the invitation email flow contradicts itself, and the link expires
   in 7 days. *Fixed 9 September 22:12 UTC.*
2. **B5** — 20 versus 10 notifications before verification becomes mandatory.
   *Fixed 9 September 22:12 UTC.*
3. **D2** — a mandatory registration field with no documentation anywhere.
   *Partly — the manual and its newer screenshot make it optional; still undocumented.*
4. **B1 / B2** — two Glossary fields whose meaning column contradicts their own
   instruction, format and form. *Both open.*
5. **E1 / E2** — the Glossary is hard to cite: the old URL is dead without a
   redirect, and the version stamp does not move when the content does. *E1
   open; E2 partly — the stamp moved once, then lagged again two hours later.*

Of the 37 findings, **15 are fixed, 6 partly addressed, 16 open** as of
10 September 2026 (D1 and B6 closed on ENISA's confirmation that Legal name was dropped).

---

## F. Seen since 9 September

Defects that appeared, or were first noticed, after the report above was
written. All **open** unless stated. Timestamps are the monitor run that first
recorded each; "11:52" marks items first seen by this report's own 10 September
re-check, ahead of the monitor.

| # | Page | Where | Text | Since (UTC) |
|---|---|---|---|---|
| F1 | Interface | "Claim the Primary AR role" step | "…**request to the Primary AR role** for a manufacturer" — a word is missing ("request to *take over* / *become*…) | 2026-09-09 22:12 |
| F2 | Registration | Confirm-details step, both flows | Primary AR flow lists "First Name, Last Name, Email"; Secondary AR flow lists "First Name, Last Name, Email, Legal name". Same screen, two field lists. | 2026-09-09 22:12 **Superseded**: the manual shows three fields in both flows; the four-field Secondary text is the stale one (F13). |
| F3 | PEC | Body text | The page's own term is spelled "**Particularly** Exceptional Circumstances (PEC)" in the opening sentence and "**Particular** Exceptional Circumstances (PEC)" seven times below it. | 2026-09-09 22:12 |
| F4 | FAQ | Q9 | "**Verification** takes place in parallel with the reporting process and does not prevent an AR from submitting notifications while **validation** is pending." | 2026-09-09 23:11 |
| F5 | FAQ / Glossary | Q16 v28/v29 vs Glossary v23/v24 | FAQ now "**Detailed** description of the severity/impact of the vulnerability"; Glossary still "**Full** description…". They agreed before this edit. | 2026-09-09 23:11 |
| F6 | Main / Registration | "User guidance" card vs the page | Card blurb: "the Assigned **Representatives** (AR) user registration"; the page itself now: "the Assigned **Representative** (AR)…". The card was reworded and re-dated in the 10 September main-page rewrite — "Updated: 9 September 2026" — but still says "Assigned Representatives (ARs)" against the page's singular. **Partly.** | 2026-09-10 00:10 |
| F7 | Glossary / FAQ | Field i35 vs FAQ i40 | Glossary: "Type of **Threat** or root cause that is likely to have triggered **incident**"; FAQ: "Type of threat or root cause that is likely to have triggered **the** incident". Brought closer on 10 September, not aligned. | 2026-09-10 07:11 |
| F8 | Interface | Manufacturer-details screenshot *(screenshot)* | The manufacturer record is labelled "Manufacturer **Addresss**" (three s), and its *Manufacturer Address* row shows "Manufacturer Sector" as its value. The same screenshot shows the manufacturer record *does* have an address field — which the registration form lacks (D4). | on the page since at least 2026-09-07 Consistent with ENISA's 10 September confirmation that the address field returns to the registration form (D4). |
| F9 | Main | "User Guidance" block, User Manual card | The card's download link is `href="https://CRA SRP – AR User Manual"` — the document's title in place of a URL. The link is dead; the manual is reachable only through the Content navigation. | 2026-09-10 11:52 |
| F10 | Manual / Registration form | Manual §2.1 step 6 vs the form *(screenshot)* | Manual: "Enter the manufacturer details, including Manufacturer Name and Additional Information **(optional)**". The form marks Additional Information **"Required field"**. On closer reading not a contradiction but a version gap: the manual's own screenshot of the step shows the field **without** the badge. The guidance page's "Required field" screenshot is the older state (F13). **Partly** — D2 adjusted accordingly. | 2026-09-10 11:52 |
| F11 | Manual | Cover and page headers vs Document History | Every page says "Version: 1.1"; the Document History table lists a single entry, "09/09/2026 v1.0 First version". Either the history is missing 1.1 or the stamp is wrong. | 2026-09-10 11:52 |
| F12 | FAQ | Q9 vs Q28 | Q9's opening sentence regressed from "The SRP is available at: https://portal.cra-srp.enisa.europa.eu" to "**The SRP will be available in due time**" — the day before the 11 September go-live that Q4, Q28 and Q29 still commit to. Q28 still gives the URL. | 2026-09-10 09:09 |
| F13 | Registration (guidance page) vs AR User Manual | Both screenshots of the registration steps | The guidance page's screenshots (uploaded 7 September) show a **"Legal name (for legal entities)"** field and Additional Information badged **"Required field"**. The manual's screenshots of the same steps (9 September) show neither: three personal fields, no badge. The manual's text matches its screenshots; the guidance page's Secondary-AR text still lists four fields. The guidance page is documenting a previous build of the form. | 2026-09-10 11:52 |


## G. Verified against the running platform

Findings from the **live SRP**, checked on **13 September 2026** by a registered
Assigned Representative with an account, and reported here. Everything else in
this document comes from ENISA's public pages; this section is the only part
that could see the form itself, and it settles questions the published material
left open. No credential, session or account detail is reproduced.

### G6 — The form asks for the detection time; the Glossary and Art. 14 ask for awareness

**The most serious item in this section.** Three sources name one timestamp
three different ways:

| Source | Wording |
|---|---|
| CRA Art. 14 | the 24- and 72-hour deadlines run from **becoming aware** |
| Glossary i37, field name | "Date and time when you **become aware** of the incident (UTC time)" |
| Glossary i37, meaning | "Date and time when the manufacturer or another relevant entity **becomes aware** of the incident." |
| **The running form** | "Date and time when the incident **was detected** (UTC time)" |

Detection and awareness are not the same moment and routinely differ by hours:
a monitoring system detects at 02:00, the people responsible for reporting
learn of it at 09:00. An AR who reads the on-screen label literally enters the
earlier one.

That matters because this is the field the deadline is computed from. ENISA's
own known-issues text says so, naming the field by its Glossary name: the
72-hour counter "will be updated in a future release to calculate the deadline
using the 'Date/Time when you became aware of the incident/actively exploited
vulnerability' field". The label on the field that release will read says
something else.

Which side moves is ENISA's to decide — the defect is that the running form,
the Glossary and the legal trigger use three different words for one timestamp,
and the one on screen is the one an AR will act on.

**Status: open.**

### G1 — The Glossary describes field i31 as a Yes/No/Unknown choice; the form is a free-text box

The Glossary's entry for **i31, "Incident is suspected of unlawful or malicious
acts"** gives Format **"Select one: Yes, No, Unknown"** and Meaning "Boolean
indication of whether available evidence suggests the incident resulted from
unlawful or malicious activity."

The running form presents a **free-text area** with the placeholder "Incident is
suspected by unlawful or malicious acts (max 255 characters)". There is no
Yes/No/Unknown control, and no 255-character limit is stated anywhere in the
Glossary.

This is the one field where preparing from the published guidance produces the
wrong answer: an AR who drafts "Yes" plus reasoning elsewhere will find a text
box expecting prose, and an AR who drafts prose has no way to know it fits in
255 characters. Either the Glossary or the form needs to move.

**Status: open.**

### G2 — The same field's label reads "suspected by", not "suspected of"

The form's label and placeholder both read **"Incident is suspected **by**
unlawful or malicious acts"**. The Glossary, the FAQ and this guide all use
**"of"**. "Suspected by" reverses the sense — it reads as though the acts did
the suspecting.

**Status: open.**

### G3 — Field 8's Format cell was not updated when the field name was

On 10 September ENISA expanded the name of field 8 to "Product Type
(Default/**Important Product with Digital Elements**/**Critical Product with
Digital Elements**)", and the form's radio buttons use those expanded labels.
The Glossary's own **Format** cell for the same field still reads "Select one:
Default, Important, Critical".

**Status: open.** Cosmetic, but it is the cell an AR reads to know what the
options are.

### G4 — Two blocks of the form repeat, and no published source says so

The form offers **"+ Add another product"**, **"+ Add another corrective
measure"** and **"+ Add another corrective measure that user can take"**, so a
single notification can carry several products, several corrective measures
taken, and several measures for users. Neither the Glossary, the FAQ nor the guidance pages
mention repetition: every field is documented as though it occurred once. This
changes how a multi-product notification is prepared, and it is not a detail an
AR can infer.

**Status: open.**

### G7 — i36 is capped at 255 characters for an answer the Glossary asks to be two things

The form limits **i36, "Type of threat or root cause that is likely to have
triggered the incident"**, to 255 characters. The Glossary's Format for the
same field is **"Classification plus short explanation"**, and its completion
instruction asks the AR to "state the most likely threat type and root cause
supported by the investigation. Explain the evidence briefly and mark the
conclusion as preliminary when analysis is ongoing."

Classification, evidence and a preliminary-status caveat in 255 characters is
tight. The limit appears nowhere in the Glossary, so an AR drafting from the
published guidance has no way to size the answer before meeting the field.

**Status: open.**

### G8 — The Glossary does not say how precise a timestamp has to be

Both date fields offer **Date, HH and MM** — no seconds. The Glossary's Format
for i37 and i38 is the bare phrase "Date and time". For a field that drives a
24- and 72-hour deadline, whether minutes are the intended granularity, and how
an AR should record a time known only to the hour, is unstated.

**Status: open.** Minor on its own; it compounds G6, since the field feeding the
deadline is also the one whose required precision is undocumented.

### G9 — The Glossary says "leave the field empty"; the control cannot be emptied

**Product class** is documented as optional, and its completion instruction
reads: "Leave the field empty when the product is not classified as important
or critical." In the form it is a pair of **radio buttons**, Class I and
Class II. A radio group has no null state once a button has been pressed: an AR
who clicks the wrong one, or who clicks to see the options, cannot get back to
empty without abandoning the draft.

The same shape applies to **Product type** (Default / Important Product with
Digital Elements / Critical Product with Digital Elements), **End of support
indicator** (Yes / No) and **Mitigating measure expected shortly** (Yes / No) —
all optional per the Glossary, all radio groups, none of them clearable. A
captured form shows "End of support indicator: Yes" selected, and that
selection cannot be withdrawn.

An optional field that cannot be returned to "not answered" is not optional in
practice, and for End of support the difference between "No" and "not stated"
is a statement about the product's support status that the AR may not be in a
position to make.

**Status: open.**

### G10 — The malicious-actor field holds 100 characters and asks for a description

**v27, "Malicious actor that has exploited/is exploiting the vulnerability"**,
is capped at **100 characters** in the form — the tightest limit anywhere in
the notification, and four times tighter than the next.

The Glossary gives its Format as "Free text" and instructs: "You may enter
confirmed information about the malicious actor or observed activity. **If
attribution is unconfirmed, describe the observed activity**…". Describing
observed activity in 100 characters is not possible in any useful sense, and
unconfirmed attribution is the normal case at the 24-hour mark.

Neither the limit nor the tension with the instruction is documented.

**Status: open.**

### G11 — The form carries drafting guidance that exists nowhere else

The **General information** field's placeholder is structured, and prescribes
the answer's shape:

> General information, in particular:
> a. General nature of the vulnerability
> b. General nature of the exploit

That a/b structure appears in no Glossary entry, no FAQ answer and no guidance
page. It is real instruction — arguably the clearest ENISA gives for that
field — and it is visible only to someone already looking at the form, which is
exactly the person who no longer needs to prepare.

**Status: open.** The same applies more weakly to every placeholder carrying a
character limit; see G7 and G10.

### G12 — "Add another corrective measure that user can take"

The repeat control under field 17 reads **"Add another corrective measure that
user can take"** — singular "user", no article, where the field above it reads
"measures that users can take".

**Status: open.** Cosmetic.

### G13 — A required field with no documentation anywhere: "Prerequisites (conditions for exploitation)"

**The most serious item found in the tutorial video.** The running AEV form
carries a field labelled **"Prerequisites (conditions for exploitation)"**,
capped at 4000 characters. It does not appear in the Glossary's 39 fields, the
FAQ, or any guidance page — searched and confirmed absent. Observed twice, on
two separate demo notifications:

- At **Early Warning**, the field carries no Required badge (optional).
- At **72h Notification**, the same field is marked **Required** — confirmed
  on both `SRP-GR-V-2026-00000018` and `SRP-GR-V-2026-00000021`, independently.

An AR preparing a 72-hour notification from the Glossary alone has no way to
know this field exists, let alone that it becomes mandatory. This is a bigger
gap than a wrong label or a tight character limit (compare G1, G6): it is a
whole required field with zero published guidance on what belongs in it.

**Source**: ENISA, *CRA SRP - AR User Tutorial Video*, published 11 September
2026, <https://videos.enisa.europa.eu/w/wS9DBDDiX2mHQZpK85QXNh>, ~03:50
(Early Warning) and ~04:40 / ~07:10 (72h Notification, two notifications).

**Status: open.**

### G14 — A Glossary field documented as "Date and time" offers a date-only control

**v22, "Date when corrective or mitigating measure has been available"**, has
Format **"Date and time"** in the Glossary. The Final Report form offers a
plain calendar date picker — day, month, year — with no time component at all,
unlike i37/i38 (Date, HH, MM) a few fields away in the same form family.

**Status: open.** Source: same tutorial video, ~07:20.

### G15 — "Required if such information available" is indistinguishable from optional on screen

**v27, "Malicious actor..."**, carries the Glossary status **"Required if such
information available"** at Final Report — a third category, distinct from
both "Optional" and plain "Required". On screen it carries **no badge at all**,
the same as an ordinary optional field. An AR cannot tell from the form itself
that this field is meant to be filled whenever the information exists, rather
than left blank at will.

**Status: open.** Source: same tutorial video, ~07:00.

### G16 — Two independent Field 8 confirmations agree; noted for completeness

Not a defect. The tutorial video's registration and product-type screens match
what G3 already reported (the CRA classification names spelled out in full,
the Glossary's Format cell still abbreviated) and the three-field Personal
Details step (no Legal name) already established in F13 — now confirmed by a
second, independent source: an official ENISA video published the same
morning as the AR User Manual screenshots. Folded into G5 rather than restated
here.

### G17 — The Dashboard's tabs are not what the guide's own screenshot shows

The guide's Dashboard screenshot (`if-04-dashboard.png`) is a stale, pre-launch
build — placeholder `(n)` counts and a status badge reading "Approved" rather
than "Active" — and its tabs read **All, Needs Submission, Corrective Measures
Required, Draft, Archive**. The AR User Manual's own Dashboard screenshots
(pp. 32, 34, all showing "Active" status and real dates) carry a different set
entirely: **All, Needs Submission, Corrective Measures Required, Closed
(Previously Valid), Closed (Previously Invalid), Draft**. There is no
"Overdue" tab and no "Archive" tab in the manual's screenshots at all — instead
there are two "Closed" states the guide does not mention anywhere.

**Status: open.** Source: AR User Manual pp. 32, 34 (PDF pages 33, 35), vs.
`img/enisa/if-04-dashboard.png` and the guide's own prose at the Dashboard
step.

### G18 — A two-tier storage split the Glossary and FAQ never mention

Section 4.8 (Update Existing Notification) states plainly that where a
notification lands depends on whether the designated CSIRT has disseminated
it yet: *"If the Notification has not yet been disseminated by the designated
CSIRT, the updated notification data (all fields) are automatically stored
only in the SRP National Endpoint Data Layer and remain only visible to the
designated CSIRT"* — versus, once disseminated, *"stored in the SRP ENISA
Master Data Layer and automatically made visible to ENISA and the concerned
CSIRTs."* Neither "National Endpoint Data Layer" nor "ENISA Master Data
Layer" appears in the Glossary, the FAQ, or anywhere in this guide. An AR has
no way of knowing, from the published sources, that pre-dissemination data
lives in a different store than post-dissemination data.

**Status: open.** Source: AR User Manual p. 48 (PDF page 49), section 4.8.

### G19 — A CSIRT-side screenshot leaked into the AR manual, and it shows more than the AR manual meant to

One screenshot (p. 50, PDF page 51) is not an AR view at all: the profile
badge reads "csirt Greece", and the top nav carries a **"User Management"**
item that never appears in any AR screenshot anywhere else in this manual or
in the guide. Its Alerts list gives the actual alert-text templates, not
paraphrased:

- *"[SRP] Notification Disseminated - SRP-GR-V-2026-00001751 — Notification
  SRP-GR-V-2026-00001751 has been disseminated under CRG by the Designated
  CSIRT GR. The concerned CSIRTs are: CSIRT_FR,CSIRT_IT. The CSIRTs that
  applied a delay are: N/A."*
- *"[SRP] Notification Submitted - SRP-GR-V-2026-00001751 - REPORT_72H — The
  Notification SRP-GR-V-2026-00001751 was submitted."*

The phrase "CSIRTs that applied a delay" confirms a per-CSIRT dissemination
delay mechanism that neither the Glossary nor the FAQ names.

**Status: open.** Source: AR User Manual p. 50 (PDF page 51).

### G20 — Two system role strings, distinct from the guide's own terminology

Registration success sets the account's system role to exactly **"AR Primary
User"**; completing a Secondary/Backup AR registration sets it to exactly
**"AR Backup User"** — both quoted verbatim from the manual (pp. 13, 16-17).
This guide, like the manual's own running prose, otherwise says "Primary AR"
and "Secondary AR" throughout; a report-filer checking their own account
against either published source would not recognise the other pair of terms
as the same thing.

**Status: open.** Source: AR User Manual pp. 13, 16-17 (PDF pages 14, 17-18).

### G21 — An internal user identifier, never screenshotted before, sits in the profile menu

The profile/user dropdown (top right, on every logged-in screen) shows an
"n"-prefixed identifier above the menu items — **"ID: n5590879"** in this
manual's demo account — followed by, in order: **Settings, FAQ, Contact
Support, Logout**. Confirmed identically across three separate screenshots
(pp. 20, 22, 24). Neither the ID nor the menu's existence and item order
appears anywhere in the guide.

**Status: open.** Source: AR User Manual pp. 20, 22, 24 (PDF pages 21, 23, 25).

### G22 — The "You are not Authorised" error screen, verbatim, in both its trigger contexts

Both Section 2 (Registration, p. 12) and Section 3 (Login, p. 19) point to
the same error screen when authentication fails, quoted here in full for the
first time:

> **You are not Authorised**
> It seems like you don't have permission to use this portal. Please sign in
> with a different account.
> [Login a different user]
> If this is an error please Contact Support to report the problem.

**Status: open.** Source: AR User Manual pp. 12, 19 (PDF pages 13, 20).

### G23 — Section 3, "AR User Login & Logout", is not referenced anywhere in this guide

Manual pages 17-20 (PDF pages 18-21) document a whole procedure this guide
has never covered: signing back in to an existing account, and logging out
— *"Click your user identifier or profile menu and select Log Out."* Nothing
here is a defect in the platform; it is a gap in the guide, since a
first-time reader following only this page has no documented way to log out.

**Status: open — guide gap, not a platform defect.** Source: AR User Manual
pp. 17-20 (PDF pages 18-21).

### G24 — What "Closed" actually means, and the rest of the status vocabulary G17 left unexplained

The manual's own FAQ (p. 53-54) defines the four notification-status words
verbatim, and nothing in this guide or in the Glossary/FAQ baselines defines
any of them:

- *"Submitted"* — "the notification has been sent through the SRP and is
  available for the next workflow step."
- *"Valid"* — "the designated CSIRT has reviewed and accepted the
  notification."
- *"Invalid"* — "the designated CSIRT has reviewed the notification and
  marked it as not valid."
- *"Closed"* — "no further action is expected for that notification in the
  current workflow."

This is the missing explanation for G17's two Dashboard tabs, "Closed
(Previously Valid)" and "Closed (Previously Invalid)": a notification is
first judged Valid or Invalid by the CDaC, and then separately becomes
Closed once nothing further is expected of it — the tab name records both
facts at once. Read on its own, G17's tab list gives no hint that "Closed"
is a second, independent axis rather than a third outcome alongside Valid
and Invalid.

**Status: open.** Source: AR User Manual p. 53-54 (PDF pages 54-55), section 6
FAQ.

### G25 — The role-selection landing screen dropped its hover tooltips for a footnote

This guide's own screenshot of the "What User are you?" landing screen
(`reg-01-role-select.png`, captured before go-live) shows each role card
carrying an "(i)" icon; hovering it reveals a short tooltip — "Appointed to
represent the manufacturer for regulations and paperwork." for Assigned
Representative. A live capture of the same screen on 2026-09-14 shows no
hover icons at all: instead, "Assigned Representative" carries an asterisk,
and a single footnote is printed under both cards:

> "For the purposes of the Single Reporting Platform (SRP), an Assigned
> Representative (AR) is the individual who submits notifications according
> to the Cyber Resilience Act (CRA) mandatory reporting obligations set out
> in Articles 14, 16 and/or 24(3) on behalf of the manufacturer or the
> open-source software steward."

Not a wording tweak — a different explanation mechanism (hover vs. static
footnote) and a materially more precise one, citing the specific CRA
articles rather than paraphrasing them. This is a running-platform UI
change, not an ENISA guidance-page edit, so it falls outside everything the
automated monitors track; it surfaced only because it was captured directly.
The exact date of the change between first capture and 2026-09-14 is not
known.

**Status: open** (guide text updated to note the discrepancy; the original
screenshot is kept as the historical capture, not replaced).

### G5 — Confirmed, not defects

Recorded so the record shows what was checked rather than only what was wrong:

- **Additional Information** is optional and capped at 255 characters — see D2.
  The AR User Manual was right and the guidance-page screenshot is a stale
  build.
- **The manufacturer address field is absent** — see D4, and note the
  withdrawal recorded there.
- **CSIRT Designated as Coordinator** is pre-filled and read-only in the
  Manufacturer Details dialog, as the manual describes.
- **Product type** carries no Required badge, matching the Glossary's "Optional"
  at Early Warning.
- **The optional fourth tab, Additional Notes**, is present as documented.
- Field **i32**'s odd comma — "General information, about the nature of the
  incident" — is ENISA's, consistently, in the Glossary and on the form. Not a
  divergence.
- **i38**, "Date and time when the incident occurred (UTC time)", matches the
  Glossary exactly, name and all.
- **i39**, "Initial assessment of the incident", carries no Required badge at
  Early Warning, matching the Glossary's "Optional" for that stage, and its
  4000-character limit is consistent with the other narrative fields.
- **The user-type entry screen** offers two tiles, "I am an Assigned
  Representative" and "I am a CSIRT Representative", before the country
  selector — matching this guide's step&nbsp;2, now confirmed on video rather
  than inferred from a screenshot alone.
- **The three-field Personal Details step** (First Name, Last Name, Email — no
  Legal name) is confirmed a second time, by ENISA's own tutorial video, not
  only the AR User Manual (F13).
- **Notification identifiers** follow the pattern
  `SRP-<country>-<V|I>-<year>-<sequence>`, e.g. `SRP-GR-V-2026-00000018` for a
  vulnerability from Greece. Published nowhere, but consistent across all four
  demo notifications shown.
- **The 48-hours-not-72 counter defect ENISA itself documents** (quoted in
  this guide's own FAQ known-issues section) is not just a documented risk:
  the tutorial video shows it happening twice with real timestamps —
  `SRP-GR-V-2026-00000018`'s Early Warning submitted 04.09.2026 06:00 UTC,
  its 72h Notification shown due 06.09.2026 06:00 UTC (48 hours, not 72); the
  same gap recurs exactly on `SRP-GR-V-2026-00000021` (06:22 UTC to 06:22 UTC
  two days later).
- **The dashboard's "All Filters" panel** offers a Member State multi-select
  plus three checkboxes — Early Warnings, 72h Notifications, Final Reports —
  in addition to the "All Types" dropdown and the tab bar. Not previously
  distinguished from "type of submission" in this guide's own Dashboard note.
- **A PEC submission carries its own status label**, "Submitted Under PEC",
  replacing the plain "Submitted" checkmark on both the dashboard list and the
  notification's own stage tracker — matches this guide's existing PEC
  documentation.
- **The Alerts page's actual wording**, confirmed for the first time:
  "[SRP] AR Association Request - Accepted" / "Your association request with
  a manufacturer has been accepted by the Designated CSIRT." Read state is
  toggled per-alert with "Mark as Read", which greys the icon and clears the
  unread count on the Alerts tab — matching the manual's colour description.
- **Field 17**'s name on the form, "Corrective or mitigating measures that
  users can take", matches the Glossary exactly. An earlier note in this
  repository had the Glossary and the FAQ differing on the word "that"; the
  Glossary now carries it.
- **Member States where product available** is a multi-select, matching the
  Glossary's "Select one or more Member States", and pre-fills the AR's own
  CDaC as the completion instruction describes.
- **CVE ID** and **EUVD ID** are plain text fields, as the Glossary implies; no
  format validation is applied at entry, so "Copy the ID exactly as published"
  is advice the form does not enforce.

---

*Compiled from a public, read-only record of the ENISA SRP pages maintained at
<https://github.com/git-z0man/single-reporting-platform>, which keeps the dated
page text these findings are quoted from.*
