---
name: knowledge-trust-assessor
description: Use to assess whether an internal knowledge claim is current, evidence-backed, consistent with code and runtime behavior, expert-validated, and applicable to the present task. Input is a bounded claim or knowledge asset, source metadata, code and test evidence, validation history, owners, scope, dates, and conflicts; output is a transparent trust assessment with factor-level evidence, last validation time, applicability, conflicts, gaps, and recommended validation. Do not use a black-box score, infer authority from seniority, or promote uncertain material to truth; preserve behavior, provenance, uncertainty, and human review authority.
---

# Knowledge Trust Assessor

## Goal

Help the team decide what internal knowledge is safe to rely on, why, and within which scope.

## Use When

Use when documentation, decisions, examples, runbooks, design notes, or team knowledge may be stale, inconsistent with implementation, unverified by an accountable expert, or valid only for a narrower scope than the current task.

## Do Not Use When

Do not use to approve source authority policy, replace domain-owner validation, or collapse trust into an unexplained numeric score.

## Inputs

Require a bounded claim or asset, source and owner metadata, creation and update dates, applicability scope, code and runtime evidence, test evidence, expert validation, conflicts, and intended use.

## Outputs

Produce:

```text
artifacts/knowledge-trust/<asset-id>/<run-id>/trust-assessment.v1.json
artifacts/knowledge-trust/<asset-id>/<run-id>/assessment.md
artifacts/capability-runs/knowledge-trust-assessor/<run-id>/run-result.json
```

Assess these factors separately:

- source authority and ownership;
- recency and last meaningful validation;
- consistency with code, tests, configuration, and observed behavior;
- expert or accountable-owner confirmation;
- evidence quality and reproducibility;
- applicability scope, environment, version, and exceptions;
- conflicts, superseding records, and unresolved unknowns.

Return status as `trusted_for_scope`, `conditionally_trusted`, `needs_validation`, `conflicted`, `superseded`, or `insufficient_evidence`, plus the exact scope and validation recommendation.

## Evidence

Every factor must cite evidence or explicitly state `not_evaluated`. Modified time alone does not prove freshness. Code consistency does not prove business correctness. Expert confirmation does not override contradictory runtime evidence without adjudication.

## Success Signals

Evaluate as `met`, `not_met`, or `not_evaluated`:

- trust is decomposed into visible factors;
- last meaningful validation is distinguished from last edit time;
- code, tests, runtime, and expert evidence are compared;
- applicability and exclusions are explicit;
- conflicts and unknowns remain visible;
- the recommended validation is concrete and owned.

## Stop Conditions

Stop at a reviewable trust assessment. Stop when source identity, intended use, scope, or essential evidence is unavailable; when authority conflicts require adjudication; or when one corrective retry fails.

## Workflow

1. Bound the claim, intended use, scope, and evidence cutoff.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted sources.
3. Gather authority, recency, implementation, validation, and applicability evidence.
4. Evaluate each factor independently.
5. Record conflicts, gaps, and superseding candidates.
6. Assign a scoped status and concrete validation path.
7. Stop for owner review.

## Rules

KTA.001 | MUST | factors | expose authority recency implementation validation applicability and conflict factors
KTA.002 | MUST | evidence | cite evidence or mark each factor not evaluated
KTA.003 | MUST | scope | bind trust status to version environment and intended use
KTA.004 | MUST | time | distinguish last edit from last meaningful validation
KTA.005 | MUST | validation | recommend a concrete validation method owner and deadline
KTA.006 | SHOULD | token | optimize quality-adjusted token ROI after factor coverage passes
KTA.007 | SHOULD | prompt | keep trust factors stable and evidence dynamic
KTA.008 | NEVER | score | use an unexplained aggregate score as the conclusion
KTA.009 | NEVER | authority | infer truth from seniority popularity or document location alone
KTA.010 | NEVER | promotion | promote conflicted or insufficient evidence into active truth

## Verification

- Every trust factor has evidence or an explicit evaluation gap.
- Status includes exact applicability.
- Conflicts, owner, validation method, and deadline are present.

## Failure Modes

- treating recency as trust;
- treating code as the only truth;
- hiding conflicts behind a score;
- omitting environment or version scope;
- recommending validation without an owner or evidence threshold.
