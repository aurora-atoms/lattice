---
name: feature-spec-author
description: "Draft bounded feature specs and feature_delivery_case JSONL from synthetic or approved open requirements while preserving source refs, ambiguity, safety constraints, and quality-adjusted token ROI. Use for turning a raw requirement into a user-usable outcome, scope, non-goals, acceptance criteria, risks, evidence needs, and unresolved questions. Do not use for coding, full technical design, raw repo/Jira/log ingestion, company-derived examples, or delivery approval. Output feature_spec.md and lat.feature_delivery_case.v1 records; query ConPort before loading or searching full skill text when inventory exists."
---

# Feature Spec Author

## Goal

Produce bounded feature specs and `feature_delivery_case` JSONL records for the Feature Delivery Harness MVP.

## Use When

```text
raw_requirement -> bounded_feature_spec
synthetic_or_open_example -> feature_delivery_case
unclear_feature_request -> assumptions_and_unresolved_questions
```

## Do Not Use When

```text
coding_or_patch_execution
full_technical_design
delivery_approval
raw_repo_jira_log_trace_pr_dump_ingestion
company_derived_example_without_review
```

## Inputs

```text
raw requirement
user goal
constraints
source refs
explicit non-goals when available
```

## Outputs

```text
feature_spec.md
lat.feature_delivery_case.v1 JSONL draft
unresolved_questions
evidence_needed
```

## Workflow

1. Query ConPort before loading or searching full skill text when inventory exists.
2. Extract user-usable outcome, scope, non-goals, acceptance criteria, assumptions, risks, validation expectations, evidence needs, and unresolved questions.
3. Preserve source refs without copying raw dumps into model-visible context.
4. Mark ambiguity instead of inventing repo facts.
5. Emit a bounded `feature_delivery_case` record matching `../../feature-delivery-harness-mvp/schemas/records/feature_delivery_case.v1.schema.json`.

## Rules

```text
FSA.001 | MUST  | output | feature_delivery_case is primary value unit
FSA.002 | MUST  | quality | preserve behavior constraints + source refs
FSA.003 | MUST  | tokens | optimize quality-adjusted token ROI, not blind minimization
FSA.004 | NEVER | input  | include raw repo/Jira/log/trace/PR/CI dump
FSA.005 | NEVER | role   | write code or approve delivery
FSA.006 | MUST  | prompt | keep stable prefix and put variable requirement in suffix
```

## Verification

```text
python3.14 ../../feature-delivery-harness-mvp/scripts/validate_jsonl.py <feature-case.jsonl>
```

## Failure Modes

```text
vague_outcome
missing_acceptance_criteria
missing_non_goals
raw_context_forbidden
source_verification_needed
review_needed
```

## References

- `references/feature-spec-patterns.md`
- `../../feature-delivery-harness-mvp/instructions/kernel.rules.md`
- `../../feature-delivery-harness-mvp/schemas/records/feature_delivery_case.v1.schema.json`
