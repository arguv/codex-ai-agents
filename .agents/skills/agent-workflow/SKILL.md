---
name: agent-workflow
description: Coordinate Planner, Developer, Tester, and Reviewer subagents for a requested change in the Codex AI Agents repository. Use when the user requests the project's delegated implementation workflow.
---

# Agent Workflow

Use the repository containing `word_count.py` and `.codex/agents/`.
Read the relevant project context, role definitions, and current Git status.
Preserve existing work and identify the requested change and acceptance criteria
before delegating. If the request supplies no change, ask for the task rather
than inventing a feature.

## Delegate and Integrate

Use separate subagents for these stages, passing requirements and the previous
stage's result forward. Wait for dependent results before starting the next stage.
While a subagent works, the parent may handle non-overlapping documentation or
integration work; define file ownership to prevent competing edits.

1. **Planner:** Follow `.codex/agents/planner.toml`. Return a small plan,
   assumptions, affected files, and validation checks without editing files.
2. **Developer:** Follow `.codex/agents/developer.toml`. Implement the in-scope
   plan and relevant regression tests. Return changed paths, decisions, and checks.
3. **Tester:** Follow `.codex/agents/tester.toml`. For this workflow, verify
   without edits. Report evidence against the acceptance criteria and any gaps.
4. **Reviewer:** Follow `.codex/agents/reviewer.toml`. Review the full requested
   change, including new files and documentation, with test results as context.
   Return actionable findings with locations, or no findings and residual risks.

Select configured agents when the available tools support named roles. Otherwise,
give general subagents the corresponding role instructions and disclose the
fallback. If delegation is unavailable, report that limitation and complete the
authorized task locally; do not claim separate agents ran.

If agents use isolated checkouts, integrate the Developer's changes before
testing and review. Supply the actual change to review, including staged edits
and new files; do not confuse unrelated pre-existing work with this task.

## Resolve Findings and Finish

Return reproducible failures and actionable review findings to the Developer.
Repeat affected checks and review after fixes. If the same failure persists
after two fix attempts, stop the automatic repair loop and report the evidence
and unresolved issue. Resolve minor implementation choices within the request;
surface requirements that would materially change its scope.

Use the repository's standard checks:

```bash
python3 -B -m unittest discover -s tests -v
git diff --check
git diff --cached --check
```

Report which agents actually ran, files changed, key decisions, verification,
and remaining limitations. Complete only when the acceptance criteria are met
and actionable findings are resolved; distinguish blocked checks from passing
checks. Close finished subagents when supported. Commit or push only when the
user requests it.
