---
name: build-loop-and-release-rhythm
description: Run a repeatable build-to-release loop with clear gates, minimal blockers, and measurable outcomes. Use when execution starts and during ongoing product iteration to prevent chaos and scope drift.
---

# Build Loop and Release Rhythm

## GitHub workflow

For Issues/Projects queries and updates, prefer `solo-os gh-list|gh-next|gh-update|gh-promote|gh-close` over ad hoc `gh issue` / `gh project` commands.

When worktrees are explicitly chosen, prefer `solo-os bl-review|bl-prepare|bl-status|bl-sync|bl-finish` over raw git worktree commands.

Default to simple mode for active Build Loop execution: stay in the current checkout on a dedicated branch unless isolated execution is clearly justified.

Follow `docs/governance/workflow-system.md` for the canonical workflow taxonomy, parent-relationship rules, and direct-to-build-loop guidance.

## Purpose
Provide a stable, low-chaos operating loop for building, shipping, and learning in short iterations.

## Trigger

Invoke this skill when:
- Creating a new build loop plan (run Checkpoint A).
- Declaring a build loop complete (run Checkpoint C).
- Preparing a release for external users (run Checkpoint B, if non-trivial).

The **cos** (Chief of Staff) agent is the default driver. Project rules should reference this skill in a "Build Loop Discipline" section so agents know to invoke it at loop boundaries.

## Use When
- You are ready to implement scoped work.
- Build execution is happening repeatedly across weeks.
- The team needs clear checkpoints without heavy process overhead.

## Execution Context (Resource Reality)
- The founder operates with advanced generative AI: autonomous agents, sub-agents, skills, and frontier models.
- AI-augmented execution capacity is high and elastic. Build loop cadence, slice sizing, and iteration speed should reflect AI-assisted productivity.
- Do not pad timelines or shrink scope assuming traditional manual development velocity. AI agents can implement, test, and iterate rapidly.
- The binding constraints are decision quality, release confidence, and customer feedback loops — not implementation throughput.

## Workflow
1. Checkpoint A: run `bl-review` and confirm goal, why now, scope, non-goals, risk tier, validation plan, and learning question.
2. Choose execution mode: `simple mode` by default; use isolated worktree mode only when stronger isolation is worth the friction.
3. Execution loop:
   - simple mode: build, test, and integrate in the current checkout on a dedicated branch
   - isolated mode: run `bl-prepare` and execute inside the returned managed `worktree_path`
4. During isolated-mode execution: use `bl-status` for visibility and `bl-sync` for upstream integration at the right cadence.
5. Checkpoint B: apply the required validation depth for the loop's risk tier and make a release decision.
6. Finish execution:
   - simple mode: merge using the normal repo flow after approval
   - isolated mode: use `bl-finish` for controlled merge-back after Checkpoint B is satisfied
7. Checkpoint C: capture outcome, product learning, and quality/process learning.
8. Feed outcomes back into the next build loop, experiments, and economics artifacts when relevant.

## Canonical Build Loop Shape

Every Build Loop should contain:
- goal
- why now
- scope
- non-goals
- parent linkage (`Roadmap` and/or `Idea`) when applicable
- demoable output
- risk tier
- validation plan
- release/rollback plan
- learning question / success signal
- evidence links (commits, PRs, artifacts)

## Execution Mode Rules

- Do not start execution without an explicit repo + issue reference.
- Default to `simple mode` while context continuity and manual orchestration still matter more than isolation.
- In simple mode, keep the loop on a dedicated branch and avoid mixing unrelated work.
- Once `bl-prepare` returns a `worktree_path`, all isolated-mode Build Loop code edits, upstream sync, and conflict resolution happen only inside that managed worktree.

## Risk Tiers

Use the canonical tiers from `docs/governance/build-loop-and-release-rhythm.md`:
- `Low`
- `Medium`
- `High`
- `Critical`

Use the lowest honest tier. Escalate if the blast radius, trust sensitivity, or rollback complexity is unclear.

## Required Output
- Current iteration goal
- Why now
- In-scope vs out-of-scope
- Risk tier
- Validation plan
- Build slice plan (ordered tasks)
- Gate decisions:
  - intake: proceed/hold
  - release: ship/ship with conditions/hold
  - post-release: continue/pivot/stop
- Next checkpoint date and owner
- Product learning and quality/process learning at Checkpoint C

## Checkpoints (Minimal Set)
- Checkpoint A: intake approved (scope + metric clear)
- Checkpoint B: release decision (risk managed)
- Checkpoint C: post-release learning decision
  - For external-facing loops: include a **release quality retrospective** — what broke during the release window, what was missed by QA, and what to feed into the next loop's QA checklist. Have `qa` review if available.

Use only these three by default. Add more only for high-risk work.

### Checkpoint A output

- goal
- why now
- scope
- non-goals
- risk tier
- planned validation
- learning question / success signal

### Checkpoint B output

- what was validated
- defects/gaps
- release decision
- rollback readiness
- monitoring/observation window

### Checkpoint C output

- outcome vs goal
- product learning
- quality/process learning
- regressions or escaped defects
- next-loop implications

## Artifact Rules
- Primary folder: `agent_generated/plans/` for iteration plan and checkpoints
- Cross-links:
  - `agent_generated/experiments/` for outcome metrics/learning decisions
  - `agent_generated/economics/` when viability assumptions shift
- Artifact class: `decision` for iteration plans and gate outcomes
- Include required metadata from `docs/governance/artifact-governance-spec.md`.
- May create/edit `draft` artifacts only.
- Never overwrite `approved` artifacts in place.
- Material changes require new version + `supersedes`.
- Keep `LATEST.md` and `_index.md` pointer/registry-only when they exist; do not turn them into status boards or pipeline trackers.
- Track active workflow state in GitHub Projects/Issues, not in markdown artifacts.

## Sub-agent Handoffs
- `cos`: orchestrate cross-functional sequence and conflict resolution.
- `staff`: implementation feasibility, architecture, and slicing.
- `qa`: release readiness and rollback safety.
- `sec`: trust/privacy checks for sensitive surfaces.
- `pm`: scope discipline and outcome alignment.
- Optionally invoke `growth` for post-release metrics when the product has meaningful funnel data and the founder wants a growth readout.
- cos runs the artifact governance checklist per spec; optionally invoke `agm` for dedicated reviews.

### Routing by risk

- `Low` internal-only loops: `pm` / `staff` is usually enough.
- `Medium` external-facing loops: add `qa`.
- `High` / `Critical` loops: add `qa`; add `sec` for auth, payments, privacy, production data integrity, or trust-sensitive changes.

## Depth and Token Guidance
- Default output target: 1200-2100 words for build-loop planning and checkpoint decisions.
- High-risk releases or conflicting specialist signals may expand to 3000 words.
- Preserve depth on gate rationale, blockers, and mitigation plans.
- Use layered output: checkpoint decisions first, then execution and risk detail.

## Implementation-Complete Mode
- When the active step is coding/implementation, prioritize delivery completeness over token compactness.
- Do not reduce technical quality, test coverage intent, or risk handling because of output length targets.
- If implementation scope is large, break delivery into explicit slices with checkpoints rather than shortening necessary technical work.
- Maintain checkpoint discipline (A/B/C), but avoid extra approvals unless risk level justifies them.

## Pre-Revenue Lite Mode

For pre-revenue projects with <100 users, use a lighter checkpoint profile:

- **Checkpoint A:** Required. 3 lines: goal, scope, metric. ~2 minutes.
- **Checkpoint B:** Lightweight only for `Low` internal loops where branch validation history is already clean and rollback is simple.
  - **Exception — external-facing loops:** If the loop ships to non-founder users (ICP outreach, public demos, beta invites), invoke `qa` for a scoped release readiness check: core flow validation, smoke test pass, share/embed/landing checks, known-issues list.
- **Checkpoint C:** Required. Learning note + next-plan update decision.
  - Include a "release quality retrospective" line: what broke, what was missed, feed into next loop.
- Skip sub-agent handoffs to `sec` unless the loop touches auth, PII, or payment.
- Skip sub-agent handoffs to `qa` only for honest `Low` internal-only loops. Invoke for any **external-facing** release (see Checkpoint B exception above).

Graduate to the full checkpoint profile when the product has paying users or public exposure (e.g., Product Hunt launch).

## Pipeline Maintenance

Maintain a queue of 2-3 execution-ready plans ahead of the active loop:

- At every **Checkpoint C**, ensure at least 2 plans are queued. If the queue drops to 1, draft the next plan.
- Each queued plan includes a **Review Pre-Step** section (below). Run this checklist before Checkpoint A when activating a queued plan.
- Track the active loop, queued plans, and related roadmap/build-loop state in GitHub Projects/Issues. If `LATEST.md` exists, keep it as a pointer-only file to the active canonical plan.
- Feed release-quality/process learning from the current loop into the next queued loop's validation plan.

### Review Pre-Step Template

Include this section at the top of every queued plan (after metadata, before the task list). The cos (Chief of Staff) runs it when transitioning to the next loop:

```markdown
## Review Pre-Step (run before Checkpoint A)

### Previous loop outcomes
- **Previous loop:** [BL{NN} name]
- **Goal achieved?** Yes / Partially / No — [1 sentence]
- **Key learnings:** [2-3 bullets from Checkpoint C of previous loop]
- **Metric moved?** [What metric, by how much, or "no metric yet"]

### Plan validity check
- [ ] Do the assumptions in this plan still hold given previous loop outcomes?
- [ ] Has the roadmap changed since this plan was drafted? (Check roadmap updated_at)
- [ ] Are there new blockers or dependencies surfaced by the previous loop?
- [ ] Does the scope still represent the smallest valuable increment?

### Decision
- **Minor adjustments needed:** [list changes] → Apply and proceed. Update plan version (minor bump).
- **Major changes needed:** [describe] → Flag for founder re-approval before proceeding. Create new plan version (major bump).
- **Plan is still valid as-is:** → Proceed to Checkpoint A.
```

## Plan Naming Convention

Build loop plans use a sequential prefix for chronological ordering:

- **Build loops:** `BL{NN}-{descriptive-name}-v{X}.md` (e.g., `BL05-domain-and-phase2-kickoff-v1.md`)
- **Reference docs:** `{descriptive-name}-v{X}.md` (roadmap, registry, brand — no prefix)
- Counter is creation-order; do not renumber. Superseded loops keep their number.

## Guardrails
- One active build slice at a time unless user explicitly approves parallel tracks.
- No scope expansion mid-iteration without checkpoint approval.
- If release risk is P0 or unresolved Hold appears, do not ship.
- If no metric moved, require explicit learning note before next build loop.
