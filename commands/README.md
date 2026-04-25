# Solo OS Commands

> **Context:** Slash-commands are power-user shortcuts for specific Solo OS workflow steps. The default path is to ask `chief-of-staff` — it handles most workflow tasks directly and routes to specialists as needed. Use slash-commands when you want to bypass routing and invoke a specific step directly. For the full AI asset model, read [How to use Solo OS](../README.md#how-to-use-solo-os) or run `solo-os onboarding`.

These are **Cursor slash-commands** that provide guided workflows for the Solo OS system. Each command gives the AI agent structured instructions for a specific workflow step — triaging ideas, creating build loops, executing work, validating outcomes, and managing your daily focus.

The Python CLI provides the underlying primitives these slash-commands use:
- `solo-os workflow-start` (quick tour: Idea → Roadmap → Build Loop)
- `solo-os gh-create` (create a GitHub issue, add to Project, and set `Kind/Status/Stage` in one step)

## Installation

Automatic (recommended):

```bash
solo-os install-commands
```

By default, Solo OS installs commands into the workspace root discovered from
`solo-os.yml`, e.g. `<workspace>/.cursor/commands/solo-os`. If no config is
available, it falls back to the current directory. Use `--target` only when you
want to override that automatic workspace resolution.

For other IDE profiles:

```bash
solo-os install-commands --ide claude-code
```

Codex support is intentionally omitted here. Codex best practices center around
`AGENTS.md` plus skills rather than markdown command packs.

Manual: copy the `.md` files from this directory into your IDE command directory in the target repo.

## Commands

| Command | Description |
|---------|-------------|
| `bl-checkpoint-b` | Run Checkpoint B validation for a Build Loop and decide Ship / Hold |
| `bl-create` | Create a new Build Loop from a roadmap item, idea, or direct objective |
| `bl-execute` | Execute a Build Loop using Solo OS (simple or isolated mode) |
| `bl-merge` | Approve and run merge-back for a completed Build Loop |
| `bl-recalibrate` | Pressure-test and recalibrate a planned but unexecuted Build Loop |
| `bl-revisit` | Revisit a completed Build Loop and evaluate the outcome |
| `daily-triage` | Run daily triage across all stages with WIP checks and focus recommendations |
| `idea-triage` | Triage a new candidate idea as Idea, Roadmap, or direct Build Loop |
| `roadmap-plan` | Promote an approved idea to a Roadmap item with outcome and linkage |

## Note

Prompts (`.prompt` files) are deprecated in favor of commands. Use the commands listed above for all Solo OS workflows.
