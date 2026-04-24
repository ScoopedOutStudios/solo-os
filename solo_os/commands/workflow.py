"""Workflow entrypoints: guided tours and glue commands."""

from __future__ import annotations

import sys
from pathlib import Path


def handle_workflow_start() -> int:
    """Print a guided walkthrough of Idea -> Roadmap -> Build Loop in Solo OS."""
    guide = Path(__file__).resolve().parent.parent / "templates" / "workflow-start.md"
    if not guide.is_file():
        print(f"Error: workflow start guide not found at {guide}", file=sys.stderr)
        return 1
    text = guide.read_text(encoding="utf-8")
    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")
    return 0