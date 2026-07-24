---
name: delivery-capability-strategy
description: Use to reframe AI-adoption requests into delivery-capability design and to connect AI token or cost evidence to visible user-usable feature delivery; do not use as a generic AI adoption campaign, activity dashboard, model competition, cost-minimization exercise, or runtime coding orchestrator; input is delivery goals, team pain points, available capabilities, Feature Delivery Cases, token or cost records with known, estimated, or provider-reported status, and outcome evidence; output is a capability strategy, Token-to-Delivery view, waste hypothesis, next optimization signal, and manager-facing recommendation that preserves behavior, active module boundaries, and DeliveryYield measurement-only scope.
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
1. Query ConPort before loading or searching the full skill text when ConPort is available; otherwise use targeted source reads.
2. Reframe adoption or cost questions around user-usable delivery outcomes.
3. Select I01 or I02 first.
4. Bind evidence to Feature Delivery Cases.
5. Preserve known, estimated, provider-reported, and unknown status.
6. Identify waste without rewarding quality degradation.
7. Produce the next optimization or investment recommendation.

## Rules
ICAT.001 | MUST | outcome | use user-usable feature delivery as the primary value unit | enforce
ICAT.002 | MUST | evidence | bind token and cost to the Feature Delivery Case | enforce
ICAT.003 | MUST | status | preserve known, estimated, provider-reported, and unknown status | enforce
ICAT.004 | MUST | modules | keep DeliveryYield measurement-only and preserve active modules | enforce
ICAT.005 | MUST | token | optimize quality-adjusted token ROI | enforce
ICAT.006 | SHOULD | prompt | keep rules and the output contract in a stable prefix | prefer
ICAT.007 | NEVER | metric | treat adoption, PR count, code volume, or agent activity as final value | block
ICAT.008 | NEVER | authority | orchestrate coding agents or approve delivery | block

## Verification
- Every cost claim has evidence status.
- Results are feature-level, not activity-level.
- DeliveryYield does not orchestrate or approve.
- Recommendations preserve quality and active module boundaries.

## Failure Modes
- Using adoption rate as the primary outcome.
- Rewarding low token use that degrades quality.
- Treating PR count or agent activity as delivered value.
