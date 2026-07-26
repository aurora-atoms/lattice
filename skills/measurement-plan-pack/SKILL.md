---
name: measurement-plan-pack
description: Use to turn a feature goal into a scoped measurement plan with success criteria, leading and lagging indicators, instrumentation, data quality checks, observation windows, guardrails, decision thresholds, owners, and review rules. Input is a Feature Delivery Case, target outcome, affected users, workflow, assumptions, risks, release plan, existing telemetry, and data constraints; output is an evidence-linked measurement plan and instrumentation gap list. Do not use to invent business value, optimize a single vanity metric, bypass privacy or data governance, or automate product decisions; preserve behavior, validation boundaries, uncertainty, and accountable authority.
---

# Measurement Plan Pack

## Goal

Define before launch how the team will know whether the feature produced the intended outcome without creating incentives around one incomplete metric.

## Use When

Use during ticket refinement, implementation planning, release readiness, experimentation, or outcome review when success criteria and observable evidence are incomplete or ambiguous.

## Do Not Use When

Do not use to retrofit convenient metrics after results are known, collect unnecessary personal data, replace qualitative judgment, or declare success from a single leading indicator.

## Inputs

Require a Feature Delivery Case, intended user or business outcome, target cohort, workflow and expected behavior change, original assumptions, risks, release or rollout plan, existing telemetry, data definitions, privacy and governance constraints, and accountable owners.

## Outputs

Write by default to:

```text
artifacts/measurement-plans/<case-id>/<run-id>/measurement-plan.v1.json
artifacts/measurement-plans/<case-id>/<run-id>/plan.md
artifacts/capability-runs/measurement-plan-pack/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Include:

- outcome statement and success criteria;
- target cohort, baseline, comparison basis, and exclusions;
- leading indicators and their expected movement;
- lagging indicators and expected decision horizon;
- guardrail metrics for user harm, reliability, cost, support, security, and compliance;
- instrumentation events, fields, timing, source systems, and owners;
- metric definitions, units, aggregation, segmentation, and data quality checks;
- observation window, minimum exposure, and freshness requirement;
- decision rules and thresholds for continue, adjust, expand, pause, stop, or insufficient evidence;
- qualitative feedback channels and review cadence;
- known measurement gaps, privacy constraints, and unresolved questions.

## Evidence

Separate facts from inference. Record uncertainty, unknown baselines, assumptions, conflicting metric definitions, source dates, data lineage, and applicability scope. A metric proxy must be labeled as a proxy. Instrumentation availability is not proof that the metric is meaningful.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- each metric maps to the intended outcome, a material assumption, or a guardrail;
- leading and lagging indicators are distinguished;
- success and failure can be interpreted without moving the goalposts;
- instrumentation, owner, timing, and data quality checks are explicit;
- privacy and governance constraints are respected;
- decision rules allow `insufficient_evidence` and preserve human authority.

## Stop Conditions

Stop when the requested measurement plan or next reviewable stage is complete. Stop for missing permission, undefined outcome, unavailable baseline, unresolved privacy or data-governance boundaries, unreliable telemetry, absent owners, or a product measurement decision. State the missing definition, evidence, or approval and the smallest next step.

## Workflow

1. Bound the Feature Delivery Case, outcome, cohort, release path, and decision authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Translate the intended outcome and assumptions into observable claims.
4. Select the smallest sufficient set of leading, lagging, guardrail, cost, and qualitative signals.
5. Define instrumentation, metric semantics, data quality, segmentation, windows, and ownership.
6. Write decision rules before outcome data is observed.
7. Produce the plan and instrumentation gaps; stop for owner and governance confirmation.

## Rules

MPP.001 | MUST | outcome | link every metric to an outcome assumption or guardrail
MPP.002 | MUST | definitions | define metric semantics baseline cohort unit and aggregation
MPP.003 | MUST | instrumentation | state event fields source timing quality checks and owner
MPP.004 | MUST | window | define minimum exposure observation window and freshness
MPP.005 | MUST | decisions | define review rules including insufficient evidence
MPP.006 | MUST | privacy | minimize data and preserve privacy governance boundaries
MPP.007 | SHOULD | balance | combine leading lagging guardrail cost and qualitative signals
MPP.008 | SHOULD | token | optimize quality-adjusted token ROI after measurement fidelity passes
MPP.009 | SHOULD | prompt | keep rules and output contract in a stable prefix
MPP.010 | NEVER | vanity | optimize or declare success from one vanity metric
MPP.011 | NEVER | authority | automate final product decisions

## Verification

- Outcome, indicators, guardrails, instrumentation, windows, owners, and decision rules are explicit.
- Metric definitions are stable and source-linked.
- Privacy, quality, and missing-data behavior are specified.
- The plan can support a later Feature Outcome Review without redefining success.

## Failure Modes

- choosing metrics because they already exist;
- measuring activity rather than user outcome;
- omitting guardrails or costs;
- defining thresholds after seeing results;
- collecting data without a decision use.
