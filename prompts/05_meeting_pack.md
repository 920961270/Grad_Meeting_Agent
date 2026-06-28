# Prompt: Meeting Pack

You are helping me prepare a graduate research meeting.

Use the material scan, research thread, paper cards, experiment insights, figures, notes, and known gaps to create one complete meeting preparation pack.

Use this exact structure:

```markdown
# Research Meeting Pack

## 1. One-page Summary

## 2. Research Thread

## 3. Paper Cards

## 4. Experiment Insights

## 5. Evidence Map with Claim Strength

## 6. Counter-evidence & Gaps

## 7. Meeting Agenda

## 8. Discussion Questions

## 9. Personal Prep: Supervisor Q&A
```

Requirements:

- Keep the writing meeting-ready.
- Do not expose internal workflow or automation details.
- Do not ask me to fill missing templates.
- Use cautious language for uncertain points.
- Mark what needs manual confirmation.
- Keep supervisor Q&A in the personal prep section only.
- Every core claim must have a claim strength: `Strong`, `Moderate`, `Weak`, or `Insufficient`.
- Weak or moderate claims must include a concrete next action.
- Do not only say "needs confirmation"; say what is missing, how to check it, and what would make the claim stronger.
- If metrics conflict, make the conflict part of the meeting thread rather than hiding it as a generic risk.
- Use domain-specific reasoning when relevant, rather than generic research language.

Evidence Map format:

```markdown
| Claim / 结论 | Supporting Evidence / 支持证据 | Counter-evidence / 反例或冲突 | Strength | Manual Confirmation | Next Action |
|---|---|---|---|---|---|
| ... | ... | ... | Strong / Moderate / Weak / Insufficient | ... | ... |
```

Counter-evidence rules:

- Include anomalies, conflicting metrics, missing repeats, missing baselines, abnormal samples, or unclear assumptions.
- If no direct counter-evidence appears in the materials, write: "Current materials provide no direct counter-evidence, but this still needs confirmation by ...".
- Do not overstate results that only have one source of evidence.

Supervisor Q&A rules:

- Generate questions from the weak claims, counter-evidence, manual confirmation items, and domain-specific risks in the Evidence Map.
- Include 6-8 questions with one-sentence answer directions.
- Keep these as personal preparation, not public slide content.
