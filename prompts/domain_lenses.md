# Prompt: Domain Lenses

Use this prompt when the materials fit a recognizable research domain. The goal is to judge evidence with the right lens, not to force every project into the same generic template.

If the domain is unclear, use the general research lens:

- What is the claim?
- What evidence supports it?
- What evidence could challenge it?
- What assumption is still unverified?
- What next check would make the claim stronger?

## CV / Video Enhancement

Look for the relationship between image quality and downstream task performance:

- PSNR / SSIM / LPIPS / perceptual quality
- detection confidence, IoU, tracking continuity, temporal stability
- low-light scenes, motion blur, artifacts, over-smoothing, color shift
- before-after visual examples and failure cases

Do not equate image quality improvement with downstream task improvement. If PSNR/SSIM improves but detection stability or IoU continuity drops, treat it as a key meeting issue.

## Robotics / Control

Look beyond average error:

- trajectory error, depth error, localization error
- sensor noise, current disturbance, water turbidity, calibration drift
- control delay, abort rate, completion status, recovery behavior
- robustness under repeated runs and disturbed scenes

Do not only report lower average error. A result may be weaker if aborts, control delay, or instability increases.

## Education / Learning Analytics

Separate engagement from learning outcomes:

- study time, login frequency, completion rate, click behavior
- quiz scores, retention, transfer tasks, delayed assessment
- selection bias, attrition, prior knowledge, survey bias
- interview coding, inter-rater agreement, qualitative evidence

Do not treat higher engagement as a causal learning effect unless outcome evidence and bias checks support it.

## HCI / AI Product Research

Balance efficiency with quality and risk:

- task time, completion rate, error rate
- error severity, trust calibration, privacy risk, human review flow
- task realism, user expertise, workload, failure recovery
- auto-generation vs assisted-review trade-offs

Do not equate task time reduction with product success. If time improves but severe errors or privacy risk increase, make that the central finding.

## Materials / Engineering

Check trade-offs and physical evidence:

- process parameters, temperature, pressure, composition, treatment time
- strength, hardness, elongation, fatigue, corrosion, stability
- microstructure evidence, grain size, phase changes, defects
- repeated samples, outliers, abnormal samples, measurement conditions

Do not treat a single highest metric as the best process. A stronger claim needs repeated samples and microstructure evidence that explains the measured performance.
