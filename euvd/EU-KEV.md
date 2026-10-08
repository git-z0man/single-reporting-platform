# The EU KEV catalogue in the EUVD

What the EU KEV is, when it appeared in the EUVD, what its dates mean, and whether
its entries can be tied to notifications through the CRA Single Reporting Platform.
Researched on 2026-10-08. Sources are named for every claim; where something could
not be established, this note says so.

**Short answer.** The EU KEV is a catalogue that ENISA keeps with the EU CSIRTs
Network. ENISA says SRP notifications *will* feed it in future. Nothing in its data
shows that any entry so far came from an SRP notification. Every entry added since
the go-live cites a public source. Two entries reported by Ireland's CSIRT fit the
SRP route on paper, and that is all the data supports.

## What it is

ENISA, *Vulnerability Services* (`enisa.europa.eu/topics/vulnerability-services`,
read 2026-10-08; the earliest archived copy carrying the text is from 2026-10-04):

> The EU KEV Catalogue assembles a validated listing of vulnerabilities known to have
> been exploited during attacks targeting entities within the EU. Information about
> confirmed exploitation activity is provided by EU CSIRTs Network members and ENISA,
> and will be further enriched by reports received from manufacturers and open-source
> software stewards through the CRA SRP. Known exploitation information provided via
> the EU KEV Catalogue is synchronised with the European Vulnerability Database (EUVD).

The SRP sentence is in the future tense. CIRCL's Vulnerability-Lookup, which tracks KEV
catalogues independently (`vulnerability.circl.lu/kev-catalogs`), lists it as "ENISA":
65 entries on 2026-10-08, described as "a list of known-exploited vulnerabilities
observed across the CSIRTs network", evidence type "CSIRT report" for all of them.

The EUVD names `https://github.com/enisaeu/EUKEV` as the catalogue's source (field
`kevSource.sourceUrl`). That repository is **not public**: `git ls-remote` asks for
credentials.

## When it appeared in the EUVD

| When | What | Evidence |
|---|---|---|
| 2025-07-11 to 07-16 | A sample file `Enisa_known_exploited_vulnerabilities.csv` with the columns `cveID,dateAdded,originSource` and placeholder rows (origins `ENISA`, `CSIRT`) sits in ENISA's docs repository for five days | `enisaeu/euvd-docs-public`, commits `19ad944` and `9d36dbb` |
| between 2025-05-27 and 2025-10-16 | The EUVD frontend gains the `fromKEVDate`/`toKEVDate` search filter | archived frontend bundles (Internet Archive) |
| between 2026-03-11 and 2026-03-25 | The frontend starts calling `/api/kevEntries` and documents `/api/kev/dump` with the source label `eu_kev` | archived bundles `d88db289` (without) and `652ee0b4` (with) |
| 2026-05-04 | The archived KEV dump already holds **25 EU KEV entries** under the label `eukev_kev` | Internet Archive copy of `/api/kev/dump` |
| between 2026-06-09 and 2026-06-19 | Entry pages get an "Exploitation Insights" box showing CISA KEV, EU KEV and honeypot sightings side by side | archived bundles `43ce1891` and `f2862759` |
| 2026-06-19 | ENISA's API documentation describes the KEV dump as "Consolidated Known Exploited Vulnerabilities from CISA KEV and ENISA EU KEV sources" | `euvd-docs-public`, commit `b4407e7` |
| 2026-09-17 | The documentation's source label is corrected from `eu_kev` to `eukev_kev` (ticket ENISASUP-805); the API had used `eukev_kev` since at least 4 May | `euvd-docs-public`, commit `69b20aa` |

The web interface never shows `originSource`, only the API does. All 30 distinct
archived bundles were read; the one from 2026-03-24, inside the March window, is held
by the archive only as an error page, so that window cannot be narrowed further.

## What its dates show

On 2026-10-08 the EUVD lists **73** EU KEV entries (`/api/kevEntries/batch`, the
`EUKEV` record of each). The `dateAdded` values run from **17 January 2025** to
**7 October 2026**:

| Month | Entries | | Month | Entries |
|---|---|---|---|---|
| 2025-01 | 12 | | 2026-04 | 6 |
| 2025-02 | 1 | | 2026-05 | 1 |
| 2025-07 | 5 | | 2026-06 | 1 |
| 2025-09 | 1 | | 2026-07 | 4 |
| 2026-01 | 4 | | 2026-08 | 12 |
| 2026-03 | 1 | | 2026-09 | 21 |
| | | | 2026-10 | 4 |

- **Dates older than the catalogue's appearance in the EUVD.** 23 entries carry dates
  before 11 March 2026, the earliest window in which the frontend shows any EU KEV code.
  Either the catalogue existed elsewhere before (the private `EUKEV` repository; the July
  2025 sample file), or dates were assigned retroactively.
- **Back-dating is documented.** Five entries dated **8 April 2026** (`EUVD-2025-9646`,
  `-14387`, `-14388`, `-200983`, `-23309`, all from the CSIRTs Network) were not EU KEV
  entries in the dump of 4 May 2026. They were added later with an earlier date.
  `EUVD-2026-75010` (dated 25 September) first appeared on 7 October. **`dateAdded` is not
  the day an entry entered the catalogue.**
- **The dump's `dateAdded` is the earliest date across catalogues**, so for an entry in
  both catalogues it is usually CISA's. Only `/api/kevEntries` gives the EU KEV's own date.
- The current baseline once said the EU KEV "took its first entry on 27 April 2026". That
  is the latest date in the 4 May dump, not the first; corrected in the baseline.

## Could entries come from SRP notifications?

### What would be expected if they did

A manufacturer notifies through the SRP, and the notification goes to the CSIRT
designated as coordinator of the Member State of its **main establishment**: the place
where cybersecurity decisions on its products are mainly taken (CRA Art. 14(7), as
ENISA's FAQ reproduced in the guide explains). ENISA's EUVD FAQ adds that reported data
is published in the EUVD only "after a security update or another form of corrective or
mitigating measure is available … in agreement with the product manufacturer"
(`euvd-docs-public`, `faq.md`). So an SRP-sourced entry would (a) appear after the fix,
(b) most likely carry the coordinator CSIRT of the vendor's main establishment as its
origin, and (c) possibly have no earlier public report.

### What the 18 entries since the go-live show

| EU KEV date | Entry | Origin | Vendor (seat, where checked) | CRA route would be | Public source in `notes` |
|---|---|---|---|---|---|
| 09-21 | 45279, 45280 | ENISA | WordPress Foundation (US) | depends on EU representative | GreyNoise blog |
| 09-22 | 75009, 84375 | ENISA | Check Point (IL) | depends on EU representative | Check Point blog |
| 09-22 | 84296 | **CSIRT-IE** | Arista Networks (US; Irish subsidiaries exist, main establishment not verified) | NCSC-IE if Ireland | Arista advisory |
| 09-22 | 84427 | ENISA | F5 (US) | depends | F5 advisory |
| 09-23 | 84555 | NCSC-NL | WordPress Foundation (US) | depends | NCSC-NL alert |
| 09-25 | 56431 | **CSIRT-IE** | Microsoft (EU main establishment Ireland under GDPR) | NCSC-IE | MSRC advisory |
| 09-25 | 75010 | CSIRTs Network | Check Point (IL) | depends | Check Point support article |
| 09-27 | 87958, 87959 | CSIRTs Network | Citrix (US) | depends | Citrix advisory |
| 09-27 | 72027 | CERT-PL | MikroTik (Riga, LV) | **CERT.LV**, not CERT-PL | CERT-PL research post |
| 09-30 | 90080, 90081 | NCSC-NL | Zammad GmbH (Berlin, DE) | **CERT-Bund**, not NCSC-NL | NCSC-NL alert |
| 10-01 | 67861 | ENISA | JFrog (IL/US) | depends | Wiz blog |
| 10-01 | 91042 | CSIRTs Network | Fortinet (US) | depends | FortiGuard advisory |
| 10-02 | 92065 | CSIRTs Network | Citrix (US) | depends | Citrix advisory |
| 10-07 | 22589 | CSIRTs Network | Microsoft | NCSC-IE | MSRC advisory (CISA listed it in April) |

CSIRT-IE is the CSIRT of Ireland's National Cyber Security Centre; the coordinator list
in `srp-domains-baseline.md` names it NCSC-IE.

Reading the table:

- **Every entry cites a public source**: a vendor advisory, a CSIRT alert or a research
  blog. That is how a catalogue built from CSIRT and public reporting looks. It is not
  what a confidential SRP notification would produce, unless the public advisory
  followed and was cited instead.
- **Two routes contradict the CRA rule.** MikroTik sits in Latvia, Zammad in Germany. A
  manufacturer's own notification would have gone to CERT.LV and CERT-Bund, not to
  CERT-PL and NCSC-NL. Both origins match those CSIRTs' own public posts, so these are
  CSIRT findings, not SRP notifications.
- **Two routes match it on paper.** CSIRT-IE appears as an origin only after the go-live,
  for Microsoft (EU main establishment in Ireland, at least for data protection) and Arista
  (Irish subsidiaries; main establishment not verified). That is what an SRP notification
  would look like. It is equally what an Irish CSIRT relaying a vendor advisory would look
  like, and both entries cite public vendor advisories released the same day CISA listed
  them.
- **"ENISA" and "CSIRTs Network" origins** say nothing about the route, and both were
  already common before the go-live (9 and 26 entries).
- **Timing does not help.** Of the 30 entries both catalogues have listed since August
  2026, the EU KEV was first for 10, level for 10 and later for 10, and its dates can be
  back-dated.

### What would settle it

- ENISA saying which entries, if any, come from SRP notifications, or an `originSource`
  value that names the SRP.
- An EU KEV entry whose `notes` cite no public source, or a manufacturer advisory that
  says it was notified under the CRA.
- Access to the `enisaeu/EUKEV` repository's history, which would show when entries were
  really added.

## Monitoring

The EUVD monitor (`euvd/check_exploited.py`, `euvd/build_stats.py`) already records each
entry's EU KEV and CISA dates and the `originSource`, and lists candidates. What it does
not do yet:

- record the day an EU KEV entry **first appears**, which would catch back-dating as it
  happens;
- compare the origin CSIRT with the coordinator of the vendor's main establishment;
- watch the *Vulnerability Services* page, whose SRP sentence may change from "will be" to
  "is".
