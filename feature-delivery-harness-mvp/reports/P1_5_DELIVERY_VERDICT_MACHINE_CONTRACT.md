# P1.5 Delivery Verdict Machine Contract

Status: implemented acceptance candidate.

```text
scope:
  delivery.verdict JSONL record
  deterministic delivery verdict authoring
  verdict JSONL validation in eval runner
  tests-pass-plus-acceptance-fail conflict handling
  missing manual acceptance conflict handling
  blocked dependency verdict handling

new_record_type:
  delivery.verdict | lat.delivery.verdict.v1

new_script:
  author_delivery_verdict.py

verdicts:
  usable
  not_user_usable
  requires_human_review
  insufficient_evidence
  blocked

conflict_codes:
  TESTS_PASS_ACCEPTANCE_FAIL
  MISSING_MANUAL_ACCEPTANCE
  BLOCKED_DEPENDENCY
```

Passing acceptance commands:

```text
python feature-delivery-harness-mvp\scripts\validate_contract_alignment.py
python feature-delivery-harness-mvp\scripts\run_mvp_evals.py
python feature-delivery-harness-mvp\scripts\author_delivery_verdict.py feature-delivery-harness-mvp\evals\failed_delivery_case_001\input.jsonl --out feature-delivery-harness-mvp\reports\generated\failed_delivery_case_001.delivery_verdict.jsonl
python feature-delivery-harness-mvp\scripts\validate_jsonl.py feature-delivery-harness-mvp\reports\generated\failed_delivery_case_001.delivery_verdict.jsonl
python scripts\validate_skill_package.py --root skills
```
