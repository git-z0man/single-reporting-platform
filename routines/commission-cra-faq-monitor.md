# Commission CRA FAQ monitor

- **Trigger**: `trig_012AzfKXKrPnRCEjXXYWBgY4`
- **Schedule**: `0 5 * * 1`
- **Writes**: `commission-cra-faq-baseline.md`, `commission-faq/`
- **Updatable by an agent**: **yes** — created via `meta_mcp`, so `update_trigger` works.

> Mirror of the live prompt. Editing this file changes nothing on its own;
> apply it with `update_trigger` in the same change.

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

The authoritative signal is the FAQ document's own version table on page 1, NOT the landing page's "Last update" date (that also moves for edits which do not change the document).

Cheapest check: the newsroom download URL's Content-Disposition filename carries the version.

    curl -sSLI https://ec.europa.eu/newsroom/dae/redirection/document/122331 | grep -i content-disposition

As of the v1.4 baseline that returns `FAQs_on_the_CRA__v14_..._122331.pdf`.

Also fetch the landing page, because a new version usually gets a NEW document id:
https://digital-strategy.ec.europa.eu/en/library/cyber-resilience-act-implementation-frequently-asked-questions
Extract every download link (PDF and Markdown) and their document ids. Prefer whatever the landing page currently points at over the ids recorded in the manifest.

Compare against `current_version` in `commission-faq/versions/manifest.json`.

## 2a. If there is NO new version

Read `last_check` from `commission-faq/versions/manifest.json` as it stands on `origin/main`:

    git show origin/main:commission-faq/versions/manifest.json | python3 -c "import json,sys; print(json.load(sys.stdin)['last_check'])"

- If it is already today's date → nothing to record. Do NOT commit, do NOT open an empty PR. End the run and report one line that the check ran.
- Otherwise → update `last_check` in that manifest and in the frontmatter of `commission-cra-faq-baseline.md` to today's date, leave `last_change` alone, then commit, PR and merge per section 5.

Still check the factpage — see section 4.

## 2b. If there IS a new version

1. Download the new PDF and, if published, the Markdown, into `commission-faq/versions/` as `FAQs-on-the-CRA-v<VERSION>.pdf` / `.md`.

2. Produce the canonical text. pypdf is needed and the system Python may ship a broken `cryptography` that pypdf imports, so use a throwaway venv:

       python3 -m venv /tmp/venv && /tmp/venv/bin/pip install pypdf
       /tmp/venv/bin/python commission-faq/tools/extract_text.py \
           commission-faq/versions/FAQs-on-the-CRA-v<VERSION>.pdf \
           commission-faq/text/FAQs-on-the-CRA-v<VERSION>.txt

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

Only if something actually changed. Commit with a message naming what changed. Push with `git push -u origin HEAD`, retrying up to 4 times with exponential backoff (2s, 4s, 8s, 16s) on network errors only.

If the push fails for lack of credentials (403), do NOT try to route around it — no workarounds, no alternate remotes, no GitHub MCP fallback. Leave the commit on the local branch and report that the push failed, with the exact error AND the branch name you pushed to, so a mismatch with the Routine's configured repository outcome can be spotted. That means this Routine is missing its repository outcome configuration and a human needs to attach it.

Otherwise open a pull request as a draft, then mark it ready for review and merge it yourself immediately. This is the standing convention for this routine, recorded in CLAUDE.md — do not leave the PR waiting for approval. It applies only to PRs that touch `commission-cra-faq-baseline.md` and `commission-faq/` alone; if for any reason your change touches anything else, leave that PR open and say so.

## 6. Report

If a new version was found: what version, its date, the substantive changes in a few sentences, and the URL of the rendered comparison page — enough to judge whether it matters without opening the PR. Flag anything touching reporting obligations, deadlines, or the Single Reporting Platform, since that is this repository's subject.

If nothing changed: one line confirming the check ran.

Either way end with one line:
CRA FAQ: v<VERSION> (<changed/unchanged>) | factpage: <changed/unchanged> | diff page: <rendered/none> | push: <OK/FAIL/nothing to push>
