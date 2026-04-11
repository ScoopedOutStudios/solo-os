"""Solo OS configuration: YAML loading and 3-tier root discovery."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

CONFIG_FILENAME = "solo-os.yml"
XDG_CONFIG_FILENAME = "config.yml"
XDG_APP_NAME = "solo-os"


class ConfigNotFoundError(FileNotFoundError):
    """Raised when no solo-os.yml can be located."""


def find_root(start: Path | None = None) -> Path:
    """Locate the directory containing solo-os.yml using 3-tier resolution.

    1. SOLO_OS_ROOT env var (explicit override)
    2. Walk up from *start* (default: cwd) looking for solo-os.yml
    3. XDG config home fallback (~/.config/solo-os/config.yml)
    """
    env_root = os.environ.get("SOLO_OS_ROOT")
    if env_root:
        root = Path(env_root).expanduser().resolve()
        if (root / CONFIG_FILENAME).is_file():
            return root
        raise ConfigNotFoundError(
            f"SOLO_OS_ROOT is set to {root} but {CONFIG_FILENAME} was not found there."
        )

    current = (start or Path.cwd()).resolve()
    while True:
        if (current / CONFIG_FILENAME).is_file():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent

    xdg_home = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    xdg_path = xdg_home / XDG_APP_NAME / XDG_CONFIG_FILENAME
    if xdg_path.is_file():
        return xdg_path.parent

    raise ConfigNotFoundError(
        f"Could not find {CONFIG_FILENAME}.\n"
        f"  Searched: cwd upward, $SOLO_OS_ROOT, ~/.config/{XDG_APP_NAME}/{XDG_CONFIG_FILENAME}\n"
        f"  Copy solo-os.example.yml to your workspace root and fill in your values."
    )


def _config_path(root: Path) -> Path:
    yml = root / CONFIG_FILENAME
    if yml.is_file():
        return yml
    return root / XDG_CONFIG_FILENAME


def load_config(root: Path | None = None) -> dict[str, Any]:
    """Parse solo-os.yml and resolve relative repo paths."""
    resolved_root = root or find_root()
    cfg_path = _config_path(resolved_root)
    with open(cfg_path, encoding="utf-8") as f:
        data: dict[str, Any] = yaml.safe_load(f) or {}

    for repo in data.get("repos", []):
        raw_path = repo.get("path", "")
        if raw_path:
            repo["_resolved_path"] = str((cfg_path.parent / raw_path).resolve())

    return data


def project_config(root: Path | None = None) -> dict[str, Any]:
    """Return GitHub project config in the shape expected by github_ops functions."""
    cfg = load_config(root)
    gh = cfg.get("github", {})
    fields = gh.get("fields", {})
    return {
        "owner": gh.get("owner", ""),
        "owner_type": gh.get("owner_type", "org"),
        "number": gh.get("project", {}).get("number", 0),
        "title": gh.get("project", {}).get("title", ""),
        "kindFieldName": fields.get("kind", {}).get("name", "Kind"),
        "statusFieldName": fields.get("status", {}).get("name", "Status"),
        "stageFieldName": fields.get("stage", {}).get("name", "Stage"),
    }


def repo_list(root: Path | None = None) -> list[dict[str, Any]]:
    """Return repos with resolved absolute paths."""
    cfg = load_config(root)
    repos = []
    for repo in cfg.get("repos", []):
        entry = {
            "id": repo.get("id", ""),
            "path": repo.get("_resolved_path", repo.get("path", "")),
            "active": repo.get("active", True),
        }
        repos.append(entry)
    return repos


def repo_alias_map(root: Path | None = None) -> dict[str, str]:
    """Build alias -> owner/repo-name map from config."""
    cfg = load_config(root)
    owner = cfg.get("github", {}).get("owner", "")
    aliases: dict[str, str] = {}
    for repo in cfg.get("repos", []):
        repo_id = repo.get("id", "")
        resolved_path = repo.get("_resolved_path", repo.get("path", ""))
        if not repo_id:
            continue
        repo_name = Path(resolved_path).name if resolved_path else repo_id
        full_repo = f"{owner}/{repo_name}"
        aliases[repo_id] = full_repo
        aliases[repo_name] = full_repo
        aliases[full_repo] = full_repo
    return aliases


def settings(section: str, root: Path | None = None) -> dict[str, Any]:
    """Return a settings section (validation, cleanup, daily_triage)."""
    cfg = load_config(root)
    return cfg.get(section, {})
