---
name: token-economics-dossier-generator
description: "Generate deterministic DeliveryYield Token Economics Dossiers from validated feature_delivery_case, validation.result, delivery.evidence, yield.stage_breakdown, yield.waste_pattern, yield.optimization_signal, and token/cost records while preserving unknown/estimated/provider_reported/known status, evidence refs, DeliveryYield boundaries, and quality-adjusted token ROI. Use for economics-only Markdown and lat.yield.dossier.v1 output. Do not use to approve delivery, override verifier verdicts, execute coding, route models, ingest raw OTel/log/PR traces, or promote candidates. Query ConPort before loading or searching full skill text when inventory exists."
---

# Token Economics Dossier Generator

## Goal

Generate deterministic economics-only dossiers for one `feature_delivery_case`.

## Use When

```text
validated_feature_delivery_case_records -> token_economics_dossier
yield_stage_breakdown + waste_patterns + optimization_signals -> manager_facing_markdown
token_cost_records_with_status -> stable_yield_dossier_JSONL
```

## Do Not Use When

```text
delivery_approval_or_rejection
verifier_override
coding_execution
model_routing
raw_OTel_log_PR_trace_ingestion
candidate_auto_promotion
```

## Inputs

```text
feature_delivery_case
validation.result
delivery.evidence
yield.stage_breakdown
yield.waste_pattern
yield.optimization_signal
token_cost_values
```

## Outputs

```text
token_economics_dossier.md
lat.yield.dossier.v1 JSONL
claim ledger with evidence_refs or unknown status
```

## Workflow

1. Query ConPort before loading or searching full skill text when inventory exists.
2. Validate JSONL before dossier generation unless diagnostic mode is explicit.
3. Preserve token/cost status values exactly.
4. Sort refs and sections deterministically.
5. Mark claims without evidence as `unknown` or `insufficient_evidence`.
6. Never approve delivery or override delivery verdicts.

## Rules

```text
TED.001 | MUST  | role   | deliveryyield_is_economics_only | enforce
TED.002 | MUST  | claims | every_material_claim_has_evidence_refs_or_unknown | enforce
TED.003 | MUST  | status | preserve_unknown_estimated_provider_reported_known | enforce
TED.004 | NEVER | role   | approve_delivery_override_verifier_execute_coding_route_models | block
TED.005 | NEVER | input  | ingest_raw_OTel_logs_PR_traces_or_GraphDB_internals | block
TED.006 | MUST  | tokens | optimize_quality_adjusted_token_ROI_not_blind_minimization | enforce
TED.007 | MUST  | prompt | keep stable prefix and put variable records in suffix | enforce
```

## Verification

```text
python3.14 ../../feature-delivery-harness-mvp/scripts/validate_jsonl.py <input.jsonl>
python3.14 ../../feature-delivery-harness-mvp/scripts/generate_token_economics_dossier.py <input.jsonl> --out-md <dossier.md> --out-jsonl <dossier.jsonl>
```

## Failure Modes

```text
invalid_jsonl
missing_feature_delivery_case
missing_evidence_refs
unknown_token_cost_status
insufficient_evidence
raw_context_forbidden
```

## References

- `references/dossier-rubric.md`
- `references/waste-pattern-catalog.md`
- `../../feature-delivery-harness-mvp/schemas/records/yield.dossier.v1.schema.json`
