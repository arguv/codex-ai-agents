
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

One project-level Planner is configured; the other agents remain planned.

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
