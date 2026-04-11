"""Daily triage for Solo OS: review all open items across Stage, flag WIP violations, suggest moves."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from typing import Any

from solo_os import config
from solo_os.display import (
    ANSI_BOLD,
    ANSI_BLUE,
    ANSI_CYAN,
    ANSI_DIM,
    ANSI_GREEN,
    ANSI_MAGENTA,
    ANSI_RED,
    ANSI_YELLOW,
    color_enabled,
    display_title,
    paint,
    short_repo_name,
    terminal_width,
)
from solo_os.github_ops import (
    ProjectIssueItem,
    field_and_option_ids,
    get_project_config,
    gh_project_metadata,
    list_project_items,
    set_single_select,
)

STATUS_PRIORITY = {
    "In Progress": 0,
    "Prioritized": 1,
    "Todo": 2,
    "Backlog": 3,
    "Blocked": 4,
}

KIND_ICON = {
    "Build Loop": "BL",
    "Roadmap": "RM",
    "Idea": "ID",
}


def sort_key(item: ProjectIssueItem) -> tuple[int, str, int]:
    return (STATUS_PRIORITY.get(item.status, 99), item.repo, item.number)


def load_triage_config() -> dict[str, int]:
    triage = config.settings("daily_triage")
    return {
        "today_limit": int(triage.get("today_limit", 3)),
        "this_week_limit": int(triage.get("this_week_limit", 7)),
        "max_bl_per_repo_today": int(triage.get("max_build_loops_per_repo_today", 1)),
    }


def render_item_line(item: ProjectIssueItem, enabled: bool) -> str:
    kind_tag = KIND_ICON.get(item.kind, "??")
    repo = paint(short_repo_name(item.repo), ANSI_DIM, enabled=enabled)
    status = item.status or "-"
    status_colored = status
    if status == "In Progress":
        status_colored = paint(status, ANSI_BOLD, ANSI_BLUE, enabled=enabled)
    elif status == "Prioritized":
        status_colored = paint(status, ANSI_YELLOW, enabled=enabled)
    elif status == "Blocked":
        status_colored = paint(status, ANSI_RED, enabled=enabled)
    elif status == "Todo":
        status_colored = paint(status, ANSI_MAGENTA, enabled=enabled)
    title = display_title(item.title)
    return f"  [{kind_tag}] {repo} #{item.number}  {status_colored}  {title}"


def render_stage_section(
    stage_name: str,
    items: list[ProjectIssueItem],
    enabled: bool,
    width: int,
    *,
    limit_label: str = "",
) -> list[str]:
    header = f"{stage_name} ({len(items)})"
    if limit_label:
        header += f"  {limit_label}"
    lines = [paint(header, ANSI_BOLD, enabled=enabled)]
    if not items:
        lines.append(paint("  (empty)", ANSI_DIM, enabled=enabled))
    else:
        for item in sorted(items, key=sort_key):
            lines.append(render_item_line(item, enabled))
    return lines


def compute_recommendations(
    items: list[ProjectIssueItem],
    today_items: list[ProjectIssueItem],
    this_week_items: list[ProjectIssueItem],
    limits: dict[str, int],
) -> dict[str, list[ProjectIssueItem]]:
    move_to_today: list[ProjectIssueItem] = []
    for item in items:
        if item.status == "In Progress" and item.stage != "Today":
            move_to_today.append(item)

    done_still_staged: list[ProjectIssueItem] = []
    for item in items:
        if item.status == "Done" and item.stage and item.stage != "":
            done_still_staged.append(item)

    no_stage: list[ProjectIssueItem] = []
    for item in items:
        if not item.stage and item.status != "Done":
            no_stage.append(item)

    return {
        "move_to_today": move_to_today,
        "move_out_of_today": [],
        "done_still_staged": done_still_staged,
        "no_stage": no_stage,
    }


def compute_warnings(
    today_items: list[ProjectIssueItem],
    this_week_items: list[ProjectIssueItem],
    limits: dict[str, int],
    enabled: bool,
) -> list[str]:
    warnings: list[str] = []

    def warn(msg: str) -> None:
        warnings.append(paint(f"  \u26a0 {msg}", ANSI_YELLOW, enabled=enabled))

    if len(today_items) > limits["today_limit"]:
        warn(f"Today has {len(today_items)} items (limit: {limits['today_limit']})")

    if len(this_week_items) > limits["this_week_limit"]:
        warn(f"This Week has {len(this_week_items)} items (limit: {limits['this_week_limit']})")

    bl_per_repo: dict[str, list[ProjectIssueItem]] = defaultdict(list)
    for item in today_items:
        if item.kind == "Build Loop":
            bl_per_repo[item.repo].append(item)
    max_bl = limits["max_bl_per_repo_today"]
    for repo, bl_items in bl_per_repo.items():
        if len(bl_items) > max_bl:
            warn(f"{short_repo_name(repo)} has {len(bl_items)} Build Loops in Today (limit: {max_bl}/repo)")

    return warnings


def apply_stage_moves(
    cfg: dict[str, Any],
    moves: list[tuple[ProjectIssueItem, str]],
) -> list[str]:
    if not moves:
        return ["No stage changes to apply."]

    project_id, fields_json = gh_project_metadata(cfg)
    stage_field = str(cfg.get("stageFieldName") or "Stage")
    results: list[str] = []
    for item, target_stage in moves:
        field_id, option_id = field_and_option_ids(fields_json, stage_field, target_stage)
        set_single_select(project_id, item.item_id, field_id, option_id)
        results.append(f"  Moved #{item.number} ({short_repo_name(item.repo)}) -> {target_stage}")
    return results


def build_json_output(
    by_stage: dict[str, list[ProjectIssueItem]],
    recommendations: dict[str, list[ProjectIssueItem]],
    warnings: list[str],
    limits: dict[str, int],
) -> dict[str, Any]:
    def items_to_dicts(items: list[ProjectIssueItem]) -> list[dict[str, Any]]:
        return [
            {
                "repo": short_repo_name(i.repo),
                "number": i.number,
                "kind": i.kind,
                "status": i.status,
                "stage": i.stage,
                "title": display_title(i.title),
            }
            for i in sorted(items, key=sort_key)
        ]

    return {
        "stages": {stage: items_to_dicts(items) for stage, items in by_stage.items()},
        "recommendations": {key: items_to_dicts(items) for key, items in recommendations.items()},
        "warnings": warnings,
        "limits": limits,
    }


def handle_daily_triage(args: argparse.Namespace) -> int:
    enabled = color_enabled(args.color)
    width = terminal_width()

    cfg = get_project_config()
    limits = load_triage_config()
    all_items = list_project_items(cfg, state="open")

    by_stage: dict[str, list[ProjectIssueItem]] = {
        "Today": [],
        "This Week": [],
        "Waiting": [],
        "Inbox": [],
        "(no stage)": [],
    }
    for item in all_items:
        if item.status == "Done":
            continue
        stage = item.stage
        if stage in by_stage:
            by_stage[stage].append(item)
        elif not stage:
            by_stage["(no stage)"].append(item)
        else:
            by_stage.setdefault(stage, []).append(item)

    today_items = by_stage["Today"]
    this_week_items = by_stage["This Week"]
    recommendations = compute_recommendations(all_items, today_items, this_week_items, limits)
    warnings = compute_warnings(today_items, this_week_items, limits, enabled=False)

    if args.format == "json":
        print(json.dumps(build_json_output(by_stage, recommendations, warnings, limits), indent=2))
        if args.apply:
            moves: list[tuple[ProjectIssueItem, str]] = []
            for item in recommendations["move_to_today"]:
                moves.append((item, "Today"))
            results = apply_stage_moves(cfg, moves)
            for line in results:
                print(line, file=sys.stderr)
        return 0

    banner = "=" * width
    print(paint(banner, ANSI_CYAN, enabled=enabled))
    print(paint("DAILY TRIAGE", ANSI_BOLD, ANSI_CYAN, enabled=enabled))
    print(paint(banner, ANSI_CYAN, enabled=enabled))
    print()

    stage_order = ["Today", "This Week", "Waiting", "Inbox", "(no stage)"]
    for stage in stage_order:
        items = by_stage.get(stage, [])
        if stage == "Today":
            limit_label = paint(f"[limit: {limits['today_limit']}]", ANSI_DIM, enabled=enabled)
        elif stage == "This Week":
            limit_label = paint(f"[limit: {limits['this_week_limit']}]", ANSI_DIM, enabled=enabled)
        else:
            limit_label = ""
        lines = render_stage_section(stage, items, enabled, width, limit_label=limit_label)
        for line in lines:
            print(line)
        print()

    colored_warnings = compute_warnings(today_items, this_week_items, limits, enabled)
    if colored_warnings:
        print(paint("Warnings", ANSI_BOLD, ANSI_YELLOW, enabled=enabled))
        for w in colored_warnings:
            print(w)
        print()

    has_recs = any(recommendations.values())
    if has_recs:
        print(paint("Recommendations", ANSI_BOLD, ANSI_GREEN, enabled=enabled))
        if recommendations["move_to_today"]:
            print(paint("  Move to Today (In Progress but not staged there):", ANSI_GREEN, enabled=enabled))
            for item in recommendations["move_to_today"]:
                print(f"    #{item.number} {short_repo_name(item.repo)}  {display_title(item.title)}")
        if recommendations["no_stage"]:
            print(paint("  Needs triage (no Stage set):", ANSI_MAGENTA, enabled=enabled))
            for item in sorted(recommendations["no_stage"], key=sort_key):
                kind_tag = KIND_ICON.get(item.kind, "??")
                print(
                    f"    [{kind_tag}] #{item.number} {short_repo_name(item.repo)}  {item.status}  {display_title(item.title)}"
                )
        if recommendations["done_still_staged"]:
            print(paint("  Done but still staged (clean up):", ANSI_DIM, enabled=enabled))
            for item in recommendations["done_still_staged"]:
                print(
                    f"    #{item.number} {short_repo_name(item.repo)}  Stage={item.stage}  {display_title(item.title)}"
                )
        print()

    if not args.apply:
        mode = paint("DRY-RUN", ANSI_YELLOW, enabled=enabled)
        print(f"Mode: {mode} \u2014 re-run with --apply to persist stage changes.")
        return 0

    moves_list: list[tuple[ProjectIssueItem, str]] = []
    for item in recommendations["move_to_today"]:
        moves_list.append((item, "Today"))

    if moves_list:
        print(paint("Applying stage changes...", ANSI_BOLD, enabled=enabled))
        results = apply_stage_moves(cfg, moves_list)
        for line in results:
            print(line)
    else:
        print("No automatic stage changes to apply.")

    print()
    print(paint("Daily triage complete.", ANSI_GREEN, enabled=enabled))
    return 0
