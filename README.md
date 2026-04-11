# Solo OS

CLI toolkit for solo/small-team project governance on GitHub Projects V2.

## Quick Start

```bash
# Install (editable mode for development)
pip install -e .

# Copy and configure
cp solo-os.example.yml /path/to/your/workspace/solo-os.yml
# Edit solo-os.yml with your GitHub owner, project number, and repo paths

# Run from anywhere inside your workspace
solo-os daily-triage
solo-os gh-list
solo-os gh-brief --question active-work
```

## Configuration

Solo OS uses a single `solo-os.yml` file for all configuration. This file is **local-only** and should never be committed to the solo-os repo.

### Config discovery (3-tier resolution)

1. **`SOLO_OS_ROOT` env var** — explicit override, highest priority
2. **Walk up from cwd** — looks for `solo-os.yml` in parent directories
3. **XDG config home** — `~/.config/solo-os/config.yml` as global fallback

### Setup

Copy `solo-os.example.yml` to your workspace root and fill in your values:

```bash
cp solo-os.example.yml ~/my-workspace/solo-os.yml
```

For a multi-repo workspace, place `solo-os.yml` above all repos:

```
my-workspace/
  solo-os.yml          # config lives here
  repo-a/
  repo-b/
  solo-os/             # the tool itself
```

## Commands

| Command | Description |
|---------|-------------|
| `solo-os daily-triage` | Review stages, flag WIP violations, suggest moves |
| `solo-os gh-list` | List project-backed GitHub issues |
| `solo-os gh-next` | Show next actionable items |
| `solo-os gh-brief --question <q>` | Answer planning questions (active-work, roadmap-now, in-progress-ideas) |
| `solo-os gh-update` | Update issue content and/or project fields |
| `solo-os gh-promote` | Promote an issue to a different Kind |
| `solo-os gh-close` | Close an issue and sync project status |
| `solo-os gh-migrate-titles` | Rename legacy workflow issue prefixes |
| `solo-os sync-audit` | Run local sync audit checks |
| `solo-os cleanup-markdown` | Archive redundant markdown artifacts |
| `solo-os build-loop-template` | Print an issue body template |

## Requirements

- Python >= 3.10
- [GitHub CLI (`gh`)](https://cli.github.com/) authenticated
- PyYAML (installed automatically via pip)

## Templates

Issue body templates for all three workflow kinds:

- `templates/idea-body-template.md`
- `templates/roadmap-body-template.md`
- `templates/build-loop-body-template.md`

Print any template: `solo-os build-loop-template --kind idea`
