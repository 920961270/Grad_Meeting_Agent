"""Experiment result reader for JSON and CSV files."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean
from typing import Any


class ExperimentReader:
    """Read structured experiment files and summarize key fields."""

    def __init__(self, experiment_dir: Path) -> None:
        self.experiment_dir = experiment_dir

    def read(self) -> dict[str, Any]:
        """Read all JSON and CSV experiment files."""
        if not self.experiment_dir.exists():
            return {"files": [], "metrics": {}, "tables": [], "warnings": ["experiment_results not found"]}

        files: list[str] = []
        metrics: dict[str, Any] = {}
        tables: list[dict[str, Any]] = []
        warnings: list[str] = []

        for path in sorted(self.experiment_dir.glob("*")):
            if path.suffix.lower() == ".json":
                files.append(path.name)
                try:
                    data = json.loads(path.read_text(encoding="utf-8"))
                    metrics[path.name] = data
                except Exception as exc:
                    warnings.append(f"Failed to parse {path.name}: {exc}")
            elif path.suffix.lower() == ".csv":
                files.append(path.name)
                try:
                    tables.append(self._read_csv(path))
                except Exception as exc:
                    warnings.append(f"Failed to parse {path.name}: {exc}")

        return {
            "files": files,
            "metrics": metrics,
            "tables": tables,
            "numeric_highlights": self._numeric_highlights(metrics, tables),
            "warnings": warnings,
        }

    def _read_csv(self, path: Path) -> dict[str, Any]:
        """Read a CSV file into a compact table summary."""
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
        return {
            "file": path.name,
            "columns": reader.fieldnames or [],
            "row_count": len(rows),
            "sample_rows": rows[:3],
        }

    def _numeric_highlights(self, metrics: dict[str, Any], tables: list[dict[str, Any]]) -> dict[str, float]:
        """Collect simple numeric averages from JSON metrics and CSV samples."""
        values: dict[str, list[float]] = {}

        def collect(prefix: str, obj: Any) -> None:
            if isinstance(obj, dict):
                for key, value in obj.items():
                    collect(f"{prefix}.{key}" if prefix else str(key), value)
            elif isinstance(obj, list):
                for item in obj:
                    collect(prefix, item)
            elif isinstance(obj, (int, float)):
                values.setdefault(prefix, []).append(float(obj))

        collect("", metrics)
        for table in tables:
            for row in table.get("sample_rows", []):
                for key, value in row.items():
                    try:
                        values.setdefault(str(key), []).append(float(value))
                    except (TypeError, ValueError):
                        continue
        return {key: round(mean(items), 4) for key, items in values.items() if items}
