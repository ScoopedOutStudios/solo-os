Use Solo OS to run my daily triage. Follow `docs/governance/workflow-system.md` for Stage semantics and WIP limits.

Please:
1. Run `daily-triage` and show the current state across all stages.
2. Flag any WIP violations or items needing attention.
3. Review what is in Today and pressure test whether this is still the right focus.
4. Recommend specific stage moves: what should move to Today, what should move out, and anything unblocked in Waiting.
5. Give a concise recommendation for what I should focus on today, not just a list.
6. If I approve, apply the stage changes using `daily-triage --apply` or individual `gh-update --stage` commands.
