# Solo OS Workflow Specification

## Purpose

Define the canonical workflow model for Solo OS so ideas, roadmap bets, and execution loops are structured consistently across repos and enforced by CLI commands, agent skills, and prompts.

## Workflow Hierarchy

```
Project Vision / Strategy / Thesis    (document, not a GH issue)
  └── Ideas                            (Kind: Idea)
        └── Roadmap Items              (Kind: Roadmap)
              └── Build Loops          (Kind: Build Loop)
                    └── AI Agent Execution Plans   (guidance, not tracked)
                          └── Git Commits          (on the BL branch)
```

### Layer Definitions

**Project Vision / Strategy / Thesis**
A document (e.g. `docs/product/vision.md`) that provides strategic context for all work in a repo or across repos. Not a GitHub issue. Not tracked by solo-os. Referenced by Ideas and Roadmap items for alignment.

**Idea** (Kind: Idea)
A speculative hypothesis, opportunity, or potential improvement. GitHub issue with `Kind = Idea`. Triaged as Go / Park / Kill. A Go decision produces one or more Roadmap items.

**Roadmap Item** (Kind: Roadmap)
A committed strategic bet or outcome worth tracking explicitly. GitHub issue with `Kind = Roadmap`. Should have a parent Idea (or a documented rationale for direct creation). Decomposed into one or more Build Loops.

**Build Loop** (Kind: Build Loop)
A bounded execution cycle with checkpoints and a concrete, demoable output. GitHub issue with `Kind = Build Loop`. Should have a parent Roadmap item (or a documented rationale for direct creation). Executed through AI Agent plan-then-execute cycles.

**AI Agent Execution Plans**
Each Build Loop is executed through one or more plan-then-execute cycles. Each cycle: the agent plans an approach, executes it, and produces commits on the BL branch. This is guidance for how agents should work, not something solo-os validates or tracks. Detailed agent skills, commands, and enforcement will be defined in BL #17.

**Git Commits**
The concrete output of each execution plan cycle. Commits land on the BL branch and are merged to main after Checkpoint B.

### Cardinality

- 1 Vision/Strategy document provides context for many Ideas
- 1 Idea can produce 1 or more Roadmap items
- 1 Roadmap item can produce 1 or more Build Loops
- 1 Build Loop is executed through 1 or more AI Agent plan cycles
- 1 AI Agent plan cycle produces 1 or more Git commits

### Direct-to-Build-Loop Rule

Skip Idea and/or Roadmap when the work is already well-understood and the main need is execution discipline rather than strategic triage. Document the rationale in the BL issue body under Parent Linkage.

Do not skip Idea or Roadmap when the work introduces a new strategic bet, prioritization across alternatives is unresolved, or the work changes roadmap direction materially.

## Kind Decision Rules

- If it is speculative, use **Idea**.
- If it is a committed strategic bet, use **Roadmap**.
- If it is a bounded execution cycle with a concrete output, use **Build Loop**.

## Status Semantics

Shared values across all Kinds: `Todo`, `Prioritized`, `Backlog`, `Blocked`, `In Progress`, `Done`.

### Interpretation by Kind

| Status | Idea | Roadmap | Build Loop |
|--------|------|---------|------------|
| Todo | Untriaged | - | - |
| Prioritized | Worth near-term pursuit | Near-term committed | Next loop (Checkpoint A complete) |
| Backlog | Parked for later | Later | - |
| Blocked | Missing input | Waiting on dependency | Waiting on dependency/decision |
| In Progress | Active evaluation | Active strategic focus | Active execution |
| Done | Resolved (promoted or killed) | Outcome achieved or abandoned | Loop complete (merged, learning captured) |

## State Transitions

### Idea Lifecycle

```
                    ┌─────────────┐
                    │   created   │
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
              ┌─────│    Todo     │─────┐
              │     └──────┬──────┘     │
              ▼            ▼            ▼
       ┌──────────┐  ┌───────────┐  ┌──────┐
       │ Backlog  │  │Prioritized│  │ Done │ (killed immediately)
       └────┬─────┘  └─────┬─────┘  └──────┘
            │               ▼
            │        ┌────────────┐
            └───────▶│In Progress │◀──┐
                     └──┬─────┬──┘   │
                        │     │      │
                        ▼     ▼      │
                  ┌──────┐ ┌───────┐ │
                  │ Done │ │Blocked├─┘
                  └──────┘ └───────┘
```

**Done (close reason: completed)**: Idea spawned one or more Roadmap items. Close the Idea if it spawned a single Roadmap item. Keep the Idea open as a parent tracker if it spawned multiple Roadmap items.

**Done (close reason: not_planned)**: Idea was killed or permanently parked.

### Roadmap Item Lifecycle

```
              ┌───────────┐     ┌──────────┐
              │Prioritized│     │ Backlog  │
              └─────┬─────┘     └────┬─────┘
                    │                │
                    ▼                │
             ┌────────────┐         │
             │In Progress │◀────────┘
             └──┬─────┬──┘
                │     │
                ▼     ▼
          ┌──────┐ ┌───────┐
          │ Done │ │Blocked│──▶ In Progress
          └──────┘ └───────┘
```

A Roadmap item is **Done** when all its child Build Loops are complete and the outcome is achieved or abandoned.

### Build Loop Lifecycle

```
        ┌───────────────────────┐
        │   Checkpoint A        │
        │   (scope, risk tier,  │
        │    validation plan)   │
        └───────────┬───────────┘
                    ▼
             ┌───────────┐
             │Prioritized│
             └─────┬─────┘
                   ▼
            ┌────────────┐
        ┌──▶│In Progress │◀──┐
        │   └──┬─────┬──┘   │
        │      │     │      │
        │      │     ▼      │
        │      │  ┌───────┐ │
        │      │  │Blocked├─┘
        │      │  └───────┘
        │      ▼
        │   ┌────────────────────┐
        │   │   Checkpoint B     │
        │   │   (validate, merge)│
        │   └────────┬───────────┘
        │            ▼
        │   ┌────────────────────┐
        │   │   Checkpoint C     │
        │   │   (learning)       │
        │   └────────┬───────────┘
        │            ▼
        │      ┌──────┐
        └──────│ Done │
               └──────┘
```

**Checkpoint A**: BL issue body is complete — scope, non-goals, risk tier, validation plan, learning question. Status moves to Prioritized or In Progress.

**Execution**: Work happens through one or more AI Agent plan-then-execute cycles. Each cycle produces commits on the BL branch.

**Checkpoint B**: Validation complete per the risk tier requirements. Release decision: Ship / Ship with Conditions / Hold. Merge to main.

**Checkpoint C**: Post-merge learning captured — outcome vs goal, quality learning, next-loop implications. Status moves to Done. Issue closed.

## Kind Promotion

| Action | Command | What happens |
|--------|---------|-------------|
| Idea → Roadmap | `solo-os gh-promote --repo R --issue N --kind Roadmap` | Updates title prefix to `[Roadmap]`, sets Kind=Roadmap, Status=Prioritized |
| Roadmap → Build Loop | Manual issue creation | Create a new BL issue with parent linkage to the Roadmap item |
| Direct to Build Loop | Manual issue creation | Create a BL issue with rationale in Parent Linkage section |

## Stage Semantics

Stage is a planning-horizon field that tracks temporal focus, independent of Status. It applies to all Kinds.

| Stage | Meaning | WIP Limit |
|-------|---------|-----------|
| Inbox | Captured but not triaged | - |
| Today | Committed to advance today | 3 items across all repos |
| This Week | Committed to advance this week | 7 items across all repos |
| Waiting | Not urgent, parked, or blocked on external dependency | - |

Additional constraint: at most 1 Build Loop in `Stage = Today` per repo.

Stage and Status are orthogonal:
- **Status** answers "where is this in the execution lifecycle?"
- **Stage** answers "when am I choosing to touch this?"

## Daily Triage

1. Run `solo-os daily-triage` to review current stage assignments.
2. Validate Today — still the right 1-3 things?
3. Pull from This Week as capacity opens.
4. Check Waiting — anything unblocked?
5. Execute Today in priority order.

## Weekly Review

1. Triage Inbox into This Week, Waiting, or close.
2. Review This Week completion rate.
3. Re-stage next week from Waiting pool.
4. Retro: was the week's staging realistic?

## Execution Guidance (brief; details in BL #17)

Build Loops are executed through one or more AI Agent plan-then-execute cycles, each producing commits on the BL branch. The detailed agent skills, commands, and enforcement for this guidance will be defined in BL #17 (agent/skill generalization).

## Anti-Patterns

- Do not use Roadmap as a generic bucket of tasks.
- Do not create Build Loops for vague, indefinite efforts with no concrete output.
- Do not skip Checkpoint A — every BL needs scope, non-goals, and a risk tier before execution.
- Do not expand scope mid-loop without revisiting Checkpoint A.
- Do not use markdown files as active status boards — keep active state in GitHub.
- Do not force child tasks by default — a Build Loop plus commits/PRs is usually sufficient.
