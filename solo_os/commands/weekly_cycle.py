"""Run weekly Solo OS maintenance cycle: sync-audit then cleanup-markdown."""

from __future__ import annotations

import argparse

from solo_os.commands.cleanup_markdown import handle_cleanup_markdown
from solo_os.commands.sync_audit import handle_sync_audit


def handle_weekly_cycle(args: argparse.Namespace) -> int:
    print("== Weekly Solo OS Cycle ==")

    print("\n1) Sync audit")
    code = handle_sync_audit()
    if code != 0:
        print("\nStopped: sync-audit failed.")
        return code

    print("\n2) Markdown cleanup (dry-run)")
    cleanup_args = argparse.Namespace(apply=False, repo=None)
    code = handle_cleanup_markdown(cleanup_args)
    if code != 0:
        print("\nStopped: cleanup-markdown failed.")
        return code

    print("\nWeekly cycle complete.")
    return 0
