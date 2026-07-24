---
name: delivery-artifact-builder
description: Use to turn requirements, implementation evidence, reviews, tests, and release context into Ticket Ready, implementation-plan, reviewer-rehearsal, PR Ready, test-asset, delivery-readiness, and PR-to-release artifacts; do not use to commit scope or dates, approve merges/releases, fabricate test evidence, or replace accountable owners; input is a bounded Feature Delivery Case with requirements, context, diff, decisions, tests, risks, and release constraints; output is an editable evidence-linked delivery artifact with gaps, validation steps, rollback or support notes, owners, and human confirmations while preserving behavioral constraints, facts, inference boundaries, and quality-adjusted token ROI.
---

# Delivery Artifact Builder

## Goal
Convert individual understanding into visible, actionable, auditable delivery artifacts.

## Use When
Select the smallest sufficient atomic capability:
- E01 Ticket Ready Package
- E02 Implementation Plan / Ticket Decomposition
- E03 Reviewer Rehearsal
- E04 PR Ready Package
- E05 Test Asset Package
- E06 Delivery Readiness Card
- E07 PR-to-Release Summary

## Do Not Use When
Do not use to commit scope or dates, approve merge/release, or fabricate completion evidence.

## Inputs
Use a bounded Feature Delivery Case with requirements, context, diff, decisions, tests, risks, release constraints, and evidence references.

## Outputs
Return the requested editable artifact with objective, scope, acceptance, plan, tests, evidence, risks, rollback/support notes, gaps, owners, and confirmations.

## Workflow
1. Identify the lifecycle stage and requested artifact.
2. Query ConPort before loading or searching the full skill text when ConPort is available; otherwise use targeted source reads.
3. Select one atomic capability first.
4. Gather only source evidence required by the artifact.
5. Separate completed evidence from missing evidence.
6. Produce an editable package with explicit owner confirmations.
7. Stop before approval or commitment authority.

## Rules
ECAT.001 | MUST | routing | select one atomic artifact capability | enforce
ECAT.002 | MUST | evidence | distinguish verified evidence from missing or claimed evidence | enforce
ECAT.003 | MUST | artifact | make output editable, traceable, and actionable | enforce
ECAT.004 | MUST | human | preserve scope, date, merge, and release authority | enforce
ECAT.005 | MUST | token | optimize quality-adjusted token ROI | enforce
ECAT.006 | SHOULD | prompt | keep rules and the output contract in a stable prefix | prefer
ECAT.007 | NEVER | evidence | fabricate test results, readiness, or completion | block
ECAT.008 | NEVER | authority | approve merge, release, or scope commitment | block

## Verification
- The artifact matches the lifecycle stage.
- Evidence and gaps are explicit.
- Owners can edit and confirm the result.

## Failure Modes
- Turning generated text into an irreversible commitment.
- Using activity lists instead of delivery state.
- Claiming tests or readiness without evidence.
