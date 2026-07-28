# Private Repository Delivery Asset Pack Guide

## Boundary

Run this process only inside the private repository. Public Lattice supplies contracts and local validators; it does not receive source, business context, evidence, human feedback, adoption observations, validation reports, or manager deliverables.

The public synthetic example at `examples/synthetic-private-consumer/` demonstrates shape and failure behavior only.

## First Real Pack

1. Pin an immutable public Lattice tag or full commit SHA and retain the resolved commit.
2. Copy `templates/private-repository/` and create the downstream consumer manifest.
3. Select the smallest dependency-ready Capability Profile and explicit capability versions; never load the whole portfolio.
4. Create one real `feature_delivery_case` as the user-value and evidence boundary.
5. Collect bounded evidence from authorized source, Issue, PR, CI, Incident, review, merge, release, or manual-acceptance records.
6. Preserve the raw human contribution locally with source, scope, time, and authority.
7. Classify every material claim as `OBSERVED`, `DERIVED`, `JUDGED`, or `UNKNOWN`.
8. Create or update one reusable-asset candidate linked to its contribution and Feature Delivery Case.
9. Record a comparable before/after diff for the same scoped asset.
10. Obtain accountable human review; automation and DeliveryYield may provide evidence but cannot approve promotion.
11. Apply only the reviewed task-scoped activation. Do not jump adoption states.
12. Record a real usage observation only after the bounded task completes with addressable evidence.
13. Generate the Manager-Ready Delivery Asset Pack under a private path.
14. Run the pinned consumer, Feature Delivery Case, asset-pack, evidence, and manager-claim validators locally.
15. Generate the canonical Markdown projection and validate it byte-for-byte against the structured claims, limitations, unknowns, and evidence origin.
16. Store the pack, validation report, and review only in the private repository.
17. On a later task, append the new usage observation and evolve the existing asset; do not rewrite prior evidence.

## Local Commands

```bash
python vendor/lattice/scripts/validate_downstream_consumer.py \
  downstream-consumer-manifest.json \
  --lattice-root vendor/lattice \
  --consumer-root .

python vendor/lattice/skills/feature-delivery-case/scripts/validate_feature_delivery_case.py \
  private/cases/<case-id>/feature-delivery-case.json

python vendor/lattice/scripts/validate_delivery_asset_pack.py \
  private/manager-ready-delivery-asset-pack \
  --lattice-root vendor/lattice

python vendor/lattice/scripts/validate_manager_claims.py \
  private/manager-ready-delivery-asset-pack/manager-brief.json \
  --evidence-ledger private/manager-ready-delivery-asset-pack/evidence-ledger.jsonl \
  --rendered-brief private/manager-ready-delivery-asset-pack/manager-brief.md
```

All commands are local. Review validator output before sharing the rendered brief.

## Choose the Smallest Asset Form

- Create or update a **Skill** when portable agent behavior, triggers, outputs, evidence, success, and stop rules must be governed together.
- Create a **Reference** for long background, rationale, examples, variants, or non-executable guidance.
- Create a **Script** for deterministic, fragile, or repeatable transformation or validation.
- Create a **Schema** for a stable machine boundary exchanged across tools or repositories.
- Create an **Eval Case** for positive behavior, a known failure mode, compatibility, or regression protection.
- Update an existing asset when the problem, identity, owner, and behavior family remain the same.
- Reject a candidate when provenance, permission, scope, evidence, safety, authority, or ownership is unresolved.
- Deprecate an asset when it is unsafe, incompatible, superseded, unmaintained, or no longer valid in its declared scope.

Do not create a new Skill merely to store background knowledge, one example, a deterministic command, or a one-off private rule.

## Manager Conclusion Stop

Do not generate or strengthen a manager conclusion when:

- a material claim has no resolvable evidence reference;
- the baseline, comparable after-state, version, or scope is missing;
- evidence origin or access is unclear;
- accountable human challenge is required but absent;
- the requested wording exceeds the current adoption state;
- a single use is being described as reuse or team adoption;
- limitations or unknowns would be hidden;
- ROI, success rate, acceptance, or business value lacks a declared method and sufficient real evidence.

Preserve `UNKNOWN` and state the next evidence needed.

## Later Use and Upgrade

A first evidenced real use can support `used_once`; a separately evidenced later use is required for `reused`; explicit private governance approval is additionally required for `team_available`. A public fixture never advances these states.

Before changing the Lattice pin, compare contract and capability versions, validate private extensions, regenerate the pack, rerun negative checks, and obtain accountable private review. Roll back to the prior immutable pin if compatibility cannot be established.
