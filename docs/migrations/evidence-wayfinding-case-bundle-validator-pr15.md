# Migration: Evidence Wayfinding Authoritative Case Bundle Validation

Status: `implemented_candidate`

Date: 2026-08-09

Source: post-Case-0A independent audit, P2 `组合层绿灯假象`

## Decision

Create one authoritative validation entrypoint for an Evidence Wayfinding case bundle:

```text
scripts/validate_evidence_wayfinding_case_bundle.py
```

The existing lower-level schemas and semantic validators remain authoritative inside their owned boundaries. The new bundle validator composes them in the required order so a consumer does not need to know which validators must be called manually.

This is a hardening change to an existing public validation path. It is not a new Skill, Agent, module, Capability Profile, workflow product surface, dashboard, or promotion mechanism.

## Root cause

`scripts/validate_evidence_wayfinding_case.py` was intentionally written as a cross-file Case Spine validator. It checked lineage and invoked selected semantic gates, but it did not execute every child object's JSON Schema.

Therefore this mutation could produce a false green when that script was used alone:

```text
outcome-receipt.json
+ unknown top-level field
-> validate_evidence_wayfinding_case.py PASS
```

Repository CI remained protected only because separate workflow steps happened to execute the Outcome Receipt schema. A downstream consumer could reasonably assume the top-level Case validator was complete and skip those steps.

That recreated the same class of failure Case 0 originally exposed: a published contract existed, but the apparently authoritative runtime entrypoint did not execute the complete contract stack.

## Direction Investment Gate

Primary value path:

```text
current_product_delivery
```

User outcome:

> A maintainer or downstream consumer can run one command and know that a Case bundle has passed all applicable structural, semantic, lineage, evidence-integrity, and governed-evolution checks implemented by the repository.

Why existing components were insufficient:

- individual validators were correct within their boundaries;
- the cross-file Case Spine validator was not a structural bundle validator;
- CI encoded the required invocation order implicitly;
- the consumer had to reconstruct that order manually.

The smallest sufficient fix is composition, not another public schema family or capability.

## Validation order

The authoritative entrypoint now performs:

```text
1. required core file presence
2. child JSON Schema validation
3. Portable Case Pack semantic validation
4. Case Spine cross-file lineage and Admission/Outcome semantics
5. repo:// evidence Git-object integrity
6. Harness Mutation Candidate structural + semantic validation when present
7. Blind Challenge structural + semantic validation when present
8. Reserved Evaluation Handoff structural + semantic validation when present
9. deterministic validation summary
```

The lower-level components remain reusable independently for targeted debugging and unit tests.

## Evidence integrity repair

Case 0 `EV-002` previously recorded:

```text
content_hash = git:pre-parity-workflow
```

The baseline file is:

```text
repo://.github/workflows/capability-profile-validate.yml@6d8365c6ef1ca8cf82a220e5c87b9b25fada8fd7
```

Its actual Git blob SHA is:

```text
4e194dfa76d2e990d07a1fbf8cc349704cc60638
```

The fixture now records that exact blob hash. The bundle validator verifies `repo://<path>@<commit>` references with the local Git object database and rejects placeholder or drifted `git:<blob-sha>` values.

`repo://commit/<sha>` evidence is also checked for commit existence and exact `git:<commit-sha>` binding.

## CI change

Case 0 is no longer validated through a hand-maintained sequence of separate structural/semantic commands. CI now uses:

```bash
python scripts/validate_evidence_wayfinding_case_bundle.py \
  examples/evidence-wayfinding/case-0-schema-parity
```

Independent generic/synthetic fixtures remain validated separately where they test compatibility that is not part of the Case 0 directory.

## Regression anchors

The bundle test rejects at least:

```text
unknown top-level Outcome Receipt field
unknown top-level Harness Mutation Candidate field
repo evidence hash drift
unknown Reserved Evaluation Handoff field
```

The first mutation directly closes the audit finding.

## Compatibility

`scripts/validate_evidence_wayfinding_case.py` remains available as the Case Spine cross-file component. It is not removed or renamed in this migration.

No existing public schema identity changes.

No active Skill or module identity changes.

## Explicit non-goals

This migration does not implement:

- authenticated-attestation ingestion or state transition;
- a real controlled Reserved Evaluation;
- private Case 0B attention measurements;
- `team_available`;
- auto-promotion;
- merge, release, or deployment authority;
- new Senior Attention UI surfaces.

## Exit criteria

This migration is ready when:

1. one Case 0 bundle command passes on the valid public replay;
2. adding an unknown Outcome Receipt field fails through that same command;
3. Case 0 `EV-002` resolves to its real baseline Git blob;
4. candidate, Blind Challenge, and handoff artifacts present in the directory are included automatically;
5. CI and regression tests pass;
6. the public Case 0 documentation no longer describes Admission and Outcome as future work.

## Next gate

After this migration, the next bounded implementation is deterministic authenticated-attestation ingestion/state transition. That work must consume a validated v2 attestation and emit only a public-safe reserved-result/evaluated-execution transition while preserving the human verdict and promotion firewall.
