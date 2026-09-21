# Scheduled routine prompts

The four monitors in this repository are driven by scheduled Routines. What a
Routine actually executes is its **prompt**, held by the platform — not
anything in this repository. This directory keeps a copy of each prompt under
version control so that:

- drift between what a routine *does* and what the repository *says* is visible
  in a diff rather than discovered by accident;
- a prompt can be reviewed, and its history read, like any other file;
- the text is ready to paste back into the Routines UI.

**These files are a mirror, not the source of truth.** Editing one here changes
nothing on its own. The corresponding Routine must be updated too — see below
for which ones an agent may update and which need a human.

## The routines

| Prompt file | Name in the Routines UI | Trigger ID | Schedule |
|---|---|---|---|
| `enisa-srp-pages-monitor.md` | **Single Reporting FAQ monitor** | `trig_015C8QiJhXwkxPkDdoMbkHeD` | `0 5 * * 1` recorded — **but it is observably running daily**, see below |
| `commission-cra-faq-monitor.md` | **Commission CRA FAQ monitor** | `trig_012AzfKXKrPnRCEjXXYWBgY4` | `0 5 * * 1` |
| `srp-domains-monitor.md` | **SRP domain reachability monitor** | `trig_01426ap5KJGGrY4Fk2pbTm8s` | `22 * * * *` |
| `notified-bodies-monitor.md` | **CRA notified body alert** | `trig_01V74LWJSJ7QETodKUS5DojP` | `0 7 * * 1-5` |

The UI name and the file name differ for the first one: an attempt to rename it
to "ENISA SRP pages monitor" was refused along with the prompt update (see
below), so the UI still shows its original name. Go by the trigger ID.

| Prompt file | Writes |
|---|---|
| `enisa-srp-pages-monitor.md` | `enisa-srp-faq-baseline.md`, `enisa-srp-glossary-baseline.md` |
| `commission-cra-faq-monitor.md` | `commission-cra-faq-baseline.md`, `commission-faq/` |
| `srp-domains-monitor.md` | `srp-domains-baseline.md`, `srp-domains/` |
| `notified-bodies-monitor.md` | `notified-bodies-baseline.md`, `notified-bodies/` |

Other Routines on this account (`FuFA Reisen`, `absence.io Zeiterfassung`) do
not write to this repository and are not mirrored here.

## The ENISA monitor ran hourly from 2026-09-07 to 2026-09-14

Weekly by design. For that one week it ran `0 * * * *` instead: ENISA
signalled frequent edits in the run-up to the 11 September go-live, and a
Tuesday change would otherwise have sat unnoticed until the following Monday.
It earned its keep — 89 dated change-log entries accumulated in
`enisa-srp-faq-baseline.md` over the week, 38 of them in the last five days
alone, with no long silent stretch — and reverted to `0 5 * * 1` on schedule
on 2026-09-14, per the revert note recorded in the prompt file's header at
the time.

## The recorded weekly schedule is not what is running (noted 2026-09-21)

The revert above updated these mirrored files to `0 5 * * 1`. The live cron on
`trig_015C8QiJhXwkxPkDdoMbkHeD` was evidently never changed to match: the
monitor has produced a check every day since, at roughly 06:10 UTC — change
entries on 15, 17, 18, 19 and 21 September and silent heartbeat commits on the
16th and 20th. That is neither the day nor the hour this table records.

Do not "fix" this by slowing the routine down without thinking about it. Daily
is what caught FAQ Q32 within hours of publication on 21 September, and ENISA
has kept editing at a pace weekly cadence would badly under-sample. The honest
options are to update this mirror to match the daily reality, or to set the
cron to the weekly value recorded here — the first is recommended, and either
way the two should agree. Changing the cron is a manual step in the Routines
UI; see "Who can update which" below.

Hourly was not just a cron change. Three rules had to go into the prompt
first, or the faster beat would have been a downgrade — and all three stayed
in the prompt after the revert, since they hold at any cadence:

- **Silence when nothing changed.** Without it, 23 notifications a day saying
  nothing happened. The rule is the one the domain monitor already uses: read
  `last_check` from `origin/main`, and if it is today, end the run with no
  commit, no PR and no report. One heartbeat commit per day, notifications only
  for real findings.
- **A UTC time in the change log heading** once a day already has a section.
  Two same-day sections titled identically is not a hypothetical: it happened
  on 2026-09-07 and was disentangled by hand into "morning" and "evening".
- **429 and 5xx are check failures, not changes.** ENISA rate-limited a burst
  of requests that day. Seven pages an hour, on top of the domain monitor's own
  hourly fetch of the CSIRT list, makes that likelier — and an error page
  diffed as content would corrupt the baseline.

## Watching a page is not watching the PDF it links to (added 2026-09-21)

The AR User Manual entered this routine's scope on 2026-09-10 as page 9 of
eleven — meaning its **landing page** was diffed every run. The document that
page exists to distribute was never fetched at all.

On 2026-09-17 ENISA republished the PDF at the same URL with a reversed
permission rule: the sentence saying a Secondary AR cannot see another AR's
notifications was deleted and replaced by one saying every AR of the
manufacturer can access and update all of them. The landing page did not
change, so the monitor reported the manual unchanged for four consecutive
days. The change was found by hand on 21 September, and only because someone
went looking.

What makes this worse than an ordinary miss is that the document's own change
signals are inert: both copies are stamped "Version: 1.1", and the Document
History table lists only "09/09/2026 v1.0 First version" in both. Size and PDF
ModDate are the only honest evidence. So the prompt now carries section 1a:
hash the PDF every run, compare against `ar_user_manual_pdf_sha256` in
`enisa-srp-faq-baseline.md`'s frontmatter, and diff the extracted text when
the hash moves.

The general lesson, worth applying to any document this or another routine
picks up: **if a tracked page's purpose is to hand out a file, the file needs
its own checksum.** Diffing the wrapper proves nothing about the contents.

Note this did not widen the routine's auto-merge scope — it still writes only
`enisa-srp-faq-baseline.md` and `enisa-srp-glossary-baseline.md`, so `CLAUDE.md`
needed no change. Archiving PDF copies *would* have widened it, and was
deliberately not done.

## Two routines watch the SRP — on purpose

`Single Reporting FAQ monitor` reads ENISA's **web pages** and diffs their
wording. `SRP domain reachability monitor` probes the 29 **hosts** of the
production zone and classifies whether they answer. Same subject, different
signal — and normally a different cadence: weekly for pages that change every
few weeks, hourly for a go-live that has to be caught when it happens.

They shared a cadence for one week (see above), and that changed nothing: the
reason to keep them apart was never only the schedule. They fail differently —
a 403 on an ENISA page and a dark production host mean opposite things, and
each needs its own reading. Their auto-merge scopes are disjoint, so a
combined run touching both files would fall out of auto-merge entirely. The
shared cadence was also temporary on only one side: the pages monitor reverted
to weekly on 14 September, while the domain monitor stays hourly for as long
as go-live detection matters. A merged routine would then have been stuck
picking one of the two beats, which is exactly the bind this separation
avoids.

**Where they did overlap, ownership decides, not merging.** ENISA's CSIRT
coordinator list is both a page to diff and the source of the country table in
`srp-domains-baseline.md`. The domain monitor owns that table, so it fetches
the list itself and applies changes directly; the pages monitor diffs the same
page for its own baseline and reports, but does not reach across. Each file has
exactly one writer, and nothing waits on a human to relay a change.

## Who can update which

A Routine created through the API or the Routines UI can only be edited by a
human, in that UI. An agent's `update_trigger` is refused:

```
update_trigger: this routine was created via "http_api", not by an agent.
Agents can only update routines they created (via create_trigger).
```

| Routine | Created via | Agent may update the prompt? |
|---|---|---|
| ENISA SRP pages monitor | `http_api` | **No — paste it in the Routines UI** |
| Commission CRA FAQ monitor | `meta_mcp` | Yes |
| SRP domain reachability monitor | `meta_mcp` | Yes |
| CRA notified body alert | `http_api` | **No — paste it in the Routines UI** |

## The paste path eats angle brackets

Verified on 2026-09-07, after the ENISA prompt was pasted in by hand: three of
its four `<placeholder>` markers were gone from the stored prompt. Its closing
report line went from

```
ENISA SRP: <n> Seiten geprüft | geändert: <Seiten oder keine> | Glossary: <HTTP-Code> | push: <OK/FAIL/nichts zu pushen>
```

to

```
ENISA SRP: Seiten geprüft | geändert: | Glossary: | push: <OK/FAIL/nichts zu pushen>
```

`<n>`, `<Seiten oder keine>` and `<HTTP-Code>` were stripped as if they were
HTML tags, while `<date>`, `<previous date>` and `<OK/FAIL/nichts zu pushen>`
in the same prompt survived. The rule is not obvious and not worth reverse
engineering.

It is the paste path, not storage: both `meta_mcp` routines keep every angle
bracket they were given (7 and 20 respectively), because they were set through
the API.

**So write placeholders in square brackets** — `[n]`, `[date]` — in any prompt
that will be pasted through the UI. They survive, and nothing else in these
prompts depends on the character. `enisa-srp-pages-monitor.md` already uses
them; the other two are set through the API and are left as they are.

After pasting, check what actually landed rather than assuming: read the
Routine back (`list_triggers` returns the stored text in
`derived_state.prompt`) and diff it against the file here, ignoring the
markdown the UI strips — backticks, `##`, list numbering and blank lines all
disappear, which is expected and harmless.

## Moving a routine to another repository

A Routine's **prompt** says what to do. Which repositories it may read and write
is separate: platform-side session config, `sources` and `outcomes`.

**No agent tool can change that.** `create_trigger` does not accept `sources` or
`outcomes` at all, and `update_trigger` reaches only name, schedule, enabled
state, model and prompt. A repository move is therefore never a prompt edit, and
pasting a repointed prompt before the config moves makes things worse rather
than better: the run looks for files that are not in its checkout and its push
comes back 403.

The order that works is **config first, prompt second**.

`CRA notified body alert` went through this on 2026-09-08, in that order:
config first, then the prompt, which was read back afterwards and matched the
mirror exactly. The config lists both repositories, as sources and as outcomes:

```
sources:  git-z0man/notified-bodies, git-z0man/single-reporting-platform
outcomes: git-z0man/notified-bodies      → claude/fervent-hamilton
          git-z0man/single-reporting-platform → claude/nifty-pasteur
```

Two consequences worth knowing before writing a prompt for such a Routine:

- **The session checks out more than one repository**, so "the repository" is
  ambiguous and a bare `git push` can update the wrong one. The prompt has to
  select its working tree explicitly — `notified-bodies-monitor.md` does it by
  matching `git remote get-url origin`, not by assuming a path.
- **Each outcome gets its own branch name**, reassigned whenever the Routine is
  edited. Prompts stay branch-agnostic and push with `git push -u origin HEAD`
  from inside the right checkout.

Leaving the old repository attached does no harm once the prompt stops writing
to it. Removing it later is tidying, not a fix.

## Keeping a prompt in sync

A monitor's scope grows over time — a new page appears, a new baseline file is
added. When that happens the prompt must grow with it, or the next run silently
reverts to the narrower job.

This is not hypothetical. On 2026-09-07 the ENISA run discovered ENISA's new
CRA SRP Glossary page, built `enisa-srp-glossary-baseline.md`, and updated
`CLAUDE.md` — while its own prompt still described a single page and a single
file. The routine was more thorough than its instructions, and nothing would
have carried that forward to the next run.

So, whenever a change widens what a monitor covers:

1. Update the prompt file here, in the same commit as the repository change.
2. Apply it to the live Routine — `update_trigger` where allowed, otherwise
   paste it into the Routines UI.
3. Update `CLAUDE.md` if the auto-merge scope changed (it lists the exact paths
   each routine may self-merge).

Step 2 is the one that actually takes effect. Steps 1 and 3 are documentation:
useful, but a routine does not read them at run time.

## The outcome branch is reassigned

The platform gives a Routine's repository outcome a fresh branch name every
time the Routine is edited (`claude/youthful-fermat` became
`claude/trusting-hawking` after a single edit). None of these prompts hard-code
a branch: they use whatever branch the session provides and push with
`git push -u origin HEAD`.

A Routine with two outcomes gets one branch per repository, each reassigned on
the same schedule — see "Moving a routine to another repository" above. The
branch is not the risk there; the working directory is.
