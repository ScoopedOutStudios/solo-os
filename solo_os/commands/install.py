"""Install agents, skills, and commands from the solo-os package."""

from __future__ import annotations

import shutil
import tempfile
import urllib.request
import zipfile
from os.path import commonpath
from pathlib import Path
from typing import Literal

from solo_os import config

IdeName = Literal["cursor", "claude-code", "codex"]
AgentsIdeName = Literal["cursor", "claude-code"]
CommandsIdeName = Literal["cursor", "claude-code"]

DEFAULT_ASSET_REF = "main"
ASSET_ARCHIVE_URL = "https://github.com/ScoopedOutStudios/solo-os/archive/refs/heads/{ref}.zip"

AGENTS_TARGETS: dict[AgentsIdeName, Path] = {
    "cursor": Path.home() / ".cursor" / "agents",
    "claude-code": Path.home() / ".claude" / "agents",
}

SKILLS_TARGETS: dict[IdeName, Path] = {
    "cursor": Path.home() / ".cursor" / "skills",
    "claude-code": Path.home() / ".claude" / "skills",
    # Codex docs recommend Agent Skills in ~/.agents/skills, not ~/.codex/skills.
    "codex": Path.home() / ".agents" / "skills",
}

COMMANDS_TARGETS: dict[CommandsIdeName, Path] = {
    "cursor": Path(".cursor") / "commands" / "solo-os",
    # Claude keeps legacy commands support, though skills are preferred long-term.
    "claude-code": Path(".claude") / "commands" / "solo-os",
}


def _resolve_ide(args: object) -> IdeName:
    ide = getattr(args, "ide", "cursor") or "cursor"
    if ide not in SKILLS_TARGETS:
        raise RuntimeError(
            f"Unsupported IDE '{ide}'. Expected one of: {', '.join(SKILLS_TARGETS)}"
        )
    return ide  # type: ignore[return-value]


def _resolve_target(args: object, kind: str) -> tuple[str, Path]:
    ide = _resolve_ide(args)
    target = getattr(args, "target", None)
    if kind == "agents" and ide not in AGENTS_TARGETS:
        raise RuntimeError(
            "IDE profile 'codex' is not supported for install-agents. "
            "Codex custom agents use TOML files in .codex/agents or ~/.codex/agents."
        )
    if kind == "commands" and ide not in COMMANDS_TARGETS:
        raise RuntimeError(
            "IDE profile 'codex' is not supported for install-commands. "
            "Codex best practices recommend AGENTS.md + skills instead of markdown command packs."
        )
    if target:
        return ide, Path(target).expanduser().resolve()
    if kind == "agents":
        return ide, AGENTS_TARGETS[ide]  # type: ignore[index]
    if kind == "skills":
        return ide, SKILLS_TARGETS[ide]
    if kind == "commands":
        return ide, _workspace_command_target(COMMANDS_TARGETS[ide])  # type: ignore[index]
    raise RuntimeError(f"Unsupported install kind: {kind}")


def _pkg_root() -> Path:
    """Return the solo-os repo/package root (parent of solo_os/)."""
    return Path(__file__).resolve().parent.parent.parent


def _workspace_command_target(relative_target: Path) -> Path:
    """Resolve workspace-local command target from solo-os config when available."""
    try:
        root = config.find_root(start=Path.cwd())
    except config.ConfigNotFoundError:
        root = Path.cwd()
    return (root / relative_target).resolve()


def _download_asset_pack(kind: str) -> Path:
    """Fetch bundled AI assets from the public repo when wheel installs lack source dirs."""
    ref = DEFAULT_ASSET_REF
    url = ASSET_ARCHIVE_URL.format(ref=ref)
    tmp_dir = Path(tempfile.mkdtemp(prefix="solo-os-assets-"))
    archive_path = tmp_dir / "solo-os.zip"
    try:
        urllib.request.urlretrieve(url, archive_path)  # noqa: S310 - fixed public GitHub URL.
        with zipfile.ZipFile(archive_path) as archive:
            for member in archive.infolist():
                target = (tmp_dir / member.filename).resolve()
                if commonpath([str(tmp_dir.resolve()), str(target)]) != str(tmp_dir.resolve()):
                    raise RuntimeError(f"Unsafe path in downloaded archive: {member.filename}")
            archive.extractall(tmp_dir)
    except Exception as exc:  # pragma: no cover - network failures are environment-specific
        raise RuntimeError(
            f"Could not fetch Solo OS {kind} assets from {url}: {exc}\n"
            "Try again with network access, or pass --target from a full solo-os checkout."
        ) from exc

    extracted_roots = [p for p in tmp_dir.iterdir() if p.is_dir() and p.name.startswith("solo-os-")]
    if not extracted_roots:
        raise RuntimeError(f"Downloaded Solo OS archive did not contain an extracted repo root: {url}")
    src = extracted_roots[0] / kind
    if not src.exists():
        raise RuntimeError(f"Downloaded Solo OS archive did not contain '{kind}' assets: {url}")
    return src


def _asset_source(kind: str) -> tuple[Path, str]:
    """Resolve asset source from checkout first, then public GitHub fallback for wheels."""
    checkout_src = _pkg_root() / kind
    if checkout_src.exists():
        return checkout_src, "local checkout"
    return _download_asset_pack(kind), "public GitHub archive"


def _copy_files(
    src: Path,
    dst: Path,
    *,
    force: bool = False,
    glob_pattern: str = "*.md",
    recursive: bool = False,
) -> list[str]:
    """Copy files matching *glob_pattern* from *src* to *dst*.

    Returns list of installed file names.
    """
    dst.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []

    if recursive:
        for child in sorted(src.iterdir()):
            if child.is_dir() and not child.name.startswith("."):
                target_dir = dst / child.name
                target_dir.mkdir(parents=True, exist_ok=True)
                for f in sorted(child.rglob(glob_pattern)):
                    if f.is_file():
                        rel = f.relative_to(child)
                        dest_file = target_dir / rel
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                        if dest_file.exists() and not force:
                            print(f"  skip (exists): {child.name}/{rel}")
                            continue
                        shutil.copy2(f, dest_file)
                        installed.append(f"{child.name}/{rel}")
        readme = src / "README.md"
        if readme.exists():
            dest_readme = dst / "README.md"
            if not dest_readme.exists() or force:
                shutil.copy2(readme, dest_readme)
                installed.append("README.md")
    else:
        for f in sorted(src.glob(glob_pattern)):
            if f.is_file():
                dest_file = dst / f.name
                if dest_file.exists() and not force:
                    print(f"  skip (exists): {f.name}")
                    continue
                shutil.copy2(f, dest_file)
                installed.append(f.name)

    return installed


def handle_install_agents(args: object) -> int:
    ide, target = _resolve_target(args, "agents")
    force = getattr(args, "force", False)
    src, source_label = _asset_source("agents")

    print(f"Installing agents for IDE '{ide}' from {source_label} to {target} ...")
    installed = _copy_files(src, target, force=force, glob_pattern="*.md")
    print(f"  {len(installed)} file(s) installed.")
    return 0


def handle_install_skills(args: object) -> int:
    ide, target = _resolve_target(args, "skills")
    force = getattr(args, "force", False)
    src, source_label = _asset_source("skills")

    print(f"Installing skills for IDE '{ide}' from {source_label} to {target} ...")
    installed = _copy_files(
        src, target, force=force, glob_pattern="*.md", recursive=True
    )
    print(f"  {len(installed)} file(s) installed across skill folders.")
    return 0


def handle_install_commands(args: object) -> int:
    ide, target = _resolve_target(args, "commands")
    force = getattr(args, "force", False)
    src, source_label = _asset_source("commands")

    print(f"Installing commands for IDE '{ide}' from {source_label} to {target} ...")
    installed = _copy_files(src, target, force=force, glob_pattern="*.md")
    print(f"  {len(installed)} file(s) installed.")
    return 0
