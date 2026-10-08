#!/usr/bin/env python3
"""Check the pinned third-party packages in requirements.txt: pinned and hashed, and no
known advisory against the pinned version.

    python3 tools/check_pins.py [--json] [--offline]

Every requirement must be `name==version` with at least one `--hash=sha256:...`. For each
pin it asks OSV (api.osv.dev, the advisory database pip-audit also reads) which advisories
affect that exact version. This is the "monitor" step of ENISA's secure-package-consumption
skill (.claude/skills/secure-package-consumption/), run by the Commission CRA FAQ monitor
before it installs pypdf; DEPENDENCIES.md has the background.

Exit: 0 pinned, hashed, no known advisory; 1 an advisory affects a pinned version;
2 the check failed (no answer from OSV, an unparseable file); 3 a requirement is not
pinned or not hashed. On 1 and 3 the pin needs a reviewed change; this script never
edits requirements.txt.
"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OSV = "https://api.osv.dev/v1/query"


class CheckError(Exception):
    pass


def parse(text):
    """[{"name", "version", "hashes", "line"}] from a requirements file; joins continued lines."""
    out = []
    for line in re.sub(r"\\\n", " ", text).split("\n"):
        line = re.sub(r"(^|\s)#.*$", "", line).strip()
        if not line:
            continue
        m = re.match(r"([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:==\s*([^\s;]+))?", line)
        if not m:          # options such as --index-url or -r are not allowed here either
            raise CheckError(f"cannot read requirement {line!r}")
        out.append({"name": m.group(1), "version": m.group(2) or "",
                    "hashes": re.findall(r"--hash=sha256:([0-9a-f]{64})", line), "line": line})
    return out


def policy(reqs):
    """Requirements that break the rule: unpinned (no ==) or without a sha256 hash."""
    return [r["line"] for r in reqs if not r["version"] or not r["hashes"]]


def osv(name, version):
    body = json.dumps({"package": {"name": name, "ecosystem": "PyPI"}, "version": version})
    r = subprocess.run(["curl", "-sS", "--retry", "3", "--retry-all-errors", "-m", "60", "-X", "POST",
                        "-H", "content-type: application/json", "-d", body, OSV], capture_output=True, text=True)
    if r.returncode:
        raise CheckError(f"OSV: {r.stderr.strip()[:200]}")
    try:
        d = json.loads(r.stdout)
    except ValueError:
        raise CheckError(f"OSV answer is not JSON: {r.stdout[:120]!r}")
    if not isinstance(d, dict):
        raise CheckError("OSV answer is not an object")
    return [{"id": v.get("id", ""), "summary": v.get("summary", ""), "aliases": v.get("aliases", [])}
            for v in d.get("vulns", [])]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--file", default=os.path.join(ROOT, "requirements.txt"))
    ap.add_argument("--offline", action="store_true", help="check pins and hashes only, no OSV query")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        with open(a.file, encoding="utf-8") as fh:
            reqs = parse(fh.read())
        bad = policy(reqs)
        found = {} if a.offline or bad else {f"{r['name']}=={r['version']}": osv(r["name"], r["version"]) for r in reqs}
    except (CheckError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    hits = {k: v for k, v in found.items() if v}
    if a.json:
        print(json.dumps({"pins": [f"{r['name']}=={r['version']}" for r in reqs], "not_pinned_or_hashed": bad,
                          "advisories": hits, "osv_checked": not a.offline and not bad}, indent=1))
    elif bad:
        print("not pinned or not hashed: " + "; ".join(bad))
    elif hits:
        for k, v in hits.items():
            print(f"{k}: " + ", ".join(f"{x['id']} ({x['summary']})" for x in v))
    else:
        print(f"{len(reqs)} pin(s), all hashed" + ("" if a.offline else "; no known advisory in OSV"))
    return 3 if bad else 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
