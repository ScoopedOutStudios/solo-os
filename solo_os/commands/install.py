"""Install agents, skills, and commands from the solo-os package."""

from __future__ import annotations

import shutil
from pathlib import Path


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
    target = Path(getattr(args, "target", None) or Path.home() / ".cursor" / "agents")
    force = getattr(args, "force", False)
    src = _pkg_root() / "agents"

    if not src.exists():
        print(f"Error: agents directory not found at {src}")
        return 1

    print(f"Installing agents to {target} ...")
    installed = _copy_files(src, target, force=force, glob_pattern="*.md")
    print(f"  {len(installed)} file(s) installed.")
    return 0


def handle_install_skills(args: object) -> int:
    target = Path(getattr(args, "target", None) or Path.home() / ".cursor" / "skills")
    force = getattr(args, "force", False)
    src = _pkg_root() / "skills"

    if not src.exists():
        print(f"Error: skills directory not found at {src}")
        return 1

    print(f"Installing skills to {target} ...")
    installed = _copy_files(
        src, target, force=force, glob_pattern="*.md", recursive=True
    )
    print(f"  {len(installed)} file(s) installed across skill folders.")
    return 0


def handle_install_commands(args: object) -> int:
    target = Path(
        getattr(args, "target", None)
        or Path(".cursor") / "commands" / "solo-os"
    )
    force = getattr(args, "force", False)
    src = _pkg_root() / "commands"

    if not src.exists():
        print(f"Error: commands directory not found at {src}")
        return 1

    print(f"Installing commands to {target} ...")
    installed = _copy_files(src, target, force=force, glob_pattern="*.md")
    print(f"  {len(installed)} file(s) installed.")
    return 0
