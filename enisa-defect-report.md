# CRA Single Reporting Platform — observed defects and gaps

A list of errors, contradictions and apparent omissions found in the public
ENISA Single Reporting Platform (SRP) pages, compiled so that they can be
passed to ENISA for correction.

**Checked against**: all eight SRP pages plus the CSIRT list, fetched
**9 September 2026, 16:08 UTC** — i.e. after ENISA's edits earlier that day.

| Page | Short name used below | Own version stamp |
|---|---|---|
| [Single Reporting Platform (main)](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp) | Main | — |
| [Frequently Asked Questions](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/frequently-asked-questions) | FAQ | Updated: 09 September 2026 |
| [CRA SRP Glossary](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2) | Glossary | version 1.1, last update: 05/09/2026 |
| [Guidance — AR User registration](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-guidance-ar-user-registration) | Registration | Last updated: 08/09/2026 |
| [Guidance — AR Notification submission and update](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-guidance-ar-notification-submission-and-update) | Submission | Last updated: 3/08/2026 |
| [Guidance — AR Interface functions](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-guidance-ar-interface-functions) | Interface | Last updated: 07/09/2026 |
| [Guidance — Particular Exceptional Circumstances (PEC)](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-guidance-particular-exceptional-circumstances-pec) | PEC | *none* — see D7 |
| [List of CSIRTs Designated as Coordinators](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/list-of-csirts-designated-as-coordinators) | CSIRT list | Updated: 04/09/2026 |

Every item below was re-verified against that fetch and was still present at the
time of writing. Items already corrected by ENISA are deliberately **not**
listed. A few findings come from screenshots published on the guidance pages
rather than from the page text; these are marked *(screenshot)* — no account,
login or form submission was used to obtain anything in this report.

Findings are numbered so that individual points can be referenced in a reply.

---

## A. Typos and wording

Current text is quoted verbatim.

| # | Page | Where | Current text | Suggested correction |
|---|---|---|---|---|
| A1 | Glossary | Field 11 "End of support indicator", instruction column | "…has reached the end of the support period or No when is **doesn't**." | "…or No when it doesn't." |
| A2 | Glossary | Field v26, instruction column | "…state that attribution is unknown (max. 100 characters)**..**" | Single full stop. |
| A3 | Glossary | Field v29, instruction column | "…CSIRT Designated as Coordinator **(CDaC)taking** their decision." | Insert a space: "(CDaC) taking". |
| A4 | Glossary | Field i36, meaning column | "Date and time when the manufacturer or **another relevant become aware** of the incident." | "…or another relevant entity became aware…" |
| A5 | Glossary | Field i37, example column | "…enter the date and time when the incident **was began** or occurred." | "…when the incident began or occurred." |
| A6 | FAQ | Q26, Final Report paragraph | "…one month after submission of the 72-hour **Sever** Incident Notification." | "Severe". |
| A7 | FAQ | Q16, introductory paragraph | "For each field, **it explains that the field means**, how it may be completed…" | "…it explains what the field means…" |
| A8 | FAQ | Q16 table, field 22 | "Corrective or mitigating measures that **user** can take" | "…that users can take" (the Glossary uses the plural). |
| A9 | PEC | Body text | "By toggling the indicator, the PEC Delay **Reson** options will be displayed." | "Reason" — the Glossary (v28) spells it correctly. |
| A10 | PEC | Screenshot of the PEC block *(screenshot)* | "…would be contrary to the essential **intrests** of that Member State" | "interests". This is in the application UI, not only in the guidance. |
| A11 | Interface | "Access the Dashboard" step | "**Yo** can access the Dashboard by:" | "You". |
| A12 | Interface | Section heading | "Add an **Association** with an Additional Manufacturer **Association** through Settings" | "Association" appears twice; drop the second. |
| A13 | Registration | Manufacturer details step | "Enter the manufacturer details (manufacturer name, manufacturer **adress**, additional information)" | "address" — but see D4: that field does not exist. |
| A14 | Registration | Invitation registration, personal details step | "These fields **cannot be edited** but are retrieved from EU Login and **cannot be edited** in the SRP." | The clause is duplicated within one sentence. |
| A15 | Submission | Expected results, 72-hour Notification and Final Report | "…subject to **Particularly Exception** Circumstances (PEC)…" (twice) | "Particular Exceptional Circumstances" — "Exception" is not a valid form. See also C2. |
| A16 | Submission | Pre-conditions, three occurrences | "you are **logged in into** the SRP" | "logged in to the SRP". |

---

## B. Contradictions

These are cases where two statements cannot both be followed. They matter more
than the typos: a reporter acting on one of them acts wrongly.

### B1 — Glossary field 11: the meaning column describes a different field

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

The same field is named two ways:

- FAQ, Q16 table: "**Applied and ongoing** mitigation measures"
- Glossary, field i32: "**Applied or ongoing** mitigation measures"

"And" and "or" are not interchangeable here: one reading requires measures to
be both already applied and still running, the other accepts either.

### B4 — Who receives the invitation email for a Secondary AR

- Interface, "Invite Secondary AR", expected result: "An email is sent to **the
  Primary AR, who instructs the Secondary AR** to complete registration."
- Registration, "Registration via Invitation (Secondary AR)", pre-conditions:
  "**You have received a valid SRP email invitation** initiated by a Primary
  AR"; and step 1: "Click the link in the email invitation."

One page has the invitation going to the inviter, the other to the invitee.
Since the link expires after 7 days, a Secondary AR who waits for an email that
was in fact sent to their Primary AR can lose the invitation.

### B5 — How many notifications before the association is verified

- FAQ, Q9: "ARs whose manufacturer association has not yet been verified may
  submit up to **20 notifications** for that manufacturer before verification
  becomes mandatory."
- Interface, "Add a manufacturer", expected result: "As unverified AR you can
  submit only up to **10 notifications**."

### B6 — "Legal name" is described as non-editable but is editable

Registration states that the pre-filled personal details "(First Name, Last
Name, Email, Legal name) … are retrieved from EU Login and cannot be edited in
the SRP". In the published screenshot of that step *(screenshot)*, First Name,
Last Name and Email are greyed out, while **Legal name is an editable input
field**. Either the text or the form is wrong.

---

## C. Inconsistent naming

Not errors in themselves, but the SRP is a legal reporting tool and users match
guidance to form labels word by word.

| # | Variants in use | Where | Suggestion |
|---|---|---|---|
| C1 | "Full description of the severity/impact" (AEV) vs. "Detailed description of the Severity/Impact" (SI) | Glossary fields v23 and i33; FAQ Q16 table | Same content, two names and two capitalisations. Pick one. |
| C2 | "Particular Exceptional Circumstances" / "Particularly Exceptional Circumstances" / "Particularly Exception Circumstances" | PEC page uses the first and second within a few lines of each other; Submission uses the third | The CRA itself has no defined term here; choose one form and use it everywhere, including the UI label. |
| C3 | "Particular Exceptional Circumstances**(PEC)**" — no space before the bracket *(screenshot)* | The toggle label in the notification form | Insert a space, to match every guidance page. |
| C4 | "validation" vs. "verification" of the AR–manufacturer association | FAQ Q9 uses both in one paragraph ("validation … before **verification** becomes mandatory"); Registration uses "validation"; Interface uses "Unverified" as the status | One term for the act, matching the status name shown in the platform. |
| C5 | Date formats: "3/08/2026", "07/09/2026", "08/09/2026", "09 September 2026", "05/09/2026", "04/09/2026" | Guidance pages, FAQ, Glossary, CSIRT list | Mixed unpadded numeric, padded numeric and long form. Numeric DD/MM is ambiguous to non-European readers; the FAQ's "09 September 2026" is unambiguous. |

---

## D. Apparently missing

### D1 — No Glossary entry for "Legal name"

The registration form asks for **"Legal name (for legal entities)"** and
Registration mentions it, but the Glossary has no entry for it (0 occurrences).
An AR registering as a natural person has nothing telling them whether to leave
it empty.

### D2 — No Glossary entry for "Additional Information", which is mandatory

The Manufacturer Details step of AR registration has a field
**"Additional Information"** marked **"Required field"** *(screenshot)*. The
term does not appear in the Glossary or the FAQ at all. Users must fill in a
mandatory free-text field with no statement of what belongs in it — and this is
the information the CSIRT uses to decide whether to verify the association.

### D3 — The 800-character limit on the PEC justification is not documented

The PEC justification box is labelled "Provide further information (max 800
characters)" *(screenshot)*. Neither the Glossary (field v29) nor the PEC page
states the limit. Compare field v26, where the Glossary does give the limit
("max. 100 characters"). A reporter drafting a justification offline has no way
to know it will be truncated or rejected.

### D4 — Registration describes a manufacturer address field that does not exist

Registration: "Enter the manufacturer details (manufacturer name, manufacturer
adress, additional information)". The published screenshot of that very step
*(screenshot)* shows only **Name**, **CSIRT Designated as Coordinator**
(read-only) and **Additional Information**. There is no address field. Either
the guidance is stale or the field was dropped.

### D5 — No screenshots of the 72-hour and Final Report forms

Submission illustrates the Early Warning flow with six screenshots, one per
step. The "Submit a 72-hour Notification" and "Submit a Final Report" sections
each have a single screenshot — of the Dashboard step that opens the
notification — and none of the tabs where the reporting actually happens. These
are the two submissions with statutory deadlines and, for AEVs, the ones where
PEC applies.

### D6 — The PEC page is missing from the main page's guidance cards

The SRP main page has a "User guidance" block with a card for each guidance
page: AR User registration, AR Notification submission and update, AR Interface
functions. The **PEC guidance page has no card** — it appears only in the
"Content" navigation list. A user browsing the main page will not find it.

### D7 — The PEC page carries no "last updated" stamp

Every other guidance page ends with "Last updated: …". The PEC page has none,
although its content was edited on 9 September 2026. There is no way to tell
which version one is reading.

### D8 — The Glossary is missing from the "Content" navigation

The "Content" list repeated on the FAQ and guidance pages has six entries: FAQ,
the three AR guidance pages, the PEC page and the CSIRT list. The **Glossary is
not among them**, although it is the reference document for every field on
those pages. It is linked from the main page only, so a user reading the
guidance has to navigate back to find it.

---

## E. Page management

### E1 — The old Glossary URL returns 403 with no redirect

The Glossary moved from
`…/single-reporting-platform-srp/cra-srp-glossary` to
`…/cra-srp-glossary2`. Re-checked 9 September 2026, 16:31 UTC: the old path
returns **HTTP 403** and sends no `Location` header. A 403 (rather than 404 or
a 301 to the new address) reads as "you may not see this page" rather than
"this page moved", which is what it actually is. Any bookmark, external link or
citation of the old address is now dead. A redirect to `…2` would fix all of
them at once.

### E2 — Glossary content changed without the version stamp moving

The Glossary footer has read "version 1.1, last update: 05/09/2026" continuously
while its content was edited on the evening of 7 September 2026. The version
number and date are therefore not a reliable indicator of whether a reader has
the current field definitions — which matters for a document that defines
mandatory reporting fields.

---

## The five that matter most

1. **B4** — the invitation email flow contradicts itself, and the link expires
   in 7 days.
2. **B5** — 20 versus 10 notifications before verification becomes mandatory.
3. **D2** — a mandatory registration field with no documentation anywhere.
4. **B1 / B2** — two Glossary fields whose meaning column contradicts their own
   instruction, format and form.
5. **E1 / E2** — the Glossary is hard to cite: the old URL is dead without a
   redirect, and the version stamp does not move when the content does.

---

*Compiled from a public, read-only record of the ENISA SRP pages maintained at
<https://github.com/git-z0man/single-reporting-platform>, which keeps the dated
page text these findings are quoted from.*
