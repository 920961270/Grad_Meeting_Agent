"""Common LLM client protocol."""

from __future__ import annotations

from typing import Protocol


class LLMClient(Protocol):
    """Minimal generation interface used by the summarizer."""

    def generate(self, prompt: str) -> str | None:
        """Generate text or return None when the backend is unavailable."""
        ...
