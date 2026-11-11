
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

Step 4: Four project-level agents and a reusable verification skill configured.

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
```

Provide exactly one input: quoted text or `--file PATH`. Omitting input or
combining the two displays usage information and exits with a nonzero status.
Unreadable files and invalid UTF-8 produce an error without a traceback.
Importing the module does not run the CLI.

The Planner defines the contract, the Developer implements the tool,
the Tester checks behavior, and the Reviewer checks correctness and scope.
All four roles have specialized agent definitions. The main agent coordinates
their handoffs and combines their results.

Run verification from the repository root:

```bash
python3 -m unittest discover -s tests -v
git diff --check
```

## Documentation

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
