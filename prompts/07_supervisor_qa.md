# Prompt: Supervisor Q&A

You are helping me prepare for questions from my supervisor in a graduate research meeting.

Based on the meeting pack, Evidence Map, claim strength labels, and available evidence, generate 6-8 likely supervisor questions.

For each question, include:

- the question
- why the supervisor might ask it
- a short answer direction
- what evidence I should cite
- what still needs confirmation
- the next verification action if the claim is weak or moderate

Output format:

```markdown
# Personal Prep: Supervisor Q&A

## Q1: ...
- Why it may be asked:
- Answer direction:
- Evidence to cite:
- Still needs confirmation:
- Next verification:
```

Rules:

- This is private preparation, not slide content.
- Focus on assumptions, baselines, metrics, limitations, and next experiments.
- Do not invent certainty where evidence is weak.
- Prefer questions that target weak claims, counter-evidence, missing baselines, metric conflicts, and manual confirmation items.
- Use `templates/supervisor_question_bank.md` as a reference when available.
- Use the relevant domain lens when the project domain is clear.
