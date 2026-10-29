# Commission CRA FAQ monitor

- **Trigger**: `trig_012AzfKXKrPnRCEjXXYWBgY4`
- **Schedule**: `0 5 * * 1`
- **Writes**: `commission-cra-faq-baseline.md`, `commission-faq/`
- **Live prompt**: a loader that reads this file from `main` - see "Loader prompts" in `routines/README.md`. Everything below the `---` line is the prompt; editing it changes the next run, with no paste in between.
- **Loader status**: **applied 2026-10-04**, read back from the Routine and equal to the loader in `routines/README.md`. This file is the prompt.
- **Updatable by an agent**: **yes** - created via `meta_mcp`, so `update_trigger` works; an agent applies the loader.
- **Dependencies (changed 2026-10-08)**: *before*, every run that found a new version installed whatever pypdf release PyPI served that day, with no version and no hash, in a session that can push to this repository. *After*, pypdf is pinned by version and wheel hash in `requirements.txt`, installed with `--require-hashes --only-binary :all:`, and checked against OSV first (`tools/check_pins.py`). Why, and how to move the pin: `DEPENDENCIES.md`, which applies ENISA's secure-package-consumption skill.

---

Check the European Commission's "FAQs on the Cyber Resilience Act" for a new version, and the CRA implementation factpage for changes.

Repository: git-z0man/single-reporting-platform (public)

## 0. Repository and branch

If the repository is already checked out in the working directory, use it. If it is not, clone it:

    git clone https://github.com/git-z0man/single-reporting-platform && cd single-reporting-platform

Then read `commission-faq/README.md` — it documents the layout, the detection signal and the tooling.

Do NOT hard-code a state branch name. This Routine's configured repository outcome gets a fresh branch name assigned by the platform whenever the Routine is edited, so any name written here goes stale. Instead:

- If the session already has a branch checked out that is not `main`, stay on it and refresh it from main: `git fetch origin main && git reset --hard origin/main`.
- Otherwise create one from main: `git fetch origin main && git checkout -B commission-faq-monitor origin/main`.

Never push to `main`. Never create a new per-run branch when the session already gave you one.

## 1. Detect the current version

The authoritative signal is the version the FAQ document itself carries, NOT the landing page's "Last update" date (that also moves for edits which do not change the document).

The newsroom document ids are stable slots: the Commission replaces the file behind `document/122331` (PDF) and `document/123307` (Markdown) in place for a new version, and the `Content-Disposition` filename carries the version. Verified 2026-10-29 against the Internet Archive — captures of 122331 from 2025-12-03, 2026-02-15, 2026-08-06 and 2026-10-18 hash byte-identically to the archived v1.0, v1.2, v1.3 and v1.4. So this one request is the primary version check, and it is the one that keeps answering when the digital-strategy pages do not:

    curl -sSLI https://ec.europa.eu/newsroom/dae/redirection/document/122331 | grep -i content-disposition

As of the v1.4 baseline that returns `FAQs_on_the_CRA__v14_..._122331.pdf`: `v15` or higher is a new version, `v14` is none. What this check cannot see is a file replaced without a version bump; the sha256 in the manifest is the cross-check if that is ever suspected.

Then fetch the landing page as the secondary check, in case the Commission breaks that practice and publishes a new version under a NEW document id:
https://digital-strategy.ec.europa.eu/en/library/cyber-resilience-act-implementation-frequently-asked-questions
Extract every download link (PDF and Markdown) and their document ids. An id the manifest does not know wins over 122331. If the page is unreachable, the version check above still stands: say so and carry on.

Compare against `current_version` in `commission-faq/versions/manifest.json`.

**A fetch that fails is a failed check, never "unchanged".** The digital-strategy pages
answer 403 to automated fetchers: it happened on 2026-10-26 to both the landing page and
the factpage, and the Internet Archive's own crawler was refused the landing page on
2026-10-23. Both answer 200 from an ordinary browser. When either does not return 200
after the retries:

- do not touch `last_check`, do not write a change-log entry, do not edit a version
  table — a 403 says nothing about whether the document changed;
- record the attempt instead, per section 1a, so the gap is visible in the baseline and
  not only in a run log;
- send curl's own `User-Agent` and no other, on **every** request including the first.
  A browser `User-Agent`, or any other disguise, is bot-check circumvention: this
  platform denies the call and the denial costs the attempt. The 2026-10-26 run put
  `-A "Mozilla/5.0"` in its very first fetch of both pages and lost it that way before
  it had a plain answer to record;
- the newsroom document id above is served by a different host and has kept answering
  through the 403s, so the version check itself usually still works. Say in the report
  which of the three checks ran and which did not, as the 2026-10-26 run did.

If `last_attempt_result` on `origin/main` already records a blocked fetch and today's
run is blocked again, that is two in a row: the source needs a person rather than
another attempt, and the report says so in those words.

## 1a. Record the attempt

`last_check` is the date of the last check that ran in full; `last_attempt` is the date
of the last run, whatever came of it. A reader compares the two: equal means the source
was actually seen, a gap means it was not.

- **Everything returned 200**: move `last_attempt` with `last_check` in section 2a or
  2b, and set `last_attempt_result` to `ok`.
- **Something was blocked**: set `last_attempt` to today and `last_attempt_result` to
  one line naming each check that failed with its status code and each that ran with its
  result. Leave `last_check` and `last_change` as they are, and add one row to the
  "Check log" table of `commission-cra-faq-baseline.md`. Nothing else.

Both fields sit in the frontmatter of `commission-cra-faq-baseline.md` and at the top of
`commission-faq/versions/manifest.json`; keep them equal in the two files. If
`last_attempt` on `origin/main` is already today's date, end the run silently — one row
per day, the rhythm the other monitors keep. Otherwise commit, PR and merge per section
5: a blocked run touches `commission-cra-faq-baseline.md` and `commission-faq/` alone,
so it stays inside this Routine's auto-merge scope.

## 2a. If there is NO new version

Read `last_check` from `commission-faq/versions/manifest.json` as it stands on `origin/main`:

    git show origin/main:commission-faq/versions/manifest.json | python3 -c "import json,sys; print(json.load(sys.stdin)['last_check'])"

- If it is already today's date → nothing to record. Do NOT commit, do NOT open an empty PR. End the run and report one line that the check ran.
- Otherwise → update `last_check`, `last_attempt` and `last_attempt_result` in that manifest and in the frontmatter of `commission-cra-faq-baseline.md`, leave `last_change` alone, then commit, PR and merge per section 5.

Still check the factpage — see section 4.

## 2b. If there IS a new version

1. Download the new PDF and, if published, the Markdown, into `commission-faq/versions/` as `FAQs-on-the-CRA-v<VERSION>.pdf` / `.md`.

2. Produce the canonical text. pypdf is needed: the repository's only third-party package, pinned by version and hash in `requirements.txt`. The system Python may ship a broken `cryptography` that pypdf imports, so use a throwaway venv:

       python3 tools/check_pins.py
       python3 -m venv /tmp/venv && /tmp/venv/bin/pip install --require-hashes --only-binary :all: -r requirements.txt
       /tmp/venv/bin/python commission-faq/tools/extract_text.py \
           commission-faq/versions/FAQs-on-the-CRA-v<VERSION>.pdf \
           commission-faq/text/FAQs-on-the-CRA-v<VERSION>.txt

   - `check_pins.py` exit 1: OSV lists an advisory against the pinned version. Carry on (the PDF is the Commission's own), and add a **Watch** line naming the advisory and saying the pypdf pin needs a reviewed update (`DEPENDENCIES.md`). Exit 2 (OSV did not answer): carry on, one line in the report. Exit 3: `requirements.txt` breaks the pin rule; stop and report.
   - If the install fails, above all on a hash mismatch, stop and report the exact message. Never fall back to an unpinned install, never edit `requirements.txt`, never install another package: each of those is a reviewed change (`CLAUDE.md`, "Dependencies").

3. Diff against the previous version:

       python3 commission-faq/tools/diff_versions.py \
           commission-faq/text/FAQs-on-the-CRA-v<PREV>.txt \
           commission-faq/text/FAQs-on-the-CRA-v<VERSION>.txt

   If both versions have a Markdown rendering, diff those instead — they have no PDF-extraction artefacts.

4. Render the visual side-by-side comparison. This is committed to the repo and served from GitHub Pages; it needs no external service, API key or network access:

       python3 commission-faq/tools/render_diff.py \
           commission-faq/text/FAQs-on-the-CRA-v<PREV>.txt \
           commission-faq/text/FAQs-on-the-CRA-v<VERSION>.txt \
           commission-faq/diff/v<PREV>-v<VERSION>.html \
           --old-label "v<PREV> (<PREV DATE>)" --new-label "v<VERSION> (<DATE>)"

   It regenerates `commission-faq/diff/index.html` itself, so commit that too.

5. Read the text diff carefully and separate SUBSTANTIVE changes from consequential ones. Consequential and not worth a change-log paragraph: the version table gaining a row, table-of-contents entries, page-number shifts, residual extraction artefacts. Substantive: any added, deleted, reworded or renumbered FAQ entry; any change to a date, deadline, obligation, scope or legal reference.

   Do NOT trust the Commission's own one-line "Changes" note in the version table — verify it against the diff. Past releases understated their changes: the v1.2 note said "minor correction of 6.2" but that release removed the NANDO number of the notified body from the module B+C CE marking step.

6. Update `commission-cra-faq-baseline.md`: add a `### v<PREV> → v<VERSION>` section at the top of the change log with the substantive changes, quoting new or changed FAQ text verbatim; refresh the "Current state" table, the version history table, the "Visual comparisons" table (new row with the change counts render_diff.py reported), and `current_version` / `last_change` / `last_check` in the frontmatter.

7. Update `commission-faq/versions/manifest.json`: new version entry with date, stated change, sha256 and byte size of each archived file, raw URL, and the newsroom document ids; and a new entry under `comparisons.pages`.

## 3. Draftable

Skip this. Draftable and Diffchecker are both denied by this environment's network egress policy, and no Draftable API plan is available — see the "Commercial comparison services" section of `commission-faq/README.md`. The visual comparison in step 2b.4 replaces it entirely. Do not try to reach either service.

## 4. Factpage

Fetch https://digital-strategy.ec.europa.eu/en/factpages/cyber-resilience-act-implementation and compare against the "Factpage baseline" section of `commission-cra-faq-baseline.md` — the milestone table and the stated last-update date. If a milestone was added, removed, or had its date changed, update that section and note it in the change log. Ignore pure wording tweaks.

## 5. Commit, PR, merge

Only if something actually changed, or if section 1a recorded a blocked attempt. Commit with a message naming what changed. Push with `git push -u origin HEAD`, retrying up to 4 times with exponential backoff (2s, 4s, 8s, 16s) on network errors only.

If the push fails for lack of credentials (403), do NOT try to route around it — no workarounds, no alternate remotes, no GitHub MCP fallback. Leave the commit on the local branch and report that the push failed, with the exact error AND the branch name you pushed to, so a mismatch with the Routine's configured repository outcome can be spotted. That means this Routine is missing its repository outcome configuration and a human needs to attach it.

Before merging, run `python3 tools/scope_guard.py commission-cra-faq-baseline.md commission-faq/`. If it exits 1 your change touches something outside this routine's scope: leave the PR open and say so.

Otherwise open a pull request as a draft, then mark it ready for review and merge it yourself immediately. This is the standing convention for this routine, recorded in CLAUDE.md — do not leave the PR waiting for approval. It applies only to PRs that touch `commission-cra-faq-baseline.md` and `commission-faq/` alone; if for any reason your change touches anything else, leave that PR open and say so.

## 6. Report

If a new version was found: what version, its date, the substantive changes in a few sentences, and the URL of the rendered comparison page — enough to judge whether it matters without opening the PR. Flag anything touching reporting obligations, deadlines, or the Single Reporting Platform, since that is this repository's subject.

If nothing changed: one line confirming the check ran.

If a check was blocked: which ones with their status codes, which ones ran, and whether
this is the second blocked run in a row.

Either way end with one line:
CRA FAQ: v<VERSION> (<changed/unchanged>) | factpage: <changed/unchanged> | diff page: <rendered/none> | push: <OK/FAIL/nothing to push>
