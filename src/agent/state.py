"""Runtime state for the graduate meeting workflow agent."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


def now_iso() -> str:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


@dataclass
class AgentState:
    """Transparent state shared by planner, tools, reporter, and verifier."""

    task_id: str
    created_at: str
    input_dir: str
    output_dir: str
    detected_inputs: list[str] = field(default_factory=list)
    research_context: dict[str, str] = field(default_factory=dict)
    paper_summaries: list[dict[str, object]] = field(default_factory=list)
    supplementary_notes: str = ""
    paper_source_mode: str = "pdf_first"
    use_paper_notes_as_sources: bool = False
    detected_pdf_papers: list[str] = field(default_factory=list)
    progress_summary: str = ""
    experiment_summary: dict[str, object] = field(default_factory=dict)
    figure_summary: dict[str, object] = field(default_factory=dict)
    git_summary: dict[str, object] = field(default_factory=dict)
    report_sections: dict[str, object] = field(default_factory=dict)
    generated_files: list[str] = field(default_factory=list)
    verifier_results: dict[str, object] = field(default_factory=dict)
    quality_checks: dict[str, object] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    status: str = "created"
    execution_plan: list[dict[str, object]] = field(default_factory=list)
    step_log: list[dict[str, str]] = field(default_factory=list)

    @classmethod
    def create(cls, input_dir: Path, output_dir: Path) -> "AgentState":
        """Create a fresh state object for one run."""
        return cls(
            task_id=f"grad-meeting-{uuid4().hex[:8]}",
            created_at=now_iso(),
            input_dir=str(input_dir),
            output_dir=str(output_dir),
        )

    def add_step(self, name: str, detail: str) -> None:
        """Append a human-readable execution step."""
        self.step_log.append({"time": now_iso(), "name": name, "detail": detail})

    def to_dict(self) -> dict[str, object]:
        """Convert state to a JSON-serializable dictionary."""
        return asdict(self)
