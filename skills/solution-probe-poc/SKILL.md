---
name: solution-probe-poc
description: Build a timeboxed proof-of-concept to test solution desirability and usability before MVP commitment. Use after idea triage when concrete prototype feedback will improve customer discovery and de-risk key assumptions.
---

# Solution Probe POC

## GitHub workflow

For Issues/Projects queries and updates, prefer `solo-os gh-list|gh-next|gh-update|gh-promote|gh-close` over ad hoc `gh issue` / `gh project` commands.

Follow `docs/governance/workflow-system.md` for the canonical workflow taxonomy, parent-relationship rules, and direct-to-build-loop guidance.

## Purpose
Create a fast, disposable proof-of-concept to validate core solution assumptions before committing to MVP scope.

## Use When
- `idea-triage` returned `Go` but major solution uncertainty remains.
- Customer interviews are too abstract without something concrete.
- You need quick evidence on value perception, usability, or feasibility.

## Execution Context (Resource Reality)
- The founder operates with advanced generative AI: autonomous agents, sub-agents, skills, and frontier models.
- POC build effort should reflect AI-assisted development speed. Functional prototypes can be produced rapidly — timebox by learning objective, not by perceived build difficulty.
- Do not skip POCs because "it would take too long to build." AI agents can scaffold working prototypes quickly enough to validate assumptions early.

## Workflow
1. Define one critical assumption to test (only one per probe).
2. Pick one user journey and one value moment.
3. Build a timeboxed POC (1-3 days, non-production).
4. Run targeted feedback sessions with intended users.
5. Decide: continue / pivot / kill and document rationale.
6. Hand off to `customer-discovery-interview` and `mvp-scope-and-roadmap` if continuing.

## Required Output
- Assumption tested
- POC scope (in-scope and explicit non-goals)
- Feedback summary (what users understood, valued, rejected)
- Decision: continue / pivot / kill
- Next step and owner

## Artifact Rules
- Primary folder: `agent_generated/discovery/` (solution validation readout)
- Optional cross-link: `agent_generated/ideas/` to originating triage decision
- Artifact class: `decision` for readouts; `ephemeral` for rough build notes
- Include metadata header for decision/canonical docs: title, artifact_type, status (draft/approved/superseded), version, owner, created_at.
- May create/edit `draft` artifacts only.
- Never overwrite `approved` artifacts in place.
- Material updates require new version + `supersedes`.
- If this becomes a canonical discovery reference and the repo still uses compatibility pointers, update `agent_generated/discovery/LATEST.md` and `agent_generated/_index.md` as pointer/registry-only surfaces.

## Sub-agent Handoffs
- `product-manager`: verify customer value and roadmap relevance of findings.
- `software-engineer`: advise on minimal scope and feasibility constraints.
- `security-engineer`: ensure probe avoids risky data collection/exposure.
- Apply artifact governance rules (metadata, placement, version) before finalizing artifacts.
- `chief-of-staff`: arbitrate if specialist recommendations conflict.

## Depth and Token Guidance
- Default output target: 1050-1950 words for probe design and readout.
- High uncertainty or conflicting user feedback may expand to 2700 words.
- Preserve depth on assumption tested, signal quality, and decision rationale.
- Use layered output: continue/pivot/kill summary first, then evidence.

## Guardrails
- POC is a learning tool, not pre-MVP production work.
- Do not optimize polish, scale, or architecture in this step.
- Keep to one user journey and one assumption to avoid scope bleed.
- If no user signal changes the decision, stop and return to discovery problem framing.
