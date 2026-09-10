---
source: European Commission — NANDO / Single Market Compliance Space
human_view: https://webgate.ec.europa.eu/single-market-compliance-space/notified-bodies/notified-body-list?filter=legislationId:167953,notificationStatusId:1
api_endpoint: https://webgate.ec.europa.eu/es/search-api/rest/search
legislation: Regulation (EU) 2024/2847 (Cyber Resilience Act)
legislation_id: "167953"
notification_status: "1 (Active)"
machine_state: notified-bodies/manifest.json
active_bodies: 0
canary: Directive 2014/53/EU (RED), legislationId 154428 — must return rows, else the check is broken
last_check: 2026-09-10
last_change: never — no body has ever been listed under the CRA
purpose: >-
  Detect the moment a conformity assessment body is first notified under the
  Cyber Resilience Act. Until one is, manufacturers of important and critical
  products with digital elements cannot complete third-party conformity
  assessment, so the first entry here is a date much of the CRA timeline hangs on.
---

# CRA Notified Bodies — Baseline

**0 bodies are notified under the Cyber Resilience Act.** Checked 2026-09-10, and on every working day since 21 June 2026 — 67 checks, never anything but zero.

That is a finding, not an absence of one. Regulation (EU) 2024/2847 requires third-party conformity assessment for important (Annex III) and critical (Annex IV) products with digital elements. No notified body means nobody is authorised to perform it. The Commission's own implementation timeline expects "sufficient CABs designated" by **11 December 2026**.

## Current state

| | |
|---|---|
| Active notified bodies (CRA) | **0** |
| Last successful check | 2026-09-10T07:15:28+00:00 |
| Last change | none — zero since monitoring began |
| Checks recorded | 67, from 2026-06-21 to 2026-09-10 |
| Canary (RED) | 366 rows, OK |

## Why there is a canary

The query returns a count, and a count of zero is indistinguishable from a query that has quietly stopped matching anything — a renamed field, a changed id, a moved endpoint. So every run asks the same question of a legislation known to be busy, **Directive 2014/53/EU (Radio Equipment)**, and requires a non-zero answer. If the canary comes back empty, the run reports the check as broken and writes nothing. A zero is believed only when the canary is healthy.

Verified independently from this repository's environment on 2026-09-08: the CRA query returned 0, the canary 366 rows across 71 distinct bodies.

## How it is queried

The human page is an Angular application and renders nothing useful without JavaScript. Behind it sits a multipart search API, recorded field by field in [`notified-bodies/manifest.json`](notified-bodies/manifest.json). What matters:

- `POST https://webgate.ec.europa.eu/es/search-api/rest/search`
- multipart fields `text=*`, `pageSize`, `apiKey`, and `query` as an `application/json` part
- the filter is `csType: nando_notification` with `notificationLegislationId` and `notificationStatusId` — **not** `csType: nb` or `legislationId`. Those return zero for every legislation and look exactly like a real answer
- the API key is the public default compiled into the site's own JavaScript bundle, not a secret
- **rows are per notification, not per body** — several rows can name one body, so dedupe on `displayTypeAndNumber`
- **a page caps at 200 rows.** Asking for 1000 returns 200 with `totalResults: 366`; page with `pageNumber` until you have them all

## Check history

One row per day; "Checks" is filled in only where a day had more than one run.

| Date | Active bodies | Checks | Canary rows |
|---|---|---|---|
| 2026-06-21 | 0 | — | — |
| 2026-06-22 | 0 | — | 360 |
| 2026-06-23 | 0 | 2 | 360 |
| 2026-06-24 | 0 | 4 | 360 |
| 2026-06-25 | 0 | 4 | 360 |
| 2026-06-26 | 0 | — | 360 |
| 2026-06-29 | 0 | — | 360 |
| 2026-06-30 | 0 | — | 360 |
| 2026-07-01 | 0 | — | 360 |
| 2026-07-02 | 0 | — | 360 |
| 2026-07-03 | 0 | — | 360 |
| 2026-07-06 | 0 | — | 360 |
| 2026-07-07 | 0 | — | 360 |
| 2026-07-08 | 0 | — | 360 |
| 2026-07-09 | 0 | — | 360 |
| 2026-07-10 | 0 | — | 360 |
| 2026-07-13 | 0 | — | 360 |
| 2026-07-14 | 0 | — | 360 |
| 2026-07-15 | 0 | — | 360 |
| 2026-07-16 | 0 | — | 360 |
| 2026-07-17 | 0 | — | 360 |
| 2026-07-20 | 0 | — | 360 |
| 2026-07-21 | 0 | — | 360 |
| 2026-07-22 | 0 | — | 360 |
| 2026-07-23 | 0 | — | 362 |
| 2026-07-24 | 0 | — | 362 |
| 2026-07-27 | 0 | — | 362 |
| 2026-07-28 | 0 | — | 362 |
| 2026-07-29 | 0 | — | 362 |
| 2026-07-30 | 0 | — | 362 |
| 2026-07-31 | 0 | — | 362 |
| 2026-08-03 | 0 | — | 362 |
| 2026-08-04 | 0 | — | 363 |
| 2026-08-05 | 0 | — | 363 |
| 2026-08-06 | 0 | — | 363 |
| 2026-08-07 | 0 | — | 363 |
| 2026-08-10 | 0 | — | 363 |
| 2026-08-11 | 0 | — | 364 |
| 2026-08-12 | 0 | — | 364 |
| 2026-08-13 | 0 | — | 364 |
| 2026-08-14 | 0 | — | 364 |
| 2026-08-17 | 0 | — | 364 |
| 2026-08-18 | 0 | — | 364 |
| 2026-08-19 | 0 | — | 364 |
| 2026-08-20 | 0 | — | 364 |
| 2026-08-21 | 0 | — | 364 |
| 2026-08-24 | 0 | — | 364 |
| 2026-08-25 | 0 | — | 365 |
| 2026-08-26 | 0 | — | 365 |
| 2026-08-27 | 0 | — | 365 |
| 2026-08-28 | 0 | — | 365 |
| 2026-08-31 | 0 | — | 365 |
| 2026-09-01 | 0 | — | 365 |
| 2026-09-02 | 0 | — | 365 |
| 2026-09-03 | 0 | — | 366 |
| 2026-09-04 | 0 | — | 366 |
| 2026-09-07 | 0 | — | 366 |
| 2026-09-08 | 0 | — | 366 |
| 2026-09-09 | 0 | — | 366 |
| 2026-09-10 | 0 | — | 366 |

## Change log

### 2026-09-08 — moved into this repository

Ported from `git-z0man/notified-bodies`, where this monitor had run since 21 June with its state on a side branch. The full 65-run history came with it.

**Fixed**

- **Paging.** The recorded request asked for `pageSize=1000` and the endpoint silently returned 200 rows. With zero CRA bodies that changed nothing, but the first time bodies appear the list would have been cut at 200 with no sign of it. The request now pages explicitly.

**Watch**

- The copy on `main` of the old repository stops at 25 June. It is stale and should not be read as current.

**Unchanged**

The query, the canary and the answer: 0 active bodies, canary 366 rows.

## Provenance

NANDO data is published by the European Commission. This file records what the public interface returned on the dates listed; it is not an official extract and carries no legal weight. Where it differs from the Commission's own page, that page governs.
