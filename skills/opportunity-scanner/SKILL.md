---
name: opportunity-scanner
description: Systematically scan a domain for user behavior trends, technology shifts, competitive whitespace, and emerging opportunities. Use when entering a new market, looking for the next product idea, or when an existing product feels stale and needs fresh opportunity hypotheses.
---

# Opportunity Scanner

## GitHub workflow

For Issues/Projects queries and updates, prefer `solo-os gh-list|gh-next|gh-update|gh-promote|gh-close` over ad hoc `gh issue` / `gh project` commands.

Follow `docs/governance/workflow-system.md` for the canonical workflow taxonomy, parent-relationship rules, and direct-to-build-loop guidance.

## Purpose
Systematically scan a domain for user behavior trends, technology shifts, competitive whitespace, and emerging opportunities that a solo AI-augmented founder can exploit.

## Use When
- Entering a new market or domain and need to understand the landscape before ideating.
- Looking for the next product idea within the portfolio.
- An existing product feels stale and needs fresh opportunity hypotheses.
- The user asks "what should I build next?" or "where are the opportunities in [space]?"

## Execution Context (Resource Reality)
- The founder operates with advanced generative AI: autonomous agents, sub-agents, skills, and frontier models.
- Opportunity assessment should account for AI-augmented execution. Opportunities that require rapid prototyping, content generation, or data processing are especially attractive given AI capabilities.
- Do not dismiss opportunities for perceived build complexity. Focus on demand signal strength, whitespace size, and founder-market fit.
- Prioritize opportunities where a small AI-augmented team has asymmetric advantage over large incumbents.

## Workflow
1. Define the domain/space to scan (user segment, industry, problem area, or technology frontier).
2. Map the current landscape:
   - Key players and their positioning
   - Dominant user behavior patterns and workflows
   - Known pain points and friction
   - Technology enablers and recent shifts
3. Identify shifts creating new openings:
   - User behavior changes (new habits, expectations, frustrations)
   - Technology shifts (AI capabilities, platform changes, new APIs)
   - Market structure changes (regulation, pricing disruption, unbundling/rebundling)
   - Cultural or demographic shifts
4. Spot whitespace:
   - Unserved segments that incumbents ignore
   - Under-served needs where existing solutions are mediocre
   - Friction that's been normalized but doesn't have to exist
   - New experiences AI makes possible that didn't exist before
5. Rank top 3-5 opportunities by:
   - Potential impact (market size, pain severity, willingness to pay)
   - Founder-market fit (domain knowledge, passion, access)
   - AI-augmented execution advantage (can AI make this disproportionately easier to build/operate?)
   - Timing (why now? what changed?)
6. For each ranked opportunity:
   - State the value hypothesis in one sentence
   - Identify the riskiest assumption
   - Propose the fastest validation approach

## Required Output
- Domain/space scanned
- Landscape summary (key players, behavior patterns, pain points)
- Top shifts creating openings (2-4)
- Ranked opportunities (3-5) each with:
  - Value hypothesis
  - Riskiest assumption
  - Validation approach
- Recommended first opportunity to pursue and why

## Artifact Rules
- Primary folder: `agent_generated/ideas/`
- Artifact class: `decision` for opportunity briefs that influence what to pursue next.
- Include metadata header: title, artifact_type, status (draft/approved/superseded), version, owner, created_at.
- May create/edit `draft` artifacts only.
- Never overwrite `approved` artifacts in place.
- Material updates require new version + `supersedes`.
- If the repo still uses compatibility pointers, update `agent_generated/ideas/LATEST.md` when a new opportunity brief becomes the active reference, while keeping it pointer-only.

## Sub-agent Handoffs
- `big_thinker`: primary agent that drives this skill — provides domain context and creative lens.
- `idea-triage`: formal Go/Park/Kill scoring for top-ranked opportunities.
- `product-manager`: roadmap fit and strategic alignment check.
- Apply artifact governance rules (metadata, placement, version) before finalizing artifacts.

## Depth and Token Guidance
- Default output target: 1200-2100 words for meaningful landscape analysis and opportunity ranking.
- High-complexity domains or multi-segment scans may expand to 3000 words.
- Prioritize depth on opportunity rationale, whitespace evidence, and validation paths over exhaustive landscape mapping.
- Use layered output: top opportunities and recommendations first, then supporting landscape analysis.

## Guardrails
- Keep scanning focused; do not attempt to cover an entire industry in one pass. Narrow the domain.
- Every opportunity must have a riskiest assumption and validation path — no pure speculation.
- Do not evaluate technical feasibility in depth; flag and hand off to `eng_lead`.
- Do not confuse "interesting trend" with "actionable opportunity" — require a clear value hypothesis for each.
- If the domain is too broad, ask the user to narrow before scanning.
