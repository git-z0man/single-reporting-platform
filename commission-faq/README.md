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
  tools/
    extract_text.py   PDF -> canonical text
    diff_versions.py  substantive diff between two versions
    draftable_compare.py  Draftable Compare API client (visual diff)
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

## Draftable — visual comparison

A text diff finds *what* changed. Draftable renders *how* the document
changed, side by side, which is what you want when reviewing a 66-page legal
document. It is a complement to the text diff, not a replacement, and the
monitor works without it.

### Status in this environment: blocked

`api.draftable.com` is denied by the network egress policy:

```
$ curl https://api.draftable.com/v1/comparisons
curl: (56) CONNECT tunnel failed, response 403
```

To enable it:

1. **Allowlist `api.draftable.com`** in the Claude Code environment's network
   policy (Settings → the environment used by the monitoring routine). Without
   this no routine running in that environment can reach the API.
2. **Set credentials** as environment variables on the routine's environment:
   `DRAFTABLE_ACCOUNT_ID` and `DRAFTABLE_AUTH_TOKEN`, from
   <https://api.draftable.com/account/credentials>. API access requires a paid
   Draftable API plan; the free web comparison tool has no API.
3. Verify with `python3 commission-faq/tools/draftable_compare.py check`.

A self-hosted Draftable instance works too — point `DRAFTABLE_BASE_URL` at it
(`https://<host>/api/v1`) and allowlist that host instead.

### The API

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
(the API downloads it itself, retrying up to 4 times), and an optional
`left.display_name`. Create also takes `identifier` (auto-generated if
omitted), `public`, and `expiry_time`.

Accepted file types: `pdf`, `docx`, `docm`, `doc`, `rtf`, `pptx`, `pptm`,
`ppt`, `txt`. Export kinds: `single_page`, `combined`, `left`, `right`.

Creation returns immediately with `ready: false`; poll `GET /comparisons/{id}`
until `ready` or `failed` (then read `error_message`).

Viewer URLs come in two forms:

- **public** — `/comparisons/viewer/{account_id}/{identifier}`, requires
  `public: true` at creation, never expires, anyone with the link can view.
- **signed** — the same path plus `?valid_until=<unix>&signature=<hex>`, where
  the signature is `HMAC-SHA256(auth_token, policy)` over the compact JSON
  `{"account_id":"…","identifier":"…","valid_until":<int>}` with the keys in
  exactly that order. Defaults to 30 minutes.

Append `?wait` (or `&wait`) to have the viewer hold until the comparison is
ready instead of erroring.

### Why this repository suits the URL-side form

The repository is public, so an archived version is already at a public URL
and Draftable can fetch both sides itself — no upload:

```bash
export DRAFTABLE_ACCOUNT_ID=... DRAFTABLE_AUTH_TOKEN=...
BASE=https://raw.githubusercontent.com/git-z0man/single-reporting-platform/main/commission-faq/versions

python3 commission-faq/tools/draftable_compare.py compare \
    "$BASE/FAQs-on-the-CRA-v1.3.pdf" \
    "$BASE/FAQs-on-the-CRA-v1.4.pdf" \
    --identifier cra-faq-v1.3-v1.4 \
    --left-name "FAQ v1.3 (01/07/2026)" \
    --right-name "FAQ v1.4 (04/09/2026)" \
    --public
```

This prints a permanent viewer URL, which goes into the comparison table in
the overview page. `--public` is deliberate: the link is recorded in a public
file, and both documents are public Commission documents under CC BY 4.0. Drop
it and the tool prints a signed URL that expires in 30 minutes instead.

Note the ordering convention: **left is the older version, right is the newer**
one. Draftable presents left as the original and right as the revision.

The comparisons are created once per version pair and kept (no
`--expires-days`), so the links in the overview page stay valid.

## Provenance

The FAQ is © European Union, 2025, reusable under CC BY 4.0 per Commission
Decision 2011/833/EU. Archived copies here are unmodified. The document is
prepared by Commission services and is not an official position of the
European Commission.
