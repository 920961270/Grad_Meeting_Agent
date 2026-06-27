"""Git history reader."""

from __future__ import annotations

import subprocess
from pathlib import Path


class GitReader:
    """Read recent git commits without failing the workflow."""

    def __init__(self, repo_dir: Path, days: int = 7) -> None:
        self.repo_dir = repo_dir
        self.days = days

    def read(self) -> dict[str, object]:
        """Return recent commits and warnings."""
        if not (self.repo_dir / ".git").exists():
            return {"commits": [], "warnings": ["Current directory is not a git repository."]}
        try:
            result = subprocess.run(
                [
                    "git",
                    "-C",
                    str(self.repo_dir),
                    "log",
                    f"--since={self.days} days ago",
                    "--pretty=format:%h | %ad | %s",
                    "--date=short",
                ],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        except Exception as exc:
            return {"commits": [], "warnings": [f"Failed to read git log: {exc}"]}

        commits = [line for line in result.stdout.splitlines() if line.strip()]
        return {"commits": commits, "warnings": []}
