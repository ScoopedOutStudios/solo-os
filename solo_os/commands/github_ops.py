"""Query and update GitHub issues/project items for Solo OS."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from solo_os import config
from solo_os.display import (
    ANSI_BOLD,
    ANSI_CYAN,
    ANSI_DIM,
    color_enabled,
    display_title,
    kind_display,
    paint,
    short_repo_name,
    status_display,
    terminal_width,
    wrap_block,
)
from solo_os.github_ops import (
    add_issue_to_project,
    close_issue,
    comment_on_issue,
    create_issue,
    ensure_project_item,
    edit_issue,
    get_project_config,
    issue_view,
    list_project_items,
    resolve_repo,
    update_project_fields,
)

STATUS_ORDER = {
    "In Progress": 0,
    "Prioritized": 1,
    "Todo": 2,
    "Backlog": 3,
    "Blocked": 4,
    "Done": 5,
}

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"


def _body_template_path(kind: str) -> Path:
    template_names = {
        "idea": "idea-body-template.md",
        "roadmap": "roadmap-body-template.md",
        "build-loop": "build-loop-body-template.md",
    }
    key = str(kind or "").strip().lower()
    filename = template_names.get(key)
    if not filename:
        expected = ", ".join(sorted(template_names))
        raise RuntimeError(
            f"Unknown template kind '{kind}'. Expected one of: {expected}"
        )
    return _TEMPLATE_DIR / filename


def row_for_item(item: Any) -> dict[str, str]:
    return {
        "repo": item.repo,
        "issue": f"#{item.number}",
        "kind": item.kind or "-",
        "status": item.status or "-",
        "stage": item.stage or "-",
        "state": item.state.lower(),
        "title": display_title(item.title),
    }


def format_rows(items: list[dict[str, str]]) -> str:
    if not items:
        return "No matching items."

    headers = ["repo", "issue", "kind", "status", "stage", "state", "title"]
    widths = {header: len(header) for header in headers}
    for item in items:
        for header in headers:
            widths[header] = max(widths[header], len(str(item[header])))

    lines = []
    header_line = "  ".join(header.ljust(widths[header]) for header in headers)
    divider = "  ".join("-" * widths[header] for header in headers)
    lines.append(header_line)
    lines.append(divider)
    for item in items:
        lines.append("  ".join(str(item[header]).ljust(widths[header]) for header in headers))
    return "\n".join(lines)


def print_items(items: list[dict[str, str]], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(items, indent=2))
        return
    print(format_rows(items))


def extract_section(body: str, heading: str) -> str:
    marker = f"## {heading}"
    start_idx = body.find(marker)
    if start_idx == -1:
        return ""
    start_idx += len(marker)
    end_idx = body.find("\n## ", start_idx)
    if end_idx == -1:
        end_idx = len(body)
    return body[start_idx:end_idx].strip()


def needs_title_migration(title: str) -> bool:
    return title != display_title(title)


def prefix_title(title: str, kind: str) -> str:
    suffix = title
    if title.startswith("[") and "]" in title:
        suffix = title[title.index("]") + 1 :].strip()
    return f"[{kind}] {suffix}".strip()


def body_from_args(args: argparse.Namespace, repo: str) -> str | None:
    if args.body is not None:
        return str(args.body)
    if args.body_file is not None:
        return Path(args.body_file).read_text(encoding="utf-8")
    if args.append_body is not None:
        current = issue_view(repo, int(args.issue))
        base = str(current.get("body") or "").rstrip()
        addition = str(args.append_body).strip()
        if not base:
            return addition
        return f"{base}\n\n{addition}\n"
    return None


def summary_for_item(item: Any) -> str:
    summary = extract_section(item.body, "Summary")
    if summary:
        return " ".join(line.strip() for line in summary.splitlines() if line.strip())
    return display_title(item.title)


def context_lines_for_item(item: Any, limit: int = 3) -> list[str]:
    context = extract_section(item.body, "Context")
    if not context:
        return []
    lines: list[str] = []
    for raw_line in context.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("- "):
            lines.append(line)
        else:
            lines.append(f"- {line}")
        if len(lines) >= limit:
            break
    return lines


def compact_meta_line(item: Any, enabled: bool) -> str:
    repo = paint(short_repo_name(item.repo), ANSI_DIM, enabled=enabled)
    kind = kind_display(item.kind, enabled)
    status = status_display(item.status, enabled)
    return f"  {repo}  #{item.number}  {kind}  {status}"


def render_compact_card(item: Any, index: int, enabled: bool, width: int) -> str:
    title = paint(f"[{index}] {display_title(item.title)}", ANSI_BOLD, enabled=enabled)
    summary = summary_for_item(item)
    lines = [
        title,
        compact_meta_line(item, enabled),
        wrap_block(summary, indent="  ", subsequent_indent="  ", width=width - 2),
    ]
    context = context_lines_for_item(item, limit=1)
    if context:
        lines.append(
            wrap_block(
                f"Context: {context[0][2:]}",
                indent="  ",
                subsequent_indent="           ",
                width=width - 2,
            )
        )
    return "\n".join(lines)


def render_pretty_card(item: Any, index: int, enabled: bool, width: int, *, full: bool) -> str:
    border = paint("-" * width, ANSI_DIM, enabled=enabled)
    lines = [border]
    lines.append(paint(f"[{index}] {display_title(item.title)}", ANSI_BOLD, enabled=enabled))
    lines.append(compact_meta_line(item, enabled))
    lines.append(
        wrap_block(
            f"Summary: {summary_for_item(item)}",
            indent="  ",
            subsequent_indent="           ",
            width=width - 2,
        )
    )

    context_limit = 5 if full else 2
    context = context_lines_for_item(item, limit=context_limit)
    if context:
        lines.append("  Context:")
        for entry in context:
            body = entry[2:] if entry.startswith("- ") else entry
            lines.append(
                wrap_block(f"- {body}", indent="    ", subsequent_indent="      ", width=width - 4)
            )
    if full:
        lines.append(f"  URL: {paint(item.url, ANSI_DIM, enabled=enabled)}")
    lines.append(border)
    return "\n".join(lines)


def print_brief(
    question: str,
    sections: list[tuple[str, list[Any]]],
    output_format: str,
    color_mode: str,
    view: str,
) -> None:
    if output_format == "json":
        payload = {
            "question": question,
            "sections": [
                {"title": title, "items": [item.as_dict() for item in items]}
                for title, items in sections
            ],
        }
        print(json.dumps(payload, indent=2))
        return

    enabled = color_enabled(color_mode)
    width = terminal_width()
    banner = "=" * width
    print(paint(banner, ANSI_CYAN, enabled=enabled))
    print(paint(question.upper(), ANSI_BOLD, ANSI_CYAN, enabled=enabled))
    print(paint(banner, ANSI_CYAN, enabled=enabled))
    for title, items in sections:
        print()
        print(paint(f"{title} ({len(items)})", ANSI_BOLD, enabled=enabled))
        if not items:
            print(f"  {paint('None.', ANSI_DIM, enabled=enabled)}")
            continue
        for index, item in enumerate(items, start=1):
            if view == "compact":
                print(render_compact_card(item, index, enabled, width))
            elif view == "full":
                print(render_pretty_card(item, index, enabled, width, full=True))
            else:
                print(render_pretty_card(item, index, enabled, width, full=False))
            if index != len(items):
                print()


# --- Command handlers ---


def handle_list(args: argparse.Namespace) -> int:
    cfg = get_project_config()
    items = list_project_items(
        cfg,
        repo=args.repo,
        kind=args.kind,
        status=args.status,
        state=args.state,
        search=args.search,
    )
    if args.stage:
        items = [item for item in items if item.stage == args.stage]
    rows = [row_for_item(item) for item in items[: args.limit]]
    print_items(rows, args.format)
    return 0


def handle_next(args: argparse.Namespace) -> int:
    cfg = get_project_config()
    items = list_project_items(cfg, repo=args.repo, state="open")
    allowed_kinds = {"Roadmap", "Build Loop"}
    if args.include_ideas:
        allowed_kinds.add("Idea")

    actionable = [
        item
        for item in items
        if item.kind in allowed_kinds and item.status in {"In Progress", "Prioritized", "Todo"}
    ]
    if not actionable:
        actionable = [item for item in items if item.kind in allowed_kinds and item.status == "Backlog"]

    actionable.sort(
        key=lambda item: (
            STATUS_ORDER.get(item.status, 999),
            item.repo,
            item.number,
        )
    )
    rows = [row_for_item(item) for item in actionable[: args.limit]]
    print_items(rows, args.format)
    return 0


def handle_brief(args: argparse.Namespace) -> int:
    cfg = get_project_config()
    items = list_project_items(cfg, repo=args.repo, state="open")

    if args.question == "in-progress-ideas":
        scoped = [item for item in items if item.kind == "Idea" and item.status == "In Progress"]
        scoped.sort(key=lambda item: (item.repo, item.number))
        print_brief(
            "What are the in-progress Ideas?",
            [("In-progress ideas", scoped[: args.limit])],
            args.format,
            args.color,
            args.view,
        )
        return 0

    if args.question == "roadmap-now":
        in_progress = [item for item in items if item.kind == "Roadmap" and item.status == "In Progress"]
        next_up = [item for item in items if item.kind == "Roadmap" and item.status == "Prioritized"]
        in_progress.sort(key=lambda item: (item.repo, item.number))
        next_up.sort(key=lambda item: (item.repo, item.number))
        print_brief(
            "What is next on the roadmap and what is currently in progress?",
            [
                ("Roadmap items in progress", in_progress[: args.limit]),
                ("Next prioritized roadmap items", next_up[: args.limit]),
            ],
            args.format,
            args.color,
            args.view,
        )
        return 0

    if args.question == "active-work":
        in_progress = [item for item in items if item.status == "In Progress"]
        ready_next = [item for item in items if item.status == "Prioritized"]
        in_progress.sort(
            key=lambda item: (STATUS_ORDER.get(item.status, 999), item.repo, item.number)
        )
        ready_next.sort(key=lambda item: (item.kind, item.repo, item.number))
        print_brief(
            "What is actively being worked and what is ready next?",
            [
                ("Currently in progress", in_progress[: args.limit]),
                ("Ready next", ready_next[: args.limit]),
            ],
            args.format,
            args.color,
            args.view,
        )
        return 0

    raise RuntimeError(f"Unsupported question: {args.question}")


def handle_update(args: argparse.Namespace) -> int:
    cfg = get_project_config()
    repo = resolve_repo(args.repo)
    new_body = body_from_args(args, repo)
    if not any([args.title, new_body is not None, args.kind, args.status, args.stage]):
        raise RuntimeError(
            "Provide at least one mutation flag: --title, --body/--body-file/--append-body, --kind, --status, or --stage"
        )

    planned = {
        "repo": repo,
        "issue": args.issue,
        "title": args.title,
        "body_changed": new_body is not None,
        "kind": args.kind,
        "status": args.status,
        "stage": args.stage,
    }
    if args.dry_run:
        print(json.dumps(planned, indent=2))
        return 0

    if args.title or new_body is not None:
        edit_issue(repo, int(args.issue), title=args.title, body=new_body)
    if args.kind or args.status or args.stage:
        update_project_fields(cfg, repo, int(args.issue), kind=args.kind, status=args.status, stage=args.stage)
    print(json.dumps({**planned, "applied": True}, indent=2))
    return 0


def handle_promote(args: argparse.Namespace) -> int:
    cfg = get_project_config()
    repo = resolve_repo(args.repo)
    issue = issue_view(repo, int(args.issue))
    new_title = prefix_title(str(issue["title"]), str(args.kind))
    planned = {
        "repo": repo,
        "issue": args.issue,
        "old_title": issue["title"],
        "new_title": new_title,
        "kind": args.kind,
        "status": args.status,
    }
    if args.dry_run:
        print(json.dumps(planned, indent=2))
        return 0

    edit_issue(repo, int(args.issue), title=new_title)
    update_project_fields(cfg, repo, int(args.issue), kind=args.kind, status=args.status)
    print(json.dumps({**planned, "applied": True}, indent=2))
    return 0


def handle_close(args: argparse.Namespace) -> int:
    cfg = get_project_config()
    repo = resolve_repo(args.repo)
    planned = {
        "repo": repo,
        "issue": args.issue,
        "reason": args.reason,
        "comment": args.comment,
        "status": args.status,
    }
    if args.dry_run:
        print(json.dumps(planned, indent=2))
        return 0

    if args.comment:
        comment_on_issue(repo, int(args.issue), str(args.comment))
    if args.status:
        update_project_fields(cfg, repo, int(args.issue), status=args.status)
    close_issue(repo, int(args.issue), reason=str(args.reason))
    print(json.dumps({**planned, "applied": True}, indent=2))
    return 0


def handle_migrate_titles(args: argparse.Namespace) -> int:
    cfg = get_project_config()
    items = list_project_items(cfg, repo=args.repo, state=args.state)
    candidates = [item for item in items if needs_title_migration(item.title)]

    rows = [
        {
            "repo": item.repo,
            "issue": f"#{item.number}",
            "kind": item.kind or "-",
            "status": item.status or "-",
            "state": item.state.lower(),
            "title": item.title,
            "new_title": display_title(item.title),
        }
        for item in candidates
    ]

    if not args.apply:
        if args.format == "json":
            print(json.dumps(rows, indent=2))
        else:
            if not rows:
                print("No legacy workflow titles to migrate.")
            else:
                headers = ["repo", "issue", "kind", "status", "state", "title", "new_title"]
                widths = {header: len(header) for header in headers}
                for row in rows:
                    for header in headers:
                        widths[header] = max(widths[header], len(str(row[header])))
                header_line = "  ".join(header.ljust(widths[header]) for header in headers)
                divider = "  ".join("-" * widths[header] for header in headers)
                print(header_line)
                print(divider)
                for row in rows:
                    print("  ".join(str(row[header]).ljust(widths[header]) for header in headers))
        return 0

    for item in candidates:
        edit_issue(item.repo, item.number, title=display_title(item.title))

    result = {
        "applied": True,
        "renamed_count": len(candidates),
        "issues": rows,
    }
    print(json.dumps(result, indent=2))
    return 0


def handle_create(args: argparse.Namespace) -> int:
    cfg = get_project_config()
    repo = resolve_repo(args.repo)

    title = str(args.title or "").strip()
    if not title:
        raise RuntimeError("--title is required")

    if args.body is not None:
        body = str(args.body)
    elif args.body_file is not None:
        body = Path(args.body_file).read_text(encoding="utf-8")
    elif args.from_template:
        template_path = _body_template_path(str(args.from_template))
        if not template_path.is_file():
            raise RuntimeError(f"Template not found: {template_path}")
        body = template_path.read_text(encoding="utf-8")
    else:
        body = ""

    labels: list[str] = []
    if args.label:
        labels.extend([str(x).strip() for x in args.label if str(x).strip()])

    planned: dict[str, Any] = {
        "repo": repo,
        "title": title,
        "body_chars": len(body),
        "labels": labels,
        "kind": args.kind,
        "status": args.status,
        "stage": args.stage,
        "add_to_project": bool(args.add_to_project),
    }
    if args.dry_run:
        print(json.dumps(planned, indent=2))
        return 0

    created = create_issue(repo, title=title, body=body, labels=labels or None)
    issue_number = int(created.get("number") or 0)
    if issue_number <= 0:
        raise RuntimeError(f"Could not parse created issue number from: {created}")

    if args.add_to_project:
        # Ensure the issue is represented as a project item, then set fields.
        issue = issue_view(repo, issue_number)
        owner = str((cfg or {}).get("owner") or "")
        project_number = int((cfg or {}).get("number") or 0)
        if not owner or project_number <= 0:
            raise RuntimeError("Config is missing github.owner or github.project.number; cannot add issue to project.")
        # Best-effort add; ensure_project_item retries until visible.
        add_issue_to_project(owner, project_number, str(issue.get("url") or ""))
        ensure_project_item(cfg, repo, issue_number)  # type: ignore[arg-type]
        if args.kind or args.status or args.stage:
            update_project_fields(cfg, repo, issue_number, kind=args.kind, status=args.status, stage=args.stage)

    result: dict[str, Any] = {
        **planned,
        "issue_number": issue_number,
        "url": str(created.get("url") or issue_view(repo, issue_number).get("url") or ""),
        "applied": True,
    }
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(
            f"Created {repo}#{issue_number} — {str(created.get('url') or result['url'])}"
        )
    return 0
