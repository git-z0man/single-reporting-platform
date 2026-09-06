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
| DNS failure | `NXDOMAIN` | not in the zone |
| exit 56 + `403` | `BLOCKED` | egress policy denied CONNECT — the check was blind |

`BLOCKED` is kept distinct on purpose: it means the monitor could not see, and
must never be recorded as a platform state. `first_live` is only ever set from
an HTTP response, so a proxied run cannot manufacture a go-live.

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
role, identifies the SSO provider, and checks the assumed CSIRT per country
instance against page title, branding, imprint, redirect target, or TLS SAN —
flipping each row in the baseline table to `verifiziert` or `korrigiert`, and
storing the deciding signal under `evidence/`.

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
