---
name: risk-ahead
description: Use to select the smallest sufficient specialist for hidden dependencies, accumulated silent risk, compliance preflight, rework early warning, or stakeholder surprise. Input is a bounded Delivery Case or change, stage and next gate, dependencies, waits, exceptions, skipped tests, assumptions, policies, stakeholders, owners, deadlines, and evidence; output is a routing decision plus one evidence-linked preventive artifact. Do not use for personnel surveillance, black-box risk scoring, unsupported escalation, or automatic legal, compliance, security, architecture, release, or risk rulings; preserve behavior, privacy, least privilege, uncertainty, and human authority.
---

# Risk Ahead

## Goal

Route a latent delivery exposure to the smallest specialist that can reveal a high-leverage preventive action before the risk becomes expensive or blocking.

## Use When

Select one primary capability first:

- D01 `shadow-dependency-map`: hidden approvals, expertise, access, environment, vendor, operational, and coordination waits;
- D02 `silent-risk-accumulator`: interacting exceptions, test gaps, assumptions, drift, and deferred actions;
- D03 `compliance-preflight`: early security, privacy, legal, regulatory, audit, data-governance, regional, payment, and customer-commitment review needs;
- D04 `rework-early-warning`: unresolved convergence gaps likely to invalidate additional work;
- D05 `stakeholder-surprise-detector`: accountable roles that need minimal early involvement.

## Do Not Use When

Do not use for broad fear scoring, personnel monitoring, automatic escalation, generic checklists, final control-function rulings, or activating all five specialists without a named evidence gap.

## Inputs

Require a bounded target, current stage and next gate, intended outcome, dependencies and ownership boundaries, exceptions and skipped validations, assumptions, applicable policies, affected roles, deadlines, authority boundary, and evidence cutoff.

## Outputs

Write by default to:

```text
artifacts/risk-ahead/<case-id>/<run-id>/risk-ahead-selection.v1.json
artifacts/risk-ahead/<case-id>/<run-id>/summary.md
artifacts/capability-runs/risk-ahead/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

The selection records the chosen specialist, trigger evidence, required inputs, gaps, excluded alternatives, expected artifact, optional dependencies, human authority, and stop boundary.

## Evidence

Separate facts from inference. State uncertainty, unknowns, assumptions, conflicts, source dates, observation window, applicability, and missing evidence explicitly. Risk counts, model confidence, communication volume, or age alone are not proof of material exposure.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- one smallest sufficient specialist is selected before composition;
- the risk is linked to a bounded outcome and commitment gate;
- system bottlenecks are separated from personnel blame;
- the preventive action is minimal, timely, owned, and verifiable;
- plausible specialist alternatives and sources are intentionally excluded;
- legal, compliance, security, privacy, architecture, release, and risk authority remains human-controlled.

## Stop Conditions

Stop when the requested specialist artifact or next reviewable stage is complete. Stop for missing permission, insufficient evidence, unavailable sources or owners, privacy, security, legal, compliance, data-governance, safety, production-risk, personnel-risk, or other high-risk boundaries, conflicting evidence, scope expansion, or required human judgment. State the missing item, accountable role, and smallest next step.

## Workflow

1. Bound the case, outcome, stage, gate, evidence window, and authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Compare the task against D01 through D05 and select one primary specialist.
4. Invoke the dedicated specialist.
5. Add another specialist only for a named dependency, interaction, control, or independent validation gap.
6. Record plausible capabilities and sources intentionally excluded.
7. Stop at the specialist artifact for accountable review.

## Rules

DCAT.001 | MUST | routing | select one primary capability before composition
DCAT.002 | MUST | specialist | use dedicated D01 through D05 Skills when available
DCAT.003 | MUST | evidence | expose sources interactions uncertainty and affected outcomes
DCAT.004 | MUST | scope | focus on system bottlenecks instead of personnel blame
DCAT.005 | MUST | leverage | prefer the smallest action that reduces material exposure
DCAT.006 | MUST | human | preserve accountable control and risk authority
DCAT.007 | SHOULD | token | optimize quality-adjusted token ROI after risk fidelity passes
DCAT.008 | SHOULD | prompt | keep routing rules stable and evidence dynamic
DCAT.009 | NEVER | scoring | hide risk composition behind a black-box score
DCAT.010 | NEVER | composition | activate several specialists because selection evidence is weak
DCAT.011 | NEVER | surveillance | rank monitor or infer performance of people
DCAT.012 | NEVER | authority | issue final legal compliance security release or risk decisions

## References

- Use `../shadow-dependency-map/SKILL.md`, `../silent-risk-accumulator/SKILL.md`, `../compliance-preflight/SKILL.md`, `../rework-early-warning/SKILL.md`, or `../stakeholder-surprise-detector/SKILL.md`.
- Route a focused authority request to `../decision-question-builder/SKILL.md` or the appropriate human-judgment capability.
- Route final readiness or release judgment to the relevant evidence and delivery-verdict capability.

## Verification

```bash
python scripts/validate_skill_package.py --root skills/risk-ahead
python scripts/validate_capability_context.py --root .
```

## Failure Modes

- retaining a category monolith instead of selecting a specialist;
- escalating speculation as fact;
- inviting every stakeholder by default;
- using a black-box risk score;
- confusing early warning with final authority;
- blaming a person for a systemic bottleneck.
