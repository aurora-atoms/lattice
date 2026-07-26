---
name: architecture-drift-radar
description: Use to compare documented architecture intent with current code, configuration, dependencies, data flows, and runtime structure so cumulative local changes become visible before major refactoring or incidents. Input is bounded architecture intent, current implementation evidence, change history, constraints, owners, and observation dates; output is an evidence-linked drift report with patterns, impact, trend, affected boundaries, and options to accept, repair, or reset the architecture intent. Do not use to label all divergence as failure or automatically mandate refactoring; preserve behavior, provenance, uncertainty, and architecture-owner authority.
---

# Architecture Drift Radar

## Goal

Make cumulative divergence between intended architecture and real system structure visible early enough for deliberate action.

## Use When

Use during architecture review, repeated cross-system change, major refactoring preparation, incident analysis, platform migration, or when many individually reasonable changes may have altered system boundaries or control flow.

## Do Not Use When

Do not use when no authoritative design intent exists, when the difference is an approved evolution already reflected in current decisions, or to automatically classify all drift as technical debt or failure.

## Inputs

Require bounded architecture intent, current code and configuration evidence, runtime or dependency evidence where available, change history, affected systems, constraints, owner, and observation dates.

## Outputs

Produce:

```text
artifacts/architecture-drift/<scope-id>/<run-id>/architecture-drift.v1.json
artifacts/architecture-drift/<scope-id>/<run-id>/review.md
artifacts/capability-runs/architecture-drift-radar/<run-id>/run-result.json
```

Each drift record states:

- intended boundary, dependency, control, or flow;
- observed current structure;
- evidence for both intent and reality;
- drift pattern: boundary erosion, dependency inversion, duplicated authority, bypassed control, hidden coupling, data-flow divergence, ownership split, or operational workaround;
- accumulated change path where known;
- affected systems, users, controls, delivery speed, reliability, or maintainability;
- trend: stable, increasing, decreasing, episodic, or unknown;
- reversibility and urgency;
- options: accept and update intent, repair implementation, isolate the exception, or reset architecture intent;
- accountable owner, validation, and next review point.

## Evidence

Documented intent is not automatically current. Current code is not automatically correct. Compare versioned intent with implementation, tests, configuration, runtime evidence, and approved decisions. Separate observed divergence from inferred cause and projected impact.

## Success Signals

Evaluate as `met`, `not_met`, or `not_evaluated`:

- each drift item compares one precise intent with one observed reality;
- cumulative patterns are distinguished from isolated exceptions;
- impact and trend are evidence-linked;
- legitimate evolution can be accepted by updating intent;
- repair and reset options include consequences and validation;
- architecture authority remains human-controlled.

## Stop Conditions

Stop at a reviewable drift report. Do not refactor, redefine architecture, or approve exceptions without explicit authority. Stop when intent, implementation evidence, scope, or owner is missing; when source conflicts require adjudication; or when one bounded retry fails.

## Workflow

1. Bound the architecture surface, intent sources, implementation evidence, and observation time.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted sources.
3. Normalize intended boundaries, flows, dependencies, and controls.
4. Map current code, configuration, data flow, dependency, and runtime structure.
5. Identify divergence and distinguish approved evolution from unreviewed drift.
6. Group repeated items into drift patterns and trends.
7. Evaluate impact, reversibility, and options to accept, repair, isolate, or reset intent.
8. Stop for architecture-owner review.

## Rules

ADR.001 | MUST | comparison | pair versioned design intent with observed implementation evidence
ADR.002 | MUST | pattern | distinguish isolated exceptions from cumulative drift patterns
ADR.003 | MUST | impact | state affected boundaries outcomes and trend
ADR.004 | MUST | options | provide accept repair isolate and reset options where applicable
ADR.005 | MUST | authority | preserve architecture-owner authority over intent and remediation
ADR.006 | MUST | lifecycle | define validation owner and next review point
ADR.007 | SHOULD | token | optimize quality-adjusted token ROI after drift fidelity passes
ADR.008 | SHOULD | prompt | keep comparison rules stable and system evidence dynamic
ADR.009 | NEVER | divergence | equate every difference with failure or debt
ADR.010 | NEVER | remediation | mandate refactoring or rewrite intent without approval

## Verification

- Every drift record has intent and observed-state evidence.
- Approved evolution is separated from unresolved drift.
- Trend, impact, options, owner, and validation are present.

## Failure Modes

- comparing against outdated intent without warning;
- treating current code as self-justifying architecture;
- listing differences without cumulative patterns;
- recommending refactoring without an acceptance option;
- failing to identify who can reset architecture intent.
