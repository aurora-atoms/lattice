# Evidence Wayfinding Contract Phase — Plan Review

## Decision

Proceed with a contract-first implementation of Evidence Wayfinding as a **reference workflow + Capability Profile + portable handoff schema + synthetic conformance fixture**.

Do not create a new Lattice module, a new general research Agent, or an immediately active `frontier-practice-scout` Skill in this change.

## Why the source plan was adjusted

The Evidence Wayfinding blueprint correctly proposes a portable decision-ready workflow rather than a new module. Since that blueprint was prepared, the repository added two enforceable governance contracts:

1. the Direction Investment Gate, which requires evidence of independent value or second-use demand before investing in a team-reuse capability; and
2. the Capability Profile runtime contract, which separates Agent role behavior from model, Skill, tool, knowledge, permission, cache, telemetry, and verification authority.

The implementation plan therefore preserves the blueprint's intent while applying the repository's newer gates.

## Review Matrix

| Proposed change | Review | Final action |
|---|---|---|
| New Evidence Wayfinding module | Duplicates existing active module boundaries. | Reject. Keep Evidence Wayfinding as a reference workflow. |
| New universal research Agent | Duplicates `delivery-capability-conductor` role and weakens the Agent/Profile boundary. | Reject. Reuse `delivery-capability-conductor@1.0.0`. |
| `senior-decision-wayfinding` capability configuration | Fits the Capability Profile runtime contract and can bind the minimum task-scoped capability set. | Implement a public synthetic runtime profile. |
| Portable Case Pack | Cross-runtime state is a schema/projection concern, not a Skill. | Implement `lat.portable_case_pack.v1`. |
| `frontier-practice-scout` immediately as a Skill | Direction gate lacks downstream second-use evidence and distinct trigger/output evals. | Defer promotion; retain a workflow stage and explicit promotion criteria. |
| Runtime-specific Gemini / NotebookLM / Copilot adapters | Public Lattice should own portable contracts; provider bindings and private evidence belong downstream. | Defer to downstream adapters after the portable contract stabilizes. |
| Automatic self-improvement | Risks target drift and false-pass propagation. | Reject. Use candidate -> replay/holdout -> human review -> versioned promotion/rejection -> rollback. |

## Implemented Scope

- `docs/evidence-wayfinding.md`
  - Mission Anchor and north-star constraints.
  - ordered ten-stage reference workflow.
  - minimal capability composition and stop rules.
  - human-attention progressive disclosure.
  - verification and governed evolution rules.
  - explicit frontier-research promotion gate.
- `schemas/capability/portable-case-pack.v1.schema.json`
  - bounded cross-Agent/cross-runtime claim and evidence handoff.
  - observed / derived / judged / unknown separation.
  - conflicts, strongest counterevidence, rejected directions, source gaps, falsification, and data classification.
- `examples/capability-profiles/senior-decision-wayfinding-runtime-profile.v1.json`
  - existing conductor Agent.
  - existing Skills only.
  - read-only GitHub MCP.
  - no merge/deploy/secret authority.
  - model-lane, verification, cache, human-factor, and telemetry boundaries.
- `examples/evidence-wayfinding/portable-case-pack.synthetic.v1.json`
  - public synthetic conformance example only; no downstream adoption claim.
- `tests/test_evidence_wayfinding.py`
  - profile boundary validation.
  - read-only and no-premature-frontier-promotion assertions.
  - portable handoff shape and evidence-reference checks.
  - no authoritative reasoning-transcript handoff.
  - governed evolution and no-progress stop rule checks.

## Preserved Boundaries

This change does not reclassify or replace Helixion, AegisFlow, Memexa, FlowGuard, OpenClaw, or DeliveryYield.

- AegisFlow may orchestrate bounded state transitions.
- FlowGuard retains scope, permission, and approval enforcement.
- Memexa retains source-scoped state and append-only history.
- Helixion may create cross-run improvement candidates and route them through evaluation/promotion governance.
- OpenClaw remains an active execution-related module with no scope change in this PR.
- DeliveryYield measures economics after quality evidence; it does not approve a decision or delivery.

## Validation Plan

Deterministic checks:

```bash
python scripts/validate_capability_profile.py --root .
python -m json.tool schemas/capability/portable-case-pack.v1.schema.json >/dev/null
python -m json.tool examples/evidence-wayfinding/portable-case-pack.synthetic.v1.json >/dev/null
python -m unittest discover -s tests -p 'test_evidence_wayfinding.py' -v
python -m unittest discover -s tests -p 'test_capability_profile_runtime.py' -v
python scripts/generate_capability_registry_projections.py --check --root .
git diff --check main...HEAD
```

## Follow-up Gate for `frontier-practice-scout`

Open a separate Skill-authoring change only after at least two governed real or replayable cases show all of the following:

- current external primary-source research materially changed a bounded decision or prevented a stale recommendation;
- existing context/understanding capabilities plus on-demand research cannot express the trigger/output boundary cleanly;
- the new capability has a named maintainer and retirement trigger;
- run/skip trigger evals and output-quality evals exist;
- promotion does not grant automatic write, policy, asset-promotion, delivery, merge, or release authority.

This preserves expansion without silently promoting a speculative capability into the public runtime.
