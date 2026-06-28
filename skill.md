# Research Meeting Skill

Use this skill to prepare graduate research meetings from scattered research materials. The goal is not to generate a decorative PPT first. The goal is to help an AI assistant organize evidence, clarify the weekly research thread, identify risks, and produce a meeting-ready preparation pack.

## Goal

Turn messy weekly research materials into a clear research meeting pack:

- what can be reported this week
- what evidence supports it
- what papers are relevant
- what experiments suggest
- what is uncertain
- what should be discussed with the supervisor
- what can optionally become a slide outline

## Inputs

Accept any combination of:

- `papers/`: PDF papers or paper text excerpts
- `paper_notes.md`: human-written literature notes
- `experiment_results/`: CSV, JSON, tables, metric logs, or copied result snippets
- `figures/`: result images, before-after comparisons, plots, failure cases
- `git log`: recent commits or a pasted commit summary
- `progress.md`: weekly progress notes
- `notes.md`: rough observations, advisor feedback, TODOs, meeting notes

Do not require every input. If materials are incomplete, produce a conservative pack and mark what needs confirmation.

## Domain Lens

After scanning the materials, infer the closest research domain or method type. If the materials clearly match one of the domain lenses in `prompts/domain_lenses.md`, use that lens when judging metrics, claims, risks, and supervisor questions.

Use the general research lens when the domain is unclear. Do not force a domain label just because one keyword appears.

## Claim Strength / 结论强度

Every core claim in the meeting pack must be assigned a claim strength:

- `Strong`: supported by multiple aligned sources, such as metrics + figures + notes + repeated results.
- `Moderate`: supported by partial experiments or literature, but limited by sample size, scenes, baselines, or validation.
- `Weak`: supported by a single source, initial observation, early sample, or unverified qualitative impression.
- `Insufficient`: current materials are not enough for a claim; treat it as an issue, hypothesis, or next question.

For each core claim, record:

- claim
- evidence source: paper, metrics, figures, notes, progress, or git
- counter-evidence or possible conflict
- manual confirmation needed
- next verification action

Do not turn weak evidence into strong conclusions. Do not only write "needs confirmation"; specify what to confirm, how to confirm it, and what result would make the claim stronger.

## Counter-example First / 反例优先

Before summarizing positive results, actively look for:

- conflicting metrics
- abnormal samples or scenes
- results that do not match expectations
- failure cases worth discussing
- missing repeats, baselines, or manual checks

Examples:

- CV / video enhancement: PSNR or SSIM improves, but detection stability, IoU continuity, or confidence drops.
- Robotics / control: average error decreases, but abort rate, control delay, or disturbance sensitivity increases.
- Education / learning analytics: study time increases, but quiz score or retention does not improve.
- HCI / AI product research: task time decreases, but error severity, trust, privacy risk, or review burden worsens.
- Materials / engineering: strength or hardness improves, but elongation, microstructure evidence, or repeatability becomes worse.

## Workflow

### 1. Material Scan

List available materials and infer what kind of evidence each can support:

- papers support background, methods, related work, and assumptions
- experiment tables support metrics, trends, and comparisons
- figures support result examples, before-after comparison, and failure cases
- notes support observations and meeting context
- git log supports implementation or experiment activity
- progress notes support explicit weekly work

Infer the likely domain and apply the matching domain lens if available.

Keep this scan internal or concise. Do not expose tool-like phrases in the final meeting material.

### 2. Research Thread

Infer the main story for this week's meeting:

- research question or task
- what changed this week
- why it matters
- what evidence supports it
- what remains uncertain

Use cautious wording. Do not turn weak evidence into strong conclusions.

### 3. Paper Cards

For each important paper, produce a compact card:

- paper name
- research problem
- method keywords
- takeaways for the current project
- how to explain it in the meeting
- still-to-confirm points

If the paper text is partial, say which conclusions need manual confirmation.

### 4. Experiment Insights

Interpret results instead of only listing files:

- which metrics or result patterns exist
- before/after changes if available
- what is worth showing
- what the results might suggest
- what risks or alternative explanations remain
- what counter-examples, anomalies, or metric conflicts should be discussed

Connect image-quality metrics and downstream-task metrics carefully.

### 5. Evidence Gap

Identify gaps and risks:

- paper method may not map cleanly to current experiments
- metric improvements may not be stable across scenes
- failure cases may be missing
- sample size may be too small
- results may need stronger baselines
- qualitative figures may not support quantitative claims

Mark these as risks, not failures.

Use an evidence map to connect each claim to supporting evidence, counter-evidence, claim strength, manual confirmation, and next action.

### 6. Meeting Pack

Generate a single preparation document with:

1. one-page summary
2. research thread
3. paper cards
4. experiment insights
5. evidence map with claim strength
6. counter-evidence, gaps, and risks
7. meeting agenda
8. discussion questions
9. personal prep: supervisor Q&A

Personal prep is for the student only. Do not include it in public slides unless explicitly asked.

### 7. Slide Outline

Optionally generate a slide outline:

1. Title
2. Research Context
3. Paper Takeaways
4. Experiment Evidence
5. Key Insights
6. Issues & Risks
7. Next Actions
8. Discussion

Slides should be concise. Keep uncertainty visible.

### 8. Supervisor Q&A

Generate 6-8 likely supervisor questions and short answer directions. Derive these questions from weak claims, counter-evidence, missing baselines, unclear metrics, manual confirmation items, and domain-specific risks.

## Output Principles

- Do not expose tool internals, execution logs, hidden file handling, or automation details.
- Do not write uncertain content as confirmed conclusions.
- Mark claim strength for core claims.
- Include counter-evidence or say how to check for it when no direct counter-evidence appears in the current materials.
- Prefer meeting-ready language over implementation commentary.
- Clearly mark points that need manual confirmation.
- Preserve useful filenames only when they help identify a paper, table, figure, or result.
- Avoid asking the user to fill missing templates. Instead say what the current evidence supports.
- Keep PPT content separate from private supervisor Q&A.
