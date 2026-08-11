# Cross-Workspace Handoff

## Purpose

Cross-workspace handoff is Lattice's public contract for moving one bounded candidate context from an evidence surface into a coding workspace without coupling their runtime, capability discovery, tools, or execution model.

The current pilot boundary is manual:

```text
Google evidence surface
-> candidate evidence
-> human source / authority / privacy gate
-> Domain Context Pack + Portable Case Pack + required verification
-> receiving coding workspace
-> workspace-native capability discovery
-> independent repository / runtime verification
```

Contracts connect contexts. Runtimes do not need to share discovery mechanisms.

## Direction Fit

```text
primary_value_path: current_product_delivery
direction_verdict: bind_to_delivery
beneficiary: a downstream Senior Attention pilot owner moving one bounded Feature or Bug case from Google evidence into coding verification
observable_state_change: the receiving workspace gets a deterministic verification request that preserves the incoming evidence boundary and cannot promote candidate claims
verification: existing Domain Context Pack and Portable Case Pack validators plus cross-workspace positive and mutation conformance
existing_capability_gap: current packs preserve context and case semantics, but no receiver-neutral oracle proves that a coding projection conserves their load-bearing handoff state
current_evidence: public contracts and synthetic conformance only
unknown: real downstream adoption, attention reduction, owner acceptance, and delivery value
next_use: one private manual Google-to-coding Feature case and one Bug case
maintenance_owner: Lattice capability governance owner
```

The verdict is `bind_to_delivery`. This work does not establish a reusable runtime platform, company adoption, or business value.

## Runtime Independence

Native workspaces execute and discover capabilities locally. A receiving workspace may use its own Skill discovery, Agent instructions, tool or MCP configuration, repository-specific selection, and runtime-native workflow.

Lattice standardizes the handoff semantics, not runtime discovery. The canonical handoff must not name a receiver-specific Skill, require `.agents/skills` or `.github/skills`, or depend on Codex-, Claude-, Copilot-, or Gemini-specific discovery behavior. Existing capability mappings may remain as non-binding implementation guidance, but they are not a cross-workspace routing contract.

The shared contract therefore remains useful when either side changes runtime. Interoperability is established by conserved case semantics and deterministic validation, not by proving that two runtimes discover the same capability in the same way.

## Evidence and Truth Boundary

Google Workspace outputs are candidate evidence. A Gem, NotebookLM notebook, or Workspace Studio flow may preserve source statements, citations, summaries, hypotheses, conflicts, counterevidence, and recommendations. Those outputs do not become coding truth because they were source-grounded or cited.

Repository- and runtime-dependent claims require independent receiving-workspace evidence. This includes code behavior, test results, reproduction state, dependencies, configuration, runtime state, root cause, fix readiness, work readiness, and delivery readiness.

```text
Google source says X
!=
repository or runtime proves X
```

Model agreement or model confidence is not an evidence-confirmation mechanism. A receiving workspace must use its own authorized repository, test, runtime, configuration, or dependency evidence and return an addressable verification result.

## Load-Bearing Handoff Semantics

Every conforming handoff preserves at least:

- the bounded target and case reference;
- selected, conditional, excluded, unavailable, and not-searched source scope;
- claims and their incoming evidence status;
- addressable evidence references;
- all unknowns;
- every unresolved conflict;
- the strongest decision-changing counterevidence;
- the candidate authority ceiling;
- privacy and source-boundary classification;
- required receiving-workspace verification, required output, and stop conditions.

`UNKNOWN` and unresolved `CONFLICT` are first-class state. Compression, Markdown conversion, model confidence, or receiver convenience must not turn either into fact. A conflict may be settled only through new evidence or the accountable adjudication path; a handoff projection cannot silently mark it resolved.

Strongest counterevidence is not a generic risk list. It is the most credible current evidence or alternative explanation that could reverse the recommendation, reopen a claim, change the verification plan, narrow scope, or block readiness. It must survive every projection.

## Authority Conservation

Authority may stay the same or be reduced during handoff. It cannot increase.

```text
candidate -> candidate                 allowed
candidate -> unknown / blocked        allowed
candidate -> confirmed                forbidden
candidate -> root_cause_verified      forbidden
candidate -> work_ready               forbidden
candidate -> approved / delivery_ready forbidden
```

Human acceptance means only that the bounded candidate is accepted as input to coding verification. It does not confirm a claim, approve a fix, authorize implementation, or grant merge, release, deployment, architecture, security, compliance, or business authority.

## Canonical Inputs and Deterministic Receipt

The conformance layer reuses:

```text
lat.domain_context_pack.v1
lat.portable_case_pack.v1
```

The Domain Context Pack carries authorized source selection, context items, unknowns, conflicts, and answerability. The Portable Case Pack carries the bounded decision, claims, evidence refs, conflicts, strongest counterevidence, falsification condition, and required output.

The narrow output contract is:

```text
lat.workspace_handoff_verification_request.v1
```

Its schema is `schemas/capability/workspace-handoff-verification-request.v1.schema.json`. The reference consumer in `scripts/validate_cross_workspace_handoff.py` validates both existing packs, checks cross-pack identity and evidence lineage, and deterministically projects:

- `case_ref` and `target`;
- source-scope state and evidence-ref IDs;
- incoming claim IDs and incoming statuses;
- claims requiring repository verification;
- unknown and conflict IDs;
- strongest counterevidence;
- candidate authority and privacy classification;
- required coding verification and output;
- stop conditions;
- the human-handoff boundary;
- receiving-workspace ownership of capability discovery.

The reference consumer does not select a Coding Skill, execute code, call MCP, determine root cause, declare readiness, approve action, send data, or write back to another system. It is a conformance oracle only.

No new Source Synthesis Candidate lifecycle is introduced. The synthetic wrapper used by the conformance tests is a harness fixture format, not another authoritative case record.

## Projection and Fact-System Rule

Google Doc, Markdown, JSON, and runtime-specific views are projections of the same bounded private case state. They are not independent fact systems and must not acquire separate claim strength or lifecycle.

For public conformance, the committed receipt is generated from the two canonical input packs and compared deterministically. In a private implementation, human corrections or verification outcomes return to the private Case Spine through the owning contract; editing a receipt or Markdown view does not change truth.

## Human Orchestration Boundary

Human handoff is the selected safety and observation boundary for the current Google-to-coding pilot. It is not treated as a temporary automation failure.

The human gate confirms the target, source scope, unresolved state, strongest counterevidence, authority ceiling, privacy boundary, and verification request before the receiving workspace begins independent investigation.

Automatic Google-to-coding invocation, automatic send, automatic writeback, automatic code execution, automatic approval, MCP/A2A orchestration, or multi-runtime routing requires a separate Direction Investment Gate and observed demand. None is authorized by this contract.

## Public / Private Boundary

Public Lattice owns:

- the semantic contract and public guidance;
- the verification-request schema;
- the deterministic validator/reference consumer;
- public-safe synthetic Feature and Bug fixtures;
- positive and negative conformance tests.

Private downstream owns:

- real Gmail, Drive, Chat, Notebook, and source-system locators;
- real repositories, code, tests, logs, configuration, and runtime evidence;
- real `feature_delivery_case` records, claims, people, owners, and decisions;
- workspace-specific discovery, Agent instructions, tools, MCP configuration, and runtime policy;
- real handoff acceptance, verification results, outcomes, adoption observations, and attention measurements.

A public-safe receipt carries IDs and classifications, not private source locators. A private locator in a public projection fails closed.

## Synthetic Conformance Boundary

Public fixtures use:

```text
simulation_status = synthetic_reference
downstream_adoption_status = not_observed
```

The Feature fixture proves conservation of a conflicting requirement, an unknown repository state, candidate authority, and repository/test verification requirements. The Bug fixture proves that symptom history and alternative explanations may cross the boundary while root cause and fix readiness remain unverified.

Mutation tests fail when a projection drops an unknown, silently resolves a conflict, removes strongest counterevidence, promotes authority or readiness, verifies root cause by declaration, removes coding verification, leaks a private locator, changes target identity, loses evidence refs, claims complete source search, requires a receiver-specific Skill, claims real adoption, or uses model confidence as confirmation.

Passing public conformance proves contract shape, deterministic projection, conservation behavior, and fail-closed boundaries. It does not prove a Google feature is enabled, a downstream workspace adopted the contract, a Senior saved time, an owner accepted a result, a defect was prevented, a case became work-ready, or production is ready.

## Validation

```bash
python scripts/validate_cross_workspace_handoff.py \
  tests/fixtures/cross-workspace-handoff/feature-requirement.synthetic.json \
  --receipt tests/fixtures/cross-workspace-handoff/feature-requirement.receipt.json
python scripts/validate_cross_workspace_handoff.py \
  tests/fixtures/cross-workspace-handoff/bug-investigation.synthetic.json \
  --receipt tests/fixtures/cross-workspace-handoff/bug-investigation.receipt.json
python -m unittest discover -s tests -p 'test_cross_workspace_handoff_conformance.py' -v
```

## Explicit Non-Goals

This contract does not create a new Skill, Agent, active module, universal discovery mechanism, runtime-specific discovery projection, Coding Harness, generic runtime protocol, Source Synthesis lifecycle, Attention Observation contract, automated orchestration, manager automation, or DeliveryYield authority.
