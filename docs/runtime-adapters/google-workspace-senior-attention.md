# Google Workspace Senior Attention Adapter

## Purpose

This is the canonical public adapter contract for projecting Lattice Senior Attention into Google Workspace execution surfaces without creating a Google-specific task Skill, Agent, module, fact store, or private execution plane.

The adapter is deliberately thin:

```text
public Senior Attention workflow + capability profile
-> canonical Google Workspace adapter source
-> later runtime-specific projections
-> private downstream source binding and verification
```

The canonical machine source is:

```text
runtime-adapters/google-workspace/senior-attention/adapter-source.v1.json
```

Its structural contract is:

```text
schemas/runtime-adapters/google-workspace-adapter-manifest.v1.schema.json
```

Its semantic validator is:

```text
scripts/validate_google_workspace_adapter.py
```

GW-1 intentionally stops before rendered Gem instructions, Workspace Studio flows, Notebook setup cards, or a Source Synthesis Candidate record contract. Those belong to later bounded adapter stages.

## Direction Fit

```text
primary_value_path: current_product_delivery
direction_verdict: bind_to_delivery
beneficiary: downstream Senior Attention pilot integrator and accountable engineering owner
observable_state_change: Google runtime boundaries become explicit and machine-checkable before any private source binding
verification: schema + semantic validator + mutation tests + public/private boundary CI
existing_capability_gap: Senior Attention already defines task semantics, but no public Google runtime contract constrains authority, source binding, availability, or surface differences
current_evidence: public Lattice contracts and adapter research only
unknown: account-specific availability, private source behavior, attention reduction, owner acceptance, and business value
next_use: render three thin projections, then run one private manual/shadow pilot
maintenance_owner: Lattice capability governance owner
```

The adapter is not independently valuable as a platform. Its value must be tested inside a real downstream delivery or validation case.

## Canonical Inputs

The adapter consumes public semantics only:

- `docs/senior-attention.md` for the shared workflow and state machine;
- `workspaces/templates/senior-attention-runtime-profile.v1.json` for the task-scoped capability allowlist, permissions, budgets, and verification posture;
- public capability contracts and public-safe metadata when a later renderer needs them.

It does not consume company Gmail, Drive, Chat, internal code, employee identities, live cases, or private telemetry.

## Three Runtime Targets

The adapter names three different runtime targets because their execution and source semantics are not interchangeable.

### Gem

Role: `interactive_intake_and_scouting`.

Use for interactive target clarification, bounded source scouting, candidate claim extraction, visible unknowns/conflicts, strongest counterevidence, and candidate artifact drafting.

Authority ceiling: `candidate`.

Do not use a Gem to claim complete enterprise search, confirm private system facts without downstream verification, execute scripts, or publish/approve a decision.

### Workspace Studio

Role: `manual_or_shadow_workflow`.

Use for a reusable manual skill or shadow flow in the user's existing Workspace context. A later projection may use Ask a Gem when the target account exposes it.

Authority ceiling: `candidate`.

Automatic send, cross-domain or irreversible writes, silent permission expansion, and decision publication are forbidden by default. Any later action-capable integration requires a separate downstream permission and human-approval boundary.

### Notebook

Role: `source_grounded_synthesis`.

Use for synthesis over a human-curated, approved source set with citations, conflicts, unknowns, and strongest counterevidence preserved.

Authority ceiling: `candidate`.

Do not assume dynamic enterprise-global search, code execution, Lattice Skill execution, or final decision authority. Notebook output remains a source-grounded candidate until private verification.

## Availability Is Not a Public Fact

The public canonical manifest sets all three target availability states to `unknown`.

That is intentional. Product packaging, administrator policy, language, account edition, source access, and UI placement can change what a particular user can use. A downstream integration may observe that a surface is available or disabled for its own account, but that observation must remain private and must not be back-projected into this public canonical source as a universal claim.

Public contract rule:

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

A runtime target does not own a new version of these task semantics.

The expected downstream mapping remains:

```text
feature requirement -> feature-understanding-loop + domain-context-pack as needed
risk                -> risk-ahead with one smallest relevant specialist
bug                 -> delivery-rescue / Bug-to-Repro and target verification
decision            -> decision-question-builder + Attention Admission
management          -> management-translation consuming validated artifacts only
```

The Google surfaces help gather or synthesize candidate inputs. Existing Lattice capabilities remain responsible for their bounded public contracts.

## Authority Firewall

Every public Google adapter output is capped at `candidate`.

The canonical contract fixes:

```text
authority_ceiling = candidate
human_confirmation_required = true
public_writeback_allowed = false
authoritative_case_write_allowed = false
delivery_verdict_allowed = false
automatic_action_default = false
```

A candidate may contain a proposed Decision Card, script, environment note, Evidence Map fragment, or manager wording draft. None of those becomes an authoritative Feature Delivery Case fact, validated root cause, approved commitment, delivery verdict, or production action merely because a Google runtime generated it.

## Source Coverage Contract

Source discovery is bounded, not complete.

The adapter requires later runtime projections and downstream integrations to distinguish:

```text
selected
unavailable
excluded
not searched / unknown
```

A successful query or cited answer cannot be reworded as "all relevant sources were searched." Missing access, product filtering, stale synchronization, source-type limitations, prompt-injection defenses, or administrator policy can reduce visible coverage.

The canonical source therefore fixes:

```text
coverage_claim = bounded_not_complete
account_availability_verification = downstream_required
private_workspace_sources = downstream_only
```

## Candidate Handoff Boundary

GW-1 only freezes the required handoff sections. The runtime-neutral candidate schema is a later bounded change.

Any later Gem, Studio, or Notebook projection must preserve at least:

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

Unsupported claims are downgraded to `UNKNOWN` or the run stops for more evidence. Compression must not delete a conflict or counterevidence that could reverse the recommendation.

## Progressive Disclosure

The adapter does not load every Senior Attention capability or all available Workspace material.

```text
stable public workflow/profile
-> one task family
-> minimum relevant runtime source scope
-> minimum existing capability set
-> private verification only for named gaps
```

`load_all_skills=false` and `minimum_capability_selection=true` are machine-enforced invariants.

## Public / Private Boundary

### Public Lattice owns

- this adapter specification;
- the canonical machine source;
- public schemas, validators, tests, and later public-safe projection templates;
- synthetic fixtures that contain no company lineage.

### Private downstream owns

- the real Workspace account and administrator configuration;
- Gmail, Drive, Chat, Notebook sources, source permissions, and source-selection decisions;
- private case refs and Feature Delivery Cases;
- runtime availability observations;
- real source coverage, citations, corrections, decisions, actions, outcomes, and attention measurements;
- any approved automated action policy.

No real private source locator, employee email, account-specific Drive/Chat URL, live case, or adoption observation belongs in the public adapter source.

## Validation

Run:

```bash
python -m json.tool schemas/runtime-adapters/google-workspace-adapter-manifest.v1.schema.json >/dev/null
python -m json.tool runtime-adapters/google-workspace/senior-attention/adapter-source.v1.json >/dev/null
python scripts/validate_json_schema_instance.py \
  schemas/runtime-adapters/google-workspace-adapter-manifest.v1.schema.json \
  runtime-adapters/google-workspace/senior-attention/adapter-source.v1.json
python scripts/validate_google_workspace_adapter.py \
  runtime-adapters/google-workspace/senior-attention/adapter-source.v1.json \
  --root .
python -m unittest discover -s tests -p 'test_google_workspace_adapter.py' -v
python scripts/validate_public_private_boundary.py --root .
```

The semantic validator additionally rejects account-specific availability claims, target/role drift, authority expansion, complete-search assumptions, private locator leakage, loss of unknown/counterevidence handoff sections, and eager capability loading.

## Explicit Non-Goals

GW-1 does not:

- create rendered Gem instructions;
- create a Workspace Studio skill/flow;
- create a Notebook setup package;
- define the full Source Synthesis Candidate schema;
- create or modify a task Skill;
- create a new Agent or module;
- bind any real company source;
- execute or authorize Google Workspace writes;
- claim downstream adoption, attention savings, or business value.

## Next Gate

The next bounded adapter step, if this contract remains justified after review, is deterministic projection of the same canonical source into three copy-ready public templates:

```text
Gem instruction projection
Workspace Studio manual/shadow projection
Notebook setup/custom-chat projection
```

That renderer must preserve the authority ceiling, public/private boundary, source-coverage caveat, and adapter-source hash. It must not become a second source of task semantics.
