
# Codex AI Agents — Learning Notes

## Step 1 — Project Foundation

### What is Codex?

Codex is an AI coding agent that can inspect repositories,
edit code, execute commands, and help with software
development tasks.

### What is AGENTS.md?

AGENTS.md contains project-specific instructions for Codex.

Codex reads applicable instruction files when starting
a session.

### What is a Subagent?

A subagent is a specialized agent that can receive
delegated work from a parent agent.

Examples:
- Planning implementation tasks
- Writing code
- Testing functionality
- Reviewing changes

### What is a Skill?

A Skill is a reusable set of instructions for a
specific workflow, optionally including scripts and
reference materials.

### Current Status

Created the initial project documentation and
repository instructions.

Four project-level agents are configured: Planner, Developer, Tester, and Reviewer.

## Step 2 — Planner Agent

The configuration is [.codex/agents/planner.toml](.codex/agents/planner.toml).
According to the [official custom-agent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents),
Codex discovers project agents as standalone TOML files in `.codex/agents/`.
No registration in `.codex/config.toml` is needed for this setup.

The file contains only the three required fields:

| Field | Purpose |
| --- | --- |
| `name` | `planner` is the identifier used to request this agent. |
| `description` | Tells the parent agent when to select the Planner. |
| `developer_instructions` | Defines inspection, requirement clarification, small plans, validation suggestions, and the prohibition on modifying files. |

Model and reasoning overrides are omitted to keep the setup minimal and
use the parent session's resolved defaults. No additional agents,
dependencies, or global configuration are introduced.

The Planner reads relevant files, reports important unanswered questions
to the parent, and returns a short plan with affected paths and checks.
It returns the plan in its response instead of writing a plan file.

The no-edit rule is an instruction, not a separate sandbox guarantee.
Custom agents inherit the parent's sandbox and approval settings;
`sandbox_mode` in a custom-agent file does not override them. For an
enforced read-only planning session, start the parent CLI with
`codex --sandbox read-only` before requesting the Planner.

Example request: "Use the planner agent to inspect this project and
propose a small implementation plan for [task]. Do not modify files."

## Step 3 — Agent Collaboration

The agent definitions live in [.codex/agents/](.codex/agents/). The Planner
returns requirements and a plan; the Developer implements them; the Tester
checks behavior; the Reviewer inspects correctness and maintainability.
The main agent passes the relevant context between stages, handles feedback,
and reports the final outcome.

Defining roles does not automatically run a workflow. Request delegation
explicitly and identify what each agent should return. See the
[official subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents).

For this learning exercise, stages run sequentially because each consumes the
previous stage's output. If testing or review identifies a problem, return it
to the Developer and repeat the affected checks. Agent instructions define
responsibilities; they do not enforce separate sandbox permissions.

[WORKFLOW.md](WORKFLOW.md) contains the next exercise and its acceptance criteria.

## Step 4 — A Reusable Verification Skill

[project-check](.agents/skills/project-check/SKILL.md) packages the recurring
verification procedure: run the standard-library tests, check both staged and
unstaged diffs, and report failures. Its instructions also account for untracked
files and Python subprocess bytecode caches.

An agent defines a worker's role. A skill defines a reusable procedure that an
agent can follow. This skill needs only instructions, so there are no helper
scripts or dependencies.

Repository skills are discovered under `.agents/skills/`, as described in the
[official skill documentation](https://learn.chatgpt.com/docs/build-skills).
Invoke this one with `$project-check` from a session opened in this repository.

## Step 5 — Continuous Integration

[The test workflow](.github/workflows/tests.yml) runs the same unittest command
used locally on a GitHub-hosted Ubuntu 24.04 runner with Python 3.10. This fixes the
interpreter version while keeping the workflow dependency-free. It follows
[GitHub's Python workflow guidance](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).

Pushes and pull requests trigger tests automatically; `workflow_dispatch`
also allows a manual run. The workflow has read-only repository permissions
and a five-minute timeout. It runs tests, while agents handle planning,
implementation, and review. CI does not invoke the Codex agents or require
an OpenAI API key.

The workflow takes effect once committed and pushed. Its remote execution
must be checked in GitHub Actions; passing local tests does not confirm a
successful hosted run.

The runner uses `ubuntu-24.04` to avoid automatic OS version migrations from
`ubuntu-latest`. The image still receives updates. `actions/setup-python@v6`
uses Node.js 24 internally, resolving the earlier Node.js 20 deprecation
warning without changing the project's Python version. See the
[action's v6 migration notes](https://github.com/actions/setup-python/tree/v6#breaking-changes-in-v6).

## Step 6 — Delegation Exercise: Standard Input

The next feature adds explicit `--stdin` support while preserving the existing
text and file sources. The same mutually exclusive argument group rejects
conflicting inputs before any stdin read. Text is read through EOF using
Python's standard-input encoding.

For this exercise, the parent passed the repository role instructions to
separate general subagents because the session tool could not select custom
agent names directly. The Planner returned a plan, the Developer changed
implementation and tests, and separate Tester and Reviewer agents checked the
result. The parent maintained documentation and integrated their findings.

This demonstrates delegation without claiming that named custom-agent loading
was exercised. See [WORKFLOW.md](WORKFLOW.md) for the feature contract.

The Tester passed all 11 tests on Python 3.10 and checked open pipes to verify
that parse errors do not wait for EOF. Interactive terminal input and other
platforms were not tested in this session.

## Step 7 — Fix a Review Limitation with Regression Tests

The prior review noted that stdin read failures could escape as tracebacks.
The next exercise reproduced this with a failing regression test that injects
an `OSError` and a `UnicodeDecodeError` into the input stream. The fix catches
these errors around the stdin read and uses the same argparse error mechanism
as file input: stderr diagnostics, exit status `2`, and no count on stdout.

The regression checks the observable error behavior rather than the exact
underlying operating-system message. Input is still buffered entirely in
memory, and stdin encoding remains controlled by Python's environment.

## Step 8 — Package Orchestration as a Skill

[agent-workflow](.agents/skills/agent-workflow/SKILL.md) turns the prior manual
handoffs into a reusable procedure. The parent supplies a concrete task and
acceptance criteria, coordinates the four roles, integrates implementation,
and returns test or review findings for correction.

The procedure defines a bounded repair loop and requires honest reporting of
delegation availability. It uses the existing role files instead of duplicating
their full instructions. As with the first skill, no scripts or runtime
dependencies are needed: the skill guides Codex's orchestration tools rather
than implementing a separate agent runtime.

Invoke it as `$agent-workflow` followed by the change you want. Creating this
skill does not itself run another feature implementation.

## Step 9 — Exercise the Orchestration Skill

The workflow's first feature exercise is `--version`. It prints
`word-count 1.0` and exits successfully without requiring an input source.
Argparse's built-in version action runs during parsing, before source reads,
so there is no separate manual parsing path to maintain.

The parent uses the skill to pass a plan, implementation, test evidence, and
review findings between separate role-guided subagents, while owning the
documentation. Regression tests verify exact output and that version reporting
does not read stdin or files. Normal argparse option-order semantics apply;
version reporting does not promise to override every malformed command line.

The Tester passed all 14 tests and separately verified that version reporting
exits with stdin still open. This exercises the skill's normal handoff path;
it does not exercise its repair-loop stopping condition or guarantee behavior
on platforms not tested locally.

## Step 10 — Preserve Exploratory Checks in CI

The review identified useful manual checks that were missing from the permanent
suite. New subprocess regressions leave the stdin pipe open while waiting for
version reporting to exit. Closing the pipe first would hide an accidental read
that blocks until EOF. A five-second timeout fails the test and kills and reaps
the child process, so a regression cannot hang the test run indefinitely.

Option-order tests also preserve argparse behavior: `--version --file` exits
with the version, while `--file --version` reports the missing file argument.
After the option terminator, `-- --version` counts the literal text as one word.
These tests turn the earlier review evidence into repeatable CI coverage.

## Step 11 — Evaluate the Agents, Not Only the Code

[EVALUATION.md](EVALUATION.md) defines controlled cases for normal delegation,
repair handoffs and their stopping condition, missing requirements, and absent
delegation tools. Each run records the setup, real agent outputs, changed files,
verification, and an evidence-backed outcome.

Application tests can pass even if a coordinator skips review or invents an
agent result. Workflow evaluation therefore checks the execution trace as well
as the final code. Failure-injection cases belong in isolated environments;
some require a harness that can pause handoffs or control returned results.

The first controlled run is recorded in
[EVALUATION_RESULTS.md](EVALUATION_RESULTS.md). Clarification and local fallback
passed. Nested delegation was unavailable, so controlled role handoffs and
repair-loop behavior remain unverified. The earlier exercises provide separate
historical evidence, not a pass for the unexecuted scenarios.

## First-Phase Handoff

The implemented learning scope covers role definitions, reusable verification
and orchestration skills, delegated feature development, regression testing,
CI, and an initial controlled evaluation. No demonstrated skill defect required
a fix after that evaluation. Documentation now distinguishes the historical
exercise contracts from current CLI behavior and records the unverified cases.

Final publication consists of committing the reviewed changes, pushing them,
and checking the resulting GitHub Actions run. That hosted result must be
reported separately from local checks. Controlled handoff and repair-limit
evaluations remain follow-up work, rather than being described as completed.
