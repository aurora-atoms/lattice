---
name: contradiction-adjudication
description: Use to find and frame contradictions across requirements, documents, code, tests, configurations, decisions, and operational evidence. Input is a bounded claim or topic, candidate sources, source authority, versions, scope, owners, and observation dates; output is an evidence-linked contradiction set containing the conflicting pair, affected behavior, source provenance, impact, required adjudicator, and recommended single source of truth. Do not use to silently choose a winner, flatten legitimate scope differences, or replace owner authority; preserve behavior, evidence, uncertainty, and human adjudication.
---

# Contradiction Adjudication

## Goal

Turn “both sources look correct” into a bounded contradiction that an accountable owner can resolve without losing scope, version, or evidence context.

## Use When

Use when requirements, code, tests, documentation, configuration, runbooks, decisions, or operational behavior disagree and the disagreement can affect implementation, validation, support, or user outcomes.

## Do Not Use When

Do not use when differences are explained by version, environment, audience, or scope; when no material behavior is affected; or when the task requires unilateral architecture, business, compliance, or ownership judgment.

## Inputs

Require the bounded claim, conflicting sources, source types, versions or observation dates, applicability scopes, authority metadata, affected behavior, and likely adjudicating role.

## Outputs

Produce:

```text
artifacts/contradictions/<conflict-id>/<run-id>/contradiction-set.v1.json
artifacts/contradictions/<conflict-id>/<run-id>/review.md
artifacts/capability-runs/contradiction-adjudication/<run-id>/run-result.json
```

Each contradiction record states:

- normalized claim A and claim B;
- exact source references, versions, dates, and scopes;
- whether the conflict is semantic, behavioral, temporal, environmental, ownership, or authority-related;
- affected systems, users, decisions, tests, controls, or delivery gates;
- evidence supporting each side;
- whether both can be valid under different scopes;
- impact if unresolved;
- required adjudicator and why that role is authoritative;
- candidate single source of truth and migration implications;
- resolution status, decision deadline, and follow-up validation.

## Evidence

Preserve both sides fairly. Separate source facts, interpretation, conflict, uncertainty, and unknowns. Runtime behavior may disprove documentation but does not automatically define intended behavior. Formal policy may define intent but does not prove implementation compliance.

## Success Signals

Evaluate as `met`, `not_met`, or `not_evaluated`:

- the conflict is represented as a precise pair rather than a vague inconsistency;
- scope and version differences have been tested before declaring contradiction;
- affected behavior and impact are explicit;
- both positions retain evidence and uncertainty;
- an accountable adjudicator and deadline are named;
- the proposed single source of truth includes update and validation consequences.

## Stop Conditions

Stop at a reviewable contradiction set. Do not resolve the conflict or modify sources without explicit authority. Stop when source access, scope, authority, or evidence is insufficient, or when one bounded retry fails.

## Workflow

1. Bound the claim, sources, scope, versions, and affected behavior.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted reads.
3. Normalize each claim without erasing qualifiers.
4. Test whether environment, time, version, or scope explains the difference.
5. Record true contradiction pairs and their impact.
6. Identify the adjudicating role and candidate single source of truth.
7. Define source-update and validation actions after resolution.
8. Stop for human adjudication.

## Rules

CAD.001 | MUST | pair | represent each contradiction as two precise scoped claims
CAD.002 | MUST | provenance | preserve source version date authority and applicability
CAD.003 | MUST | impact | state affected behavior and consequence if unresolved
CAD.004 | MUST | fairness | preserve evidence and uncertainty for both sides
CAD.005 | MUST | authority | identify who must adjudicate and why
CAD.006 | MUST | truth | recommend one governed source of truth with migration steps
CAD.007 | SHOULD | token | optimize quality-adjusted token ROI after conflict fidelity passes
CAD.008 | SHOULD | prompt | keep comparison rules stable and source evidence dynamic
CAD.009 | NEVER | resolution | silently choose a winner or overwrite a source
CAD.010 | NEVER | flattening | treat legitimate scope or version differences as contradictions

## Verification

- Every conflict has two claims and two source references.
- Scope and version reconciliation was attempted.
- Impact, adjudicator, deadline, and post-resolution validation are present.

## Failure Modes

- declaring contradiction from wording alone;
- privileging code, documents, or seniority without authority analysis;
- hiding one side's evidence;
- recommending a source of truth without update ownership;
- resolving a disputed matter inside the analysis.
