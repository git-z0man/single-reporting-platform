# CRA Single Reporting Platform — guide and tracking archive

Manufacturers of products with digital elements must report actively exploited
vulnerabilities and severe incidents through ENISA's **Single Reporting
Platform (SRP)** from **11 September 2026**, under Article 14 of the Cyber
Resilience Act.

This repository holds two things: a walkthrough of what that reporting looks
like, and a dated archive of how the official sources have changed while the
platform was being built. The archive is the part that is hard to reconstruct
later — ENISA's pages are edited in place, and one of them has already been
temporarily withdrawn.

## The guide

[`index.html`](index.html) — a manufacturer's walkthrough of the four stages:
registration, early warning (24 h), notification (72 h), and final report,
plus ENISA's FAQ. Published via GitHub Pages at
<https://git-z0man.github.io/single-reporting-platform/>.

## The tracking archive

Four baselines, each with a dated change log recording what moved and when.
Every one reproduces its source verbatim — including typos and internal
inconsistencies, which are noted rather than corrected, because a baseline that
quietly tidies its source cannot be diffed against it.

| File | Tracks | Notes |
|---|---|---|
| [`enisa-srp-faq-baseline.md`](enisa-srp-faq-baseline.md) | ENISA's SRP pages: main page, FAQ (27 entries), CSIRT coordinator list, three AR guidance pages | The FAQ went from 23 to 27 entries in a single September rewrite |
| [`enisa-srp-glossary-baseline.md`](enisa-srp-glossary-baseline.md) | The CRA SRP Glossary — every reporting field, its meaning, format and per-stage status | The live page returned HTTP 403 hours after capture; this is currently the only record of its contents |
| [`commission-cra-faq-baseline.md`](commission-cra-faq-baseline.md) | The Commission's *FAQs on the CRA*, a versioned 66-page document (now v1.4) | Four versions archived verbatim under [`commission-faq/`](commission-faq/), with side-by-side diffs |
| [`srp-domains-baseline.md`](srp-domains-baseline.md) | The production DNS zone `cra-srp.enisa.europa.eu` — 29 hosts | Country → CSIRT mapping verified against ENISA's official list; reachability history under [`srp-domains/`](srp-domains/) |

### Things in here you may not find elsewhere

- **Every archived version of the Commission FAQ**, as PDF, as diffable text,
  and as rendered side-by-side comparisons under
  [`commission-faq/diff/`](commission-faq/diff/). The Commission publishes only
  the current version. The diffs show that its own one-line change notes
  understate what changed: v1.2 was described as a "minor correction of 6.2",
  and it removed the notified body's NANDO number from the CE marking step.
- **The full SRP Glossary**, field by field, captured while it was reachable.
- **The country → CSIRT-designated-as-coordinator mapping** for all 27 Member
  States, checked against ENISA's published list — 19 confirmed, 8 corrected,
  with the superseded value kept in a footnote and per-country evidence under
  [`srp-domains/evidence/`](srp-domains/evidence/).
- **A reachability record of the production zone** from before launch: all 29
  hosts resolving to a filtering anycast edge that accepts TCP and drops the
  TLS handshake.

## How it is maintained

Three scheduled tasks re-check the sources and open a pull request when
something moves. Their prompts, schedules and output paths are mirrored in
[`routines/`](routines/); the conventions they follow are in
[`CLAUDE.md`](CLAUDE.md).

| Monitor | Cadence | Writes |
|---|---|---|
| ENISA SRP pages | weekly | the two ENISA baselines |
| Commission CRA FAQ | weekly | the Commission baseline and archive |
| SRP domain reachability | hourly until launch, then daily | the domain baseline and its logs |

Each baseline records `last_check` (when it was last verified) and
`last_change` (when the source last actually moved), so a stale monitor is
visible rather than silent.

One deliberate design note, since it is the kind of thing that gets
"simplified" later: the domain monitor decides liveness on an HTTP status code
and **not** on a completed TLS handshake. Behind an intercepting proxy, TCP and
TLS succeed against every host — including hosts that are dark, and including a
reserved unroutable address. The reasoning is in the header of
[`srp-domains/check.sh`](srp-domains/check.sh).

## What this is not

Not affiliated with ENISA or the European Commission. **Not legal advice.**

The guide is unofficial and based on the Commission's draft CRA guidance, which
is not yet adopted; the platform itself is in test operation and its data
fields are not final. Where this repository and an official source disagree,
the official source governs — the baselines exist to make such differences
visible, not to replace anything.

This is the **public** build. Portal screenshots and material shared through
the CRA Expert Group were removed following Commission feedback and are not
distributed here.

## Provenance

The Commission FAQ is © European Union, reusable under CC BY 4.0 per Commission
Decision 2011/833/EU; archived copies are unmodified. ENISA page content is
reproduced for change tracking and remains ENISA's. Everything written for this
repository is MIT-licensed — see [`LICENSE`](LICENSE).
