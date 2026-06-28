# Supervisor Question Bank

Use these questions to generate `Personal Prep: Supervisor Q&A`. Choose questions based on weak claims, counter-evidence, manual confirmation items, and domain-specific risks from the Evidence Map.

## General Questions

- What is the exact sample size, and is it enough for this claim?
- How are the key metrics defined, and are they comparable across baselines?
- Is the baseline fair, recent, and configured under the same conditions?
- Can the result be reproduced across repeated runs or different scenes?
- What is the strongest counter-example or failure case?
- How well does this result generalize beyond the current dataset or scenario?
- Which results require manual review before being shown as evidence?
- What stronger baseline or ablation should be tested next?
- Why did the failure case happen, and can it be categorized?
- If there is only time for one next experiment, which one most reduces uncertainty?

## CV / Video Enhancement

- Why do PSNR/SSIM and downstream detection or tracking metrics agree or disagree?
- Has the detector or downstream model been sanity-checked on original and enhanced images?
- What failure taxonomy can explain low-light, blur, artifact, or temporal instability cases?

## Robotics / Control

- How is control delay measured, and does it change under disturbance?
- Are current disturbance, sensor noise, or calibration drift reproducible across runs?
- Are abort runs included in the statistics or filtered out?

## Education / Learning Analytics

- Does higher engagement actually map to improved learning outcomes?
- Could selection bias or attrition explain the observed result?
- Was interview coding checked by more than one coder or with agreement evidence?

## HCI / AI Product Research

- How is error severity scored, and are severe errors more important than average speed?
- How should privacy risk influence the product decision?
- Is the system replacing human judgment or improving the review flow?

## Materials / Engineering

- How many repeated samples support the reported result?
- Does microstructure evidence explain the mechanical performance?
- Is there a strength, hardness, or elongation trade-off that changes the best process choice?
