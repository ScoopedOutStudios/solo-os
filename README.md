# Solo OS

CLI toolkit for solo/small-team project governance on GitHub Projects V2.

## Tracking Backend: GitHub Projects V2

Solo OS uses **GitHub Projects V2** as its single source of truth for tracking ideas, roadmap items, build loops, and day-to-day tasks. All issue triage, status updates, and planning queries go through a GitHub Project board with structured fields (Kind, Status, Stage).

Other project-tracking backends (Linear, Jira, Notion, etc.) are **not currently supported**. The architecture is open to adding alternative backends in the future — contributions are welcome.

## Prerequisites

- `gh` installed and authenticated (`gh auth login`)
- `git` installed
- Python available (3.10+)

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
# 1. Install solo-os
pip install -e .          # or: pip install solo-os

# 2. Navigate to your workspace root
#    Single-repo:  cd into the cloned repo
#    Multi-repo:   cd into the parent directory above your repos
cd ~/my-workspace

# 3. Run guided setup (creates solo-os.yml + GitHub Project fields)
solo-os init

# 4. Verify everything is configured correctly
solo-os verify

# 5. Start using solo-os (works from anywhere inside the workspace)
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


## Requirements

- Python >= 3.10
- [GitHub CLI (`gh`)](https://cli.github.com/) authenticated
- git
- PyYAML (installed automatically via pip)

`solo-os init` now performs prerequisite checks at startup and exits with actionable fixes if `gh`/`git` are missing or `gh` auth is not configured.

## Init Examples

```bash
# Interactive setup — run from your workspace root
cd ~/my-workspace
solo-os init

# Non-interactive with an existing GitHub Project
solo-os init --yes --owner ScoopedOutStudios --project 7

# Non-interactive — creates a new GitHub Project automatically
solo-os init --yes --owner ScoopedOutStudios --project-title "Solo OS Planning"

# Single-repo shortcut — run from inside a cloned repo
cd ~/my-workspace/my-app
solo-os init --mode single
```

## Templates

Issue body templates for all three workflow kinds:

- `templates/idea-body-template.md`
- `templates/roadmap-body-template.md`
- `templates/build-loop-body-template.md`

Print any template: `solo-os build-loop-template --kind idea`