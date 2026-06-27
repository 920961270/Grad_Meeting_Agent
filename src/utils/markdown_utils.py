"""Markdown formatting helpers."""

from __future__ import annotations


def bullet_list(items: object) -> str:
    """Format a sequence as a Markdown bullet list."""
    if isinstance(items, str):
        values = [line.strip("- ").strip() for line in items.splitlines() if line.strip()]
    else:
        values = [str(item).strip() for item in items if str(item).strip()]  # type: ignore[arg-type]
    if not values:
        return "- 暂无明确记录。"
    return "\n".join(f"- {item}" for item in values)


def compact_lines(text: str, limit: int = 5) -> list[str]:
    """Extract readable non-heading lines from Markdown text."""
    lines: list[str] = []
    for line in text.splitlines():
        cleaned = line.strip()
        if not cleaned or cleaned.startswith("#"):
            continue
        cleaned = cleaned.strip("-* ")
        if cleaned:
            lines.append(cleaned)
        if len(lines) >= limit:
            break
    return lines
