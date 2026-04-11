"""Run local sync audit checks for solo-os governance."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from solo_os import config
from solo_os.common import read_env_file

REQUIRED_ENV_KEYS = ("GITHUB_TOKEN",)


def write_report(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def evaluate_link_validation(
    repo_path: Path,
    project_id: str,
    link_cfg: dict,
    errors: list[str],
    warnings: list[str],
) -> dict:
    result: dict = {"checked": False, "status": "skipped", "details": ""}
    if not link_cfg.get("enabled", False):
        return result

    plan_pointer = str(link_cfg.get("plan_pointer_file", "")).strip()
    required_any = [str(x) for x in link_cfg.get("required_url_substrings_any", []) if str(x).strip()]
    severity = str(link_cfg.get("severity", "warning")).lower()
    pointer_path = repo_path / plan_pointer

    result["checked"] = True
    result["pointerPath"] = str(pointer_path)
    result["requiredAny"] = required_any
    result["severity"] = severity

    if not plan_pointer:
        result["status"] = "skipped"
        result["details"] = "plan_pointer_file is not configured"
        return result

    if not pointer_path.exists():
        message = f"[{project_id}] missing link-validation pointer file: {plan_pointer}"
        if severity == "error":
            errors.append(message)
            result["status"] = "error"
        else:
            warnings.append(message)
            result["status"] = "warning"
        result["details"] = message
        return result

    text = pointer_path.read_text(encoding="utf-8")
    matched = [needle for needle in required_any if needle in text]
    if required_any and not matched:
        message = (
            f"[{project_id}] pointer file has no expected external links "
            f"(expected any of: {', '.join(required_any)})"
        )
        if severity == "error":
            errors.append(message)
            result["status"] = "error"
        else:
            warnings.append(message)
            result["status"] = "warning"
        result["details"] = message
        return result

    result["status"] = "pass"
    result["details"] = "Link validation passed."
    result["matched"] = matched
    return result


def handle_sync_audit() -> int:
    root = config.find_root()
    repos = config.repo_list(root)
    validation = config.settings("validation", root)
    report_rel = "reports/latest-sync-audit.json"
    report_path = root / report_rel

    errors: list[str] = []
    warnings: list[str] = []
    project_results: list[dict] = []

    env_values = read_env_file(root)
    missing_env = [key for key in REQUIRED_ENV_KEYS if not env_values.get(key)]
    if missing_env:
        errors.append(f"Missing required env keys: {', '.join(missing_env)}")

    required_files = validation.get("required_repo_files", [])
    link_cfg = validation.get("link_validation", {})

    if not repos:
        errors.append("No repos found in solo-os.yml")

    for repo in repos:
        if not repo.get("active", True):
            continue

        project_id = repo.get("id", "unknown")
        repo_path_raw = repo.get("path", "")
        repo_path = Path(repo_path_raw) if repo_path_raw else None

        if not repo_path_raw:
            errors.append(f"[{project_id}] active repo is missing path")
            continue

        if repo_path is None or not repo_path.exists():
            errors.append(f"[{project_id}] path does not exist: {repo_path_raw}")
            continue

        project_result: dict = {
            "projectId": project_id,
            "repoPath": repo_path_raw,
            "requiredFiles": [],
        }

        for rel_path in required_files:
            required_path = repo_path / rel_path
            found = required_path.exists()
            project_result["requiredFiles"].append({"path": rel_path, "exists": found})
            if not found:
                warnings.append(f"[{project_id}] missing expected file: {rel_path}")

        project_result["linkValidation"] = evaluate_link_validation(
            repo_path=repo_path,
            project_id=project_id,
            link_cfg=link_cfg,
            errors=errors,
            warnings=warnings,
        )
        project_results.append(project_result)

    status = "ok"
    if errors:
        status = "fail"
    elif warnings:
        status = "warn"

    report = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "projects": project_results,
    }
    write_report(report_path, report)

    print("== Solo OS Sync Audit ==")
    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"- {error}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")

    if not errors and not warnings:
        print("\nOK: all checks passed.")
    elif not errors:
        print("\nPASS WITH WARNINGS")
    else:
        print("\nFAIL")
    print(f"\nReport: {report_path}")

    return 1 if errors else 0
