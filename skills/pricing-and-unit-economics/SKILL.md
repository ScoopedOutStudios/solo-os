---
name: pricing-and-unit-economics
description: Evaluate pricing options and unit economics to confirm business viability. Use when pricing is undecided, margins are uncertain, or viability assumptions need structured review.
---

# Pricing and Unit Economics

## GitHub workflow

For Issues/Projects queries and updates, prefer `solo-os gh-list|gh-next|gh-update|gh-promote|gh-close` over ad hoc `gh issue` / `gh project` commands.

Follow `docs/governance/workflow-system.md` for the canonical workflow taxonomy, parent-relationship rules, and direct-to-build-loop guidance.

## Purpose
Ensure product decisions remain economically viable at solopreneur scale.

## Use When
- Pricing model needs definition or revision.
- Unit economics are uncertain (CAC, conversion, churn, cost-to-serve).
- The user asks if the idea is financially viable.

## Execution Context (Resource Reality)
- The founder operates with advanced generative AI: autonomous agents, sub-agents, skills, and frontier models.
- AI agents can build financial models, sensitivity analyses, and pricing simulations rapidly. Do not simplify economic analysis due to perceived modeling effort.
- Cost-to-serve estimates should account for AI-driven infrastructure where applicable (e.g., AI API costs as a variable input, not fixed headcount).
- The binding constraints are market data quality and pricing hypothesis validity — not analysis capacity.

## Workflow
1. Define pricing options and key assumptions.
2. Build simple economics view (revenue, costs, contribution margin).
3. Run sensitivity checks on top uncertain assumptions.
4. Conclude viability: viable / borderline / not viable.
5. Recommend pricing decision and next validation step.

## Required Output
- Pricing options compared
- Core assumptions
- Break-even or margin view
- Decision: adopt / test further / defer

## Artifact Rules
- Primary folder: `agent_generated/economics/`
- Artifact class: `decision` for pricing memos; `canonical` for current pricing/econ model.
- Include required metadata for decision/canonical docs.
- May create/edit `draft` artifacts only.
- Never overwrite `approved` artifacts in place.
- Major version bump required when pricing or viability conclusion changes materially.
- If the repo still uses compatibility pointers, update `agent_generated/economics/LATEST.md` and `_index.md` for canonical promotions while keeping them pointer/registry-only.

## Sub-agent Handoffs
- `product-manager`: validate customer value vs pricing tradeoffs.
- Use `go-to-market-experiments` (skill) to align acquisition/activation assumptions with economics model when needed.
- `eng_lead`: assess cost-to-serve implications of technical scope.
- Apply artifact governance rules (metadata, placement, version) before finalizing artifacts.
- `chief_of_staff`: resolve cross-functional tradeoff conflicts.

## Depth and Token Guidance
- Default output target: 1200-2100 words for pricing and viability recommendations.
- High-stakes pricing or ambiguous viability may expand to 3000 words.
- Preserve depth on assumptions, sensitivity, and risk tradeoffs.
- Use layered output: recommendation summary first, then economics detail.

## Guardrails
- State assumptions explicitly; avoid hidden model logic.
- Separate observed metrics from assumptions.
- If viability is uncertain, recommend smallest next test to reduce uncertainty.
