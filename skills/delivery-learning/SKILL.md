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
2. Query ConPort before loading or searching the full skill text when ConPort is available; otherwise use targeted source reads.
3. Select one atomic capability first.
4. Link evidence to the Feature Delivery Case.
5. Separate reusable candidate from approved reusable asset.
6. Add applicability, review, and expiry conditions.
7. Require owner review before promotion.

## Rules
FCAT.001 | MUST | object | use the Feature Delivery Case as the primary learning unit | enforce
FCAT.002 | MUST | routing | select one atomic capability before composing | enforce
FCAT.003 | MUST | evidence | attach source, scope, and result evidence | enforce
FCAT.004 | MUST | promotion | keep a candidate separate from approved memory, rule, or skill | enforce
FCAT.005 | MUST | metrics | preserve multi-metric product judgment | enforce
FCAT.006 | MUST | token | optimize quality-adjusted token ROI | enforce
FCAT.007 | SHOULD | prompt | keep rules and the output contract in a stable prefix | prefer
FCAT.008 | NEVER | memory | store raw transcripts as memory | block
FCAT.009 | NEVER | promotion | auto-promote single-case learning | block

## Verification
- Learning is linked to a Feature Delivery Case.
- Candidate status and applicability limits are explicit.
- Review and expiry conditions exist.

## Failure Modes
- Storing raw transcripts as memory.
- Auto-promoting candidates into beliefs or rules.
- Equating delivery completion with product success.
