# Evidence Wayfinding Attention / Outcome Contracts — PR 9

## Source decision

This change implements the next gate recorded by the merged Case 0 replay: formalize only the two receipt contracts whose need is now demonstrated by an executed repository case.

Source design material includes the case-calibrated Senior Attention audit and the governed Senior Attention decision-system report. Both converge on the same corrections:

- replace the old `5-of-4` attention heuristic with mandatory invariants;
- keep Decision Card / Map as projections rather than second truth stores;
- settle outcomes per Claim with evidence, status, version, cutoff, and history;
- let one real outcome create a candidate signal, never team-level promotion authority.

## Direction Investment Gate

```yaml
primary_value_path: current_product_delivery
direction_verdict: proceed
evidence_refs:
  - repo://examples/evidence-wayfinding/case-0-schema-parity@ca74491cd63ad248714dc2bb591c5d0c833bca11
  - repo://docs/evidence-wayfinding/case-0-schema-parity.md@ca74491cd63ad248714dc2bb591c5d0c833bca11
existing_capability_gap: >
  Case 0 showed admission and outcome as necessary failure-sensitive boundaries,
  but they remained candidate-shaped and the case validator embedded their
  semantics locally. A reusable deterministic contract is now justified.
user_outcome: >
  A Case can deterministically decide whether scarce Senior attention may be
  requested, then settle every Claim and failure point after delivery without
  creating a second lifecycle truth or granting self-promotion authority.
```

## Changes

This PR introduces:

```text
schemas/capability/attention-admission-receipt.v1.schema.json
schemas/capability/outcome-receipt.v1.schema.json
scripts/validate_attention_admission.py
scripts/validate_outcome_receipt.py
tests/test_attention_outcome_contracts.py
```

Case 0 is migrated from candidate receipt shapes to the v1 contracts, while its Decision Card and Verification Receipt remain case-scoped candidate projections.

## Admission rule

The five mandatory invariants are:

```text
M1 target
M2 evidence
M3 counterevidence
M4 risk / authority
M5 delivery
```

Overall verdict:

```text
any escalate -> ESCALATE
else any fail -> BLOCKED
else -> READY
```

There is no waiver score.

A non-UNKNOWN `derived` Claim without evidence is intentionally handled as an Admission failure rather than a silent Portable Case Pack v1 schema rewrite.

## Outcome rule

Outcome Receipt v1 requires a settlement record for every Case Pack Claim and preserves:

```text
status
version
evidence_refs
cutoff
status_history
```

Outcome status uses the existing Evidence Wayfinding lifecycle vocabulary:

```text
UNKNOWN
HYPOTHESIS
EVIDENCED
CONFIRMED
CONFLICTED
STALE
INVALIDATED
```

A JUDGED Claim remains JUDGED as provenance in the Portable Case Pack; its outcome status expresses evidentiary settlement rather than changing provenance category.

## Boundary review

This PR intentionally does not:

- add or change an active Skill;
- promote `frontier-practice-scout`;
- create a new Agent or active module;
- make Decision Card an authoritative state object;
- rewrite Portable Case Pack v1 Claim structure;
- implement candidate generation, canary, promotion, or rollback orchestration;
- assert private adoption or Senior Attention ROI from synthetic replay evidence.

`feature_delivery_case` remains the primary delivery lifecycle boundary. Admission and Outcome are projections around that boundary.

## Next gate

The next PR may encode exactly one Harness Mutation Candidate from Case 0's earliest failure point and evaluate incumbent vs challenger on representative/hard/reserved cases. It must not yet build a general-purpose self-modifying Harness.

## Validation

```bash
python -m pip install -r requirements-validation.txt
python scripts/validate_json_schema_instance.py \
  schemas/capability/attention-admission-receipt.v1.schema.json \
  examples/evidence-wayfinding/case-0-schema-parity/admission-receipt.json
python scripts/validate_json_schema_instance.py \
  schemas/capability/outcome-receipt.v1.schema.json \
  examples/evidence-wayfinding/case-0-schema-parity/outcome-receipt.json
python scripts/validate_attention_admission.py \
  examples/evidence-wayfinding/case-0-schema-parity/admission-receipt.json \
  examples/evidence-wayfinding/case-0-schema-parity/portable-case-pack.json \
  examples/evidence-wayfinding/case-0-schema-parity/case-contract.json
python scripts/validate_outcome_receipt.py \
  examples/evidence-wayfinding/case-0-schema-parity/outcome-receipt.json \
  examples/evidence-wayfinding/case-0-schema-parity/portable-case-pack.json
python -m unittest discover -s tests -p 'test_attention_outcome_contracts.py' -v
python -m unittest discover -s tests -p 'test_evidence_wayfinding_case0.py' -v
```
