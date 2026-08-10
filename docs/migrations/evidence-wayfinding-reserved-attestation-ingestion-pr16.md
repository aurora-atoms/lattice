# Evidence Wayfinding Reserved Attestation Ingestion — PR 16

## Source and sequencing

This change follows the post-Case-0A audit sequence after:

```text
PR 42  authenticated reserved-attestation trust boundary
PR 43  observed-evidence gate
PR 44  authoritative Case bundle validation
```

The remaining bounded gap is not another evaluation concept. It is a deterministic state transition from a cryptographically authenticated reserved result into a public-safe coordinator projection.

## Direction Investment Gate

```yaml
primary_value_path: current_product_delivery
direction_verdict: proceed
existing_capability_gap: >
  Reserved Evaluation Handoff v2 can authenticate one exact evaluator result,
  but the repository had no deterministic ingestion boundary for consuming that
  attestation without manually copying fields, leaking reserved information, or
  accidentally jumping directly to a governed verdict.
user_outcome: >
  A downstream coordinator can validate one signed reserved attestation and emit
  a deterministic public-safe result showing exactly what evidence was ingested,
  what frozen allocations remain missing, and whether later human adjudication is
  even eligible to begin.
verification_method: >
  Schema validation, cryptographic handoff validation, replay mutation tests,
  deterministic digest tests, allocation-settlement tests, and CI execution.
```

This directly removes a blocker to controlled Case 0B-style evaluation. It does not create a team reuse system or a new Skill.

## Implemented slice

Adds:

```text
schemas/capability/reserved-evaluation-ingest-result.v1.schema.json
scripts/ingest_reserved_evaluation_attestation.py
tests/test_reserved_evaluation_ingestion.py
docs/evidence-wayfinding/reserved-evaluation-ingestion.md
```

The script requires the already-frozen candidate and blocked Blind Challenge execution plus a completed v2 request/attestation, trusted public-key store, and consumed-nonce ledger.

It delegates authentication to the existing v2 handoff validator and emits only:

```text
request/bundle binding
authenticated evaluator metadata
reserved result safe projection
safe evidence refs
allocation settlement status
canonical ingest digest
human/promotion firewall
```

## No hidden verdict

The ingest result intentionally has no fields for:

```text
variant_mapping
decision
scoped_canary_scope
team_available
```

Its fixed human gate states:

```text
governed_verdict_included = false
variant_mapping_included = false
governed_verdict_allowed = false
automatic_promotion_allowed = false
team_available_allowed = false
human_decision_required = true
```

An authenticated attestation is evidence, not authority.

## Allocation settlement rule

The source blocked Blind Challenge may already contain public representative/hard/counterexample results. Ingestion adds only the authenticated reserved result for settlement accounting.

The output calculates:

```text
merged_case_ids
missing_case_ids
all_allocations_settled
ready_for_governed_adjudication
```

`ready_for_governed_adjudication` equals true only when every frozen allocation is represented after the reserved result is added.

This is readiness for a later human-controlled adjudication step, not a verdict.

## Replay handling

Ingestion validates the request nonce against the supplied consumed ledger. The CLI optionally supports `--commit-nonce` to atomically append the successfully ingested request nonce to that ledger.

The public repository does not own a real production nonce ledger. Private controlled evaluators/coordinators own that state.

## Synthetic boundary

The existing signed synthetic v2 handoff remains conformance-only.

When ingested against the current public Case 0 blocked execution, the correct result is still not adjudication-ready because the blocked execution does not contain the three non-reserved case results:

```text
all_allocations_settled = false
ready_for_governed_adjudication = false
```

No fixture is relabeled as real downstream evidence.

## Compatibility

No existing contract is removed or renamed.

The new ingest result is an additional bounded public contract that directly bridges two existing surfaces:

```text
Reserved Evaluation Handoff v2
-> later Blind Challenge human adjudication
```

`lat.blind_challenge_execution.v1` is not weakened or silently changed to accept a partially evaluated state.

## Explicit non-goals

This PR does not:

- create or modify a Skill;
- create a new module or Agent;
- reveal the reserved oracle;
- reveal A/B variant mapping;
- compute `reject | revise | continue_shadow | scoped_canary`;
- approve a canary;
- grant `team_available`;
- create a dashboard;
- claim real downstream adoption;
- claim Senior Attention ROI;
- merge, release, or deploy anything.

## Next gate

After this PR, the public architecture should stop expanding until real controlled evaluation evidence exists.

The next evidence-bearing activity is private/downstream:

```text
real non-reserved results
+ real authenticated reserved attestation
-> deterministic ingest
-> human adjudication candidate
```

Only after that real execution should another public contract or workflow change be considered.
