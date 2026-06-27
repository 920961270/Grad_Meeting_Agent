"""Workflow executor for the meeting report agent."""

from __future__ import annotations

from pathlib import Path

from src.agent.reporter import Reporter
from src.agent.state import AgentState
from src.agent.verifier import Verifier
from src.llm.base import LLMClient
from src.tools.experiment_reader import ExperimentReader
from src.tools.figure_reader import FigureReader
from src.tools.git_reader import GitReader
from src.tools.output_writer import OutputWriter
from src.tools.paper_reader import PaperReader
from src.tools.pptx_writer import PPTXWriter
from src.tools.progress_reader import ProgressReader
from src.tools.summarizer import Summarizer


class Executor:
    """Run planned workflow steps and update AgentState."""

    def __init__(
        self,
        state: AgentState,
        plan: list[dict[str, object]],
        llm_client: LLMClient | None,
        repo_dir: Path,
        days: int,
        ppt_template: Path | None = None,
        paper_source_mode: str = "pdf_first",
        use_paper_notes_as_sources: bool = False,
        with_slides: bool = False,
        export_details: bool = False,
    ) -> None:
        self.state = state
        self.plan = plan
        self.input_dir = Path(state.input_dir)
        self.output_dir = Path(state.output_dir)
        self.llm_client = llm_client
        self.repo_dir = repo_dir
        self.days = days
        self.ppt_template = ppt_template
        self.paper_source_mode = paper_source_mode
        self.use_paper_notes_as_sources = use_paper_notes_as_sources
        self.with_slides = with_slides
        self.export_details = export_details
        self.writer = OutputWriter(self.output_dir)
        self.state.paper_source_mode = paper_source_mode
        self.state.use_paper_notes_as_sources = use_paper_notes_as_sources

    def run(self) -> AgentState:
        """Execute the plan from readers through verification."""
        self.state.status = "running"
        for step in self.plan:
            if not step.get("enabled", True):
                continue
            step_id = str(step["id"])
            getattr(self, f"_run_{step_id}")()

        self.state.status = "passed" if self.state.verifier_results.get("passed") else "needs_review"
        self.writer.write_state(self.state)
        return self.state

    def _run_read_progress(self) -> None:
        result = ProgressReader(self.input_dir).read()
        self.state.research_context.update(result)
        self.state.progress_summary = result.get("combined", "")
        self.state.add_step("read_progress", "read progress.md and notes.md")

    def _run_read_papers(self) -> None:
        result = PaperReader(
            self.input_dir,
            paper_source_mode=self.paper_source_mode,
            use_paper_notes_as_sources=self.use_paper_notes_as_sources,
        ).read()
        self.state.paper_summaries = result["summaries"]
        self.state.supplementary_notes = str(result.get("supplementary_notes", ""))
        self.state.detected_pdf_papers = [str(item) for item in result.get("pdf_files", [])]
        self.state.paper_source_mode = str(result.get("paper_source_mode", self.paper_source_mode))
        self.state.use_paper_notes_as_sources = bool(
            result.get("use_paper_notes_as_sources", self.use_paper_notes_as_sources)
        )
        if result.get("raw"):
            self.state.research_context["paper_notes"] = str(result["raw"])
        pdf_files = result.get("pdf_files", [])
        if pdf_files:
            self.state.research_context["pdf_papers"] = ", ".join(str(item) for item in pdf_files)
        for warning in result.get("warnings", []):
            self.state.warnings.append(str(warning))
        self.state.add_step(
            "read_papers",
            f"found {len(self.state.paper_summaries)} paper summaries; detected_pdf={bool(pdf_files)}",
        )

    def _run_read_experiments(self) -> None:
        result = ExperimentReader(self.input_dir / "experiment_results").read()
        self.state.experiment_summary = result
        self.state.add_step("read_experiments", f"read {len(result.get('files', []))} experiment files")

    def _run_read_figures(self) -> None:
        result = FigureReader(self.input_dir / "figures").read()
        self.state.figure_summary = result
        self.state.add_step("read_figures", f"read {len(result.get('files', []))} figure files")

    def _run_read_git(self) -> None:
        result = GitReader(self.repo_dir, days=self.days).read()
        self.state.git_summary = result
        for warning in result.get("warnings", []):
            self.state.warnings.append(str(warning))
        count = len(result.get("commits", []))
        self.state.add_step("read_git", f"found {count} recent commits")

    def _run_summarize(self) -> None:
        summarizer = Summarizer(llm_client=self.llm_client)
        self.state.report_sections = summarizer.summarize(self.state)
        self.state.add_step("summarize", "built report sections with fallback-safe summarizer")

    def _run_report(self) -> None:
        for warning in self.writer.cleanup_generated_outputs():
            self.state.warnings.append(warning)

        reporter = Reporter()
        documents = {"meeting_pack.md": reporter.build_meeting_pack(self.state)}

        if self.export_details:
            for filename, content in reporter.build_detail_documents(self.state).items():
                documents[f"details/{filename}"] = content

        if self.with_slides:
            documents["ppt_outline.md"] = reporter.build_ppt_outline(self.state)

        written = self.writer.write_markdown_files(documents)

        if self.with_slides:
            pptx_writer = PPTXWriter(self.output_dir, template_path=self.ppt_template)
            pptx_file = pptx_writer.write_deck(self.state)
            if pptx_file:
                written.append(pptx_file)
            else:
                self.state.warnings.append(
                    pptx_writer.last_warning
                    or "PPTX export skipped because python-pptx is unavailable."
                )
        self.state.generated_files = written + ["agent_state.json"]
        self.state.add_step("report", f"wrote {len(written)} report files")

    def _run_verify(self) -> None:
        self.state.verifier_results = Verifier(
            self.output_dir,
            input_dir=self.input_dir,
            use_paper_notes_as_sources=self.use_paper_notes_as_sources,
            detected_pdf_papers=self.state.detected_pdf_papers,
            with_slides=self.with_slides,
            export_details=self.export_details,
        ).verify()
        quality_checks = self.state.verifier_results.get("quality_checks", {})
        if isinstance(quality_checks, dict):
            if self.with_slides and "group_meeting_slides.pptx" not in self.state.generated_files:
                quality_checks["pptx_generated_this_run"] = {
                    "passed": False,
                    "reason": "group_meeting_slides.pptx was not written during this run.",
                }
                self.state.verifier_results["passed"] = False
            self.state.quality_checks = quality_checks
        passed = self.state.verifier_results.get("passed", False)
        self.state.add_step("verify", f"passed={passed}")
