---
name: customer-discovery-interview
description: Run customer discovery planning and synthesis to validate pain, urgency, and demand. Use when an idea needs evidence, when ICP/problem clarity is weak, or when deciding whether to move into MVP planning.
---

# Customer Discovery Interview

## GitHub workflow

For Issues/Projects queries and updates, prefer `solo-os gh-list|gh-next|gh-update|gh-promote|gh-close` over ad hoc `gh issue` / `gh project` commands.

Follow `docs/governance/workflow-system.md` for the canonical workflow taxonomy, parent-relationship rules, and direct-to-build-loop guidance.

## Purpose
Validate whether the target customer has a real, urgent problem worth solving now.

## Use When
- An idea passed triage and needs evidence.
- Customer segment or problem statement is unclear.
- The user asks for interview plans, scripts, or synthesis.

## Execution Context (Resource Reality)
- The founder operates with advanced generative AI: autonomous agents, sub-agents, skills, and frontier models.
- AI agents can help with interview prep, script generation, synthesis, and pattern analysis at scale. Do not underestimate the speed and depth of discovery preparation and analysis.
- The binding constraint is access to real customers and quality of human conversation — not preparation bandwidth.

## Workflow
1. Define ICP and job-to-be-done.
2. Draft focused interview plan (goals, participants, questions, anti-leading prompts).
3. Capture findings and synthesize signal patterns.
4. Conclude: validated / partially validated / not validated.
5. Recommend move to `mvp-scope-and-roadmap` or return to `idea-triage`.

## Required Output
- Problem statement (current version)
- Evidence summary (signals, contradictions, confidence)
- Decision gate: "Validated enough to scope MVP?"
- Top 3 open questions

## Artifact Rules
- Primary folder: `agent_generated/discovery/`
- Artifact class: `decision` for synthesis/readouts, `ephemeral` for raw notes.
- Include required metadata for decision/canonical docs.
- May create/edit `draft` artifacts only.
- Never overwrite `approved` artifacts in place.
- Major version bump required if ICP/problem statement changes materially.
- If the repo still uses compatibility pointers, update `agent_generated/discovery/LATEST.md` and `_index.md` for canonical promotions while keeping them pointer/registry-only.

## Sub-agent Handoffs
- `product-manager`: validate customer-value framing and roadmap relevance.
- `growth-operator`: shape testable demand/activation hypotheses.
- `pricing-and-unit-economics` skill or `growth-operator`: if willingness-to-pay signal is central.
- Apply artifact governance rules (metadata, placement, version) before finalizing artifacts.

## Depth and Token Guidance
- Default output target: 1200-2100 words for discovery synthesis and recommendations.
- Complex evidence with conflicting signals may expand to 3000 words.
- Do not compress away contradictory evidence; include it explicitly.
- Use layered output: summary first, then evidence and implications.

## Guardrails
- Do not claim validation from anecdotal single-source evidence.
- Keep recommendations evidence-first, not opinion-first.
- If evidence is mixed, propose the smallest next validation step.
