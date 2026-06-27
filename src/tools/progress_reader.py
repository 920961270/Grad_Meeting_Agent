"""Readers for progress and free-form notes."""

from __future__ import annotations

from pathlib import Path

from src.utils.file_utils import read_text_if_exists
from src.utils.template_filter import remove_placeholder_lines


class ProgressReader:
    """Read progress.md and notes.md from an input directory."""

    def __init__(self, input_dir: Path) -> None:
        self.input_dir = input_dir

    def read(self) -> dict[str, str]:
        """Return progress, notes, and a combined text block."""
        progress = remove_placeholder_lines(read_text_if_exists(self.input_dir / "progress.md"))
        notes = remove_placeholder_lines(read_text_if_exists(self.input_dir / "notes.md"))
        combined = "\n\n".join(part for part in [progress, notes] if part)
        return {"progress": progress, "notes": notes, "combined": combined}
