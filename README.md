# CRA Single Reporting Platform — guide and tracking archive

Manufacturers of products with digital elements must report actively exploited
vulnerabilities and severe incidents through ENISA's **Single Reporting
Platform (SRP)** from **11 September 2026**, under Article 14 of the Cyber
Resilience Act.

This repository holds two things: a walkthrough of what that reporting looks
like, and a dated archive of how the official sources have changed while the
platform was being built. The archive is the part that is hard to reconstruct
later — ENISA's pages are edited in place, one has already changed address
mid-flight, and another was rewritten without its version stamp moving.

## The guide

[`index.html`](index.html) — a manufacturer's walkthrough of the four stages:
registration, early warning (24 h), notification (72 h), and final report.
Each stage runs screen by screen: ENISA's own screenshot, the fields as that
screen labels them, and what goes in each — with every reporting field
explained from ENISA's Glossary, and its FAQ in full. Published via GitHub Pages at
<https://git-z0man.github.io/single-reporting-platform/>.

The archive below is served from the same site, so anything in it can be linked
directly — most usefully the [FAQ version comparisons](https://git-z0man.github.io/single-reporting-platform/commission-faq/diff/)
and the [current reachability status](https://git-z0man.github.io/single-reporting-platform/srp-domains/status.md).

## The tracking archive

Five baselines, each with a dated change log recording what moved and when.
Every one reproduces its source verbatim — including typos and internal
inconsistencies, which are noted rather than corrected, because a baseline that
quietly tidies its source cannot be diffed against it.

| File | Tracks | Notes |
|---|---|---|
| [`enisa-srp-faq-baseline.md`](enisa-srp-faq-baseline.md) | ENISA's SRP pages: main page, FAQ (30 entries), CSIRT coordinator list, four AR guidance pages | The FAQ went from 23 to 27 entries in a single September rewrite |
| [`enisa-srp-glossary-baseline.md`](enisa-srp-glossary-baseline.md) | The CRA SRP Glossary — every reporting field, its meaning, format and per-stage status | The page moved without a redirect — the old URL still returns HTTP 403 — and its content has been edited without the version stamp moving |
| [`commission-cra-faq-baseline.md`](commission-cra-faq-baseline.md) | The Commission's *FAQs on the CRA*, a versioned 66-page document (now v1.4) | Four versions archived verbatim under [`commission-faq/`](commission-faq/), with side-by-side diffs |
| [`srp-domains-baseline.md`](srp-domains-baseline.md) | The production DNS zone `cra-srp.enisa.europa.eu` — 29 hosts | Country → CSIRT mapping verified against ENISA's official list; reachability history under [`srp-domains/`](srp-domains/) |
| [`notified-bodies-baseline.md`](notified-bodies-baseline.md) | Conformity assessment bodies notified under the CRA | **Still zero**, on every working day since 21 June 2026 — 65 checks. Machine state under [`notified-bodies/`](notified-bodies/) |
| [`enisa-defect-report.md`](enisa-defect-report.md) | Errors, contradictions and gaps found in ENISA's own SRP pages, written to be handed to ENISA | 37 findings, tracked: within a day ENISA fixed 13, partly addressed 7, 17 open (re-checked 10 September 2026 against the pages and the new AR User Manual) |

### Things in here you may not find elsewhere

- **A count of the notified bodies authorised to certify under the CRA: zero**,
  checked every working day since June and recorded each time. The interesting
  number here is a date that has not arrived yet — until a body is notified,
  third-party conformity assessment for important and critical products cannot
  be completed at all, and the Commission's timeline expects "sufficient CABs
  designated" by 11 December 2026. The check carries a canary query against a
  busy directive, because a query that has quietly stopped matching returns the
  same zero as a true one.

- **Every archived version of the Commission FAQ**, as PDF, as diffable text,
  and as [rendered side-by-side comparisons](https://git-z0man.github.io/single-reporting-platform/commission-faq/diff/)
  (source under [`commission-faq/diff/`](commission-faq/diff/) — those are HTML,
  so read them through the link, not in the repository). The Commission
  publishes only the current version. The diffs show that its own one-line change notes
  understate what changed: v1.2 was described as a "minor correction of 6.2",
  and it removed the notified body's NANDO number from the CE marking step.
- **The full SRP Glossary**, field by field — including the entry whose stated
  meaning contradicts its own completion instructions, and the day ENISA
  rewrote 29 of 38 rows without changing the version number in the footer.
- **The country → CSIRT-designated-as-coordinator mapping** for all 27 Member
  States, checked against ENISA's published list — 19 confirmed, 8 corrected,
  with the superseded value kept in a footnote and per-country evidence under
  [`srp-domains/evidence/`](srp-domains/evidence/).
- **A reachability record of the production zone** from before launch: all 29
  hosts resolving to a filtering anycast edge which, from a non-allowlisted
  source, accepts TCP and drops the TLS handshake.

## How it is maintained

Four scheduled tasks re-check the sources and open a pull request when
something moves. Their prompts, schedules and output paths are mirrored in
[`routines/`](routines/); the conventions they follow are in
[`CLAUDE.md`](CLAUDE.md).

| Monitor | Cadence | Writes |
|---|---|---|
| ENISA SRP pages | hourly until 14 Sep, then weekly | the two ENISA baselines |
| Commission CRA FAQ | weekly | the Commission baseline and archive |
| SRP domain reachability | hourly until launch, then daily | the domain baseline and its logs |
| CRA notified bodies | weekdays | the notified-bodies baseline and its state |

Each baseline records `last_check` (when it was last verified) and
`last_change` (when the source last actually moved), so a stale monitor is
visible rather than silent.

One deliberate design note, since it is the kind of thing that gets
"simplified" later: the domain monitor decides liveness on an HTTP status code
and **not** on a completed TLS handshake. That is about the measuring end, not
the edge: behind the intercepting proxy this monitor runs through, TCP and TLS
succeed against every host — including hosts that are dark, and including a
reserved unroutable address. The reasoning is in the header of
[`srp-domains/check.sh`](srp-domains/check.sh).

## What this is not

Not affiliated with ENISA or the European Commission. **Not legal advice.**

The guide is unofficial. It follows ENISA's published SRP guidance, Glossary
and FAQ, and the Commission's Article 26 guidance adopted on 27 July 2026 —
all of which are still being edited, several of them in the same week this was
written. Where this repository and an official source disagree, the official
source governs; the baselines exist to make such differences visible, not to
replace anything.

This is the **public** build. Portal screenshots and material shared through
the CRA Expert Group were removed following Commission feedback and are not
distributed here.

## Provenance

The Commission FAQ is © European Union, reusable under CC BY 4.0 per Commission
Decision 2011/833/EU; archived copies are unmodified. ENISA page content is
reproduced for change tracking and remains ENISA's. Everything written for this
repository is MIT-licensed — see [`LICENSE`](LICENSE).
