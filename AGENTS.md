# AGENTS.md

This repository is an AI-native Research Meeting Skill for preparing graduate research meetings.

Do not treat this as a CLI-first project. The Python scripts are optional automation only.

Default reading order:

- `README.md`
- `skill.md`
- `prompts/`
- `templates/`

When the user asks to organize meeting materials:

- First look for a `materials/` directory in the current workspace.
- If there is no `materials/`, then check `input/`.
- Do not assume you can access arbitrary local folders on the user's computer.
- If no materials are available in the workspace, ask the user to place materials in `materials/` or upload a zip archive such as `meeting_materials.zip`.
- Do not ask the user to upload files one by one if a workspace directory or zip upload can be used.

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

Shortest coding-agent invocation:

```text
请按本仓库的 AGENTS.md 和 skill.md，整理 materials/ 里的材料；如果没有 materials/，再检查 input/。先生成 Research Meeting Pack。
如果后续需要展示材料，再基于 Meeting Pack 生成 slide outline 或可编辑 PPT 骨架。
```
