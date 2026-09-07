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

| Prompt file | Trigger ID | Schedule | Writes |
|---|---|---|---|
| `enisa-srp-pages-monitor.md` | `trig_015C8QiJhXwkxPkDdoMbkHeD` | `0 5 * * 1` | `enisa-srp-faq-baseline.md`, `enisa-srp-glossary-baseline.md` |
| `commission-cra-faq-monitor.md` | `trig_012AzfKXKrPnRCEjXXYWBgY4` | `0 5 * * 1` | `commission-cra-faq-baseline.md`, `commission-faq/` |
| `srp-domains-monitor.md` | `trig_01426ap5KJGGrY4Fk2pbTm8s` | `22 * * * *` | `srp-domains-baseline.md`, `srp-domains/` |

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
