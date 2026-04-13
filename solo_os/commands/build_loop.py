"""Build Loop review and status commands for Solo OS."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from solo_os import config
from solo_os.display import (
    ANSI_BOLD,
    ANSI_DIM,
    ANSI_GREEN,
    ANSI_RED,
    ANSI_YELLOW,
    color_enabled,
    display_title,
    kind_display,
    paint,
    short_repo_name,
    status_display,
    terminal_width,
)
from solo_os.github_ops import (
    get_project_config,
    get_project_item,
    issue_view,
    list_project_items,
    resolve_repo,
)

KIND_BUILD_LOOP = "Build Loop"

REVIEW_REQUIRED_HEADINGS = [
    "Summary",
    "Why Now",
    "Scope",
    "Non-Goals",
    "Parent Linkage",
    "Demoable Output",
    "Risk Tier",
    "Validation Plan",
    "Release / Rollback Plan",
    "Learning Question / Success Signal",
    "Context",
    "Evidence Links",
]

REVIEW_CRITICAL_HEADINGS = {
    "Summary",
    "Why Now",
    "Scope",
    "Non-Goals",
    "Demoable Output",
    "Risk Tier",
    "Validation Plan",
    "Learning Question / Success Signal",
    "Context",
}

REVIEW_ADVISORY_HEADINGS = {
    "Parent Linkage",
    "Release / Rollback Plan",
    "Evidence Links",
}

FUTURE_HEADINGS = {
    "Checkpoint B Outcome",
    "Checkpoint C Learning",
}


def _strip_markdown_tokens(line: str) -> str:
    stripped = line.strip()
    stripped = re.sub(r"^[-*]\s+", "", stripped)
    return stripped.strip()


def parse_markdown_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current_heading: str | None = None
    current_lines: list[str] = []
    for raw_line in text.splitlines():
        if raw_line.startswith("## "):
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = raw_line[3:].strip()
            current_lines = []
            continue
        if current_heading is not None:
            current_lines.append(raw_line)
    if current_heading is not None:
        sections[current_heading] = "\n".join(current_lines).strip()
    return sections


def _template_sections() -> dict[str, str]:
    template_path = Path(__file__).resolve().parent.parent / "templates" / "build-loop-body-template.md"
    return parse_markdown_sections(template_path.read_text(encoding="utf-8"))


def _section_has_substance(heading: str, actual: str, template: str) -> bool:
    actual_lines = [_strip_markdown_tokens(line) for line in actual.splitlines() if _strip_markdown_tokens(line)]
    if not actual_lines:
        return False
    template_lines = {_strip_markdown_tokens(line) for line in template.splitlines() if _strip_markdown_tokens(line)}
    if heading in FUTURE_HEADINGS:
        return True
    if all(line in template_lines for line in actual_lines):
        return False
    return True


def review_issue(repo_full: str, issue_number: int) -> dict[str, Any]:
    cfg = get_project_config()
    project_item = get_project_item(cfg, repo=repo_full, number=issue_number)
    if project_item is None:
        raise RuntimeError(f"{repo_full}#{issue_number} is not present in the project board")
    if project_item.kind != KIND_BUILD_LOOP:
        raise RuntimeError(f"{repo_full}#{issue_number} is '{project_item.kind}', not '{KIND_BUILD_LOOP}'")

    issue = issue_view(repo_full, issue_number)
    actual_sections = parse_markdown_sections(str(issue.get("body") or ""))
    canonical_sections = _template_sections()

    missing_required: list[str] = []
    critical_gaps: list[str] = []
    advisory_gaps: list[str] = []
    section_details: list[dict[str, Any]] = []

    for heading, template_body in canonical_sections.items():
        actual_body = actual_sections.get(heading, "")
        present = heading in actual_sections
        substantive = _section_has_substance(heading, actual_body, template_body) if present else False
        category = "future" if heading in FUTURE_HEADINGS else "required"
        if heading in REVIEW_REQUIRED_HEADINGS and not present:
            missing_required.append(heading)
        elif heading in REVIEW_CRITICAL_HEADINGS and not substantive:
            critical_gaps.append(heading)
        elif heading in REVIEW_ADVISORY_HEADINGS and not substantive:
            advisory_gaps.append(heading)

        section_details.append(
            {
                "heading": heading,
                "present": present,
                "substantive": substantive,
                "category": category,
            }
        )

    if missing_required or critical_gaps:
        verdict = "fail"
    elif advisory_gaps:
        verdict = "pass_with_gaps"
    else:
        verdict = "pass"

    repo_short = short_repo_name(repo_full)
    return {
        "repo": repo_full,
        "issue_number": issue_number,
        "issue_title": str(issue["title"]),
        "issue_url": str(issue["url"]),
        "issue_state": str(issue["state"]).lower(),
        "kind": project_item.kind,
        "status": project_item.status,
        "verdict": verdict,
        "missing_required_sections": missing_required,
        "critical_gaps": critical_gaps,
        "advisory_gaps": advisory_gaps,
        "future_sections": sorted(FUTURE_HEADINGS),
        "sections": section_details,
        "next_action": "safe_to_execute" if verdict in {"pass", "pass_with_gaps"} else "fix_checkpoint_a",
    }


def _format_review_table(payload: dict[str, Any], enabled: bool, width: int) -> str:
    lines: list[str] = []
    border = paint("=" * width, ANSI_DIM, enabled=enabled)
    lines.append(border)
    lines.append(paint("BUILD LOOP REVIEW (Checkpoint A)", ANSI_BOLD, enabled=enabled))
    lines.append(border)
    lines.append("")

    title = display_title(payload["issue_title"])
    lines.append(f"  {paint(title, ANSI_BOLD, enabled=enabled)}")
    lines.append(f"  {short_repo_name(payload['repo'])} #{payload['issue_number']}  "
                 f"{kind_display(payload['kind'], enabled)}  "
                 f"{status_display(payload['status'], enabled)}")
    lines.append("")

    verdict = payload["verdict"]
    if verdict == "pass":
        verdict_display = paint("PASS", ANSI_GREEN, enabled=enabled)
    elif verdict == "pass_with_gaps":
        verdict_display = paint("PASS WITH GAPS", ANSI_YELLOW, enabled=enabled)
    else:
        verdict_display = paint("FAIL", ANSI_RED, enabled=enabled)
    lines.append(f"  Verdict: {verdict_display}")

    if payload["missing_required_sections"]:
        lines.append(paint("  Missing required sections:", ANSI_RED, enabled=enabled))
        for heading in payload["missing_required_sections"]:
            lines.append(f"    - {heading}")

    if payload["critical_gaps"]:
        lines.append(paint("  Critical gaps (present but not substantive):", ANSI_RED, enabled=enabled))
        for heading in payload["critical_gaps"]:
            lines.append(f"    - {heading}")

    if payload["advisory_gaps"]:
        lines.append(paint("  Advisory gaps:", ANSI_YELLOW, enabled=enabled))
        for heading in payload["advisory_gaps"]:
            lines.append(f"    - {heading}")

    lines.append("")
    action = payload["next_action"]
    if action == "safe_to_execute":
        lines.append(paint("  Next: safe to execute", ANSI_GREEN, enabled=enabled))
    else:
        lines.append(paint("  Next: fix Checkpoint A gaps before execution", ANSI_RED, enabled=enabled))
    lines.append(border)
    return "\n".join(lines)


def _format_status_table(items: list[dict[str, Any]], enabled: bool) -> str:
    if not items:
        return "No open Build Loops."
    headers = ["repo", "issue", "status", "state", "title"]
    rows: list[dict[str, str]] = []
    for item in items:
        rows.append(
            {
                "repo": short_repo_name(item["repo"]),
                "issue": f"#{item['issue_number']}",
                "status": item["status"] or "-",
                "state": item["issue_state"],
                "title": display_title(item["issue_title"]),
            }
        )
    widths = {h: len(h) for h in headers}
    for row in rows:
        for h in headers:
            widths[h] = max(widths[h], len(row[h]))
    lines = []
    lines.append("  ".join(h.ljust(widths[h]) for h in headers))
    lines.append("  ".join("-" * widths[h] for h in headers))
    for row in rows:
        lines.append("  ".join(row[h].ljust(widths[h]) for h in headers))
    return "\n".join(lines)


def handle_bl_review(args: argparse.Namespace) -> int:
    repo_full = resolve_repo(args.repo)
    payload = review_issue(repo_full, int(args.issue))
    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        enabled = color_enabled(getattr(args, "color", "auto"))
        width = terminal_width()
        print(_format_review_table(payload, enabled, width))
    return 0


def handle_bl_status(args: argparse.Namespace) -> int:
    cfg = get_project_config()
    repo_filter = args.repo
    if repo_filter:
        repo_filter = resolve_repo(repo_filter)

    items = list_project_items(cfg, repo=repo_filter, kind=KIND_BUILD_LOOP, state="open")
    items.sort(key=lambda item: (item.repo, item.number))

    payload = [
        {
            "repo": item.repo,
            "issue_number": item.number,
            "issue_title": item.title,
            "issue_url": item.url,
            "kind": item.kind,
            "status": item.status,
            "issue_state": item.state.lower(),
        }
        for item in items[: args.limit]
    ]

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        enabled = color_enabled(getattr(args, "color", "auto"))
        print(_format_status_table(payload, enabled))
    return 0
