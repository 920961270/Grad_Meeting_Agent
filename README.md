# Grad Meeting Agent

> 一个给 ChatGPT / Claude / Codex / Cursor 使用的 **AI-native 研究生组会准备 workflow skill**。

**AI-native Workflow Skill** · **Research Meeting Pack** · **Not a PPT Generator** · **Optional CLI Automation**

![AI-native Research Meeting Skill Workflow](pic/figure0.png)

## 🌱 这个项目是什么？

**Grad Meeting Agent 不是一键生成漂亮 PPT 的工具，也不是 CLI-first 项目。**

它是一套可复用的 AI 工作流 skill，帮助研究生把论文、实验结果、图像材料、进度记录、零散笔记和 git commits 整理成组会可用的 **meeting-ready evidence pack**。

组会前最痛苦的往往不是“做 PPT”，而是不知道这一周到底能讲什么、证据在哪里、哪些结论还不能说太满。

所以这个项目更像是“给 AI 的组会准备说明书”：你可以把 [skill.md](skill.md) 或 [prompts/](prompts/) 发给 ChatGPT / Claude / Codex / Cursor，让 AI 按固定流程帮你整理材料、提炼主线、标出风险，再生成 `Research Meeting Pack`。

PPT 是 optional，核心是 **research thinking organization**。

## ✨ 它能帮你做什么？

- 扫描论文、笔记、实验结果、图像材料、git commits
- 提炼本周组会主线 `Research Thread`
- 生成论文卡片 `Paper Cards`
- 分析实验结果 `Experiment Insights`
- 标出证据缺口 `Evidence Gap`
- 生成核心文档 `Research Meeting Pack`
- 给出可选 PPT 大纲 `Slide Outline`
- 准备导师可能追问 `Supervisor Q&A`

## 🧠 为什么不是直接问 ChatGPT？

当然可以直接问 AI：“帮我做组会 PPT。”

但这种问法通常会太泛：AI 可能直接开始写页面标题、堆 bullet，甚至把不确定的实验现象说成确定结论。

这个 repo 提供的是一套稳定、可复用、可检查的 workflow：

1. 先扫描材料，判断有哪些证据。
2. 再提炼本周可以汇报的研究主线。
3. 然后生成论文卡片、实验洞察、风险缺口。
4. 最后再决定哪些内容适合进入 PPT。

也就是说，它不是“另一个 prompt”，而是一套让 AI 更像科研助理一样工作的组会准备流程。

## 🗂️ 推荐输入材料

你不需要每一项都准备齐。材料不完整时，skill 会保守整理，并标记需要人工确认的点。

- `papers/` 或 PDF papers：论文、方法背景、相关工作
- `paper_notes.md`：中文阅读笔记、方法启发
- `experiment_results/`：CSV / JSON / metrics / tables
- `figures/`：plots / screenshots / before-after / failure cases
- `progress.md`：本周进展记录
- `notes.md`：零散想法、老师反馈、实验观察
- `git commits`：近期代码改动、实验脚本更新

可以参考：[templates/materials_checklist.md](templates/materials_checklist.md)

## 🚀 三种使用方式

### 方式 A：复制 skill.md 给 ChatGPT / Claude

适合你已经在 ChatGPT / Claude 里整理材料的情况。

```text
请使用下面这个 Research Meeting Skill 帮我准备研究生组会。
请先扫描材料，再提炼本周组会主线，最后生成 Research Meeting Pack。
不要把不确定内容写成强结论。
不要把导师 Q&A 放进公开 PPT。

<paste skill.md here>
```

然后把论文摘录、实验结果、图像说明、notes 或 progress 一起发给 AI。

你也可以分步骤复制这些 prompt：

- [01_material_scan.md](prompts/01_material_scan.md)
- [02_research_thread.md](prompts/02_research_thread.md)
- [03_paper_cards.md](prompts/03_paper_cards.md)
- [04_experiment_insights.md](prompts/04_experiment_insights.md)
- [05_meeting_pack.md](prompts/05_meeting_pack.md)
- [06_slide_outline.md](prompts/06_slide_outline.md)
- [07_supervisor_qa.md](prompts/07_supervisor_qa.md)

### 方式 B：让 Codex / Cursor 读取整个仓库

适合你的材料已经放在项目目录里，希望 AI 直接读取文件并整理。

```text
Read this repository as an AI-native Research Meeting Skill.
Use skill.md, prompts/ and templates/ to help me prepare a meeting-ready evidence pack.
Scan my input materials, infer the research thread, generate paper cards, experiment insights, gaps, discussion questions, and optional slide outline.
Do not treat this as a CLI-first project.
```

推荐材料目录：

```text
input/
├── papers/
├── experiment_results/
├── figures/
├── paper_notes.md
├── notes.md
└── progress.md
```

如果你在 Codex / Cursor 里工作，也可以让它顺手查看最近的 git commits，作为实现进展或实验脚本变化的证据。

### 方式 C：可选本地自动化 CLI

Python CLI 只是 optional automation，不是主入口。适合你想自动生成文件、反复跑 demo、或把流程接入本地材料时使用。

```bash
python main.py --input input --output output --backend rule
```

默认只输出：

```text
output/
├── meeting_pack.md
└── agent_state.json
```

生成 PPT：

```bash
python main.py --input input --output output --backend rule --with-slides
```

导出拆分明细文件：

```bash
python main.py --input input --output output --backend rule --export-details
```

生成全部内容：

```bash
python main.py --input input --output output --backend rule --all
```

## 📦 输出内容

核心输出：

- `Research Meeting Pack`：组会准备总文档
- `Evidence Map`：材料与证据链
- `Discussion Questions`：适合拿到组会上问导师的问题
- `Personal Prep Q&A`：自己会前准备的导师追问

可选输出：

- `Slide Outline`：PPT 结构建议
- `Editable PPT Skeleton`：可编辑 PPT 骨架
- `Optional CLI Automation`：本地自动生成文件

注意：`Personal Prep Q&A` 是给自己准备回答思路的，不适合直接放到公开 PPT 里。

## 📁 项目结构

```text
Grad_Meeting_Agent/
├── skill.md
├── prompts/
├── templates/
├── examples/
├── pic/
│   └── figure0.png
├── input/
├── src/
├── main.py
└── README.md
```

- `skill.md`：主 workflow，适合直接复制给 AI
- `prompts/`：分步骤 prompt，适合逐步整理材料
- `templates/`：Research Meeting Pack 模板和材料清单
- `examples/`：示例材料和使用说明
- `pic/`：README 图片
- `src/` 和 `main.py`：可选本地自动化

## 🧩 Workflow

1. `Material Scan`：扫描材料，判断有哪些证据
2. `Research Thread`：提炼本周可汇报主线
3. `Paper Cards`：生成论文卡片
4. `Experiment Insights`：解释实验结果
5. `Evidence Gap`：指出缺口和风险
6. `Meeting Pack`：生成组会准备包
7. `Optional Slide Outline`：生成可选 PPT 结构
8. `Supervisor Q&A`：生成个人准备问题

## 🤝 适合谁？

- 每周/月需要开组会的研究生
- 经常读论文但不知道怎么汇报的人
- 有实验结果但不知道怎么组织证据链的人
- 已经会用 ChatGPT / Claude / Codex / Cursor，想要更稳定 workflow 的人
- 想把“零散科研材料”整理成“组会可讲内容”的科研新手

## 🛣️ Roadmap

- [x] AI-native skill workflow
- [x] `skill.md`
- [x] `prompts/`
- [x] meeting pack template
- [x] optional CLI automation
- [x] README workflow diagram
- [ ] 更好的 examples
- [ ] 中文/英文双语模板
- [ ] 更强的 paper grounded extraction
- [ ] figures 图像理解与失败案例整理
- [ ] Streamlit demo，可选

## 📄 License

MIT
