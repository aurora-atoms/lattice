# Release and Compatibility Policy

## Identity

Public capability identity uses:

```text
skill:<family-name>@<semantic-version>
agent:<family-name>@<semantic-version>
```

The family name is stable. A private extension uses its private namespace and references, but never impersonates, the public identity.

## Public Package Lifecycle

```text
draft
-> contract_validated
-> conformance_validated
-> released
-> deprecated
```

- `draft`: contract incomplete or under review; downstream pinning is unsupported.
- `contract_validated`: identity, schema, evidence, authority, and compatibility contracts pass.
- `conformance_validated`: positive, negative, migration, and synthetic conformance checks pass.
- `released`: an accountable maintainer has published an immutable version for downstream pinning.
- `deprecated`: still addressable for compatibility, with replacement or migration guidance.

No stage may be skipped. Green CI is validation evidence, not release authority or business-value evidence.

## Private Adoption Lifecycle

Private downstream adoption is separate:

```text
not_observed
-> imported
-> task_scoped
-> used_once
-> reused
-> team_available
-> deprecated
```

Only private evidence and human review can advance this lifecycle. Public Lattice never projects synthetic conformance into private adoption.

## Semantic Versioning

- Patch: wording, examples, discovery clarity, or validator correction without observable contract change.
- Minor: backward-compatible trigger, optional context, output, workflow, evidence, success, stop, profile, or validator capability.
- Major: incompatible required input, permission, removed output, trigger narrowing, authority change, evidence weakening/strengthening that rejects prior valid records, or behavior semantic change.

Required inputs, permissions, outputs, evidence, success signals, stop conditions, authority boundaries, and behavior semantics are compatibility surfaces. Deprecation is explicit; a new version does not silently delete the old contract.

## Release Evidence

A release candidate records:

```text
identity and version
capability role and public package status
source commit
schema and projection versions
positive and negative conformance results
compatibility decision and migration note
known limitations
accountable review
```

Synthetic fixtures are labeled `simulation_status=synthetic_reference` and `downstream_adoption_status=not_observed`.

## Downstream Upgrade

A downstream repository changes its immutable pin only after:

```text
manifest validation
capability identity and version resolution
schema compatibility and migration checks
private extension compatibility
evidence and asset-pack validation
manager-claim validation
negative cases
accountable private review
```

The public repository does not read the private evidence used by these checks.

## Compatibility Projections

`registry/capability-manifest.json` is canonical. Existing registries remain supported generated projections:

- old fields are preserved while version, canonical role, public status, description, and trigger are added;
- `scripts/generate_capability_registry_projections.py --check` rejects projection drift;
- `scripts/validate_capability_manifest.py` rejects identity, version, status, role, path, description/trigger, and deprecation-reference failures;
- `docs/migrations/canonical-manifest-pr2.md` records the one-time migration and review boundary.

## Human Authority

Maintainers approve public releases and deprecations. Private owners approve private extensions, adoption, asset promotion, and manager wording. DeliveryYield, selectors, validators, synthetic fixtures, and registry scores provide evidence only; none is an approval authority.
