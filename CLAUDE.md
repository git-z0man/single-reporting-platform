# Repository conventions for Claude Code

## Routine prompts are files in this repository

Each Routine runs a scheduled **prompt**, held by the platform. The live prompt
of every Routine is meant to be a short **loader** that reads the real prompt
from `routines/<name>.md` on `main`; where the loader is applied, that file *is*
the prompt, and editing it changes the next run. Where it is not applied yet, the
file's header says so and the file is only a mirror. `routines/README.md` has the
loader text, the status of each Routine and the rollback.

**Whenever a change widens what a monitor covers — a new page to watch, a new
baseline file, a new output path — update its file in `routines/` in the same
commit**, and then:

1. If the loader is not applied to that Routine yet, apply the full text to the
   live Routine (`update_trigger` where the Routine was created by an agent,
   otherwise paste it into the Routines UI) and read it back.
2. Update the auto-merge paths in this file if the routine now writes somewhere
   new.

Trust note: because a loader executes whatever is on `main`, `routines/` is in
**no** auto-merge scope. Every change to a prompt goes through review.

This is not hypothetical. On 2026-09-07 the ENISA run discovered ENISA's new CRA
SRP Glossary page, built `enisa-srp-glossary-baseline.md`, and updated this
file, while its own prompt still described a single page and a single file. The
routine was more thorough than its instructions, and nothing carried that
forward to the next run. Loaders end that class of drift; they do not remove the
one manual step each `http_api`-created Routine (ENISA, notified bodies) needs,
the first paste of the loader.

Which repositories a Routine may read and write is separate again: session
config, not prompt, and no agent tool can set it. Moving a monitor to another
repository is config first, prompt second. `routines/README.md` has the detail.

## How a change log entry is written

Every baseline in this repository carries a change log, and they are read by
people, not only diffed. The house format, substance first:

    ### [date] [HH:MM] UTC (vs. [what it was compared against])

    One or two sentences: what a reader needs if they read nothing else.

    **New** / **Changed** / **Fixed** / **Watch**   — one finding per bullet
    **Editorial**   — one line, counts and a pointer, never a list
    **Unchanged**   — one line, with the identifying stamps

Empty rubrics are left out; the order of the rest stays. Aim for 250 words —
not a hard limit, but an entry over it has usually spelled out editorial work
that belonged in one summarising line. Typos, punctuation, capitalisation and
house-style shifts are counted, not enumerated: the defects themselves stay
marked in the content sections below, so nothing is lost by not listing them
twice. Quote verbatim only where the wording *is* the finding — a changed
obligation, a new field name, a corrected legal reference.

This is why: on 2026-09-08 a single entry ran to 600 words, most of it about a
wording pass over two guidance pages, while the two things that mattered — the
Glossary links working again, and two ENISA pages disagreeing about who
receives an invitation email — sat buried in the middle of it.

## ENISA SRP FAQ baseline-check routine

`enisa-srp-faq-baseline.md` and `enisa-srp-glossary-baseline.md` are
maintained by a scheduled task that periodically re-checks the ENISA Single
Reporting Platform page (its guidance subpages, the CRA SRP Glossary page,
and the CSIRT-list page) for changes, updates the baseline file(s), and
opens a PR. The Glossary page needs its own full record for two reasons
established on 2026-09-07: it changed address that day (the old path still
returns HTTP 403, the page lives on and is reachable at the new one), and its
content was edited the same evening without its version stamp or date moving.
Neither the URL nor the version number is a reliable handle on it. So
`enisa-srp-glossary-baseline.md` is the full-detail historical record of its
field-by-field content — kept diffable in the same one-block-per-entry style
as the rest of these baselines, and not to be reconstructed only from the
(deliberately trimmed) summary table that `enisa-srp-faq-baseline.md` also
carries.

For this specific recurring task, no manual review is required: after
pushing the branch and opening the PR (create it as a draft first, per the
usual flow), mark it ready for review and merge it immediately yourself —
do not leave it open waiting for approval.

This auto-merge behavior applies only to PRs from this routine that touch
`enisa-srp-faq-baseline.md` and/or `enisa-srp-glossary-baseline.md` alone.
Any other change to this repository follows the normal review-and-confirm
flow.

The check runs daily, at 06:04 UTC. It ran hourly from 2026-09-07 to
2026-09-14, because ENISA signalled frequent edits in the run-up to the
11 September go-live; a revert to weekly was documented at the time but never
applied to the live Routine, and daily has since been confirmed as the
intended cadence — it is what caught the new FAQ Q32 within hours on
21 September. See `routines/README.md` for what these cadences actually
caught. The same daily-rhythm rule as the domain routine still applies: the repository keeps
**one measurement point per day** plus every real change. A run that finds
nothing changed and sees today's date in `last_check` on `main` ends
silently — no commit, no PR, no notification — and that is the normal outcome
for most runs. Any substantive change is committed and reported immediately,
whatever the time of day.

Fetches are rate-limited by ENISA: an HTTP 429 or 5xx that survives the retries
is a failed check, never a content change. Do not diff an error page against a
baseline, and do not touch the baseline because a fetch failed.

## CRA notified bodies routine

`notified-bodies-baseline.md` and everything under `notified-bodies/` are
maintained by a scheduled task that checks whether any conformity assessment
body has been notified under the Cyber Resilience Act. The answer has been
**zero** on every working day since 21 June 2026.

The same convention as the other routines applies: no manual review is
required. After pushing the branch and opening the PR (create it as a draft
first, per the usual flow), mark it ready for review and merge it immediately.

This auto-merge behavior applies only to PRs from this routine that touch
`notified-bodies-baseline.md` and `notified-bodies/` alone. Any other change to
this repository follows the normal review-and-confirm flow.

The daily-rhythm rule applies here too: one measurement point per day plus
every real change. A run that finds nothing changed and sees today's date in
`last_check` on `main` ends silently — no commit, no PR, no notification.

Three things about this check are easy to get wrong, and each of them turns a
broken query into a confident "0 bodies, no change":

- **The canary is not optional.** Every run also queries a legislation known to
  have many active bodies (Directive 2014/53/EU, Radio Equipment,
  `legislationId 154428`). If that returns nothing, the pipeline is broken:
  report it and write nothing. A zero is believable only when the canary is
  healthy.
- **The field names are `csType: nando_notification` and
  `notificationLegislationId`** — not `csType: nb` and `legislationId`, which is
  what the site's own filter URL suggests and which returns zero for every
  legislation.
- **A result page caps at 200 rows** however large a `pageSize` is requested,
  and rows are per notification rather than per body. Page through
  `totalResults` and dedupe on `displayTypeAndNumber`, or the list silently
  truncates the first time bodies actually appear.

Do not render the NANDO page with a headless browser. It is an Angular
application that shows nothing without JavaScript, and this environment's
egress proxy resets browser connections to `webgate.ec.europa.eu` in any case —
`curl` against the recorded API works, a browser does not.

## Commission CRA FAQ version-check routine

`commission-cra-faq-baseline.md` and everything under `commission-faq/` are
maintained by a scheduled task that periodically re-checks the European
Commission's *FAQs on the Cyber Resilience Act* (and the CRA implementation
factpage) for a new version, archives it, records the diff, and opens a PR.

The same convention as the ENISA routine applies: no manual review is
required. After pushing the branch and opening the PR (create it as a draft
first, per the usual flow), mark it ready for review and merge it immediately
— do not leave it open waiting for approval.

This auto-merge behavior applies only to PRs from this routine that touch
`commission-cra-faq-baseline.md` and `commission-faq/` alone. Any other change
to this repository follows the normal review-and-confirm flow.

## SRP domain reachability routine

`srp-domains-baseline.md` and everything under `srp-domains/` are maintained by
a scheduled task that periodically re-checks the CRA Single Reporting Platform
production zone (`cra-srp.enisa.europa.eu`, 29 hosts), records the reachability
state, detects the go-live, and opens a PR.

The same convention as the ENISA and Commission routines applies: no manual
review is required. After pushing the branch and opening the PR (create it as a
draft first, per the usual flow), mark it ready for review and merge it
immediately — do not leave it open waiting for approval.

This auto-merge behavior applies only to PRs from this routine that touch
`srp-domains-baseline.md` and `srp-domains/` alone. Any other change to this
repository follows the normal review-and-confirm flow.

The check runs daily, at 06:00 UTC. It ran hourly until 13 September 2026 to
catch the go-live quickly; the routine switched itself to daily once that had
happened, on its own prompt's instruction. The repository keeps
**one measurement point per day** plus every real event. A run that finds
no change and sees today's date already in `srp-domains/manifest.json` on
`main` ends silently: no commit, no PR, no notification. That is the normal
outcome for most runs. Anything substantive — a host going live, a new host in
the zone, a host falling away — is committed and reported immediately,
regardless of the daily rhythm.

`srp-domains/reachability-log.csv` therefore holds one set of 29 rows per day.
Under the hourly cadence it held the same one set per day rather than 24, since
the silent runs committed nothing — the log's shape did not change when the
schedule did. Each run gets a fresh container, so a run that does not commit
discards its result by design.

The routine does not hard-code its state branch. The platform assigns the
Routine's outcome branch a new name whenever the Routine is edited, so the
prompt uses whatever branch the session provides and pushes with
`git push -u origin HEAD`.

Note for anyone editing `srp-domains/check.sh`: liveness is decided on an HTTP
status code and deliberately **not** on the TLS handshake. Behind an
intercepting egress proxy both TCP and TLS succeed against every host while the
platform is dark, so the obvious simplification silently breaks the monitor.
The reasoning is in the script's header comment.

## EUVD exploited-vulnerabilities routine

`euvd-exploited-baseline.md` and everything under `euvd/` (the scripts, the data
in `euvd/exploited.json`, the statistics page `euvd/stats.html` with its data
`euvd/stats.json` and the daily record `euvd/history.jsonl`, both written by
`euvd/build_stats.py`, one record per entry under `euvd/details/`, including the
EUVD's honeypot sensor sightings, and the page `euvd/index.html`) are maintained by a scheduled task that runs
`euvd/check_exploited.py` daily at 06:20 UTC. The prompt is
`routines/euvd-exploited-monitor.md`.

The same convention as the other monitors applies: no manual review is required.
After pushing the branch and opening the PR (create it as a draft first), mark it
ready for review and merge it immediately. This applies only to PRs from this
routine that touch `euvd-exploited-baseline.md` and `euvd/` alone, checked with
`tools/scope_guard.py euvd-exploited-baseline.md euvd/`. Any other change to this
repository, including to `euvd/check_exploited.py`, `euvd/enrich.py`, `euvd/build_stats.py`,
`euvd/charts.js` or `euvd/prerender.js`, follows the
normal review-and-confirm flow, and the Routine does not edit them.

The daily-rhythm rule applies: one measurement point per day plus every real
change. A run that finds nothing changed and sees today's date in `last_check` on
`main` ends silently. A failed fetch (HTTP error, unparseable answer, incomplete
paging, an implausibly small set) is a failed check, never a content change.

The baseline never says which entry was the first reported through the SRP: no
source records the reporting route, and the list largely follows CISA's catalogue.
It may list **candidates**, and does so in its "SRP candidates" section, but only by
the criteria stated there (computed by the script) and always as indications. A
change-log entry names a new candidate as such and must not imply that it was
reported through the SRP.

## Guide sync routine

`index.html` (the guide) and everything under `guide-sync/` are maintained by a
scheduled task that runs `tools/fetch_enisa.py`, `tools/check_guide.py` and
`tools/sync_guide.py` daily at 07:30 UTC, after the ENISA and domain monitors.
The prompt is `routines/guide-sync.md`; the rules for what is mechanical are in
`tools/README.md`.

Unlike the monitors, this one auto-merges only under a narrow gate: the pull
request touches `index.html` and `guide-sync/` alone, `tools/verify_mechanical.py
origin/main` exits 0 (the change is exactly what the script produces, byte for
byte), `tools/scope_guard.py index.html guide-sync/` exits 0,
`tools/check_guide.py` exits 0, and `tools/guide-sync.paused` does not exist on
`main`. Anything that needs judgment (a rewritten answer, a changed stage, a new
Required field) stays a draft pull request for a person, as does any other change
to `index.html`.

While `tools/guide-sync.paused` exists, this Routine opens drafts only. It ships
present; deleting it arms auto-merge.

The same daily rule applies: a run that finds the guide matching ENISA ends
silently, with no commit, no PR and no notification. A fetch that fails (HTTP 429
or 5xx, or a page that no longer parses) is a failed check, never a content
change.
