# Evidence Wayfinding Case 0 — PR 8

## Source and sequencing

This change follows the case-calibrated Senior Attention research sequence:

```text
published contract
-> executable contract parity
-> one bounded replay case
-> receipts and observed state change
-> only then generalize Attention Admission / Outcome contracts
-> only after repeated evidence consider Harness mutation promotion
```

The preceding schema-parity change fixed the P0 false-ready condition. This PR replays that defect as the first complete public Evidence Wayfinding case spine.

## Direction Investment Gate

```yaml
primary_value_path: current_product_delivery
direction_verdict: proceed
evidence_refs:
  - repo://commit/863ceb307416975ddb43ec3fba2606648b2c0c59
  - repo://docs/migrations/evidence-wayfinding-schema-parity-pr7.md
existing_capability_gap: >
  The repository had workflow documentation, Portable Case Pack validation,
  and the repaired CI contract, but no linked public case spine showing one
  bounded decision progressing through admission, decision projection,
  verification, and observed outcome.
user_outcome: >
  A maintainer can inspect one public replay and verify how the Evidence
  Wayfinding workflow maps a real repository failure point to a bounded,
  evidence-linked state change without creating a new module or Skill.
```

The value is the executable replay and its reviewable lineage, not the existence of new files.

## Implemented slice

The public synthetic replay contains:

```text
case-contract.json
portable-case-pack.json
admission-receipt.json
decision-card.json
verification-receipt.json
outcome-receipt.json
```

A deterministic validator checks cross-file identity, evidence references, mandatory admission checks, Decision Card option lineage, verification verdict, observed state change, and the prohibition on promotion authority from this single case.

Portable Case Pack structural and semantic validation remain owned by their existing validators. The case-spine validator does not duplicate that authority.

## Candidate receipts, not new canonical objects

The Admission Receipt, Decision Card, Verification Receipt, and Outcome Receipt use `candidate.v0` contract identifiers inside the public replay.

They are not yet registered as independent canonical capabilities or record types. Case 0 is the evidence used to decide what should become general contract surface next.

The Feature Delivery Case remains the primary lifecycle and value boundary.

## Public/private boundary

Every public Case 0 receipt is marked:

```text
simulation_status = synthetic_reference
downstream_adoption_status = not_observed
data_classification = public
```

The replay uses public repository history only. It does not contain private business evidence, manager-ready claims, employee feedback, or adoption observations.

## Why no Skill changes

Case 0 exposes a contract/runtime lineage need, not a missing atomic Skill. Existing Evidence Wayfinding routing, understanding, challenge, decision, delivery, and outcome capabilities remain sufficient for this replay.

`frontier-practice-scout` remains a candidate. Nothing in this case provides second-use evidence for it.

## What is intentionally deferred

This PR does not:

- create a new module or Agent;
- modify an active Skill;
- register the candidate receipts as canonical runtime records;
- change Portable Case Pack v1 semantics;
- build a generic mutation engine;
- grant a candidate team availability;
- claim Senior Attention value from synthetic conformance alone.

## Next implementation gate

Case 0 now provides evidence for a narrower next change:

1. formalize Attention Admission as mandatory invariants with `READY | BLOCKED | ESCALATE`;
2. formalize Outcome Receipt claim/state lineage;
3. keep both as projections around the Feature Delivery Case;
4. require schemas, negative cases, and deterministic validation;
5. do not generalize Harness mutation until a failure point is replayed against representative/reserved cases.

## Validation

```bash
python -m pip install -r requirements-validation.txt
python scripts/validate_json_schema_instance.py \
  schemas/capability/portable-case-pack.v1.schema.json \
  examples/evidence-wayfinding/case-0-schema-parity/portable-case-pack.json
python scripts/validate_portable_case_pack.py \
  examples/evidence-wayfinding/case-0-schema-parity/portable-case-pack.json
python scripts/validate_evidence_wayfinding_case.py \
  examples/evidence-wayfinding/case-0-schema-parity
python -m unittest discover -s tests -p 'test_evidence_wayfinding_case0.py' -v
```
