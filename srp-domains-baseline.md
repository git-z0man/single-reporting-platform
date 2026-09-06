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
last_check: 2026-09-06
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
| Last check | 2026-09-06 |
| Last change | 2026-09-06 (baseline created) |

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

One host per Member State (EU-27). The CSIRT column is the **expected**
operator, to be confirmed per instance at go-live — see "Verification after
go-live". `Status` is `angenommen` until a live endpoint proves it, then
`verifiziert` or `korrigiert`.

| Code | Land | Nationales CSIRT (erwartet) | Host | Status | Belegt am |
|------|------|------------------------------|------|--------|-----------|
| at | Österreich | CERT.at / GovCERT Austria | `at.cra-srp.enisa.europa.eu` | angenommen | — |
| be | Belgien | CERT.be (Centre for Cybersecurity Belgium, CCB) | `be.cra-srp.enisa.europa.eu` | angenommen | — |
| bg | Bulgarien | CERT Bulgaria (National CERT) | `bg.cra-srp.enisa.europa.eu` | angenommen | — |
| cy | Zypern | National CSIRT-CY | `cy.cra-srp.enisa.europa.eu` | angenommen | — |
| cz | Tschechien | GovCERT.CZ (NÚKIB) | `cz.cra-srp.enisa.europa.eu` | angenommen | — |
| de | Deutschland | CERT-Bund (BSI) | `de.cra-srp.enisa.europa.eu` | angenommen | — |
| dk | Dänemark | CFCS / DKCERT (Center for Cybersikkerhed) | `dk.cra-srp.enisa.europa.eu` | angenommen | — |
| ee | Estland | CERT-EE (RIA) | `ee.cra-srp.enisa.europa.eu` | angenommen | — |
| es | Spanien | INCIBE-CERT / CCN-CERT | `es.cra-srp.enisa.europa.eu` | angenommen | — |
| fi | Finnland | NCSC-FI (Traficom) | `fi.cra-srp.enisa.europa.eu` | angenommen | — |
| fr | Frankreich | CERT-FR (ANSSI) | `fr.cra-srp.enisa.europa.eu` | angenommen | — |
| gr | Griechenland | National CSIRT Greece (NCSA) | `gr.cra-srp.enisa.europa.eu` | angenommen | — |
| hr | Kroatien | CERT.hr (CARNET) / ZSIS | `hr.cra-srp.enisa.europa.eu` | angenommen | — |
| hu | Ungarn | NKI (National Cyber Security Center Hungary) | `hu.cra-srp.enisa.europa.eu` | angenommen | — |
| ie | Irland | NCSC-IE / CSIRT-IE | `ie.cra-srp.enisa.europa.eu` | angenommen | — |
| it | Italien | CSIRT Italia (ACN) | `it.cra-srp.enisa.europa.eu` | angenommen | — |
| lt | Litauen | NKSC / CERT-LT | `lt.cra-srp.enisa.europa.eu` | angenommen | — |
| lu | Luxemburg | CIRCL / GOVCERT.LU | `lu.cra-srp.enisa.europa.eu` | angenommen | — |
| lv | Lettland | CERT.LV | `lv.cra-srp.enisa.europa.eu` | angenommen | — |
| mt | Malta | CSIRTMalta | `mt.cra-srp.enisa.europa.eu` | angenommen | — |
| nl | Niederlande | NCSC-NL | `nl.cra-srp.enisa.europa.eu` | angenommen | — |
| pl | Polen | CSIRT NASK | `pl.cra-srp.enisa.europa.eu` | angenommen | — |
| pt | Portugal | CERT.PT (CNCS) | `pt.cra-srp.enisa.europa.eu` | angenommen | — |
| ro | Rumänien | DNSC (vormals CERT-RO) | `ro.cra-srp.enisa.europa.eu` | angenommen | — |
| se | Schweden | CERT-SE (MSB) | `se.cra-srp.enisa.europa.eu` | angenommen | — |
| si | Slowenien | SI-CERT | `si.cra-srp.enisa.europa.eu` | angenommen | — |
| sk | Slowakei | SK-CERT (NBÚ) | `sk.cra-srp.enisa.europa.eu` | angenommen | — |

For the countries with more than one candidate CSIRT (ES, CZ, HR, GR, IE) the
endpoint actually served at go-live decides; the assumed value is kept as a
footnote if it turns out wrong.

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
| DNS failure | `NXDOMAIN` | host not in the zone |
| exit 56 + `403` | `BLOCKED` | egress policy denied CONNECT — the check was blind; **not** a statement about the platform |

`BLOCKED` is deliberately distinct: it means the monitor could not see, which
must never be recorded as "the SRP is down" or as a go-live.

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
   selection. If it exposes a selector, the real country → endpoint mapping is
   extracted from it and **overrides** the assumed table above.
2. **SSO** — the identity provider behind `auth.…` (EU Login / Keycloak /
   other), from redirect target, page title, or login branding.
3. **Per country** — the actual CSIRT per live instance, from page title,
   branding, imprint, redirect target, or TLS certificate SAN.
4. **Backend separation** — whether each country host serves a distinct
   instance or one shared application behind the anycast pair, from differing
   TLS SANs, `Server`/`Set-Cookie` headers, redirect targets, or page identity.
5. **Evidence** — the deciding signal per host is stored in
   `srp-domains/evidence/<host>.txt` so every mapping stays checkable.

## Delta history

### 2026-09-06 — baseline created

All 29 production hosts resolve to the WEDOS edge; none answers HTTP. Zone
delegation, edge chain and the country table recorded from operator input, with
the DNS state verified host by host. Two findings beyond the supplied data:
`test-cra-srp.enisa.europa.eu` (test zone apex) resolves to `195.251.97.116`
and was not previously recorded; and a TLS handshake cannot be used as the
go-live signal in the monitoring environment, so liveness is decided on HTTP.
