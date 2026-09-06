# Commission CRA FAQ monitor

Change detection for the European Commission's *FAQs on the Cyber Resilience
Act*, the counterpart to the ENISA SRP FAQ monitor that maintains
`enisa-srp-faq-baseline.md`.

Overview page: [`commission-cra-faq-baseline.md`](../commission-cra-faq-baseline.md)

## Layout

```
commission-faq/
  versions/           each released version, verbatim (PDF, and Markdown where published)
    manifest.json     version metadata: dates, sha256, raw URLs, Draftable comparison ids
  text/               canonical plain text per version, for diffing
  diff/               rendered side-by-side comparisons (HTML) + index
  tools/
    extract_text.py   PDF -> canonical text
    diff_versions.py  substantive diff between two versions
    render_diff.py    side-by-side HTML comparison + index
    draftable_compare.py  Draftable API client (unused; see below)
```

## Why an archive rather than an inlined baseline

The ENISA baseline inlines the FAQ text because it is a web page of ~23 short
answers. The Commission FAQ is a 66-page PDF, so the archive holds each
version verbatim and the overview page carries the deltas. This also means a
diff is a real diff between two files rather than a recollection, and any
version pair can be re-compared later.

## Detecting a new version

The document carries its own version table on page 1:

| FAQ Version | Date | Changes |
|---|---|---|
| 1.4 | 04/09/2026 | Addition of FAQ 5.5 |

That table is the authoritative signal. The landing page's "Last update" date
also moves for edits that do not change the document, so it is a hint, not a
trigger. The download URLs are stable newsroom document ids
(`https://ec.europa.eu/newsroom/dae/redirection/document/<id>`) and the
`Content-Disposition` filename carries the version, e.g.
`FAQs_on_the_CRA__v14_…_122331.pdf` — cheap to check with a HEAD request.

## Producing a diff

```bash
# One-off: pypdf is only needed for PDF extraction, and the system Python in
# some environments ships a broken `cryptography` that pypdf imports.
python3 -m venv .venv && .venv/bin/pip install pypdf

.venv/bin/python commission-faq/tools/extract_text.py \
    commission-faq/versions/FAQs-on-the-CRA-v1.5.pdf \
    commission-faq/text/FAQs-on-the-CRA-v1.5.txt

python3 commission-faq/tools/diff_versions.py \
    commission-faq/text/FAQs-on-the-CRA-v1.4.txt \
    commission-faq/text/FAQs-on-the-CRA-v1.5.txt
```

`diff_versions.py` exits 1 when there are substantive differences and 0 when
there are none. It matches sentences with all whitespace removed, because PDF
text extraction inserts spurious spaces inside words ("expres sed") and those
artefacts differ between two renderings of an unchanged sentence — a plain
`diff` reports dozens of changes that are not changes. Where the Commission
publishes the Markdown rendering, diff that instead: it has no such artefacts.

## Visual comparison

A text diff finds *what* changed. A rendered side-by-side view shows *how*, which
is what you want when reviewing a 66-page legal document.

`render_diff.py` produces that as a self-contained HTML page — no external CSS,
JS, fonts or network calls — committed to the repository and served from GitHub
Pages at
<https://git-z0man.github.io/single-reporting-platform/commission-faq/diff/>

```bash
python3 commission-faq/tools/render_diff.py \
    commission-faq/text/FAQs-on-the-CRA-v1.4.txt \
    commission-faq/text/FAQs-on-the-CRA-v1.5.txt \
    commission-faq/diff/v1.4-v1.5.html \
    --old-label "v1.4 (04/09/2026)" --new-label "v1.5 (<date>)"
```

It uses the same whitespace-insensitive matching as `diff_versions.py`, adds
word-level highlighting inside modified sentences, and shows changed passages
with surrounding context (`--full` for the whole document, `--context N` to
widen). After each render it regenerates `diff/index.html` by globbing the
directory, so the index cannot go stale.

The pages are theme-aware (light and dark) and collapse to a single column on
narrow screens.

## Commercial comparison services

Draftable and Diffchecker were both evaluated and neither is usable here.

This environment's network egress policy is a strict allowlist. It denies
`api.draftable.com`, `draftable.com`, `help.draftable.com`,
`api.diffchecker.com` and `diffchecker.com`:

```
$ curl https://api.draftable.com/v1/comparisons
curl: (56) CONNECT tunnel failed, response 403
```

This was confirmed from a freshly started container, so it is the policy
itself, not a stale one cached by a long-running session. Draftable also
requires a paid API plan, which is not available.

`draftable_compare.py` is kept anyway — it is a complete client, so nothing
needs rewriting if the situation changes. It is not on the routine's normal
path; the routine skips it unless `DRAFTABLE_ACCOUNT_ID` and
`DRAFTABLE_AUTH_TOKEN` are set *and* the host answers.

### The Draftable API, for reference

Base URL `https://api.draftable.com/v1`. One header authenticates everything:
`Authorization: Token <auth_token>`. The account id is never sent in a header;
it appears only in viewer URLs.

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/comparisons` | list; results under `"results"` |
| `GET` | `/comparisons/{id}` | fetch one |
| `POST` | `/comparisons` | create (multipart/form-data) |
| `DELETE` | `/comparisons/{id}` | delete |
| `GET` | `/comparisons/{id}/change-details` | the change list as JSON |
| `POST` | `/exports` | render a comparison to a PDF |
| `GET` | `/exports/{id}` | poll an export |

A comparison has two sides, `left` and `right`, each given as flattened form
fields — `left.file_type` plus either `left.file` (upload) or `left.source_url`
(the API downloads it itself), and an optional `left.display_name`. Create also
takes `identifier`, `public`, and `expiry_time`.

Accepted file types: `pdf`, `docx`, `docm`, `doc`, `rtf`, `pptx`, `pptm`,
`ppt`, `txt`. Export kinds: `single_page`, `combined`, `left`, `right`.

Creation returns immediately with `ready: false`; poll `GET /comparisons/{id}`
until `ready` or `failed` (then read `error_message`).

Viewer URLs come in two forms: **public** —
`/comparisons/viewer/{account_id}/{identifier}`, requires `public: true`, never
expires; and **signed** — the same path plus `?valid_until=<unix>&signature=<hex>`,
where the signature is `HMAC-SHA256(auth_token, policy)` over the compact JSON
`{"account_id":"…","identifier":"…","valid_until":<int>}` with the keys in
exactly that order, defaulting to 30 minutes. Append `?wait` to have the viewer
hold until the comparison is ready.

Since this repository is public, archived versions could be handed to the API as
`source_url` sides with no upload — the raw URLs in `manifest.json` resolve
publicly. Left is the older version, right the newer.

## Provenance

The FAQ is © European Union, 2025, reusable under CC BY 4.0 per Commission
Decision 2011/833/EU. Archived copies here are unmodified. The document is
prepared by Commission services and is not an official position of the
European Commission.
