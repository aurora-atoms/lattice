# PR49: Canonical Google Workspace Senior Attention Adapter Contract

## Decision

Add one public, machine-validatable Google Workspace adapter contract for Senior Attention without creating a Google-specific task Skill, Agent, module, private data plane, or rendered runtime package.

The canonical source is:

```text
runtime-adapters/google-workspace/senior-attention/adapter-source.v1.json
```

The source projects the existing public Senior Attention workflow and runtime profile into three explicitly different runtime targets:

```text
gem
workspace_studio
notebook
```

All three remain candidate-only and require private downstream verification plus human confirmation.

## Direction Investment Gate

```text
primary_value_path: current_product_delivery
direction_verdict: bind_to_delivery
```

Beneficiary: a downstream Senior Attention pilot integrator and accountable engineering owner.

Observable change: before any company source is connected, the public repository can deterministically reject a Google adapter that broadens authority, assumes complete search, treats product availability as universal, drops counterevidence/unknowns, or binds private source material into the public contract.

Existing capability gap: PR46 established the canonical Senior Attention workflow/profile, PR47 hardened Domain Context Pack, and PR48 hardened Bug Investigation. None of those contracts describes provider-specific Google Workspace surfaces, account availability assumptions, or the candidate-only handoff ceiling.

Current evidence: public Lattice contracts and public adapter research. Real downstream usefulness, source coverage, attention reduction, owner acceptance, and account configuration remain unknown.

Next use: render three thin public projections, then run a private manual/shadow pilot. Public conformance does not establish adoption.

## Format Decision

The research design allowed a YAML-like canonical source. This implementation uses JSON instead:

```text
adapter-source.v1.json
```

Reason:

- Lattice already uses Draft 2020-12 JSON Schema and deterministic JSON validation;
- `requirements-validation.txt` does not require a YAML parser;
- JSON avoids adding a new parser/dependency solely for an adapter manifest;
- later renderers can still emit provider-specific text or YAML where the provider requires it.

This is a representation choice, not a change to the adapter architecture.

## Authority Boundary

The contract fixes:

```text
authority_ceiling = candidate
human_confirmation_required = true
public_writeback_allowed = false
authoritative_case_write_allowed = false
delivery_verdict_allowed = false
automatic_action_default = false
```

Gem, Workspace Studio, and Notebook are therefore input/synthesis surfaces. They cannot independently upgrade a claim into confirmed truth, write an authoritative Feature Delivery Case, approve a manager commitment, or issue delivery authority.

## Availability Boundary

The public canonical source records all target availability as `unknown`.

Account edition, admin policy, UI placement, source access, language, and product rollout can change what a downstream user can actually invoke. Only the downstream account may record an observed enabled/disabled state. The public repository must not convert one account observation into a universal product contract.

## Public / Private Boundary

Public Lattice may contain only:

- the adapter specification;
- schema and validator;
- public-safe tests;
- future public templates and synthetic fixtures.

Private downstream owns:

- Gmail, Drive, Chat, Notebook sources and permissions;
- real employee/customer/business context;
- account-specific availability;
- private Feature Delivery Cases;
- real candidate outputs, decisions, actions, outcomes, and attention measurements.

No private locator, employee email, account-specific source URL, live case, or adoption observation is added by this PR.

## Compatibility

This PR is additive.

It does not change:

- `docs/senior-attention.md` task semantics;
- `senior-attention-runtime@1.0.0` permissions or activation policy;
- any existing Skill version or behavior;
- active module boundaries;
- Evidence Wayfinding / reserved evaluation contracts;
- merge, release, deployment, promotion, or `team_available` authority.

The adapter contract is intentionally not registered as a new task capability in `registry/capability-manifest.json`. It is a provider projection contract over existing capabilities, not an independently routable Skill/profile/workflow. A future change should register a capability only if a distinct independently useful and governable capability actually emerges.

## Validation

CI validates:

```text
schema syntax
canonical adapter source syntax
Draft 2020-12 instance conformance
semantic adapter invariants
mutation regressions
public/private boundary
Python compilation / diff hygiene
```

Mutation cases include target availability overclaim, authority expansion, complete-search assumptions, private Google locator leakage, dropped counterevidence/unknowns, and accidental creation of a Google-specific task Skill/Agent/module.

## Next Gate

GW-2 may add deterministic renderers and three thin public projections only after this contract is green and reviewed.

GW-2 must not duplicate task semantics. It must derive from this canonical source and preserve an adapter-source hash so drift between Gem, Workspace Studio, and Notebook projections is detectable.
