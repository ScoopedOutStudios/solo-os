# Git Commit Protocol (Solo OS)

Solo OS’s execution model is **not** a replacement for your repo’s engineering hygiene. The Build Loop is a **planning + discipline container**; the repo still enforces quality through your normal toolchains.

## Default posture

- **Use your repo’s real checks** (formatters, typecheck, tests) as the primary execution guardrails.
- **Prefer small, reviewable commits** with meaningful messages.
- **Do not bypass checks** to “save time” on risky loops, especially for user-facing and trust-sensitive changes.

## Branching (common Solo OS practice)

- For Build Loops, a dedicated branch is usually enough for solo/small team speed.
- **Isolated worktrees** are optional advanced ergonomics, not a requirement for using Solo OS.

## Relationship to build loop checkpoints

- **Checkpoint A** is primarily “do we have a real plan?” (Solo OS helps via templates + `solo-os bl-review`.)
- **Checkpoint B** is “are we actually safe to ship/merge for this risk tier?” — this is dominated by the repo’s checks + human judgment, not a Solo OS subcommand in the current CLI.
- **Checkpoint C** is “what did we learn?” — capture in the issue, release notes, and/or the next loop plan.

## Agent-generated execution

If you use AI agents to code:
- they should follow the **same** checks as a human
- the human still owns the merge/release decision, especially for `High` / `Critical` risk work

If an AI subagent or skill references commands that are not in `solo-os --help`, treat that as a documentation mismatch and prefer the **Python CLI** as the source of truth for what is shipped in this repository.