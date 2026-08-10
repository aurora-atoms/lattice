# Evidence Wayfinding Observed Evidence Gate — PR 14

## Source finding

Post-Case-0A audit identified a false-ready path in `lat.blind_challenge_execution.v1`:

```text
synthetic evaluated execution
-> relabel simulation_status = downstream_observed
-> relabel downstream_adoption_status = observed_once
-> choose decision.verdict = scoped_canary
-> leave execution/case/variant/protected-metric evidence_refs empty
-> semantic validator still passes
```

After Reserved Evaluation Handoff v2, a second gap remained: Blind Challenge could carry attestation-shaped metadata without proving that its reserved result was the result in the authenticated v2 attestation.

This change closes only those two evidence gates.

## Direction Investment Gate

```yaml
primary_value_path: current_product_delivery
direction_verdict: proceed
beneficiary: maintainers and downstream evaluators consuming Blind Challenge results
user_outcome: >
  A receipt cannot claim observed downstream evaluation or request a scoped canary
  unless its result evidence is explicit and its reserved result is bound to an
  authenticated evaluator attestation.
existing_capability_gap: >
  Blind Challenge v1 validates allocation, protected metrics, verdict boundaries,
  and attestation-shaped metadata, while Reserved Evaluation Handoff v2 validates
  cryptographic trust independently. No existing gate composes the two and rejects
  evidence-empty downstream-observed claims.
verification: mutation tests plus existing Blind Challenge and v2 attestation tests
```

No new Skill, Agent, module, workflow lifecycle, dashboard, or promotion mechanism is introduced.

## Contract decision

The JSON shape of `lat.blind_challenge_execution.v1` is unchanged.

This is a semantic hardening because the problematic states were already semantically false claims rather than a missing transport field. Synthetic conformance fixtures may retain empty evidence arrays while they remain:

```text
simulation_status = synthetic_reference
downstream_adoption_status = not_observed
```

Real observed states fail closed unless evidence and trust context are supplied.

## Downstream-observed evidence invariants

For:

```text
simulation_status = downstream_observed
```

semantic validation requires:

```text
status = evaluated
downstream_adoption_status = observed_once | reused
execution.evidence_refs is non-empty
each case_result.evidence_refs is non-empty
each variant_outcome.evidence_refs is non-empty
each protected_metric.evidence_refs is non-empty
all evidence refs are URI-like
```

This does not copy private evidence into public Lattice. The owning downstream repository may retain raw evidence and expose only bounded references or redacted/digest projections under its existing data policy.

## Authenticated reserved-result binding

Any of the following requires a verified Reserved Evaluation Handoff v2 context:

```text
simulation_status = downstream_observed
or
decision.verdict = scoped_canary
```

The Blind Challenge validator delegates cryptographic trust verification to `validate_reserved_evaluation_handoff_v2.py` and then checks composition invariants:

```text
evaluated execution_id == blocked source execution_id
execution reserved result == authenticated attestation reserved_case_result
reserved_oracle.attestation_ref == authenticated attestation ref
reserved_oracle.attestation_hash == attestation canonical digest
reserved_oracle.evaluated_by == trusted evaluator id
reserved_oracle.evaluated_at == authenticated evaluated_at
execution.evidence_refs contains authenticated attestation_ref
```

The Blind Challenge validator does not own trusted-key policy or signature algorithms. Those remain in Reserved Evaluation Handoff v2.

## Promotion boundary

Authentication and evidence completeness do not grant promotion.

The existing firewall remains:

```text
automatic_promotion_allowed = false
team_available_allowed = false
human_owner_required = true
scoped_canary_requires_human_approval = true
```

A validated `scoped_canary` means only that the evidence package is eligible to be presented to the human canary authority under the existing candidate scope and rollback rules.

## Compatibility

Existing valid states remain valid:

- public Case 0 remains `blocked_pending_reserved_oracle`;
- synthetic evaluated conformance remains `synthetic_reference / not_observed` and may validate without a real trust context when its verdict is not `scoped_canary`;
- Reserved Evaluation Handoff v1 and v2 contracts are unchanged;
- Blind Challenge JSON Schema v1 is unchanged.

New behavior is fail-closed for claims that previously overstated evidence status.

## Regression cases

Tests now cover:

- `scoped_canary` without authenticated v2 context -> reject;
- matching signed v2 attestation + scoped canary -> pass synthetic conformance;
- relabeled `downstream_observed` with empty evidence -> reject even with a trusted attestation;
- evidence-complete downstream-observed in-memory conformance -> pass;
- non-URI evidence refs -> reject;
- reserved result diverges from authenticated attestation -> reject;
- evaluator metadata diverges from authenticated attestation -> reject;
- `synthetic_reference` claiming downstream adoption -> reject.

The positive downstream-observed case exists only as in-memory test conformance. No public fixture is promoted to real adoption evidence.

## Deferred findings

This PR intentionally does not address:

- the single authoritative Case bundle validator;
- deterministic attestation ingestion/state transition;
- Case 0 `EV-002` content-hash repair;
- Case 0 documentation status drift outside the Blind Challenge page;
- private Case 0B Senior Attention measurements;
- `team_available`, auto-promotion, merge, release, or deployment.

The next public hardening step should be the authoritative Case bundle validation entrypoint, not new capability surface.
