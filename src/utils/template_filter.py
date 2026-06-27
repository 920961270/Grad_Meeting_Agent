"""Helpers for filtering empty input templates and placeholders."""

from __future__ import annotations

import re


PLACEHOLDER_PHRASES = [
    "请在这里填写",
    "关注点：",
    "方法启发：",
    "和当前实验关系：",
    "疑问：",
    "本周完成",
    "实验观察",
    "组会提醒",
    "老师反馈",
    "其他想法",
    "实验结果",
    "当前问题",
    "下周计划",
    "补充阅读笔记",
    "你对 PDF 文献",
    "本文档只作为补充说明",
    "不应被当成独立论文条目",
    "如果 input/papers/",
    "论文 1",
    "论文 2",
]


def is_placeholder_line(line: str) -> bool:
    """Return True when a line is an empty template placeholder."""
    stripped = line.strip()
    if not stripped:
        return True
    if re.fullmatch(r"[-*+]\s*", stripped):
        return True
    if re.fullmatch(r"#{1,6}\s*.+", stripped):
        title = re.sub(r"^#{1,6}\s*", "", stripped)
        return any(phrase in title for phrase in PLACEHOLDER_PHRASES)
    content = re.sub(r"^[-*+]\s*", "", stripped).strip()
    if re.fullmatch(r"[\w\u4e00-\u9fff\s]+[:：]\s*", content):
        return True
    return any(phrase in content for phrase in PLACEHOLDER_PHRASES)


def remove_placeholder_lines(text: str) -> str:
    """Remove placeholder lines while preserving user-authored content."""
    lines = [line for line in text.splitlines() if not is_placeholder_line(line)]
    return "\n".join(lines).strip()


def has_meaningful_content(text: str) -> bool:
    """Return True when text contains non-placeholder content."""
    cleaned = remove_placeholder_lines(text)
    meaningful = re.sub(r"[\s#\-*+_:：，。,.；;、()（）\[\]]", "", cleaned)
    return len(meaningful) >= 8
