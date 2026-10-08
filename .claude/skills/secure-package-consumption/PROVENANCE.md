# Provenance of this skill

This directory is ENISA's **secure-package-consumption** skill, copied unchanged from
ENISA's public repository so that Claude Code loads it as a project skill in this
repository (`.claude/skills/<name>/SKILL.md`), in interactive sessions and in the
scheduled Routines alike.

| | |
|---|---|
| Source | <https://github.com/enisaeu/agentic-skills>, `skills/secure-package-consumption/` |
| Commit | `202058f242eb098c485087504fddb91b186db82b` (2026-09-16, "Added secure-package-consumption v2.0-beta") |
| Skill version | 2.0-beta |
| Copied | 2026-10-08; `SKILL.md`, `README.md` and `references/` byte-identical to the source |
| Licence | **EUPL-1.2** (`LICENSE.txt`, copied from the source repository's root). This directory is not covered by the repository's MIT licence. |
| Source publication | ENISA, *Technical Advisory for Secure Use of Package Managers*, DOI [10.2824/6157993](https://doi.org/10.2824/6157993) |

Only this file and `LICENSE.txt` were added. To update, copy the directory again from
a newer commit, replace the files, and update the table above; do not edit the skill's
own files, so that a diff against ENISA's repository stays empty.

ENISA's repository describes its skills as provided "for demonstration and reference
purposes only" and not for production use "without appropriate review, testing, and
adaptation". Here it is guidance for the agent, nothing more: dependency changes still
go through review (`CLAUDE.md`, "Dependencies"), and `tools/tests/test_dependencies.py`
enforces the pins the skill led to.

How it was applied to this repository, with what changed and why: `DEPENDENCIES.md`.
