# Solo OS Agent Specs

Agent specs are markdown files that provide role-specific AI guidance for Cursor's autonomous agent system. Each spec defines a specialized persona — its responsibilities, decision protocols, collaboration patterns, and guardrails — so that AI agents operate with consistent quality and clear boundaries.

When installed, these agents are available as sub-agents that can be invoked by name (e.g., `@pm`, `@eng_lead`, `@chief_of_staff`) within Cursor conversations.

## Installation

**Automatic (recommended):**

```
solo-os install-agents
```

Install for another IDE profile:

```bash
solo-os install-agents --ide claude-code
```

`install-agents` does not target Codex yet. Codex custom agents are TOML files in
`.codex/agents/` or `~/.codex/agents/`, which differ from Solo OS markdown agent specs.

**Manual:**

Copy all `.md` files from this directory to your IDE's agent directory.

## Agents

| Name | Description |
|------|-------------|
| `big_thinker` | Big Thinker — visionary product thinker and creative strategist for ideation, opportunity spotting, and problem reframing. |
| `chief_of_staff` | Chief of Staff — cross-functional orchestrator that routes work, resolves conflicts, and produces execution-ready plans. |
| `design` | Design Lead — UI/UX specialist that reviews and elevates visual design, interaction quality, usability, and brand consistency. |
| `research_guru` | Research Guru — expert internet researcher that finds and structures factual evidence for product, technical, and market decisions. |
| `pm` | Product Manager — keeps execution aligned to roadmap with ruthless prioritization, PMF focus, and customer-centric framing. |
| `qa` | QA & Release Manager — defines risk-based test plans, release readiness checks, and rollback safeguards. |
| `security_eng` | Security & Privacy Engineer — reviews architecture, code, and releases for data protection, access control, and trust risks. |
| `eng_lead` | Engineering Lead — reviews architecture, implementation, and code for correctness, maintainability, security, and performance. |
