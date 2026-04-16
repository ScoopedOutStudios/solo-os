"""Install agents, skills, and commands from the solo-os package."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Literal

IdeName = Literal["cursor", "claude-code", "codex"]
AgentsIdeName = Literal["cursor", "claude-code"]
CommandsIdeName = Literal["cursor", "claude-code"]

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
        return ide, Path(target)
    if kind == "agents":
        return ide, AGENTS_TARGETS[ide]  # type: ignore[index]
    if kind == "skills":
        return ide, SKILLS_TARGETS[ide]
    if kind == "commands":
        return ide, COMMANDS_TARGETS[ide]  # type: ignore[index]
    raise RuntimeError(f"Unsupported install kind: {kind}")


def _pkg_root() -> Path:
    """Return the solo-os repo/package root (parent of solo_os/)."""
    return Path(__file__).resolve().parent.parent.parent


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
    src = _pkg_root() / "agents"

    if not src.exists():
        print(f"Error: agents directory not found at {src}")
        return 1

    print(f"Installing agents for IDE '{ide}' to {target} ...")
    installed = _copy_files(src, target, force=force, glob_pattern="*.md")
    print(f"  {len(installed)} file(s) installed.")
    return 0


def handle_install_skills(args: object) -> int:
    ide, target = _resolve_target(args, "skills")
    force = getattr(args, "force", False)
    src = _pkg_root() / "skills"

    if not src.exists():
        print(f"Error: skills directory not found at {src}")
        return 1

    print(f"Installing skills for IDE '{ide}' to {target} ...")
    installed = _copy_files(
        src, target, force=force, glob_pattern="*.md", recursive=True
    )
    print(f"  {len(installed)} file(s) installed across skill folders.")
    return 0


def handle_install_commands(args: object) -> int:
    ide, target = _resolve_target(args, "commands")
    force = getattr(args, "force", False)
    src = _pkg_root() / "commands"

    if not src.exists():
        print(f"Error: commands directory not found at {src}")
        return 1

    print(f"Installing commands for IDE '{ide}' to {target} ...")
    installed = _copy_files(src, target, force=force, glob_pattern="*.md")
    print(f"  {len(installed)} file(s) installed.")
    return 0
