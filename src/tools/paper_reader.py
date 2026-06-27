"""Readers for Markdown reading notes and PDF papers."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from src.utils.content_cleaner import clean_text
from src.utils.file_utils import read_text_if_exists
from src.utils.template_filter import has_meaningful_content, remove_placeholder_lines


class PaperReader:
    """Read paper_notes.md and input/papers/*.pdf with explicit source priority."""

    def __init__(
        self,
        input_dir: Path,
        paper_source_mode: str = "pdf_first",
        use_paper_notes_as_sources: bool = False,
    ) -> None:
        self.input_dir = input_dir
        self.paper_source_mode = paper_source_mode
        self.use_paper_notes_as_sources = use_paper_notes_as_sources

    def read(self) -> dict[str, object]:
        """Return structured paper entries, supplementary notes, and warnings."""
        raw_notes = read_text_if_exists(self.input_dir / "paper_notes.md")
        cleaned_notes = remove_placeholder_lines(raw_notes)
        note_has_content = has_meaningful_content(raw_notes)

        pdf_entries, pdf_files, warnings = self._read_pdf_entries()
        has_pdf = bool(pdf_files)
        summaries: list[dict[str, object]] = []

        if self.paper_source_mode == "pdf_first" and has_pdf:
            summaries.extend(pdf_entries)
            if self.use_paper_notes_as_sources and note_has_content:
                summaries.extend(self._note_entries(cleaned_notes))
            supplementary_notes = cleaned_notes if note_has_content and not self.use_paper_notes_as_sources else ""
        else:
            if has_pdf:
                summaries.extend(pdf_entries)
            if note_has_content:
                summaries.extend(self._note_entries(cleaned_notes))
            supplementary_notes = ""

        return {
            "raw": raw_notes,
            "summaries": summaries,
            "supplementary_notes": supplementary_notes,
            "pdf_files": pdf_files,
            "detected_pdf": bool(pdf_files),
            "paper_source_mode": self.paper_source_mode,
            "use_paper_notes_as_sources": self.use_paper_notes_as_sources,
            "warnings": warnings,
        }

    def _note_entries(self, cleaned_notes: str) -> list[dict[str, object]]:
        """Split meaningful reading notes into note source entries."""
        entries: list[dict[str, object]] = []
        for index, section in enumerate(self._split_sections(cleaned_notes), start=1):
            title = self._section_title(section, fallback=f"阅读笔记 {index}")
            body = "\n".join(line for line in section.splitlines() if not line.startswith("#"))
            body = remove_placeholder_lines(clean_text(body))
            if not has_meaningful_content(body):
                continue
            entries.append(
                {
                    "source_type": "note",
                    "title": title,
                    "content": body,
                }
            )
        return entries

    def _read_pdf_entries(self) -> tuple[list[dict[str, object]], list[str], list[str]]:
        """Extract text from PDF files under input/papers."""
        papers_dir = self.input_dir / "papers"
        if not papers_dir.exists():
            return [], [], []

        entries: list[dict[str, object]] = []
        files: list[str] = []
        warnings: list[str] = []

        for pdf_path in sorted(papers_dir.glob("*.pdf")):
            files.append(pdf_path.name)
            try:
                text = self._extract_pdf_text(pdf_path)
            except Exception as exc:
                warnings.append(f"Failed to parse PDF {pdf_path.name}: {exc}")
                continue

            cleaned = clean_text(self._compact_pdf_text(text))
            if not cleaned:
                warnings.append(f"PDF {pdf_path.name} did not contain extractable text.")
                continue
            entries.append(
                {
                    "source_type": "pdf",
                    "title": pdf_path.name,
                    "content": cleaned,
                }
            )

        return entries, files, warnings

    def _split_sections(self, raw: str) -> list[str]:
        """Split Markdown notes by headings."""
        if not raw.strip():
            return []
        sections: list[str] = []
        current: list[str] = []
        for line in raw.splitlines():
            if line.startswith("#") and current:
                sections.append("\n".join(current).strip())
                current = [line]
            else:
                current.append(line)
        if current:
            sections.append("\n".join(current).strip())
        return [section for section in sections if section]

    def _section_title(self, section: str, fallback: str) -> str:
        """Return the first Markdown heading in a section."""
        for line in section.splitlines():
            if line.startswith("#"):
                return line.strip("# ").strip() or fallback
        return fallback

    def _extract_pdf_text(self, pdf_path: Path) -> str:
        """Extract PDF text using pypdf, falling back to PyMuPDF when available."""
        extractors: list[Callable[[Path], str]] = [self._extract_with_pypdf, self._extract_with_pymupdf]
        errors: list[str] = []
        for extractor in extractors:
            try:
                return extractor(pdf_path)
            except Exception as exc:
                errors.append(f"{extractor.__name__}: {exc}")
        raise RuntimeError("; ".join(errors) or "No PDF extractor is available.")

    def _extract_with_pypdf(self, pdf_path: Path) -> str:
        """Extract text from a PDF with pypdf."""
        try:
            from pypdf import PdfReader  # type: ignore
        except ImportError as exc:
            raise ImportError("pypdf is not installed") from exc

        reader = PdfReader(str(pdf_path))
        pages: list[str] = []
        for index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(f"[Page {index}]\n{text.strip()}")
        return "\n\n".join(pages)

    def _extract_with_pymupdf(self, pdf_path: Path) -> str:
        """Extract text from a PDF with PyMuPDF."""
        try:
            import fitz  # type: ignore
        except ImportError as exc:
            raise ImportError("PyMuPDF is not installed") from exc

        pages: list[str] = []
        with fitz.open(str(pdf_path)) as document:
            for index, page in enumerate(document, start=1):
                text = page.get_text("text") or ""
                if text.strip():
                    pages.append(f"[Page {index}]\n{text.strip()}")
        return "\n\n".join(pages)

    def _compact_pdf_text(self, text: str, max_chars: int = 6000) -> str:
        """Normalize and cap extracted PDF text for prompt-safe summaries."""
        lines = [" ".join(line.split()) for line in text.splitlines()]
        cleaned = "\n".join(line for line in lines if line)
        return cleaned[:max_chars]
