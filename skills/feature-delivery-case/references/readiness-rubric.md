# Readiness Rubric

## Result Enum

Use exactly one result:

- `ready`: all mandatory criteria are supported by current evidence and no blocker remains.
- `not_ready`: one or more remediable criteria fail.
- `blocked`: an external dependency, authority, permission, or unresolved condition prevents progress.
- `insufficient_evidence`: the result cannot be determined from bounded evidence.
- `human_decision_required`: evidence is available, but an accountable judgment or approval is required.

Do not use confidence language such as probably, mostly, seems, nearly, or likely ready as the result.

## Universal Ready Gate

A `ready` result requires:

1. purpose, beneficiary, expected change, scope, non-goals, and acceptance are explicit;
2. context coverage is complete or explicitly not applicable;
3. active decisions and assumptions are current and reviewable;
4. no expired active assumption exists;
5. no blocking dependency is unsatisfied;
6. no blocking unresolved item remains open;
7. readiness criteria all pass;
8. evidence refs are current and traceable;
9. direct and compound risks have owners and acceptable controls;
10. the target artifact exists;
11. readiness has an expiry or event-based review trigger;
12. the authority note preserves accountable approval.

## Target Gates

### Ready for refinement

Require a readiness card, user outcome, affected users, initial boundary, context gaps, decision owners, and unresolved questions.

### Ready for implementation

Require a Jira or implementation-ready artifact, bounded scope, acceptance criteria, technical and shadow dependencies, decision and assumption state, target surfaces, validation plan, and risk controls.

### Ready for test

Require a test handoff, implemented-scope reference, acceptance-to-test mapping, environment and data dependencies, known limitations, negative tests, observability expectations, and unresolved defect state.

### Ready for review

Require a PR readiness artifact, diff or implementation summary reference, acceptance mapping, tests and validation evidence, decision deviations, security or compatibility review needs, and known risks.

### Ready for merge

Require a PR readiness artifact, current review evidence, required checks, acceptance evidence, unresolved comment state, known defect and risk state, migration or rollback notes when applicable, and no expired readiness evidence.

A ready-for-merge result is not approval to merge.

### Ready for deployment

Require a deployment handoff, merge or build artifact refs, environment and configuration dependencies, migration and rollback plan, monitoring and alert expectations, operational ownership, change-window constraints, and deployment-specific risk controls.

### Ready for release

Require a release summary, deployment evidence, user-visible behavior summary, support and rollback information, metrics or observation plan, known limitations, stakeholder communication, and release-specific approvals identified as human decisions.

### Ready for next step

Require a readiness card that names the exact next step, owner, entry criteria, output expected, evidence supplied, blockers, expiry, and review triggers.

## Re-evaluation Triggers

Invalidate or re-evaluate readiness when:

- scope or acceptance changes;
- a decision is reversed or superseded;
- an assumption expires or is invalidated;
- a dependency changes state;
- new contradictory evidence appears;
- tests, reviews, metrics, or validations become stale;
- risk exposure increases or controls change;
- target environment, release window, policy, or accountable owner changes.
