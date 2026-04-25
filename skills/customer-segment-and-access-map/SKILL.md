---
name: customer-segment-and-access-map
description: Define reachable customer segments and a practical recruitment plan for discovery. Use after idea triage when the team needs to know who to talk to, where to find them, and how to recruit interviews quickly.
---

# Customer Segment and Access Map

## GitHub workflow

For Issues/Projects queries and updates, prefer `solo-os gh-list|gh-next|gh-update|gh-promote|gh-close` over ad hoc `gh issue` / `gh project` commands.

Follow `docs/governance/workflow-system.md` for the canonical workflow taxonomy, parent-relationship rules, and direct-to-build-loop guidance.

## Purpose
Turn a triaged idea into an actionable customer access plan so discovery can run fast and with the right people.

## Use When
- `idea-triage` returned `Go`.
- Discovery is blocked by unclear ICP or weak outreach channels.
- The user asks who the first customers are and how to reach them.

## Execution Context (Resource Reality)
- The founder operates with advanced generative AI: autonomous agents, sub-agents, skills, and frontier models.
- AI agents can assist with segment research, channel mapping, outreach script drafting, and ICP refinement at high speed. Do not simplify segmentation due to perceived analysis effort.
- The binding constraint is real-world access to target customers — not research or synthesis bandwidth.

## Workflow
1. Define ICP v1 and exclusion criteria.
2. List 2-3 candidate segments and rank by pain urgency + reachability.
3. Build a recruitment channel map (communities, directories, warm intros, outbound lists).
4. Draft outreach scripts for each channel.
5. Set interview recruitment targets and fallback plan if response is low.
6. Hand off into `customer-discovery-interview`.

## Required Output
- ICP v1 and exclusions
- Priority segments (ranked)
- Channel map (where/how to reach each segment)
- Outreach script template
- Recruitment target (count, timeline, owner)
- Backup plan if response rate underperforms

## Artifact Rules
- Primary folder: `agent_generated/discovery/`
- Optional cross-link: originating triage record in `agent_generated/ideas/`
- Artifact class: `decision` for final segment/access strategy
- Include metadata header: title, artifact_type, status (draft/approved/superseded), version, owner, created_at.
- May create/edit `draft` artifacts only.
- Never overwrite `approved` artifacts in place.
- Material changes require new version + `supersedes`.
- If the repo still uses compatibility pointers, update `agent_generated/discovery/LATEST.md` and `agent_generated/_index.md` if promoted to canonical, while keeping them pointer/registry-only.

## Sub-agent Handoffs
- `product-manager`: validate segment choice against roadmap and value proposition.
- Use `go-to-market-experiments` (skill) when channel strategy and conversion optimization require experiment planning.
- Apply artifact governance rules (metadata, placement, version) before finalizing artifacts.
- `chief-of-staff`: resolve cross-functional conflicts or blocked recruitment decisions.

## Depth and Token Guidance
- Default output target: 1050-1950 words for segmentation and channel planning.
- High uncertainty on customer access may expand to 2700 words.
- Preserve depth on segment ranking logic, outreach plan, and fallback strategy.
- Use layered output: target segment summary first, then channel-level detail.

## Guardrails
- Do not proceed with broad "everyone is the customer" framing.
- Prefer reachable segments over theoretically ideal but inaccessible ones.
- If no reliable channel exists, mark risk explicitly before discovery starts.
