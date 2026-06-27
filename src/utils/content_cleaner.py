"""Content cleaning helpers for report and slide generation."""

from __future__ import annotations

import re


def remove_markdown_headers_inside_bullets(text: str) -> str:
    """Remove accidental Markdown headings embedded in bullet items."""
    cleaned_lines: list[str] = []
    for line in text.splitlines():
        cleaned = re.sub(r"^(\s*[-*]\s+)#{1,6}\s*", r"\1", line)
        cleaned_lines.append(cleaned)
    return "\n".join(cleaned_lines)


def remove_pdf_artifacts(text: str) -> str:
    """Remove common PDF extraction artifacts such as page markers and page numbers."""
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if re.fullmatch(r"\[?\s*Page\s+\d+\s*\]?", stripped, flags=re.IGNORECASE):
            continue
        if re.fullmatch(r"\d{1,3}", stripped):
            continue
        if re.fullmatch(r"[-_=\s]{3,}", stripped):
            continue
        stripped = re.sub(r"\[?\s*Page\s+\d+\s*\]?", "", stripped, flags=re.IGNORECASE).strip()
        if stripped:
            lines.append(stripped)
    return "\n".join(lines)


def remove_incomplete_english_fragments(text: str) -> str:
    """Drop likely OCR/PDF English fragments that are not useful report evidence."""
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        ascii_chars = sum(1 for char in stripped if ord(char) < 128)
        ascii_ratio = ascii_chars / max(len(stripped), 1)
        word_count = len(re.findall(r"[A-Za-z]+", stripped))
        has_cjk = bool(re.search(r"[\u4e00-\u9fff]", stripped))
        ends_cleanly = stripped.endswith((".", "。", "！", "？", ":", "：", ")", "）"))
        starts_lower = bool(re.match(r"^[a-z]", stripped))
        looks_metric = bool(re.search(r"\b(PSNR|SSIM|Recall|Continuity|mAP|IoU|API|LLM)\b", stripped))
        if not has_cjk and ascii_ratio > 0.85 and word_count >= 6 and (starts_lower or not ends_cleanly) and not looks_metric:
            continue
        lines.append(stripped)
    return "\n".join(lines)


def normalize_bullets(text: str) -> str:
    """Normalize bullet markers to '- ' while preserving non-list lines."""
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        bullet = re.match(r"^(\d+[.)]|[-*+])\s+(.+)$", stripped)
        if bullet:
            lines.append(f"- {bullet.group(2).strip()}")
        else:
            lines.append(stripped)
    return "\n".join(lines)


def deduplicate_bullets(items: list[str]) -> list[str]:
    """Remove duplicate bullet items while preserving order."""
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = re.sub(r"\W+", "", item).lower()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def filter_empty_or_too_short_items(items: list[str], min_chars: int = 6) -> list[str]:
    """Drop empty, noisy, or too-short list items."""
    result: list[str] = []
    for item in items:
        cleaned = clean_text(item).strip("-# \t")
        meaningful = re.sub(r"[\s,.;:，。；：、()\[\]（）]", "", cleaned)
        if len(meaningful) < min_chars:
            continue
        if re.fullmatch(r"#+\s*.+", cleaned):
            continue
        result.append(cleaned)
    return result


def clean_text(text: str) -> str:
    """Apply all text-level cleanup passes."""
    text = remove_pdf_artifacts(text)
    text = remove_incomplete_english_fragments(text)
    text = remove_markdown_headers_inside_bullets(text)
    text = normalize_bullets(text)
    return text.strip()


def clean_items(items: list[str], limit: int | None = None, min_chars: int = 6) -> list[str]:
    """Clean, filter, and deduplicate list items."""
    cleaned = filter_empty_or_too_short_items(items, min_chars=min_chars)
    deduped = deduplicate_bullets(cleaned)
    return deduped[:limit] if limit else deduped
