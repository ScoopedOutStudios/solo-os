"""Solo OS — AI-assisted operating layer for GitHub Projects-based execution."""

from __future__ import annotations


def _get_version() -> str:
    try:
        from importlib.metadata import version

        return version("solo-os")
    except Exception:
        return "0.0.0-unknown"


__version__ = _get_version()
