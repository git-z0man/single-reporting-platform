# ENISA SRP pages monitor

- **Trigger**: `trig_015C8QiJhXwkxPkDdoMbkHeD`
- **Schedule**: `0 5 * * 1` (Mondays 05:00 UTC)
- **Writes**: `enisa-srp-faq-baseline.md`, `enisa-srp-glossary-baseline.md`
- **Updatable by an agent**: **no** — created via `http_api`, so the prompt below
  must be pasted into the Routines UI by hand.

> **Not yet applied.** The live Routine still runs the original June prompt,
> which fetches only the main SRP page and diffs only
> `enisa-srp-faq-baseline.md`. Paste the text below into the Routines UI to
> bring it in line with what the monitor actually covers.

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

## 1. The pages to check — all seven

Both baseline files carry the authoritative URL list in their frontmatter. Read them first and use the URLs recorded there; the list below is what it should be, but the files win if they disagree (they get updated when ENISA moves a page).

Tracked in `enisa-srp-faq-baseline.md`:

1. Main SRP page — `url` in the frontmatter
2. FAQ subpage — `faq_url`
3. List of CSIRTs Designated as Coordinators — `csirt_list_url`
4. AR User Registration guidance — `guidance_urls[0]`
5. AR Notification Submission and Update guidance — `guidance_urls[1]`
6. AR Interface Functions guidance — `guidance_urls[2]`

Tracked in `enisa-srp-glossary-baseline.md`:

7. CRA SRP Glossary — `url` in that file's frontmatter

Fetch raw HTML and diff word-for-word against the baseline. Do not rely on a rendered or summarised view — past checks caught wording-level edits that a summary would have hidden.

Also walk the page navigation ("Content" subtopics list) on the main page. If a page appears there that is not in either baseline, that is itself a finding: ENISA added the Glossary and the CSIRT list this way on 2026-09-07. Add it to the appropriate baseline and say so in the report.

## 2. The Glossary needs specific handling

`enisa-srp-glossary-baseline.md` is the full-detail, field-by-field historical record of the Glossary page, kept as one table row per field (Common / AEV / SI groups) so a single changed field shows up as a single-row diff.

The live Glossary page is unreliable — it returned **HTTP 403 on 2026-09-07** while every other tracked SRP page returned 200. Therefore:

- A 403 (or any non-200) on the Glossary is **not a run failure and not a reason to touch the table content**. Never delete, empty, or trim the baseline because the page is unavailable — it is the record precisely for that case.
- A reachability transition is itself a reportable finding. Update the `status:` line in the frontmatter with what you found and the UTC timestamp, and mention it in the report. Both directions matter: 200 → 403 and 403 → 200.
- Only when the page returns 200 do you diff its content and update the tables, `page_version`, and `retrieved`.
- Check the other six pages in the same run before concluding anything: a Glossary-only failure means ENISA is editing or unpublishing that page; all seven failing means a site-wide outage.

Note that `enisa-srp-faq-baseline.md` also carries a deliberately trimmed summary table of the Glossary fields (in Q16 and its "CRA SRP Glossary" section). That summary is NOT the record — never reconstruct the full baseline from it, and keep the two consistent when the Glossary changes.

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
- Add a dated `## Change log (<date> check, vs. <previous date> baseline)` section at the top of the change log, naming what was added, deleted, or reworded. Quote new or changed text verbatim.
- Reproduce ENISA's text as-is, including typos and inconsistencies. Note them rather than silently correcting them — past checks recorded a doubled "inin", a missing "d" in "adress", an untagged Q19, and a duplicated sentence in Q9. That fidelity is the point of a baseline.
- Separate substantive changes (a question added, deleted or reworded; a changed date, obligation, field, or legal reference) from cosmetic ones (link markup, page numbering).
- Update `retrieved`, `last_check`, and `last_change` in the frontmatter of whichever file changed. `last_check` moves on every successful check; `last_change` only when content actually changed.

If nothing changed anywhere, update `last_check` in both files and leave `last_change` alone. If that leaves nothing to commit because the dates already say today, do not invent a change and do not open an empty PR.

## 5. Commit, PR, merge

Only if something actually changed. Commit with a message naming what changed. Push with `git push -u origin HEAD`, retrying up to 4 times with exponential backoff (2s, 4s, 8s, 16s) on network errors only.

If the push fails for lack of credentials (403), do NOT try to route around it — no workarounds, no alternate remotes, no GitHub MCP fallback. Leave the commit on the local branch and report that the push failed, with the exact error AND the branch name you pushed to, so a mismatch with this Routine's configured repository outcome can be spotted.

Otherwise open a pull request as a draft, then mark it ready for review and merge it yourself immediately. This is the standing convention recorded in CLAUDE.md — do not leave the PR waiting for approval. It applies only to PRs that touch `enisa-srp-faq-baseline.md` and/or `enisa-srp-glossary-baseline.md` alone. If your change touches anything else — including `CLAUDE.md` or anything under `srp-domains/` — leave that PR open, do not merge it, and say so.

## 6. If you widen what this routine covers, update this prompt

If you start tracking a new page or a new baseline file, this prompt is now out of date and the next run will not know about it. Say so explicitly in your report, naming this trigger (`trig_015C8QiJhXwkxPkDdoMbkHeD`) and what needs adding, so a human can update it in the Routines UI. A copy of this prompt lives at `routines/enisa-srp-pages-monitor.md` in the repository — update that too, in the same commit as the change that widened the scope.

Updating CLAUDE.md alone is not enough: CLAUDE.md documents the convention, this prompt is what actually runs.

That is exactly how the Glossary was nearly lost. The 2026-09-07 run discovered the page, built the baseline, and updated CLAUDE.md — but this prompt still described a single page and a single file.

## 7. Report

Answer in German, concisely.

- **Substantive change on any page** — what changed, on which page, quoting new or reworded text where it matters. Flag anything touching reporting obligations, deadlines, data fields, or the CSIRT mapping.
- **A new page appeared in the navigation** — name it and say it has been added to the baseline.
- **The CSIRT list changed** — prominently, with the affected countries (see section 3).
- **A Glossary reachability transition** — state the direction and that the baseline content was left intact.
- **Nothing changed** — one line.

End with exactly one line:
ENISA SRP: <n> Seiten geprüft | geändert: <Seiten oder keine> | Glossary: <200/403> | push: <OK/FAIL/nichts zu pushen>
