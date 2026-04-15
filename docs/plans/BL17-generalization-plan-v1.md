# BL17 Generalization Plan — Port Agent and Skill Specs to solo-os

artifact_type: plan
status: draft
version: v1.0
created_at: 2026-04-15
parent_issue: ScoopedOutStudios/sos-hq#17
parent_roadmap: ScoopedOutStudios/sos-hq#12

## Overview

This plan documents per-file decisions for porting agent specs, skill specs, commands, and prompts from the private `sos-hq` repo to the public `solo-os` repo. It captures review findings and cross-cutting improvements identified during Phase 1.

---

## 1. Cross-cutting changes (apply to ALL ported files)

### 1a. ScoopedOut → Solo OS language

Every ported file must replace:

| Find | Replace with |
|------|-------------|
| `In ScoopedOut Studios repos, …` | `In repos managed by Solo OS, …` |
| `ScoopedOut Studios` | Remove or replace with generic context |
| `ScoopedOutStudios` (GitHub org) | `<owner>` or remove |
| `sos-hq` (repo name) | Remove; use repo-relative paths or `docs/` |
| `From the sos-hq repo root, prefer …` | `Prefer …` (no root assumption) |
| `Datamural` / `Datamural.io` | Remove product-specific examples; use generic placeholders |

### 1b. CLI path update

| Find | Replace with |
|------|-------------|
| `python3 solo-os/scripts/solo_os.py` | `solo-os` |
| `(from sos-hq repo root)` | Remove |

### 1c. Governance doc paths

| Find | Replace with |
|------|-------------|
| `sos-hq/docs/governance/workflow-system.md` | `docs/governance/workflow-system.md` |
| `sos-hq/docs/governance/build-loop-and-release-rhythm.md` | `docs/governance/build-loop-and-release-rhythm.md` |
| `sos-hq/docs/governance/artifact-governance-spec.md` | `docs/governance/artifact-governance-spec.md` |
| `sos-hq/docs/governance/leadership-team.md` | `docs/governance/leadership-team.md` |
| `sos-hq/docs/governance/backlog-and-papercut-sweep.md` | `docs/governance/backlog-and-papercut-sweep.md` |

### 1d. Model version references

Replace `Claude Opus 4.6` or similar dated model names with `frontier generative AI models` in Execution Context sections.

### 1e. Cursor IDE references

For this BL, keep Cursor-specific formatting (YAML frontmatter, `.cursor/` paths) since IDE-agnostic support is BL #18. Note Cursor-specific elements with comments for future extraction.

---

## 2. Agent specs — per-file decisions

**Source:** `sos-hq/agents-spec/` → **Target:** `solo-os/agents/`

### 2a. All agents (shared changes)

Every agent spec has a **Repo scope** block and **GitHub CLI** block that are near-identical. Apply cross-cutting changes from §1 uniformly.

The shared boilerplate to generalize in every agent:

1. **Repo scope block**: Replace `In ScoopedOut Studios repos` with `In repos managed by Solo OS`
2. **Canonical workflow model**: Replace `sos-hq/docs/governance/workflow-system.md` with `docs/governance/workflow-system.md`
3. **GitHub CLI**: Replace `python3 solo-os/scripts/solo_os.py gh-list|...` with `solo-os gh-list|...`; remove `(from sos-hq repo root)`
4. **Build Loop CLI** (cos, staff only): Replace `python3 solo-os/scripts/solo_os.py bl-review|...` with `solo-os bl-review|...`
5. **Artifact governance path**: Replace `sos-hq/docs/governance/artifact-governance-spec.md` with `docs/governance/artifact-governance-spec.md`
6. **Execution Context**: Replace `Claude Opus 4.6` with `frontier generative AI models`

### 2b. Per-file special cases

| File | Special action |
|------|---------------|
| `README.md` | Rewrite entirely for public solo-os context. Remove sync-cursor-assets.sh references, sos-hq framing. Add install-agents usage instructions. |
| `agm.md` | Replace `studio-level repo (sos-hq)` with `hub repo` or `workspace root`. |
| `cos.md` | Deepest coupling. Replace multiple `sos-hq/docs/governance/` paths (5+ unique docs). Reconcile papercut sweep GitHub-first vs markdown backlog note. |
| `design.md` | Replace `Design system decisions that affect multiple products belong in sos-hq` with `…belong in the hub repo`. Remove Datamural if present. |
| `guru.md` | Replace `For research that serves multiple products, place in sos-hq` with `…place in the hub repo`. |
| `pm.md` | Remove doubled ScoopedOut reference in strategic roadmap section. |
| `staff.md` | **Fix name inconsistency:** frontmatter says `name: staff-eng`, but all other specs refer to it as `staff`. Normalize to `staff` everywhere. |
| `qa.md` | Add `or equivalent per repo` after npm-specific pre-commit examples. |

---

## 3. Skill specs — per-file decisions

**Source:** `sos-hq/.cursor/skills/` → **Target:** `solo-os/skills/`

### 3a. 13 skills with `## GitHub workflow (ScoopedOut)` section

**Decision:** Replace the entire `## GitHub workflow (ScoopedOut)` section with a generalized `## GitHub workflow` section:

```markdown
## GitHub workflow

For Issues/Projects queries and updates, prefer `solo-os gh-list|gh-next|gh-update|gh-promote|gh-close` over ad hoc `gh issue` / `gh project` commands.

Follow `docs/governance/workflow-system.md` for the canonical workflow taxonomy, parent-relationship rules, and direct-to-build-loop guidance.
```

**Skills getting this treatment:**
10x-vision-sprint, build-loop-and-release-rhythm, customer-discovery-interview, customer-segment-and-access-map, go-to-market-experiments, idea-triage, mvp-scope-and-roadmap, opportunity-scanner, pr-faq-generator, pricing-and-unit-economics, problem-reframer, solution-probe-poc, solopreneur-business-plan

### 3b. 4 skills without the GitHub section

These need only governance path updates (`docs/governance/artifact-governance-spec.md` already uses relative paths in most cases):
competitive-intelligence-brief, market-and-audience-research, technical-research-brief, design-inspiration

### 3c. Per-file special cases

| File | Special action |
|------|---------------|
| `build-loop-and-release-rhythm/SKILL.md` | Extra bl-* CLI line: replace `python3 solo-os/scripts/solo_os.py bl-review\|...` with `solo-os bl-review\|...`. Replace `Default to simple mode for active Build Loop execution in ScoopedOut repos` with `Default to simple mode`. Remove `.cursorrules` reference (BL #18 territory). |
| `idea-triage/SKILL.md` | **Heaviest coupling.** Remove entire Repo Creation Protocol that references `ScoopedOutStudios` org, `sos-hq` artifact migration, and `sos.code-workspace`. Replace with generic: "Follow the Repo Creation Protocol in `docs/governance/artifact-governance-spec.md` if applicable." |
| `design-inspiration/SKILL.md` | Replace all `Datamural.io` / `Datamural` references with generic `your product` or `the target product`. Keep curated URL tables as-is. |

### 3d. reference.md files

Both `solopreneur-business-plan/reference.md` and `pr-faq-generator/reference.md` are **already org-agnostic**. Port as-is with no changes needed.

---

## 4. Commands — packaging decision

**Source:** `sos-hq/.cursor/commands/solo-os/` → **Target:** `solo-os/commands/`

**Decision:** Ship commands as copy-ready Markdown in `solo-os/commands/`. The `install-agents` / `install-skills` commands (or a broader `install` command) will copy these to the appropriate target.

### 4a. Changes needed

| File | Change |
|------|--------|
| `README.md` | Rewrite for public solo-os context. Reference `solo-os install-commands` for setup. |
| `daily-triage.md` | Replace `sos-hq/docs/governance/workflow-system.md` with `docs/governance/workflow-system.md`. |
| `idea-triage.md` | Replace `<repo-or-sos-hq>` with `<repo>`. |
| All others | No ScoopedOut-specific content found. Port as-is. |

### 4b. Prompts

**Decision:** Do NOT port prompts to the public repo. They are a legacy mirror of commands. The commands README will note that prompts are deprecated in favor of commands.

### 4c. `.cursorrules`

**Decision:** Do NOT port the full studio `.cursorrules`. Create a minimal `solo-os/.cursorrules.example` that references Solo OS conventions without studio-specific content. The full file is too broad and org-specific.

### 4d. `sync-cursor-assets.sh`

**Decision:** Do NOT port this script. Replace with `solo-os install-agents` and `solo-os install-skills` CLI commands.

---

## 5. New CLI commands

### `solo-os install-agents`

```
solo-os install-agents [--target ~/.cursor/agents] [--force]
```

- Copies all `.md` files from `solo-os/agents/` to the target directory
- Default target: `~/.cursor/agents/`
- `--force` overwrites existing files without prompting
- Reports count of files installed

### `solo-os install-skills`

```
solo-os install-skills [--target ~/.cursor/skills] [--force]
```

- Copies all skill folders from `solo-os/skills/` to the target directory
- Default target: `~/.cursor/skills/`
- `--force` overwrites existing
- Reports count of skills installed

### `solo-os install-commands`

```
solo-os install-commands [--target .cursor/commands/solo-os] [--force]
```

- Copies all command `.md` files from `solo-os/commands/` to the target directory
- Default target: `.cursor/commands/solo-os/` (project-local, not global)
- `--force` overwrites existing
- Reports count of commands installed

---

## 6. New/updated README files

| Location | Content |
|----------|---------|
| `solo-os/agents/README.md` | What agents are, how they work, `solo-os install-agents` usage, list of included agents with one-line descriptions |
| `solo-os/skills/README.md` | What skills are, how they work, `solo-os install-skills` usage, list of included skills with one-line descriptions |
| `solo-os/commands/README.md` | What commands are, how they work, `solo-os install-commands` usage, list of included commands |

---

## 7. Validation checklist

- [ ] `grep -r 'ScoopedOut\|sos-hq\|Datamural' solo-os/agents/ solo-os/skills/ solo-os/commands/` returns zero matches
- [ ] `grep -r 'python3 solo-os/scripts/solo_os.py' solo-os/agents/ solo-os/skills/ solo-os/commands/` returns zero matches
- [ ] `grep -r 'sos\.code-workspace' solo-os/agents/ solo-os/skills/ solo-os/commands/` returns zero matches
- [ ] `solo-os install-agents` copies all agent specs to target directory
- [ ] `solo-os install-skills` copies all skill folders to target directory
- [ ] `solo-os install-commands` copies all commands to target directory
- [ ] Each generalized spec reads coherently for a non-ScoopedOutStudios user
- [ ] No personal or business-sensitive content in any ported file
