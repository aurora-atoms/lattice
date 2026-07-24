---
name: risk-ahead
description: Use for shadow dependency mapping, accumulated silent-risk analysis, compliance pre-flight, rework early warning, and stakeholder-surprise detection; do not use for personnel surveillance, automatic compliance rulings, broad fear scoring, or escalation without evidence; input is a bounded change, dependencies, waits, exceptions, skipped tests, assumptions, policies, stakeholders, and historical review evidence; output is a compositional risk packet with evidence, interaction effects, threshold conditions, minimum preventive actions, owners, deadlines, and human escalation points that preserves least privilege and quality-adjusted token ROI.
---

# Risk Ahead

## Goal
Expose hidden technical, organizational, compliance, and coordination risks while they are still cheap to address.

## Use When
Select the smallest sufficient atomic capability:
- D01 Shadow Dependency Map
- D02 Silent Risk Accumulator
- D03 Compliance Pre-Flight
- D04 Rework Early Warning
- D05 Stakeholder Surprise Detector

## Do Not Use When
Do not use for personnel monitoring, automatic legal/compliance rulings, or unsupported risk escalation.

## Inputs
Use a bounded change, dependency and wait evidence, exceptions, skipped tests, assumptions, policies, stakeholders, and historical review records.

## Outputs
Return hidden dependencies, interacting risks, pre-flight evidence requirements, rework drivers, stakeholder notice needs, owners, deadlines, and minimum preventive actions.

## Workflow
1. Bound the change and affected Delivery Case.
2. Select one atomic capability first.
3. Gather evidence for dependencies, exceptions, and exposure.
4. Model interaction effects without hiding composition.
5. Recommend the smallest preventive action.
6. Escalate only evidence-backed risk requiring human authority.

## Rules
DCAT.001 | MUST | routing | select_one_atomic_capability_before_composing | enforce
DCAT.002 | MUST | evidence | expose_risk_components_and_interactions | enforce
DCAT.003 | MUST | scope | focus_on_system_bottlenecks_not_personnel_blame | enforce
DCAT.004 | MUST | human | reserve_compliance_legal_and_business_judgment_for_owners | enforce
DCAT.005 | MUST | token | optimize_quality_adjusted_output_per_token_cost | enforce
DCAT.006 | SHOULD | prompt | keep_rules_and_output_contract_in_stable_prefix | prefer
DCAT.007 | NEVER | scoring | use_black_box_risk_score_without_composition | block
DCAT.008 | NEVER | surveillance | rank_or_monitor_people | block

## Verification
- Each risk has evidence, scope, interaction, and owner.
- The proposed action is minimal and timely.
- Final compliance or legal judgment remains human-controlled.

## Failure Modes
- Producing context-free risk scores.
- Inviting every stakeholder by default.
- Escalating speculation as fact.
