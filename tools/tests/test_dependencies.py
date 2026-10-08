"""Dependency rules from DEPENDENCIES.md, which follows ENISA's secure-package-consumption skill:
every third-party package pinned by version and hash, installed only from requirements.txt
with hashes enforced, and nothing else installed by a script or a Routine prompt."""
import contextlib
import importlib.util
import io
import os
import re
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location("check_pins", os.path.join(REPO, "tools", "check_pins.py"))
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

SKIP_DIRS = {".git", ".claude", "node_modules", "__pycache__", "img", os.path.join("euvd", "details"),
             "guide-sync", os.path.join("commission-faq", "text"), os.path.join("commission-faq", "versions")}
SKIP_FILES = {"DEPENDENCIES.md",                                   # quotes the old commands as "before"
              os.path.join("tools", "tests", "test_dependencies.py")}
INSTALL = re.compile(r"\b(?:pip3?|python3? -m pip)\s+install\s+[-\w./]|\bnpm\s+(?:i|install|ci|add)\s+[-\w@./]"
                     r"|\bnpx\s+\w|\b(?:yarn|pnpm)\s+(?:add|install)\b|\bapt(?:-get)?\s+install\s+\w")
HASH = "a" * 64


def repo_text_files():
    for d, dirs, files in os.walk(REPO):
        rel = os.path.relpath(d, REPO)
        dirs[:] = [x for x in dirs if os.path.normpath(os.path.join(rel, x)) not in SKIP_DIRS and x not in SKIP_DIRS]
        for f in files:
            path = os.path.normpath(os.path.join(rel, f))
            if f.endswith((".md", ".py", ".sh", ".js")) and path not in SKIP_FILES:
                yield path


class Rules(unittest.TestCase):
    def test_requirements_are_pinned_and_hashed(self):
        reqs = cp.parse(open(os.path.join(REPO, "requirements.txt"), encoding="utf-8").read())
        self.assertEqual([r["name"] for r in reqs], ["pypdf"])
        self.assertEqual(cp.policy(reqs), [])

    def test_installs_only_from_the_hashed_requirements(self):
        bad = []
        for path in repo_text_files():
            for n, line in enumerate(open(os.path.join(REPO, path), encoding="utf-8", errors="replace"), 1):
                m = INSTALL.search(line)
                if m and not ("pip" in m.group(0) and "--require-hashes" in line and "-r requirements.txt" in line):
                    bad.append(f"{path}:{n}: {line.strip()[:100]}")
        self.assertEqual(bad, [], "install commands outside requirements.txt with --require-hashes")


class CheckPins(unittest.TestCase):
    def run_main(self, text, advisories=None):
        fd, path = tempfile.mkstemp(suffix=".txt")
        with os.fdopen(fd, "w") as fh:
            fh.write(text)
        self.addCleanup(os.remove, path)
        orig = cp.osv
        cp.osv = lambda name, version: list(advisories or [])
        self.addCleanup(setattr, cp, "osv", orig)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return cp.main(["--file", path])

    def test_parse_joins_continued_lines_and_drops_comments(self):
        reqs = cp.parse(f"# comment\npypdf==6.19.0 \\\n    --hash=sha256:{HASH}  # trailing\n")
        self.assertEqual(reqs[0]["name"], "pypdf")
        self.assertEqual((reqs[0]["version"], reqs[0]["hashes"]), ("6.19.0", [HASH]))

    def test_clean_pin_passes(self):
        self.assertEqual(self.run_main(f"pypdf==6.19.0 --hash=sha256:{HASH}\n"), 0)

    def test_advisory_on_the_pinned_version(self):
        self.assertEqual(self.run_main(f"pypdf==6.18.1 --hash=sha256:{HASH}\n", [{"id": "GHSA-x", "summary": "s"}]), 1)

    def test_unpinned_or_unhashed_breaks_the_rule(self):
        self.assertEqual(self.run_main("pypdf\n"), 3)
        self.assertEqual(self.run_main("pypdf>=6\n"), 3)
        self.assertEqual(self.run_main("pypdf==6.19.0\n"), 3)

    def test_index_options_are_refused(self):
        self.assertEqual(self.run_main(f"--extra-index-url https://example.org/simple\npypdf==6.19.0 --hash=sha256:{HASH}\n"), 2)


if __name__ == "__main__":
    unittest.main()
