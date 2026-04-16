---
name: problem-reframer
description: Take an existing problem, product, or stuck build loop and generate alternative framings that unlock new solution spaces. Use when an idea got Park/Kill, discovery revealed the original framing was wrong, engagement is flat, or the user feels stuck on how to think about a problem.
---

# Problem Reframer

## GitHub workflow

For Issues/Projects queries and updates, prefer `solo-os gh-list|gh-next|gh-update|gh-promote|gh-close` over ad hoc `gh issue` / `gh project` commands.

Follow `docs/governance/workflow-system.md` for the canonical workflow taxonomy, parent-relationship rules, and direct-to-build-loop guidance.

## Purpose
Generate alternative problem framings that unlock new solution spaces, user segments, or value propositions when the current framing is stuck, invalidated, or limiting.

## Use When
- An idea got "Park" or "Kill" and the user wants to explore angles before abandoning.
- Discovery interviews reveal the original problem framing was wrong or incomplete.
- A product exists but engagement is flat — need to rethink the core value proposition.
- The user says "I feel like we're thinking about this wrong."
- A promising domain has no clear product angle yet.

## Execution Context (Resource Reality)
- The founder operates with advanced generative AI: autonomous agents, sub-agents, skills, and frontier models.
- Reframing should not be constrained by build effort. If a different framing leads to a more valuable product, AI-augmented execution can handle the pivot.
- Consider framings that leverage AI capabilities as a core differentiator — what problem framings become tractable because of AI that weren't before?

## Workflow
1. State the current problem framing explicitly:
   - Who is the user?
   - What problem are we solving?
   - What is the current value proposition?
   - Why is it stuck or invalidated? (evidence)
2. Apply reframing lenses systematically:
   - **Different user segment**: Who else has this pain? Who has it worse? Who would pay more?
   - **Different job-to-be-done**: What if the real job is upstream (before the problem) or downstream (after)?
   - **Inversion**: What if we solved the opposite problem? What if we removed the need entirely?
   - **Constraint removal**: What if [key constraint] didn't exist? What does AI make possible that wasn't before?
   - **Analogy transfer**: How does [another domain] solve a structurally similar problem?
   - **Stakeholder shift**: What if we served the buyer instead of the user (or vice versa)?
   - **Scope shift**: What if the problem is actually much bigger (platform) or much smaller (wedge)?
3. Generate 3-5 alternative framings, each with:
   - Reframed problem statement
   - Target user/segment
   - Distinct value hypothesis
   - Why this framing might be better than the original
4. Identify which reframing changes the riskiest assumption from the original framing.
5. Recommend which framing to test first and why (strongest signal, fastest to validate, or highest upside).

## Required Output
- Current framing (explicit statement of what's stuck and why)
- Alternative framings (3-5) each with:
  - Reframed problem statement
  - Target user
  - Value hypothesis
  - Key advantage over original framing
- Recommended framing to test first with rationale
- Proposed validation step for the recommended framing

## Artifact Rules
- Primary folder: `agent_generated/discovery/` (reframings are pre-validation).
- Artifact class: `decision` when the reframing changes strategic direction, `ephemeral` for exploratory drafts.
- Include metadata header: title, artifact_type, status (draft/approved/superseded), version, owner, created_at.
- May create/edit `draft` artifacts only.
- Never overwrite `approved` artifacts in place.
- Material updates require new version + `supersedes`.
- Cross-reference the originating idea/triage artifact that triggered the reframing.

## Sub-agent Handoffs
- `big_thinker`: primary agent that drives this skill — provides creative reframing lens.
- `idea-triage`: if reframing produces a substantially new idea, run it through triage.
- `customer-discovery-interview`: when the recommended reframing needs customer validation.
- `product-manager`: when reframing implies a strategic pivot or roadmap change.
- Apply artifact governance rules (metadata, placement, version) before finalizing artifacts.

## Depth and Token Guidance
- Default output target: 1050-1800 words for meaningful reframing with supporting rationale.
- Complex multi-lens reframings or pivots with significant strategic implications may expand to 2700 words.
- Prioritize depth on reframing rationale and why each alternative is distinct, not on restating background.
- Use layered output: recommended framing and validation step first, then full set of alternatives.

## Guardrails
- Always state the current framing explicitly before generating alternatives — no reframing without a baseline.
- Every alternative framing must have a distinct value hypothesis, not just a rephrased version of the original.
- Do not evaluate technical feasibility of reframed solutions; flag and hand off.
- Do not run customer discovery; propose what to validate and hand off.
- If the original framing was never validated, recommend validation before reframing (avoid reframing assumptions).
- Respect strategic intent — challenge framing, not the user's goals.
