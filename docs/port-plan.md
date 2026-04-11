# Port Plan: solo-os v0.1.0 (BL #13)

## Workflow Design Findings

### What works well
- Idea / Roadmap / Build Loop taxonomy is clear and well-differentiated
- Status vs Stage orthogonality (lifecycle position vs temporal focus)
- WIP limits are concrete (3 Today, 7 This Week, 1 BL per repo Today)
- Checkpoint A/B/C structure with explicit required outputs
- Risk Tiers (Low/Medium/High/Critical) with validation matrix
- Direct-to-Build-Loop rule for well-understood work

### Confusing or underspecified
- Idea lifecycle end-state: what "resolved" means for a Done Idea is unclear
- "Ready To Merge" status exists in code but is not documented in workflow-system.md
- Transition mechanics (Idea -> Roadmap, Roadmap -> BL) lack concrete steps
- sos-hq docs described "simple mode" vs "isolated mode" execution — unnecessary complexity removed from solo-os

### Missing
- No templates for Ideas or Roadmap issue bodies (only Build Loop had one)
- No Checkpoint C prompt in the prompt pack
- No weekly review prompt (weekly-cycle is just sync + cleanup, not planning)
- When to close vs leave open after spawning child work

### Simplified for v1
- All execution mode and worktree content removed entirely (not deferred)
- References to hardcoded org/paths made generic
- `agent_generated/` folder convention not assumed for external users

### Docs-vs-code drift
- "Ready To Merge" status: used in build_loop_ops.py but absent from Status options
- Branch naming convention was only enforced in worktree_ops.py (removed from solo-os scope)
- Operating Rules reference `python3 solo-os/scripts/solo_os.py` (old path)

## Per-Module Decisions

| Module | Decision | Notes |
|--------|----------|-------|
| tools/common.py | Port (modified) | `solo_os_root()` removed; `read_env_file()` takes explicit root param; `load_json()` kept as-is |
| tools/github_ops.py | Port (modified) | `project_config()` and `repo_alias_map()` delegate to config module; GraphQL query supports org + user owner types |
| scripts/solo_os.py | Port (redesigned) | Subprocess delegation replaced with direct function imports; only in-scope commands wired |
| scripts/github_ops.py | Port (modified) | Uses config-driven accessors; ANSI helpers extracted to shared display module |
| scripts/daily_triage.py | Port (modified) | Uses config.settings("daily_triage"); ANSI helpers shared; snake_case config keys |
| scripts/sync_audit.py | Port (modified) | Uses config.repo_list() and config.settings("validation"); report path relative to config root |
| scripts/cleanup_markdown.py | Port (modified) | Uses config accessors; report path relative to config root |
| scripts/build_loop_ops.py | **Removed** | Depended on worktree_ops; removed from solo-os scope |
| scripts/worktree_ops.py | **Removed** | Worktree management removed entirely from solo-os scope |
| scripts/init_repo.py | **Deferred** | BL #15 scope |
| scripts/weekly_cycle.py | **Deferred** | Later BL |
| scripts/validate_env.py | **Deferred** | Later BL |
| scripts/bootstrap_github_project.py | **Dropped** | Likely drop for v1; heavily hardcoded seed data |
| config/projects.json | **Migrated** | Values moved to repos: section of solo-os.yml with relative paths |
| config/github_project.json | **Migrated** | Values moved to github: section of solo-os.yml |
| config/settings.json | **Migrated** | Values moved to top-level sections; worktrees section dropped |
| config/github_bootstrap.json | **Not ported** | Seed data stays in sos-hq |
| templates/build-loop-body-template.md | Port (as-is) | Ported unchanged |
| NEW: templates/idea-body-template.md | **Created** | New Idea issue body template |
| NEW: templates/roadmap-body-template.md | **Created** | New Roadmap issue body template |

## Cross-Cutting Improvements

1. **ANSI color helpers extracted** to `solo_os/display.py` — eliminates duplication between github_ops and daily_triage
2. **sys.path.insert() boilerplate eliminated** — proper Python package structure with pip install
3. **GraphQL owner_type support** — separate queries for `organization(login:...)` and `user(login:...)` based on config
4. **Report paths** relative to config root (workspace), not tool installation directory
5. **Consistent error handling** — top-level try/except in CLI catches RuntimeError and prints cleanly
6. **snake_case config keys** throughout — no camelCase/snake_case mismatch

## YAML Parser Decision

**Choice: PyYAML** (adds one dependency via `pyproject.toml`)

Rationale: The config uses nested maps, lists of maps, and quoted strings. A hand-rolled parser would be fragile. TOML would require Python 3.11+ and rename the file. PyYAML is battle-tested and the schema explicitly names `.yml`.

## Confirmed Port List

### Ported in BL #13
- solo_os/config.py (new)
- solo_os/common.py (from tools/common.py)
- solo_os/github_ops.py (from tools/github_ops.py)
- solo_os/display.py (new, extracted from duplicated ANSI code)
- solo_os/cli.py (from scripts/solo_os.py)
- solo_os/commands/github_ops.py (from scripts/github_ops.py)
- solo_os/commands/daily_triage.py (from scripts/daily_triage.py)
- solo_os/commands/sync_audit.py (from scripts/sync_audit.py)
- solo_os/commands/cleanup_markdown.py (from scripts/cleanup_markdown.py)
- templates/build-loop-body-template.md (ported)
- templates/idea-body-template.md (new)
- templates/roadmap-body-template.md (new)

### Removed (not deferred)
- build_loop_ops.py — depended on worktrees, removed from solo-os scope
- worktree_ops.py — worktree management removed entirely from solo-os scope

### Deferred
- init_repo.py, weekly_cycle.py, validate_env.py, bootstrap_github_project.py
