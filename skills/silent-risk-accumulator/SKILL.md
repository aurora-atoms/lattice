---
name: silent-risk-accumulator
description: Use to detect when individually tolerable exceptions, skipped tests, deferred decisions, expired assumptions, architecture drift, manual workarounds, and unresolved risks combine into a materially larger delivery exposure. Input is a bounded Delivery Case, risk and exception records, test gaps, assumptions, drift evidence, deadlines, owners, mitigations, and change history; output is an evidence-linked risk-combination map with interaction paths, threshold conditions, leverage ranking, and minimum pressure-relief actions. Do not use black-box scoring, fear language, personnel blame, or automatic blocking; preserve behavior, validation boundaries, uncertainty, and human risk authority.
---

# Silent Risk Accumulator

## Goal

Expose risk created by interaction and accumulation before a single obvious red alert appears.

## Use When

Use when several temporary exceptions, skipped validations, deferred actions, fragile dependencies, or unverified assumptions remain open across a bounded delivery and may amplify one another.

## Do Not Use When

Do not use to aggregate unrelated risks, rank teams or people, manufacture urgency from count alone, or replace formal risk acceptance and release authority.

## Inputs

Require the bounded case, current stage and next gate, active risks and exceptions, skipped or missing tests, assumptions, architecture or dependency drift, mitigation state, owners, deadlines, historical outcomes, and the authorized evidence boundary.

## Outputs

Write by default to:

```text
artifacts/silent-risk/<case-id>/<run-id>/risk-combination.v1.json
artifacts/silent-risk/<case-id>/<run-id>/review.md
artifacts/capability-runs/silent-risk-accumulator/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Include:

- atomic risk components and their evidence;
- interaction edges and plausible amplification mechanisms;
- threshold or trigger conditions;
- affected outcomes and delivery gates;
- reversibility, time sensitivity, and observability;
- leverage ranking based on how many material paths one action reduces;
- minimum pressure-relief action, owner, deadline, and validation;
- accepted residual risk and reopen conditions.

## Evidence

Separate facts from inference. Record uncertainty, unknown interactions, assumptions, conflicting evidence, source dates, and applicability scope. Counts, age, or model confidence alone do not establish cumulative materiality.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- each combination is traceable to concrete components and interaction evidence;
- interaction effects are visible rather than hidden in one score;
- the highest-leverage few actions are distinguishable from broad cleanup;
- proposed actions are minimal, owned, and verifiable;
- accepted residual risk has monitoring and reopen conditions;
- accountable humans retain blocking and risk-acceptance authority.

## Stop Conditions

Stop when the requested risk-combination map or next reviewable stage is complete. Stop for missing permission, insufficient evidence, unavailable owners, unresolved security, privacy, compliance, safety, or production-risk boundaries, conflicting signals requiring human judgment, or scope expansion. State the missing item and smallest next step.

## Workflow

1. Bound the case, stage, gate, evidence window, and risk authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Normalize atomic exceptions, gaps, assumptions, and deferred actions.
4. Map interaction paths and threshold conditions without collapsing them into a black-box score.
5. Rank actions by material paths reduced, urgency, reversibility, and evidence strength.
6. Recommend the smallest pressure-relief set and stop for owner review.

## Rules

SRA.001 | MUST | composition | show atomic risks and explicit interaction paths
SRA.002 | MUST | evidence | link every material combination to sources and affected outcomes
SRA.003 | MUST | leverage | rank actions by material exposure reduced rather than activity volume
SRA.004 | MUST | threshold | state trigger conditions and latest-safe action time
SRA.005 | MUST | authority | preserve human blocking and risk-acceptance authority
SRA.006 | SHOULD | action | prefer the smallest set that reduces several material paths
SRA.007 | SHOULD | token | optimize quality-adjusted token ROI after risk fidelity passes
SRA.008 | SHOULD | prompt | keep combination rules stable and case evidence dynamic
SRA.009 | NEVER | score | hide composition behind an unexplained aggregate score
SRA.010 | NEVER | blame | attribute systemic accumulation to personnel performance

## Verification

- Every combination identifies components, interactions, evidence, impact, and owner.
- Leverage ranking is explainable without false numeric precision.
- Minimum actions have validation and reopen conditions.
- Unrelated risks remain separate.

## Failure Modes

- counting open items and calling the count risk;
- treating every exception as equally important;
- proposing a large cleanup instead of a small pressure-relief action;
- hiding uncertainty behind a severity score;
- using the report to blame the team that recorded the risk.
