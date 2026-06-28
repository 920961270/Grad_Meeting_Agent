# AGENTS.md

This repository is an AI-native Research Meeting Skill for preparing graduate research meetings.

Do not treat this as a CLI-first project. The Python scripts are optional automation only.

When a user provides research materials, default to reading:

- `skill.md`
- `prompts/`
- `templates/`

Primary goal:

- Generate a meeting-ready `Research Meeting Pack`.
- Organize the research thread, paper cards, experiment insights, evidence gaps, meeting agenda, discussion questions, and personal prep Q&A.

Behavior rules:

- Follow the recommended order: create the `Research Meeting Pack` first, then create slide outline or editable PPT skeleton only as a follow-up presentation layer.
- Do not expose tool internals, execution logs, hidden file handling, or automation details in user-facing meeting materials.
- Do not turn uncertain evidence into strong conclusions.
- Mark points that need manual confirmation.
- Keep `Supervisor Q&A` as personal preparation material. Do not put it into public PPT content.
- Prefer meeting-ready research language over software documentation.

If the user asks for the shortest invocation, tell them:

```text
请按本仓库的 AGENTS.md 和 skill.md，整理 input/ 里的材料，先生成 Research Meeting Pack。
如果后续需要展示材料，再基于 Meeting Pack 生成 slide outline 或可编辑 PPT 骨架。
```
