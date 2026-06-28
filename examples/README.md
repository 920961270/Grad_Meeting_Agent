# Example Workflow

This example shows how the Research Meeting Skill can be used with scattered weekly research materials.

## Example Materials

A student may have:

- `papers/EDVR.pdf`: a video restoration paper
- `paper_notes.md`: rough notes about alignment, fusion, and degradation modeling
- `experiment_results/metrics.json`: PSNR, SSIM, Recall, or Continuity metrics
- `experiment_results/results.csv`: scene-level records
- `figures/`: before-after examples, plots, or failure cases
- `notes.md`: advisor feedback and observations
- recent git commits: experiment scripts or evaluation changes

The materials do not need to be complete. The workflow should still produce a conservative meeting pack.

## How AI Scans the Materials

The assistant first identifies what each material can support:

- papers support research background and method takeaways
- experiment tables support metric evidence
- figures support qualitative examples and failure cases
- notes support interpretation and discussion questions
- git commits support implementation progress

The scan should not become the final report. It is a reasoning step that helps the AI avoid overclaiming.

## Example Meeting Pack Shape

The final `Research Meeting Pack` should look like:

```markdown
# Research Meeting Pack

## 1. One-page Summary
- This week focuses on video enhancement evidence and downstream evaluation.
- Current metrics suggest a possible improvement trend, but stability needs more scenes.
- The paper reading suggests alignment and temporal fusion are relevant to the current task.

## 2. Research Thread
Current evidence suggests the main question is whether enhancement improves both visual quality and downstream detection consistency.

## 3. Paper Cards
### Paper 1: EDVR
- Research problem: video restoration under degradation
- Method keywords: alignment, temporal fusion, reconstruction
- Takeaway: compare temporal consistency and downstream continuity in current experiments
- Still needs confirmation: which module maps cleanly to the current setup

## 4. Experiment Insights
- PSNR/SSIM can support visual-quality claims.
- Recall/Continuity should be used for downstream-task claims.
- Failure cases are needed to explain where improvement does not hold.

## 5. Evidence Map with Claim Strength
| Claim / 结论 | Supporting Evidence / 支持证据 | Counter-evidence / 反例或冲突 | Strength | Manual Confirmation | Next Action |
|---|---|---|---|---|---|
| Enhancement may improve visual quality in current samples. | PSNR/SSIM metrics, before-after figures | Current materials may not cover enough scenes. | Moderate | Check scene diversity and failure cases. | Run evaluation on more low-light and motion-blur scenes. |
```

## Synthetic Case Policy

`test_outputs/` may contain generated evaluation results. Do not copy those generated packs into examples as if they were source materials.

If synthetic cases are added later, keep only the raw `materials/` for each case under `examples/synthetic_cases/`, and avoid committing generated outputs.

## What Belongs In Slides

Good slide content:

- research context
- 2-3 paper takeaways
- key metrics or before-after comparisons
- representative result figures
- issues and risks
- next actions
- 3-5 discussion questions

## What Is Personal Prep Only

Keep these out of public slides unless explicitly needed:

- supervisor Q&A answer scripts
- uncertainty notes that are not ready to show
- private TODOs
- tool logs or automation details
- unverified guesses

## Optional CLI Example

If you want the repository to generate files automatically:

```bash
python main.py --input examples/ai_cv_research_example --output output --backend rule
```

For slides:

```bash
python main.py --input examples/ai_cv_research_example --output output --backend rule --with-slides
```
