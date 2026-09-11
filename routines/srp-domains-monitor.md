# SRP domain reachability monitor

- **Trigger**: `trig_01426ap5KJGGrY4Fk2pbTm8s`
- **Schedule**: `22 * * * *` (hourly; section 5 switches it to `0 6 * * *` from 12 September 2026)
- **Writes**: `srp-domains-baseline.md`, `srp-domains/`
- **Also reads**: ENISA's List of CSIRTs Designated as Coordinators — it owns
  the country table, so it applies changes to that list itself rather than
  waiting on a handoff from the ENISA pages monitor.
- **Updatable by an agent**: **yes** — created via `meta_mcp`, so `update_trigger` works.

> Mirror of the live prompt. Editing this file changes nothing on its own;
> apply it with `update_trigger` in the same change.
>
> **Live since 2026-09-11 12:54 UTC**, applied with `update_trigger` and read
> back word-for-word. That update rewrote the prompt for a *running* platform:
> the go-live happened at 11:24 UTC the same day, so section 4 became a drift
> check against the settled architecture instead of a go-live verification,
> and a host going dark — not a host coming up — is now the headline event.

---

Check the CRA Single Reporting Platform production zone for outages and reachability changes. The platform went live on 11 September 2026; this monitor now watches a running service.

Repository: git-z0man/single-reporting-platform (public)

## 0. Repository and branch

If the repository is already checked out in the working directory, use it. Otherwise clone it:

    git clone https://github.com/git-z0man/single-reporting-platform && cd single-reporting-platform

Then read `srp-domains/README.md` — it documents the layout, the detection signal and the proxy trap.

Do NOT hard-code a state branch name. This Routine's configured repository outcome gets a fresh branch name assigned by the platform whenever the Routine is edited, so any name written here goes stale. Instead:

- If the session already has a branch checked out that is not `main`, stay on it and refresh it from main: `git fetch origin main && git reset --hard origin/main`.
- Otherwise create one from main: `git fetch origin main && git checkout -B srp-domains-monitor origin/main`.

Never push to `main`. Never create a new per-run branch when the session already gave you one.

## 1. Run the check

    bash srp-domains/check.sh

It checks 29 hosts (portal, auth, and the 27 Member State instances). Exit code: 0 = no state change, 1 = at least one host changed state, 2 = error.

It rewrites `srp-domains/status.md`, appends to `srp-domains/reachability-log.csv`, and updates `srp-domains/manifest.json`.

READ THIS BEFORE INTERPRETING ANYTHING: liveness is decided ONLY on an HTTP status code relayed from upstream. Behind the intercepting egress proxy, TCP connect and the TLS handshake succeed against every host — including hosts that are dark, and including a reserved unroutable address. Do NOT conclude a host is live from a completed TLS handshake, and do not "fix" the script to do so. A host is live when and only when `check.sh` classifies it `LIVE`.

A host classified `BLOCKED` means the egress policy denied CONNECT and the check was blind for that host. That is a monitoring problem, never a statement about the platform. Report it separately; do not record it as a platform state.

A host classified `EDGE_BLOCKED` got a real HTTP response that was WEDOS's own branded error page rather than the SRP origin. Real information, but not a platform signal: it never counts toward the live tally. See the header of `check.sh` (2026-09-11).

The `dns` column says `ok` only when an address actually came back. It reads `unknown` when nothing resolved and nothing positively failed — which is the normal case in this environment, where the local resolver has been unavailable since 2026-09-09. `unknown` is NOT a platform finding and NOT a regression. Never state which IPs the zone points at based on a run that resolved nothing; that has to come from an external lookup.

## 2. Check the CSIRT coordinator list

One extra HTTP request per run. This routine owns the country table in
`srp-domains-baseline.md`, so it checks the source of that table itself instead
of waiting for the ENISA pages monitor to report a change and a human to act on
it.

Fetch ENISA's list of CSIRTs designated as coordinators — the URL is recorded
as `csirt_source.url` in `srp-domains/manifest.json`. Parse the 27 Member State
entries (country plus one or more contact links) and compare against the
`csirt` and `csirt_url` fields of the country hosts in the manifest.

- **Non-200 (403, timeout, anything)** — not a failure and not a change. ENISA's
  SRP pages have shown themselves unreliable; the Glossary page returned 403
  while everything else stayed up. Do NOT touch the country table, do NOT treat
  it as a removal. Note it in the report only if it persists; otherwise stay
  silent and carry on with the reachability result.
- **List unchanged** — nothing to do. This is the normal outcome.
- **List changed** — a Member State's coordinator changed, or an entry was
  added or removed. This is an EVENT: commit and report it regardless of the
  daily rhythm (see section 3). Update the affected rows in the country table
  of `srp-domains-baseline.md` (`Status` becomes `korrigiert`, with the
  superseded value in a footnote alongside the existing ones), the matching
  host entries in `srp-domains/manifest.json` (`csirt`, `csirt_url`,
  `csirt_status`, `csirt_verified_on`), and the country's
  `srp-domains/evidence/<host>.txt`. Add a dated entry to the delta history
  naming the countries and what changed.

Do not edit `enisa-srp-faq-baseline.md` or `enisa-srp-glossary-baseline.md` —
those belong to the ENISA pages monitor, and touching them would put this PR
outside this routine's auto-merge scope. That monitor checks the same page for
its own word-for-word diff; the two are independent on purpose.

## 3. Decide whether to commit

The repository keeps only ONE measurement point per day plus every real event. This keeps real events visible instead of buried under routine PRs. Note that each run gets a fresh container, so a run that does not commit discards its result — that is intended.

### 3a. Exit 1, or the CSIRT list changed

Always commit, PR, merge AND report, regardless of the daily rhythm. This is what the monitor exists for. `check.sh` prints each reachability change on stderr as `CHANGE: ...`. Cases:

- **A live host went dark** — this is now the headline event. The platform launched on 2026-09-11; a host that stops answering is an outage, and the most important thing this monitor can catch. Say so prominently, name the hosts and the HTTP codes or curl errors, and check whether it is all 29 (a platform-wide outage) or a subset (one Member State instance).
- **A host that was not live becomes live** — record it; for a host that has never been live, note the first-live timestamp.
- **A new host appeared in the zone** — record it in the baseline's delta history, and in the country table if it is a country code. Check whether it was previously in the "Names that do not exist" list and move it out.
- **The CSIRT coordinator list changed** (section 2) — apply it to the country table, manifest and evidence files as described there, and name the affected countries in the report.

Add a dated entry at the top of the "Delta history" section of `srp-domains-baseline.md`, refresh the "Current state" table (live count, last check, last change) and the frontmatter `last_check` / `last_change`. Keep the two in step: the frontmatter and the "Current state" table have drifted apart before, when a heartbeat moved only the frontmatter.

### 3b. Exit 0 and the CSIRT list unchanged

Only when BOTH the reachability check and the CSIRT list came back unchanged. Read `last_check` from `srp-domains/manifest.json` as it stands on `origin/main`:

    git show origin/main:srp-domains/manifest.json | python3 -c "import json,sys; print(json.load(sys.stdin)['last_check'])"

- If it is **today's date** → today's measurement point is already recorded. Do NOT commit, do NOT open a PR, do NOT report anything. End the run silently. This is the normal outcome for almost every run.
- If it is an **earlier date** → this is the first run of the day. Update `last_check` in the frontmatter of `srp-domains-baseline.md` to today AND the "Last check" row of its "Current state" table, leave `last_change` alone, then commit, PR and merge per section 6. Do NOT report — a routine heartbeat is not worth a notification.

### 3c. Exit 2 — the check itself failed

Do not commit. Report the failure and its cause. Do not work around it.

## 4. Post-launch conformance

The platform went live on 2026-09-11 at 11:24:01 UTC (28 hosts; `es` followed at 11:36:58). Use publicly visible signals ONLY — NO login attempts, NO form input, NO authentication, no credentials of any kind. Fetch pages and read what is publicly served, nothing more.

Two things were settled at go-live and are recorded in `srp-domains-baseline.md`. Do NOT re-derive either. What this section asks for is a drift check against them.

1. **Country → CSIRT mapping** — settled 2026-09-07 against ENISA's published "List of CSIRTs Designated as Coordinators" (19 of 27 assumptions confirmed, 8 corrected). Every row reads `verifiziert` or `korrigiert`; none reads `angenommen`. Do NOT overwrite the table from what the platform serves. If the running platform's routing disagrees with ENISA's published list, that is a finding to report prominently and record in the evidence file — naming both sources — not a reason to rewrite the table.

2. **Architecture** — all 29 host labels serve ONE shared frontend application, not per-country backends: the same Kubernetes Deployment `srp-ui-ddb75f59b` (header `server: srp`) behind every label, one shared Keycloak realm `srp` at `auth.cra-srp.enisa.europa.eu`, and per-country separation expressed only as per-country OAuth clients `srp-ar-fe-<cc>` (verified identical to the host's own ISO code for all 27) plus Host-header routing. Every country requests `kc_idp_hint=eu-login`.

Report drift from that architecture, which means any of:

- the ReplicaSet hash in the callback target changing from `srp-ui-ddb75f59b` (an ordinary redeployment — note it in one line, do not treat it as an incident);
- a country whose `client_id` stops matching its own ISO code, or a host that stops requesting `kc_idp_hint=eu-login`;
- a host leaving the shared frontend for a distinct backend, or the edge pool moving outside `185.8.236.33`–`185.8.236.77` / AS208414;
- the identity provider at `auth` changing away from the shared Keycloak realm.

Also note whether the platform still matches the scope ENISA stated for launch: mandatory reporting under Art 14 and 24(x) only, with voluntary reporting under Art 15 not available.

## 5. Switch to the daily schedule

This Routine still runs hourly. That cadence was for catching the go-live, which has happened, so hourly no longer earns its keep once the launch has settled.

Try to switch it yourself: call update_trigger on trigger `trig_01426ap5KJGGrY4Fk2pbTm8s` with cron_expression `0 6 * * *`. Do this once, on or after 12 September 2026, and skip it if the schedule already is `0 6 * * *`.

If the update_trigger tool is not available in your session (this Routine runs without connector tools, so it very likely is not), do NOT treat that as an error and do NOT try to work around it. Just add one line to your report: "Zeitplanumstellung auf täglich steht noch aus — bitte in der Routines-UI auf `0 6 * * *` ändern (trig_01426ap5KJGGrY4Fk2pbTm8s)."

## 6. Commit, PR, merge

Only when section 3 says to commit. Commit with a message naming what changed. Push with `git push -u origin HEAD`, retrying up to 4 times with exponential backoff (2s, 4s, 8s, 16s) on network errors only.

If the push fails for lack of credentials (403), do NOT try to route around it — no workarounds, no alternate remotes, no GitHub MCP fallback. Leave the commit on the local branch and report that the push failed, with the exact error AND the branch name you pushed to, so a mismatch with the Routine's configured repository outcome can be spotted.

Otherwise open a pull request as a draft, then mark it ready for review and merge it yourself immediately. This is the standing convention for this routine, recorded in CLAUDE.md — do not leave the PR waiting for approval. It applies only to PRs that touch `srp-domains-baseline.md` and `srp-domains/` alone; if your change touches anything else, leave that PR open and say so.

## 7. Report — only when there is something to say

Stay SILENT for a run that changed nothing, including the daily heartbeat commit. No summary line, no "check ran" message. Silence is the expected output most of the time.

Report, in German and concisely, only when:

- **A live host went dark** — say so first and clearly: which hosts, what HTTP codes or errors, whether it is all 29 or a subset, and since when. This is now the event this monitor exists for.
- **A new host appeared in the zone, or a host became live for the first time** — one short paragraph.
- **Drift from the settled architecture** (section 4) — name what changed and against which recorded value.
- **The CSIRT coordinator list changed** — name the countries and what changed, old value and new.
- **The run failed** — check.sh exit 2, or the push failed. Name the cause; do not work around it.

When you do report, end with exactly one line:
SRP domains: [n]/29 live | neue Hosts: [n] | CSIRT-Abweichungen: [n] | push: [OK/FAIL/nichts zu pushen]
