---
name: technical-research-brief
description: Research technical options — APIs, libraries, platforms, architecture patterns, and implementation approaches for a specific build decision. Use when staff evaluates build options, during POC planning, or when choosing between technical approaches.
---

# Technical Research Brief

## Purpose
Research and compare technical options (APIs, libraries, frameworks, platforms, architecture patterns) to support a specific build decision with structured evidence and source attribution.

## Use When
- Staff-engineer needs to evaluate build options or choose between technical approaches.
- Planning a POC and need to assess available tools, APIs, or platforms.
- Security-engineer needs threat intelligence, compliance standards, or security tool options.
- Evaluating whether to build vs. buy vs. integrate for a specific capability.
- Assessing migration paths, breaking changes, or platform transitions.

## Execution Context (Resource Reality)
- The founder operates with advanced generative AI: autonomous agents, sub-agents, skills, and frontier models.
- AI-augmented research can process documentation, compare libraries, and synthesize community signals rapidly.
- Produce thorough, decision-ready technical briefs — not superficial feature lists. Engineers need confidence to act on findings.

## Preferred Sources
- **Official documentation** — always the primary source for APIs, libraries, and platforms
- **GitHub** — repos, issues, stars, community activity, release cadence, open issues
- **Stack Overflow** — common issues, community solutions, adoption signals
- **npm / PyPI / crates.io** — package download trends, dependency health, version history
- **Hacker News / Reddit (r/programming, r/webdev, etc.)** — developer sentiment, real-world adoption stories, known gotchas
- **ThoughtWorks Technology Radar** — technology maturity and adoption assessments
- **Benchmarks and performance comparisons** — published benchmarks, load test results
- **Migration guides and changelogs** — official or community migration documentation
- **Security advisories** (CVE databases, Snyk, GitHub Security Advisories) — vulnerability history

Adapt source selection based on the specific technology domain.

## Workflow
1. Define the technical question: what decision this supports, constraints, and requirements.
2. Identify candidate options (3-5): libraries, APIs, platforms, or architecture patterns.
3. For each option, research:
   - Maturity and stability (version, release cadence, breaking change history)
   - Community and ecosystem (stars, downloads, contributors, Stack Overflow activity)
   - Performance characteristics (benchmarks, known limitations)
   - Documentation quality and learning curve
   - Known issues and gotchas (open issues, common complaints)
   - Security track record (CVEs, vulnerability history, maintenance responsiveness)
   - Ecosystem fit (integration with existing stack, dependency compatibility)
4. Build a structured comparison matrix.
5. Identify the strongest option and key tradeoffs.
6. Note migration/adoption considerations and risks.
7. Label all findings with evidence tiers: `[Verified]`, `[Directional]`, `[Inference]`.

## Required Output
- Technical question and decision context
- Options evaluated (3-5) with profiles
- Comparison matrix (maturity, community, performance, security, ecosystem fit)
- Known issues and gotchas per option
- Recommendation with tradeoff rationale
- Migration/adoption considerations
- Source references with URLs and dates

## Artifact Rules
- Primary folder: `agent_generated/plans/` (if supporting build decisions) or `agent_generated/discovery/` (if exploratory).
- Artifact class: `decision` when the analysis directly influences architecture or stack choices.
- Include metadata header: title, artifact_type, status (draft/approved/superseded), version, owner, created_at.
- May create/edit `draft` artifacts only.
- Never overwrite `approved` artifacts in place.
- Every technical claim must have source attribution.

## Sub-agent Handoffs
- `research-analyst`: primary agent that drives this skill.
- `software-engineer`: receives technical findings for architecture and build decisions.
- `security-engineer`: receives security-relevant findings (CVEs, vulnerability history).
- `solution-probe-poc` (skill): receives technical options to inform POC technology choices.
- `build-loop-and-release-rhythm` (skill): receives technical context for implementation planning.
- Apply artifact governance rules (metadata, placement, version) before finalizing artifacts.

## Depth and Token Guidance
- Default output target: 1200-2100 words for meaningful technical comparison.
- Complex multi-option evaluations or deep architecture analysis may expand to 3000 words.
- Use comparison tables — more information-dense and scannable than prose.
- Prioritize depth on tradeoffs, known issues, and migration risks over feature checklists.

## Guardrails
- Every technical claim must be labeled `[Verified]`, `[Directional]`, or `[Inference]` with source.
- Do not fabricate benchmark numbers, download counts, or version histories.
- Do not make final architecture decisions — present findings and hand off to `software-engineer`.
- If the technical question is too broad ("what framework should I use?"), ask for constraints before researching.
- Flag when documentation is poor, community is inactive, or security history is concerning.
