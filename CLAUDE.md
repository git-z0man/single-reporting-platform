# Repository conventions for Claude Code

## ENISA SRP FAQ baseline-check routine

`enisa-srp-faq-baseline.md` is maintained by a scheduled task that
periodically re-checks the ENISA Single Reporting Platform page (and its
guidance subpages) for changes, updates the baseline file, and opens a PR.

For this specific recurring task, no manual review is required: after
pushing the branch and opening the PR (create it as a draft first, per the
usual flow), mark it ready for review and merge it immediately yourself —
do not leave it open waiting for approval.

This auto-merge behavior applies only to PRs from this routine that touch
`enisa-srp-faq-baseline.md` alone. Any other change to this repository
follows the normal review-and-confirm flow.

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
