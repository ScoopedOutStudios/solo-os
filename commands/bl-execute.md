Use the Solo OS workflow in GitHub Projects/Issues.

Execute Build Loop <repo>#<issue-number> using Solo OS. Default to `simple mode` unless I explicitly ask for isolated worktree execution.

Please:
1. Run `bl-review` and summarize any gaps.
2. If simple mode is appropriate, stay in the current checkout and use a dedicated branch for the loop.
3. Only run `bl-prepare` and use a managed worktree if isolated mode is clearly warranted or I explicitly ask for it.
4. Run the required automated checks.
5. Stop before merge-back and report Checkpoint B readiness, blockers, and the recommended next action.

Do not run `bl-finish` unless I explicitly approve merge.
