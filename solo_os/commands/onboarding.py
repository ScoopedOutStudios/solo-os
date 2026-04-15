"""Onboarding commands for first-time solo-os setup and validation."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from solo_os import config
from solo_os.display import ANSI_GREEN, ANSI_RED, ANSI_YELLOW, paint
from solo_os.github_ops import run_gh_json, run_gh_text

REQUIRED_FIELDS: dict[str, list[str]] = {
    "Kind": ["Idea", "Roadmap", "Build Loop"],
    "Status": ["Todo", "Prioritized", "Backlog", "Blocked", "In Progress", "Done"],
    "Stage": ["Inbox", "Today", "This Week", "Waiting"],
}


@dataclass
class CheckResult:
    """Result of one verify check."""

    name: str
    status: str
    detail: str
    fix: str = ""

    def as_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "status": self.status,
            "detail": self.detail,
            "fix": self.fix,
        }


def _run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def _run_git_text(args: list[str], cwd: Path) -> str:
    proc = _run(["git", *args], cwd=cwd)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "git command failed")
    return proc.stdout.strip()


def _status_rank(status: str) -> int:
    if status == "FAIL":
        return 2
    if status == "WARN":
        return 1
    return 0


_STATUS_ICON = {"PASS": "✓", "WARN": "!", "FAIL": "✗"}
_STATUS_COLOR = {"PASS": ANSI_GREEN, "WARN": ANSI_YELLOW, "FAIL": ANSI_RED}


def _format_doctor(results: list[CheckResult], output_format: str) -> str:
    if output_format == "json":
        return json.dumps([item.as_dict() for item in results], indent=2)

    lines = []
    for item in results:
        color = _STATUS_COLOR.get(item.status, "")
        icon = _STATUS_ICON.get(item.status, " ")
        status_str = paint(f"[{icon}] {item.status}", color, enabled=True)
        lines.append(f"{status_str}  {item.name}")
        lines.append(f"       {item.detail}")
        if item.fix:
            lines.append(paint(f"       Fix: {item.fix}", ANSI_YELLOW, enabled=True))
    return "\n".join(lines)


def _print_doctor_summary(results: list[CheckResult]) -> None:
    failures = sum(1 for item in results if item.status == "FAIL")
    warnings = sum(1 for item in results if item.status == "WARN")
    if failures:
        print(paint(f"\nResult: {failures} failing check(s), {warnings} warning(s).", ANSI_RED, enabled=True))
    elif warnings:
        print(paint(f"\nResult: all checks passed, {warnings} warning(s).", ANSI_YELLOW, enabled=True))
    else:
        print(paint("\nResult: all checks passed.", ANSI_GREEN, enabled=True))


def _gh_is_authenticated() -> bool:
    proc = _run(["gh", "auth", "status"])
    return proc.returncode == 0


def _gh_token_scopes() -> list[str]:
    """Return the list of scopes granted to the current gh token."""
    proc = _run(["gh", "auth", "status"])
    if proc.returncode != 0:
        return []
    for line in (proc.stdout + proc.stderr).splitlines():
        if "Token scopes:" in line:
            raw = line.split("Token scopes:", 1)[1]
            return [s.strip().strip("'\"") for s in raw.split(",") if s.strip()]
    return []


def _has_gh_token() -> bool:
    if os.environ.get("GITHUB_TOKEN"):
        return True
    proc = _run(["gh", "auth", "token"])
    return proc.returncode == 0 and bool(proc.stdout.strip())


def _extract_field_options(field: dict[str, Any]) -> list[str]:
    options = field.get("options") or []
    values: list[str] = []
    for option in options:
        if isinstance(option, dict):
            name = option.get("name")
            if name:
                values.append(str(name))
    return values


def _project_check_from_config(loaded_config: dict[str, Any]) -> CheckResult:
    gh_cfg = loaded_config.get("github", {})
    owner = str(gh_cfg.get("owner") or "").strip()
    project_number = (gh_cfg.get("project") or {}).get("number")
    if not owner or not isinstance(project_number, int) or project_number <= 0:
        return CheckResult(
            name="project-access",
            status="FAIL",
            detail="Config is missing github.owner or github.project.number.",
            fix="Set github.owner and github.project.number in solo-os.yml.",
        )

    try:
        project_view = run_gh_json(
            [
                "project",
                "view",
                str(project_number),
                "--owner",
                owner,
                "--format",
                "json",
            ]
        )
        fields = run_gh_json(
            [
                "project",
                "field-list",
                str(project_number),
                "--owner",
                owner,
                "--format",
                "json",
            ]
        )
    except RuntimeError as exc:
        return CheckResult(
            name="project-access",
            status="FAIL",
            detail=f"Could not access GitHub Project {owner}/{project_number}: {exc}",
            fix="Confirm owner/project number and run `gh auth login` with project access.",
        )

    existing_fields: dict[str, list[str]] = {}
    for field in fields.get("fields", []):
        field_name = str(field.get("name") or "")
        if field_name:
            existing_fields[field_name] = _extract_field_options(field)

    missing_fields = [name for name in REQUIRED_FIELDS if name not in existing_fields]
    missing_options: list[str] = []
    for field_name, required_options in REQUIRED_FIELDS.items():
        if field_name not in existing_fields:
            continue
        options = set(existing_fields[field_name])
        for option_name in required_options:
            if option_name not in options:
                missing_options.append(f"{field_name}:{option_name}")

    if missing_fields:
        return CheckResult(
            name="project-access",
            status="FAIL",
            detail=(
                f"Project '{project_view.get('title', '')}' is reachable, "
                f"but required fields are missing: {', '.join(missing_fields)}."
            ),
            fix="Run `solo-os init --owner <owner> --project <number>` to bootstrap required fields.",
        )

    if missing_options:
        return CheckResult(
            name="project-access",
            status="WARN",
            detail=(
                f"Project is reachable but missing recommended options: "
                f"{', '.join(missing_options)}."
            ),
            fix="Add missing options in GitHub Project field settings.",
        )

    return CheckResult(
        name="project-access",
        status="PASS",
        detail=f"Project '{project_view.get('title', '')}' is reachable and has required fields.",
    )


def _parse_github_remote(remote_url: str) -> tuple[str, str] | None:
    text = remote_url.strip()
    patterns = [
        r"^git@github\.com:(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$",
        r"^https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$",
        r"^ssh://git@github\.com/(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$",
    ]
    for pattern in patterns:
        match = re.match(pattern, text)
        if not match:
            continue
        return match.group("owner"), match.group("repo")
    return None


def _detect_git_remote(path: Path) -> tuple[str, str] | None:
    try:
        remote = _run_git_text(["config", "--get", "remote.origin.url"], cwd=path)
    except RuntimeError:
        return None
    if not remote:
        return None
    return _parse_github_remote(remote)


def _prompt(message: str, *, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{message}{suffix}: ").strip()
    if value:
        return value
    return default or ""


def _project_url(owner: str, owner_type: str, number: int) -> str:
    if owner_type == "user":
        return f"https://github.com/users/{owner}/projects/{number}"
    return f"https://github.com/orgs/{owner}/projects/{number}"


def _detect_owner_type(owner: str) -> str:
    org_probe = _run(["gh", "api", f"orgs/{owner}"])
    if org_probe.returncode == 0:
        return "org"
    user_probe = _run(["gh", "api", f"users/{owner}"])
    if user_probe.returncode == 0:
        return "user"
    return "org"


def _init_prereq_failures() -> list[str]:
    failures: list[str] = []
    if shutil.which("git") is None:
        failures.append("git is not installed. Install git and try again.")
    if shutil.which("gh") is None:
        failures.append("gh is not installed. Install GitHub CLI from https://cli.github.com/ and try again.")
        return failures
    if not _gh_is_authenticated():
        failures.append("gh is not authenticated. Run `gh auth login` and grant project access.")
    return failures


def _create_project(owner: str, title: str) -> dict[str, Any]:
    return run_gh_json(
        [
            "project",
            "create",
            "--owner",
            owner,
            "--title",
            title,
            "--format",
            "json",
        ]
    )


def _field_exists(fields_payload: dict[str, Any], field_name: str) -> bool:
    for field in fields_payload.get("fields", []):
        if str(field.get("name") or "") == field_name:
            return True
    return False


def _ensure_project_fields(owner: str, project_number: int) -> list[str]:
    created: list[str] = []
    fields_payload = run_gh_json(
        [
            "project",
            "field-list",
            str(project_number),
            "--owner",
            owner,
            "--format",
            "json",
        ]
    )
    for field_name, options in REQUIRED_FIELDS.items():
        if _field_exists(fields_payload, field_name):
            continue
        run_gh_text(
            [
                "project",
                "field-create",
                str(project_number),
                "--owner",
                owner,
                "--name",
                field_name,
                "--data-type",
                "SINGLE_SELECT",
                "--single-select-options",
                ",".join(options),
            ]
        )
        created.append(field_name)
        fields_payload = run_gh_json(
            [
                "project",
                "field-list",
                str(project_number),
                "--owner",
                owner,
                "--format",
                "json",
            ]
        )
    return created


def _repo_entry(mode: str, repo_name: str, repo_id_override: str | None, repo_path_override: str | None) -> dict[str, Any]:
    repo_id = (repo_id_override or repo_name or "my-project").strip()
    if mode == "single":
        repo_path = repo_path_override or "./"
    else:
        default_path = f"./{repo_name}" if repo_name else "./my-project"
        repo_path = repo_path_override or default_path
    return {
        "id": repo_id,
        "path": repo_path,
        "active": True,
    }


def _write_config(
    path: Path,
    *,
    owner: str,
    owner_type: str,
    project_number: int,
    project_title: str,
    repo_entry: dict[str, Any],
) -> None:
    payload = {
        "github": {
            "owner": owner,
            "owner_type": owner_type,
            "project": {
                "number": project_number,
                "title": project_title,
            },
            "fields": {
                "kind": {"name": "Kind", "options": REQUIRED_FIELDS["Kind"]},
                "status": {"name": "Status", "options": REQUIRED_FIELDS["Status"]},
                "stage": {"name": "Stage", "options": REQUIRED_FIELDS["Stage"]},
            },
        },
        "repos": [repo_entry],
        "daily_triage": {
            "today_limit": 3,
            "this_week_limit": 7,
            "max_build_loops_per_repo_today": 1,
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False)


def _print_view_guidance(project_url: str) -> None:
    print("\nRecommended GitHub Project Views (create manually in the GitHub UI):")
    print("1) Active Work (board): group by Status, filter Status != Done")
    print("2) By Repo (table): group by Repository")
    print("3) Today Focus (table): filter Stage = Today")
    print("4) Build Loops (board): filter Kind = Build Loop, group by Status")
    print(f"\nOpen your project: {project_url}")


def handle_doctor(args: argparse.Namespace) -> int:
    check_path = Path(getattr(args, "path", ".")).expanduser().resolve()
    results: list[CheckResult] = []

    has_gh = shutil.which("gh") is not None
    results.append(
        CheckResult(
            name="gh-installed",
            status="PASS" if has_gh else "FAIL",
            detail="GitHub CLI is installed." if has_gh else "GitHub CLI (`gh`) not found.",
            fix="" if has_gh else "Install from https://cli.github.com/ and re-run verify.",
        )
    )

    has_git = shutil.which("git") is not None
    results.append(
        CheckResult(
            name="git-installed",
            status="PASS" if has_git else "FAIL",
            detail="Git is installed." if has_git else "Git not found.",
            fix="" if has_git else "Install git and re-run verify.",
        )
    )

    python_ok = (sys.version_info.major, sys.version_info.minor) >= (3, 9)
    results.append(
        CheckResult(
            name="python-version",
            status="PASS" if python_ok else "FAIL",
            detail=f"Python {sys.version_info.major}.{sys.version_info.minor} detected.",
            fix="" if python_ok else "Use Python 3.9+.",
        )
    )

    if has_gh:
        gh_auth = _gh_is_authenticated()
        results.append(
            CheckResult(
                name="gh-auth",
                status="PASS" if gh_auth else "FAIL",
                detail="gh is authenticated." if gh_auth else "gh is not authenticated.",
                fix="" if gh_auth else "Run `gh auth login` and grant project scope.",
            )
        )
        if gh_auth:
            scopes = _gh_token_scopes()
            has_project_scope = "project" in scopes
            results.append(
                CheckResult(
                    name="gh-scope-project",
                    status="PASS" if has_project_scope else "FAIL",
                    detail=(
                        "gh token has the 'project' scope."
                        if has_project_scope
                        else f"gh token is missing the 'project' scope (current scopes: {', '.join(scopes) or 'none'})."
                    ),
                    fix=(
                        ""
                        if has_project_scope
                        else "Run: gh auth refresh --scopes project"
                    ),
                )
            )
    else:
        results.append(
            CheckResult(
                name="gh-auth",
                status="FAIL",
                detail="Cannot check auth because `gh` is unavailable.",
                fix="Install gh first.",
            )
        )

    token_ok = _has_gh_token() if has_gh else bool(os.environ.get("GITHUB_TOKEN"))
    results.append(
        CheckResult(
            name="github-token",
            status="PASS" if token_ok else "FAIL",
            detail=(
                "GITHUB_TOKEN found (env or gh auth token)."
                if token_ok
                else "No GITHUB_TOKEN in env and no token from gh auth."
            ),
            fix=(
                ""
                if token_ok
                else "Set GITHUB_TOKEN or run `gh auth login` so `gh auth token` works."
            ),
        )
    )

    try:
        root = config.find_root(start=check_path)
        loaded = config.load_config(root=root)
        results.append(
            CheckResult(
                name="config-file",
                status="PASS",
                detail=f"Found valid solo-os config at {root / config.CONFIG_FILENAME}.",
            )
        )
        if has_gh:
            results.append(_project_check_from_config(loaded))
        else:
            results.append(
                CheckResult(
                    name="project-access",
                    status="WARN",
                    detail="Config found, but skipped project validation because gh is unavailable.",
                    fix="Install/authenticate gh and re-run verify.",
                )
            )
    except (config.ConfigNotFoundError, yaml.YAMLError) as exc:
        results.append(
            CheckResult(
                name="config-file",
                status="WARN",
                detail=f"No valid config found near {check_path}: {exc}",
                fix="Run `solo-os init` to generate solo-os.yml.",
            )
        )
        results.append(
            CheckResult(
                name="project-access",
                status="WARN",
                detail="Skipped project checks because no valid solo-os.yml was found.",
                fix="Create config via `solo-os init` then re-run `solo-os verify`.",
            )
        )

    print(_format_doctor(results, getattr(args, "format", "table")))
    if getattr(args, "format", "table") == "table":
        _print_doctor_summary(results)

    return 1 if any(item.status == "FAIL" for item in results) else 0


def handle_init(args: argparse.Namespace) -> int:
    prereq_failures = _init_prereq_failures()
    if prereq_failures:
        joined = "\n- ".join([""] + prereq_failures)
        raise RuntimeError(f"Init prerequisites not met:{joined}")

    cwd = Path.cwd()
    detected = _detect_git_remote(cwd) or ("", "")
    detected_owner, detected_repo = detected

    owner = str(args.owner or detected_owner).strip()
    if not owner and not args.yes:
        owner = _prompt("GitHub owner (org or user)", default=detected_owner or "")
    if not owner:
        raise RuntimeError("Missing owner. Provide --owner or run interactively.")

    owner_type = str(args.owner_type or "").strip() or _detect_owner_type(owner)
    if owner_type not in {"org", "user"}:
        owner_type = "org"

    project_number = int(args.project) if args.project else 0
    project_title = str(args.project_title or "Solo OS Planning").strip()
    created_project = False

    if project_number <= 0:
        if args.yes:
            create = True
        else:
            entered = _prompt(
                "Existing project number (leave blank to create a new project)",
                default="",
            )
            if entered:
                try:
                    project_number = int(entered)
                except ValueError as exc:
                    raise RuntimeError(f"Invalid project number: {entered}") from exc
            create = project_number <= 0

        if create:
            try:
                project = _create_project(owner, project_title)
            except RuntimeError as exc:
                msg = str(exc)
                if "permission" in msg.lower() or "createProjectV2" in msg:
                    raise RuntimeError(
                        "GitHub token is missing the 'project' scope required to create projects.\n"
                        "  Fix: gh auth refresh --scopes project\n"
                        "  Then re-run: solo-os init"
                    ) from None
                raise
            project_number = int(project["number"])
            project_title = str(project.get("title") or project_title)
            created_project = True

    # Confirm project exists before writing config.
    try:
        view_payload = run_gh_json(
            [
                "project",
                "view",
                str(project_number),
                "--owner",
                owner,
                "--format",
                "json",
            ]
        )
    except RuntimeError as exc:
        msg = str(exc)
        if "permission" in msg.lower() or "project" in msg.lower():
            raise RuntimeError(
                f"Cannot access GitHub Project #{project_number} for '{owner}'.\n"
                "  If the project exists, make sure your token has the 'project' scope:\n"
                "  Fix: gh auth refresh --scopes project\n"
                "  Then re-run: solo-os init"
            ) from None
        raise
    project_title = str(view_payload.get("title") or project_title)
    try:
        created_fields = _ensure_project_fields(owner, project_number)
    except RuntimeError as exc:
        msg = str(exc)
        if "permission" in msg.lower():
            raise RuntimeError(
                "GitHub token is missing the 'project' scope required to manage project fields.\n"
                "  Fix: gh auth refresh --scopes project\n"
                "  Then re-run: solo-os init"
            ) from None
        raise

    mode = str(args.mode or "").strip().lower()
    if mode not in {"single", "multi"}:
        if args.yes:
            mode = "single"
        else:
            mode = _prompt("Setup mode: single or multi repo", default="single").lower()
            if mode not in {"single", "multi"}:
                mode = "single"

    repo_name = detected_repo or "my-project"
    repo_entry = _repo_entry(
        mode=mode,
        repo_name=repo_name,
        repo_id_override=args.repo_id,
        repo_path_override=args.repo_path,
    )

    config_path = Path(args.config_path or (cwd / "solo-os.yml")).expanduser().resolve()
    if config_path.exists() and not args.force:
        raise RuntimeError(
            f"{config_path} already exists. Re-run with --force to overwrite, or choose --config-path."
        )

    _write_config(
        config_path,
        owner=owner,
        owner_type=owner_type,
        project_number=project_number,
        project_title=project_title,
        repo_entry=repo_entry,
    )

    # Validate generated config can be parsed.
    with config_path.open(encoding="utf-8") as handle:
        parsed = yaml.safe_load(handle) or {}
    if not isinstance(parsed, dict):
        raise RuntimeError("Generated config is invalid YAML.")

    project_url = str(view_payload.get("url") or _project_url(owner, owner_type, project_number))
    payload = {
        "owner": owner,
        "owner_type": owner_type,
        "project_number": project_number,
        "project_title": project_title,
        "project_url": project_url,
        "created_project": created_project,
        "created_fields": created_fields,
        "mode": mode,
        "config_path": str(config_path),
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print("solo-os init complete.")
        print(f"- Config written: {config_path}")
        print(f"- Owner: {owner} ({owner_type})")
        print(f"- Project: #{project_number} ({project_title})")
        if created_project:
            print("- Project bootstrap: created new project")
        if created_fields:
            print(f"- Fields created: {', '.join(created_fields)}")
        else:
            print("- Fields created: none (already present)")
        _print_view_guidance(project_url)
        print("\nNext steps:")
        print("1) Review `solo-os.yml` for repo aliases/paths")
        print("2) Run `solo-os verify`")
        print("3) Run `solo-os gh-next` to pick the next item")

    return 0
