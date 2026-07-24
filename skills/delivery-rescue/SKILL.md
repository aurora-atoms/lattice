---
name: delivery-rescue
description: Use for evidence-grounded diagnosis of CI failures, bug reproduction, local environment failures, and contract-breaking changes that block delivery; do not use for feature planning, release approval, production deployment, or speculative diagnosis without source evidence; input is bounded logs, diffs, environment facts, contracts, tests, and Feature Delivery Case context; output is a ranked root-cause assessment, minimum next action, validation command, evidence classification, human confirmation points, and bounded write-back that preserves behavioral constraints, safety, and quality-adjusted token ROI.
---

# Delivery Rescue

## Goal
Move a blocked Feature Delivery Case to a verified next action or restored working state.

## Use When
Select the smallest sufficient atomic capability:
- A01 Red-to-Green CI Diagnosis
- A02 Bug-to-Repro
- A03 Environment Doctor
- A04 Contract Break Detector

## Do Not Use When
Do not use for feature planning, release approval, production deployment, or unsupported speculation.

## Inputs
Use a task-bounded context pack: relevant logs, diff, tests, environment facts, contracts, permissions, and evidence references.

## Outputs
Return a ranked diagnosis, minimum repair or reproduction path, validation commands, affected consumers, human confirmations, and bounded Feature Delivery Case write-back.

## Workflow
1. Classify the blocker.
2. Query ConPort before loading or searching the full skill text when ConPort is available; otherwise use targeted source reads.
3. Select one atomic capability before composing several.
4. Load only minimum authorized evidence.
5. Separate fact, inference, and unknown.
6. Produce an actionable repair, reproduction, or compatibility path.
7. Stop at the requested visible result or escalate.

## Rules
ACAT.001 | MUST | scope | use the Feature Delivery Case as the primary context boundary | enforce
ACAT.002 | MUST | routing | select one atomic capability before composing | enforce
ACAT.003 | MUST | evidence | separate fact, inference, and unknown | enforce
ACAT.004 | MUST | context | load the minimum authorized context pack instead of a raw dump | enforce
ACAT.005 | MUST | human | preserve owner confirmation and final judgment | enforce
ACAT.006 | MUST | token | optimize quality-adjusted token ROI | enforce
ACAT.007 | SHOULD | prompt | keep rules and the output contract in a stable prefix | prefer
ACAT.008 | NEVER | authority | approve merge, release, deploy, or business scope | block
ACAT.009 | NEVER | memory | auto-promote output to memory, belief, rule, or skill | block

## Verification
- Claims have evidence or are marked inference/unknown.
- The output creates a state change or executable next step.
- High-risk or global changes require human approval.

## Failure Modes
- Treating a flaky symptom as a proven root cause.
- Modifying global or production state without approval.
- Silently accepting a breaking contract.
- Loading full logs or repositories by default.
