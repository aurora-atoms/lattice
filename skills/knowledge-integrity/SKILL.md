---
name: knowledge-integrity
description: Use for alignment receipts, contradiction detection, assumption-expiry review, knowledge trust scoring, decision half-life review, architecture drift analysis, and future-maintainer notes; do not use to make unilateral business, architecture, compliance, or ownership decisions; input is bounded requirements, designs, code, tests, documents, decisions, assumptions, owners, dates, and evidence references; output is a traceable integrity report containing conflicts, trust factors, expired assumptions, decisions needing review, architecture drift, concise maintenance intent, and required human adjudication while preserving uncertainty and quality-adjusted token ROI.
---

# Knowledge Integrity

## Goal
Make internal knowledge and decisions current, explainable, traceable, and explicitly bounded.

## Use When
Select the smallest sufficient atomic capability:
- C01 Alignment Receipt
- C02 Contradiction Finder
- C03 Assumption Expiry Radar
- C04 Knowledge Trust Score
- C05 Decision Half-Life Tracker
- C06 Architecture Drift Radar
- C07 Future Maintainer Note

## Do Not Use When
Do not use to unilaterally replace a decision, resolve business ownership, or issue final architecture or compliance rulings.

## Inputs
Use bounded requirements, designs, code, tests, documents, decisions, assumptions, owners, dates, and evidence references.

## Outputs
Return conflicts, trust factors, expired assumptions, decisions needing review, architecture drift, maintenance intent, owners, and human adjudication requests.

## Workflow
1. Identify the target knowledge or decision object.
2. Select one atomic capability first.
3. Compare sources, dates, owners, code state, and validation evidence.
4. Separate fact, inference, conflict, and unknown.
5. Request human adjudication where authority is required.

## Rules
CCAT.001 | MUST | scope | bind_analysis_to_versioned_source_and_scope | enforce
CCAT.002 | MUST | routing | select_one_atomic_capability_before_composing | enforce
CCAT.003 | MUST | evidence | expose_source_owner_date_scope_and_validation | enforce
CCAT.004 | MUST | uncertainty | separate_fact_inference_conflict_and_unknown | enforce
CCAT.005 | MUST | human | preserve_owner_or_governance_decision_authority | enforce
CCAT.006 | MUST | token | optimize_quality_adjusted_output_per_token_cost | enforce
CCAT.007 | SHOULD | prompt | keep_rules_and_output_contract_in_stable_prefix | prefer
CCAT.008 | NEVER | authority | silently_replace_decision_or_architecture_intent | block

## Verification
- Every conclusion has source, scope, status, and version context.
- Conflicts are identified rather than silently resolved.
- Review or expiry conditions are explicit.

## Failure Modes
- Using a black-box trust score.
- Treating historical decisions as permanent truth.
- Equating architecture drift with automatic failure.
