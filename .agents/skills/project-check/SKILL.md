---
name: project-check
description: Verify the Codex AI Agents word-count project by running its unittest suite and checking the working diff. Use for project verification or a pre-commit check.
---

# Project Check

Run from this repository's root, identified by `word_count.py` and
`tests/test_word_count.py`. If running elsewhere, locate that root first.

Inspect `git status --short` and the relevant changes to establish scope.
Include staged changes and new files when reviewing; `git diff` alone omits them.

Run these checks separately so each outcome is recorded:

```bash
python3 -B -m unittest discover -s tests -v
git diff --check
git diff --cached --check
```

The Python tool uses only the standard library. Do not install packages to run
these tests. `-B` avoids bytecode caches; subprocesses also need `-B` if adding
tests that launch Python.

Report test counts, command outcomes, and concrete failures or unverified areas.
A check that could not run is not a pass. Verification alone does not authorize
fixes, staging, commits, or pushes; report failures unless the user also asked
for fixes.
