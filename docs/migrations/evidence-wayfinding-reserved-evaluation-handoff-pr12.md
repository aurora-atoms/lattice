# Evidence Wayfinding Reserved Evaluation Handoff — PR 12

## Source decision

Merged PR 40 made Blind Challenge execution deterministic but intentionally left the public Case 0 state blocked because a public repository cannot host a credible hidden reserved oracle.

This change implements only the trust-boundary protocol needed to cross that gap safely.

Sequence:

```text
Outcome Receipt
-> Harness Mutation Candidate
-> Blind Challenge contract
-> controlled reserved-evaluation handoff
-> real reserved attestation
-> governed Blind Challenge verdict
```

The current PR implements the handoff. It does not fabricate the real attestation or the final verdict.

## Direction Investment Gate

```yaml
primary_value_path: current_product_delivery
direction_verdict: proceed
existing_capability_gap: >
  Blind Challenge v1 can represent a reserved result but the repository had no
  executable contract for sending a frozen evaluation request across a private
  trust boundary or for returning a safe attestation without leaking the oracle,
  private evidence, or A/B mapping.
user_outcome: >
  A maintainer can hand one frozen candidate to a controlled private evaluator
  and mechanically verify that the returned record preserves evaluation lineage
  and privacy while granting no promotion authority.
```

## Why this is a protocol, not a new module or Skill

The problem is deterministic cross-boundary transport and validation, not a missing reasoning capability.

Therefore the implementation is:

```text
JSONL handoff
+ JSON Schema
+ deterministic request projection
+ deterministic validator
+ conformance tests
```

It does not create:

- a new active module;
- a new Agent;
- a new Skill;
- a second Feature Delivery Case lifecycle;
- a new private-data store;
- an autonomous promotion service.

## Record contract

Each handoff line follows the authoritative structured handoff shape:

```text
type
id
schema
source
target
scope
payload
constraints
```

Supported record types:

```text
eval.reserved_request
eval.reserved_attestation
```

Contract id:

```text
lat.reserved_evaluation_handoff.v1
```

## Trust zones

Request direction:

```text
public_repository
-> controlled_private_evaluator
```

Attestation direction:

```text
controlled_private_evaluator
-> public_repository
```

The request contains only frozen plan metadata and an opaque `controlled://` variant-bundle reference.

The attestation contains only anonymous A/B outcomes, protected metric statuses, safe evidence digests, evaluator metadata, and an attestation digest.

Neither side of the public handoff may serialize:

- raw reserved oracle content;
- raw private evidence;
- incumbent/challenger mapping;
- a governed Blind Challenge verdict;
- `team_available` or auto-promotion authority.

## Current Case 0 state

The public Case 0 adds one request-only JSONL record:

```text
examples/evidence-wayfinding/case-0-schema-parity/
  reserved-evaluation-handoff.request.jsonl
```

It intentionally does not add a real attestation.

The repository also contains a synthetic completed fixture under `tests/fixtures/` to test schema/validator behavior. It is conformance evidence only.

## Validation responsibilities

Structural authority:

```text
schemas/capability/reserved-evaluation-handoff-record.v1.schema.json
```

Semantic/cross-file authority:

```text
scripts/validate_reserved_evaluation_handoff.py
```

Request projection:

```text
scripts/prepare_reserved_evaluation_request.py
```

The validator checks candidate/execution lineage, frozen hash parity, evaluator version, metrics, reserved allocation, anonymous A/B outputs, safe evidence-reference schemes, ordering, and the promotion firewall.

## Boundaries preserved

This PR does not modify active Skills and does not promote `frontier-practice-scout`.

It does not alter the responsibilities of Helixion, AegisFlow, Memexa, FlowGuard, OpenClaw, or DeliveryYield.

`feature_delivery_case` remains the primary user-value lifecycle and Blind Challenge remains an evolution projection around it.

## Why no automatic ingestion yet

An ingestion helper that transforms an attestation into an evaluated Blind Challenge record would be easy to implement synthetically, but that would move the repository back toward framework construction ahead of real evidence.

The next gate is therefore not another public simulation. It is one actual controlled reserved evaluation.

Once a real valid `eval.reserved_attestation` exists, a later PR may implement deterministic ingestion and the governed verdict path using that evidence.

## Validation commands

```bash
python -m json.tool schemas/capability/reserved-evaluation-handoff-record.v1.schema.json >/dev/null

python scripts/validate_reserved_evaluation_handoff.py \
  examples/evidence-wayfinding/case-0-schema-parity/reserved-evaluation-handoff.request.jsonl \
  examples/evidence-wayfinding/case-0-schema-parity/harness-mutation-candidate.json \
  examples/evidence-wayfinding/case-0-schema-parity/blind-challenge-execution.blocked.json \
  --schema schemas/capability/reserved-evaluation-handoff-record.v1.schema.json

python scripts/validate_reserved_evaluation_handoff.py \
  tests/fixtures/evidence-wayfinding/reserved-evaluation/handoff.synthetic-complete.jsonl \
  examples/evidence-wayfinding/case-0-schema-parity/harness-mutation-candidate.json \
  examples/evidence-wayfinding/case-0-schema-parity/blind-challenge-execution.blocked.json \
  --schema schemas/capability/reserved-evaluation-handoff-record.v1.schema.json

python -m unittest discover -s tests -p 'test_reserved_evaluation_handoff.py' -v
```
