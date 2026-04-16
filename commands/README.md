# Solo OS Commands

These are **Cursor slash-commands** that provide guided workflows for the Solo OS system. Each command gives the AI agent structured instructions for a specific workflow step — triaging ideas, creating build loops, executing work, validating outcomes, and managing your daily focus.

## Installation

Automatic (recommended):

```bash
solo-os install-commands
```

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
