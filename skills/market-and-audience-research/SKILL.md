---
name: market-and-audience-research
description: Find market size, audience demographics, user behavior data, pricing benchmarks, industry trends, and regulatory landscape for a specific domain. Use during discovery, pricing analysis, MVP scoping, go-to-market planning, or opportunity scanning when quantitative market evidence is needed.
---

# Market and Audience Research

## Purpose
Find and structure quantitative market evidence — market size, audience demographics, user behavior data, pricing benchmarks, industry trends, and regulatory context — to support product and business decisions.

## Use When
- During discovery to quantify the market opportunity and target audience.
- When pricing-and-unit-economics skill needs market benchmarks and willingness-to-pay data.
- When customer-segment-and-access-map skill needs demographic and behavioral data.
- During MVP scoping to validate market size assumptions.
- When opportunity-scanner needs quantitative evidence for opportunity ranking.
- Optionally when go-to-market experiments need channel benchmarks and audience data.
- When any agent asks "how big is this market?" or "who is the audience?"

## Execution Context (Resource Reality)
- The founder operates with advanced generative AI: autonomous agents, sub-agents, skills, and frontier models.
- AI-augmented research can synthesize data from multiple sources, cross-reference estimates, and produce structured market analyses rapidly.
- Produce thorough, sourced market briefs — not hand-wavy estimates. Decisions about market entry, pricing, and resource allocation depend on research quality.

## Preferred Sources
- **Statista** — market size, industry statistics, consumer data
- **US Census Bureau / Bureau of Labor Statistics** — demographic, economic, and employment data
- **Google Trends** — search interest trends over time, geographic distribution
- **Pew Research / Gallup** — consumer behavior, attitudes, and technology adoption surveys
- **CB Insights / PitchBook** — market maps, funding trends, category analysis
- **Industry reports** (McKinsey, Bain, a16z, Deloitte) — market analysis and forecasts
- **App Annie / Sensor Tower / data.ai** — mobile market data, app category sizing
- **SimilarWeb** — web traffic, audience demographics, engagement metrics
- **Reddit / Quora / Twitter/X** — qualitative audience signals, pain points, behavior patterns
- **Government/regulatory sites** — compliance requirements, industry regulations
- **Trade associations and professional organizations** — industry-specific data and reports

Adapt source selection based on the specific market and geography.

## Workflow
1. Define the market research question: what domain, geography, segment, and decision this supports.
2. Research market size and structure:
   - TAM / SAM / SOM estimates (where data allows)
   - Market growth rate and trajectory
   - Key market segments and their relative size
   - Market maturity and competitive density
3. Research target audience:
   - Demographics (age, income, geography, profession)
   - Behavior patterns (habits, tools used, workflows, pain points)
   - Technology adoption and digital behavior
   - Willingness to pay and spending patterns
4. Research pricing and business model benchmarks:
   - Comparable product pricing in the space
   - Common pricing models (subscription, freemium, usage-based, etc.)
   - Conversion rate benchmarks for the category
   - Customer acquisition cost references
5. Research industry trends and shifts:
   - Growth drivers and headwinds
   - Technology disruptions affecting the market
   - Regulatory changes or emerging requirements
6. Assess data quality and gaps:
   - Note where estimates conflict across sources
   - Flag where data is outdated or geographically limited
   - Identify what additional primary research could fill gaps
7. Label all findings with evidence tiers: `[Verified]`, `[Directional]`, `[Inference]`.

## Required Output
- Market definition and research question
- Market size estimates (TAM/SAM/SOM where possible) with sources
- Audience profile (demographics, behavior, technology adoption)
- Pricing and business model benchmarks
- Industry trends and shifts (2-4)
- Regulatory landscape (if applicable)
- Data quality assessment and gaps
- Source references with URLs, dates, and credibility notes

## Artifact Rules
- Primary folder: `agent_generated/discovery/` or `agent_generated/economics/` (if supporting pricing/viability).
- Artifact class: `decision` when the analysis influences market entry or pricing decisions.
- Include metadata header: title, artifact_type, status (draft/approved/superseded), version, owner, created_at.
- May create/edit `draft` artifacts only.
- Never overwrite `approved` artifacts in place.
- Every data point must have source attribution with publication date.

## Sub-agent Handoffs
- `research_guru`: primary agent that drives this skill.
- `product-manager`: receives market context for roadmap and scoping decisions.
- `pricing-and-unit-economics` (skill): receives pricing benchmarks and willingness-to-pay data.
- `customer-segment-and-access-map` (skill): receives audience demographics and behavior data.
- `opportunity-scanner` (skill): receives market size and trend data for opportunity ranking.
- Optionally use `go-to-market-experiments` (skill) when channel/audience data is for experiment design.
- Apply artifact governance rules (metadata, placement, version) before finalizing artifacts.

## Depth and Token Guidance
- Default output target: 1200-2100 words for meaningful market analysis.
- Multi-segment or multi-geography research may expand to 3000 words.
- Use tables for quantitative comparisons — more information-dense and verifiable than prose.
- Prioritize depth on market size evidence, audience behavior, and pricing benchmarks over trend narrative.

## Guardrails
- Every data point must be labeled `[Verified]`, `[Directional]`, or `[Inference]` with source and date.
- Do not fabricate market size numbers, demographic data, or pricing benchmarks.
- Do not make strategic or pricing decisions — present findings and hand off to the appropriate agent.
- If the market definition is too broad, ask for narrowing before researching.
- Flag when market data is thin, conflicting, or dominated by a single source.
- Note geographic and temporal limitations of data — US data doesn't apply globally, 2020 data may not reflect 2026 reality.
