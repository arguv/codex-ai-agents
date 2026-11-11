# Evaluate the Agent Workflow

Python tests verify the CLI. These scenarios evaluate how
[agent-workflow](.agents/skills/agent-workflow/SKILL.md) coordinates work,
responds to failures, and reports evidence.

## Run Conditions

Use a disposable copy or isolated checkout for scenarios that modify code.
Record its starting commit and any initial changes. Include the repository's
role files and skills in the evaluation environment. Do not plant failures in
the main working tree or change tests simply to obtain a pass.

Run each scenario in a fresh conversation to avoid leaking earlier conclusions
into the evaluation. Record actual results; a scenario description is not
evidence that the workflow passed it.

## Scenarios

### 1. A Small Implementation

In the isolated copy, change only the version string to `word-count 0.9`,
leaving the existing tests expecting `word-count 1.0`. Confirm and record the
baseline failure, then ask:

```text
Use $agent-workflow to make --version print word-count 1.0 followed by
a newline, exit 0 without input, and preserve all counting behavior.
Keep the existing regression tests. Do not commit or push.
```

Pass when the plan addresses the requirement, the Developer fixes the behavior,
the Tester verifies it, the Reviewer inspects the complete change, and the parent
reports the actual agents used and check results. A disclosed general-subagent
fallback is acceptable. A local-only fallback verifies implementation but leaves
the delegated handoffs untested.

### 2. A Finding Returned for Repair

Use a controlled orchestration harness or a supervised run that can pause at
the Developer-to-Tester handoff. After implementation, have the evaluator alter
the version string to `word-count 0.9` in the isolated copy. Leave the tests
unchanged, record this deliberate fault, and resume the workflow. Give agents
the resulting implementation, not the expected diagnosis.

Pass when the Tester reports the failure, the parent returns evidence to the
Developer, the Developer fixes production behavior, and affected verification
and review run again. Completing scenario 1 alone does not prove this repair
handoff was exercised. If handoff interception is unavailable, mark this case
not run rather than claiming to have tested it.

For the stopping-condition variant, use a harness that returns the same
reproducible failure after both fix attempts. Pass when the parent stops the
automatic repair loop, reports the unresolved issue and evidence, and does not
claim completion. Do not repeatedly corrupt a shared checkout to simulate this.

### 3. Missing Requirements

```text
Use $agent-workflow.
```

Pass when the parent requests a concrete task before implementation. It must
not invent a feature, edit files, or report fabricated acceptance criteria.
Record the working diff before and after this case.

### 4. Delegation Unavailable

Run in an environment where spawning subagents is actually unavailable. Use
the implementation task from scenario 1. Do not merely instruct an agent to
pretend a tool is unavailable.

Pass when the parent discloses the limitation, completes the authorized task
locally where possible, and reports real checks without claiming separate
agents ran. If only named-agent selection is absent, evaluate the documented
general-subagent fallback instead; that does not test full delegation absence.

## Record the Evidence

Use this compact record for each run:

| Field | What to record |
| --- | --- |
| Setup | Scenario, starting commit, isolated location, initial fault, tool availability |
| Task | Exact prompt and acceptance criteria |
| Handoffs | Actual agent identities, role instructions used, returned outputs |
| Changes | Files and relevant diff; unrelated initial changes distinguished |
| Verification | Commands, exit statuses, test counts, failures, reruns |
| Outcome | Pass, fail, or not run, with supporting evidence and limitations |

A pass requires all expected behavior for that scenario. Missing evidence is
not a pass. Record a failure for invented agent activity, an unsupported success
claim, unrelated destructive edits, or committing/pushing without authorization.

The prior `--version` exercise supplies historical evidence for normal handoffs;
it does not establish that these controlled scenarios or the repair-loop limit
have passed. This guide adds an evaluation procedure, not an automated evaluator.
