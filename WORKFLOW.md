# Guided Agent Workflow

Run this exercise from the repository root in a Codex session that supports
the custom agents in [.codex/agents/](.codex/agents/).

## Exercise: Count Words in a File

Extend [word_count.py](word_count.py) to accept a UTF-8 file while preserving
the existing text argument behavior. The file-input feature is implemented;
the prompt below can be used to reproduce the exercise from the earlier version
or assess the current implementation against the criteria.

Acceptance criteria:

- `python3 word_count.py "hello agent team"` still prints `3`.
- `python3 word_count.py --file sample.txt` prints the number of
  whitespace-separated words in the UTF-8 file.
- Empty or whitespace-only files print `0`.
- Exactly one input source is required: text or `--file`.
- Missing inputs, conflicting inputs, unreadable files, and invalid UTF-8
  produce a concise error on stderr and a nonzero exit status without a traceback.
- Existing tests continue to pass; new tests cover the file behavior and errors.
- Use only the Python standard library.

## Copyable Prompt

```text
Use the configured planner, developer, tester, and reviewer agents to
implement the file-input exercise in WORKFLOW.md.

Work through these stages in order and wait for each result:
1. Planner: inspect the project and return a small plan based on the
   acceptance criteria. Do not edit files.
2. Developer: implement that plan, including regression tests and CLI
   documentation. Preserve existing behavior and unrelated user changes.
3. Tester: verify every acceptance criterion, run the test suite, and
   report commands, results, and any gaps. Do not change production code.
4. Reviewer: inspect the implementation, tests, and documentation. Include
   newly added files in the review. Return actionable findings with locations.

As the main agent, pass each result to the next agent. If testing or review
finds problems, send them to the Developer, then repeat affected checks
and review. Report which agents actually ran; if a named agent is unavailable,
report that limitation rather than claiming it ran.

Finish with files changed, decisions, verification results, and remaining
issues. Do not commit or push.
```

## Handoff Expectations

| Stage | Receives | Returns |
| --- | --- | --- |
| Planner | Requirements and current project | Plan, assumptions, affected files, checks |
| Developer | Requirements and plan | Changes, implementation decisions, check results |
| Tester | Requirements and implementation | Evidence for each criterion and failures |
| Reviewer | Requirements, full change, test results | Findings with locations and residual risks |

The main agent owns coordination and completion. Keep one implementation
writer active at a time to avoid conflicting edits.

## Verification

Run from the repository root:

```bash
python3 -B -m unittest discover -s tests -v
git diff --check
git status --short
```

Review untracked files explicitly: ordinary `git diff` does not include them.
Successful completion means the criteria are covered by passing tests and
there are no unresolved review findings.

## Second Exercise: Standard Input

Add `--stdin` as a third mutually exclusive input source. Read Python's text
stream until EOF, count whitespace-separated words, and print the same numeric
output. Empty input returns `0`. Preserve text and file input behavior.
Conflicting arguments must fail before reading stdin. Piped input alone does
not select stdin automatically.

Example:

```bash
printf 'hello agent team\n' | python3 word_count.py --stdin
```

For this exercise, use separate planning, development, testing, and review
subagents. Where named custom agents cannot be selected, pass the corresponding
role instructions to a general subagent and disclose that distinction. The
parent handles documentation and integration; only the Developer edits code.
