"""Execution planner for available research inputs."""

from __future__ import annotations

from pathlib import Path

from src.agent.state import AgentState


class Planner:
    """Build a small, file-aware execution plan."""

    def __init__(self, input_dir: Path, repo_dir: Path, days: int = 7) -> None:
        self.input_dir = input_dir
        self.repo_dir = repo_dir
        self.days = days

    def create_plan(self, state: AgentState) -> list[dict[str, object]]:
        """Detect inputs and create an ordered plan."""
        detected = self._detect_inputs()
        state.detected_inputs = detected

        plan: list[dict[str, object]] = []
        if any(name in detected for name in ("progress.md", "notes.md")):
            plan.append({"id": "read_progress", "tool": "ProgressReader", "enabled": True})
        if "paper_notes.md" in detected or any(name.startswith("papers/") for name in detected):
            plan.append({"id": "read_papers", "tool": "PaperReader", "enabled": True})
        if any(name.startswith("experiment_results/") for name in detected):
            plan.append({"id": "read_experiments", "tool": "ExperimentReader", "enabled": True})
        if any(name.startswith("figures/") for name in detected):
            plan.append({"id": "read_figures", "tool": "FigureReader", "enabled": True})
        plan.append({"id": "read_git", "tool": "GitReader", "enabled": True, "days": self.days})
        plan.append({"id": "summarize", "tool": "Summarizer", "enabled": True})
        plan.append({"id": "report", "tool": "Reporter", "enabled": True})
        plan.append({"id": "verify", "tool": "Verifier", "enabled": True})

        state.execution_plan = plan
        state.status = "planned"
        state.add_step("planner", f"created {len(plan)} steps from {len(detected)} inputs")
        return plan

    def _detect_inputs(self) -> list[str]:
        """Return known input files that exist in the input directory."""
        detected: list[str] = []
        for filename in ("progress.md", "notes.md", "paper_notes.md"):
            if (self.input_dir / filename).exists():
                detected.append(filename)

        papers_dir = self.input_dir / "papers"
        if papers_dir.exists():
            for path in sorted(papers_dir.glob("*.pdf")):
                detected.append(f"papers/{path.name}")

        experiment_dir = self.input_dir / "experiment_results"
        if experiment_dir.exists():
            for path in sorted(experiment_dir.glob("*")):
                if path.suffix.lower() in {".json", ".csv"}:
                    detected.append(f"experiment_results/{path.name}")

        figures_dir = self.input_dir / "figures"
        if figures_dir.exists():
            for path in sorted(figures_dir.glob("*")):
                if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff", ".gif", ".svg"}:
                    detected.append(f"figures/{path.name}")

        if (self.repo_dir / ".git").exists():
            detected.append("git_recent_commits")
        return detected
