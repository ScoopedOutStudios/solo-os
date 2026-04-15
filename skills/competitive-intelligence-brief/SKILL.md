---
name: competitive-intelligence-brief
description: Research competitors, alternatives, positioning, pricing, features, reviews, and market gaps for a specific product or domain. Use before idea triage, during discovery, when PM needs competitive context, or when designing positioning experiments.
---

# Competitive Intelligence Brief

## Purpose
Research and structure a comprehensive competitive landscape analysis for a specific product domain, including player profiles, feature/pricing comparisons, user sentiment, and positioning gaps.

## Use When
- Entering a new product domain and need to understand the competitive landscape.
- Before idea triage to assess whether a space is crowded or has whitespace.
- During discovery to understand how competitors solve the same problem.
- When PM needs competitive positioning context for roadmap decisions.
- When designing positioning or differentiation experiments (optionally invoke growth-operator for dedicated growth review).
- When big-thinker or opportunity-scanner needs landscape awareness.

## Execution Context (Resource Reality)
- The founder operates with advanced generative AI: autonomous agents, sub-agents, skills, and frontier models.
- AI-augmented research capacity is high. Thorough competitive analysis across multiple players, pricing tiers, and review sources can be done rapidly.
- Do not provide shallow one-paragraph summaries. Produce decision-ready competitive intelligence with structured comparisons and source attribution.

## Preferred Sources
- **Crunchbase** — funding, team, company profiles, growth signals
- **G2 / Capterra** — software reviews, feature comparisons, user sentiment
- **ProductHunt** — new launches, community reception, feature positioning
- **SimilarWeb** — traffic estimates, audience overlap, channel breakdown
- **App Store / Play Store** — app reviews, ratings, feature changelogs
- **LinkedIn** — team size, hiring patterns, org structure signals
- **Company websites / pricing pages** — feature lists, pricing tiers, positioning copy
- **SEC filings / PitchBook** — financial data for larger competitors
- **Reddit / Twitter/X / Hacker News** — user complaints, unmet needs, sentiment

Adapt source selection based on the specific domain. These are starting points, not constraints.

## Workflow
1. Define the competitive domain: what product category, user segment, and job-to-be-done to analyze.
2. Identify key players (5-10): direct competitors, indirect alternatives, and emerging entrants.
3. For each player, research:
   - Positioning and value proposition
   - Key features and differentiators
   - Pricing model and tiers
   - User sentiment (reviews, complaints, praise)
   - Funding, team size, and growth signals (where available)
   - Technology approach (where relevant)
4. Build a structured comparison:
   - Feature comparison matrix
   - Pricing comparison table
   - Positioning map (who serves whom)
5. Identify competitive gaps and opportunities:
   - Under-served segments
   - Common user complaints across competitors
   - Missing features or poor execution areas
   - Pricing gaps or model innovation opportunities
6. Label all findings with evidence tiers: `[Verified]`, `[Directional]`, `[Inference]`.

## Required Output
- Domain definition (category, segment, job-to-be-done)
- Player profiles (5-10) with positioning, features, pricing, sentiment
- Feature comparison matrix
- Pricing comparison table
- Competitive gaps and opportunities (3-5)
- User sentiment summary (common complaints, unmet needs)
- Source references with URLs and dates

## Artifact Rules
- Primary folder: `agent_generated/discovery/` (or `agent_generated/ideas/` if pre-triage).
- Artifact class: `decision` when the analysis influences product direction.
- Include required metadata from `docs/governance/artifact-governance-spec.md`.
- May create/edit `draft` artifacts only.
- Never overwrite `approved` artifacts in place.
- Material updates require new version + `supersedes`.
- Every factual claim must have source attribution.

## Sub-agent Handoffs
- `research-guru`: primary agent that drives this skill.
- `big-thinker` / `opportunity-scanner`: receives competitive gaps as opportunity input.
- `product-manager`: receives positioning context for roadmap decisions.
- Optionally `growth-operator`: when brief feeds positioning experiments and user requests growth review.
- `pricing-and-unit-economics` (skill): receives pricing comparisons as input.
- Apply artifact governance per spec; optionally invoke `artifact-governance-manager` for placement/version validation.

## Depth and Token Guidance
- Default output target: 1200-2100 words for meaningful competitive analysis.
- Complex markets with many players or multi-segment analysis may expand to 3000 words.
- Prioritize depth on competitive gaps, user sentiment, and pricing over exhaustive player profiles.
- Use tables and matrices for comparisons — more information-dense than prose.

## Guardrails
- Every factual claim must be labeled `[Verified]`, `[Directional]`, or `[Inference]` with source.
- Do not fabricate company data, funding amounts, or review quotes.
- Do not make strategic recommendations — present findings and hand off to PM or big-thinker.
- If the competitive domain is too broad, ask the user to narrow before researching.
- Flag when competitive data is thin or unreliable for a specific player.
