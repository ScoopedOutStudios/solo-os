# Active-Only Migration Checklist

Use this checklist when migrating to Solo OS. Do not bulk-migrate historical artifacts.

## Scope

- Confirm active repositories in `solo-os.yml`
- Confirm active build loops and next-up loops per repo
- Confirm ideas/opportunities worth carrying forward

## Per-Repo Migration

- GitHub Project item exists for active work
- GitHub entrypoint exists (issues/PRs/repo links)
- Execution links section exists for active items

## Closeout

- Run `solo-os sync-audit`
- Resolve all errors; accept warnings with explicit rationale
- Log migration completion date in repo notes