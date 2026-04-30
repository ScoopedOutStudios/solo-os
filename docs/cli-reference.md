# Solo OS CLI Reference

These are the CLI commands available in the `solo-os` package. Most users interact with Solo OS through `chief-of-staff` and the installed AI agents — these commands are the **primitives that agents use under the hood** and are also available for direct use when you prefer manual control.

`solo-os --help` intentionally shows the small AI-assisted path: setup, install the AI packs, ask `chief-of-staff`, and use a few high-signal focus/build commands. This reference keeps the complete command surface for agents, automation, and power users.

## Version and Diagnostics

```bash
solo-os --version       # print installed version
solo-os verify          # first check reports version + executable path
```

If `solo-os --help` shows outdated commands or a stale layout, the installed CLI needs upgrading:

```bash
pipx upgrade solo-os                # normal upgrade
# or force reinstall if the shim is stale:
pipx install --force git+https://github.com/rohitnandwate/solo-os.git
solo-os --version                   # confirm update
```

## Default Help Commands

These commands appear in `solo-os --help` because they are useful to first-time users or common enough to run directly:

| Command | Description |
|---------|-------------|
| `solo-os --version` | Print the installed Solo OS version |
| `solo-os init` | Set up `solo-os.yml` and GitHub Project fields |
| `solo-os verify` | Validate environment, config, and GitHub Project setup |
| `solo-os onboarding` | Print the AI-first getting-started guide |
| `solo-os workflow-start` | Print a guided Idea → Roadmap → Build Loop tour |
| `solo-os install-agents` | Install Solo OS AI agent specs |
| `solo-os install-skills` | Install Solo OS AI skills |
| `solo-os install-commands` | Install Solo OS slash-command shortcuts |
| `solo-os gh-create` | Create a project-backed Idea, Roadmap item, or Build Loop |
| `solo-os gh-next` | Show next actionable items grouped by Kind |
| `solo-os daily-triage` | Review current focus and stage hygiene |
| `solo-os bl-review` | Review Build Loop Checkpoint A readiness |

## Setup Commands

| Command | Description |
|---------|-------------|
| `solo-os init` | Guided setup for `solo-os.yml` and GitHub Project fields |
| `solo-os verify` | Validate environment, config, and project setup |
| `solo-os onboarding` | Print the getting-started guide (empty project, workflow, AI packs) |
| `solo-os workflow-start` | Print a guided Idea → Roadmap → Build Loop tour |

## Install Commands

| Command | Description |
|---------|-------------|
| `solo-os install-agents` | Install agent specs (`--ide cursor\|claude-code`; optional `--target`) |
| `solo-os install-skills` | Install skill specs (`--ide cursor\|claude-code\|codex`; optional `--target`) |
| `solo-os install-commands` | Install command packs (`--ide cursor\|claude-code`; optional `--target`) |

## GitHub Operations (Agent Primitives)

These are the commands that agents use to read and mutate GitHub Project state. You can also run them directly.

| Command | Description |
|---------|-------------|
| `solo-os gh-create` | Create an issue and add it to the Project (optionally set Kind/Status/Stage) |
| `solo-os gh-list` | List project-backed GitHub issues |
| `solo-os gh-next` | Show next actionable items grouped by Kind |
| `solo-os gh-brief --question <q>` | Answer planning questions (`active-work`, `roadmap-now`, `in-progress-ideas`) |
| `solo-os gh-update` | Update issue content and/or project fields |
| `solo-os gh-promote` | Promote an issue to a different Kind |
| `solo-os gh-close` | Close an issue and sync project status |
| `solo-os gh-migrate-titles` | Rename legacy workflow issue prefixes |

## Build Loop Operations

| Command | Description |
|---------|-------------|
| `solo-os bl-review` | Review Build Loop Checkpoint A readiness |
| `solo-os bl-status` | Show open Build Loop issues across repos |
| `solo-os build-loop-template` | Print canonical issue body templates |
| `solo-os daily-triage` | Review stages, flag WIP violations, suggest moves |

## Maintenance

| Command | Description |
|---------|-------------|
| `solo-os sync-audit` | Run local sync audit checks |
| `solo-os cleanup-markdown` | Archive redundant markdown artifacts |
| `solo-os weekly-cycle` | Run weekly maintenance (`sync-audit` + `cleanup-markdown`) |

## Init Examples

```bash
# Interactive
solo-os init

# Existing GitHub Project
solo-os init --yes --owner my-org --project 7

# Create a new GitHub Project
solo-os init --yes --owner my-org --project-title "Solo OS Planning"

# Auto-detect your GitHub username
solo-os init --owner @me
```
