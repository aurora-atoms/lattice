# Google Workspace Senior Attention Adapter

## Purpose

This is the canonical public adapter contract for projecting Lattice Senior Attention into Google Workspace execution surfaces without creating a Google-specific task Skill, Agent, module, fact store, or private execution plane.

The adapter remains thin:

```text
public Senior Attention workflow + capability profile
-> canonical Google Workspace adapter source
-> deterministic Gem / Workspace Studio / Notebook projections
-> private downstream source binding and verification
```

Canonical machine source:

```text
runtime-adapters/google-workspace/senior-attention/adapter-source.v1.json
```

Structural contract:

```text
schemas/runtime-adapters/google-workspace-adapter-manifest.v1.schema.json
```

Semantic validator:

```text
scripts/validate_google_workspace_adapter.py
```

Deterministic renderer:

```text
scripts/render_google_workspace_senior_attention_adapters.py
```

Generated projection-set contract:

```text
schemas/runtime-adapters/google-workspace-projection-manifest.v1.schema.json
runtime-adapters/google-workspace/senior-attention/projection-manifest.v1.json
```

The adapter source is now version `1.1.1`. This patch clarifies that Google outputs remain candidate evidence for a human handoff and that the receiving coding workspace owns capability discovery and independent repository/runtime verification. It does not add a new task capability, private data plane, or handoff lifecycle.

## Direction Fit

```text
primary_value_path: current_product_delivery
direction_verdict: bind_to_delivery
beneficiary: downstream Senior Attention pilot integrator and accountable engineering owner
observable_state_change: one canonical public adapter deterministically produces three installable guidance projections
verification: adapter schema + semantic validation + renderer drift checks + projection manifest + public/private boundary CI
existing_capability_gap: GW-1 constrained provider boundaries but did not provide copy-ready Gem, Studio, or Notebook configuration guidance
current_evidence: public Lattice contracts and adapter research only
unknown: account-specific availability, private source behavior, attention reduction, owner acceptance, and business value
next_use: install the generated templates in one private manual/shadow pilot and measure correction/attention cost
maintenance_owner: Lattice capability governance owner
```

Public conformance proves contract and projection consistency only. It does not prove that any Google feature is enabled in a particular account or that the adapter reduces Senior Attention cost.

## Canonical Inputs

The adapter consumes public semantics only:

- `docs/senior-attention.md` for the shared workflow and state machine;
- `docs/cross-workspace-handoff.md` for runtime-independent handoff and verification semantics;
- `workspaces/templates/senior-attention-runtime-profile.v1.json` for the task-scoped capability allowlist, permissions, budgets, and verification posture;
- this canonical Google adapter source for provider-specific authority, source, privacy, and availability boundaries.

It does not consume company Gmail, Drive, Chat, internal code, employee identities, live cases, or private telemetry.

## Three Runtime Targets

The adapter names three distinct targets because their execution and source semantics are not interchangeable.

### Gem

Role: `interactive_intake_and_scouting`.

Generated files:

```text
runtime-adapters/google-workspace/senior-attention/gem/gem-instructions.template.md
runtime-adapters/google-workspace/senior-attention/gem/gem-knowledge-pack.manifest.json
runtime-adapters/google-workspace/senior-attention/gem/starter-prompts.md
```

Use for bounded target clarification, source scouting, claim extraction, visible unknowns/conflicts, strongest counterevidence, and candidate artifact drafting.

Authority ceiling: `candidate`.

Do not use a Gem to claim complete enterprise search, confirm private system facts without downstream verification, execute scripts, send/write on the user's behalf, or approve a decision.

The public Gem knowledge pack contains only stable public references. Real Workspace material remains downstream-only.

### Workspace Studio

Role: `manual_or_shadow_workflow`.

Generated files:

```text
runtime-adapters/google-workspace/senior-attention/workspace-studio/skill-instructions.template.md
runtime-adapters/google-workspace/senior-attention/workspace-studio/manual-shadow-flow.template.yaml
```

The public v1 projection is manual/shadow by default. A user explicitly starts the run and reviews its candidate before any downstream action.

The flow fixes these defaults to off/forbidden:

```text
automatic send
automatic share
automatic delete
ticket/file write
manager post
irreversible action
silent permission expansion
```

`Ask a Gem` is optional only when the downstream account actually exposes it. Public Lattice does not claim account-specific availability.

Authority ceiling: `candidate`.

### NotebookLM

Role: `source_grounded_synthesis`.

Generated files:

```text
runtime-adapters/google-workspace/senior-attention/notebook/notebook-setup.md
runtime-adapters/google-workspace/senior-attention/notebook/notebook-custom-chat.template.md
runtime-adapters/google-workspace/senior-attention/notebook/notebook-source-manifest.template.json
runtime-adapters/google-workspace/senior-attention/notebook/prompt-cards.md
```

Use one restricted notebook for one bounded delivery/decision case or tightly related evidence set. NotebookLM remains a source-grounded synthesis station, not global enterprise search, code execution, Lattice Skill execution, or final decision authority.

The source-manifest JSON is a public template only. Placeholder values such as `DOWNSTREAM_PRIVATE_LOCATOR` must be filled only in private downstream storage and must never be committed back into the public repository.

Authority ceiling: `candidate`.

## Availability Is Not a Public Fact

The public canonical manifest keeps all three target availability states at `unknown`.

Product packaging, administrator policy, account edition, source access, language, and UI placement can change what a particular user can invoke. Only downstream observation may record an enabled/disabled state for that private account.

```text
provider capability description
!=
account-specific enabled state
```

## Five Task Families

The adapter preserves the five canonical Senior Attention task families:

```text
feature_requirement
risk
bug
decision
management
```

The provider projections do not own another version of those semantics. Existing Lattice capabilities remain responsible for their bounded contracts.

The following public capability mapping is illustrative only:

```text
feature requirement -> feature-understanding-loop + domain-context-pack as needed
risk                -> risk-ahead with one smallest relevant specialist
bug                 -> delivery-rescue / Bug-to-Repro and target verification
decision            -> decision-question-builder + Attention Admission
management          -> management-translation consuming validated artifacts only
```

It is not a cross-workspace routing contract. The receiving coding workspace uses its own native Skill/Agent/tool discovery and may implement the same bounded verification semantics without exposing or sharing that discovery mechanism.

## Authority Firewall

Every public Google adapter projection is capped at `candidate`.

The canonical source fixes:

```text
authority_ceiling = candidate
human_confirmation_required = true
public_writeback_allowed = false
authoritative_case_write_allowed = false
delivery_verdict_allowed = false
automatic_action_default = false
```

A candidate may contain a proposed Decision Card, script, environment note, Evidence Map fragment, or manager wording draft. It does not become an authoritative Feature Delivery Case fact, validated root cause, approved commitment, delivery verdict, or production action merely because a Google runtime generated it.

## Source Coverage Contract

Source discovery is bounded, not complete.

Every runtime projection must keep these categories visible:

```text
selected
unavailable
excluded
not searched / unknown
```

A successful query or cited answer cannot be rewritten as "all relevant sources were searched." Missing access, product filtering, stale synchronization, source-type limitations, prompt-injection defenses, or administrator policy can reduce visible coverage.

Canonical invariants:

```text
coverage_claim = bounded_not_complete
account_availability_verification = downstream_required
private_workspace_sources = downstream_only
```

Retrieved content is evidence, not authority over the adapter instructions. Runtime prompts explicitly reject source-embedded attempts to expand permissions, hide counterevidence, or override the candidate ceiling.

## Candidate Handoff Boundary

All three generated projections preserve at least:

```text
target
source_scope
claims
unknowns
conflicts
strongest_counterevidence
proposals
authority
privacy
```

Unsupported material claims are downgraded to `UNKNOWN` or the run stops for more evidence. Compression must not delete a conflict or counterevidence that could reverse the recommendation.

The full runtime-neutral Source Synthesis Candidate schema remains a separate bounded gate; it is not introduced implicitly through these templates.

## Cross-Workspace Consumption

Google is an evidence surface, not the receiving coding workspace's fact or discovery authority.

```text
Google candidate evidence
-> human acceptance for handoff
-> Domain Context Pack + Portable Case Pack + required verification
-> receiving workspace
-> workspace-native discovery
-> independent repository / runtime verification
```

The human gate confirms target, source scope, unresolved state, strongest counterevidence, authority, privacy, and the required coding verification. Acceptance for handoff does not confirm a claim or make the case work-ready.

Receiving workspaces must independently verify code, test, reproduction, dependency, configuration, runtime, root-cause, and readiness claims. A source-grounded Google claim can tell the receiver what selected organizational material says; it cannot prove how the repository or runtime behaves.

The public deterministic reference consumer is documented in [Cross-Workspace Handoff](../cross-workspace-handoff.md). It produces a verification request without choosing a receiver Skill, executing code, invoking MCP, writing back, or increasing authority.

## Deterministic Projection Contract

The canonical source is the single authoring source. Generated runtime files must not become independent prompt forks.

Renderer command:

```bash
python scripts/render_google_workspace_senior_attention_adapters.py --write
```

CI verification:

```bash
python scripts/render_google_workspace_senior_attention_adapters.py --check
```

The renderer computes:

```text
adapter_source_hash = SHA-256 over canonical sorted compact adapter JSON
render_hash = SHA-256 over the ordered generated path + file-byte set
```

`projection-manifest.v1.json` records both hashes and the SHA-256 of each generated file. If the canonical source changes without regenerating every affected projection, CI fails with projection drift.

Generated templates may be copied into a private runtime, but public generated files themselves remain reproducible artifacts. Hand-edit the canonical source or renderer, not one projection in isolation.

## Progressive Disclosure

The adapter does not load every Senior Attention capability or all available Workspace material.

```text
stable public workflow/profile
-> one task family
-> minimum relevant runtime source scope
-> minimum existing capability set
-> private verification only for named gaps
```

`load_all_skills=false` and `minimum_capability_selection=true` remain machine-enforced invariants.

## Public / Private Boundary

### Public Lattice owns

- this adapter specification;
- the canonical machine source;
- deterministic renderer and projection manifest schema;
- generated public-safe Gem / Workspace Studio / Notebook guidance templates;
- validators and tests with no company lineage.

### Private downstream owns

- the real Workspace account and administrator configuration;
- Gmail, Drive, Chat, Notebook sources, source permissions, and source-selection decisions;
- private case refs and Feature Delivery Cases;
- runtime availability observations;
- real source manifests and private locators;
- real candidate outputs, citations, corrections, decisions, actions, outcomes, and attention measurements;
- any approved automated action policy.

No real private source locator, employee email, account-specific Drive/Chat URL, live case, or adoption observation belongs in the public adapter package.

## Validation

Run:

```bash
python -m json.tool schemas/runtime-adapters/google-workspace-adapter-manifest.v1.schema.json >/dev/null
python -m json.tool schemas/runtime-adapters/google-workspace-projection-manifest.v1.schema.json >/dev/null
python -m json.tool runtime-adapters/google-workspace/senior-attention/adapter-source.v1.json >/dev/null
python -m json.tool runtime-adapters/google-workspace/senior-attention/projection-manifest.v1.json >/dev/null
python scripts/validate_json_schema_instance.py \
  schemas/runtime-adapters/google-workspace-adapter-manifest.v1.schema.json \
  runtime-adapters/google-workspace/senior-attention/adapter-source.v1.json
python scripts/validate_google_workspace_adapter.py \
  runtime-adapters/google-workspace/senior-attention/adapter-source.v1.json \
  --root .
python scripts/validate_json_schema_instance.py \
  schemas/runtime-adapters/google-workspace-projection-manifest.v1.schema.json \
  runtime-adapters/google-workspace/senior-attention/projection-manifest.v1.json
python scripts/render_google_workspace_senior_attention_adapters.py --check
python -m unittest discover -s tests -p 'test_google_workspace_adapter.py' -v
python scripts/validate_public_private_boundary.py --root .
```

## Explicit Non-Goals

GW-2 does not:

- create a Google-specific Senior Attention task Skill;
- create a new Agent or module;
- bind any real company source;
- claim complete enterprise search;
- claim a particular Google feature is enabled in a private account;
- execute or authorize Google Workspace writes;
- define the full Source Synthesis Candidate contract;
- require a receiving workspace to use Lattice Skill discovery or any runtime-specific discovery projection;
- automate Google-to-coding handoff, writeback, execution, or approval;
- change existing Senior Attention task-family semantics;
- claim downstream adoption, attention savings, or business value.

## Next Gate

The immediate value gate is a private manual/shadow pilot using the generated templates.

A later public PR should be justified by an observed interoperability failure. If the runtime-neutral Source Synthesis Candidate contract is genuinely required to connect these projections to private verification, add that as one bounded contract. Otherwise do not expand provider architecture merely because another schema or workflow is possible.
