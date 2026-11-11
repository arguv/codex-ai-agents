
# Codex AI Agents

A hands-on project for learning specialized AI coding
agents using OpenAI Codex.

## Goals

- Understand Codex project instructions.
- Create custom coding subagents.
- Build reusable Agent Skills.
- Learn task delegation and coordination.
- Practice automated testing and code review.
- Build reliable multi-agent development workflows.

## Configured Agents

1. Planner Agent
2. Developer Agent
3. Tester Agent
4. Reviewer Agent

## Current Progress

Step 10: Retain the review's open-stdin and option-order checks as regression tests.

Follow [WORKFLOW.md](WORKFLOW.md) for a guided collaboration exercise.

Ask Codex: "Use the planner agent to inspect this project and
propose a small implementation plan for [task]. Do not modify files."

## First Coding Exercise: Word Count

This exercise practices the Planner, Developer, Tester, and Reviewer
handoffs with a small Python command-line tool. It requires Python 3
and uses only the standard library.

`count_words(text)` in `word_count.py` counts whitespace-separated tokens.
Empty or whitespace-only text returns `0`; punctuation stays attached
to tokens. Quote text containing spaces when using the CLI:

```bash
python3 word_count.py "hello agent team"  # Prints 3
python3 word_count.py ""                  # Prints 0
python3 word_count.py --file sample.txt   # Counts words in a UTF-8 file
python3 word_count.py --version          # Prints word-count 1.0
printf 'hello agent team\n' | python3 word_count.py --stdin  # Prints 3
```

Provide exactly one input: quoted text, `--file PATH`, or `--stdin`. Omitting input or
combining sources displays usage information and exits with a nonzero status.
Unreadable files and invalid UTF-8 produce an error without a traceback.
Importing the module does not run the CLI.

`--stdin` reads piped text until EOF using Python's standard-input encoding.
Empty or whitespace-only input prints `0`. With interactive input, finish
with EOF (Ctrl-D on Unix). Input is read only when `--stdin` is selected.
Stdin I/O and decoding failures print an error on stderr and exit with status
`2`, without printing a count or a traceback.

The Planner defines the contract, the Developer implements the tool,
the Tester checks behavior, and the Reviewer checks correctness and scope.
All four roles have specialized agent definitions. The main agent coordinates
their handoffs and combines their results.

Run verification from the repository root:

```bash
python3 -m unittest discover -s tests -v
git diff --check
```

## Automated Tests

[GitHub Actions](.github/workflows/tests.yml) runs the tests on Ubuntu 24.04 with
Python 3.10 for pushes, pull requests, and manual runs. No package installation
is needed. After pushing the workflow, open the repository's **Actions** tab
and select **Python tests** to inspect the result. Pull requests also show the
test result in their checks.

These automated tests complement `$project-check`: review and local diff
checks still run locally. A failing test fails the job; making it a required
merge check is a separate repository setting.

## Documentation

Use [agent-workflow](.agents/skills/agent-workflow/SKILL.md) to coordinate the
four roles for a specific change. Example request:

```text
Use $agent-workflow to add --version to the CLI. It should print
word-count 1.0 and exit successfully without requiring an input source.
Preserve existing counting behavior and add regression tests.
```

The `--version` example is implemented and exits without requiring an input
source or reading stdin or a file. It uses argparse's built-in version action.
The skill passes plans and results between agents, returns findings for fixes, and reports
which agents actually ran. It does not commit or push automatically.

The repository skill [project-check](.agents/skills/project-check/SKILL.md)
runs the test suite and checks staged and unstaged diffs. In a Codex session
opened in this repository, ask:

```text
Use $project-check to verify this project and report the results.
```

If the skill is not shown in the selector, restart the Codex session in this
repository. The skill checks the project; it does not automatically fix or commit.

See [EXPLANATION.md](EXPLANATION.md) for detailed
technical explanations and learning notes.
