---
name: mvp-scope-and-roadmap
description: Define a ruthlessly scoped MVP and phased roadmap with explicit non-goals. Use when discovery evidence supports execution and the user needs a smallest-valuable build plan.
---

# MVP Scope and Roadmap

## GitHub workflow

For Issues/Projects queries and updates, prefer `solo-os gh-list|gh-next|gh-update|gh-promote|gh-close` over ad hoc `gh issue` / `gh project` commands.

Follow `docs/governance/workflow-system.md` for the canonical workflow taxonomy, parent-relationship rules, and direct-to-build-loop guidance.

## Purpose
Convert validated customer evidence into a smallest-valuable product scope and delivery sequence.

## Use When
- Discovery evidence is sufficient to start building.
- Scope feels too broad and needs reduction.
- The user asks for MVP definition, milestones, or non-goals.

## Execution Context (Resource Reality)
- The founder operates with advanced generative AI: autonomous agents, sub-agents, skills, and frontier models.
- AI-augmented execution capacity is high and elastic. Scope and phasing decisions should reflect AI-assisted build speed, not traditional manual estimates.
- "Too complex to build" is rarely a valid scope-cut justification. Scope cuts should be driven by customer value priority and learning sequence, not build effort fear.
- The binding constraints are customer evidence quality, risk, and strategic focus — not implementation bandwidth.

## Workflow
1. Restate customer/problem evidence and outcome target.
2. Define MVP scope (must-have), non-goals (explicitly out). **Non-goals must be justified by customer value or learning priority, not effort avoidance.**
3. Sequence milestones by dependency and learning value.
4. Identify top risks and risk-reduction steps.
5. Produce phased roadmap with clear "build now vs later."

## Required Output
- MVP scope
- Non-goals
- Milestones (Phase 1, 2, 3)
- Decision gate: build now / reduce scope / defer

## Artifact Rules
- Primary folder: `agent_generated/plans/`
- Artifact class: `decision` or `canonical` for active roadmap/MVP docs.
- Include required metadata for decision/canonical docs.
- May create/edit `draft` artifacts only.
- Never overwrite `approved` artifacts in place.
- Major version bump required for material scope/assumption changes.
- If the repo still uses compatibility pointers, update `agent_generated/plans/LATEST.md` and `_index.md` for canonical promotions while keeping them pointer/registry-only.

## Sub-agent Handoffs
- `product-manager`: confirm roadmap alignment and prioritization quality.
- `staff-engineer`: validate feasibility, sequencing, and technical risk.
- `security-privacy-engineer`: review trust/privacy implications of scoped features.
- `qa-release-manager`: verify release-readiness expectations for phased delivery.
- `artifact-governance-manager`: enforce artifact lifecycle and placement rules.

## Depth and Token Guidance
- Default output target: 1200-2100 words for meaningful scope and sequencing decisions.
- High-risk or high-uncertainty scope tradeoffs may expand to 3000 words.
- Preserve rationale depth for non-goals, sequencing, and risk mitigations.
- Use layered output: executive scope summary, then milestone/risk detail.

## Guardrails
- Keep MVP narrow; avoid bundling optional features.
- Every milestone must map to measurable customer or business outcome.
- If roadmap direction changes, require explicit user confirmation.
