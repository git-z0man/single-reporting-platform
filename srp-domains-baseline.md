---
source: ENISA — CRA Single Reporting Platform (SRP), production DNS zone
zone: cra-srp.enisa.europa.eu
edge: 185.8.236.7 / 185.8.236.8 (WEDOS Global, CZ — filtering anycast proxy, not the origin)
test_zone: test-cra-srp.enisa.europa.eu
state: srp-domains/ (manifest.json, status.md, reachability-log.csv, evidence/)
check: srp-domains/check.sh
expected_go_live: 2026-09-11
retrieved: 2026-09-06
purpose: Reachability baseline for the SRP production environment. The routine re-checks all 29 hosts, records the first successful HTTP response per host, detects new hosts appearing in the zone, and verifies the assumed country-to-CSIRT mapping once the platform answers.
note: Only an HTTP status code relayed from upstream counts as live. TCP and TLS are recorded but are forged by an intercepting egress proxy in the monitoring environment — see "Why a TLS handshake is not evidence" below.
last_check: 2026-09-09
last_change: 2026-09-06
---

# CRA SRP — Production domain reachability baseline

The reporting obligation under CRA Article 14 applies from **11 September
2026**. The production zone is fully provisioned and access-filtered: DNS
resolves for every host, but the edge drops connections from non-allowlisted
source IPs. This page is the baseline that the reachability routine updates
when that changes.

## Current state

| | |
|---|---|
| Hosts watched | **29** (portal, auth, 27 Member State instances) |
| Live | **0 / 29** |
| Zone | `cra-srp.enisa.europa.eu` — independently delegated |
| Edge | `185.8.236.7`, `185.8.236.8` (WEDOS Global, CZ) |
| State | provisioned, not yet released |
| Expected go-live | in the coming days, at the latest **11 September 2026** |
| Last check | 2026-09-09 |
| Last change | 2026-09-07 (country → CSIRT mapping verified) |

Live per-host detail: [`srp-domains/status.md`](srp-domains/status.md).

## Naming scheme

Final scheme is `<function|country-code>.cra-srp.enisa.europa.eu`.

| Host | Role |
|---|---|
| `portal.cra-srp.enisa.europa.eu` | front door — portal/relay to the national CSIRT |
| `auth.cra-srp.enisa.europa.eu` | SSO / identity provider |
| `<cc>.cra-srp.enisa.europa.eu` | one instance per Member State (27) |

The earlier candidate name **`crasrp.eu` was discarded** — confirmed NXDOMAIN
on 2026-09-06, as is `cra-srp.eu`.

## Infrastructure

**Zone delegation.** `cra-srp.enisa.europa.eu` is delegated separately from
`enisa.europa.eu`, to Azure DNS: `ns1-02.azure-dns.com`, `ns2-02.azure-dns.net`,
`ns3-02.azure-dns.org`, `ns4-02.azure-dns.info`.

**Edge.** Each country code carries its **own host label**, pointed by a WEDOS
Global CNAME —
`<cc>.cra-srp.enisa.europa.eu` → `<cc>.cra-srp.enisa.europa.eu.wedos.global` —
at the shared anycast pair `185.8.236.7` / `185.8.236.8` (WEDOS, CZ), which
provides DDoS protection and WAF.

That pair is **an upstream proxy/CDN with active access filtering, not the
origin server.** All 29 labels resolving to the same two addresses therefore
says nothing about how many backends exist behind them. One endpoint per
Member State matches the decentralised reporting model of the CRA SRP; whether
a separate backend actually runs per country can only be verified after
go-live, from behind the edge. Recorded as an open question, not an assumption.

> **Verification status.** The delegation and the CNAME chain are
> operator-supplied and were **not** verified in the monitoring environment —
> it has no `dig`/`host` and the Python stdlib cannot query NS or CNAME
> records. The A records were verified host by host. To confirm the rest:
>
> ```
> dig NS cra-srp.enisa.europa.eu +short
> dig CNAME de.cra-srp.enisa.europa.eu +short
> ```

## Member State instances

One host per Member State (EU-27). The CSIRT column is the **authoritative**
operator, taken from ENISA's published [List of CSIRTs Designated as
Coordinators](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/list-of-csirts-designated-as-coordinators) (page dated 04/09/2026, retrieved 2026-09-07) — not from the
hosts themselves, which are still dark. `Status` is `verifiziert` where the
official list confirms the value assumed when this baseline was created, and
`korrigiert` where it does not; the superseded assumption is kept in a
footnote. Per-country evidence is in `srp-domains/evidence/<host>.txt`.

| Code | Land | CSIRT designated as coordinator | Host | Status | Belegt am |
|------|------|----------------------------------|------|--------|-----------|
| at | Österreich | CERT.at | `at.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| be | Belgien | CCB / CERT.be | `be.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| bg | Bulgarien | GovCERT.bg[^1] | `bg.cra-srp.enisa.europa.eu` | korrigiert | 2026-09-07 |
| cy | Zypern | CSIRT-CY | `cy.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| cz | Tschechien | NÚKIB (GovCERT.CZ) | `cz.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| de | Deutschland | CERT-Bund (BSI) | `de.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| dk | Dänemark | CFCS (Center for Cybersikkerhed)[^2] | `dk.cra-srp.enisa.europa.eu` | korrigiert | 2026-09-07 |
| ee | Estland | CERT-EE (RIA) | `ee.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| es | Spanien | INCIBE-CERT[^3] | `es.cra-srp.enisa.europa.eu` | korrigiert | 2026-09-07 |
| fi | Finnland | NCSC-FI (Traficom) | `fi.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| fr | Frankreich | CERT-FR (ANSSI) | `fr.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| gr | Griechenland | National Cybersecurity Authority (cyber.gov.gr)[^4] | `gr.cra-srp.enisa.europa.eu` | korrigiert | 2026-09-07 |
| hr | Kroatien | CERT.hr (CARNET)[^5] | `hr.cra-srp.enisa.europa.eu` | korrigiert | 2026-09-07 |
| hu | Ungarn | NCSC Hungary[^6] | `hu.cra-srp.enisa.europa.eu` | korrigiert | 2026-09-07 |
| ie | Irland | NCSC-IE | `ie.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| it | Italien | CSIRT Italia (ACN) | `it.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| lt | Litauen | NKSC[^7] | `lt.cra-srp.enisa.europa.eu` | korrigiert | 2026-09-07 |
| lu | Luxemburg | CIRCL[^8] | `lu.cra-srp.enisa.europa.eu` | korrigiert | 2026-09-07 |
| lv | Lettland | CERT.LV | `lv.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| mt | Malta | CSIRTMalta (MITA) | `mt.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| nl | Niederlande | NCSC-NL | `nl.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| pl | Polen | CERT.PL (NASK) | `pl.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| pt | Portugal | CERT.PT (CNCS) | `pt.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| ro | Rumänien | DNSC | `ro.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| se | Schweden | CERT-SE (MSB) | `se.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| si | Slowenien | SI-CERT | `si.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |
| sk | Slowakei | SK-CERT (NBÚ) | `sk.cra-srp.enisa.europa.eu` | verifiziert | 2026-09-07 |

The countries that had more than one candidate CSIRT are now resolved from the
official list: **ES** → INCIBE-CERT (CCN-CERT is not the coordinator), **HR** →
CERT.hr (not ZSIS), **LT** → NKSC, **LU** → CIRCL, **DK** → CFCS (not DKCERT).
**CZ** (NÚKIB/GovCERT.CZ) and **IE** (NCSC-IE) confirmed as assumed.

Footnotes — the value assumed on 2026-09-06 and superseded by the official list:

[^1]: was assumed to be *CERT Bulgaria (National CERT)*.
[^2]: was assumed to be *CFCS / DKCERT*.
[^3]: was assumed to be *INCIBE-CERT / CCN-CERT*.
[^4]: was assumed to be *National CSIRT Greece (NCSA)*.
[^5]: was assumed to be *CERT.hr (CARNET) / ZSIS*.
[^6]: was assumed to be *NKI (National Cyber Security Center Hungary)*.
[^7]: was assumed to be *NKSC / CERT-LT*.
[^8]: was assumed to be *CIRCL / GOVCERT.LU*.

## Current reachability

Measured 2026-09-06 across all 29 hosts:

- **DNS resolves** for every host, all to `185.8.236.7` + `185.8.236.8`.
- **TCP 443 and 80 accept.**
- **The TLS handshake is dropped**, from a non-allowlisted source IP.

So the platform is **provisioned but not released**. No host has ever returned
an HTTP status code; `first_live` is `null` for all 29.

### Why a TLS handshake is not evidence of launch

The monitoring environment routes egress through an intercepting proxy, and
that proxy terminates TCP and TLS *itself*, before knowing whether the upstream
host works. Measured there on 2026-09-06:

- TCP connect succeeds even to `240.0.0.1`, a reserved unroutable address.
- The TLS handshake completes against **all 29 SRP hosts — while the platform
  is dark** — presenting a certificate issued by
  `Anthropic / Egress Gateway SDS Issuing CA (production)`. The same happens
  for `example.com` and `www.enisa.europa.eu`.

A check that treated a completed handshake as go-live would therefore report
all 29 hosts live on its first run and every run after. `check.sh` decides
liveness **only** on an HTTP status code relayed from upstream, and classifies
on curl's exit code:

| curl result | Recorded state | Meaning |
|---|---|---|
| HTTP status returned | `LIVE` | upstream answered — go-live |
| exit 35 / 28 / 7 / 52 | `PROVISIONED` | connected, upstream dropped the handshake |
| DNS: fast negative answer | `NXDOMAIN` | resolver confirmed no such name/record |
| DNS: resolver never answered | `DNS_TIMEOUT` | the check was blind; **not** a statement about the platform |
| exit 56 + `403` | `BLOCKED` | egress policy denied CONNECT — the check was blind; **not** a statement about the platform |

`BLOCKED` and `DNS_TIMEOUT` are deliberately distinct: both mean the monitor
could not see, which must never be recorded as "the SRP is down" or as a
go-live. See the 2026-09-08 delta history entry below for the incident that
made this distinction necessary.

## Test environment

| Host | Address | Notes |
|---|---|---|
| `de.test-cra-srp.enisa.europa.eu` | `195.251.97.115` | German test instance |
| `test-cra-srp.enisa.europa.eu` | `195.251.97.116` | zone apex — **found 2026-09-06**, not previously recorded |

Hosted at GRNET / Greece (ENISA hosting), delegated separately
(`ns*-04.azure-dns.*`), access by IP filter. Not part of the 29 watched
production hosts; recorded so a change here is not mistaken for production.

## Names that do not exist

Verified NXDOMAIN/NODATA on 2026-09-06. Kept as a negative baseline so that one
of them *starting* to resolve is itself a detectable change.

`cra-srp.enisa.europa.eu` (the apex itself) · `srp.enisa.europa.eu` ·
`cra.enisa.europa.eu` · `crasrp.enisa.europa.eu` · `crasrp.eu` · `cra-srp.eu` ·
and under `cra-srp.enisa.europa.eu`: `www.` `app.` `home.` `gateway.` `relay.`
`login.` `report.`

## Verification after go-live

Dormant while every host is `PROVISIONED`. Once any host returns an HTTP code,
the routine additionally confirms, using **only publicly visible signals — no
login attempts, no form input, no authentication**:

1. **Portal** — that `portal.…` is the entry point with country/CSIRT
   selection. If it exposes a selector, extract the real country → endpoint
   mapping and cross-check it against the table above. That table is already
   verified against ENISA's official coordinator list, so a divergence here
   means the platform disagrees with ENISA's own published list — worth
   flagging rather than silently overwriting.
2. **SSO** — the identity provider behind `auth.…` (EU Login / Keycloak /
   other), from redirect target, page title, or login branding.
3. **Per country** — cross-check the CSIRT each live instance actually
   serves (page title, branding, imprint, redirect target, TLS SAN) against
   the verified table. No longer the open question it was: the mapping is
   settled from ENISA's official list, so this step only catches an
   implementation that departs from it.
4. **Backend separation** — whether each country host serves a distinct
   instance or one shared application behind the anycast pair, from differing
   TLS SANs, `Server`/`Set-Cookie` headers, redirect targets, or page identity.
5. **Evidence** — the deciding signal per host is stored in
   `srp-domains/evidence/<host>.txt` so every mapping stays checkable.

## Delta history

### 2026-09-09 02:04 UTC (vs. the DNS_TIMEOUT reading, 2026-09-09 00:22 UTC)

Follow-up to yesterday's `DNS_TIMEOUT` fix: bounding the local resolver calls
stopped the false NXDOMAIN, but `getent`/`socket.getaddrinfo` (the fallback
used since `dig` is absent from this image) kept hanging on every one of the
29 hosts regardless, so two consecutive runs recorded `DNS_TIMEOUT` across the
board and the monitor stayed blind. `curl`, run directly against the same
hosts in the same sessions, resolved and connected to all 29 in about a
second every time.

**Fixed** — `check.sh` no longer lets a hung local lookup skip the probe: it
always attempts the `curl` HTTP fetch that already decides `LIVE`/
`PROVISIONED`/`BLOCKED`, and now also decides `NXDOMAIN` (curl exit 6) from
that same attempt. `DNS_TIMEOUT` still exists as a fallback, but only fires
when curl's own attempt times out too (exit 28) — it is no longer the default
outcome whenever the local resolver hangs. `resolve()`/`getent`/`python3` are
kept only to populate the informational "Resolves to" column.
**Unchanged** — reachability itself: still 0/29 live, all `PROVISIONED`, with
this run's `last_checked` timestamps now genuinely current rather than stale
behind two days of `DNS_TIMEOUT`. CSIRT coordinator list re-checked against
ENISA's page (200 OK, 27 rows) — matches the table above exactly, no changes.

### 2026-09-08 23:54 UTC (vs. the last confirmed reading, 2026-09-08 00:30 UTC)

`check.sh`'s DNS resolver calls had no timeout. When this run's monitoring
environment stopped getting an answer for the zone's real records, that
silently read as NXDOMAIN for all 29 hosts, and the run looked like the
entire production zone had vanished. It had not.

**Fixed** — `resolve()` now bounds every DNS lookup with `timeout` and
reports `DNS_TIMEOUT` distinctly from a genuine negative answer;
`manifest.json` now excludes `BLOCKED`/`DNS_TIMEOUT` from ever overwriting a
host's last confirmed state or counting as a platform change.
**Watch** — with the fix applied, all 29 hosts still read `DNS_TIMEOUT` this
run. A confirmed nonexistent name under the same zone
(`www.cra-srp.enisa.europa.eu`) answers in under a second; the 29 monitored
hosts, which had resolved fine 23 hours earlier, do not answer at all. This
looks like a resolution problem specific to this monitoring environment's
path to the zone's real records, not a platform withdrawal — but it has now
held across two consecutive runs and needs watching.
**Unchanged** — reachability per host: still 0/29 live, all `PROVISIONED`,
same as 2026-09-06. Country → CSIRT mapping: re-checked against ENISA's list
(still dated 04/09/2026), no discrepancies.

### 2026-09-07 — country → CSIRT mapping verified against ENISA's official list

ENISA published a **List of CSIRTs Designated as Coordinators** (page dated
04/09/2026), found by the ENISA SRP FAQ monitor in the same pass that took the
FAQ from 23 to 27 questions. It is the authoritative country → CSIRT mapping
and it settles the table above **without waiting for go-live**, which is what
the original plan had assumed would be necessary.

Of the 27 assumptions recorded on 2026-09-06: **19 confirmed, 8 corrected.**

| Code | Assumed | Actual |
|---|---|---|
| bg | CERT Bulgaria (National CERT) | **GovCERT.bg** |
| dk | CFCS / DKCERT | **CFCS (Center for Cybersikkerhed)** |
| es | INCIBE-CERT / CCN-CERT | **INCIBE-CERT** |
| gr | National CSIRT Greece (NCSA) | **National Cybersecurity Authority (cyber.gov.gr)** |
| hr | CERT.hr (CARNET) / ZSIS | **CERT.hr (CARNET)** |
| hu | NKI (National Cyber Security Center Hungary) | **NCSC Hungary** |
| lt | NKSC / CERT-LT | **NKSC** |
| lu | CIRCL / GOVCERT.LU | **CIRCL** |

Most corrections drop a second candidate that turned out not to be the
coordinator (DK, ES, HR, LT, LU); BG, GR and HU name a different body
altogether. Evidence per country is stored under `srp-domains/evidence/`.

The reachability state is unchanged: still **0/29 live**, all `PROVISIONED`.
The remaining go-live verification steps — portal role, SSO provider, and
whether each country host has its own backend behind the shared anycast edge —
are untouched by this and still need the platform to answer.

### 2026-09-06 — baseline created

All 29 production hosts resolve to the WEDOS edge; none answers HTTP. Zone
delegation, edge chain and the country table recorded from operator input, with
the DNS state verified host by host. Two findings beyond the supplied data:
`test-cra-srp.enisa.europa.eu` (test zone apex) resolves to `195.251.97.116`
and was not previously recorded; and a TLS handshake cannot be used as the
go-live signal in the monitoring environment, so liveness is decided on HTTP.
