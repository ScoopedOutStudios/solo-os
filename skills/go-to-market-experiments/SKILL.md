---
name: go-to-market-experiments
description: Design, run, and interpret go-to-market and growth experiments with clear success criteria. Use when testing acquisition, activation, retention, messaging, or channel hypotheses.
---

# Go-to-Market Experiments

## GitHub workflow

For Issues/Projects queries and updates, prefer `solo-os gh-list|gh-next|gh-update|gh-promote|gh-close` over ad hoc `gh issue` / `gh project` commands.

Follow `docs/governance/workflow-system.md` for the canonical workflow taxonomy, parent-relationship rules, and direct-to-build-loop guidance.

## Purpose
Run disciplined experiments that improve growth outcomes and reduce go-to-market uncertainty.

## Use When
- The user asks for growth tests or GTM strategy.
- Funnel bottlenecks are unclear.
- You need evidence before scaling channel or messaging investment.

## Execution Context (Resource Reality)
- The founder operates with advanced generative AI: autonomous agents, sub-agents, skills, and frontier models.
- AI agents can rapidly build landing pages, instrumentation, tracking, A/B test setups, and analytics tooling. Experiment velocity should reflect this capacity.
- Do not limit experiment ambition because of perceived build effort. The binding constraints are customer signal quality, channel access, and strategic focus.

## Workflow
1. Define bottleneck (acquisition, activation, retention, conversion, revenue).
2. Form one clear hypothesis and smallest viable test.
3. Set success metric, guardrail metrics, and decision threshold.
4. Record result and conclude: continue / iterate / stop.
5. Feed learnings back to `plans/` if roadmap/scope should change.

## Required Output
- Hypothesis
- Test plan (audience, channel, timeline)
- Metrics and thresholds
- Decision: continue / iterate / stop

## Artifact Rules
- Primary folder: `agent_generated/experiments/`
- Artifact class: `decision` for experiment plan/readout; `canonical` for active playbook.
- Include required metadata for decision/canonical docs.
- May create/edit `draft` artifacts only.
- Never overwrite `approved` artifacts in place.
- Major version bump when strategy or viability assumptions change materially.
- If the repo still uses compatibility pointers, update `agent_generated/experiments/LATEST.md` and `_index.md` for canonical promotions while keeping them pointer/registry-only.

## Sub-agent Handoffs
- `product-manager`: validate strategic alignment and resource tradeoffs.
- `staff-engineer`: assess implementation/instrumentation feasibility.
- `security-privacy-engineer`: validate privacy-safe instrumentation and data handling.
- `qa-release-manager`: validate safe rollout/rollback for experiment changes.
- Optionally invoke `growth-operator` for experiment prioritization and funnel strategy when the user requests dedicated growth review.
- Apply artifact governance per spec (metadata, placement, version); optionally invoke `artifact-governance-manager` for canonical promotion.

## Depth and Token Guidance
- Default output target: 1200-2100 words for experiment design and interpretation.
- High-uncertainty funnels or conflicting results may expand to 3000 words.
- Prioritize depth on hypotheses, metrics, guardrails, and decision thresholds.
- Use layered output: experiment summary first, then metric/risk detail.

## Guardrails
- Do not run experiments without explicit success criteria.
- Do not optimize vanity metrics without retained-value signal.
- Keep tests small and fast unless prior evidence justifies scaling.
