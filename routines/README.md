# Scheduled routine prompts

The three monitors in this repository are driven by scheduled Routines. What a
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
| `enisa-srp-pages-monitor.md` | **Single Reporting FAQ monitor** | `trig_015C8QiJhXwkxPkDdoMbkHeD` | `0 5 * * 1` |
| `commission-cra-faq-monitor.md` | **Commission CRA FAQ monitor** | `trig_012AzfKXKrPnRCEjXXYWBgY4` | `0 5 * * 1` |
| `srp-domains-monitor.md` | **SRP domain reachability monitor** | `trig_01426ap5KJGGrY4Fk2pbTm8s` | `22 * * * *` |

The UI name and the file name differ for the first one: an attempt to rename it
to "ENISA SRP pages monitor" was refused along with the prompt update (see
below), so the UI still shows its original name. Go by the trigger ID.

| Prompt file | Writes |
|---|---|
| `enisa-srp-pages-monitor.md` | `enisa-srp-faq-baseline.md`, `enisa-srp-glossary-baseline.md` |
| `commission-cra-faq-monitor.md` | `commission-cra-faq-baseline.md`, `commission-faq/` |
| `srp-domains-monitor.md` | `srp-domains-baseline.md`, `srp-domains/` |

Other Routines on this account (`CRA notified body alert`, `FuFA Reisen`,
`absence.io Zeiterfassung`) do not write to this repository and are not
mirrored here.

## Two routines watch the SRP — on purpose

`Single Reporting FAQ monitor` reads ENISA's **web pages** and diffs their
wording. `SRP domain reachability monitor` probes the 29 **hosts** of the
production zone and classifies whether they answer. Same subject, different
signal — and, decisively, different cadence: weekly for pages that change every
few weeks, hourly for a go-live that has to be caught when it happens.

Merging them would force one of two bad outcomes: fetching seven ENISA pages
every hour, or slowing go-live detection to a weekly beat, which would defeat
the only reason the domain monitor exists. They also fail differently (a 403 on
an ENISA page and a dark production host mean opposite things) and their
auto-merge scopes are disjoint, so a combined run touching both would fall out
of auto-merge entirely.

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
