# Repository conventions for Claude Code

## Routine prompts must be kept in sync with the repository

Each of the three monitors below is driven by a scheduled Routine. What a
Routine executes is its **prompt**, held by the platform — not anything in
this repository. A copy of each prompt is mirrored under `routines/`, together
with its trigger ID and whether an agent may update it.

**Whenever a change widens what a monitor covers — a new page to watch, a new
baseline file, a new output path — the prompt must be updated in the same
change.** Otherwise the next scheduled run silently reverts to the narrower
job, and the wider scope survives only as long as the session that invented it.

Concretely, in this order:

1. Update the mirrored prompt in `routines/`, in the same commit as the
   repository change.
2. **Apply it to the live Routine** — `update_trigger` where the routine was
   created by an agent, otherwise paste it into the Routines UI. This is the
   step that actually takes effect; the other two are documentation.
3. Update the auto-merge paths in this file if the routine now writes
   somewhere new.

This is not hypothetical. On 2026-09-07 the ENISA run discovered ENISA's new
CRA SRP Glossary page, built `enisa-srp-glossary-baseline.md`, and updated
this file — while its own prompt still described a single page and a single
file. The routine was more thorough than its instructions, and nothing carried
that forward to the next run.

Note that an agent can only update a Routine it created itself. The ENISA
monitor was created through the API, so its prompt changes are a manual step
in the Routines UI; see `routines/README.md`.

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

The check normally runs weekly. **Until 2026-09-14 it runs hourly**, because
ENISA signalled frequent edits in the run-up to the 11 September go-live and a
Tuesday change would otherwise wait until the following Monday. The same
daily-rhythm rule as the domain routine applies while it does: the repository
keeps **one measurement point per day** plus every real change. A run that
finds nothing changed and sees today's date in `last_check` on `main` ends
silently — no commit, no PR, no notification — and that is the normal outcome
for most runs. Any substantive change is committed and reported immediately,
whatever the time of day.

Fetches are rate-limited by ENISA: an HTTP 429 or 5xx that survives the retries
is a failed check, never a content change. Do not diff an error page against a
baseline, and do not touch the baseline because a fetch failed.

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

The check runs hourly to catch the go-live quickly, but the repository keeps
only **one measurement point per day** plus every real event. A run that finds
no change and sees today's date already in `srp-domains/manifest.json` on
`main` ends silently: no commit, no PR, no notification. That is the normal
outcome for most runs. Anything substantive — a host going live, a new host in
the zone, a host falling away — is committed and reported immediately,
regardless of the daily rhythm.

This is why `srp-domains/reachability-log.csv` holds roughly one set of 29 rows
per day rather than 24: the hourly runs still happen, they just stay quiet.
Each run gets a fresh container, so a run that does not commit discards its
result by design.

The routine does not hard-code its state branch. The platform assigns the
Routine's outcome branch a new name whenever the Routine is edited, so the
prompt uses whatever branch the session provides and pushes with
`git push -u origin HEAD`.

Note for anyone editing `srp-domains/check.sh`: liveness is decided on an HTTP
status code and deliberately **not** on the TLS handshake. Behind an
intercepting egress proxy both TCP and TLS succeed against every host while the
platform is dark, so the obvious simplification silently breaks the monitor.
The reasoning is in the script's header comment.
