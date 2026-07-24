---
name: risk-ahead
description: Use for shadow dependency mapping, accumulated silent-risk analysis, compliance pre-flight, rework early warning, and stakeholder-surprise detection; do not use for personnel surveillance, automatic compliance rulings, broad fear scoring, or escalation without evidence; input is a bounded change, dependencies, waits, exceptions, skipped tests, assumptions, policies, stakeholders, and historical review evidence; output is a compositional risk packet with evidence, interaction effects, threshold conditions, minimum preventive actions, owners, deadlines, and human escalation points that preserves behavior, least privilege, and quality-adjusted token ROI.
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
2. Query ConPort before loading or searching the full skill text when ConPort is available; otherwise use targeted source reads.
3. Select one atomic capability first.
4. Gather evidence for dependencies, exceptions, and exposure.
5. Model interaction effects without hiding composition.
6. Recommend the smallest preventive action.
7. Escalate only evidence-backed risk requiring human authority.

## Rules
DCAT.001 | MUST | routing | select one atomic capability before composing | enforce
DCAT.002 | MUST | evidence | expose risk components and interactions | enforce
DCAT.003 | MUST | scope | focus on system bottlenecks instead of personnel blame | enforce
DCAT.004 | MUST | human | reserve compliance, legal, and business judgment for owners | enforce
DCAT.005 | MUST | token | optimize quality-adjusted token ROI | enforce
DCAT.006 | SHOULD | prompt | keep rules and the output contract in a stable prefix | prefer
DCAT.007 | NEVER | scoring | use a black-box risk score without composition | block
DCAT.008 | NEVER | surveillance | rank or monitor people | block

## Verification
- Each risk has evidence, scope, interaction, and owner.
- The proposed action is minimal and timely.
- Final compliance or legal judgment remains human-controlled.

## Failure Modes
- Producing context-free risk scores.
- Inviting every stakeholder by default.
- Escalating speculation as fact.
