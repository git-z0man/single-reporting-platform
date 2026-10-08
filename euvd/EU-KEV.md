# The EU KEV catalogue in the EUVD

What the EU KEV is, when it appeared in the EUVD, what its dates mean, and whether
its entries can be tied to notifications through the CRA Single Reporting Platform.
Researched on 2026-10-08. Sources are named for every claim; where something could
not be established, this note says so.

**Short answer.** The EU KEV is a catalogue that ENISA keeps with the EU CSIRTs
Network. ENISA says SRP notifications *will* feed it. Nothing public says which entry,
if any, came from one. **If the route does run**, the EUVD's own insertion order dates
its start: **22 September 2026**, eleven days after the go-live. From then on the EU KEV
took most manufacturers' newly disclosed exploited vulnerabilities within days, after
taking nothing for twelve days. The first entry in the shape the CRA route predicts,
from the coordinator CSIRT of the manufacturer's main establishment, is Arista's
`EUVD-2026-84296` (CSIRT-IE). It was inserted between 27 and 29 September and dated 22
September.

## What it is

ENISA, *Vulnerability Services* (`enisa.europa.eu/topics/vulnerability-services`,
read 2026-10-08; the same paragraph is in the Internet Archive's earliest copy, of
2026-09-21, and in its copy of 2026-10-04):

> The EU KEV Catalogue assembles a validated listing of vulnerabilities known to have
> been exploited during attacks targeting entities within the EU. Information about
> confirmed exploitation activity is provided by EU CSIRTs Network members and ENISA,
> and will be further enriched by reports received from manufacturers and open-source
> software stewards through the CRA SRP. Known exploitation information provided via
> the EU KEV Catalogue is synchronised with the European Vulnerability Database (EUVD).

The SRP sentence is in the future tense. The page probably went online with ENISA's
reorganised topic taxonomy: the SRP pages moved under its `vulnerability-services` path
on 2026-09-19 (`enisa-srp-faq-baseline.md`). The ENISA monitor tracks the page from
2026-10-08 for this sentence. CIRCL's Vulnerability-Lookup, which tracks KEV catalogues
independently (`vulnerability.circl.lu/kev-catalogs`), lists the catalogue as "ENISA": 65
entries on 2026-10-08, described as "a list of known-exploited vulnerabilities observed
across the CSIRTs network", evidence type "CSIRT report" for all of them.

The EUVD names `https://github.com/enisaeu/EUKEV` as the catalogue's source (field
`kevSource.sourceUrl`). That repository is **not public**: `git ls-remote` asks for
credentials. ENISA's SRP launch notice of 11 September 2026 does not mention the EU KEV or
the EUVD at all.

## The insertion clock

The EU KEV's own date (`dateAdded`) can be set to any day, so it cannot tell when an entry
arrived. The EUVD's row numbers can. `/api/kevEntries` returns, for every KEV record, an
internal `id`: one sequence for both catalogues, counting up as rows are inserted.

- Rows 1 to 1551 are CISA's whole catalogue up to 20 March 2026, re-inserted in no
  particular order: the KEV table was rebuilt on or after that day.
- From row 1576 on, CISA rows arrive one day at a time, in the order of CISA's
  `dateAdded`. Of 184 such rows, one pair is out of order, by one day. Three numbers are
  missing (1583, 1589, 1618): deleted rows.
- An EU KEV row numbered after a CISA row cannot have been inserted before CISA added
  that entry. The latest CISA date below it is therefore a **hard lower bound** for its
  insertion. The next CISA date above it is an upper bound, provided the EUVD imports a
  CISA entry the day CISA adds it, which the order of the rows suggests.

By this clock the first **24** EU KEV rows (1552 to 1575) were inserted together, between
20 and 26 March 2026, right after the rebuild. 49 rows followed.

## When it appeared in the EUVD

| When | What | Evidence |
|---|---|---|
| 2025-07-11 to 07-16 | A sample file `Enisa_known_exploited_vulnerabilities.csv` with the columns `cveID,dateAdded,originSource` and placeholder rows (origins `ENISA`, `CSIRT`) sits in ENISA's docs repository for five days | `enisaeu/euvd-docs-public`, commits `19ad944` and `9d36dbb` |
| between 2025-05-27 and 2025-10-16 | The EUVD frontend gains the `fromKEVDate`/`toKEVDate` search filter | archived frontend bundles (Internet Archive) |
| between 2026-03-11 and 2026-03-25 | The frontend starts calling `/api/kevEntries` and documents `/api/kev/dump` with the source label `eu_kev` | archived bundles `d88db289` (without) and `652ee0b4` (with) |
| between 2026-03-20 and 2026-03-26 | The KEV table is rebuilt and the first 24 EU KEV rows are inserted | insertion clock |
| 2026-05-04 | The archived KEV dump holds **25 EU KEV entries** under the label `eukev_kev` | Internet Archive copy of `/api/kev/dump` |
| between 2026-06-09 and 2026-06-19 | Entry pages get an "Exploitation Insights" box showing CISA KEV, EU KEV and honeypot sightings side by side | archived bundles `43ce1891` and `f2862759` |
| 2026-06-19 | ENISA's API documentation describes the KEV dump as "Consolidated Known Exploited Vulnerabilities from CISA KEV and ENISA EU KEV sources" | `euvd-docs-public`, commit `b4407e7` |
| 2026-09-17 | The documentation's source label is corrected from `eu_kev` to `eukev_kev` (ticket ENISASUP-805); the API had used `eukev_kev` since at least 4 May | `euvd-docs-public`, commit `69b20aa` |
| 2026-09-10 to 09-22 | No EU KEV row is inserted | insertion clock |
| from 2026-09-22 | The EU KEV takes most newly disclosed exploited vulnerabilities within days (see below) | insertion clock, CISA catalogue |

The web interface never shows `originSource`, only the API does. All 30 distinct archived
bundles were read; the one from 2026-03-24 is held by the archive only as an error page.

## What its dates show

On 2026-10-08 the EUVD lists **73** EU KEV entries. Their `dateAdded` values run from
**17 January 2025** to **7 October 2026**:

| Month | Entries | | Month | Entries |
|---|---|---|---|---|
| 2025-01 | 12 | | 2026-04 | 6 |
| 2025-02 | 1 | | 2026-05 | 1 |
| 2025-07 | 5 | | 2026-06 | 1 |
| 2025-09 | 1 | | 2026-07 | 4 |
| 2026-01 | 4 | | 2026-08 | 12 |
| 2026-03 | 1 | | 2026-09 | 21 |
| | | | 2026-10 | 4 |

- **The 23 dates before March 2026 belong to the initial import.** The first 24 rows were
  inserted in late March with dates going back to January 2025, presumably carried over
  from the private `EUKEV` repository.
- **Back-dating is routine.** Of the 49 rows inserted after the initial import, **21**
  carry a date at least one day before their insertion. The five dated **8 April 2026**
  (`EUVD-2025-9646`, `-14387`, `-14388`, `-200983`, `-23309`) were inserted on 1 or 2 June,
  54 days later, which is why the dump of 4 May did not have them. Since the go-live:
  `EUVD-2026-84296` 5 days, `-56431` and `-84555` 2 days, `-45279` and `-45280` 1 day,
  `-75010` (dated 25 September, inserted on or after 4 October) at least 9 days.
  **`dateAdded` is not the day an entry entered the catalogue.**
- **The dump's `dateAdded` is the earliest date across catalogues**, so for an entry in
  both catalogues it is usually CISA's. Only `/api/kevEntries` gives the EU KEV's own date.
- **Origins changed spelling in mid-August**: `cnw` became `CNW` and `CERT-PL` became
  `CERT.PL`, and `ENISA` first appears as an origin on 11 August. That is a change in how
  entries are entered, a month before the go-live; it has nothing to do with the SRP.
- The baseline once said the EU KEV "took its first entry on 27 April 2026". That is the
  latest date in the 4 May dump, not the first; corrected in the baseline.

## Could entries come from SRP notifications?

### What would be expected if they did

A manufacturer notifies through the SRP, and the notification goes to the CSIRT
designated as coordinator of the Member State of its **main establishment**: the place
where cybersecurity decisions on its products are mainly taken (CRA Art. 14(7), as
ENISA's FAQ reproduced in the guide explains). ENISA receives it at the same moment.
The manufacturer must also inform the users (Art. 14(8)), which is usually a public
advisory. ENISA's EUVD FAQ adds that reported data is published in the EUVD only "after a
security update or another form of corrective or mitigating measure is available … in
agreement with the product manufacturer" (`euvd-docs-public`, `faq.md`). A manufacturer
need not report exploitation it knew of before 11 September 2026 (ENISA's SRP FAQ Q13,
citing the Commission's CRA FAQ, subsections 5.1 and 5.3).

So an SRP-sourced entry would (a) appear only after the go-live and after the fix,
(b) concern exploitation first known after 11 September, (c) most likely carry the
coordinator CSIRT of the vendor's main establishment, or ENISA, as its origin, and
(d) cite the vendor's own advisory.

### What the 18 entries inserted since the go-live show

| Inserted | EU KEV date | Entry | Origin | Vendor (seat, where checked) | CRA route would be | Public source in `notes` |
|---|---|---|---|---|---|---|
| 09-22 to 09-24 | 09-21 | 45279, 45280 | ENISA | WordPress Foundation (US) | depends on EU representative | GreyNoise, Wiz (CISA listed both in July) |
| 09-22 to 09-24 | 09-22 | 75009, 84375 | ENISA | Check Point (IL) | depends | Check Point blog |
| 09-22 to 09-24 | 09-22 | 84427 | ENISA | F5 (US) | depends | F5 advisory |
| 09-25 | 09-23 | 84555 | NCSC-NL | WordPress Foundation (US) | depends | NCSC-NL alert |
| 09-25 to 09-27 | 09-27 | 72027 | CERT.PL | MikroTik (Riga, LV) | **CERT.LV**, not CERT.PL | CERT-PL research post |
| 09-27 to 09-29 | 09-22 | 84296 | **CSIRT-IE** | Arista Networks (US; Irish subsidiaries exist, main establishment not verified) | NCSC-IE if Ireland | Arista advisory |
| 09-27 to 09-29 | 09-27 | 87958, 87959 | CNW | Citrix (US) | depends | Citrix advisory |
| 09-27 to 09-29 | 09-25 | 56431 | **CSIRT-IE** | Microsoft (EU main establishment Ireland under GDPR) | NCSC-IE | MSRC advisory |
| 09-30 to 10-01 | 09-30 | 90080, 90081 | NCSC-NL | Zammad GmbH (Berlin, DE) | **CERT-Bund**, not NCSC-NL | NCSC-NL alert |
| 09-30 to 10-01 | 10-01 | 67861 | ENISA | JFrog (IL/US) | depends | Wiz blog (CISA listed it on 2 September) |
| 10-01 to 10-02 | 10-01 | 91042 | CNW | Fortinet (US) | depends | FortiGuard advisory |
| 10-02 to 10-04 | 10-02 | 92065 | CNW | Citrix (US) | depends | Citrix advisory |
| from 10-04 | 09-25 | 75010 | CNW | Check Point (IL) | depends | Check Point support article |
| from 10-04 | 10-07 | 22589 | CNW | Microsoft | NCSC-IE | MSRC advisory (CISA listed it in April) |

CSIRT-IE is the CSIRT of Ireland's National Cyber Security Centre; the coordinator list
in `srp-domains-baseline.md` names it NCSC-IE. CNW is the EUVD's code for the CSIRTs
Network as a whole.

- **Every entry cites a public source.** For the SRP route that is expected rather than
  contrary: the vendor's advisory to its users is the public trace of a notification.
- **Two routes contradict the CRA rule.** MikroTik sits in Latvia, Zammad in Germany. A
  manufacturer's own notification would have gone to CERT.LV and CERT-Bund, not to
  CERT.PL and NCSC-NL. Both origins match those CSIRTs' own public posts, so these are
  CSIRT findings.
- **Two routes match it.** CSIRT-IE appears as an origin only after the go-live, for
  Microsoft (EU main establishment in Ireland, at least for data protection) and Arista
  (Irish subsidiaries; main establishment not verified). That is what an SRP notification
  would look like. It is equally what an Irish CSIRT relaying a vendor advisory would look
  like.
- **"ENISA" and "CNW" origins** say nothing about the route. Both were common before the
  go-live (9 and 26 entries), and ENISA receives every SRP notification anyway.
- **An early EU KEV date is weak evidence.** Several "EU KEV before CISA" cases are
  back-dating: `EUVD-2026-84555` is dated two days before CISA but was inserted on CISA's
  day. Genuinely earlier by the clock: Zammad (inserted 30 September or 1 October, CISA
  2 October), and before the go-live MikroTik, VMware and Zimbra. Citrix `92065` was
  inserted before CISA's row for it, possibly on the same day.

## If the SRP route does feed it: when did it start?

The question here takes as given that SRP notifications reach the EU KEV, as ENISA says
they will, and asks from when the data shows it. The SRP gives ENISA, within 24 hours,
every exploited vulnerability that a manufacturer discloses. Once the route runs, the
EU KEV should therefore start taking such vulnerabilities systematically, soon after the
vendor's fix and advisory. CISA's catalogue records them independently and serves as the
yardstick.

**Share of CISA's new entries that the EU KEV also lists** (CISA catalogue 2026.10.04,
EU KEV as of 2026-10-08):

| CISA added | CISA entries | Also in the EU KEV |
|---|---|---|
| 1 June to 10 September 2026 | 98 | 16 (16 %) |
| 11 to 21 September | 12 | **0** |
| 22 September to 4 October | 17 | **13 (76 %)** |

The recent period had the least time to catch up, so the jump is not a backlog effect. By
the insertion clock the EU KEV took **no row at all** between the Cisco rows of 9 or 10
September and 22 September. Insertions resumed between 22 and 24 September with Check Point
(twice) and F5, within two days of the day the vendor disclosed them and CISA listed them,
alongside two WordPress catch-ups from July. Between 27 and 29 September came the first rows
from **CSIRT-IE**: Arista (dated 22 September) and Microsoft (dated 25 September), two to
seven days after the vendor's advisory. That leaves room for a 72-hour notification and the
CSIRT's processing.

Under the assumption, then:

- **The route starts on 22 September 2026.** Nothing in the data supports an earlier start:
  in the eleven days from the go-live CISA listed 12 new exploited vulnerabilities,
  including two each from Cisco and JFrog and one each from Google (Pixel), GitLab and
  ConnectWise, and the EU KEV took none.
- **The first entry in the CRA route's own shape** (coordinator CSIRT of the main
  establishment, vendor advisory, after the fix) is `EUVD-2026-84296`, Arista VeloCloud
  Orchestrator, CVE-2026-93952, origin CSIRT-IE. It was inserted between 27 and 29
  September and dated 22 September. `EUVD-2026-56431` (Microsoft SharePoint,
  CVE-2026-65660, also CSIRT-IE) followed in the same batch.
- **Not everything arrives.** Since 22 September CISA listed four that the EU KEV lacks so
  far: WSO2 and Adobe Commerce (24 September), Apple (29 September) and Cisco Catalyst
  SD-WAN Manager (30 September). Apple and Cisco are manufacturers the SRP covers. Possible
  reasons: exploitation known before 11 September, manufacturer agreement still pending,
  or simple lag.

What the data cannot exclude: on 22 September ENISA may simply have begun tracking vendors'
zero-day advisories itself, with no notification involved. That would leave the same rows.
The two are hard to tell apart, since the notification and the vendor's advisory to users
arrive within a day of each other. Only ENISA, or an `originSource` that names the SRP, can
settle it.

## What would settle it

- ENISA saying which entries, if any, come from SRP notifications, or an `originSource`
  value that names the SRP.
- The *Vulnerability Services* page changing "will be further enriched" to the present tense.
- An EU KEV entry whose `notes` cite no public source, or a manufacturer advisory that
  says it was notified under the CRA.
- Access to the `enisaeu/EUKEV` repository's history.

## Monitoring

Since 2026-10-08:

- The EUVD monitor keeps the **EU KEV register** `euvd/eukev.json` (`euvd/eukev.py`, run by
  `euvd/check_exploited.py`): every EU KEV entry with the day the monitor first saw it, the
  check before that which did not list it, and its insertion window by the clock above. A
  new entry, a moved date, a removed entry and an origin never seen before are each
  reported. The baseline lists the register's entries from 1 September on.
- The ENISA monitor tracks the *Vulnerability Services* page as its twelfth page and reports
  any change to the EU KEV paragraph first.

Not done: comparing an origin with the coordinator of the vendor's main establishment. That
needs each vendor's main establishment, which no public register gives; the monitor's report
says it where a public source makes it clear.
