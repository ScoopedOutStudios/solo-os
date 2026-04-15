Use the Solo OS workflow in GitHub Projects/Issues.

I approve merge-back for Build Loop <repo>#<issue-number> if it passes the Solo OS release gate. Default to simple mode unless this loop is explicitly running in isolated worktree mode.

Please:
1. Verify the issue status is `Ready To Merge`.
2. Verify `Checkpoint B Outcome` is substantive and the release decision is `Ship` or `Ship with Conditions`.
3. Verify the branch is synced and clean.
4. If this loop is using isolated mode, run `bl-finish`. Otherwise use the normal repo merge flow.
5. If successful, close the issue if appropriate and tell me what merged.
6. If blocked, do not merge; tell me exactly what blocker remains.
