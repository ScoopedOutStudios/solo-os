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


def _run(args: list[str], cwd: Path | None = None, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False, input=input_text)


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
            fix="Run `solo-os init` to add missing options automatically.",
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


@dataclass
class DetectedRepo:
    """A git repo discovered during workspace scan."""

    name: str
    path: str
    remote_url: str
    owner_repo: str

    def as_entry(self, relative_to: Path) -> dict[str, Any]:
        try:
            rel = str(Path(self.path).relative_to(relative_to))
            if rel == ".":
                rel_path = "./"
            elif not rel.startswith("./"):
                rel_path = f"./{rel}"
            else:
                rel_path = rel
        except ValueError:
            rel_path = self.path
        return {"id": self.name, "path": rel_path, "active": True}


def _scan_workspace_repos(cwd: Path) -> list[DetectedRepo]:
    """Scan cwd itself and its immediate subdirectories for git repos."""
    repos: list[DetectedRepo] = []
    candidates = [cwd] + sorted(
        p for p in cwd.iterdir() if p.is_dir() and not p.name.startswith(".")
    )
    for candidate in candidates:
        git_dir = candidate / ".git"
        if not git_dir.exists():
            continue
        remote_info = _detect_git_remote(candidate)
        if remote_info:
            owner, repo_name = remote_info
            owner_repo = f"{owner}/{repo_name}"
        else:
            owner_repo = ""
            repo_name = candidate.name
        repos.append(
            DetectedRepo(
                name=repo_name,
                path=str(candidate),
                remote_url="",
                owner_repo=owner_repo,
            )
        )
    return repos


def _parse_github_url(url: str) -> tuple[str, str] | None:
    """Parse a GitHub HTTPS or SSH URL into (owner, repo)."""
    return _parse_github_remote(url)


def _clone_repo(url: str, target_dir: Path) -> DetectedRepo:
    """Clone a GitHub URL into target_dir and return a DetectedRepo."""
    parsed = _parse_github_url(url)
    if not parsed:
        raise RuntimeError(
            f"Could not parse GitHub URL: {url}\n"
            "  Expected: https://github.com/owner/repo or git@github.com:owner/repo"
        )
    owner, repo_name = parsed
    dest = target_dir / repo_name
    if dest.exists():
        raise RuntimeError(
            f"Directory already exists: {dest}\n"
            f"  If this repo is already cloned, it should have been detected automatically."
        )
    proc = _run(["git", "clone", url, str(dest)])
    if proc.returncode != 0:
        raise RuntimeError(
            f"git clone failed: {proc.stderr.strip() or proc.stdout.strip()}"
        )
    return DetectedRepo(
        name=repo_name,
        path=str(dest),
        remote_url=url,
        owner_repo=f"{owner}/{repo_name}",
    )


def _collect_repos(cwd: Path, *, interactive: bool, repo_id_override: str | None, repo_path_override: str | None) -> list[dict[str, Any]]:
    """Guided repo collection: detect, confirm, add-by-URL, return entries."""
    detected = _scan_workspace_repos(cwd)

    if not interactive:
        if detected:
            return [r.as_entry(cwd) for r in detected]
        return [{"id": "my-project", "path": "./", "active": True}]

    if repo_id_override or repo_path_override:
        is_inside_repo = any(Path(r.path) == cwd for r in detected)
        repo_name = detected[0].name if detected else "my-project"
        entry = _repo_entry(
            repo_name=repo_name,
            repo_id_override=repo_id_override,
            repo_path_override=repo_path_override,
            is_inside_repo=is_inside_repo,
        )
        return [entry]

    selected: list[DetectedRepo] = []

    if detected:
        print(f"\nFound {len(detected)} git repo(s) in {cwd}:")
        for i, repo in enumerate(detected, 1):
            suffix = f"  (origin: {repo.owner_repo})" if repo.owner_repo else ""
            print(f"  [{i}] {repo.name}{suffix}")
        print()

        include_all = _prompt("Include all?", default="Y")
        if include_all.lower() in {"y", "yes", ""}:
            selected = list(detected)
        else:
            numbers = _prompt("Enter repo numbers to include (e.g. 1,3)")
            for part in numbers.split(","):
                part = part.strip()
                if not part:
                    continue
                try:
                    idx = int(part) - 1
                    if 0 <= idx < len(detected):
                        selected.append(detected[idx])
                except ValueError:
                    pass
            if not selected:
                print("No repos selected from detected list.")
    else:
        print(f"\nNo git repos detected in {cwd}.")

    while True:
        url = _prompt(
            "Add a repo by GitHub URL? (paste URL or press Enter to finish)",
            default="",
        )
        if not url:
            break
        try:
            cloned = _clone_repo(url, cwd)
            selected.append(cloned)
            print(f"  Cloned {cloned.owner_repo} into {cloned.path}")
        except RuntimeError as exc:
            print(f"  Error: {exc}")

    if not selected:
        is_inside_repo = (cwd / ".git").exists()
        repo_name = cwd.name if is_inside_repo else "my-project"
        return [_repo_entry(
            repo_name=repo_name,
            repo_id_override=None,
            repo_path_override=None,
            is_inside_repo=is_inside_repo,
        )]

    return [r.as_entry(cwd) for r in selected]


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


def _resolve_at_me() -> str:
    """Resolve @me to the authenticated GitHub username."""
    proc = _run(["gh", "api", "user", "--jq", ".login"])
    if proc.returncode == 0 and proc.stdout.strip():
        return proc.stdout.strip()
    raise RuntimeError(
        "Could not resolve @me to a GitHub username.\n"
        "  Fix: Run `gh auth login` and try again."
    )


def _resolve_owner(raw: str) -> str:
    """Normalize owner input: resolve @me, strip whitespace."""
    value = raw.strip()
    if value.lower() == "@me":
        return _resolve_at_me()
    return value


def _validate_owner(owner: str) -> tuple[str, str]:
    """Verify the owner exists on GitHub and return (owner, owner_type).

    Raises RuntimeError with an actionable message if the owner cannot be found.
    """
    org_probe = _run(["gh", "api", f"orgs/{owner}"])
    if org_probe.returncode == 0:
        return owner, "org"
    user_probe = _run(["gh", "api", f"users/{owner}"])
    if user_probe.returncode == 0:
        return owner, "user"
    raise RuntimeError(
        f"'{owner}' is not a valid GitHub org or username.\n"
        f"  Check the spelling, or use @me for your own account.\n"
        f"  Example: solo-os init --owner my-org\n"
        f"  Example: solo-os init --owner @me"
    )


def _detect_owner_type(owner: str) -> str:
    try:
        _, owner_type = _validate_owner(owner)
        return owner_type
    except RuntimeError:
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


def _list_projects(owner: str) -> list[dict[str, Any]]:
    """Fetch open GitHub Projects V2 for an owner. Returns list of {number, title, item_count, url}."""
    try:
        payload = run_gh_json(
            ["project", "list", "--owner", owner, "--format", "json"]
        )
    except RuntimeError:
        return []
    results: list[dict[str, Any]] = []
    for proj in payload.get("projects", []):
        if proj.get("closed"):
            continue
        results.append({
            "number": proj.get("number", 0),
            "title": proj.get("title", ""),
            "item_count": (proj.get("items") or {}).get("totalCount", 0),
            "url": proj.get("url", ""),
        })
    return results


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


_OPTION_COLORS = ["GRAY", "BLUE", "GREEN", "YELLOW", "ORANGE", "RED", "PINK", "PURPLE"]


def _find_field(fields_payload: dict[str, Any], field_name: str) -> dict[str, Any] | None:
    for field in fields_payload.get("fields", []):
        if str(field.get("name") or "") == field_name:
            return field
    return None


def _add_missing_options(field_id: str, existing_options: list[dict[str, Any]], required_names: list[str]) -> list[str]:
    """Add missing options to an existing single-select field via GraphQL. Returns names added."""
    existing_names = {opt.get("name", "") for opt in existing_options}
    missing = [name for name in required_names if name not in existing_names]
    if not missing:
        return []

    all_options: list[dict[str, str]] = []
    for opt in existing_options:
        all_options.append({
            "name": opt["name"],
            "color": opt.get("color", "GRAY"),
            "description": opt.get("description", ""),
        })
    color_idx = len(all_options)
    for name in missing:
        all_options.append({
            "name": name,
            "color": _OPTION_COLORS[color_idx % len(_OPTION_COLORS)],
            "description": "",
        })
        color_idx += 1

    query = (
        "mutation($fieldId: ID!, $opts: [ProjectV2SingleSelectFieldOptionInput!]!) {"
        "  updateProjectV2Field(input: { fieldId: $fieldId, singleSelectOptions: $opts }) {"
        "    projectV2Field { ... on ProjectV2SingleSelectField { id } }"
        "  }"
        "}"
    )
    body = json.dumps({"query": query, "variables": {"fieldId": field_id, "opts": all_options}})
    proc = _run(["gh", "api", "graphql", "--input", "-"], input_text=body)
    if proc.returncode != 0:
        raise RuntimeError(f"Failed to update field options: {proc.stderr.strip() or proc.stdout.strip()}")
    return missing


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
    for field_name, required_options in REQUIRED_FIELDS.items():
        existing_field = _find_field(fields_payload, field_name)
        if existing_field:
            field_id = existing_field.get("id", "")
            existing_opts = existing_field.get("options") or []
            if field_id and existing_opts:
                added = _add_missing_options(field_id, existing_opts, required_options)
                if added:
                    created.append(f"{field_name} (+{', '.join(added)})")
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
                ",".join(required_options),
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


def _repo_entry(repo_name: str, repo_id_override: str | None, repo_path_override: str | None, *, is_inside_repo: bool) -> dict[str, Any]:
    repo_id = (repo_id_override or repo_name or "my-project").strip()
    if is_inside_repo:
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
    repos: list[dict[str, Any]],
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
        "repos": repos,
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


def handle_onboarding() -> int:
    """Print the bundled getting-started guide (markdown)."""
    guide = Path(__file__).resolve().parent.parent / "templates" / "user-guide-getting-started.md"
    if guide.is_file():
        text = guide.read_text(encoding="utf-8")
    else:
        # This should be rare: the guide is part of the package, but this fallback
        # prevents a completely broken `solo-os onboarding` in partial checkouts.
        text = (
            "Solo OS onboarding guide is missing from the package.\n"
            f"Expected: {guide}\n\n"
            "Fix:\n"
            "- Reinstall solo-os, or use a full checkout of the `solo-os` repository.\n"
            "- In development: ensure `solo_os/templates/user-guide-getting-started.md` exists.\n"
        )
    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")
    return 0


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

    python_ok = (sys.version_info.major, sys.version_info.minor) >= (3, 10)
    results.append(
        CheckResult(
            name="python-version",
            status="PASS" if python_ok else "FAIL",
            detail=f"Python {sys.version_info.major}.{sys.version_info.minor} detected.",
            fix="" if python_ok else "Use Python 3.10+ (matches pyproject.toml).",
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
        for repo in loaded.get("repos", []):
            repo_id = str(repo.get("id") or "")
            if not repo.get("active", True):
                continue
            resolved = str(repo.get("_resolved_path") or repo.get("path") or "")
            if not resolved:
                results.append(
                    CheckResult(
                        name=f"repo:{repo_id}",
                        status="WARN",
                        detail=f"Repo '{repo_id}' has no path configured.",
                        fix=f"Set a path for '{repo_id}' in solo-os.yml.",
                    )
                )
                continue
            repo_path = Path(resolved)
            if not repo_path.is_dir():
                results.append(
                    CheckResult(
                        name=f"repo:{repo_id}",
                        status="FAIL",
                        detail=f"Repo '{repo_id}' path does not exist: {resolved}",
                        fix=f"Clone the repo or update the path in solo-os.yml.",
                    )
                )
                continue
            git_dir = repo_path / ".git"
            if not git_dir.exists():
                results.append(
                    CheckResult(
                        name=f"repo:{repo_id}",
                        status="WARN",
                        detail=f"Repo '{repo_id}' exists at {resolved} but is not a git repository.",
                        fix=f"Run `git init` in {resolved} or update the path in solo-os.yml.",
                    )
                )
            else:
                results.append(
                    CheckResult(
                        name=f"repo:{repo_id}",
                        status="PASS",
                        detail=f"Repo '{repo_id}' is a valid git repository at {resolved}.",
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


def _repair_existing_config(config_path: Path, args: argparse.Namespace) -> int:
    """Read existing config and ensure project fields are up to date."""
    try:
        with config_path.open(encoding="utf-8") as fh:
            cfg = yaml.safe_load(fh) or {}
    except Exception as exc:
        raise RuntimeError(f"Could not read {config_path}: {exc}") from exc

    gh = cfg.get("github") or {}
    owner = gh.get("owner", "")
    project_cfg = gh.get("project") or {}
    project_number = int(project_cfg.get("number", 0))
    if not owner or project_number <= 0:
        print("Existing config does not contain owner/project info. Nothing to repair.")
        return 0

    print(f"Checking project fields for {owner} #{project_number}...")
    try:
        created_fields = _ensure_project_fields(owner, project_number)
    except RuntimeError as exc:
        raise RuntimeError(f"Could not repair project fields: {exc}") from exc

    if created_fields:
        print(f"Updated fields: {', '.join(created_fields)}")
    else:
        print("All fields and options are already up to date.")
    return 0


def handle_init(args: argparse.Namespace) -> int:
    prereq_failures = _init_prereq_failures()
    if prereq_failures:
        joined = "\n- ".join([""] + prereq_failures)
        raise RuntimeError(f"Init prerequisites not met:{joined}")

    cwd = Path.cwd()

    config_path = Path(args.config_path or (cwd / "solo-os.yml")).expanduser().resolve()
    if config_path.exists() and not args.force:
        if args.yes:
            raise RuntimeError(
                f"{config_path} already exists. Re-run with --force to overwrite."
            )
        print(f"\n{config_path} already exists.")
        overwrite = _prompt("Overwrite it?", default="n")
        if overwrite.lower() not in {"y", "yes"}:
            return _repair_existing_config(config_path, args)
        args.force = True
    detected = _detect_git_remote(cwd) or ("", "")
    detected_owner, detected_repo = detected

    default_owner = str(args.owner or detected_owner).strip()
    if not default_owner:
        try:
            default_owner = _resolve_at_me()
        except RuntimeError:
            pass
    if args.owner:
        raw_owner = args.owner.strip()
    elif not args.yes:
        raw_owner = _prompt(
            "GitHub org or username",
            default=default_owner or "",
        )
    else:
        raw_owner = default_owner
    if not raw_owner:
        raise RuntimeError("Missing owner. Provide --owner or run interactively.")

    owner = _resolve_owner(raw_owner)
    owner, owner_type = _validate_owner(owner)
    if args.owner_type and args.owner_type in {"org", "user"}:
        owner_type = args.owner_type

    project_number = int(args.project) if args.project else 0
    default_title = str(args.project_title or "Solo OS Planning").strip()
    project_title = default_title
    created_project = False

    if project_number <= 0:
        existing = _list_projects(owner)

        if args.yes:
            # Non-interactive: auto-select or create
            if not existing:
                create = True
            elif len(existing) == 1:
                project_number = existing[0]["number"]
                project_title = existing[0]["title"]
                create = False
            else:
                title_match = next(
                    (p for p in existing if p["title"] == default_title), None
                )
                pick = title_match or existing[0]
                project_number = pick["number"]
                project_title = pick["title"]
                create = False
        elif existing:
            print(f"\nFound {len(existing)} existing project(s) for {owner}:")
            for i, proj in enumerate(existing, 1):
                print(f"  [{i}] {proj['title']:<30} (#{proj['number']}, {proj['item_count']} items)")
            print("  [+] Create a new project")
            print()
            choice = _prompt("Select a project", default="1")
            if choice.strip() == "+":
                create = True
            else:
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(existing):
                        project_number = existing[idx]["number"]
                        project_title = existing[idx]["title"]
                        create = False
                    else:
                        raise ValueError("out of range")
                except ValueError:
                    raise RuntimeError(
                        f"Invalid selection: {choice}. Enter a number 1-{len(existing)} or '+' to create."
                    )
        else:
            print(f"\nNo existing projects found for {owner}.")
            create = True

        if create:
            if not args.yes and not args.project_title:
                project_title = _prompt("Project name", default=default_title)
            try:
                project = _create_project(owner, project_title)
            except RuntimeError as exc:
                msg = str(exc)
                if "permission" in msg.lower() or "createProjectV2" in msg:
                    scopes = _gh_token_scopes()
                    if "project" not in scopes:
                        raise RuntimeError(
                            "GitHub token is missing the 'project' scope.\n"
                            "  Fix: gh auth refresh --scopes project\n"
                            "  Then re-run: solo-os init"
                        ) from None
                    raise RuntimeError(
                        f"Cannot create a project under '{owner}'.\n"
                        f"  Make sure '{owner}' is your GitHub username or an org you have admin access to.\n"
                        f"  Tip: Use @me to auto-detect your username: solo-os init --owner @me"
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
            scopes = _gh_token_scopes()
            if "project" not in scopes:
                raise RuntimeError(
                    f"Cannot access GitHub Project #{project_number} for '{owner}'.\n"
                    "  Your token is missing the 'project' scope.\n"
                    "  Fix: gh auth refresh --scopes project\n"
                    "  Then re-run: solo-os init"
                ) from None
            raise RuntimeError(
                f"Cannot access GitHub Project #{project_number} for '{owner}'.\n"
                f"  Make sure '{owner}' owns project #{project_number} and you have access.\n"
                f"  Verify at: https://github.com/{owner}?tab=projects"
            ) from None
        raise
    project_title = str(view_payload.get("title") or project_title)
    try:
        created_fields = _ensure_project_fields(owner, project_number)
    except RuntimeError as exc:
        msg = str(exc)
        if "permission" in msg.lower():
            scopes = _gh_token_scopes()
            if "project" not in scopes:
                raise RuntimeError(
                    "GitHub token is missing the 'project' scope required to manage project fields.\n"
                    "  Fix: gh auth refresh --scopes project\n"
                    "  Then re-run: solo-os init"
                ) from None
            raise RuntimeError(
                f"Cannot manage fields on project #{project_number} for '{owner}'.\n"
                f"  Make sure you have admin access to this project."
            ) from None
        raise

    repos = _collect_repos(
        cwd,
        interactive=not args.yes,
        repo_id_override=args.repo_id,
        repo_path_override=args.repo_path,
    )

    _write_config(
        config_path,
        owner=owner,
        owner_type=owner_type,
        project_number=project_number,
        project_title=project_title,
        repos=repos,
    )

    # Validate generated config can be parsed.
    with config_path.open(encoding="utf-8") as handle:
        parsed = yaml.safe_load(handle) or {}
    if not isinstance(parsed, dict):
        raise RuntimeError("Generated config is invalid YAML.")

    project_url = str(view_payload.get("url") or _project_url(owner, owner_type, project_number))
    repo_ids = [r.get("id", "") for r in repos]
    payload = {
        "owner": owner,
        "owner_type": owner_type,
        "project_number": project_number,
        "project_title": project_title,
        "project_url": project_url,
        "created_project": created_project,
        "created_fields": created_fields,
        "repos": repos,
        "config_path": str(config_path),
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print("\nsolo-os init complete.")
        print(f"- Config written: {config_path}")
        print(f"- Owner: {owner} ({owner_type})")
        print(f"- Project: #{project_number} ({project_title})")
        if created_project:
            print("- Project bootstrap: created new project")
        if created_fields:
            print(f"- Fields created: {', '.join(created_fields)}")
        else:
            print("- Fields created: none (already present)")
        print(f"- Repos: {', '.join(repo_ids)}")
        _print_view_guidance(project_url)
        print("\nNext steps:")
        print("1) Run `solo-os verify` to confirm setup")
        print("2) Run `solo-os onboarding` once (empty project + idea→roadmap→build loop + AI packs)")
        print("3) Run `solo-os workflow-start` for a compact tour, or create your first issues with `solo-os gh-create` + `--from-template`")
        print("4) Add/adjust issues on your GitHub Project with Kind/Status/Stage, then run `solo-os daily-triage` + `solo-os gh-next`")

    return 0
