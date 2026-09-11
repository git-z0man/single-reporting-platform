# SRP production domain monitor

Reachability monitoring for the CRA Single Reporting Platform production zone
`cra-srp.enisa.europa.eu` — the third monitor in this repository, alongside the
ENISA SRP FAQ baseline and the Commission CRA FAQ version check.

Overview page: [`srp-domains-baseline.md`](../srp-domains-baseline.md)

## Layout

```
srp-domains/
  check.sh              the check — bash + curl, no other dependencies
  manifest.json         zone, delegation, edge, and per-host state
  status.md             overwritten each run: current table + "X/29 live"
  reachability-log.csv  append-only history, one row per host per run
  evidence/             per-host proof of the CSIRT mapping, filled at go-live
```

## What it watches

29 hosts: `portal`, `auth`, and the 27 Member State instances
`<cc>.cra-srp.enisa.europa.eu`. Four stages per host — DNS, TCP 443, TLS
handshake, HTTP status.

## The detection signal

**Only an HTTP status code relayed from upstream counts as live.** Everything
below HTTP can be forged by an intercepting proxy, and in the Claude Code cloud
environment it *is*:

- TCP connect succeeds even to `240.0.0.1`, a reserved unroutable address.
- The TLS handshake completes against all 29 SRP hosts while the platform is
  dark, presenting a certificate issued by
  `Anthropic / Egress Gateway SDS Issuing CA (production)` — the same
  certificate `example.com` and `www.enisa.europa.eu` get.

So a check that treats a completed handshake as go-live reports all 29 hosts
live on its first run and stays wrong forever. `check.sh` decides on HTTP and
classifies by curl's exit code:

| curl result | State | Meaning |
|---|---|---|
| HTTP status returned, body is the SRP origin | `LIVE` | upstream answered — go-live |
| HTTP status returned, body is WEDOS's own error page | `EDGE_BLOCKED` | the edge answered, not the SRP origin |
| exit 35 / 28 / 7 / 52 | `PROVISIONED` | connected, upstream dropped |
| exit 6 | `NXDOMAIN` | curl itself could not resolve the host |
| exit 28, local DNS also hung | `DNS_TIMEOUT` | nothing answered in time — the check was blind |
| exit 56 + `403` | `BLOCKED` | egress policy denied CONNECT — the check was blind |

`BLOCKED` and `DNS_TIMEOUT` are kept distinct on purpose: both mean the
monitor could not see, and must never be recorded as a platform state or
overwrite the last confirmed one. `first_live` is only ever set from an HTTP
response classified `LIVE`, so a proxied run cannot manufacture a go-live —
and, since 2026-09-11, neither can the edge's own error page.

**2026-09-11** — a run got a real HTTP response, with a genuine Sectigo
certificate (no proxy forgery), from 28 of 29 hosts: HTTP 456 on all of them.
That is exactly the signal this monitor exists to catch, and for a moment it
looked like the go-live. The response body said otherwise: every one was
WEDOS's own templated error page ("WEDOS.protection – 404 Not Found"),
generated entirely at the edge — its diagnostic block read `Server: - /
ip_denied`, an empty origin field, meaning the request never reached the SRP
application. A second run eight minutes later, and several manual checks in
between, mostly got the old TLS-drop (`PROVISIONED`) for the same hosts, with
only `portal` answering this way consistently. A genuine public launch does
not flap between 28/29 "live" and 0/29 within minutes with no origin content
ever served; an edge access rule that sometimes answers with a decoy 404
instead of dropping the connection does. So `check.sh` now inspects the body
and headers of any HTTP response before trusting it: a response carrying the
`x-protected-by: ... WEDOS ...` header and `WEDOS.protection` branding in the
body is classified `EDGE_BLOCKED`, not `LIVE` — real (unlike `BLOCKED`/
`DNS_TIMEOUT`, the check did see something), but not a platform signal, so it
never sets `first_live` and never counts toward the live tally.

Both `NXDOMAIN` and `DNS_TIMEOUT` are decided from curl's own attempt during
the same HTTP probe that already decides `LIVE`/`PROVISIONED`/`BLOCKED` — not
from a separate DNS lookup gating the whole host. Two incidents established
why:

- **2026-09-08** — `resolve()` called `getent`/`python3` with no timeout at
  all. When this run's environment stopped getting an answer for the zone's
  real records, the hang silently read as an empty result, indistinguishable
  from a genuine negative, and all 29 hosts were recorded NXDOMAIN — as if
  the entire production zone had vanished overnight. It had not: a control
  lookup of a name confirmed not to exist under the zone answered in under a
  second, while the 29 monitored hosts (which had resolved fine hours
  earlier) hung for 40+ seconds with nothing back.
- **2026-09-09**, the day after that fix landed — bounding `resolve()` with
  `timeout` and adding the distinct `DNS_TIMEOUT` state stopped the false
  NXDOMAIN, but `getent`/`python3` (the fallback used since `dig` is absent
  from this image) kept hanging on every host regardless, so two consecutive
  runs recorded `DNS_TIMEOUT` across the board and the monitor stayed blind.
  `curl`, run directly against the same 29 hosts in the same sessions,
  resolved and connected to all of them in about a second every time.

So the check now always attempts the `curl` probe, even when `resolve()`
itself timed out, and only falls back to `DNS_TIMEOUT` when curl's own
attempt also fails to get an answer (exit 28). `resolve()` still runs,
`timeout`-bounded, purely to populate the informational "Resolves to"
column — it never gates classification.

When it detects a proxy (`HTTPS_PROXY` set, or an `Anthropic` certificate
issuer) the run records `trust=proxied` and reports the TCP and TLS columns as
`unreliable` rather than pretending they mean something.

## Running it

```bash
bash srp-domains/check.sh            # full output
bash srp-domains/check.sh --quiet    # only the summary
```

Exit code: `0` no state change, `1` at least one host changed state (the
routine commits a delta), `2` error.

It takes a few minutes — 29 hosts, each with a 20 s ceiling, all currently
timing out at the TLS stage.

### Two places to run it, and what each tells you

- **As the scheduled cloud routine** — detects the **public** launch. A real
  HTTP response from an arbitrary IP means the allowlist has been lifted. This
  is what the Routine does.
- **From your own allowlisted IP** — a local `cron`/`launchd` entry runs the
  identical script and additionally tells you whether *your* access works
  before the public launch. There TCP and TLS are meaningful and the run
  records `trust=direct`.

## Verification after go-live

Dormant until a host reports `LIVE`. Then the routine confirms the portal's
role, identifies the SSO provider, and cross-checks the CSIRT each country
instance actually serves against the verified table in the baseline.

The country → CSIRT mapping itself is **already settled** as of 2026-09-07,
from ENISA's published [List of CSIRTs Designated as
Coordinators](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/list-of-csirts-designated-as-coordinators)
— 19 of the original 27 assumptions confirmed, 8 corrected. It did not need
the platform to go live. Per-country evidence is in `evidence/`. What remains
open is whether the running platform's CSIRT assignment agrees with that list:
the go-live check on 2026-09-11 confirmed the routing only — each host
redirects to its own correctly-scoped country client, with no cross-wiring —
because the CSIRT branding and imprint sit behind EU Login, where no publicly
visible signal reaches them.

It also settles the open infrastructure question: all 29 labels resolve into
the same 45-address WEDOS pool (`185.8.236.33`-`.77`), but that pool is a
filtering proxy and not the origin, so whether each Member State has a separate
backend was only answerable once the platform answered. It did, on 2026-09-11:
one shared frontend behind every label, with per-country separation expressed
as per-country OAuth clients rather than separate deployments. The detail is in
`srp-domains-baseline.md`.

**Publicly visible signals only — no login attempts, no form input, no
authentication.**

## Not verified here

This image has no `dig`/`host` and the Python stdlib cannot query NS or CNAME
records, so this monitor's own `check.sh` only ever confirms A records
(informationally) and HTTP status.

On 2026-09-11, the delegation and edge pool were independently confirmed via
[bgp.tools](https://bgp.tools) (an external, non-proxied resolver, reached
with a descriptive User-Agent as its access policy requires) for
`portal`/`auth`/`de.cra-srp.enisa.europa.eu`:

- **Azure DNS delegation** — confirmed. All four nameservers
  (`ns1-02.azure-dns.com`, `ns2-02.azure-dns.net`, `ns3-02.azure-dns.org`,
  `ns4-02.azure-dns.info`) resolve under AS8075 (Microsoft Corporation).
- **Edge IP pool** — corrected, not just confirmed. All three hosts resolve to
  the *same* 45-address round-robin pool, `185.8.236.33`–`185.8.236.77`
  (within `185.8.236.0/24`, AS208414 WEDOS Internet a.s., RPKI valid) — not
  the two-address pair (`185.8.236.7`/`.8`) `manifest.json` recorded before.
  That pair was never seen in this lookup; see `manifest.json`'s `edge.ips`
  and `edge.ips_note`.
- **`wedos.global` CNAME chain** — not observed. All three hosts returned
  direct A records with no CNAME. The chain may not apply to this zone, or
  bgp.tools may not surface it; either way, `cname_verified` stays `false`.
  See `manifest.json`'s `edge.cname_check_2026_09_11`.

Cross-check any of this from a machine with `dig`:

```bash
dig NS cra-srp.enisa.europa.eu +short
dig CNAME de.cra-srp.enisa.europa.eu +short
dig A de.cra-srp.enisa.europa.eu +short
```
