# P1 Evidence And Context-Pack Hardening

Status: implemented acceptance candidate.

```text
scope:
  context_pack JSONL record
  promotion.candidate JSONL record
  promotion.review JSONL record
  bounded context pack builder
  acceptance evidence completeness checker
  evidence_refs resolution checker
  manual-only promotion boundary checker

new_record_types:
  context_pack              | lat.context_pack.v1
  promotion.candidate       | lat.promotion.candidate.v1
  promotion.review          | lat.promotion.review.v1

new_scripts:
  build_context_pack.py
  check_evidence_completeness.py

new_eval_cases:
  missing_evidence_case_001
  dangling_evidence_ref_case_001
  promotion_candidate_no_auto_case_001

hardening_rules:
  every acceptance criterion has validation.result or delivery.evidence coverage
  every evidence_refs item resolves to a record id or declared external ref
  promotion.candidate cannot be promoted without approved promotion.review
  context_pack contains projected summaries only, never raw source dumps
```

Passing acceptance commands:

```text
python feature-delivery-harness-mvp\scripts\validate_contract_alignment.py
python feature-delivery-harness-mvp\scripts\run_mvp_evals.py
python feature-delivery-harness-mvp\scripts\build_context_pack.py feature-delivery-harness-mvp\evals\good_feature_case_001\input.jsonl --out feature-delivery-harness-mvp\reports\generated\good_feature_case_001.context_pack.jsonl
python feature-delivery-harness-mvp\scripts\validate_jsonl.py feature-delivery-harness-mvp\reports\generated\good_feature_case_001.context_pack.jsonl
python scripts\validate_skill_package.py --root skills
```

Expected-failure spot checks:

```text
check_evidence_completeness.py missing_evidence_case_001 -> MISSING_EVIDENCE_FOR_ACCEPTANCE
check_evidence_completeness.py dangling_evidence_ref_case_001 -> DANGLING_EVIDENCE_REF
check_evidence_completeness.py promotion_candidate_no_auto_case_001 -> AUTO_PROMOTION_FORBIDDEN
```
