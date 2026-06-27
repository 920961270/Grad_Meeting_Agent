"""Figure and screenshot inventory reader."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class FigureReader:
    """Record image files that may be useful for meeting slides."""

    IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff", ".gif", ".svg"}

    def __init__(self, figures_dir: Path) -> None:
        self.figures_dir = figures_dir

    def read(self) -> dict[str, Any]:
        """Return a lightweight inventory without image understanding."""
        if not self.figures_dir.exists():
            return {"files": [], "items": [], "warnings": []}

        items: list[dict[str, str]] = []
        for path in sorted(self.figures_dir.glob("*")):
            if path.suffix.lower() not in self.IMAGE_EXTENSIONS:
                continue
            items.append(
                {
                    "file": path.name,
                    "type": self._classify(path.name),
                    "suggested_use": self._suggested_use(path.name),
                }
            )
        return {"files": [item["file"] for item in items], "items": items, "warnings": []}

    def _classify(self, filename: str) -> str:
        """Classify image intent from filename keywords."""
        name = filename.lower()
        if "before" in name or "after" in name or "compare" in name or "comparison" in name:
            return "before_after_or_comparison"
        if "fail" in name or "error" in name or "bad" in name or "risk" in name:
            return "failure_case"
        if "chart" in name or "curve" in name or "metric" in name or "plot" in name:
            return "metric_chart"
        if "result" in name or "demo" in name or "sample" in name:
            return "result_example"
        return "supporting_figure"

    def _suggested_use(self, filename: str) -> str:
        """Suggest how the image could be used in a group meeting."""
        figure_type = self._classify(filename)
        suggestions = {
            "before_after_or_comparison": "用于展示增强前后或方法对比。",
            "failure_case": "用于说明当前问题、风险或失败案例。",
            "metric_chart": "用于支撑实验结果趋势和指标分析。",
            "result_example": "用于展示代表性实验结果。",
            "supporting_figure": "可作为组会展示的补充图像材料。",
        }
        return suggestions[figure_type]
