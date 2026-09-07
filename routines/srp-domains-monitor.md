# SRP domain reachability monitor

- **Trigger**: `trig_01426ap5KJGGrY4Fk2pbTm8s`
- **Schedule**: `22 * * * *`
- **Writes**: `srp-domains-baseline.md`, `srp-domains/`
- **Also reads**: ENISA's List of CSIRTs Designated as Coordinators — it owns
  the country table, so it applies changes to that list itself rather than
  waiting on a handoff from the ENISA pages monitor.
- **Updatable by an agent**: **yes** — created via `meta_mcp`, so `update_trigger` works.

> Mirror of the live prompt. Editing this file changes nothing on its own;
> apply it with `update_trigger` in the same change.

---

Check the CRA Single Reporting Platform production zone for reachability changes and go-live.

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

It checks 29 hosts (portal, auth, and the 27 Member State instances) and takes several minutes — each host currently times out at the TLS stage. Exit code: 0 = no state change, 1 = at least one host changed state, 2 = error.

It rewrites `srp-domains/status.md`, appends to `srp-domains/reachability-log.csv`, and updates `srp-domains/manifest.json`.

READ THIS BEFORE INTERPRETING ANYTHING: liveness is decided ONLY on an HTTP status code relayed from upstream. Behind the intercepting egress proxy, TCP connect and the TLS handshake succeed against every host — including hosts that are dark, and including a reserved unroutable address. Do NOT conclude the platform is live from a completed TLS handshake, and do not "fix" the script to do so. A host is live when and only when `check.sh` classifies it `LIVE`.

A host classified `BLOCKED` means the egress policy denied CONNECT and the check was blind for that host. That is a monitoring problem, never a statement about the platform. Report it separately; do not record it as a platform state.

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

The check runs hourly, but the repository keeps only ONE measurement point per day plus every real event. This keeps the go-live PR visible instead of buried under ~120 routine PRs. Note that each run gets a fresh container, so a run that does not commit discards its result — that is intended.

### 3a. Exit 1, or the CSIRT list changed

Always commit, PR, merge AND report, regardless of the daily rhythm. This is what the monitor exists for. `check.sh` prints each reachability change on stderr as `CHANGE: ...`. Cases:

- **A host went LIVE for the first time** — this is the go-live. Go to section 4.
- **A new host appeared in the zone** — record it in the baseline's delta history, and in the country table if it is a country code. Check whether it was previously in the "Names that do not exist" list and move it out.
- **A host stopped resolving or stopped answering** — record it; if a previously live host goes dark, say so prominently.
- **The CSIRT coordinator list changed** (section 2) — apply it to the country table, manifest and evidence files as described there, and name the affected countries in the report.

Add a dated entry at the top of the "Delta history" section of `srp-domains-baseline.md`, refresh the "Current state" table (live count, last check, last change) and the frontmatter `last_check` / `last_change`.

### 3b. Exit 0 and the CSIRT list unchanged

Only when BOTH the reachability check and the CSIRT list came back unchanged. Read `last_check` from `srp-domains/manifest.json` as it stands on `origin/main`:

    git show origin/main:srp-domains/manifest.json | python3 -c "import json,sys; print(json.load(sys.stdin)['last_check'])"

- If it is **today's date** → today's measurement point is already recorded. Do NOT commit, do NOT open a PR, do NOT report anything. End the run silently. This is the normal outcome for 23 of the 24 daily runs.
- If it is an **earlier date** → this is the first run of the day. Update `last_check` in the frontmatter of `srp-domains-baseline.md` to today, leave `last_change` alone, then commit, PR and merge per section 6. Do NOT report — a routine heartbeat is not worth a notification.

### 3c. Exit 2 — the check itself failed

Do not commit. Report the failure and its cause. Do not work around it.

## 4. Go-live verification

Only when at least one host is classified LIVE. Use publicly visible signals ONLY — NO login attempts, NO form input, NO authentication, no credentials of any kind. Fetch pages and read what is publicly served, nothing more.

IMPORTANT — the country → CSIRT mapping is ALREADY SETTLED as of 2026-09-07, verified against ENISA's published "List of CSIRTs Designated as Coordinators" (19 of 27 assumptions confirmed, 8 corrected). The table in `srp-domains-baseline.md` is authoritative and every row reads `verifiziert` or `korrigiert`; none reads `angenommen`. Do NOT re-derive it, and do NOT overwrite it from what the platform serves. What is left is a cross-check.

1. Portal: fetch https://portal.cra-srp.enisa.europa.eu/ and confirm it is the entry point with country/CSIRT selection or redirection. If it exposes a country selector, extract the real country → national endpoint mapping and CROSS-CHECK it against the verified table. A divergence means the running platform disagrees with ENISA's own published list — that is a finding worth reporting prominently, not a reason to silently rewrite the table.

2. SSO: identify the identity provider at auth.cra-srp.enisa.europa.eu (EU Login / Keycloak / something else), from the redirect target, page title, or login branding. Note it in one line. The FAQ states EU Login with MFA is required, so confirm or contradict that.

3. Per country: for each live `<cc>.cra-srp.enisa.europa.eu`, cross-check the CSIRT actually served (page title, branding, imprint, redirect target, TLS certificate SAN) against the verified table. Where they agree, append one line to that country's existing `srp-domains/evidence/<host>.txt` recording the confirmation from the live host. Where they DISAGREE, do not change the table — report the discrepancy and record both values in the evidence file, naming ENISA's list and the live host as the two conflicting sources.

4. Backend separation: the 29 host labels all resolve to the same anycast pair 185.8.236.7/.8, but that is a filtering proxy and not the origin. Now that the edge answers, record whether each country host serves a distinct instance or one shared application — from differing TLS SANs, Server/Set-Cookie headers, redirect targets, or page identity. Write the answer into the "Infrastructure" section, replacing the open question. THIS is the main open infrastructure question at go-live.

5. Also note whether the platform matches the FAQ's stated go-live scope: "On the 11th of September the platform will ONLY allow the submission of mandatory reporting fulfilling Art 14 and 24(x). Voluntary reporting per art15 will not be possible."

## 5. Switch to the daily schedule

This Routine runs hourly to catch the go-live. From 12 September 2026 onwards hourly is wasteful and it should run daily instead.

Try to switch it yourself: call update_trigger on trigger `trig_01426ap5KJGGrY4Fk2pbTm8s` with cron_expression `0 6 * * *`. Do this once, on or after 12 September 2026, and skip it if the schedule already is `0 6 * * *`.

If the update_trigger tool is not available in your session (this Routine runs without connector tools, so it very likely is not), do NOT treat that as an error and do NOT try to work around it. Just add one line to your report: "Zeitplanumstellung auf täglich steht noch aus — bitte in der Routines-UI auf `0 6 * * *` ändern (trig_01426ap5KJGGrY4Fk2pbTm8s)."

## 6. Commit, PR, merge

Only when section 3 says to commit. Commit with a message naming what changed. Push with `git push -u origin HEAD`, retrying up to 4 times with exponential backoff (2s, 4s, 8s, 16s) on network errors only.

If the push fails for lack of credentials (403), do NOT try to route around it — no workarounds, no alternate remotes, no GitHub MCP fallback. Leave the commit on the local branch and report that the push failed, with the exact error AND the branch name you pushed to, so a mismatch with the Routine's configured repository outcome can be spotted.

Otherwise open a pull request as a draft, then mark it ready for review and merge it yourself immediately. This is the standing convention for this routine, recorded in CLAUDE.md — do not leave the PR waiting for approval. It applies only to PRs that touch `srp-domains-baseline.md` and `srp-domains/` alone; if your change touches anything else, leave that PR open and say so.

## 7. Report — only when there is something to say

Stay SILENT for a run that changed nothing, including the daily heartbeat commit. No summary line, no "check ran" message. Silence is the expected output most of the time.

Report, in German and concisely, only when:

- **The go-live happened** — say so first and clearly: which hosts, what HTTP codes, what the portal and SSO turned out to be, whether the platform's country → CSIRT routing agrees with ENISA's published list, and whether each country host has its own backend. This is the event this monitor exists for.
- **A new host appeared in the zone, or a host went dark** — one short paragraph.
- **The CSIRT coordinator list changed** — name the countries and what changed, old value and new.
- **The run failed** — check.sh exit 2, or the push failed. Name the cause; do not work around it.

When you do report, end with exactly one line:
SRP domains: <n>/29 live | new hosts: <n> | CSIRT-Abweichungen: <n> | push: <OK/FAIL/nothing to push>
