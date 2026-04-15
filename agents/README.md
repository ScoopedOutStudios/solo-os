# Solo OS Agent Specs

Agent specs are markdown files that provide role-specific AI guidance for Cursor's autonomous agent system. Each spec defines a specialized persona — its responsibilities, decision protocols, collaboration patterns, and guardrails — so that AI agents operate with consistent quality and clear boundaries.

When installed, these agents are available as sub-agents that can be invoked by name (e.g., `@pm`, `@staff`, `@cos`) within Cursor conversations.

## Installation

**Automatic (recommended):**

```
solo-os install-agents
```

**Manual:**

Copy all `.md` files from this directory to `~/.cursor/agents/`.

## Agents

| Name | Description |
|------|-------------|
| `bt` | Big Thinker — visionary product thinker and creative strategist for ideation, opportunity spotting, and problem reframing. |
| `cos` | Chief of Staff — cross-functional orchestrator that routes work, resolves conflicts, and produces execution-ready plans. |
| `design` | Design Lead — UI/UX specialist that reviews and elevates visual design, interaction quality, usability, and brand consistency. |
| `growth` | Growth Operator — drives acquisition, activation, retention, and revenue loops with measurable experiments. |
| `guru` | Research Guru — expert internet researcher that finds and structures factual evidence for product, technical, and market decisions. |
| `pm` | Product Manager — keeps execution aligned to roadmap with ruthless prioritization, PMF focus, and customer-centric framing. |
| `qa` | QA & Release Manager — defines risk-based test plans, release readiness checks, and rollback safeguards. |
| `sec` | Security & Privacy Engineer — reviews architecture, code, and releases for data protection, access control, and trust risks. |
| `staff` | Staff Engineer — reviews architecture, implementation, and code for correctness, maintainability, security, and performance. |
