# ENISA SRP pages monitor

- **Trigger**: `trig_015C8QiJhXwkxPkDdoMbkHeD`
- **Schedule**: `0 * * * *` — **hourly, temporarily**, for the run-up to go-live. Back to `0 5 * * 1` (Mondays 05:00 UTC) on **2026-09-14**.
- **Writes**: `enisa-srp-faq-baseline.md`, `enisa-srp-glossary-baseline.md`
- **Updatable by an agent**: **no** — created via `http_api`, so the prompt below
  must be pasted into the Routines UI by hand.

> **Pending in the Routines UI: an hourly schedule and this prompt.** ENISA has
> signalled frequent changes in the run-up to the 11 September go-live, so the
> monitor moves from Mondays 05:00 UTC to `0 * * * *` until **2026-09-14**,
> when it goes back to weekly. Set the cron and paste the prompt below in the
> same visit.
>
> Two things to know when saving: the platform anchors `0 * * * *` to the
> **minute you save**, and the domain monitor already sits at `:22` fetching
> the same CSIRT list — so save at a minute well away from it, say `:05`–`:15`
> or `:35`–`:50`. And every edit reassigns the Routine's outcome branch name;
> harmless here, since this prompt pushes with `git push -u origin HEAD`.
>
> **Hourly needed three prompt changes first**, all from problems seen on
> 2026-09-07 rather than imagined: runs that find nothing changed now end
> silently (section 4, the pattern the domain monitor already uses), a second
> change log section on the same day carries a UTC time (section 4), and a 429
> or 5xx that survives the retries is reported as a failed check instead of
> being diffed as content (section 1).
>
> **The 2026-09-07 paste is otherwise live and verified** — read back from the
> Routine and diffed against this file: same sections, same rules, 0.998
> word-level match, the remainder being markdown the UI strips. The one loss
> was three `<placeholder>` markers in the closing report line, eaten as if
> they were HTML tags; the placeholders here are square brackets now, which
> survive.
>
> An agent cannot update this Routine — `update_trigger` and `fire_trigger`
> both refuse it, because it was created via `http_api`. Prompt and schedule
> alike are a manual step.
>
> **Pending in the Routines UI (added 2026-09-08 14:10 UTC): an eighth
> tracked page.** Walking the main page's "Content" navigation, as section 1
> requires, turned up a new guidance subpage — "CRA SRP guidance - Particular
> Exceptional Circumstances (PEC)" — not in either baseline. It has been added
> to `enisa-srp-faq-baseline.md` as `guidance_urls[3]`, and the section below
> updated to list it as page 7 (Glossary renumbered to 8). The live Routine's
> stored prompt still says "all seven" and lists only six items under
> `enisa-srp-faq-baseline.md`; paste the updated section 1 below into the
> Routines UI so the next scheduled run checks the new page too — until then
> it will keep re-discovering it from scratch every run instead of diffing it
> against a baseline.

---

Check ENISA's Single Reporting Platform pages for changes.

Repository: git-z0man/single-reporting-platform (public)

## 0. Repository and branch

If the repository is already checked out in the working directory, use it. Otherwise clone it:

    git clone https://github.com/git-z0man/single-reporting-platform && cd single-reporting-platform

Read `CLAUDE.md` first — it records the conventions for this routine.

Do NOT hard-code a state branch name. The platform assigns this Routine's outcome branch a fresh name whenever the Routine is edited, so any name written here goes stale. Instead:

- If the session already has a branch checked out that is not `main`, stay on it and refresh it: `git fetch origin main && git reset --hard origin/main`.
- Otherwise create one from main: `git fetch origin main && git checkout -B enisa-srp-monitor origin/main`.

Never push to `main`. Never create a new per-run branch when the session already gave you one.

## 1. The pages to check — all eight

Both baseline files carry the authoritative URL list in their frontmatter. Read them first and use the URLs recorded there; the list below is what it should be, but the files win if they disagree (they get updated when ENISA moves a page).

Tracked in `enisa-srp-faq-baseline.md`:

1. Main SRP page — `url` in the frontmatter
2. FAQ subpage — `faq_url`
3. List of CSIRTs Designated as Coordinators — `csirt_list_url`
4. AR User Registration guidance — `guidance_urls[0]`
5. AR Notification Submission and Update guidance — `guidance_urls[1]`
6. AR Interface Functions guidance — `guidance_urls[2]`
7. Particular Exceptional Circumstances (PEC) guidance — `guidance_urls[3]` (added 2026-09-08, found via the "Content" navigation — see below)

Tracked in `enisa-srp-glossary-baseline.md`:

8. CRA SRP Glossary — `url` in that file's frontmatter

Fetch raw HTML and diff word-for-word against the baseline. Do not rely on a rendered or summarised view — past checks caught wording-level edits that a summary would have hidden.

Fetch with backoff — `curl --retry 5 --retry-delay 5 --retry-all-errors` — because ENISA rate-limits. On 2026-09-07 it answered a burst of requests with HTTP 429.

Then check what actually came back, and treat a bad fetch as a bad fetch:

- **HTTP 429 or 5xx that survives the retries is a check failure, not a change.** Do not touch the baseline, never diff an error page as if it were content, and report the run as failed with the exact status. This is the same mistake class as reading a 403 as an unpublished page: an HTTP status tells you about the fetch, not about the page.
- Confirm each response really is the page — a non-empty HTML body, not an error document — before diffing. Check the content, not just curl's exit code: on 2026-09-07 ten downloads returned error bodies with exit code 0 and were only caught by inspecting the files.

Also walk the page navigation ("Content" subtopics list) on the main page. If a page appears there that is not in either baseline, that is itself a finding: ENISA added the Glossary and the CSIRT list this way on 2026-09-07, and the PEC guidance page this way on 2026-09-08. Add it to the appropriate baseline and say so in the report.

## 2. The Glossary needs specific handling

`enisa-srp-glossary-baseline.md` is the full-detail, field-by-field historical record of the Glossary page, kept as one table row per field (Common / AEV / SI groups) so a single changed field shows up as a single-row diff.

The Glossary page has already moved once: on 2026-09-07 the URL that had been tracked began returning **HTTP 403**, and the page turned out to have been republished at `.../cra-srp-glossary2`. Note also that the FAQ page kept linking to the old path afterwards, so ENISA's own links can be stale. A 403 on this page is therefore an ambiguous signal, not a diagnosis. Rules:

- A non-200 on the Glossary is **not a run failure and not a reason to touch the table content**. Never delete, empty, or trim the baseline because the page is unavailable — it is the record precisely for that case.
- Before concluding anything from a non-200, **look for the page under a new address**: walk the "Content" subtopics navigation on the main SRP page and search the site for a Glossary entry. A moved page is the more likely explanation than an unpublished one. If you find it, update `url` in the frontmatter, keep the previous address in `old_url`, and report the move.
- Only if no replacement address exists is the page genuinely unavailable. Record that in the `status:` line with the UTC timestamp, and report it. Both directions matter: 200 → non-200 and non-200 → 200.
- Correct an earlier wrong diagnosis in `status:` rather than overwriting it silently. The frontmatter is what the next run reads; a stale wrong URL there produces a false reachability finding a week later.
- Only when the page returns 200 do you diff its content and update the tables, `page_version`, and `retrieved`.
- Check the other seven pages in the same run before concluding anything: a Glossary-only failure means ENISA moved, is editing, or unpublished that page; all eight failing means a site-wide outage.

Note that `enisa-srp-faq-baseline.md` also carries a deliberately trimmed summary table of the Glossary fields (in Q16 and its "CRA SRP Glossary" section). That summary is NOT the record — never reconstruct the full baseline from it, and keep the two consistent when the Glossary changes. It also repeats the Glossary URL in prose — when the page moves, update those occurrences too.

## 3. The CSIRT list — diff it, but do not act on it

`csirt_list_url` is the authoritative country → CSIRT-designated-as-coordinator
mapping. Diff it word-for-word like every other page and record changes in
`enisa-srp-faq-baseline.md`, the same as you would for the FAQ.

Do **not** edit `srp-domains-baseline.md` or anything under `srp-domains/`.
That table is owned by the SRP domain reachability routine, which fetches this
same list on its own hourly run and applies changes to its country table
itself — so no handoff is needed and nothing is waiting on you. Touching those
paths would also put your PR outside this routine's auto-merge scope.

Mention a change in your report anyway, briefly, so it is visible from both
sides.

## 4. Recording changes

For each changed page, update the relevant baseline file:

- One logical block per FAQ entry / per guidance subpage / one table row per Glossary field, so diffs stay readable.
- Add an entry at the top of the `## Change log` section, in the format below. Leave existing entries alone; baselines are not renamed retroactively.
- Reproduce ENISA's text as-is, including typos and inconsistencies. Note them rather than silently correcting them — past checks recorded a doubled "inin", a missing "d" in "adress", an untagged Q19, and a duplicated sentence in Q9. That fidelity is the point of a baseline.
- Update `retrieved`, `last_check`, and `last_change` in the frontmatter of whichever file changed. `last_check` moves on every successful check; `last_change` only when content actually changed.
### The change log entry

A reader must be able to take in an entry in half a minute, however much ENISA moved. Substance first, editorial work summarised. Use exactly this shape:

    ### [date] [HH:MM] UTC (vs. [what it was compared against])

    One or two sentences: what a reader needs if they read nothing else.

    **New**
    - Things that did not exist before: a page, a question, a field, a rule.

    **Changed**
    - Substantive changes to something that already existed.

    **Fixed**
    - Defects this record has been tracking that no longer apply. Say so, and stop flagging them.

    **Watch**
    - Contradictions, oddities, anything a later run should keep an eye on.

    **Editorial**
    One line: counts and a pointer, never a list.

    **Unchanged**
    One line, with the identifying stamps.

Rules for it:

- **Empty rubrics are left out.** Keep the order of those that remain.
- **One finding per bullet**, one or two sentences. If a single finding genuinely needs more — a changed reporting path, say — give it its own short `####` heading inside its rubric rather than a long paragraph.
- **Quote verbatim only where the wording is the finding**: a changed obligation, a new field name, a corrected legal reference. Otherwise point at the content sections further down, which already carry the page text in full. Do not reproduce it twice.
- **Editorial means summarised.** Typos, punctuation, capitalisation, link markup, house-style shifts ("Article" → "Art.") get counted, not enumerated: "three new typos and two stray full stops on the rewritten pages, verbatim in the text below". The defects themselves stay marked in the content sections, so nothing is lost by not listing them here.
- **Aim for 250 words.** Not a hard limit — a day like 2026-09-07, with a published platform URL and two new questions, earns more. But an entry over budget is usually one that spelled out editorial work.
- **The heading carries a UTC time** whenever the day already has an entry, which running hourly is normal.
- Separate substantive changes (a question added, deleted or reworded; a changed date, obligation, field, or legal reference) from cosmetic ones (link markup, page numbering) — that separation is what the rubrics are for.

### Nothing changed anywhere

Only when all eight pages came back unchanged. Read `last_check` as it stands on `origin/main`:

    git show origin/main:enisa-srp-faq-baseline.md | sed -n 's/^last_check: //p' | head -1

- If it is **today's date** → today's measurement point is already recorded. Do NOT commit, do NOT open a PR, do NOT report anything. End the run silently. Running hourly, this is the normal outcome for 23 of the 24 daily runs.
- If it is an **earlier date** → this is the first run of the day. Update `last_check` in the frontmatter of both baseline files to today, leave `last_change` alone, then commit, PR and merge per section 5. Do NOT report — a routine heartbeat is not worth a notification.

Never invent a change and never open an empty PR. This silence applies only when nothing changed: **any** substantive change is committed and reported immediately, whatever the time of day and whether or not today already has a measurement point.

## 5. Commit, PR, merge

Only if something actually changed. Commit with a message naming what changed. Push with `git push -u origin HEAD`, retrying up to 4 times with exponential backoff (2s, 4s, 8s, 16s) on network errors only.

If the push fails for lack of credentials (403), do NOT try to route around it — no workarounds, no alternate remotes, no GitHub MCP fallback. Leave the commit on the local branch and report that the push failed, with the exact error AND the branch name you pushed to, so a mismatch with this Routine's configured repository outcome can be spotted.

Otherwise open a pull request as a draft, then mark it ready for review and merge it yourself immediately. This is the standing convention recorded in CLAUDE.md — do not leave the PR waiting for approval. It applies only to PRs that touch `enisa-srp-faq-baseline.md` and/or `enisa-srp-glossary-baseline.md` alone. If your change touches anything else — including `CLAUDE.md` or anything under `srp-domains/` — leave that PR open, do not merge it, and say so.

## 6. If you widen what this routine covers, update this prompt

If you start tracking a new page or a new baseline file, this prompt is now out of date and the next run will not know about it. Say so explicitly in your report, naming this trigger (`trig_015C8QiJhXwkxPkDdoMbkHeD`) and what needs adding, so a human can update it in the Routines UI. A copy of this prompt lives at `routines/enisa-srp-pages-monitor.md` in the repository — update that too, in the same commit as the change that widened the scope.

Updating CLAUDE.md alone is not enough: CLAUDE.md documents the convention, this prompt is what actually runs.

That is exactly how the Glossary was nearly lost. The 2026-09-07 run discovered the page, built the baseline, and updated CLAUDE.md — but this prompt still described a single page and a single file.

## 7. Report

Answer in German, concisely, and in the same shape as the change log entry — same problem, same cure. Lead with one or two sentences on what matters, then the rubrics that apply (**Neu**, **Geändert**, **Behoben**, **Beobachtet**, **Redaktionell**, **Unverändert**), leaving out the empty ones. Editorial work is summarised in a line, never enumerated.

What earns a mention at all:

- **Substantive change on any page** — what changed and where, quoting new or reworded text where the wording is the point. Flag anything touching reporting obligations, deadlines, data fields, or the CSIRT mapping.
- **A new page appeared in the navigation** — name it and say it has been added to the baseline.
- **The CSIRT list changed** — prominently, with the affected countries (see section 3).
- **A Glossary reachability transition or move** — state the direction or the new address, and that the baseline content was left intact.
- **A fetch failed** (429 or 5xx after the retries) — say which page and which status, and that the baseline was left untouched.
- **Nothing changed** — report nothing at all, whether or not this run wrote the day's heartbeat commit. See "Nothing changed anywhere" in section 4. Running hourly, silence is the normal outcome and the only signal worth sending is a real one.

When you report, end with exactly one line (a silent run reports nothing, this line included):
ENISA SRP: [n] Seiten geprüft | geändert: [Seiten oder keine] | Glossary: [HTTP-Code] | push: [OK/FAIL/nichts zu pushen]
