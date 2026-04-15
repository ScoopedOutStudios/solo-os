"""Single command entrypoint for solo-os operations."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="solo-os",
        description="CLI toolkit for solo/small-team project governance on GitHub Projects V2",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- gh-list ---
    gh_list = subparsers.add_parser("gh-list", help="List project-backed GitHub issues")
    gh_list.add_argument("--repo", help="Repo alias or owner/name")
    gh_list.add_argument("--kind", help="Filter by Kind")
    gh_list.add_argument("--status", help="Filter by Status")
    gh_list.add_argument("--stage", help="Filter by Stage")
    gh_list.add_argument("--state", choices=["open", "closed", "all"], default="open")
    gh_list.add_argument("--search", help="Simple text search against title/body")
    gh_list.add_argument("--limit", type=int, default=20)
    gh_list.add_argument("--format", choices=["table", "json"], default="table")

    # --- gh-next ---
    gh_next = subparsers.add_parser("gh-next", help="Show the next actionable project-backed items")
    gh_next.add_argument("--repo", help="Repo alias or owner/name")
    gh_next.add_argument("--include-ideas", action="store_true", help="Include Idea items in shortlist")
    gh_next.add_argument("--limit", type=int, default=10)
    gh_next.add_argument("--format", choices=["table", "json"], default="table")

    # --- gh-brief ---
    gh_brief = subparsers.add_parser("gh-brief", help="Answer common planning questions with pretty output")
    gh_brief.add_argument(
        "--question",
        required=True,
        choices=["in-progress-ideas", "roadmap-now", "active-work"],
        help="Named planning question to answer",
    )
    gh_brief.add_argument("--repo", help="Repo alias or owner/name")
    gh_brief.add_argument("--limit", type=int, default=5)
    gh_brief.add_argument("--format", choices=["pretty", "json"], default="pretty")
    gh_brief.add_argument("--view", choices=["compact", "pretty", "full"], default="pretty")
    gh_brief.add_argument("--color", choices=["auto", "always", "never"], default="auto")

    # --- gh-update ---
    gh_update = subparsers.add_parser("gh-update", help="Update issue content and/or project fields")
    gh_update.add_argument("--repo", required=True, help="Repo alias or owner/name")
    gh_update.add_argument("--issue", required=True, type=int, help="Issue number")
    gh_update.add_argument("--title", help="Replace the issue title")
    body_group = gh_update.add_mutually_exclusive_group()
    body_group.add_argument("--body", help="Replace the issue body with inline text")
    body_group.add_argument("--body-file", help="Replace the issue body from a file path")
    gh_update.add_argument("--append-body", help="Append markdown to the existing body")
    gh_update.add_argument("--kind", help="Set the project Kind field")
    gh_update.add_argument("--status", help="Set the project Status field")
    gh_update.add_argument("--stage", help="Set the project Stage field")
    gh_update.add_argument("--dry-run", action="store_true", help="Preview the mutation without applying it")

    # --- gh-promote ---
    gh_promote = subparsers.add_parser("gh-promote", help="Promote an issue to a different Kind")
    gh_promote.add_argument("--repo", required=True, help="Repo alias or owner/name")
    gh_promote.add_argument("--issue", required=True, type=int, help="Issue number")
    gh_promote.add_argument("--kind", default="Roadmap", help="Target Kind")
    gh_promote.add_argument("--status", default="Prioritized", help="Target Status")
    gh_promote.add_argument("--dry-run", action="store_true", help="Preview the mutation without applying it")

    # --- gh-close ---
    gh_close = subparsers.add_parser("gh-close", help="Close an issue and sync project status")
    gh_close.add_argument("--repo", required=True, help="Repo alias or owner/name")
    gh_close.add_argument("--issue", required=True, type=int, help="Issue number")
    gh_close.add_argument("--reason", choices=["completed", "not_planned"], default="completed")
    gh_close.add_argument("--comment", help="Optional closing comment")
    gh_close.add_argument("--status", default="Done", help="Project Status to set before closing")
    gh_close.add_argument("--dry-run", action="store_true", help="Preview the mutation without applying it")

    # --- gh-migrate-titles ---
    gh_migrate = subparsers.add_parser("gh-migrate-titles", help="Rename legacy workflow issue prefixes")
    gh_migrate.add_argument("--repo", help="Repo alias or owner/name")
    gh_migrate.add_argument("--state", choices=["open", "closed", "all"], default="open")
    gh_migrate.add_argument("--apply", action="store_true", help="Apply the title migration")
    gh_migrate.add_argument("--format", choices=["table", "json"], default="table")

    # --- daily-triage ---
    daily_triage = subparsers.add_parser(
        "daily-triage", help="Daily triage: review stages, flag WIP violations, suggest moves"
    )
    daily_triage.add_argument("--apply", action="store_true", help="Persist recommended stage changes")
    daily_triage.add_argument("--color", choices=["auto", "always", "never"], default="auto")
    daily_triage.add_argument("--format", choices=["pretty", "json"], default="pretty")

    # --- sync-audit ---
    subparsers.add_parser("sync-audit", help="Run local sync audit checks")

    # --- verify ---
    verify = subparsers.add_parser("verify", help="Validate environment, config, and project setup")
    verify.add_argument("--path", default=".", help="Directory to start config discovery from")
    verify.add_argument("--format", choices=["table", "json"], default="table")

    # --- init ---
    init_cmd = subparsers.add_parser("init", help="Guided setup for solo-os.yml and GitHub Project fields")
    init_cmd.add_argument("--yes", action="store_true", help="Non-interactive mode using defaults")
    init_cmd.add_argument("--owner", help="GitHub owner (org or user)")
    init_cmd.add_argument("--owner-type", choices=["org", "user"], help="Owner type override")
    init_cmd.add_argument("--project", type=int, help="Existing GitHub Project number")
    init_cmd.add_argument("--project-title", default="Solo OS Planning", help="Project title when creating")
    init_cmd.add_argument("--mode", choices=["single", "multi"], help="Single-repo or multi-repo setup")
    init_cmd.add_argument("--repo-id", help="Repo alias to write into solo-os.yml")
    init_cmd.add_argument("--repo-path", help="Repo path to write into solo-os.yml")
    init_cmd.add_argument("--config-path", help="Output path for generated solo-os.yml")
    init_cmd.add_argument("--force", action="store_true", help="Overwrite existing config file")
    init_cmd.add_argument("--format", choices=["table", "json"], default="table")

    # --- cleanup-markdown ---
    cleanup = subparsers.add_parser("cleanup-markdown", help="Archive redundant markdown artifacts")
    cleanup.add_argument("--apply", action="store_true", help="Move cleanup candidates to archive")
    cleanup.add_argument("--repo", help="Optional repo id to scope cleanup")

    # --- bl-review ---
    bl_review = subparsers.add_parser("bl-review", help="Review a Build Loop issue for Checkpoint A readiness")
    bl_review.add_argument("--repo", required=True, help="Repo alias or owner/name")
    bl_review.add_argument("--issue", required=True, type=int, help="Build Loop issue number")
    bl_review.add_argument("--format", choices=["table", "json"], default="table")
    bl_review.add_argument("--color", choices=["auto", "always", "never"], default="auto")

    # --- bl-status ---
    bl_status = subparsers.add_parser("bl-status", help="Show open Build Loop issues across repos")
    bl_status.add_argument("--repo", help="Optional repo alias or owner/name")
    bl_status.add_argument("--limit", type=int, default=20, help="Maximum items to show")
    bl_status.add_argument("--format", choices=["table", "json"], default="table")
    bl_status.add_argument("--color", choices=["auto", "always", "never"], default="auto")

    # --- weekly-cycle ---
    subparsers.add_parser("weekly-cycle", help="Run weekly maintenance: sync-audit then cleanup-markdown")

    # --- build-loop-template ---
    blt = subparsers.add_parser("build-loop-template", help="Print the canonical Build Loop issue body template")
    blt.add_argument("--kind", choices=["idea", "roadmap", "build-loop"], default="build-loop",
                     help="Which template to print")
    blt.add_argument("--path-only", action="store_true", help="Print only the template path")

    return parser


def _template_path(kind: str) -> Path:
    """Resolve the path to a bundled issue body template."""
    template_names = {
        "idea": "idea-body-template.md",
        "roadmap": "roadmap-body-template.md",
        "build-loop": "build-loop-body-template.md",
    }
    filename = template_names.get(kind, "build-loop-body-template.md")
    pkg_dir = Path(__file__).resolve().parent
    return pkg_dir / "templates" / filename


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    try:
        if args.command == "gh-list":
            from solo_os.commands.github_ops import handle_list
            return handle_list(args)
        if args.command == "gh-next":
            from solo_os.commands.github_ops import handle_next
            return handle_next(args)
        if args.command == "gh-brief":
            from solo_os.commands.github_ops import handle_brief
            return handle_brief(args)
        if args.command == "gh-update":
            from solo_os.commands.github_ops import handle_update
            return handle_update(args)
        if args.command == "gh-promote":
            from solo_os.commands.github_ops import handle_promote
            return handle_promote(args)
        if args.command == "gh-close":
            from solo_os.commands.github_ops import handle_close
            return handle_close(args)
        if args.command == "gh-migrate-titles":
            from solo_os.commands.github_ops import handle_migrate_titles
            return handle_migrate_titles(args)
        if args.command == "daily-triage":
            from solo_os.commands.daily_triage import handle_daily_triage
            return handle_daily_triage(args)
        if args.command == "sync-audit":
            from solo_os.commands.sync_audit import handle_sync_audit
            return handle_sync_audit()
        if args.command == "verify":
            from solo_os.commands.onboarding import handle_doctor
            return handle_doctor(args)
        if args.command == "init":
            from solo_os.commands.onboarding import handle_init
            return handle_init(args)
        if args.command == "cleanup-markdown":
            from solo_os.commands.cleanup_markdown import handle_cleanup_markdown
            return handle_cleanup_markdown(args)
        if args.command == "bl-review":
            from solo_os.commands.build_loop import handle_bl_review
            return handle_bl_review(args)
        if args.command == "bl-status":
            from solo_os.commands.build_loop import handle_bl_status
            return handle_bl_status(args)
        if args.command == "weekly-cycle":
            from solo_os.commands.weekly_cycle import handle_weekly_cycle
            return handle_weekly_cycle(args)
        if args.command == "build-loop-template":
            kind = getattr(args, "kind", "build-loop")
            tpl = _template_path(kind)
            if args.path_only:
                print(tpl)
            else:
                if not tpl.exists():
                    print(f"Template not found: {tpl}", file=sys.stderr)
                    return 1
                print(tpl.read_text(encoding="utf-8"), end="")
            return 0
    except KeyboardInterrupt:
        return 130
    except (RuntimeError, FileNotFoundError, ImportError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
