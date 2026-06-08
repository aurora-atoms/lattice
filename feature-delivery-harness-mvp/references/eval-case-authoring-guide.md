# Eval Case Authoring Guide

Use synthetic examples only. Each eval directory contains `input.jsonl` and `expected.json`; valid dossier cases may also contain `expected_dossier.md`.

```text
good_feature_case_001       | valid end-to-end feature_delivery_case loop
vague_spec_case_001         | missing outcome, acceptance, non-goals, validation, or bounded scope
oversized_context_case_001  | raw context or excessive scope/token budget
failed_delivery_case_001    | tests pass while acceptance or usability fails
missing_evidence_case_001   | acceptance criterion lacks validation or delivery evidence
dangling_evidence_ref_case_001 | evidence_refs item does not resolve to record id or declared external ref
promotion_candidate_no_auto_case_001 | promoted candidate lacks approved promotion.review
```
