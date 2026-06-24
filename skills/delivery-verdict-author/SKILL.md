---
name: delivery-verdict-author
description: "Assess user-usable delivery from feature spec, task packet, validation.result, delivery.evidence, implementation summary, defect, and risk input records while preserving evidence bounds, safety, and token ROI. Use for delivery_verdict.md, lat.delivery.verdict.v1, or bounded delivery.evidence updates. Do not use for token economics approval, coding, PR approval, merge, release, model routing, raw logs, or overriding verifier evidence. Output verdict enum usable/not_user_usable/requires_human_review/insufficient_evidence/blocked; query ConPort before full skill text when inventory exists."
---

# Delivery Verdict Author

## Goal

Assess whether a feature delivery case is user-usable from bounded evidence.

## Use When

```text
feature spec + task packet + validation.result + delivery.evidence -> delivery.verdict
tests pass, acceptance unclear -> insufficient_evidence or requires_human_review
acceptance failed -> not_user_usable
blocked dependency -> blocked
```

## Do Not Use When

```text
token economics approval
coding or patch execution
PR approval, merge, release, deploy
raw log, trace, PR diff ingestion
overriding verifier or human evidence
```

## Inputs

```text
feature spec
task packet
validation.result records
delivery.evidence records
implementation summary
known defects
unresolved risks
```

## Outputs

```text
delivery_verdict.md
lat.delivery.verdict.v1 JSONL
lat.delivery.evidence.v1 updates when applicable
verdict enum: usable | not_user_usable | requires_human_review | insufficient_evidence | blocked
```

## Workflow

1. Query ConPort before loading or searching full skill text when inventory exists.
2. Compare acceptance criteria to validation and delivery evidence.
3. Treat PR merged or tests passed as insufficient by itself.
4. Mark missing evidence as `insufficient_evidence`.
5. Emit `delivery.verdict` when machine-readable downstream routing needs an explicit verdict.
6. Never use token economics to approve or override delivery.

## Rules

```text
DVA.001 | MUST  | evidence | cite bounded evidence refs
DVA.002 | NEVER | verdict  | treat tests passed or PR merged as sufficient alone
DVA.003 | MUST  | missing  | missing evidence -> insufficient_evidence
DVA.004 | NEVER | role     | token economics approves delivery
DVA.005 | MUST  | tokens   | optimize quality-adjusted token ROI, not blind minimization
DVA.006 | MUST  | prompt   | keep stable prefix; put variable evidence in suffix
DVA.007 | MUST  | conflict | tests pass + acceptance fail -> not_user_usable
DVA.008 | MUST  | missing  | missing manual acceptance -> insufficient_evidence
DVA.009 | MUST  | blocked  | blocked dependency -> blocked
```

## Verification

```text
python3.14 ../../feature-delivery-harness-mvp/scripts/validate_jsonl.py <delivery-evidence.jsonl>
python3.14 ../../feature-delivery-harness-mvp/scripts/author_delivery_verdict.py <input.jsonl> --out <delivery-verdict.jsonl>
python3.14 ../../feature-delivery-harness-mvp/scripts/validate_jsonl.py <delivery-verdict.jsonl>
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
- `../../feature-delivery-harness-mvp/schemas/records/delivery.verdict.v1.schema.json`
