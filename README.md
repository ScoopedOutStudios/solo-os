# Solo OS

CLI toolkit for solo/small-team project governance on GitHub Projects V2.

## Tracking Backend: GitHub Projects V2

Solo OS uses **GitHub Projects V2** as its single source of truth for tracking ideas, roadmap items, build loops, and day-to-day tasks. All issue triage, status updates, and planning queries go through a GitHub Project board with structured fields (Kind, Status, Stage).

Other project-tracking backends (Linear, Jira, Notion, etc.) are **not currently supported**. The architecture is open to adding alternative backends in the future — contributions are welcome.

## Prerequisites

Install the required tools before running solo-os.

**macOS (Homebrew)**

```bash
brew install gh git python pipx
gh auth login
gh auth refresh --scopes project   # required for GitHub Projects access
```

**Linux (apt)**

```bash
sudo apt install git python3 python3-pip pipx
pipx ensurepath
# Install gh: https://github.com/cli/cli/blob/trunk/docs/install_linux.md
gh auth login
gh auth refresh --scopes project   # required for GitHub Projects access
```

**Windows**

```bash
winget install GitHub.cli Git.Git Python.Python.3 pipx
gh auth login
gh auth refresh --scopes project   # required for GitHub Projects access
```

After setup, confirm your token has the right scopes:

```bash
gh auth status   # should show 'project' in Token scopes
```

## Key Concept: Workspace vs Repo

Solo OS is a **workspace-level** tool, not a per-repo tool. It manages one or more Git repos through a single `solo-os.yml` config file that sits at your **workspace root** — the parent directory that contains your repo(s).

```
# Single-repo workspace             # Multi-repo workspace
my-project/                          my-workspace/
  solo-os.yml  ← config here           solo-os.yml  ← config here
  src/                                  app-backend/
  ...                                   app-frontend/
                                        marketing-site/
```

You run `solo-os init` **once** from the workspace root. It creates the config, sets up your GitHub Project, and registers your first repo. You do **not** run init separately for each repo.

## Quick Start

```bash
# Install (no clone required)
pipx install git+https://github.com/ScoopedOutStudios/solo-os.git

# Set up — run from your workspace root
cd ~/my-workspace        # parent dir of your repo(s)
solo-os init

# Confirm everything works
solo-os verify
```

That's it — three commands to a working setup. Now use solo-os from anywhere inside your workspace:

```bash
solo-os daily-triage
solo-os gh-list
solo-os gh-brief --question active-work
```

## Configuration

Solo OS uses a single `solo-os.yml` file for all configuration. This file is **local-only** and should not be committed to any repo.

### Config discovery (3-tier resolution)

1. `**SOLO_OS_ROOT` env var** — explicit override, highest priority
2. **Walk up from cwd** — looks for `solo-os.yml` in parent directories (so commands work from any subdirectory)
3. **XDG config home** — `~/.config/solo-os/config.yml` as global fallback

### Adding repos to an existing workspace

You do **not** re-run `solo-os init` to add repos. Edit `solo-os.yml` directly:

```yaml
repos:
  - id: app-backend        # existing repo
    path: ./app-backend
    active: true
  - id: app-frontend       # add this block for the new repo
    path: ./app-frontend
    active: true
```

All repos share the same GitHub Project and field configuration.

## Commands


| Command                           | Description                                                             |
| --------------------------------- | ----------------------------------------------------------------------- |
| `solo-os init`                    | Guided setup for `solo-os.yml` and GitHub Project fields                |
| `solo-os verify`                  | Validate environment, config, and project setup                         |
| `solo-os daily-triage`            | Review stages, flag WIP violations, suggest moves                       |
| `solo-os gh-list`                 | List project-backed GitHub issues                                       |
| `solo-os gh-next`                 | Show next actionable items                                              |
| `solo-os gh-brief --question <q>` | Answer planning questions (active-work, roadmap-now, in-progress-ideas) |
| `solo-os gh-update`               | Update issue content and/or project fields                              |
| `solo-os gh-promote`              | Promote an issue to a different Kind                                    |
| `solo-os gh-close`                | Close an issue and sync project status                                  |
| `solo-os gh-migrate-titles`       | Rename legacy workflow issue prefixes                                   |
| `solo-os sync-audit`              | Run local sync audit checks                                             |
| `solo-os cleanup-markdown`        | Archive redundant markdown artifacts                                    |
| `solo-os build-loop-template`     | Print an issue body template                                            |


## Init Examples

```bash
# Interactive setup — run from your workspace root
cd ~/my-workspace
solo-os init

# Non-interactive with an existing GitHub Project
solo-os init --yes --owner ScoopedOutStudios --project 7

# Non-interactive — creates a new GitHub Project automatically
solo-os init --yes --owner ScoopedOutStudios --project-title "Solo OS Planning"

# Use @me to auto-detect your GitHub username
solo-os init --owner @me
```

## Templates

Issue body templates for all three workflow kinds:

- `templates/idea-body-template.md`
- `templates/roadmap-body-template.md`
- `templates/build-loop-body-template.md`

Print any template: `solo-os build-loop-template --kind idea`

## Development

To contribute or modify solo-os itself, clone the repo and install in editable mode:

```bash
git clone https://github.com/ScoopedOutStudios/solo-os.git
cd solo-os
pipx install -e .        # or: pip install -e .
```

Changes to the source are immediately reflected in the `solo-os` command.