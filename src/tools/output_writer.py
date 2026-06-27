"""Output writer for Markdown and JSON artifacts."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from src.agent.state import AgentState


class OutputWriter:
    """Write generated files to an output directory."""

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_markdown_files(self, documents: dict[str, str]) -> list[str]:
        """Write Markdown documents and return file names."""
        written: list[str] = []
        for filename, content in documents.items():
            path = self.output_dir / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            written.append(filename)
        return written

    def cleanup_generated_outputs(self) -> list[str]:
        """Remove known generated artifacts from previous runs."""
        warnings: list[str] = []
        root_files = [
            ".gitkeep",
            "meeting_pack.md",
            "research_brief.md",
            "paper_cards.md",
            "experiment_insights.md",
            "meeting_agenda.md",
            "weekly_report.md",
            "oral_script.md",
            "supervisor_qa.md",
            "next_week_plan.md",
            "ppt_outline.md",
            "group_meeting_slides.pptx",
            "group_meeting_slides_verified.pptx",
        ]
        for filename in root_files:
            path = self.output_dir / filename
            if not path.exists():
                continue
            try:
                path.unlink()
            except PermissionError:
                warnings.append(f"Could not remove locked generated file: {path}")

        details_dir = self.output_dir / "details"
        if details_dir.exists():
            try:
                shutil.rmtree(details_dir)
            except PermissionError:
                warnings.append(f"Could not remove locked generated directory: {details_dir}")
        return warnings

    def write_state(self, state: AgentState) -> str:
        """Write agent_state.json and return the file name."""
        path = self.output_dir / "agent_state.json"
        path.write_text(json.dumps(state.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        return "agent_state.json"
