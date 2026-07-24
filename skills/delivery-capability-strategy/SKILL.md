---
name: delivery-capability-strategy
description: Use to reframe AI-adoption requests into delivery-capability design and to connect AI token or cost evidence to visible user-usable feature delivery; do not use as a generic AI adoption campaign, activity dashboard, model competition, cost-minimization exercise, or runtime coding orchestrator; input is delivery goals, team pain points, available capabilities, Feature Delivery Cases, token or cost records with known, estimated, or provider-reported status, and outcome evidence; output is a capability strategy, Token-to-Delivery view, waste hypothesis, next optimization signal, and manager-facing recommendation that preserves active module boundaries and DeliveryYield measurement-only scope.
---

# Delivery Capability Strategy

## Goal
Choose and evaluate delivery capabilities by user-usable outcomes and quality-adjusted token economics rather than AI activity or raw cost alone.

## Use When
Select the smallest sufficient atomic capability:
- I01 Delivery Capability Operating Layer Reframing
- I02 Token Economics / Delivery Yield Reframing

## Do Not Use When
Do not use as a generic AI adoption campaign, model competition, raw activity dashboard, or runtime agent orchestrator.

## Inputs
Use delivery goals, team pain points, capability inventory, Feature Delivery Cases, token/cost records with evidence status, and visible delivery outcomes.

## Outputs
Return delivery-problem-to-capability mapping, feature-level token/cost-to-outcome view, waste hypotheses, evidence status, next optimization signals, and manager-facing recommendations.

## Workflow
1. Reframe adoption or cost questions around user-usable delivery outcomes.
2. Select I01 or I02 first.
3. Bind evidence to Feature Delivery Cases.
4. Preserve known, estimated, provider-reported, and unknown status.
5. Identify waste without rewarding quality degradation.
6. Produce next optimization or investment recommendation.

## Rules
ICAT.001 | MUST | outcome | use_user_usable_feature_delivery_as_primary_value_unit | enforce
ICAT.002 | MUST | evidence | bind_token_and_cost_to_feature_delivery_case | enforce
ICAT.003 | MUST | status | preserve_known_estimated_provider_reported_and_unknown_status | enforce
ICAT.004 | MUST | modules | keep_deliveryyield_measurement_only_and_preserve_active_modules | enforce
ICAT.005 | MUST | token | optimize_quality_adjusted_output_per_token_cost | enforce
ICAT.006 | SHOULD | prompt | keep_rules_and_output_contract_in_stable_prefix | prefer
ICAT.007 | NEVER | metric | treat_adoption_pr_count_code_volume_or_agent_activity_as_final_value | block
ICAT.008 | NEVER | authority | orchestrate_coding_agents_or_approve_delivery | block

## Verification
- Every cost claim has evidence status.
- Results are feature-level, not activity-level.
- DeliveryYield does not orchestrate or approve.
- Recommendations preserve quality and active module boundaries.

## Failure Modes
- Using adoption rate as the primary outcome.
- Rewarding low token use that degrades quality.
- Treating PR count or agent activity as delivered value.
