"""Shared terminal display helpers — colors, formatting, layout."""

from __future__ import annotations

import os
import shutil
import sys
import textwrap

ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_DIM = "\033[2m"
ANSI_RED = "\033[31m"
ANSI_GREEN = "\033[32m"
ANSI_YELLOW = "\033[33m"
ANSI_BLUE = "\033[34m"
ANSI_MAGENTA = "\033[35m"
ANSI_CYAN = "\033[36m"
ANSI_WHITE = "\033[37m"


def color_enabled(mode: str) -> bool:
    if mode == "always":
        return True
    if mode == "never":
        return False
    term = os.environ.get("TERM", "")
    return sys.stdout.isatty() and term.lower() != "dumb"


def paint(text: str, *codes: str, enabled: bool) -> str:
    if not enabled or not codes:
        return text
    return f"{''.join(codes)}{text}{ANSI_RESET}"


def terminal_width() -> int:
    return max(72, min(shutil.get_terminal_size(fallback=(110, 24)).columns, 140))


def short_repo_name(repo: str) -> str:
    if "/" in repo:
        return repo.split("/", 1)[1]
    return repo


def wrap_block(
    text: str,
    *,
    indent: str,
    width: int,
    subsequent_indent: str | None = None,
) -> str:
    return textwrap.fill(
        text,
        width=max(20, width),
        initial_indent=indent,
        subsequent_indent=subsequent_indent or indent,
        break_long_words=False,
        break_on_hyphens=False,
    )


def status_display(status: str, enabled: bool) -> str:
    palette = {
        "In Progress": (ANSI_BOLD, ANSI_BLUE),
        "Prioritized": (ANSI_BOLD, ANSI_YELLOW),
        "Todo": (ANSI_MAGENTA,),
        "Backlog": (ANSI_DIM,),
        "Blocked": (ANSI_BOLD, ANSI_RED),
        "Done": (ANSI_GREEN,),
    }
    label = status.upper() if status else "-"
    return paint(label, *palette.get(status, ()), enabled=enabled)


def kind_display(kind: str, enabled: bool) -> str:
    palette = {
        "Idea": (ANSI_MAGENTA,),
        "Roadmap": (ANSI_CYAN,),
        "Build Loop": (ANSI_BLUE,),
    }
    label = kind or "-"
    return paint(label, *palette.get(kind, ()), enabled=enabled)


def display_title(title: str) -> str:
    normalized = title.replace("[Initiative]", "[Build Loop]")
    return normalized.replace("[Ops]", "[Build Loop]")
