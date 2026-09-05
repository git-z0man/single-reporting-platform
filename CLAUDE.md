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
