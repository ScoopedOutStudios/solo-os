# Workflow System (Solo OS)

This document is a **governance-level** view of the Solo OS workflow.

For the full canonical model (including anti-patterns and edge cases), read [`../workflow-spec.md`](../workflow-spec.md).

## Core workflow hierarchy (tracked in GitHub)

- **Idea** (`Kind: Idea`) — hypothesis / opportunity, triaged to Go / Park / Kill
- **Roadmap** (`Kind: Roadmap`) — a committed bet or outcome
- **Build Loop** (`Kind: Build Loop`) — bounded execution slice with a demoable output

Solo OS intentionally keeps the active workflow state in **GitHub Projects + Issues**, not long-lived markdown “status boards” in random folders.

## Project fields (defaults)

- **Kind:** `Idea`, `Roadmap`, `Build Loop`
- **Status:** `Todo`, `Prioritized`, `Backlog`, `Blocked`, `In Progress`, `Done`
- **Stage (timebox):** `Inbox`, `Today`, `This Week`, `Waiting`

## Key rules

- **Do not** use Roadmap as a generic task bucket. Roadmap is for committed strategy bets, not “misc work”.
- **Do not** create Build Loops for vague, never-ending work. A Build Loop must have a concrete, demoable output.
- You may use **Direct-to-Build-Loop** when the main risk is execution discipline, not strategy uncertainty (see `../workflow-spec.md`).

## CLI primitives (as shipped in this repository)

- Query/update items on a GitHub Project: `solo-os gh-list|gh-next|gh-brief|gh-update|gh-promote|gh-close|gh-migrate-titles|gh-create`
- Daily focus: `solo-os daily-triage`
- Build loop intake: `solo-os bl-review` and `solo-os build-loop-template`

> Note: Some AI assets in `skills/`, `commands/`, and `agents/` may reference future or optional orchestration features. The Python CLI in this repo is the most reliable “what exists right now” surface.