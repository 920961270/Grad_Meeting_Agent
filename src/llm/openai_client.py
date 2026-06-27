"""OpenAI backend client."""

from __future__ import annotations

import os


class OpenAIClient:
    """Small wrapper around the OpenAI Responses API."""

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.model = model
        self.last_error: str | None = None

    def generate(self, prompt: str) -> str | None:
        """Generate text using OpenAI, returning None on any failure."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            self.last_error = "OPENAI_API_KEY is not set"
            return None
        try:
            from openai import OpenAI  # type: ignore

            client = OpenAI(api_key=api_key)
            response = client.responses.create(model=self.model, input=prompt)
            return response.output_text
        except Exception as exc:
            self.last_error = str(exc)
            return None
