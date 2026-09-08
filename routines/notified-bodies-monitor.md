# CRA notified bodies monitor

- **Trigger**: `trig_01V74LWJSJ7QETodKUS5DojP` (UI name: **CRA notified body alert**)
- **Schedule**: `0 7 * * 1-5` (weekdays 07:00 UTC)
- **Writes**: `notified-bodies-baseline.md`, `notified-bodies/manifest.json`
- **Updatable by an agent**: **no** — created via `http_api`, so the prompt below
  must be pasted into the Routines UI by hand.

> **Not yet live, and it needs more than a paste.** The Routine's configured
> source and outcome repository is still `git-z0man/notified-bodies`:
>
> ```
> sources:  https://github.com/git-z0man/notified-bodies
> outcomes: git-z0man/notified-bodies, branch claude/youthful-gauss
> ```
>
> That is platform-side session config, not part of the prompt, and no agent
> tool can change it — `create_trigger` and `update_trigger` both refuse to set
> `sources`/`outcomes`. Until it points at `git-z0man/single-reporting-platform`,
> pasting the prompt below only makes the routine fail: it would look for
> `notified-bodies-baseline.md` in the wrong repository and its push would be
> rejected.
>
> So this file is the destination state, not the running one. See
> `routines/README.md` → "Moving a routine to another repository".
>
> The old repository keeps running the old prompt in the meantime, so nothing
> stops being monitored while this is pending.

---

Check whether any conformity assessment body has been notified under the Cyber Resilience Act, and alert only when the answer changes or the check itself breaks.

Repository: git-z0man/single-reporting-platform (public)

## 0. Repository and branch

If the repository is already checked out in the working directory, use it. Otherwise clone it:

    git clone https://github.com/git-z0man/single-reporting-platform && cd single-reporting-platform

Read `CLAUDE.md` first — it records the conventions for this routine.

Do NOT hard-code a state branch name. The platform assigns this Routine's outcome branch a fresh name whenever the Routine is edited, so any name written here goes stale.

- If the session already has a branch checked out that is not `main`, stay on it and refresh it: `git fetch origin main && git reset --hard origin/main`.
- Otherwise create one from main: `git fetch origin main && git checkout -B notified-bodies-monitor origin/main`.

Never push to `main`. Never create a new per-run branch when the session already gave you one.

## 1. Run the two queries

`notified-bodies/manifest.json` holds the request under `search_request`, field by field. **Use it exactly as recorded; do not re-derive it, and do not render the human page with a browser.** That page is an Angular application that shows nothing without JavaScript, and a headless browser cannot reach it from this environment in any case — the egress proxy resets the connection.

Two queries, both against `https://webgate.ec.europa.eu/es/search-api/rest/search`:

1. **The CRA query** — `csType: nando_notification`, `notificationLegislationId: 167953`, `notificationStatusId: 1`.
2. **The canary** — the same shape with `notificationLegislationId: 154428` (Directive 2014/53/EU, Radio Equipment), a legislation known to have many active bodies.

Watch three things that make a wrong answer look like a right one:

- **A page caps at 200 rows** whatever `pageSize` asks for. Read `totalResults` from the first response and page with `pageNumber` (1-based) until you have every row. Deduping a truncated page under-reports without any error.
- **Rows are per notification, not per body.** Several rows can name the same body. Dedupe on `displayTypeAndNumber` after collecting every page.
- **The field names matter.** `csType: nb` and `legislationId` are the names the site's own URL suggests, and they return zero for *every* legislation — indistinguishable from a true zero.

## 2. The canary decides whether the answer is believable

- **Canary returns rows** → the pipeline works, and the CRA count is the finding, zero included.
- **Canary returns 0, or either request errors, returns non-200, or will not parse** → the check is BROKEN. Report that, say which request failed and how, and **stop. Write nothing, commit nothing.** A silently broken query reporting "0 bodies, no change" is the one outcome this monitor must never produce.

Record the canary's row count in the history entry either way.

## 3. Compare, then record

Build the current active list from the deduped rows: `organizationName`, `displayTypeAndNumber`, `organizationCountryName`. Compare it against `current_snapshot.bodies` in the manifest, by number. Determine what was added and what was removed **before** writing anything, so a real change is detected even if the commit or push then fails.

On a successful check:

- Update `current_snapshot` (count, bodies, `checked_at`) and append an entry to `history` in `notified-bodies/manifest.json`. Set `last_successful_check` at the top level. These timestamps move **only** on success, so a stale one is itself the signal that the monitor stalled.
- In `notified-bodies-baseline.md`: add a row to the check-history table, refresh the "Current state" table and the frontmatter `last_check` (and `last_change`, only if the set of bodies actually changed).
- If bodies were added or removed, add a change log entry in the house format — see "How a change log entry is written" in `CLAUDE.md`. The first body ever notified under the CRA belongs under **New**, with its name, number and country.

### Nothing changed

Only when the set of bodies is unchanged and the canary is healthy. Read `last_check` as it stands on `origin/main`:

    git show origin/main:notified-bodies-baseline.md | sed -n 's/^last_check: //p' | head -1

- If it is **today's date** → today's measurement point is already recorded. Do NOT commit, do NOT open a PR, do NOT report anything. End the run silently.
- If it is an **earlier date** → this is the first run of the day. Update `last_check` and append the history entry, then commit, PR and merge per section 4. Do NOT report — a routine heartbeat is not worth a notification.

## 4. Commit, PR, merge

Only if something actually changed. Commit with a message naming what changed. Push with `git push -u origin HEAD`, retrying up to 4 times with exponential backoff (2s, 4s, 8s, 16s) on network errors only.

If the push fails for lack of credentials (403), do NOT try to route around it — no workarounds, no alternate remotes, no GitHub MCP fallback. Leave the commit on the local branch and report that the push failed, with the exact error AND the branch name you pushed to, so a mismatch with this Routine's configured repository outcome can be spotted. A 403 here most likely means the Routine still points at the old `notified-bodies` repository.

Otherwise open a pull request as a draft, then mark it ready for review and merge it yourself immediately. This is the standing convention recorded in CLAUDE.md. It applies only to PRs that touch `notified-bodies-baseline.md` and/or `notified-bodies/` alone. If your change touches anything else, leave that PR open, do not merge it, and say so.

## 5. Report

Answer in German, concisely, in the same shape as the change log — lead with one or two sentences, then the rubrics that apply, leaving out the empty ones.

Report **only** when:

- **A body was added or removed.** Name it: organisation, NB number, country. The first CRA notified body is the single most consequential thing this monitor can find — say so plainly, and note that third-party conformity assessment for Annex III and IV products becomes possible from that point.
- **The check broke** (canary empty, request failed, response unparseable) — which request, which status, and that nothing was written.
- **The push failed** — separately from the data result.

Otherwise report nothing at all, including on the run that writes the day's heartbeat. Silence is the normal outcome.

When you report, end with exactly one line:
CRA notified bodies: [n] aktiv | Änderung: [was oder keine] | Canary: [Zeilen/FAIL] | push: [OK/FAIL/nichts zu pushen]
