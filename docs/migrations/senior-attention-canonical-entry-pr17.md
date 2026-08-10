# Senior Attention Canonical Entry Migration

## Decision

Add one canonical public Senior Attention reference workflow and one contract-validated runtime profile without creating a Senior Attention Skill, Agent, or module.

## Why

The public repository already contains the Feature Delivery Case spine, Evidence Wayfinding contracts, context, risk, blocker, decision, management, outcome, and governed-evolution capabilities. The gap is discoverability and composition: downstream integrators otherwise need project-history knowledge to assemble the five Senior Attention task families safely.

This migration therefore changes the public entry surface, not the underlying specialist behavior.

## Direction Investment Gate

```text
primary_value_path: current_product_delivery
direction_verdict: bind_to_delivery
beneficiary: downstream Senior Attention pilot integrator and accountable delivery owner
observable_before: Senior Attention behavior is distributed across research, example profiles, and specialist packages
observable_after: one canonical workflow and one validated profile expose the five bounded task families
verification: profile/schema validation, canonical manifest registration, generated projection parity, five positive and five negative fallback discovery probes, public/private boundary validation
existing_capability_gap: specialist capabilities exist; a canonical cross-family entry does not
unknown: real private adoption, attention savings, owner acceptance, and business value
```

The result remains bound to a downstream validation case. `contract_validated` is a public-package lifecycle state, not evidence of real use.

## Added public assets

```text
docs/senior-attention.md
workspaces/templates/senior-attention-runtime-profile.v1.json
tests/fixtures/senior-attention-entry/routing-cases.v1.json
tests/test_senior_attention_entrypoint.py
```

The canonical manifest registers:

```text
workspace:senior-attention-workflow@1.0.0
  role = reference_workflow

workspace:senior-attention-runtime@1.0.0
  role = capability_profile
```

Registry compatibility projections are regenerated from the manifest.

## Five task families

```text
feature requirement / work ready
risk preflight
bug / delivery rescue
decision support
management translation
```

The profile lists a bounded set of available Skills, but almost all are `on_demand`. `decision-question-builder` remains explicit. `delivery-capability-conductor` is not implicitly loaded; native runtime discovery remains the preferred selection mechanism and the deterministic router remains fallback/evaluation infrastructure.

## Routing conformance

Synthetic probes cover one natural-language request for each family plus negative controls for ordinary formatting, summarization, README wording, local renaming, and punctuation editing.

These tests prove only public routing/conformance behavior. They do not prove that a private Senior used the workflow, that a real defect was prevented, or that attention cost was reduced.

## Public/private boundary

No private company source, schema, path, person, case, message, log, telemetry, or business field is added. The workflow defines only opaque downstream extension references and requires private ACL, purpose, authority, retention, and evidence handling to remain downstream.

## Compatibility

The existing `examples/capability-profiles/senior-decision-wayfinding-runtime-profile.v1.json` remains unchanged as a historical synthetic Evidence Wayfinding reference. This migration does not silently rename or replace it.

## Explicit non-goals

This migration does not:

- create `skills/senior-attention`;
- create a Senior Attention Agent or module;
- modify `domain-context-pack`, `delivery-rescue`, `risk-ahead`, or `management-translation` behavior;
- make `senior-attention-queue` the universal entry;
- add write, merge, deployment, secret, or destructive authority;
- claim downstream adoption or ROI;
- change Outcome, Harness Mutation, Blind Challenge, reserved evaluation, canary, or promotion authority.

## Next bounded work

After merge, the next public hardening step may add the Domain Context machine contract only if it is still required to unblock the downstream pilot. Public architecture expansion must remain subordinate to private/live evidence.
