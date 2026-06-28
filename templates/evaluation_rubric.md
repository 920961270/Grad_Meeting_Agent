# Research Meeting Pack Evaluation Rubric

Use this rubric to review whether a generated `Research Meeting Pack` is meeting-ready and evidence-aware.

Score each dimension from 1 to 5:

- `1`: missing
- `2`: generic
- `3`: adequate
- `4`: good with specific evidence
- `5`: strong handling of conflict, counter-evidence, and uncertainty

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Claim strength accuracy | Claims have no strength labels or overstate weak evidence. | Most claims have reasonable strength labels. | Strength labels clearly match evidence coverage, sample size, repeats, and validation limits. |
| Counter-evidence identification | No counter-evidence, anomalies, or failure cases are mentioned. | Some risks are mentioned, but not always tied to specific claims. | Conflicting metrics, abnormal cases, missing baselines, and failure examples are explicitly linked to claims. |
| Evidence vs assumption vs speculation | Evidence, assumptions, and guesses are mixed together. | Some uncertainty is marked. | Each major statement clearly distinguishes observed evidence, interpretation, and speculation. |
| Actionable next actions | Next steps are vague, such as "continue testing". | Next steps are mostly concrete. | Next actions specify what to test, how to test it, and what result would strengthen or weaken the claim. |
| Domain-specific reasoning | The pack uses generic research language. | Some domain terms appear, but the reasoning is shallow. | The pack uses the right domain lens and catches domain-specific trade-offs or metric conflicts. |
| Meeting readiness | The pack reads like raw notes or a software log. | The pack can support a basic meeting. | The pack gives a clear story, evidence map, discussion agenda, and personal preparation questions. |

## Review Questions

- Does every core claim have supporting evidence and claim strength?
- Does the Evidence Map include counter-evidence or a concrete way to search for it?
- Are weak and moderate claims paired with specific next actions?
- Are domain-specific metrics interpreted carefully?
- Are Supervisor Q&A questions derived from weak claims and evidence gaps?
