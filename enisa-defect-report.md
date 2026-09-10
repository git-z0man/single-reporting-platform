# CRA Single Reporting Platform — observed defects and gaps

A list of errors, contradictions and apparent omissions found in the public
ENISA Single Reporting Platform (SRP) pages, compiled so that they can be
passed to ENISA for correction.

**Checked against**: all eight SRP pages plus the CSIRT list, fetched
**9 September 2026, 16:08 UTC** — i.e. after ENISA's edits earlier that day.

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
| A13 | Registration | Manufacturer details step | "Enter the manufacturer details (manufacturer name, manufacturer **adress**, additional information)" | "address" — but see D4: that field does not exist. | **fixed** · 2026-09-09 22:12 UTC — now "address"; the field itself is still missing, see D4 |
| A14 | Registration | Invitation registration, personal details step | "These fields **cannot be edited** but are retrieved from EU Login and **cannot be edited** in the SRP." | The clause is duplicated within one sentence. | **fixed** · 2026-09-09 22:12 UTC — now "These fields are retrieved from EU Login and cannot be edited in the SRP." |
| A15 | Submission | Expected results, 72-hour Notification and Final Report | "…subject to **Particularly Exception** Circumstances (PEC)…" (twice) | "Particular Exceptional Circumstances" — "Exception" is not a valid form. See also C2. | **open** — three occurrences now, after the Submission page was rewritten on 9 September 22:12 UTC |
| A16 | Submission | Pre-conditions, three occurrences | "you are **logged in into** the SRP" | "logged in to the SRP". | **open** — still three occurrences |

---

## B. Contradictions

These are cases where two statements cannot both be followed. They matter more
than the typos: a reporter acting on one of them acts wrongly.

### B1 — Glossary field 11: the meaning column describes a different field

**Status: open** — meaning column unchanged on 10 September.

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

**Status: open** — both columns unchanged on 10 September.

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

**Status: partly · 2026-09-09 22:12 UTC** — the Primary AR flow now lists only "First Name, Last Name, Email", so its sentence is true. The Secondary AR flow still lists all four, Legal name included, as "retrieved from EU Login and cannot be edited". The AR User Manual (10 September) settles which is current: its screenshots of both flows show three fields and no Legal name at all, so the Secondary-flow text and the guidance page's screenshot are stale (F13).

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

**Status: partly · 2026-09-10 11:52 UTC** — resolved by removal rather than documentation: the AR User Manual's own screenshots of the personal-details step (Primary and invitation flows alike) show **three fields — First Name, Last Name, Email** — and its text lists the same three. The field appears to have been dropped from the platform. The guidance page's screenshot and its Secondary-AR text still show it, so the web page is now the stale one (F13).

The registration form asks for **"Legal name (for legal entities)"** and
Registration mentions it, but the Glossary has no entry for it (0 occurrences).
An AR registering as a natural person has nothing telling them whether to leave
it empty.

### D2 — No Glossary entry for "Additional Information", which is mandatory

**Status: partly · 2026-09-10 11:52 UTC** — still documented nowhere, but no longer mandatory: the AR User Manual calls it optional, and the manual's newer screenshot of the step shows the field **without** the "Required field" badge that ENISA's guidance-page screenshot carries. The badge on the guidance page is the older state (F13). What belongs in the field remains unexplained.

The Manufacturer Details step of AR registration has a field
**"Additional Information"** marked **"Required field"** *(screenshot)*. The
term does not appear in the Glossary or the FAQ at all. Users must fill in a
mandatory free-text field with no statement of what belongs in it — and this is
the information the CSIRT uses to decide whether to verify the association.

### D3 — The 800-character limit on the PEC justification is not documented

**Status: open** — the limit appears in neither the Glossary nor the PEC page on 10 September, nor in the AR User Manual (0 hits for "800").

The PEC justification box is labelled "Provide further information (max 800
characters)" *(screenshot)*. Neither the Glossary (field v29) nor the PEC page
states the limit. Compare field v26, where the Glossary does give the limit
("max. 100 characters"). A reporter drafting a justification offline has no way
to know it will be truncated or rejected.

### D4 — Registration describes a manufacturer address field that does not exist

**Status: open** — the typo is fixed (A13) but the text still lists "manufacturer address" for a screen that has no address field.

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

Of the 37 findings, **13 are fixed, 7 partly addressed, 17 open** as of
10 September 2026, 11:52 UTC.

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
| F8 | Interface | Manufacturer-details screenshot *(screenshot)* | The manufacturer record is labelled "Manufacturer **Addresss**" (three s), and its *Manufacturer Address* row shows "Manufacturer Sector" as its value. The same screenshot shows the manufacturer record *does* have an address field — which the registration form lacks (D4). | on the page since at least 2026-09-07 |
| F9 | Main | "User Guidance" block, User Manual card | The card's download link is `href="https://CRA SRP – AR User Manual"` — the document's title in place of a URL. The link is dead; the manual is reachable only through the Content navigation. | 2026-09-10 11:52 |
| F10 | Manual / Registration form | Manual §2.1 step 6 vs the form *(screenshot)* | Manual: "Enter the manufacturer details, including Manufacturer Name and Additional Information **(optional)**". The form marks Additional Information **"Required field"**. On closer reading not a contradiction but a version gap: the manual's own screenshot of the step shows the field **without** the badge. The guidance page's "Required field" screenshot is the older state (F13). **Partly** — D2 adjusted accordingly. | 2026-09-10 11:52 |
| F11 | Manual | Cover and page headers vs Document History | Every page says "Version: 1.1"; the Document History table lists a single entry, "09/09/2026 v1.0 First version". Either the history is missing 1.1 or the stamp is wrong. | 2026-09-10 11:52 |
| F12 | FAQ | Q9 vs Q28 | Q9's opening sentence regressed from "The SRP is available at: https://portal.cra-srp.enisa.europa.eu" to "**The SRP will be available in due time**" — the day before the 11 September go-live that Q4, Q28 and Q29 still commit to. Q28 still gives the URL. | 2026-09-10 09:09 |
| F13 | Registration (guidance page) vs AR User Manual | Both screenshots of the registration steps | The guidance page's screenshots (uploaded 7 September) show a **"Legal name (for legal entities)"** field and Additional Information badged **"Required field"**. The manual's screenshots of the same steps (9 September) show neither: three personal fields, no badge. The manual's text matches its screenshots; the guidance page's Secondary-AR text still lists four fields. The guidance page is documenting a previous build of the form. | 2026-09-10 11:52 |

---

*Compiled from a public, read-only record of the ENISA SRP pages maintained at
<https://github.com/git-z0man/single-reporting-platform>, which keeps the dated
page text these findings are quoted from.*
