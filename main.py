"""Command line entrypoint for grad-meeting-agent."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

from src.agent.executor import Executor
from src.agent.planner import Planner
from src.agent.state import AgentState
from src.llm.ollama_client import OllamaClient
from src.llm.openai_client import OpenAIClient


def load_config(path: Path) -> dict[str, Any]:
    """Load YAML config when PyYAML is installed, otherwise return defaults."""
    if not path.exists():
        return {}
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data or {}
    except Exception:
        return {}


def build_llm_client(backend: str, config: dict[str, Any]):
    """Create an optional LLM client for the selected backend."""
    llm_config = config.get("llm", {}) if isinstance(config, dict) else {}
    if backend == "openai":
        return OpenAIClient(model=llm_config.get("openai_model", "gpt-4o-mini"))
    if backend == "ollama":
        return OllamaClient(
            model=llm_config.get("ollama_model", "qwen2.5:3b"),
            url=llm_config.get("ollama_url", "http://localhost:11434/api/generate"),
        )
    return None


def resolve_optional_path(value: str | None) -> Path | None:
    """Resolve a config path relative to the current working directory."""
    if not value:
        return None
    return Path(value).resolve()


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate graduate group meeting reports.")
    parser.add_argument("--input", default="input", help="Input directory with notes and results.")
    parser.add_argument("--output", default="output", help="Output directory for generated files.")
    parser.add_argument(
        "--backend",
        choices=("openai", "ollama", "rule"),
        default="rule",
        help="LLM backend. Rule runs offline.",
    )
    parser.add_argument("--config", default="config.yaml", help="Path to config YAML.")
    parser.add_argument("--days", type=int, default=None, help="Days of git history to inspect.")
    parser.add_argument("--with-slides", action="store_true", help="Also generate PPTX and ppt_outline.md.")
    parser.add_argument("--export-details", action="store_true", help="Also export detailed Markdown files under output/details/.")
    parser.add_argument("--all", action="store_true", help="Generate meeting pack, slides, and all detailed files.")
    return parser.parse_args()


def main() -> int:
    """Run the full agent workflow."""
    args = parse_args()
    config = load_config(Path(args.config))
    days = args.days or int(config.get("report", {}).get("days", 7))
    with_slides = bool(args.with_slides or args.all)
    export_details = bool(args.export_details or args.all)

    input_dir = Path(args.input).resolve()
    output_dir = Path(args.output).resolve()

    state = AgentState.create(input_dir=input_dir, output_dir=output_dir)
    state.add_step(
        "start",
        f"backend={args.backend}, days={days}, with_slides={with_slides}, export_details={export_details}",
    )

    if args.backend == "openai" and not os.getenv("OPENAI_API_KEY"):
        state.warnings.append("OPENAI_API_KEY is not set; falling back to rule-based content.")

    planner = Planner(input_dir=input_dir, repo_dir=Path.cwd(), days=days)
    plan = planner.create_plan(state)

    executor = Executor(
        state=state,
        plan=plan,
        llm_client=build_llm_client(args.backend, config),
        repo_dir=Path.cwd(),
        days=days,
        ppt_template=resolve_optional_path(config.get("ppt_template")),
        paper_source_mode=str(config.get("paper_source_mode", "pdf_first")),
        use_paper_notes_as_sources=bool(config.get("use_paper_notes_as_sources", False)),
        with_slides=with_slides,
        export_details=export_details,
    )
    executor.run()

    print("Core output:")
    print("- meeting_pack.md")

    print("\nOptional:")
    print("- use --with-slides to generate PPTX")
    print("- use --export-details to export detailed markdown files")
    print("- use --all to generate everything")

    if with_slides or export_details:
        print("\nGenerated files:")
        for filename in state.generated_files:
            print(f"- {filename}")

    passed = state.verifier_results.get("passed", False)
    print(f"\nVerifier passed: {passed}")
    if state.warnings:
        print("\nWarnings:")
        for warning in state.warnings:
            print(f"- {warning}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
