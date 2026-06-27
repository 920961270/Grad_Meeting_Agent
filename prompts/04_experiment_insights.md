# Prompt: Experiment Insights

You are helping me interpret experiment results for a graduate research meeting.

I will provide metrics, CSV/JSON results, figure names, plots, screenshots, or notes.

Please produce experiment insights, not just a file summary.

Cover:

1. Which metrics or results exist.
2. Before/after changes if available.
3. Which results are worth showing.
4. What the results might suggest.
5. What risks or alternative explanations remain.
6. What experiment should be done next.

Output format:

```markdown
# Experiment Insights

## Metrics or Results
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
