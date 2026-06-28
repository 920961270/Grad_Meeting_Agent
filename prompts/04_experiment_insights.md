# Prompt: Experiment Insights

You are helping me interpret experiment results for a graduate research meeting.

I will provide metrics, CSV/JSON results, figure names, plots, screenshots, or notes.

Please produce experiment insights, not just a file summary.

Start with **Counter-example First / 反例优先**:

- Look for conflicting metrics.
- Look for abnormal samples, scenes, users, runs, or conditions.
- Look for results that do not match expectations.
- Look for missing repeats, missing baselines, or missing manual checks.
- Treat failure cases as useful meeting evidence, not as something to hide.

Cover:

1. Which metrics or results exist.
2. Before/after changes if available.
3. Which metric conflicts, anomalies, or counter-examples exist.
4. Which results are worth showing.
5. What the results might suggest.
6. What risks or alternative explanations remain.
7. What experiment should be done next.

Use a domain lens when relevant:

- CV / Video Enhancement: distinguish visual quality from downstream task performance. Do not equate PSNR/SSIM improvement with detection, tracking, or continuity improvement.
- Robotics / Control: check not only average error, but also abort rate, control delay, disturbance robustness, and completion status.
- Education / Learning Analytics: distinguish engagement from learning outcomes; check selection bias, attrition, survey bias, and interview coding reliability.
- HCI / AI Product Research: compare efficiency with error severity, trust, privacy risk, review flow, and task realism.
- Materials / Engineering: check process parameters, strength/hardness/elongation trade-offs, microstructure evidence, repeated samples, and abnormal samples.

Output format:

```markdown
# Experiment Insights

## Metrics or Results
- ...

## Counter-examples and Metric Conflicts
- ...

## Results Worth Showing
- ...

## Interpretation
- ...

## Risks and Alternative Explanations
- ...

## Next Experiment Suggestions
- ...
```

Rules:

- Do not treat a single result as a definitive conclusion.
- Explain image-quality metrics and downstream-task metrics separately when needed.
- Mention missing failure cases or missing baselines if relevant.
- If no direct counter-evidence is available, say what should be checked to find possible counter-evidence.
- State what evidence would make a weak or moderate interpretation stronger.
