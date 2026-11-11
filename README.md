
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

Step 3: Four project-level agents configured in [.codex/agents/](.codex/agents/).

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
```

Omitting the text argument displays usage information and exits with a
nonzero status. Importing the module does not run the CLI.

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

See [EXPLANATION.md](EXPLANATION.md) for detailed
technical explanations and learning notes.
