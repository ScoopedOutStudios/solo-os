# Solo OS Agent Specs

> **Context:** `chief-of-staff` is the single primary AI entrypoint. Ask it what to do next and it will handle simple workflow tasks directly or route to specialists as needed. For the skill vs command vs sub-agent model, read [Use the bundled AI assets](../README.md#use-the-bundled-ai-assets) or run `solo-os onboarding`.

Agent specs are markdown files that provide role-specific AI guidance for Cursor's autonomous agent system. Each spec defines a specialized persona — its responsibilities, decision protocols, collaboration patterns, and guardrails — so that AI agents operate with consistent quality and clear boundaries.

When installed, these agents are available as sub-agents that can be invoked by name (e.g., `@chief-of-staff`, `@software-engineer`, `@product-manager`) within Cursor conversations.

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
| `chief-of-staff` | Chief of Staff — single AI entrypoint; handles workflow-object creation directly, routes cross-functional work to specialists, resolves conflicts, and produces execution-ready plans. |
| `software-engineer` | Software Engineer — reviews architecture, implementation, and code for correctness, maintainability, security, and performance. |
| `product-manager` | Product Manager — keeps execution aligned to roadmap with ruthless prioritization, PMF focus, and customer-centric framing. |
| `quality-engineer` | Quality Engineer — defines risk-based test plans, release readiness checks, and rollback safeguards. |
| `security-engineer` | Security & Privacy Engineer — reviews architecture, code, and releases for data protection, access control, and trust risks. |
| `design-lead` | Design Lead — UI/UX specialist that reviews and elevates visual design, interaction quality, usability, and brand consistency. |
| `research-analyst` | Research Analyst — expert internet researcher that finds and structures factual evidence for product, technical, and market decisions. |
| `big-thinker` | Big Thinker — visionary product thinker and creative strategist for ideation, opportunity spotting, and problem reframing. |
