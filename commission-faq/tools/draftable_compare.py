#!/usr/bin/env python3
"""Minimal Draftable Compare API client for the CRA FAQ version monitor.

Standard library only, so a monitoring run needs no pip install.  Written
against the REST surface used by Draftable's own client libraries
(https://github.com/draftable/compare-api-python-client).

API surface (cloud base URL https://api.draftable.com/v1):

    GET    /comparisons                     list, results under "results"
    GET    /comparisons/{id}                fetch one
    POST   /comparisons                     create (multipart/form-data)
    DELETE /comparisons/{id}                delete
    GET    /comparisons/{id}/change-details change list as JSON
    POST   /exports                          render a comparison to PDF
    GET    /exports/{id}                     poll an export

Authentication is a single header: `Authorization: Token <auth_token>`.
The account id is not sent in the header; it only appears in viewer URLs.

A comparison side is either an uploaded file (`left.file`) or a URL the API
downloads itself (`left.source_url`).  This repository is public, so the
archived PDFs under commission-faq/versions/ can be handed to Draftable as
source URLs -- no upload needed.

Viewer URLs:
    public  /comparisons/viewer/{account_id}/{identifier}
    signed  ... ?valid_until=<unix>&signature=<hex hmac>
            signature = HMAC-SHA256(auth_token,
                '{"account_id":"..","identifier":"..","valid_until":<int>}')

Credentials come from the environment:
    DRAFTABLE_ACCOUNT_ID, DRAFTABLE_AUTH_TOKEN
    DRAFTABLE_BASE_URL  (optional; set this for a self-hosted instance)

Subcommands:
    check                       verify reachability and credentials
    compare <left> <right>      create a comparison, print the viewer URL
    get <identifier>            fetch one comparison as JSON
    changes <identifier>        fetch the change details as JSON
    list                        list comparisons
    delete <identifier>         delete a comparison
    export <identifier>         render the comparison to a PDF URL

<left> and <right> are https URLs or local file paths.
"""

import argparse
import hashlib
import hmac
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone

DEFAULT_BASE_URL = "https://api.draftable.com/v1"

# Accepted by the API; anything else is rejected before the request is sent.
FILE_TYPES = {"pdf", "docx", "docm", "doc", "rtf", "pptx", "pptm", "ppt", "txt"}
EXPORT_KINDS = ("single_page", "combined", "left", "right")


class DraftableError(RuntimeError):
    pass


def credentials():
    account_id = os.environ.get("DRAFTABLE_ACCOUNT_ID", "").strip()
    auth_token = os.environ.get("DRAFTABLE_AUTH_TOKEN", "").strip()
    if not account_id or not auth_token:
        raise DraftableError(
            "DRAFTABLE_ACCOUNT_ID and DRAFTABLE_AUTH_TOKEN must be set "
            "(cloud credentials: https://api.draftable.com/account/credentials)"
        )
    return account_id, auth_token


def base_url():
    return os.environ.get("DRAFTABLE_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def _encode_multipart(fields, files):
    """Build a multipart/form-data body.

    `fields` maps name -> str, `files` maps name -> (filename, bytes).
    The API expects nested side data flattened as "left.file_type" etc.
    """
    boundary = f"----draftable{uuid.uuid4().hex}"
    body = bytearray()

    for name, value in fields.items():
        if value is None:
            continue
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
        body += f"{value}\r\n".encode()

    for name, (filename, payload) in files.items():
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        body += f"--{boundary}\r\n".encode()
        body += (
            f'Content-Disposition: form-data; name="{name}"; '
            f'filename="{filename}"\r\n'.encode()
        )
        body += f"Content-Type: {content_type}\r\n\r\n".encode()
        body += payload
        body += b"\r\n"

    body += f"--{boundary}--\r\n".encode()
    return bytes(body), f"multipart/form-data; boundary={boundary}"


def request(method, path, fields=None, files=None, timeout=120):
    """Send one authenticated request and return the decoded JSON body."""
    _, auth_token = credentials()
    url = f"{base_url()}{path}"

    data = None
    headers = {
        "Authorization": f"Token {auth_token}",
        "Accept": "application/json",
        "User-Agent": "cra-faq-monitor/1.0",
    }

    if fields is not None or files is not None:
        data, content_type = _encode_multipart(fields or {}, files or {})
        headers["Content-Type"] = content_type

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:1000]
        raise DraftableError(f"{method} {url} -> HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        # The common case here is the egress proxy refusing api.draftable.com.
        raise DraftableError(f"{method} {url} unreachable: {exc.reason}") from exc

    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


def side(name, location, display_name=None):
    """Build the form fields (and file payload) for one comparison side."""
    fields, files = {}, {}

    if location.startswith(("http://", "https://")):
        file_type = location.rsplit(".", 1)[-1].lower().split("?")[0]
        if file_type not in FILE_TYPES:
            raise DraftableError(
                f"cannot infer a supported file type from {location!r}; "
                f"expected one of {sorted(FILE_TYPES)}"
            )
        fields[f"{name}.source_url"] = location
        fields[f"{name}.file_type"] = file_type
        default_name = location.rsplit("/", 1)[-1]
    else:
        file_type = location.rsplit(".", 1)[-1].lower()
        if file_type not in FILE_TYPES:
            raise DraftableError(f"unsupported file type {file_type!r}")
        with open(location, "rb") as handle:
            files[f"{name}.file"] = (os.path.basename(location), handle.read())
        fields[f"{name}.file_type"] = file_type
        default_name = os.path.basename(location)

    fields[f"{name}.display_name"] = display_name or default_name
    return fields, files


def public_viewer_url(account_id, identifier, wait=True):
    url = f"{base_url()}/comparisons/viewer/{account_id}/{identifier}"
    return url + "?wait" if wait else url


def signed_viewer_url(account_id, auth_token, identifier, valid_for=timedelta(minutes=30)):
    valid_until = int(
        (datetime.now(timezone.utc) + valid_for).timestamp()
    )
    # Field order matters: the API recomputes the HMAC over exactly this JSON.
    policy = json.dumps(
        {
            "account_id": str(account_id),
            "identifier": str(identifier),
            "valid_until": valid_until,
        },
        separators=(",", ":"),
    )
    signature = hmac.new(
        auth_token.encode("utf-8"), policy.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    return (
        f"{base_url()}/comparisons/viewer/{account_id}/{identifier}"
        f"?valid_until={valid_until}&signature={signature}"
    )


def wait_until_ready(identifier, timeout=600, interval=5):
    """Poll a comparison until the API reports it ready or failed."""
    deadline = time.monotonic() + timeout
    while True:
        comparison = request("GET", f"/comparisons/{identifier}")
        if comparison.get("failed"):
            raise DraftableError(
                f"comparison {identifier} failed: "
                f"{comparison.get('error_message', 'no error message')}"
            )
        if comparison.get("ready"):
            return comparison
        if time.monotonic() > deadline:
            raise DraftableError(f"comparison {identifier} not ready after {timeout}s")
        time.sleep(interval)


def cmd_check(args):
    account_id, _ = credentials()
    result = request("GET", "/comparisons")
    count = len(result.get("results", []))
    print(f"OK: reachable at {base_url()}, account {account_id}, {count} comparison(s)")
    return 0


def cmd_compare(args):
    account_id, auth_token = credentials()

    left_fields, left_files = side("left", args.left, args.left_name)
    right_fields, right_files = side("right", args.right, args.right_name)

    fields = {**left_fields, **right_fields, "public": "true" if args.public else "false"}
    if args.identifier:
        fields["identifier"] = args.identifier
    if args.expires_days:
        expiry = datetime.now(timezone.utc) + timedelta(days=args.expires_days)
        fields["expiry_time"] = expiry.isoformat()

    comparison = request(
        "POST", "/comparisons", fields=fields, files={**left_files, **right_files}
    )
    identifier = comparison["identifier"]
    print(f"created comparison {identifier}", file=sys.stderr)

    if args.wait:
        wait_until_ready(identifier)

    if args.public:
        print(public_viewer_url(account_id, identifier))
    else:
        print(signed_viewer_url(account_id, auth_token, identifier))
    return 0


def cmd_get(args):
    print(json.dumps(request("GET", f"/comparisons/{args.identifier}"), indent=2))
    return 0


def cmd_changes(args):
    print(
        json.dumps(
            request("GET", f"/comparisons/{args.identifier}/change-details"), indent=2
        )
    )
    return 0


def cmd_list(args):
    result = request("GET", "/comparisons")
    for comparison in result.get("results", []):
        print(
            f"{comparison['identifier']}\t"
            f"ready={comparison.get('ready')}\t"
            f"{comparison.get('creation_time', '')}"
        )
    return 0


def cmd_delete(args):
    request("DELETE", f"/comparisons/{args.identifier}")
    print(f"deleted {args.identifier}")
    return 0


def cmd_export(args):
    export = request(
        "POST",
        "/exports",
        fields={
            "comparison": args.identifier,
            "kind": args.kind,
            "include_cover_page": "true" if args.cover_page else "false",
        },
    )
    identifier = export["identifier"]
    deadline = time.monotonic() + 600
    while not export.get("ready"):
        if export.get("failed"):
            raise DraftableError(f"export {identifier} failed: {export.get('error_message')}")
        if time.monotonic() > deadline:
            raise DraftableError(f"export {identifier} not ready after 600s")
        time.sleep(5)
        export = request("GET", f"/exports/{identifier}")
    print(export.get("url", json.dumps(export)))
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="verify reachability and credentials").set_defaults(
        func=cmd_check
    )

    compare = sub.add_parser("compare", help="create a comparison")
    compare.add_argument("left", help="URL or path of the older version")
    compare.add_argument("right", help="URL or path of the newer version")
    compare.add_argument("--identifier", help="stable id, e.g. cra-faq-v1.3-v1.4")
    compare.add_argument("--left-name", help="display name for the left side")
    compare.add_argument("--right-name", help="display name for the right side")
    compare.add_argument(
        "--public",
        action="store_true",
        help="anyone with the link can view; required for a durable link in the overview page",
    )
    compare.add_argument(
        "--expires-days", type=int, help="delete automatically after N days"
    )
    compare.add_argument(
        "--no-wait", dest="wait", action="store_false", help="do not poll until ready"
    )
    compare.set_defaults(func=cmd_compare, wait=True)

    get = sub.add_parser("get", help="fetch one comparison")
    get.add_argument("identifier")
    get.set_defaults(func=cmd_get)

    changes = sub.add_parser("changes", help="fetch change details as JSON")
    changes.add_argument("identifier")
    changes.set_defaults(func=cmd_changes)

    sub.add_parser("list", help="list comparisons").set_defaults(func=cmd_list)

    delete = sub.add_parser("delete", help="delete a comparison")
    delete.add_argument("identifier")
    delete.set_defaults(func=cmd_delete)

    export = sub.add_parser("export", help="render a comparison to PDF")
    export.add_argument("identifier")
    export.add_argument("--kind", choices=EXPORT_KINDS, default="single_page")
    export.add_argument("--cover-page", action="store_true")
    export.set_defaults(func=cmd_export)

    return parser


def main():
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except DraftableError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
