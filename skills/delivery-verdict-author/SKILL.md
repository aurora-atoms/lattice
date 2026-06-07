---
name: delivery-verdict-author
description: "Assess user-usable delivery from feature spec, task packet, validation.result, delivery.evidence, implementation summary, defect, and risk input records while preserving evidence boundaries, safety constraints, and quality-adjusted token ROI. Use for writing delivery_verdict.md or bounded delivery.evidence updates. Do not use for token economics approval, coding, PR approval, merge, release, model routing, raw logs, or overriding verifier evidence. Output verdict vocabulary usable/not_user_usable/requires_human_review/insufficient_evidence/blocked; query ConPort before loading or searching full skill text when inventory exists."
---

# Delivery Verdict Author

## Goal

Assess whether a feature delivery case is user-usable from bounded evidence.

## Use When

```text
feature_spec + task_packet + validation_results + delivery_evidence -> delivery_verdict
tests_pass_but_acceptance_unclear -> insufficient_evidence_or_requires_human_review
acceptance_failed -> not_user_usable
```

## Do Not Use When

```text
token_economics_approval
coding_or_patch_execution
PR_approval_merge_release_deploy
raw_log_trace_pr_diff_ingestion
overriding_verifier_or_human_evidence
```

## Inputs

```text
feature_spec
task_packet
validation.result records
delivery.evidence records
implementation summary
known defects
unresolved risks
```

## Outputs

```text
delivery_verdict.md
lat.delivery.evidence.v1 updates when applicable
verdict: usable | not_user_usable | requires_human_review | insufficient_evidence | blocked
```

## Workflow

1. Query ConPort before loading or searching full skill text when inventory exists.
2. Compare acceptance criteria to validation and delivery evidence.
3. Treat PR merged or tests passed as insufficient by itself.
4. Mark missing evidence as `insufficient_evidence`.
5. Never use token economics to approve or override delivery.

## Rules

```text
DVA.001 | MUST  | evidence | verdict_cites_bounded_evidence_refs | enforce
DVA.002 | NEVER | verdict  | tests_passed_or_PR_merged_is_sufficient_alone | block
DVA.003 | MUST  | missing  | missing_evidence_means_insufficient_evidence | enforce
DVA.004 | NEVER | role     | token_economics_approves_delivery | block
DVA.005 | MUST  | tokens   | optimize_quality_adjusted_token_ROI_not_blind_minimization | enforce
DVA.006 | MUST  | prompt   | keep stable prefix and put variable evidence in suffix | enforce
```

## Verification

```text
python ../../feature-delivery-harness-mvp/scripts/validate_jsonl.py <delivery-evidence.jsonl>
```

## Failure Modes

```text
insufficient_evidence
conflicting_evidence
acceptance_failed
blocked_dependency
raw_context_forbidden
review_needed
```

## References

- `references/delivery-verdict-rubric.md`
- `../../feature-delivery-harness-mvp/references/evidence-taxonomy.md`
- `../../feature-delivery-harness-mvp/schemas/records/delivery.evidence.v1.schema.json`
