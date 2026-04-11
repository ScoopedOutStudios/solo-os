"""Archive redundant markdown artifacts in active repos (safe, non-destructive)."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from solo_os import config

VERSION_RE = re.compile(r"^(?P<base>.+)-v(?P<ver>\d+)\.md$")
BACKTICK_MD_RE = re.compile(r"`([^`]+\.md)`")
STATUS_RE = re.compile(r"^status:\s*(.+)$", re.IGNORECASE | re.MULTILINE)


def _build_path_ref_re(target_dir: str) -> re.Pattern[str]:
    escaped = re.escape(target_dir)
    return re.compile(rf"{escaped}/[A-Za-z0-9_\-./]+\.md")


def collect_keep_paths(
    scan_root: Path, keep_names: list[str], target_dir: str
) -> set[Path]:
    keep: set[Path] = set()
    all_md = list(scan_root.rglob("*.md"))
    path_ref_re = _build_path_ref_re(target_dir)

    for p in all_md:
        if p.name in keep_names:
            keep.add(p)

    pointer_files = [p for p in all_md if p.name == "LATEST.md" or p.name == "_index.md"]
    for pointer in pointer_files:
        text = pointer.read_text(encoding="utf-8")
        for match in path_ref_re.findall(text):
            resolved = scan_root.parent / match
            if resolved.exists():
                keep.add(resolved)

        for rel in BACKTICK_MD_RE.findall(text):
            rel_path = rel.strip()
            if rel_path.startswith(f"{target_dir}/"):
                candidate = scan_root.parent / rel_path
            else:
                candidate = pointer.parent / rel_path
            if candidate.exists():
                keep.add(candidate)

    groups: dict[str, list[Path]] = {}
    for p in all_md:
        match = VERSION_RE.match(p.name)
        if not match:
            continue
        key = f"{p.parent.as_posix()}::{match.group('base')}"
        groups.setdefault(key, []).append(p)

    for files in groups.values():
        latest = max(files, key=lambda item: int(VERSION_RE.match(item.name).group("ver")))  # type: ignore[union-attr]
        keep.add(latest)

    return keep


def has_superseded_status(file_path: Path) -> bool:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    match = STATUS_RE.search(text)
    if not match:
        return False
    status = match.group(1).strip().lower()
    return status in {"superseded", "archived"}


def candidate_reason(path: Path, keep: set[Path]) -> str | None:
    if path in keep:
        return None
    if has_superseded_status(path):
        return "status is superseded/archived"
    m = VERSION_RE.match(path.name)
    if m:
        return "older versioned artifact not in keep set"
    return None


def archive_destination(scan_root: Path, archive_root_name: str, source: Path) -> Path:
    rel = source.relative_to(scan_root)
    today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    return scan_root / archive_root_name / today / rel


def handle_cleanup_markdown(args: argparse.Namespace) -> int:
    root = config.find_root()
    repos = config.repo_list(root)
    cleanup_cfg = config.settings("cleanup", root)

    target_dir = str(cleanup_cfg.get("target_directory", "")).strip()
    if not target_dir:
        print("== Markdown Cleanup ==")
        print("- SKIP: no cleanup.target_directory configured in solo-os.yml")
        return 0

    keep_names = [str(x) for x in cleanup_cfg.get("keep_file_names", [])]
    archive_root_name = str(cleanup_cfg.get("archive_root_name", "archive"))
    report_rel = str(cleanup_cfg.get("report_path", "reports/latest-cleanup-report.json"))
    report_path = root / report_rel

    if args.repo:
        repos = [r for r in repos if r.get("id") == args.repo]
    else:
        repos = [r for r in repos if r.get("active", True)]

    all_candidates: list[dict[str, Any]] = []
    moved: list[dict[str, Any]] = []

    print("== Markdown Cleanup ==")
    print(f"- Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"- Target directory: {target_dir}/")

    for repo in repos:
        repo_id = str(repo.get("id"))
        repo_path = Path(str(repo.get("path", "")))
        scan_root = repo_path / target_dir
        if not scan_root.exists():
            print(f"- SKIP [{repo_id}]: missing {target_dir}/")
            continue

        keep = collect_keep_paths(scan_root, keep_names, target_dir)
        md_files = [
            p for p in scan_root.rglob("*.md") if f"/{archive_root_name}/" not in p.as_posix()
        ]

        project_candidates: list[tuple[Path, str]] = []
        for md in md_files:
            reason = candidate_reason(md, keep)
            if reason:
                project_candidates.append((md, reason))

        if not project_candidates:
            print(f"- [{repo_id}] no cleanup candidates")
            continue

        print(f"- [{repo_id}] candidates: {len(project_candidates)}")
        for source, reason in project_candidates:
            rel = source.relative_to(repo_path).as_posix()
            print(f"  - {rel} :: {reason}")
            all_candidates.append({"repoId": repo_id, "path": rel, "reason": reason})

            if args.apply:
                dest = archive_destination(scan_root, archive_root_name, source)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(dest))
                moved.append(
                    {
                        "repoId": repo_id,
                        "from": rel,
                        "to": dest.relative_to(repo_path).as_posix(),
                        "reason": reason,
                    }
                )

    report = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "mode": "apply" if args.apply else "dry-run",
        "candidates": all_candidates,
        "moved": moved,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"\nReport: {report_path}")
    print(f"- candidate_count: {len(all_candidates)}")
    if args.apply:
        print(f"- moved_count: {len(moved)}")
    return 0
