---
name: delivery-learning
description: Use for Feature Delivery Case maintenance, bounded delivery-memory assets, incident-to-control conversion, feature outcome review, measurement planning, and case-level delivery confidence; do not use to auto-promote one lesson into a universal rule, approve delivery, or replace product judgment with one metric; input is lifecycle evidence, decisions, tests, incidents, outcomes, metrics, user feedback, and scoped human annotations; output is a versioned Delivery Case update, reusable learning candidate, immune-control proposal, measurement plan, outcome comparison, and confidence evidence with applicability limits, review conditions, and behavior-preserving safeguards.
---

# Delivery Learning

## Goal
Make each delivery improve the next one while preserving evidence, scope, review, and expiry boundaries.

## Use When
Select the smallest sufficient atomic capability:
- F01 Feature Delivery Case
- F02 Delivery Memory Asset
- F03 Delivery Immune System
- F04 Feature Outcome Loop
- F05 Measurement Plan Pack
- F06 Delivery Confidence Loop

## Do Not Use When
Do not use to generalize from one case, auto-promote memory/rules, approve delivery, or reduce product value to one metric.

## Inputs
Use lifecycle intent, decisions, tests, risks, incidents, release evidence, outcomes, metrics, user feedback, and human annotations.

## Outputs
Return versioned Delivery Case updates, reusable candidates with limits, immune-control proposals, measurement plans, outcome comparisons, and case-level confidence evidence.

## Workflow
1. Identify the lifecycle event and target learning object.
2. Select one atomic capability first.
3. Link evidence to the Feature Delivery Case.
4. Separate reusable candidate from approved reusable asset.
5. Add applicability, review, and expiry conditions.
6. Require owner review before promotion.

## Rules
FCAT.001 | MUST | object | use_feature_delivery_case_as_primary_learning_unit | enforce
FCAT.002 | MUST | routing | select_one_atomic_capability_before_composing | enforce
FCAT.003 | MUST | evidence | attach_source_scope_and_result_evidence | enforce
FCAT.004 | MUST | promotion | keep_candidate_separate_from_approved_memory_rule_or_skill | enforce
FCAT.005 | MUST | metrics | preserve_multi_metric_product_judgment | enforce
FCAT.006 | MUST | token | optimize_quality_adjusted_output_per_token_cost | enforce
FCAT.007 | SHOULD | prompt | keep_rules_and_output_contract_in_stable_prefix | prefer
FCAT.008 | NEVER | memory | store_raw_transcripts_as_memory | block
FCAT.009 | NEVER | promotion | auto_promote_single_case_learning | block

## Verification
- Learning is linked to a Feature Delivery Case.
- Candidate status and applicability limits are explicit.
- Review and expiry conditions exist.

## Failure Modes
- Storing raw transcripts as memory.
- Auto-promoting candidates into beliefs or rules.
- Equating delivery completion with product success.
