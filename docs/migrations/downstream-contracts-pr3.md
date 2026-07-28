# Downstream Consumer Contracts and Validators — PR 3

## Decision

PR 3 turns the PR 1 downstream and manager policies into local machine contracts. A private repository can pin an immutable public Lattice version, select exact dependency-ready capability versions, declare scoped private extensions, validate evidence-linked manager claims, and validate a Manager-Ready Delivery Asset Pack without uploading private content.

## PR 2 Review Amendments

Two issues were corrected before adding downstream consumers:

1. The canonical validator now enforces non-empty structured contract fields, exact evidence/compatibility objects, and exact top-level fields rather than relying on schema-file syntax checks.
2. `workspace:pr-review-template@1.0.0` passed the existing workspace validator and moved from `draft` to `contract_validated`, making a real Capability Profile selectable without claiming conformance, release, or adoption.

The migration remains deterministic and legacy projection fields are preserved.

## Contracts

```text
schemas/downstream/downstream-consumer-manifest.v1.schema.json
schemas/downstream/private-capability-extension.v1.schema.json
schemas/evidence/evidence-claim.v1.schema.json
schemas/evidence/delivery-evidence-asset-pack.v1.schema.json
schemas/manager/manager-delivery-brief.v1.schema.json
```

Contract version is `1.0.0` for each new family. These public versions describe the initial downstream boundary and do not change any existing Skill package behavior.

## Validators

```text
scripts/validate_downstream_consumer.py
scripts/validate_delivery_asset_pack.py
scripts/validate_manager_claims.py
```

The validators are standard-library Python and make no network calls. They read only explicit local inputs and the pinned Lattice canonical manifest. The asset-pack validation report contains rule results and stays in the private pack.

## Deterministic Gates

PR 3 rejects:

- floating Lattice refs or malformed commit pins;
- nonexistent, wildcard, draft, or deprecated public capability versions;
- broad default capability loading;
- private extensions using `lat` or `lattice`, impersonating public status, or overriding without review;
- unsafe relative paths or an evidence store that permits public upload;
- missing or dangling evidence references;
- `OBSERVED`, `DERIVED`, or `JUDGED` claims without required basis;
- `UNKNOWN` presented as fact;
- hidden limitations;
- synthetic adoption above `not_observed`;
- one use described as reuse;
- one case described as team-wide;
- team availability without governance approval;
- synthetic manager acceptance or ROI;
- DeliveryYield used as an approval authority;
- missing asset-pack files or cross-file case/pack identity drift.

## Templates and Compatibility

Public templates live under:

```text
templates/private-repository/
templates/delivery-evidence-asset-pack/
templates/manager-delivery-brief/
```

`REPLACE_...` placeholders intentionally fail until the private repository supplies its immutable pin, private identifiers, paths, owner, and timestamps. Existing public capability IDs and registry projections remain compatible. No private content, real evidence, adoption observation, or manager conclusion is added to Lattice.

## Remaining PR 4 Boundary

PR 3 proves contract and negative-rule behavior through unit fixtures. It does not prove the complete synthetic downstream generation workflow, golden output stability, heterogeneous full-runner behavior, real private adoption, manager acceptance, reuse, team availability, or ROI.
