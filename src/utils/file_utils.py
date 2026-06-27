"""Filesystem helpers."""

from __future__ import annotations

from pathlib import Path


def read_text_if_exists(path: Path) -> str:
    """Read UTF-8 text when a file exists, otherwise return an empty string."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")
