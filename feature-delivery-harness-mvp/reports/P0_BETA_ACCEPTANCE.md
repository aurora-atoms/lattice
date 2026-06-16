# P0-Beta Acceptance Snapshot

Status: stabilized acceptance candidate.

```text
scope:
  feature_delivery_case vertical slice
  JSONL envelope + eight P0-beta record types
  deterministic validators
  deterministic waste detection
  deterministic Token Economics Dossier
  four top-level skill control planes

stabilization_gates:
  schema_runtime_contract_alignment
  strict_expected_failure_codes
  strict_expected_waste_patterns
  generated_dossier_jsonl_validation
  golden_dossier_markdown_for_dossier_cases
  full_skill_package_validation

boundaries:
  project_id=lattice
  namespace=lat
  examples=synthetic
  deliveryyield=economics_only
  no_raw_company_context
```

Current hardening overlay:

```text
implemented_after_p0_beta:
  P1 evidence/context-pack hardening
  P1.5 delivery verdict machine contract
  schema-subset runtime payload validation
  verdict-first dossier evidence path

current_eval_count:
  10 deterministic eval cases
```

Acceptance commands:

```text
python feature-delivery-harness-mvp\scripts\validate_contract_alignment.py
python feature-delivery-harness-mvp\scripts\run_mvp_evals.py
python feature-delivery-harness-mvp\scripts\validate_jsonl.py feature-delivery-harness-mvp\evals\good_feature_case_001\input.jsonl
python feature-delivery-harness-mvp\scripts\validate_task_packet.py feature-delivery-harness-mvp\evals\good_feature_case_001\input.jsonl
python scripts\validate_skill_package.py --root skills
```
