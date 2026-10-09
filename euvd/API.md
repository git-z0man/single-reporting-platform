# EUVD API notes

What the EU Vulnerability Database serves, which parts ENISA documents, and which
parts only its own web page uses. Checked on 2026-10-07 against
`https://euvdservices.enisa.europa.eu/api`. The undocumented endpoints can change
without notice; `euvd/check_exploited.py` treats an incomplete or unparseable answer
as a failed check, never as a content change.

## Where this comes from

- **The documentation**: <https://euvd.enisa.europa.eu/apidoc>, a page that renders
  `apidoc.md` from <https://github.com/enisaeu/euvd-docs-public>. That repository
  holds only three prose pages (`apidoc.md`, `faq.md`, `about.md`), no code or schema.
- **The frontend bundle** `https://euvd.enisa.europa.eu/static/js/main.<hash>.js`
  (hash `bdd2ef30` today). Every call the web page makes is a `fetch(base + path)`
  there, and the API documentation page's endpoint table is data in the same file.
- **No OpenAPI schema.** `/v3/api-docs`, `/api-docs`, `/swagger-ui.html` and
  `/actuator/health` all return 404.
- **Guessing paths does not work.** About 25 plausible names (`stats`, `vendors`,
  `products`, `honeypot`, `trends`, ...) answered 403 (only the three `/dump...`
  guesses gave 404), which looks like an
  allow-list in front of the service rather than a missing route. Anything not in
  the frontend bundle was therefore not found, which is not proof that it does not exist.

## Documented (listed on the API page)

| Endpoint | Returns | Notes |
|---|---|---|
| `/api/lastvulnerabilities` | latest entries | at most 8 |
| `/api/exploitedvulnerabilities` | latest exploited entries | **at most 8**, so unusable for a full list |
| `/api/criticalvulnerabilities` | latest critical entries | at most 8 |
| `/api/search` | filtered entries, `{"items": [...], "total": n}` | `size` up to 100, `page` from 0 |
| `/api/enisaid?id=EUVD-...` | one full record | products, vendors, vulnerabilities, advisories |
| `/api/advisory?id=...` | one advisory | |
| `/api/dump/cve-euvd-mapping` | CSV `euvd_id,cve_id` | about 11.6 MB, 384,152 rows, refreshed 07:00 UTC |
| `/api/kev/dump` | JSON list of known-exploited CVEs | about 260 KB, 1,746 entries, refreshed 07:00 UTC |

`/api/search` parameters (documented): `fromScore`, `toScore`, `fromEpss`, `toEpss`,
`fromDate`, `toDate`, `fromUpdatedDate`, `toUpdatedDate`, `product`, `vendor`,
`assigner`, `exploited`, `text`, `page`, `size`. The web page also sends `advisory`
and **`fromKEVDate` / `toKEVDate`**, which the API page does not list but which work
(they select entries by the day a KEV catalogue added them).

`/api/kev/dump` entry: `cveId`, `euvdId`, `dateAdded` (the earliest day across all
sources), `sources` (`cisa_kev`, `eukev_kev`). It has no vendor and no per-source date.

## Undocumented (used by the web page)

| Endpoint | Returns |
|---|---|
| `/api/kevEntries?cveId=CVE-...` | list of KEV entries for one CVE |
| `/api/kevEntries/batch?ids=EUVD-...,EUVD-...` | `{euvdId: [KEV entries]}`; 40 ids per call work |
| `/api/honeypotObservations?cveId=CVE-...` | list of sensor observations for one CVE |
| `/api/honeypotObservations/batch?ids=...` | `{euvdId: [observations]}`; 50 ids per call work |
| `/api/assigners/names` | list of assigner names: ENISA, NCSC-FI, NCSC-NL, CERT-PL, SK-CERT, INCIBE, CIRCL |
| `/api/banner` | `{"enabled": false, "message": "."}` |

**KEV entry** (`kevEntries`): `id`, `cveId`, `kevSource` (`code` `CISA` or `EUKEV`,
`displayName`, `tooltip`, `sourceUrl`), `dateAdded`, and for EU KEV entries also
`vendorProject`, `product`, `originSource` (for example `NCSC-NL`), `shortDescription`,
`notes`. This is where each catalogue's own date lives; the dump only has the earliest.

**Honeypot observation** (`source` is `shadowserver`): `cveId`, `firstSeenAt`,
`lastSeenAt`, `connections1d`, `uniqueIps1d`, `avg7d`, `avg30d`, `avg90d`, `vendor`,
`product`, `vulnClass`, `vulnSeverity`, `cisaKevFlag`, `trend` (`UPTICK`, `STEADY`,
`DECLINE`), `isNew`. Entries the sensors have only first seen carry just `firstSeenAt`,
`trend` and `isNew`. About 330 of 1,746 exploited entries have any observation. There
is **no history**: only today's count and three averages. The `trend` rule is not documented. In the data of
2026-10-09, `connections1d / avg7d` was at least 2.4 for every `UPTICK`, about 1 for
`STEADY` and at most 0.3 for `DECLINE`: a one-day comparison with the week, which flags 50
or more entries on a normal day. Since 2026-10-09 `euvd/build_stats.py` records
`[connections1d, uniqueIps1d, trend, avg30d]` per entry and day in `euvd/history.jsonl`
(earlier lines hold the connections only) and derives stricter "surges" from it.

**Record** (`enisaid`): `id`, `enisaUuid`, `description`, `datePublished`, `dateUpdated`,
`baseScore`, `baseScoreVersion`, `baseScoreVector`, `references`, `aliases`, `assigner`,
`epss`, `exploitedSince`, `enisaIdProduct`, `enisaIdVendor`, `enisaIdVulnerability`,
`enisaIdAdvisory`. The advisories are CSAF documents from CERTs and vendors
(`csaf_certbund`, `csaf_ncscnl`, `csaf_redhat`, `csaf_suse`, ...), each with `id`,
`description`, `summary`, `datePublished`, `dateUpdated`, `references`, `aliases`,
`source` and `advisoryProduct`.

## Counting without downloading

Every `/api/search` answer carries `total`, the number of matching records, so a
query with `size=1` counts anything the filters can express: records per month
(`fromDate`/`toDate`, the publication date), per assigner (`assigner=CERTVDE`; the
value is the CNA's short name, `CERT@VDE` returns 0), critical ones
(`fromScore=9&toScore=10`) or exploited ones (`exploited=true`). The whole EUVD held
401,624 records on 2026-10-07. Counting 25 months for 16 series took 400 requests and
about two minutes; a daily run only needs the current month.

**No browser access.** The API answers 403 to any request carrying a foreign
`Origin` header (no CORS for other sites), so a page cannot query it live from the
reader's browser. Every figure on the page has to be computed in advance by the
daily run.

## What the data cannot give

- **No history anywhere.** Honeypot counts, EPSS, scores and the exploited set are only
  served as of today. Time series have to be recorded by the monitor from now on.
- **No reporting route.** Nothing says how an entry reached ENISA. The "SRP candidates"
  in `euvd-exploited-baseline.md` are indications computed from KEV dates, nothing more.
- **`exploitedSince` is a date, and for most entries it equals CISA's `dateAdded`.**

## Related, not used

CIRCL's Vulnerability-Lookup (the software the EUVD is built on) has a public API with
vulnerability sightings and statistics (`https://vulnerability.circl.lu/api/`). It
answered from here but is not read by the monitor.

The live charts are `euvd/stats.html`, rebuilt daily by `euvd/build_stats.py` (data in `euvd/stats.json`, renderer `euvd/charts.js`). The first drafts remain in `euvd/mockups/`: see `euvd/mockups/index.html` for the charts these data support (pre-rendered, no JavaScript needed) and `euvd/mockups/live.html` for the same page drawn in the browser from the embedded data, the way the live page would draw from `euvd/stats.json`.
