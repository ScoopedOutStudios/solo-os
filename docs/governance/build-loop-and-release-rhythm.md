# Build Loop and Release Rhythm

title: Build Loop and Release Rhythm
artifact_type: canonical
status: approved
version: v1.0
owner: studio
created_at: 2026-02-19
updated_at: 2026-03-25
project: solo-os
supersedes: docs/governance/build-loop-and-release-rhythm.md#v0.2

## 1) Purpose

Define the canonical structure for `Build Loop` execution so every loop has clear scope, right-sized validation, explicit release decisions, and captured learning.

## 2) Scope

Applies whenever a `Build Loop` is created or executed in repos managed by Solo OS, whether it is product-facing, internal-only, or studio-ops/tooling work.

## 3) Relationship To Other Governance Docs

- `docs/governance/workflow-system.md` defines the canonical workflow taxonomy and where `Build Loop` fits.
- `docs/governance/git-commit-protocol.md` defines commit discipline and per-commit validation rules.
- This document defines what a `Build Loop` must contain and what must happen at Checkpoints A, B, and C.

### 3.1) Open-source CLI reality check (this repository)

The governance in this document describes the **full operating model** Solo OS is designed to support over time.

The **Python CLI shipped in this repo** (see `solo-os --help`) is intentionally narrower: it is strong at **GitHub Project operations**, **daily triage**, and **Checkpoint A review** (`bl-review`), but it does **not** currently ship `bl-prepare`, `bl-sync`, or `bl-finish` helpers.

If you need isolated worktree execution today, use normal `git worktree` workflows and your repo’s validation commands, and keep the Build Loop issue as the source of truth for scope, risk tier, and checkpoint notes.

## 4) Canonical Build Loop Shape

Every `Build Loop` should contain or link to the following:

1. **Goal**
  - One primary outcome in plain language.
2. **Why now**
  - Why this loop should exist now instead of later.
3. **Scope**
  - In-scope work only.
4. **Non-goals**
  - Explicitly out-of-scope work to prevent drift.
5. **Parent linkage**
  - Related `Roadmap` and/or `Idea` when applicable.
6. **Demoable output**
  - What concrete thing should exist by the end of the loop.
7. **Risk tier**
  - `Low`, `Medium`, `High`, or `Critical`.
8. **Validation plan**
  - What checks prove the loop is good enough for Checkpoint B.
9. **Release / rollback plan**
  - How it will ship safely and how it can be reverted.
10. **Learning question / success signal**
  - What the team expects to learn or improve.
11. **Evidence links**
  - Commits, PRs, notes, test output, demo links, release notes, or follow-up artifacts.

## 5) Default Build Loop Flow

1. **Checkpoint A: intake and structure**
  - Confirm goal, why now, scope, non-goals, risk tier, validation plan, and learning question.
  - Start from the Build Loop body template (`solo-os build-loop-template`) so the GitHub issue is self-sufficient.
2. **Execution cycle**
  - Build one active slice at a time by default.
  - Track blockers and active state in GitHub Projects/Issues, not in markdown status boards.
  - Default to `simple mode`: use the current checkout on a dedicated branch when that keeps orchestration and context continuity easier.
  - Use `isolated mode` only when local isolation is worth the friction, for example parallel loops, risky refactors, or messy local state.
3. **Checkpoint B: release gate**
  - Validate to the required depth for the loop's risk tier.
  - Decide `Ship`, `Ship with Conditions`, or `Hold`.
  - Mark the Build Loop `Ready To Merge` only after Checkpoint B is complete and merge approval is granted.
4. **Checkpoint C: measure and learn**
  - Record outcome, quality misses, regressions, and next-loop implications.
  - Decide `Continue`, `Pivot`, or `Stop`.

## 6) Risk Tiers

Use the lowest tier that honestly matches the loop:

- **Low**
  - Internal-only engineering, tooling, cleanup, or low-blast-radius changes.
- **Medium**
  - User-visible but reversible changes with limited blast radius.
- **High**
  - Critical user flows, broad surface-area changes, or changes with meaningful trust/reliability risk.
- **Critical**
  - Auth, payments, privacy, production data integrity, or high-blast-radius release changes.

## 7) Validation Matrix


| Risk tier | Minimum Checkpoint B validation                                                                                                                                                       | QA required                                                       | Security required                             | Rollback requirement                            |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------- | ----------------------------------------------- |
| Low       | Confirm branch passed required pre-commit checks; targeted smoke check of the changed flow                                                                                            | Optional                                                          | No                                            | Simple rollback path noted                      |
| Medium    | Targeted smoke + targeted regression on affected flow(s); verify known failure paths                                                                                                  | Recommended for external-facing loops; optional for internal-only | Optional unless trust-sensitive               | Explicit rollback trigger + owner               |
| High      | Re-run critical automated checks, targeted/manual regression, release checklist, and monitoring plan                                                                                  | Required                                                          | Required if auth, privacy, or trust-sensitive | Explicit rollback steps + monitoring window     |
| Critical  | Full release review: critical automated checks, regression/E2E where available, rollback rehearsal or equivalent confidence, release checklist, monitoring owner, known-issues review | Required                                                          | Required                                      | Fast rollback path must be explicit and trusted |


## 8) Checkpoint Outputs

### Checkpoint A

Required output:

- goal
- why now
- scope
- non-goals
- parent linkage (if any)
- demoable output
- risk tier
- planned validation
- learning question / success signal

### Checkpoint B

Required output:

- what was actually validated
- open defects or known limitations
- release decision: `Ship` / `Ship with Conditions` / `Hold`
- rollback readiness
- monitoring or observation window
- who owns the release watch

### Checkpoint C

Required output:

- outcome vs original goal
- what shipped and what did not
- product learning
- quality learning
- regressions or escaped defects
- what changes in the next loop
- final decision: `Continue` / `Pivot` / `Stop`

## 9) Release Profiles

### Internal-only build loops

- Usually `Low` or `Medium` risk.
- `qa` is optional for `Low`; use `qa` if the loop changes shared tooling, release infrastructure, or brittle core workflows.
- Checkpoint B can stay lightweight if the loop is reversible and branch validation is already clean.

### External-facing product loops

- At least `Medium` risk unless the change is trivial.
- `qa` is required for `Medium+` loops shipping to non-founder users.
- Include a release quality retrospective at Checkpoint C.

### High-risk or critical loops

- Always involve `qa`.
- Involve `sec` when auth, payments, privacy, or trust-sensitive surfaces are touched.
- Require explicit rollback steps and a defined monitoring owner before `Ship`.

## 10) Git Commit Checkpoints

Each checkpoint has explicit git expectations:


| Checkpoint       | Git Action                                                              | Validation expectation                                                        |
| ---------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| A (Intake)       | Create feature branch `agent/{artifact-ref}/{brief-desc}` if not exists | N/A                                                                           |
| During Execution | Commit after each logical unit of work                                  | Run all required pre-commit checks for the repo                               |
| B (Release)      | Merge or prepare to merge only after risk-tier validation is complete   | Confirm branch validation history + required release validation for risk tier |
| C (Learning)     | Tag release if shipped, when appropriate                                | N/A                                                                           |


## 11) Execution Modes

There are two valid Build Loop execution modes:

### Simple mode (default)

Use when:

- only one Build Loop is active
- manual orchestration and thread/context continuity matter more than isolation
- the repo is not carrying unrelated local work that would create confusion

Rules:

- create or use a dedicated branch for the loop
- keep unrelated work out of that branch
- use `bl-review` for Checkpoint A readiness
- run normal repo validation and manual checks in the current checkout
- stop for explicit Checkpoint B approval before merge-back

Simple mode is the default because it minimizes execution friction while the operating system is still being learned and manually orchestrated.

### Isolated mode (explicit worktree path)

Use when:

- parallel loops are active or likely
- the repo already has unrelated local changes you do not want mixed in
- the loop is risky enough that stronger isolation is worth the overhead
- you want a clean dedicated workspace for a larger refactor

Use worktrees as an execution mechanism, not as a second planning system:

- default posture is still one active managed worktree at a time
- parallel worktrees are an explicit exception for independent loops, not the starting posture
- each active isolated-mode `Build Loop` should map to one dedicated branch and one dedicated worktree path
- do not reuse the same worktree for unrelated loops just because it is convenient
- if a loop is complete, merge or archive it, then remove the worktree

Recommended branch/path convention:

- Branch: `agent/<artifact-ref>/<slug>`
- Worktree path: `.worktrees/<repo>/<artifact-ref>-<slug>`

Recommended Solo OS orchestration flow for isolated mode:

1. `solo-os bl-review` for Checkpoint A readiness (or validate the issue body manually against the canonical template)
2. Create or reuse a dedicated worktree using `git worktree` (or an organization-specific wrapper, if you have one)
3. Execute inside the dedicated worktree path
4. Sync/rebase at the recommended cadence during execution
5. Finish/merge only after Checkpoint B conditions are satisfied (merge using your repo’s normal PR/merge flow)

Merge-back protocol for isolated mode:

- default to rebasing the Build Loop branch onto latest `main` during sync for agent-owned temporary branches
- resolve conflicts inside the Build Loop worktree, never in the main checkout
- re-run required repo checks after any conflict resolution or material branch sync
- merge back to `main` only when the branch is current, validated, the issue status is `Ready To Merge`, and Checkpoint B is satisfied with a release decision of `Ship` or `Ship with Conditions`
- after merge-back or explicit abandonment, remove the managed worktree and clean up the branch according to the chosen finish flow

Recommended sync cadence:

- at the start of a new work session
- before starting a new logical unit when upstream changes may have landed
- before final merge-back
- more aggressively when parallel Build Loops in the same repo may overlap

## 12) Learning And Regression Loop

Checkpoint C must capture two kinds of learning:

1. **Product learning**
  - Did the loop move the intended user or business signal?
2. **Quality/process learning**
  - What broke?
  - What was missed by testing?
  - What should be added to the next loop's QA checklist or release plan?

Every external-facing loop should include a lightweight **release quality retrospective**:

- escaped defects
- missed validation
- checklist/process improvement for the next loop

Feed quality learning into:

- the next loop's Checkpoint A validation plan
- the Review Pre-Step for queued loops
- test automation backlog only when repeated manual checks create real drag

## 13) Required Artifacts

- Required artifacts per cycle:
  - build loop plan / checkpoint A record (in the GitHub issue body)
  - release gate decision note / checkpoint B record
  - post-release learning note / checkpoint C record
- Keep active loop, roadmap, and build-loop state in GitHub Projects/Issues.

## 14) Approval Policy

- User approval required for:
  - major scope expansion
  - roadmap direction change
  - unresolved `High` / `Critical` risk acceptance
- No extra approval required for:
  - normal draft updates within scope
  - minor sequencing changes that preserve goals/non-goals
  - expected in-cycle implementation adjustments

## 15) Anti-Chaos Rules

- One active build slice at a time unless explicitly approved otherwise.
- No scope expansion mid-loop without revisiting Checkpoint A.
- Do not let a `Build Loop` become a vague umbrella with no demoable output.
- If an agent returns `Hold` with P0 or unresolved `Critical` risk, do not ship.
- If no meaningful learning was captured, do not open the next loop as if the current one taught nothing.

## 15) Trigger Prompt (Recommended)

Use:

`Use chief-of-staff to run the build loop for this scoped slice. Enforce checkpoints A/B/C, set an honest risk tier, define the validation plan, and capture product + quality learning for the next loop.`