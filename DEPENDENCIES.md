# Dependencies

What this repository takes from outside, how each piece arrives, and the rule for adding
more. Written on 2026-10-08 by applying ENISA's **secure-package-consumption** skill to the
repository. The skill lives in [`.claude/skills/secure-package-consumption/`](.claude/skills/secure-package-consumption/)
(EUPL-1.2, copied unchanged, provenance in its `PROVENANCE.md`).

**In short.** The scripts use the Python standard library and nothing else, with one
exception: **pypdf**, which extracts the Commission's CRA FAQ PDFs. Until now every run that
needed it installed whatever release PyPI served that day. It is now pinned by version and
wheel hash in [`requirements.txt`](requirements.txt), checked against OSV before use, and a
test fails if anything else installs a package.

## The skill

ENISA published the skill on 2026-09-16 (version 2.0-beta) as an operational form of its
*Technical Advisory for Secure Use of Package Managers*
([DOI 10.2824/6157993](https://doi.org/10.2824/6157993)). It tells an AI agent how to treat
third-party packages: decide first whether a dependency is needed at all, check identity,
vulnerabilities, provenance and install behaviour before installing anything, pin and hash
what is accepted, verify the result, record the evidence, and keep monitoring.

**How it is used here.** Claude Code loads every directory under `.claude/skills/` as a
project skill, in interactive sessions on this repository and in the scheduled Routines,
which work on a clone of it. It applies when a change adds, updates or removes a package,
touches `requirements.txt`, adds an import from outside the standard library, puts an
install command into a script or a Routine prompt, or when `tools/check_pins.py` reports an
advisory. It can also be called by name, `/secure-package-consumption`. Its output is a
short decision note (format in its `SKILL.md`), which belongs in the pull request. The note
for pypdf is below.

The skill is guidance, not enforcement. What enforces the result here is
`tools/tests/test_dependencies.py`, which the EUVD and Guide sync Routines run before their
daily work, `tools/check_pins.py` at the point of use, and the review that
every change to `requirements.txt`, `routines/` and the scripts goes through (`CLAUDE.md`,
"Dependencies").

## Inventory

As of 2026-10-08.

| What | Used by | Comes from | How it arrives | Status |
|---|---|---|---|---|
| Python standard library | every script in `tools/`, `euvd/`, `commission-faq/tools/` | the interpreter | nothing to install | no third-party Python code |
| **pypdf 6.19.0** | `commission-faq/tools/extract_text.py`, run by the Commission CRA FAQ monitor only when a new FAQ version appears | PyPI | `requirements.txt`: exact version and wheel hash, `--require-hashes --only-binary :all:`, throwaway venv | **pinned on 2026-10-08** (was unpinned) |
| Playwright 1.56.1 with Chromium | `euvd/prerender.js`, pre-renders `euvd/stats.html` | the run environment (`/opt/node22/lib/node_modules`, `/opt/pw-browsers`) | never installed by the repository; no `npm install` anywhere | if absent, the page draws its charts in the browser |
| `curl`, `git` | all monitors | the system | | |
| `pdftotext` (poppler) | ENISA monitor, for the AR User Manual PDF | the system, where present; absent in this environment (checked 2026-10-08) | never installed | the monitor records the hash and says the text diff could not be made |
| IBM Plex from Google Fonts | `index.html` | fonts.googleapis.com | the reader's browser | a web resource, not a package: outside the skill's scope; falls back to system fonts |
| `app.js`, `euvd/charts.js` | the pages | this repository | | first-party, no libraries |

## Decision note: pypdf

In the skill's extended format.

```text
Dependency decision: allow with controls
Risk: low
Confidence: high
Evidence status: partial
Package: pypdf 6.19.0 (pip / PyPI, runtime dependency of a monitoring tool)
Intended use: canonical text of the Commission's CRA FAQ PDFs (commission-faq/tools/extract_text.py)
Source: PyPI, the default index; no extra index
Necessity: the standard library cannot extract PDF text, and pdftotext is absent from the
  Routine environment. The dependency already existed, unpinned; kept, with controls.
Evidence and checks:
- Identity: PyPI project "pypdf", source github.com/py-pdf/pypdf, maintainers Martin Thoma
  and stefan6419846; BSD-3-Clause. Not a lookalike: the maintained successor of PyPDF2.
- Provenance: PyPI attestation for pypdf-6.19.0-py3-none-any.whl, trusted publisher GitHub
  py-pdf/pypdf, workflow publish-to-pypi.yaml (pypi.org/integrity, read 2026-10-08).
- Vulnerabilities: OSV lists no advisory for 6.19.0 (2026-10-08). 6.18.1 has three
  (GHSA-php9-fj8v-98fj, GHSA-v247-6f48-mgcj, GHSA-w23x-9jrw-r45c: long runtimes or memory use
  on crafted PDFs), fixed in 6.19.0. pypdf has 101 OSV advisories in all, mostly denial of
  service on malformed PDFs; it parses files downloaded from the Commission's site.
- Install behaviour: pure-Python wheel (py3-none-any): no native code, no build step, no
  install scripts. No dependencies on Python 3.11 (typing_extensions only below 3.11;
  cryptography only with the "crypto" extra, which is not used).
- Release: 2026-09-16; the project releases about weekly.
- Verification: in a throwaway venv the hash-checked wheel extracts the archived v1.0, v1.2,
  v1.3 and v1.4 PDFs byte for byte as stored in commission-faq/text/.
- GitHub dependency review of this change (dependency-graph/compare, 2026-10-08): pypdf
  6.19.0 added from requirements.txt, ecosystem pip, scope runtime, BSD-3-Clause, no
  vulnerabilities in the GitHub Advisory Database.
Checks not performed / capability limits:
- pip-audit and osv-scanner are not installed here (checked); OSV was queried through its API.
- Maintainer and ownership history: not reviewed beyond PyPI metadata.
- Dependabot alert list: not readable from the agent's GitHub access (HTTP 403, "Resource
  not accessible by integration"). The owner switched the alerts on on 2026-10-08; until
  then the API answered "Dependabot alerts are disabled for this repository". Alerts reach
  the owner through GitHub's own notifications, not the Routines.
- SBOM: the repository keeps none; with one dependency, requirements.txt is the record.
Required controls / approval:
- Exact version and wheel hash in requirements.txt; install with --require-hashes
  --only-binary :all: into a throwaway venv; no fallback to an unpinned install.
- tools/check_pins.py (OSV) before each use; an advisory becomes a Watch line and a
  reviewed pin update.
- Dependabot alerts (on since 2026-10-08) watch requirements.txt on main between uses; they
  cover the pin from the merge of this change on, since GitHub reads the default branch.
- requirements.txt sits outside every auto-merge scope; no Routine edits it.
Next action: proceed with controls
```

On a Python older than 3.11 pypdf needs `typing_extensions`, which is not hashed in
`requirements.txt`, so `--require-hashes` refuses the install. That is the intended
failure: the Routine stops and reports, and nobody adds a package unreviewed.

## What changed because of the skill

| Where | Before | Problem | After |
|---|---|---|---|
| `routines/commission-cra-faq-monitor.md`, step 2b.2 (the live prompt, through its loader) | `python3 -m venv /tmp/venv && /tmp/venv/bin/pip install pypdf` | The newest release at run time, without version or hash, ran in a session that can push to this repository. A compromised release, or one that extracts text differently, would have gone unnoticed. | `python3 tools/check_pins.py`, then `pip install --require-hashes --only-binary :all: -r requirements.txt`. On a hash mismatch the run stops; there is no fallback. The prompt's header records the change. |
| `commission-faq/README.md`, "Producing a diff" | `.venv/bin/pip install pypdf` | The same, for a person running it by hand. | The pinned install, and a note on the change. |
| `commission-faq/tools/extract_text.py`, docstring | `.venv/bin/pip install pypdf` | The same. | The pinned install. |
| `requirements.txt` (new) | none | Nothing recorded which version produced the archived texts. | Version and wheel hash, outside every auto-merge scope. |
| `tools/check_pins.py` (new) | none | Nothing watched the dependency for advisories. | Checks that every requirement is pinned and hashed, and asks OSV about the pinned version. Exit 0 clean, 1 advisory, 2 check failed, 3 rule broken. |
| `tools/tests/test_dependencies.py` (new) | none | The rule existed only in prose. | Fails on any install command (`pip`, `npm`, `npx`, `yarn`, `pnpm`, `apt`) in the scripts, prompts and documents other than the hashed one, and on an unpinned or unhashed requirement. |
| `CLAUDE.md`, "Dependencies" (new) | none | No rule told an agent what to do before installing something. | The rule, with the skill as the procedure. |

Checked and left as they were: the standard-library-only scripts, Playwright from the
environment, `pdftotext`, Google Fonts (see the inventory).

## Moving the pin

When `check_pins.py` reports an advisory, or a newer pypdf is wanted:

1. Apply the skill (`/secure-package-consumption`) and write a new decision note.
2. Read the new version's wheel hash from PyPI: `https://pypi.org/pypi/pypdf/<version>/json`,
   the `digests.sha256` of the `py3-none-any.whl` file. Check its provenance at
   `https://pypi.org/integrity/pypdf/<version>/<wheel file name>/provenance`.
3. Update `requirements.txt` and install into a throwaway venv with `--require-hashes
   --only-binary :all:`.
4. Re-extract the archived PDFs in `commission-faq/versions/` and compare with
   `commission-faq/text/`. Identical, or explain every difference in the pull request.
5. Run `python3 tools/check_pins.py` and the tests, and open a pull request with the note. It
   needs review; no Routine merges it.
