# Guide sync

- **Trigger**: not created yet - see "Guide sync" in `routines/README.md`; its ID goes here once it exists
- **Schedule**: `30 7 * * *` (daily, 07:30 UTC - after the ENISA monitor at 06:04 and the domain monitor at 06:00, so any baseline PR they opened is already merged)
- **Writes**: `index.html`, `guide-sync/`
- **Live prompt**: a loader that reads this file from `main` - see "Loader prompts" in `routines/README.md`. Everything below the `---` line is the prompt.
- **Loader status**: **Routine not created yet** (2026-10-04).
- **Updatable by an agent**: **yes** once created, because an agent will create it (`meta_mcp`). An agent cannot attach the repository, though: `create_trigger` takes no sources or outcomes, so a person does that once in the Routines UI before enabling it.
- **Canary**: while `tools/guide-sync.paused` exists on `main` this Routine opens **draft** pull requests only and never merges. Deleting that file arms auto-merge.

> **What it is for.** The monitors record what ENISA changed; they never touch the guide, and until now nothing did except a person in a session. Between 15 and 21 September the guide fell behind on a reversed access rule, a new FAQ question and three Glossary fields, and a full audit on 4 October found its field cross-references mostly broken. This Routine closes that gap for everything a script can decide, and hands the rest to a person with the question already framed.
>
> **What it will and will not do on its own.** Mechanical: counts, versions and dates in `data-sync` markers, link repoints for pages ENISA moved, new FAQ questions appended verbatim, typo-class corrections, new Glossary cards for fields that are optional at every stage. Judgment, never merged unattended: a rewritten FAQ answer, a changed stage, a new Required field (the phase tables must change too), a changed link target, a removed question or field. `tools/README.md` has the full rules.

---

Keep the guide (`index.html`) in line with ENISA's FAQ and Glossary.

Repository: git-z0man/single-reporting-platform (public)

Read `CLAUDE.md` and `tools/README.md` first. The reasoning behind everything below is recorded there.

## 0. Repository and branch

Find the working tree by its remote rather than by guessing a path:

    for d in */ .; do
      git -C "$d" remote get-url origin 2>/dev/null | grep -q single-reporting-platform && cd "$d" && break
    done
    git remote -v   # must name git-z0man/single-reporting-platform

If it is not checked out, clone it: `git clone https://github.com/git-z0man/single-reporting-platform && cd single-reporting-platform`.

Do NOT hard-code a branch name; the platform assigns this Routine's outcome branch a fresh name whenever the Routine is edited. Stay on the branch the session gave you (if that is `main`, create `guide-sync` from it). Then:

    git fetch origin
    # If origin/[your branch] exists and carries commits that are not in origin/main, an
    # earlier run's pull request is still open. Continue it, so a pending decision is not made twice:
    git reset --hard origin/[your branch] && git merge --no-edit origin/main
    # Otherwise:
    git reset --hard origin/main

Never push to `main`.

Before relying on the tools, run their own tests: `python3 -m unittest discover -s tools/tests -t .`. If they fail the tools are broken: report that and stop. Do not work around it and do not edit anything.

## 1. Observe

    python3 tools/fetch_enisa.py

Exit 0: nothing changed on ENISA's side. Exit 1: `guide-sync/` was rewritten. **Exit 2: the fetch failed.** A rate-limit or server error (HTTP 429, 5xx) or a page that no longer parses is a failed check, never a content change. Change nothing, report the exact message and stop. Do not edit the JSON by hand and do not "fix" the parser to get past it.

## 2. Is there anything to do?

    python3 tools/check_guide.py

If it exits 0 and `git status --porcelain` is empty, the guide matches ENISA. End the run silently: no commit, no PR, no report. That is the normal outcome on almost every day. Exit 2 means the check itself broke: report it and stop.

## 3. Sync

    python3 tools/sync_guide.py --json

The report's `mechanical` list is what was edited. Its `judgment` list is what only a person can decide, and **was not edited**.

Do not edit `index.html` or anything under `guide-sync/` by hand, for any reason. Section 4 recomputes the change and demands byte equality, so one hand edit disqualifies it from auto-merge; and anything that needs words of your own belongs in the pull request description, not in the guide.

Run `python3 tools/check_guide.py` again. What it still reports should be exactly the judgment items. Anything else is a bug in the tools: report it, do not merge.

## 4. Merge, or leave it for a person

Auto-merge only when **all** of these hold:

1. the sync report says `eligible_for_auto_merge` is true (which implies no judgment items);
2. `python3 tools/verify_mechanical.py origin/main` exits 0;
3. `python3 tools/scope_guard.py index.html guide-sync/` exits 0;
4. `python3 tools/check_guide.py` exits 0;
5. `tools/guide-sync.paused` does **not** exist on `origin/main`: `git cat-file -e origin/main:tools/guide-sync.paused` exiting 0 means it exists, so never auto-merge.

If any one fails, the pull request stays a draft.

## 5. Commit, PR, merge

Commit exactly what the tools wrote, with a message naming what changed, for example "Guide sync: FAQ Q34 added, Glossary 1.5". Push with `git push -u origin HEAD`, retrying up to 4 times with exponential backoff (2s, 4s, 8s, 16s) on network errors only. If the push fails for lack of credentials (403), do NOT try to route around it - no workarounds, no alternate remotes, no GitHub MCP fallback. Leave the commit on the local branch and report the exact error and the branch name.

Open a pull request as a draft. If section 4 allows it, mark it ready for review and merge it yourself immediately. That is the standing convention recorded in CLAUDE.md, and it applies only to pull requests from this Routine that touch `index.html` and `guide-sync/` alone and pass `verify_mechanical.py`.

Otherwise leave it open. Its description lists every judgment item (class, target, detail), what was edited mechanically, and what you would check for each: a new Required field, for instance, means the phase tables and the walkthrough need a row, and a rewritten FAQ answer means a person should read whether the walkthrough still agrees with it.

## 6. Report

Answer in German, concisely. Stay silent when nothing changed. Report only when:

- **something was merged into the published guide unattended**: one line on what changed, because nobody reviewed it first;
- **a draft pull request was opened or updated**: one line per judgment item, saying what needs a decision;
- **the run failed**: which step, and the exact message.

When you report, end with exactly one line:
Guide sync: [n] mechanisch | [n] Urteil offen | merge: [auto/Entwurf/keine Änderung]
