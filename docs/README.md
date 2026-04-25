# Solo OS Documentation

This folder is the documentation hub for the standalone `solo-os` repository.

## Start here

- [`../README.md`](../README.md) — Install, quick start, AI-first workflow, and the product overview
- [`cli-reference.md`](cli-reference.md) — Full CLI command reference (agent primitives and advanced operations)
- [`workflow-spec.md`](workflow-spec.md) — Canonical `Kind` / `Status` / `Stage` semantics
- [`governance/build-loop-and-release-rhythm.md`](governance/build-loop-and-release-rhythm.md) — Build loop structure + Checkpoints A/B/C (governance, not "magic automation" by default)

## AI assets (recommended)

These are installed into your editor profile by the Solo OS CLI. Start with `chief-of-staff` — it is the single AI entrypoint that handles workflow-object creation directly and routes to specialists as needed.

- [`../agents/README.md`](../agents/README.md) — Agent role specs (`chief-of-staff`, `software-engineer`, `product-manager`, etc.)
- [`../skills/README.md`](../skills/README.md) — Structured workflow playbooks agents use for repeatable tasks
- [`../commands/README.md`](../commands/README.md) — Power-user slash-command shortcuts

## Issue body templates (bundled with the Python package)

- `../solo_os/templates/idea-body-template.md`
- `../solo_os/templates/roadmap-body-template.md`
- `../solo_os/templates/build-loop-body-template.md`

## First-run printouts (same text also exists on disk)

- `../solo_os/templates/user-guide-getting-started.md` (also: `solo-os onboarding`)
- `../solo_os/templates/workflow-start.md` (also: `solo-os workflow-start`)
