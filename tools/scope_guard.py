#!/usr/bin/env python3
"""Fail if a change touches anything outside the paths a Routine may auto-merge.

    python3 tools/scope_guard.py index.html guide-sync/

Each argument is an exact file or, with a trailing "/", a directory prefix. The
changed files are those that differ between BASE (default origin/main) and the
working tree, plus untracked files, so it works before and after committing.

CLAUDE.md lists each Routine's auto-merge scope in prose. This turns the prose
into a check a Routine can run before it merges its own pull request.

A Routine may never auto-merge a change to code, whatever its scope says. Three
scopes contain the scripts their own Routine runs the next morning - euvd/ holds
build_stats.py, charts.js and prerender.js, srp-domains/ holds check.sh,
commission-faq/ holds its tools - so a directory prefix alone would let a run
rewrite what it executes tomorrow and merge that itself. CODE denies those
extensions; a person changes a script through review, which is what CLAUDE.md
already says in prose ("the Routine does not edit them"). --allow-code is for a
person running the guard by hand, never for a Routine.

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


CODE = (".py", ".sh", ".js", ".mjs", ".bash", ".zsh")


def allowed(path, scope, allow_code=False):
    if not allow_code and path.endswith(CODE):
        return False
    return any(path == s or (s.endswith("/") and path.startswith(s)) for s in scope)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("scope", nargs="+", help="allowed file, or directory ending in /")
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--root", default=".")
    ap.add_argument("--allow-code", action="store_true",
                    help="permit scripts to change too; for a person, never for a Routine")
    a = ap.parse_args(argv)
    try:
        files = changed_files(a.base, a.root)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if not files:
        print("nothing changed")
        return 0
    outside = [f for f in files if not allowed(f, a.scope, a.allow_code)]
    if outside:
        print("OUTSIDE SCOPE (" + ", ".join(a.scope) + "):")
        for f in outside:
            print("  " + f + ("   <- code: a Routine never merges this itself" if f.endswith(CODE) and not a.allow_code else ""))
        return 1
    print(f"in scope: {len(files)} file(s), all within {', '.join(a.scope)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
