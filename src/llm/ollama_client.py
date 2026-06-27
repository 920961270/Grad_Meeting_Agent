"""Ollama backend client."""

from __future__ import annotations

import json
import urllib.error
import urllib.request


class OllamaClient:
    """Call a local Ollama generate endpoint."""

    def __init__(self, model: str = "qwen2.5:3b", url: str = "http://localhost:11434/api/generate") -> None:
        self.model = model
        self.url = url
        self.last_error: str | None = None

    def generate(self, prompt: str) -> str | None:
        """Generate text with Ollama, returning None if unavailable."""
        payload = json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode("utf-8")
        request = urllib.request.Request(
            self.url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
            return data.get("response")
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, Exception) as exc:
            self.last_error = str(exc)
            return None
