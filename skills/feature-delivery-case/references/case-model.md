# Feature Delivery Case Model

## Purpose

A Feature Delivery Case is the durable record of user value, scope, context, choices, dependencies, evidence, uncertainty, risk, artifacts, and readiness for one bounded change.

It is not synonymous with a Jira ticket, PR, commit, CI run, release, or activity timeline. Those are evidence or linked artifacts.

## Required Lifecycle Sections

For `case_profile=lifecycle_v1`, maintain:

1. `purpose`: why, beneficiaries, expected change, and success signals.
2. `boundary`: feature boundary, affected surfaces, compatibility constraints, impact areas, and out-of-scope statements.
3. `context_coverage`: explicit coverage of business rules, system constraints, similar cases, negative knowledge, and source facts.
4. `decision_log`: append-only decision history with supersession status.
5. `assumption_log`: assumptions with basis, confidence, owner, validity, expiry, and review triggers.
6. `dependencies`: technical, shadow, data, operational, external, decision, and stakeholder dependencies.
7. `evidence_ledger`: tests, logs, reviews, metrics, validations, source facts, and manual acceptance.
8. `risk_ledger`: direct and compound risks, controls, owners, evidence, and review triggers.
9. `unresolved_items`: questions, decisions, missing evidence, waivers, and expired assumptions.
10. `artifacts`: shareable case, Jira, test, PR, readiness, deployment, release, or next-step artifacts.
11. `readiness`: one target and one explicit result at the current revision.

## History Semantics

Do not overwrite the historical reason for a choice. Mark prior entries `superseded`, `reversed`, `invalidated`, `expired`, or `waived` and link the newer entry.

A decision or assumption is incomplete without:

- creation or decision time;
- accountable person or role;
- rationale or basis;
- applicability conditions;
- evidence refs;
- time-based review date, event-based review triggers, or both.

## Dependency Semantics

A shadow dependency is a dependency not declared in the primary implementation plan but capable of changing delivery outcome, such as a shared schema consumer, undocumented operational step, data producer, security review, downstream report, support process, or stakeholder approval.

Record dependency state as `unknown`, `identified`, `pending`, `satisfied`, `waived`, `failed`, or `blocked`. A blocking dependency that is not satisfied or waived prevents readiness.

## Evidence Semantics

Evidence must be addressable and bounded. Record:

- `kind`;
- stable reference;
- what it supports or contradicts;
- result;
- observation time;
- freshness or expiry when relevant;
- confidence and source authority.

An assertion without evidence is a claim, not evidence.

## Risk Semantics

A compound risk exists when two or more individually tolerable conditions interact to create materially larger exposure. Link component risks, dependencies, assumptions, or timing conditions rather than describing only the final symptom.

## Artifact Semantics

Every artifact must include or link:

```text
feature_delivery_case_id
case_revision
artifact_id and kind
readiness target and result when applicable
evidence refs
blocking items and limitations
owner or accountable role
generated time
expiry or review trigger
authority note
```

## Readiness Authority

A `ready` result is an evidence-backed recommendation for the named next step. It is never merge, release, deployment, compliance, or business-scope approval. The accountable human or governed system retains authority.
