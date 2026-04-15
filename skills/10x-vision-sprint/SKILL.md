---
name: 10x-vision-sprint
description: Given a validated problem, imagine the most ambitious possible solution (the 10x version), then work backward to the smallest version that captures the core magic. Use when discovery confirms a real problem but the user wants to think bigger, the MVP feels uninspiring, or exploring platform potential.
---

# 10x Vision Sprint

## GitHub workflow

For Issues/Projects queries and updates, prefer `solo-os gh-list|gh-next|gh-update|gh-promote|gh-close` over ad hoc `gh issue` / `gh project` commands.

Follow `docs/governance/workflow-system.md` for the canonical workflow taxonomy, parent-relationship rules, and direct-to-build-loop guidance.

## Purpose
Imagine the most ambitious possible solution to a validated problem, distill the "core magic" that makes it fundamentally better, then work backward to the smallest version that still delivers that magic.

## Use When
- Discovery confirms a real problem but the user wants to think bigger before scoping.
- The MVP feels uninspiring and needs a north star to guide it.
- Exploring whether a validated niche problem could become a platform play.
- The user asks "what's the biggest version of this?" or "what's the dream product?"
- Need to align the team on long-term vision before cutting scope for v1.

## Execution Context (Resource Reality)
- The founder operates with advanced generative AI: autonomous agents, sub-agents, skills, and frontier models.
- The 10x vision should leverage AI capabilities as a core enabler — not just incremental automation, but fundamentally new experiences AI makes possible.
- Do not limit the vision based on current team size. AI-augmented execution means ambitious technical scope is achievable if validated.
- The smallest-magic version should still be buildable rapidly with AI-assisted development.

## Workflow
1. Restate the validated problem and user evidence:
   - Who is the user? What problem is confirmed?
   - What evidence supports this? (discovery data, interviews, POC feedback)
   - What is the current MVP scope (if any)?
2. Remove all constraints — imagine the ideal 10x solution:
   - What would the perfect experience look like with unlimited resources?
   - What would make users say "I can't believe this exists" or "I can't go back to the old way"?
   - What would make this a category-defining product, not just a good one?
   - How would AI capabilities amplify the experience beyond what's currently imaginable?
3. Identify the "core magic":
   - What makes the 10x version fundamentally better, not just bigger?
   - What is the single most compelling moment in the user experience?
   - Strip away features — what is the irreducible essence that creates the "wow"?
4. Work backward to the smallest-magic version:
   - What is the minimum product that still delivers the core magic?
   - What can be manual, ugly, or incomplete and still preserve the wow moment?
   - How does this differ from the current MVP scope?
5. Define the gap between smallest-magic and current MVP:
   - What is the current MVP missing that the smallest-magic version has?
   - What should be added, changed, or resequenced?
6. Propose a staged path from MVP to 10x:
   - 3-5 stages with clear validation gates between each
   - Each stage should deliver incremental user value while building toward the vision
   - Identify which stages require new capabilities, partnerships, or data

## Required Output
- Validated problem restatement (with evidence)
- 10x vision description (the dream product)
- Core magic distillation (the irreducible wow)
- Smallest-magic MVP (minimum product that delivers the core magic)
- Gap analysis (smallest-magic vs current MVP)
- Staged path from MVP to 10x (3-5 stages with gates)
- Top risks to the vision and how each stage mitigates them

## Artifact Rules
- Primary folder: `agent_generated/plans/` (vision documents inform roadmap).
- Artifact class: `decision` when the vision shapes strategic direction and MVP scope.
- Include metadata header: title, artifact_type, status (draft/approved/superseded), version, owner, created_at.
- May create/edit `draft` artifacts only.
- Never overwrite `approved` artifacts in place.
- Material updates require new version + `supersedes`.
- Cross-reference the discovery/validation artifacts that support the problem evidence.
- If the repo still uses compatibility pointers, update `agent_generated/plans/LATEST.md` when a vision doc becomes the active north star, while keeping it pointer-only.

## Sub-agent Handoffs
- `big-thinker`: primary agent that drives this skill — provides visionary lens and creative ambition.
- `mvp-scope-and-roadmap`: for formal scoping of the smallest-magic MVP.
- `product-manager`: for roadmap alignment and staged delivery planning.
- `staff-engineer`: for feasibility assessment of technically ambitious vision elements.
- `solution-probe-poc`: when the core magic needs a quick prototype to validate desirability.
- Apply artifact governance rules (metadata, placement, version) before finalizing artifacts.

## Depth and Token Guidance
- Default output target: 1200-2100 words for meaningful vision development and backward reasoning.
- High-ambiguity visions or complex platform-play analysis may expand to 3000 words.
- Prioritize depth on core magic distillation and smallest-magic MVP definition over exhaustive 10x feature lists.
- Use layered output: core magic and smallest-magic MVP first, then full 10x vision and staged path.

## Guardrails
- Require validated problem evidence before running a vision sprint. Do not vision-sprint on unvalidated ideas.
- The 10x vision must be grounded in user need, not technology fascination. "Cool tech" without user pull is not a valid 10x.
- The smallest-magic version must be meaningfully different from a standard MVP — it should preserve the wow, not just be "small."
- Every stage in the path from MVP to 10x must have a clear validation gate — no assumed progression.
- Do not scope or estimate the stages in detail; hand off to `mvp-scope-and-roadmap` and `staff-engineer`.
- If the validated evidence is weak, recommend more discovery before running a vision sprint.
