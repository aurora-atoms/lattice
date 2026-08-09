# Evidence Wayfinding Schema Parity — PR 7

## Source and decision

Source material: `Lattice_Senior_Attention_Case_Calibrated_Harness_Research_Report_CN`, evidence cutoff 2026-08-08.

The source report identified a P0 false-ready condition: `portable-case-pack.v1.schema.json` declared a closed Draft 2020-12 contract, while CI only checked that the schema file was valid JSON and then relied on a narrower handwritten semantic validator. Invalid instances could therefore pass the runtime gate even though the published schema said they were illegal.

Decision: fix contract execution before adding new Skills, Harness mutation machinery, or broader Senior Attention surfaces.

## Authority split

The validation boundary is now explicit:

```text
Draft 2020-12 JSON Schema
  owns structural validity:
    required fields
    primitive/object/array types
    enum/const values
    additionalProperties
    nested shape
    format checks such as date-time

Portable Case Pack semantic validator
  owns cross-field semantics:
    evidence-reference resolution
    claim-reference resolution
    duplicate identifiers
    public/private evidence compatibility
    observed-claim evidence requirements
    forbidden reasoning-transcript keys
    mission and contract invariants
```

The semantic validator may add domain constraints, but it must not be treated as a substitute for executing the published schema.

## Regression anchors

The PR adds one valid minimal fixture and four structural mutation fixtures that MUST fail the authoritative schema:

1. unknown top-level field;
2. missing `audience`;
3. missing `required_output`;
4. malformed evidence `date` that is not a `date-time`.

These are regression anchors for the false-ready failure discovered by the source audit.

## Explicitly deferred semantic decision

The source audit also tested a `derived` claim with empty `evidence_refs`. Portable Case Pack v1 currently permits that shape structurally, and the current semantic validator only requires evidence for `observed` claims.

This PR does **not** silently tighten that rule. A dedicated fixture preserves the ambiguity as an explicit contract decision. Changing it requires one of:

- a compatible, reviewed semantic-contract clarification with evidence; or
- a versioned Portable Case Pack contract change.

The parity repair must not smuggle a new claim-state model into v1.

## Why this is the first Case-Calibrated change

This change follows the report's case-first ordering:

```text
documented contract
-> executable structural contract
-> regression mutations
-> real/replay Case 0
-> Decision/Outcome receipts
-> bounded Harness candidate
```

This PR stops at executable contract parity. The next PR should use the schema-parity defect as Evidence Wayfinding Case 0 and produce the full case spine. It should not pre-build a generic self-evolution platform.

## Non-goals

This PR does not:

- create or modify an active Skill;
- promote `frontier-practice-scout`;
- create a new module or Agent;
- change Portable Case Pack v1 claim semantics;
- add Decision Card or Outcome Receipt as authoritative second state objects;
- implement Harness mutation, promotion, canary, or rollback infrastructure;
- change active module ownership or authority.

## Validation

```bash
python -m pip install -r requirements-validation.txt
python scripts/validate_json_schema_instance.py \
  schemas/capability/portable-case-pack.v1.schema.json \
  examples/evidence-wayfinding/portable-case-pack.synthetic.v1.json
python -m unittest discover -s tests -p 'test_portable_case_pack_schema.py' -v
python scripts/validate_portable_case_pack.py \
  examples/evidence-wayfinding/portable-case-pack.synthetic.v1.json
```

Structural validation must run before semantic validation in CI.
