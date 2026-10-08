# Guide tooling

Stdlib-only Python (no packages to install). These scripts keep `index.html`, the
unofficial guide, in line with ENISA's FAQ and Glossary. They are what the
**Guide sync** Routine runs (`routines/guide-sync.md`); every one can be run by
hand.

Run the tests first, from the repository root:

    python3 -m unittest discover -s tools/tests -t .

## Observe, then render

The design separates looking at ENISA from editing the guide.

| Script | Touches network | Does |
|---|---|---|
| `fetch_enisa.py` | **yes** (curl, retried) | Parses ENISA's live FAQ and Glossary into `guide-sync/faq.json` and `guide-sync/glossary.json`. URLs come from the baselines' frontmatter. A question or field whose *words* are unchanged keeps its stored entry, so markup churn on ENISA's side makes no diff. Exit 0 unchanged, 1 written, **2 failed (HTTP 429/5xx or an unparseable page is a failed check, never a content change; nothing is written)**. |
| `check_guide.py` | no (`--online` hashes the manual PDF) | Read-only. Compares the guide with the extracts: FAQ questions and answer bodies, Glossary version and fields, stage chips, link targets, truncated links, `#f-...` anchors resolving to the right card, `data-sync` markers, tag balance. Exit 0 clean, 1 drift, 2 the check itself broke. |
| `sync_guide.py` | no | Edits `index.html` from the extracts. A pure function of repository files, which is what makes the next script possible. `--dry-run`, `--json`, `--include-judgment`. Exit 0 nothing to do, 1 edited, 3 only judgment items wait, 2 error. |
| `verify_mechanical.py BASE` | no | The auto-merge gate. Recomputes `sync(BASE index.html, working-tree extracts)` and requires **byte equality** with the working-tree `index.html`. A hand edit by a person or a model makes them differ. Exit 0 eligible. |
| `scope_guard.py PATH...` | no | Fails if the diff against `origin/main` touches anything outside the allowed files or directories (a directory ends in `/`). Used by every Routine before it merges. |
| `check_pins.py` | **yes** (OSV API; `--offline` skips it) | Checks `requirements.txt`: every requirement pinned with `==` and hashed, and no OSV advisory against the pinned version. Run by the Commission monitor before it installs pypdf. Exit 0 clean, 1 advisory, 2 check failed, 3 a requirement is unpinned or unhashed. See `DEPENDENCIES.md`. |

The baselines (`enisa-srp-*-baseline.md`) are annotated narrative: ENISA's text
interleaved with change-log prose, unlinked e-mail addresses, nested
parentheses. They are not a source for guide text. They supply URLs and serve as
an advisory cross-check; the text comes from `guide-sync/`.

## What counts as mechanical

Auto-merge is allowed only when **every** edit is one of these:

- a count, version or date in a `data-sync` span (`faq-count`, `faq-asof`,
  `glossary-count`, `glossary-version`, `glossary-asof`, `footer-asof`);
- a link repointed because ENISA moved the page;
- a new FAQ question, appended verbatim;
- a typo-class word change: same length, words of five or more letters, at most
  two letters different;
- a new Glossary card, only if every stage is Optional or n/a.

**Judgment**, never merged unattended: a rewritten FAQ answer, a changed link
target, a changed stage, a new Required or If-available field (the phase tables
and the walkthrough must change too), a removed question or field. These are
reported with the question already framed, and left for a person.

Also: a diff over 60 lines is never mechanical, and the guide's own text is never
touched: `guide-note` paragraphs, `OWN-NOTE` placeholders, the amendment notes,
the `max N characters` suffixes.

## The gate, in full

The Guide sync merges its own pull request only when all hold: the sync report is
eligible; `verify_mechanical.py origin/main` exits 0; `scope_guard.py index.html
guide-sync/` exits 0; `check_guide.py` exits 0; and `tools/guide-sync.paused` does
**not** exist on `origin/main`.

## The kill switch

While `tools/guide-sync.paused` exists on `main`, the Guide sync opens draft pull
requests only. It ships present, so the first runs can be inspected. Delete the
file to arm auto-merge; restore it to stop merging, with no change to the
Routine.

## Limits worth knowing

- Scope is enforced by the Routine following its prompt and calling
  `scope_guard.py`, as with every monitor; nothing at the platform level stops a
  Routine writing elsewhere.
- Merging to `main` very likely publishes the guide (`.nojekyll` suggests GitHub
  Pages); that could not be confirmed from this environment.
- `check_guide.py` does not follow the EUR-Lex links; they cannot be verified
  from here.
