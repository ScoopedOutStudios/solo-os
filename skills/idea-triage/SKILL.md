---
name: idea-triage
description: Evaluate early-stage ideas quickly with a go/park/kill decision and explicit assumptions. Use when a new product idea, feature concept, or opportunity is proposed and needs fast prioritization before discovery.
---

# Idea Triage

## GitHub workflow

For Issues/Projects queries and updates, prefer `solo-os gh-list|gh-next|gh-update|gh-promote|gh-close` over ad hoc `gh issue` / `gh project` commands.

Follow `docs/governance/workflow-system.md` for the canonical workflow taxonomy, parent-relationship rules, and direct-to-build-loop guidance.

## Purpose
Decide quickly whether an idea should move to discovery now, be parked, or be killed.

## Use When
- A new idea is proposed and priority is unclear.
- The user asks "is this worth pursuing?"
- The backlog has too many unvalidated ideas.

## Execution Context (Resource Reality)
- The founder operates with advanced generative AI: autonomous agents, sub-agents, skills, and frontier models.
- AI-augmented execution capacity is high and elastic. When scoring **effort**, reflect AI-assisted development speed — not manual solo-developer estimates.
- Do not let implementation complexity alone drive a `Park` or `Kill` decision. If impact and confidence are strong, AI resources can handle significant build scope.
- The binding constraints for triage are customer signal strength, strategic fit, and decision quality — not raw dev bandwidth.

## Workflow
1. Define the idea in one sentence (problem, user, expected value).
2. Score quickly on impact, confidence, and effort (high/medium/low is enough). **Effort scores must reflect AI-augmented execution capacity.**
3. Identify top assumptions and biggest unknown.
4. Decide: `Go`, `Park`, or `Kill`.
5. If `Go`, create a dedicated product repo before any discovery work:
   - Follow the repo creation protocol if applicable.
6. If `Go`, hand off to `customer-discovery-interview`.

## Required Output
- Decision: `Go` / `Park` / `Kill`
- Reason: one paragraph max
- Top 3 assumptions
- Next step (if `Go`, include discovery question to answer first)

## Artifact Rules
- Primary folder: `agent_generated/ideas/`
- Artifact class: usually `decision` (or `ephemeral` for scratch notes)
- If decision-impacting, include metadata header: title, artifact_type, status (draft/approved/superseded), version, owner, created_at.
- May create/edit `draft` artifacts only.
- Never overwrite `approved` artifacts in place.
- Material updates require new version + `supersedes`.
- If this becomes canonical criteria and the repo still uses compatibility pointers, update `agent_generated/ideas/LATEST.md` and `agent_generated/_index.md` as pointer/registry-only surfaces.

## Sub-agent Handoffs
- `product-manager`: confirm roadmap fit and priority.
- Apply artifact governance rules (metadata, placement, version) before finalizing artifacts.
- `cos`: only if cross-functional conflicts need arbitration.

## Depth and Token Guidance
- Default output target: 1050-1800 words when decisions are non-trivial.
- High-ambiguity or high-stakes triage may expand to 2700 words.
- Prioritize depth on assumptions, risks, and decision rationale over brevity.
- Use layered output: short decision summary first, then supporting analysis.

## Guardrails
- Keep triage lightweight; do not run deep planning at this stage.
- Do not promote to build planning without at least one explicit unknown to validate.
- If idea is out of roadmap scope, require user confirmation before `Go`.
