# Downstream Private Repository Contract

## Purpose

This contract defines how a private repository consumes public Lattice without exposing private evidence or impersonating a public capability package.

## Required Consumer Declaration

The downstream repository must keep a machine-readable consumer manifest with at least:

```yaml
consumer_id:
consumer_repository:
lattice_source:
  repository:
  ref:
  commit_sha:
contract_versions:
capability_profiles:
public_capabilities:
private_extensions:
evidence_storage:
manager_projection:
validation_commands:
compatibility_policy:
```

The PR 3 schema will make these fields deterministic. Until then, this document is the normative contract and a manifest is not validator-conformant.

## Pinning

- `lattice_source.ref` must be an immutable release tag or full commit SHA.
- `lattice_source.commit_sha` records the resolved full commit.
- Floating branches such as `main`, `master`, or a moving feature branch are invalid pins.
- `contract_versions` declares every consumed schema or contract family.
- Each public capability reference includes stable family name and semantic version.
- The manifest must not load all public capabilities by default.

The private repository records the pin; public Lattice does not fetch the private repository or its evidence.

## Capability Profile Selection

Choose the smallest profile that can satisfy the task. A profile declares selected atomic capabilities, selectors, workflows, schemas, validators, and templates. Optional context is advisory and cannot trigger eager portfolio loading.

Profile resolution order:

```text
explicit task scope
-> selected private Capability Profile
-> pinned public capability identity
-> declared private extension
-> optional bounded context for a named gap
```

## Private Extension Identity and Precedence

A private extension must use a private namespace controlled by the downstream repository and record:

```text
extension_id
extension_version
private_namespace
relationship = extends | overrides | composes
public_capability_id
public_capability_version
scope
required_permissions
authority_boundary
compatibility
```

Rules:

- a private extension never uses the `lat` namespace as its own identity;
- it never changes or republishes the public capability's identity or status;
- it cannot claim public release or public conformance;
- it takes precedence only inside its declared private scope;
- an override requires explicit private governance review;
- an extension cannot weaken public safety, evidence, privacy, or human-authority rules without a documented exception owned by an accountable private authority;
- public Lattice does not validate or store the extension's private content.

## Schema Compatibility and Migration

The consumer declares exact contract versions. Compatible patch and minor upgrades may be accepted only after local validation. A major version, deprecated contract, removed field, stricter evidence rule, authority change, or extension conflict requires a migration decision.

Before changing a pin:

1. resolve the proposed tag and commit;
2. compare capability and contract versions;
3. validate every selected profile and capability;
4. validate private extensions against their referenced public versions;
5. migrate local records in a reviewable change;
6. regenerate asset packs;
7. rerun negative and manager-claim checks;
8. obtain accountable review before adopting the new pin.

Rollback restores the prior immutable pin and its compatible private artifacts. Do not silently reinterpret old evidence under a new schema.

## Local Evidence and Secret Boundary

`evidence_storage` resolves only inside the private repository or its approved private evidence service. It must not point to a public Lattice writeback path.

Private storage may contain real source, tickets, PRs, CI output, incidents, review comments, human feedback, asset candidates, usage observations, and manager packs. Secrets should be referenced through approved secret management, never embedded in manifests, evidence ledgers, generated packs, logs, or public fixtures.

Public validator processes may read bounded local files. They must not upload them, write them into the public dependency checkout, emit raw private content in public CI artifacts, or require public network submission.

## Standard Local Flow

```text
pin Lattice
-> validate consumer manifest and capability versions
-> select smallest Capability Profile
-> create one real feature_delivery_case
-> collect bounded private evidence
-> preserve raw human contribution
-> create or update a reusable asset candidate
-> obtain accountable human review
-> activate only within approved scope
-> record real usage locally
-> generate Manager-Ready Delivery Asset Pack
-> validate evidence refs and manager wording
-> keep all real artifacts private
```

The executable validator names reserved for PR 3 are:

```text
scripts/validate_downstream_consumer.py
scripts/validate_delivery_asset_pack.py
scripts/validate_manager_claims.py
```

Their absence in PR 1 is explicit; documentation conformance must not be reported as schema or runtime conformance.

## Asset Pack Location and Shape

A private case may use:

```text
manager-ready-delivery-asset-pack/
  asset-pack.manifest.json
  feature-delivery-case.json
  evidence-ledger.jsonl
  contribution-ledger.jsonl
  reusable-assets/<asset-id>/
  reusable-asset-dossier.md
  manager-brief.md
  validation-report.json
```

Public Lattice stores only schemas, templates, validators, and explicitly synthetic examples of this shape.
