"""Markdown report composition."""

from __future__ import annotations

import re

from src.agent.state import AgentState
from src.utils.content_cleaner import clean_items, clean_text
from src.utils.markdown_utils import bullet_list


class Reporter:
    """Create user-facing meeting materials from structured sections."""

    INTERNAL_PATTERNS = [
        r"检测到\s*\d+\s*篇\s*PDF",
        r"空模板",
        r"占位内容已过滤",
        r"progress\.md\s*为空",
        r"agent_state\.json\s*记录",
        r"use_paper_notes_as_sources",
        r"source_type",
        r"本工具",
        r"本\s*Agent",
        r"运行命令",
    ]

    def build_meeting_pack(self, state: AgentState) -> str:
        """Return the default single-file meeting pack."""
        sections = state.report_sections
        return clean_text(self._meeting_pack(sections)) + "\n"

    def build_detail_documents(self, state: AgentState) -> dict[str, str]:
        """Return optional detailed Markdown documents."""
        sections = state.report_sections
        return {
            "research_brief.md": clean_text(self._research_brief(sections)),
            "paper_cards.md": clean_text(self._paper_cards_doc(sections)),
            "experiment_insights.md": clean_text(self._experiment_insights_doc(sections)),
            "meeting_agenda.md": clean_text(self._meeting_agenda_doc(sections)),
            "weekly_report.md": clean_text(self._weekly_report(sections)),
            "oral_script.md": clean_text(self._oral_script(sections)),
            "supervisor_qa.md": clean_text(self._supervisor_qa(sections)),
            "next_week_plan.md": clean_text(self._next_week_plan(sections)),
        }

    def build_ppt_outline(self, state: AgentState) -> str:
        """Return the optional slide outline."""
        return clean_text(self._ppt_outline(state.report_sections)) + "\n"

    def build_documents(self, state: AgentState) -> dict[str, str]:
        """Backward-compatible detail export."""
        return self.build_detail_documents(state)

    def _meeting_pack(self, sections: dict[str, object]) -> str:
        return "\n\n".join(
            [
                "# Research Meeting Pack",
                "## 1. 一页概览\n" + bullet_list(self._one_page_overview(sections)),
                "## 2. 本周可以汇报什么\n" + bullet_list(self._work_items(sections, limit=6)),
                "## 3. 文献卡片\n" + self._paper_cards_block(sections),
                "## 4. 实验结果洞察\n" + self._experiment_insights_body(sections),
                "## 5. 图像与结果材料\n" + self._figure_materials_block(sections),
                "## 6. 当前问题与风险\n" + bullet_list(self._risks(sections)),
                "## 7. 建议 PPT 结构\n" + bullet_list(self._suggested_ppt_structure()),
                "## 8. 组会讨论问题\n" + bullet_list(self._discussion_items(sections)),
                "## 9. 个人准备：导师可能追问\n" + self._supervisor_qa_body(sections, limit=8),
            ]
        )

    def _research_brief(self, sections: dict[str, object]) -> str:
        return "\n\n".join(
            [
                "# Research Meeting Brief",
                "## 1. 本周材料概览\n" + bullet_list(self._material_items(sections)),
                "## 2. 自动推断的本周工作\n" + bullet_list(self._work_items(sections, limit=6)),
                "## 3. 文献关键信息\n" + self._paper_cards_block(sections),
                "## 4. 实验结果洞察\n" + self._experiment_insights_body(sections),
                "## 5. 当前证据链\n" + bullet_list(self._evidence_items(sections)),
                "## 6. 缺口与风险\n" + bullet_list(self._risks(sections)),
                "## 7. 组会建议讨论点\n" + bullet_list(self._discussion_items(sections)),
                "## 8. 下一步行动\n" + self._next_week_plan_body(sections),
            ]
        ) + "\n"

    def _paper_cards_doc(self, sections: dict[str, object]) -> str:
        return "# Paper Cards\n\n" + self._paper_cards_block(sections) + "\n"

    def _experiment_insights_doc(self, sections: dict[str, object]) -> str:
        return "# Experiment Insights\n\n" + self._experiment_insights_body(sections) + "\n"

    def _meeting_agenda_doc(self, sections: dict[str, object]) -> str:
        agenda = [
            "先用 1 分钟说明本周研究主线和可展示证据。",
            "再汇报文献 takeaways，强调和当前实验的关系。",
            "随后展示实验结果，突出指标变化、代表性结果和失败风险。",
            "最后讨论下一步行动和需要导师判断的问题。",
        ]
        private_items = [
            "导师可能追问和回答思路只作为个人准备，不放入展示 PPT。",
            "未验证猜测、工具配置和执行日志不进入正式汇报。",
        ]
        return "\n\n".join(
            [
                "# Meeting Agenda",
                "## 先汇报什么\n" + bullet_list(agenda),
                "## 哪些结果值得展示\n" + bullet_list(self._display_worthy_results(sections)),
                "## 哪些问题需要请导师判断\n" + bullet_list(self._discussion_items(sections)),
                "## 哪些内容只适合自己准备\n" + bullet_list(private_items),
                "## 会后行动建议\n" + bullet_list(self._plan(sections)["must"][:3]),
            ]
        ) + "\n"

    def _weekly_report(self, sections: dict[str, object]) -> str:
        return "\n\n".join(
            [
                "# 本周组会汇报",
                "## 1. 本周工作概览\n" + bullet_list(self._work_items(sections, limit=5)),
                "## 2. 文献阅读总结\n" + self._paper_cards_block(sections),
                "## 3. 实验/项目进展\n" + bullet_list(self._display_worthy_results(sections)),
                "## 4. 当前问题与分析\n" + self._analysis_block(sections),
                "## 5. 下周计划\n" + self._next_week_plan_body(sections),
                "## 6. 需要导师建议的问题\n" + bullet_list(self._discussion_items(sections)),
            ]
        ) + "\n"

    def _ppt_outline(self, sections: dict[str, object]) -> str:
        cards = self._list_dicts(sections, "paper_cards")
        metrics = self._list_dicts(sections, "metric_cards")
        analysis = self._list_dicts(sections, "analysis_cards")
        plan = self._plan(sections)

        slides = [
            ("Title", ["本周组会汇报", "研究背景、实验结果与下一步验证"]),
            ("Research Context", self._work_items(sections, limit=5)),
            (
                "Paper Takeaways",
                [
                    f"{card.get('paper')}：方法关键词：{card.get('method')}；启发：{card.get('insight')}"
                    for card in cards[:3]
                ],
            ),
            ("Experiment Evidence", [str(card.get("summary")) for card in metrics[:4]] or self._display_worthy_results(sections)),
            (
                "Key Insights",
                [
                    f"发现：{card.get('finding')}；解释：{card.get('explanation')}；证据：{card.get('evidence')}"
                    for card in analysis[:3]
                ],
            ),
            ("Issues & Risks", self._risks(sections)),
            (
                "Next Actions",
                [f"Must：{item}" for item in plan["must"][:2]]
                + [f"Should：{item}" for item in plan["should"][:2]]
                + [f"Could：{item}" for item in plan["could"][:1]],
            ),
            ("Discussion", self._discussion_items(sections)),
        ]

        parts = ["# 组会 PPT 大纲"]
        for index, (title, bullets) in enumerate(slides, start=1):
            safe_bullets = self._visible_items([str(item) for item in bullets], limit=8)
            if index != 1:
                safe_bullets = self._pad_slide_bullets(title, safe_bullets)
            parts.append(f"## Slide {index}: {title}\n" + bullet_list(safe_bullets))
        return "\n\n".join(parts) + "\n"

    def _oral_script(self, sections: dict[str, object]) -> str:
        overview = "；".join(self._work_items(sections, limit=3))
        experiments = "；".join(self._display_worthy_results(sections)[:4])
        issues = "；".join(self._risks(sections)[:3])
        must = "；".join(self._plan(sections)["must"][:2])
        return "\n\n".join(
            [
                "# 3-5 分钟口头汇报稿",
                "老师好，我本周汇报的主题是视频增强与下游评估的阶段性进展。",
                f"第一部分是本周可以汇报的工作：{overview}。",
                "第二部分是文献阅读，我会重点说明研究问题、方法关键词以及对当前课题的启发。",
                f"第三部分是实验结果：{experiments}。",
                f"目前主要风险是：{issues}。",
                f"下周我会优先完成：{must}。",
                "以上是本周汇报，想请老师重点建议实验优先级、指标体系和失败案例展示方式。",
            ]
        ) + "\n"

    def _supervisor_qa(self, sections: dict[str, object]) -> str:
        return "# 导师可能追问清单\n\n" + self._supervisor_qa_body(sections, limit=8) + "\n"

    def _supervisor_qa_body(self, sections: dict[str, object], limit: int = 8) -> str:
        parts: list[str] = []
        for index, (question, answer) in enumerate(self._questions(sections)[:limit], start=1):
            parts.append(f"### Q{index}: {self._strip_internal(question)}\n建议回答方向：{self._strip_internal(answer)}")
        return "\n\n".join(parts)

    def _next_week_plan(self, sections: dict[str, object]) -> str:
        return "# 下周计划\n\n" + self._next_week_plan_body(sections) + "\n"

    def _next_week_plan_body(self, sections: dict[str, object]) -> str:
        plan = self._plan(sections)
        return "\n\n".join(
            [
                "### Must do\n" + bullet_list(plan["must"]),
                "### Should do\n" + bullet_list(plan["should"]),
                "### Could do\n" + bullet_list(plan["could"]),
            ]
        )

    def _one_page_overview(self, sections: dict[str, object]) -> list[str]:
        items: list[str] = []
        papers = self._list_dicts(sections, "paper_cards")
        metrics = self._list_dicts(sections, "metric_cards")
        figures = self._list_dicts(sections, "figure_items")
        if papers:
            names = "、".join(str(card.get("paper")) for card in papers[:3])
            items.append(f"文献方面：围绕 {names} 梳理了研究问题、方法关键词和可借鉴点。")
        if metrics:
            metric_names = "、".join(str(card.get("name")) for card in metrics[:4])
            items.append(f"实验方面：已有 {metric_names} 等 before/after 指标，可用于说明结果变化。")
            items.append(self._metric_direction(metrics))
        else:
            items.append("实验方面：当前更适合展示阶段性现象、代表性样例和下一轮验证设计。")
        if figures:
            items.append("图像方面：已有图像材料可辅助说明代表性结果、对比效果或失败案例。")
        else:
            items.append("展示方面：建议补充 before/after 对比图和失败案例图，增强汇报说服力。")
        items.extend(self._risks(sections)[:2])
        items.extend(self._discussion_items(sections)[:1])
        return self._visible_items(items, limit=8)

    def _work_items(self, sections: dict[str, object], limit: int = 6) -> list[str]:
        items = self._visible_items(self._list(sections, "inferred_work_items"), limit=limit)
        if not items:
            items = [
                "当前证据显示，本周材料更适合汇报为文献背景、实验观察和下一步验证计划。",
                "组会主线可以围绕研究问题、指标变化和风险补强展开。",
            ]
        return self._visible_items(items, limit=limit)

    def _paper_cards_block(self, sections: dict[str, object]) -> str:
        cards = self._list_dicts(sections, "paper_cards")
        if not cards:
            return "当前文献证据较少，建议后续补充 1-2 篇与当前实验最相关的论文。"
        parts: list[str] = []
        for index, card in enumerate(cards, start=1):
            title = self._strip_internal(str(card.get("paper", f"文献 {index}")))
            method = self._strip_internal(str(card.get("method", "")))
            insight = self._strip_internal(str(card.get("insight", "")))
            limitation = self._strip_internal(str(card.get("limitation", "")))
            problem = self._strip_internal(str(card.get("problem", "")))
            parts.append(
                "\n".join(
                    [
                        f"### 文献 {index}: {title}",
                        f"- 研究问题：{problem}",
                        f"- 方法关键词：{method}",
                        f"- 对当前课题的启发：{insight}",
                        "- 组会上可以怎么讲：先说明论文解决的问题，再讲方法关键词，最后落到当前实验可验证的假设。",
                        f"- 仍需确认的点：{limitation}",
                    ]
                )
            )
        return "\n\n".join(parts)

    def _experiment_insights_body(self, sections: dict[str, object]) -> str:
        metrics = self._list_dicts(sections, "metric_cards")
        metric_lines = [str(card.get("summary")) for card in metrics]
        if not metric_lines:
            metric_lines = ["当前证据显示，数值结果还不足以支撑强结论，适合结合代表性样例做保守汇报。"]

        return "\n\n".join(
            [
                "### 有哪些指标或结果\n" + bullet_list(self._visible_items(metric_lines, limit=6)),
                "### 哪些结果值得展示\n" + bullet_list(self._display_worthy_results(sections)),
                "### 可能说明什么\n" + bullet_list(self._analysis_summaries(sections)),
                "### 有哪些风险\n" + bullet_list(self._risks(sections)),
            ]
        )

    def _figure_materials_block(self, sections: dict[str, object]) -> str:
        figures = self._list_dicts(sections, "figure_items")
        if not figures:
            return "建议补充一张增强前后对比图和一张失败案例图，便于把指标变化讲清楚。"
        lines = []
        for item in figures:
            filename = str(item.get("file", "figure"))
            lines.append(f"- {filename}：建议用途：{self._figure_use_label(item)}")
        return "\n".join(lines)

    def _display_worthy_results(self, sections: dict[str, object]) -> list[str]:
        metrics = self._list_dicts(sections, "metric_cards")
        items = [str(card.get("summary")) for card in metrics if card.get("summary")]
        if metrics:
            items.append("可以优先展示同向提升的指标，再用失败案例解释仍未解决的问题。")
        figures = self._list_dicts(sections, "figure_items")
        if figures:
            items.append("图像材料适合用于补充代表性结果、对比图或失败场景。")
        if not items:
            items.append("当前更适合展示代表性现象和下一轮验证计划，避免过度解读单次结果。")
        return self._visible_items(items, limit=6)

    def _analysis_summaries(self, sections: dict[str, object]) -> list[str]:
        cards = self._list_dicts(sections, "analysis_cards")
        items = [
            f"{card.get('finding')} {card.get('explanation')} 证据：{card.get('evidence')}"
            for card in cards[:3]
        ]
        return self._visible_items(items, limit=4)

    def _analysis_block(self, sections: dict[str, object]) -> str:
        cards = self._list_dicts(sections, "analysis_cards")
        parts: list[str] = []
        for card in cards:
            finding = self._strip_internal(str(card.get("finding", "")))
            explanation = self._strip_internal(str(card.get("explanation", "")))
            evidence = self._strip_internal(str(card.get("evidence", "")))
            parts.append(
                "\n".join(
                    [
                        f"### {finding}",
                        f"- 现象：{finding}",
                        f"- 可能原因：{explanation}",
                        f"- 下一步验证：结合实验配置、失败案例和指标变化继续验证。证据：{evidence}",
                    ]
                )
            )
        risks = self._risks(sections)
        if risks:
            parts.append("### 当前风险\n" + bullet_list(risks))
        return "\n\n".join(parts)

    def _material_items(self, sections: dict[str, object]) -> list[str]:
        return self._visible_items(self._list(sections, "material_overview"), limit=8)

    def _evidence_items(self, sections: dict[str, object]) -> list[str]:
        return self._visible_items(self._list(sections, "evidence_chain_items"), limit=6)

    def _risks(self, sections: dict[str, object]) -> list[str]:
        fallback = [
            "文献方法与当前实验的对应关系仍需确认。",
            "指标结果是否稳定仍需更多场景验证。",
            "缺少失败案例可视化会影响汇报说服力。",
        ]
        risks = self._visible_items(self._list(sections, "issue_items"), limit=5)
        for item in fallback:
            if len(risks) >= 3:
                break
            risks.append(item)
        return self._visible_items(risks, limit=5)

    def _discussion_items(self, sections: dict[str, object]) -> list[str]:
        fallback = [
            "下周是否优先补充低光照和运动模糊场景？",
            "是否建议将检测连续性作为核心汇报指标之一？",
            "是否需要增加失败案例可视化来支撑指标解释？",
        ]
        items = self._visible_items(self._list(sections, "discussion_items"), limit=5)
        for item in fallback:
            if len(items) >= 3:
                break
            items.append(item)
        return self._visible_items(items, limit=5)

    def _suggested_ppt_structure(self) -> list[str]:
        return [
            "Title：本周组会汇报、日期和主题。",
            "Research Context：研究问题、本周材料和汇报主线。",
            "Paper Takeaways：文献方法关键词、启发和局限。",
            "Experiment Evidence：核心指标、代表性结果和 before/after 证据。",
            "Key Insights：发现、解释和支撑证据。",
            "Issues & Risks：当前问题、稳定性风险和失败案例需求。",
            "Next Actions：下周优先实验、文献核对和图像材料补充。",
            "Discussion：需要导师判断的 3-5 个问题。",
        ]

    def _metric_direction(self, metrics: list[dict[str, object]]) -> str:
        positives = []
        for card in metrics:
            try:
                delta = float(card.get("delta", 0))
            except (TypeError, ValueError):
                continue
            if delta > 0:
                positives.append(str(card.get("name", "Metric")))
        if positives:
            return f"指标变化方面：{', '.join(positives)} 呈现提升趋势，但稳定性仍需更多场景验证。"
        return "指标变化方面：当前结果需要结合更多场景判断是否稳定。"

    def _metric_strength_lines(self, metrics: list[dict[str, object]]) -> list[str]:
        lines: list[str] = []
        for card in metrics:
            try:
                delta = float(card.get("delta", 0))
            except (TypeError, ValueError):
                continue
            label = str(card.get("name", "Metric"))
            if abs(delta) >= 1:
                strength = "提升幅度较明显"
            elif abs(delta) >= 0.03:
                strength = "有可见提升"
            else:
                strength = "提升较小，需要更多场景验证"
            lines.append(f"{label}: {strength}（delta={delta:.3f}）。")
        return lines or ["当前缺少可计算 before/after 的指标，提升幅度保持保守判断。"]

    def _figure_use_label(self, item: dict[str, object]) -> str:
        figure_type = str(item.get("type", "supporting_figure"))
        labels = {
            "before_after_or_comparison": "before-after 对比",
            "failure_case": "失败案例",
            "metric_chart": "结果展示",
            "result_example": "结果展示",
            "supporting_figure": "补充材料",
        }
        return labels.get(figure_type, "补充材料")

    def _pad_slide_bullets(self, title: str, bullets: list[str]) -> list[str]:
        fallbacks = {
            "Paper Takeaways": [
                "文献展示重点放在研究问题、方法关键词、可借鉴点和仍需确认的限制。",
                "每篇论文尽量对应一个当前实验可验证的假设。",
            ],
            "Experiment Evidence": [
                "优先展示 before/after 指标或代表性结果。",
                "若指标不足，可用结果图和失败案例解释实验现象。",
                "实验结论需要同时关注图像质量和下游任务表现。",
            ],
            "Issues & Risks": [
                "文献方法与当前实验的对应关系仍需确认。",
                "指标结果是否稳定仍需更多场景验证。",
                "缺少失败案例可视化会影响汇报说服力。",
            ],
            "Discussion": [
                "下周是否优先补充低光照和运动模糊场景？",
                "是否建议将检测连续性作为核心汇报指标之一？",
                "是否需要增加失败案例可视化来支撑指标解释？",
            ],
        }
        padded = list(bullets)
        for item in fallbacks.get(title, ["当前页面结论保持证据优先和保守表达。"]):
            if len(padded) >= 3:
                break
            padded.append(item)
        return self._visible_items(padded, limit=8)

    def _list(self, sections: dict[str, object], key: str, limit: int | None = None) -> list[str]:
        values = sections.get(key, [])
        if not isinstance(values, list):
            return []
        return clean_items([str(item) for item in values], limit=limit)

    def _list_dicts(self, sections: dict[str, object], key: str) -> list[dict[str, object]]:
        values = sections.get(key, [])
        return [item for item in values if isinstance(item, dict)] if isinstance(values, list) else []

    def _plan(self, sections: dict[str, object]) -> dict[str, list[str]]:
        plan = sections.get("prioritized_plan", {})
        if not isinstance(plan, dict):
            plan = {}
        return {
            "must": self._visible_items([str(item) for item in plan.get("must", [])], limit=5),
            "should": self._visible_items([str(item) for item in plan.get("should", [])], limit=5),
            "could": self._visible_items([str(item) for item in plan.get("could", [])], limit=5),
        }

    def _questions(self, sections: dict[str, object]) -> list[tuple[str, str]]:
        raw = sections.get("questions", [])
        questions: list[tuple[str, str]] = []
        if isinstance(raw, list):
            for item in raw:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    questions.append((str(item[0]), str(item[1])))
        return questions

    def _visible_items(self, items: list[str], limit: int | None = None) -> list[str]:
        visible: list[str] = []
        for item in items:
            cleaned = self._strip_internal(str(item))
            if cleaned:
                visible.append(cleaned)
        return clean_items(visible, limit=limit)

    def _strip_internal(self, text: str) -> str:
        cleaned = str(text).strip()
        for pattern in self.INTERNAL_PATTERNS:
            if re.search(pattern, cleaned, flags=re.IGNORECASE):
                return ""
        cleaned = re.sub(r"（source_type:.*?）", "", cleaned)
        cleaned = cleaned.replace("source_type:", "")
        return cleaned.strip()
