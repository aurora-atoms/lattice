---
name: management-translation
description: Use to translate Feature Delivery Case evidence into executive feature briefs, risk escalation packets, and audience-specific management updates; do not use to hide uncertainty, beautify status by dropping risks, make commitments, or expose unnecessary technical or sensitive detail; input is a bounded readiness card, outcome evidence, risks, options, deadlines, resource requests, and audience level; output is a traceable one-page brief, decision request, oral-update outline, or escalation packet focused on purpose, delivered state, evidence, risk, next milestone, and required decision while preserving factual accuracy and human approval.
---

# Management Translation

## Goal
Turn engineering evidence into concise, accurate, actionable management communication without losing uncertainty or decision context.

## Use When
Select the smallest sufficient atomic capability:
- H01 Executive Feature Brief
- H02 Risk Escalation Packet
- H03 Management Translation Output

## Do Not Use When
Do not use to hide risk, create unauthorized commitments, or expose unnecessary sensitive detail.

## Inputs
Use a bounded readiness card, outcome evidence, risks, options, deadlines, resource requests, audience level, and source references.

## Outputs
Return a one-page brief, decision request, oral-update outline, or escalation packet focused on purpose, current delivery state, evidence, risk, milestone, and required decision.

## Workflow
1. Identify audience and decision need.
2. Select one atomic capability first.
3. Project only necessary evidence for that audience.
4. Preserve facts, uncertainty, risks, and decision ownership.
5. Produce a concise artifact suitable for owner review.

## Rules
HCAT.001 | MUST | routing | select_one_atomic_capability_before_composing | enforce
HCAT.002 | MUST | evidence | preserve_source_traceability_and_uncertainty | enforce
HCAT.003 | MUST | audience | minimize_detail_without_losing_decision_context | enforce
HCAT.004 | MUST | human | require_owner_confirmation_for_recommendation_or_commitment | enforce
HCAT.005 | MUST | token | optimize_quality_adjusted_output_per_token_cost | enforce
HCAT.006 | SHOULD | prompt | keep_rules_and_output_contract_in_stable_prefix | prefer
HCAT.007 | NEVER | narrative | hide_risk_or_unknown_for_presentation_quality | block
HCAT.008 | NEVER | metric | lead_with_commits_pr_count_tokens_or_agent_activity | block

## Verification
- The artifact states purpose, delivery state, evidence, risk, and decision need.
- Claims remain traceable.
- Recommendations and commitments are owner-confirmed.

## Failure Modes
- Leading with engineering activity rather than delivery state.
- Removing risk to make status look better.
- Presenting generated language as an approved commitment.
