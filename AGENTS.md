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
- Include claim strength and an evidence map for core claims.

Behavior rules:

- Follow the recommended order: create the `Research Meeting Pack` first, then create slide outline or editable PPT skeleton only as a follow-up presentation layer.
- After reading materials, determine the likely domain or research type.
- Use `prompts/domain_lenses.md` when the materials fit a domain lens; otherwise use a general research lens.
- Actively look for counter-evidence, conflicting metrics, abnormal samples, failure cases, missing repeats, missing baselines, and manual checks.
- Every core claim should be labeled as `Strong`, `Moderate`, `Weak`, or `Insufficient`.
- For weak or moderate claims, state the concrete next verification action.
- Do not expose tool internals, execution logs, hidden file handling, or automation details in user-facing meeting materials.
- Do not turn uncertain evidence into strong conclusions.
- Mark points that need manual confirmation.
- Build `Supervisor Q&A` from weak claims, evidence gaps, counter-evidence, manual confirmation items, and domain-specific risks.
- Keep `Supervisor Q&A` as personal preparation material. Do not put it into public PPT content.
- Prefer meeting-ready research language over software documentation.

Shortest coding-agent invocation:

```text
请按本仓库的 AGENTS.md 和 skill.md，整理 materials/ 里的材料；如果没有 materials/，再检查 input/。先生成 Research Meeting Pack，并标注核心结论的证据强度与 Evidence Map。
如果后续需要展示材料，再基于 Meeting Pack 生成 slide outline 或可编辑 PPT 骨架。
```
