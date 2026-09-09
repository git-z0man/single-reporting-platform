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
| HTTP status returned | `LIVE` | upstream answered — go-live |
| exit 35 / 28 / 7 / 52 | `PROVISIONED` | connected, upstream dropped |
| exit 6 | `NXDOMAIN` | curl itself could not resolve the host |
| exit 28, local DNS also hung | `DNS_TIMEOUT` | nothing answered in time — the check was blind |
| exit 56 + `403` | `BLOCKED` | egress policy denied CONNECT — the check was blind |

`BLOCKED` and `DNS_TIMEOUT` are kept distinct on purpose: both mean the
monitor could not see, and must never be recorded as a platform state or
overwrite the last confirmed one. `first_live` is only ever set from an HTTP
response, so a proxied run cannot manufacture a go-live.

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
open at go-live is whether the running platform agrees with that list.

It also settles the open infrastructure question: all 29 labels resolve to the
same anycast pair, but that pair is a filtering proxy and not the origin, so
whether each Member State has a separate backend is only answerable from behind
the edge.

**Publicly visible signals only — no login attempts, no form input, no
authentication.**

## Not verified here

The Azure DNS delegation and the `wedos.global` CNAME chain are
operator-supplied. This image has no `dig`/`host` and the Python stdlib cannot
query NS or CNAME records, so only the A records were verified. Confirm the
rest from a machine with `dig`:

```bash
dig NS cra-srp.enisa.europa.eu +short
dig CNAME de.cra-srp.enisa.europa.eu +short
```
