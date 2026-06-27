"""Fallback-safe summarization utilities."""

from __future__ import annotations

import json
import re
from typing import Any

from src.agent.state import AgentState
from src.llm.base import LLMClient
from src.utils.content_cleaner import clean_items, clean_text
from src.utils.markdown_utils import bullet_list
from src.utils.template_filter import remove_placeholder_lines


class Summarizer:
    """Create structured, meeting-ready report sections."""

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm_client = llm_client

    def summarize(self, state: AgentState) -> dict[str, object]:
        """Build structured sections used by both Markdown and PPTX outputs."""
        overview_items = self._overview_items(state)
        paper_cards = self._paper_cards(state)
        metric_cards = self._metric_cards(state)
        figure_items = self._figure_items(state)
        material_overview = self._material_overview(state, figure_items)
        inferred_work_items = self._inferred_work_items(state, paper_cards, metric_cards, figure_items)
        experiment_items = self._experiment_items(state, metric_cards)
        analysis_cards = self._analysis_cards(state, metric_cards)
        issue_items = self._issue_items(state)
        evidence_chain_items = self._evidence_chain_items(state, paper_cards, metric_cards, figure_items)
        plan = self._prioritized_plan(state)
        questions = self._questions(metric_cards)
        discussion_items = self._discussion_items()

        return {
            "topic": "Research Meeting Evidence Pack",
            "material_overview": material_overview,
            "overview_items": overview_items,
            "inferred_work_items": inferred_work_items,
            "paper_cards": paper_cards,
            "supplementary_notes": state.supplementary_notes,
            "metric_cards": metric_cards,
            "experiment_items": experiment_items,
            "figure_items": figure_items,
            "analysis_cards": analysis_cards,
            "evidence_chain_items": evidence_chain_items,
            "issue_items": issue_items,
            "discussion_items": discussion_items,
            "prioritized_plan": plan,
            "questions": questions,
            "overview": bullet_list(overview_items),
            "papers": self._render_paper_cards(paper_cards, state.supplementary_notes),
            "experiments": bullet_list(experiment_items),
            "problems": self._render_analysis_cards(analysis_cards, issue_items),
            "next_plan": self._render_plan(plan),
            "mentor_help": bullet_list(discussion_items),
        }

    def _overview_items(self, state: AgentState) -> list[str]:
        """Extract 3-5 completed work items from progress notes."""
        progress_text = state.research_context.get("progress", state.progress_summary)
        raw_items = self._bullet_items(self._remove_next_plan_sections(progress_text))
        completed = [
            item
            for item in raw_items
            if not re.search(r"下周|计划|next|todo", item, flags=re.IGNORECASE)
        ]
        if state.git_summary.get("commits"):
            completed.append(f"纳入最近 {len(state.git_summary.get('commits', []))} 条 git 提交作为进展证据。")

        if state.detected_pdf_papers:
            fallback = [
                "完成文献背景整理，重点关注视频增强、恢复质量和下游评估之间的关系。",
                "结合实验结果和文献材料，形成了本周可以汇报的研究线索。",
                "当前材料更适合围绕方法启发、指标变化和风险验证来组织组会汇报。",
            ]
        else:
            fallback = [
                "当前证据显示，本周材料可围绕实验结果、图像材料、notes 或代码记录展开。",
                "当前材料更适合先汇报阶段性观察，再说明后续需要补齐的验证。",
                "组会汇报可以聚焦已有证据、风险判断和下一步实验设计。",
            ]
        return clean_items(completed or fallback, limit=5)

    def _material_overview(self, state: AgentState, figure_items: list[dict[str, str]]) -> list[str]:
        """Summarize the input materials available for inference."""
        items: list[str] = []
        if state.detected_pdf_papers:
            items.append(f"PDF 文献：{', '.join(state.detected_pdf_papers)}。")
        experiment_files = state.experiment_summary.get("files", [])
        if experiment_files:
            items.append(f"实验结果文件：{', '.join(str(item) for item in experiment_files)}。")
        if figure_items:
            items.append(f"图像材料：{len(figure_items)} 个文件，可用于结果展示或失败案例说明。")
        if state.git_summary.get("commits"):
            items.append(f"代码记录：最近 {len(state.git_summary.get('commits', []))} 条提交。")
        notes = state.research_context.get("notes") or state.supplementary_notes
        if notes:
            items.append("零散 notes：已作为解释实验现象和组会讨论点的补充材料。")
        if not items:
            items.append("当前证据较少，适合将本次组会定位为研究计划和验证思路讨论。")
        return clean_items(items, limit=8)

    def _inferred_work_items(
        self,
        state: AgentState,
        paper_cards: list[dict[str, object]],
        metric_cards: list[dict[str, object]],
        figure_items: list[dict[str, str]],
    ) -> list[str]:
        """Infer weekly work from materials when progress.md is empty."""
        explicit = self._overview_items(state)
        if state.research_context.get("progress"):
            return explicit

        inferred: list[str] = []
        if state.detected_pdf_papers:
            inferred.append(f"围绕 {len(state.detected_pdf_papers)} 篇 PDF 文献整理研究问题、方法关键词和可借鉴点。")
        if metric_cards:
            inferred.append("整理实验指标的 before/after 变化，用于判断本轮实验收益。")
        elif state.experiment_summary.get("files"):
            inferred.append("整理结构化实验结果，为后续指标解释和失败案例分析建立基础。")
        if figure_items:
            inferred.append("整理实验图、对比图或失败案例截图，形成可用于组会展示的图像清单。")
        if state.git_summary.get("commits"):
            inferred.append("读取近期代码提交记录，作为工程进展证据。")
        if paper_cards:
            inferred.append("将文献启发、实验指标和展示材料组织成可用于组会讨论的证据链。")
        return clean_items(inferred or explicit, limit=6)

    def _paper_cards(self, state: AgentState) -> list[dict[str, object]]:
        """Convert PDF papers and optional note sources into structured cards."""
        cards: list[dict[str, object]] = []
        for index, entry in enumerate(state.paper_summaries, start=1):
            if not isinstance(entry, dict):
                continue
            source_type = str(entry.get("source_type", "note"))
            title = str(entry.get("title", f"文献 {index}"))
            content = remove_placeholder_lines(clean_text(str(entry.get("content", ""))))
            if not content:
                continue
            lines = [line.strip("-# ") for line in content.splitlines() if line.strip()]
            if source_type == "pdf":
                cards.append(self._pdf_card(title, content))
            else:
                cards.append(
                    {
                        "paper": title,
                        "source_type": "note",
                        "problem": self._first_match(lines, ["研究问题", "问题", "task"], "用户补充笔记关注当前论文与实验任务之间的关系。"),
                        "method": self._first_match(lines, ["核心方法", "方法", "method", "方法启发"], "补充笔记记录了可借鉴的方法线索。"),
                        "insight": self._first_match(lines, ["启发", "可借鉴", "关注点", "insight"], "可作为 PDF 文献理解的中文补充。"),
                        "limitation": self._first_match(lines, ["局限", "风险", "疑问", "limitation"], "仍需结合 PDF 原文进一步核对关键章节。"),
                    }
                )

        if not cards:
            cards.append(
                {
                    "paper": "本周文献输入",
                    "source_type": "none",
                    "problem": "当前材料中没有可解析的文献来源。",
                    "method": "本轮 evidence pack 将更多依赖实验结果、图像材料、notes 或 git 记录。",
                    "insight": "本次汇报可先以实验现象和后续验证计划为主。",
                    "limitation": "文献证据不足时，组会中应降低文献结论权重。",
                }
            )
        return cards[:4]

    def _pdf_card(self, title: str, content: str) -> dict[str, object]:
        """Create a conservative display-ready card for a PDF source."""
        lower = f"{title}\n{content}".lower()
        if "edvr" in lower or "deformable" in lower:
            method = "关注视频恢复中的特征对齐、多帧融合与重建模块，可用于理解增强模型如何利用时序信息。"
            insight = "可借鉴其对齐与融合思想，后续对比当前任务中的时序一致性和检测连续性。"
        else:
            method = "围绕视频增强、恢复或退化建模问题提供背景材料，可用于补充当前实验的方法脉络。"
            insight = "建议结合具体章节进一步梳理其对数据退化、重建质量或下游任务评价的启发。"
        return {
            "paper": title,
            "source_type": "pdf",
            "problem": "如何在退化或复杂视频场景中提升视觉质量，并进一步支撑下游任务评估。",
            "method": method,
            "insight": insight,
            "limitation": "关键结论仍需结合原文章节、实验设置和中文阅读笔记进一步核对。",
        }

    def _metric_cards(self, state: AgentState) -> list[dict[str, object]]:
        """Extract before/after metrics and compute deltas."""
        flattened = self._flatten_numbers(state.experiment_summary.get("metrics", {}))
        metric_specs = [
            ("PSNR", "psnr_before", "psnr_after", "dB"),
            ("SSIM", "ssim_before", "ssim_after", ""),
            ("Recall", "recall_before", "recall_after", ""),
            ("Continuity", "continuity_before", "continuity_after", ""),
        ]
        cards: list[dict[str, object]] = []
        for label, before_key, after_key, unit in metric_specs:
            before = self._find_metric(flattened, before_key)
            after = self._find_metric(flattened, after_key)
            if before is None or after is None:
                continue
            delta = after - before
            cards.append(
                {
                    "name": label,
                    "before": before,
                    "after": after,
                    "delta": delta,
                    "unit": unit,
                    "summary": f"{label}: {self._fmt(before)} -> {self._fmt(after)}，提升 {self._fmt(delta, signed=True)}{unit}",
                }
            )
        return cards

    def _experiment_items(self, state: AgentState, metric_cards: list[dict[str, object]]) -> list[str]:
        """Create experiment summary bullets with metric deltas."""
        summary = state.experiment_summary
        files = summary.get("files", [])
        items: list[str] = []
        if files:
            items.append("结构化实验结果可用于支撑本轮 before/after 指标对比。")
        for card in metric_cards:
            items.append(str(card["summary"]) + "。")
        tables = summary.get("tables", [])
        if isinstance(tables, list):
            for table in tables[:2]:
                items.append(
                    f"{table.get('file')} 包含 {table.get('row_count')} 条场景记录，可用于定位低光照、模糊等失败样例。"
                )
        if not items:
            items.append("当前缺少结构化实验指标，实验洞察将主要依赖图像、notes 或代码记录。")
        return clean_items(items, limit=8)

    def _analysis_cards(self, state: AgentState, metric_cards: list[dict[str, object]]) -> list[dict[str, str]]:
        """Build finding/explanation/evidence analysis cards."""
        evidence = "；".join(str(card["summary"]) for card in metric_cards[:2]) or "来自当前输入材料与文献背景。"
        if not metric_cards and state.detected_pdf_papers:
            evidence = "文献阅读材料可支撑研究背景，实验洞察可继续结合图像和表格材料细化。"
        return [
            {
                "finding": "已有材料可以支撑一次组会汇报。",
                "explanation": "PDF、实验结果、图像材料和代码记录分别提供背景、指标、案例和工程证据。",
                "evidence": evidence,
            },
            {
                "finding": "后续需要把文献启发落实到可验证实验。",
                "explanation": "组会材料应连接文献方法、实验配置、指标变化和失败案例。",
                "evidence": "文献卡片、实验洞察、图像清单和下周行动已分别生成。",
            },
            {
                "finding": "本周工作可以从多类材料交叉说明。",
                "explanation": "文献、实验表格、图像材料和代码记录可以分别支撑背景、结果、案例和实现进展。",
                "evidence": "文献卡片、指标变化、图像清单和下周行动可以构成完整汇报线索。",
            },
        ]

    def _issue_items(self, state: AgentState) -> list[str]:
        """Extract current issues and risks."""
        paper_text = "\n".join(
            str(entry.get("content", "")) for entry in state.paper_summaries if isinstance(entry, dict)
        )
        raw = "\n".join(
            [
                self._remove_next_plan_sections(state.progress_summary),
                paper_text,
                json.dumps(state.experiment_summary, ensure_ascii=False),
            ]
        )
        candidates = [
            line.strip("- *")
            for line in raw.splitlines()
            if re.search(r"问题|风险|不稳定|低光照|失败|伪影|误检|unstable|issue|risk", line, flags=re.IGNORECASE)
        ]
        fallback = [
            "文献启发和当前实验之间的对应关系仍需人工确认。",
            "指标提升是否具有统计稳定性仍需结合更多场景判断。",
            "图像材料若缺少失败案例，问题风险展示会偏保守。",
        ]
        items = clean_items(candidates, limit=5)
        for item in fallback:
            if len(items) >= 3:
                break
            items.append(item)
        return clean_items(items, limit=5)

    def _prioritized_plan(self, state: AgentState) -> dict[str, list[str]]:
        """Generate Must/Should/Could next-week tasks."""
        return {
            "must": [
                "确认文献方法与当前实验假设之间的对应关系。",
                "整理 2-3 条可直接用于组会的文献 takeaways。",
                "选择最值得展示的指标变化或失败场景。",
            ],
            "should": [
                "把 PDF 文献中的方法模块与当前实验设计建立对应关系。",
                "整理 3-5 个失败案例或代表性结果，支撑问题分析。",
                "明确哪些内容适合对外展示，哪些内容留作会前核对。",
            ],
            "could": [
                "为 PDF 文献加入章节级摘要和引用页码定位。",
                "增加自动图表或样例帧拼图，用于展示失败案例。",
                "补充更多场景下的稳定性实验，减少单次结果偶然性。",
            ],
        }

    def _questions(self, metric_cards: list[dict[str, object]]) -> list[tuple[str, str]]:
        """Return at least eight supervisor questions with answer directions."""
        metric_hint = "；".join(str(card["summary"]) for card in metric_cards[:2]) or "结合 before/after 指标或已补充实验记录回答。"
        return [
            ("本周最核心的研究结论是什么？", f"用指标变化、文献启发和失败场景共同回答，例如 {metric_hint}"),
            ("为什么该文献适合作为当前工作的背景？", "说明它与视频增强、恢复、退化建模或下游评估的关系。"),
            ("文献中的方法模块能否直接迁移？", "区分可直接借鉴的思路和需要重新验证的实现细节。"),
            ("当前实验是否已经支撑文献启发？", "说明已有指标、缺失指标和下一步验证计划。"),
            ("PSNR/SSIM 与检测连续性是否一致？", "回答它们衡量对象不同，需要同时报告图像质量和下游任务指标。"),
            ("下周最优先补什么数据？", "优先补能验证关键假设的数据，例如低光照、运动模糊或失败案例。"),
            ("PPT 展示中哪些内容需要老师建议？", "聚焦实验优先级、核心指标选择和失败案例展示方式。"),
            ("当前材料最适合形成什么样的汇报主线？", "强调文献背景、指标变化、失败风险和下一步验证之间的逻辑关系。"),
        ]

    def _discussion_items(self) -> list[str]:
        """Return questions suitable for the public presentation deck."""
        return [
            "下周是否优先补充低光照和运动模糊场景？",
            "是否建议将检测连续性作为核心汇报指标之一？",
            "是否需要增加失败案例可视化来支撑指标解释？",
        ]

    def _figure_items(self, state: AgentState) -> list[dict[str, str]]:
        """Return figure inventory items."""
        raw = state.figure_summary.get("items", [])
        if not isinstance(raw, list):
            return []
        return [item for item in raw if isinstance(item, dict)]

    def _evidence_chain_items(
        self,
        state: AgentState,
        paper_cards: list[dict[str, object]],
        metric_cards: list[dict[str, object]],
        figure_items: list[dict[str, str]],
    ) -> list[str]:
        """Connect materials to meeting-ready evidence."""
        items: list[str] = []
        if paper_cards:
            items.append("文献证据：论文卡片提供研究问题、方法关键词和可借鉴点。")
        if metric_cards:
            items.append("指标证据：实验结果提供 before/after 对比和提升幅度。")
        if figure_items:
            items.append("图像证据：figures 文件可用于展示代表性结果、对比图或失败案例。")
        if state.git_summary.get("commits"):
            items.append("工程证据：git log 可说明近期代码实现或实验脚本变化。")
        if not items:
            items.append("当前证据链较短，输出将以已检测材料为主保持保守。")
        return clean_items(items, limit=6)

    def _bullet_items(self, text: str) -> list[str]:
        """Extract cleaned bullet-like lines from Markdown text."""
        items: list[str] = []
        for line in clean_text(text).splitlines():
            stripped = line.strip()
            if stripped.startswith("- "):
                items.append(stripped[2:].strip())
        return items

    def _remove_next_plan_sections(self, text: str) -> str:
        """Remove explicit next-week-plan sections before extracting current work."""
        return re.sub(r"(?is)\n?#{1,6}\s*下周计划.*?(?=\n#{1,6}\s|\Z)", "", text)

    def _first_match(self, lines: list[str], keywords: list[str], fallback: str) -> str:
        """Find the first cleaned line matching any keyword."""
        for line in lines:
            if any(keyword.lower() in line.lower() for keyword in keywords):
                return re.sub(
                    r"^(核心方法|方法重点|方法|启发|可借鉴点|局限|风险|研究问题|关注点|疑问|方法启发)[:：]\s*",
                    "",
                    line,
                ).strip()
        return fallback

    def _flatten_numbers(self, obj: Any, prefix: str = "") -> dict[str, float]:
        """Flatten nested numeric metrics."""
        values: dict[str, float] = {}
        if isinstance(obj, dict):
            for key, value in obj.items():
                child = f"{prefix}.{key}" if prefix else str(key)
                values.update(self._flatten_numbers(value, child))
        elif isinstance(obj, (int, float)):
            values[prefix] = float(obj)
        return values

    def _find_metric(self, values: dict[str, float], suffix: str) -> float | None:
        """Find a metric by suffix in flattened data."""
        for key, value in values.items():
            if key.endswith(suffix):
                return value
        return None

    def _fmt(self, value: float, signed: bool = False) -> str:
        """Format metric values compactly."""
        prefix = "+" if signed and value > 0 else ""
        return f"{prefix}{value:.3f}".rstrip("0").rstrip(".")

    def _render_paper_cards(self, cards: list[dict[str, object]], supplementary_notes: str = "") -> str:
        """Render paper cards as Markdown."""
        parts: list[str] = []
        for index, card in enumerate(cards, start=1):
            source_type = str(card.get("source_type", "unknown"))
            source_label = "PDF" if source_type == "pdf" else "Note"
            parts.append(
                "\n".join(
                    [
                        f"### 文献 {index}: {card['paper']}（source_type: {source_label}）",
                        f"- 研究问题：{card['problem']}",
                        f"- 方法亮点：{card['method']}",
                        f"- 可借鉴点：{card['insight']}",
                        f"- 局限或疑问：{card['limitation']}",
                    ]
                )
            )
        notes = clean_items(remove_placeholder_lines(supplementary_notes).splitlines(), limit=6)
        if notes:
            parts.append("### 补充阅读笔记\n" + bullet_list(notes))
        return "\n\n".join(parts)

    def _render_analysis_cards(self, cards: list[dict[str, str]], issues: list[str]) -> str:
        """Render analysis and issue items."""
        parts = []
        for card in cards:
            parts.append(f"- 发现：{card['finding']} 原因：{card['explanation']} 证据：{card['evidence']}")
        parts.extend(f"- 风险：{item}" for item in issues[:3])
        return "\n".join(parts)

    def _render_plan(self, plan: dict[str, list[str]]) -> str:
        """Render prioritized plan as Markdown."""
        return "\n\n".join(
            [
                "### Must do\n" + bullet_list(plan["must"]),
                "### Should do\n" + bullet_list(plan["should"]),
                "### Could do\n" + bullet_list(plan["could"]),
            ]
        )
