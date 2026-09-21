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
| `enisa-srp-pages-monitor.md` | **Single Reporting FAQ monitor** | `trig_015C8QiJhXwkxPkDdoMbkHeD` | `4 6 * * *` |
| `commission-cra-faq-monitor.md` | **Commission CRA FAQ monitor** | `trig_012AzfKXKrPnRCEjXXYWBgY4` | `0 5 * * 1` |
| `srp-domains-monitor.md` | **SRP domain reachability monitor** | `trig_01426ap5KJGGrY4Fk2pbTm8s` | `0 6 * * *` |
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
alone, with no long silent stretch. The documented revert to `0 5 * * 1` on
2026-09-14 was written into these files but never applied to the Routine; see
the section below for how that was found and resolved.

## The weekly revert never happened, and daily is now the intended cadence

The 2026-09-14 revert updated these mirrored files to `0 5 * * 1`. The live cron
was never changed to match — it is `4 6 * * *`, daily at 06:04 UTC, confirmed by
reading the Routine back on 2026-09-21. The mirror said weekly for a week while
the monitor ran daily.

Resolved in favour of what was running. Daily is what caught FAQ Q32 within
hours of publication on 21 September, and ENISA has been editing at a pace
weekly cadence would badly under-sample — the hourly week alone produced 89
change-log entries. The table above now records `4 6 * * *`; no cron change is
outstanding.

The lesson is narrower than "keep the docs in sync": **a cron written here is a
claim about someone else's system, and it goes stale the moment a paste is
skipped.** Read the Routine back with `list_triggers` rather than trusting this
file, the same way the paste-path section below says to verify a pasted prompt.
That check is what found this, and it found the domain monitor's mismatch in the
same pass.

## The domain monitor switched its own schedule, as designed

Not drift, and worth distinguishing from the case above. Hourly was only ever
for catching the go-live. Section 5 of `srp-domains-monitor.md` therefore told
the run to switch itself: call `update_trigger` on
`trig_01426ap5KJGGrY4Fk2pbTm8s` with `0 6 * * *`, once, on or after
12 September, and skip it if already set — with a fallback line to report the
switch as outstanding if the tool was unavailable, which in that Routine's
sessions it normally is. The switch was applied on 2026-09-13 17:38 UTC and the
cron has read `0 6 * * *` since. The instruction did its job; only this file
never caught up, and claimed `22 * * * *` for another eight days.

The instruction has now been removed from both the mirror and the live prompt,
because a completed one-shot task left in a prompt is not harmless: every run
re-read it, and its own fallback line said to report "Zeitplanumstellung auf
täglich steht noch aus" whenever `update_trigger` was unavailable — which that
Routine's sessions normally are. It was one unlucky run away from reporting an
outstanding task that had been done days earlier.

**So: a self-modifying instruction needs a removal step, and the removal is not
optional.** If a prompt tells a routine to change something once, whoever
confirms it happened also deletes the instruction and corrects this file.

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
  fetch of the CSIRT list, made that likelier — and an error page diffed as
  content would corrupt the baseline. Both monitors are daily now, so the
  request volume is far lower, but the rule stands: a 429 is a failed check,
  never a change.

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
signal.

They now also run at nearly the same time — `4 6 * * *` and `0 6 * * *`, four
minutes apart — so the cadence argument for keeping them separate has
evaporated entirely. It was never the real one. They fail differently: a 403 on
an ENISA page and a dark production host mean opposite things, and each needs
its own reading. Their auto-merge scopes are disjoint, so a combined run
touching both files would fall out of auto-merge altogether. And each is free
to change beat without dragging the other along, which is precisely what
happened — the domain monitor went hourly-to-daily on 13 September and the
pages monitor hourly-to-daily on its own schedule, neither affecting the other.
Keep them apart for those reasons, not for the clock.

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
