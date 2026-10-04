#!/usr/bin/env python3
"""Fail if a change touches anything outside the paths a Routine may auto-merge.

    python3 tools/scope_guard.py index.html guide-sync/

Each argument is an exact file or, with a trailing "/", a directory prefix. The
changed files are those that differ between BASE (default origin/main) and the
working tree, plus untracked files, so it works before and after committing.

CLAUDE.md lists each Routine's auto-merge scope in prose. This turns the prose
into a check a Routine can run before it merges its own pull request.

Exit: 0 inside scope (or nothing changed), 1 outside scope, 2 error.
"""
import argparse
import subprocess
import sys


def git(*args, root="."):
    r = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr.strip() or f"git {' '.join(args)} failed")
    return r.stdout


def changed_files(base, root="."):
    names = set(git("diff", "--name-only", base, root=root).split("\n"))
    names |= set(git("ls-files", "--others", "--exclude-standard", root=root).split("\n"))
    return sorted(n for n in names if n)


def allowed(path, scope):
    return any(path == s or (s.endswith("/") and path.startswith(s)) for s in scope)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("scope", nargs="+", help="allowed file, or directory ending in /")
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--root", default=".")
    a = ap.parse_args(argv)
    try:
        files = changed_files(a.base, a.root)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if not files:
        print("nothing changed")
        return 0
    outside = [f for f in files if not allowed(f, a.scope)]
    if outside:
        print("OUTSIDE SCOPE (" + ", ".join(a.scope) + "):")
        for f in outside:
            print("  " + f)
        return 1
    print(f"in scope: {len(files)} file(s), all within {', '.join(a.scope)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
