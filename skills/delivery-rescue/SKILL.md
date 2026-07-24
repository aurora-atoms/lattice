---
name: delivery-rescue
description: Use for evidence-grounded diagnosis of CI failures, bug reproduction, local environment failures, and contract-breaking changes that block delivery; do not use for feature planning, release approval, production deployment, or speculative diagnosis without source evidence; input is bounded logs, diffs, environment facts, contracts, tests, and Feature Delivery Case context; output is a ranked root-cause assessment, minimum next action, validation command, evidence classification, human confirmation points, and bounded write-back that preserves safety and quality-adjusted token ROI.
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
2. Select one atomic capability before composing several.
3. Load only minimum authorized evidence.
4. Separate fact, inference, and unknown.
5. Produce an actionable repair, reproduction, or compatibility path.
6. Stop at the requested visible result or escalate.

## Rules
ACAT.001 | MUST | scope | use_feature_delivery_case_as_primary_context_boundary | enforce
ACAT.002 | MUST | routing | select_one_atomic_capability_before_composing | enforce
ACAT.003 | MUST | evidence | separate_fact_inference_and_unknown | enforce
ACAT.004 | MUST | context | load_minimum_authorized_context_pack_not_raw_dump | enforce
ACAT.005 | MUST | human | preserve_owner_confirmation_and_final_judgment | enforce
ACAT.006 | MUST | token | optimize_quality_adjusted_output_per_token_cost | enforce
ACAT.007 | SHOULD | prompt | keep_rules_and_output_contract_in_stable_prefix | prefer
ACAT.008 | NEVER | authority | approve_merge_release_deploy_or_business_scope | block
ACAT.009 | NEVER | memory | auto_promote_output_to_memory_belief_rule_or_skill | block

## Verification
- Claims have evidence or are marked inference/unknown.
- The output creates a state change or executable next step.
- High-risk or global changes require human approval.

## Failure Modes
- Treating a flaky symptom as a proven root cause.
- Modifying global or production state without approval.
- Silently accepting a breaking contract.
- Loading full logs or repositories by default.
