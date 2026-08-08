# Evidence Wayfinding Blueprint Preservation — PR 6

## Context

PR #34 implemented the contract-first phase of Evidence Wayfinding: reference workflow, Portable Case Pack, synthetic runtime profile, validation, and tests. The source blueprint also contained substantially more design intent than the initial operational document captured, including VDY, claim lifecycle, EIR/ECR, receipts, cross-runtime conformance, asset lifecycle, rollout, pre-mortem, source ledger, and the proposed `frontier-practice-scout` Skill.

The follow-up request was to continue toward the blueprint, add or modify Skills if justified, and ensure the blueprint is documented in enough detail that future work does not lose the original design.

## Review

### New Skill review

The candidate `frontier-practice-scout` is still **not ready for active Skill creation**.

Reason:

- PR #34 merging did not create second-use evidence.
- The Direction Investment Gate requires value evidence before capability investment.
- The repository still lacks at least two governed cases demonstrating distinct decision-changing value beyond ordinary on-demand research.
- Trigger/output boundaries remain design hypotheses rather than replay-validated contracts.
- A maintained Skill would therefore be premature and would violate the blueprint's own anti-self-promotion principle.

Verdict: `retain_candidate`.

### Existing Skill modification review

No existing Skill is modified in this PR.

Reason:

- `delivery-capability-conductor` already owns minimum-capability routing and stop behavior.
- `feature-understanding-loop`, `context-mastery`, `system-mental-model`, challenge Skills, `decision-question-builder`, delivery artifacts, and outcome-learning capabilities already cover the workflow roles described by the blueprint.
- Adding Evidence Wayfinding-specific wording to generic Skills would create version churn and tighter coupling without observed behavior evidence.
- The correct abstraction is a `reference_workflow` plus Capability Profile, which is already the repository taxonomy.

Verdict: reuse existing Skills; change them later only when a replay or real case exposes a concrete behavior, trigger, output, or authority gap.

## Changes

- Preserve the complete source-aligned blueprint in `docs/evidence-wayfinding/blueprint-preserved.md`.
- Preserve the deferred `frontier-practice-scout` candidate, Direction Fit rationale, output concept, run/skip seed cases, and explicit promotion gate in `docs/evidence-wayfinding/frontier-practice-scout-candidate.md`.
- Preserve cross-runtime adapter invariants and five common conformance tests in `docs/evidence-wayfinding/runtime-conformance.md`.
- Preserve VDY, correctness ladder, claim lifecycle, EIR/ECR, candidate lifecycle, evaluation design, rollout, and rollback in `docs/evidence-wayfinding/evaluation-and-evolution.md`.
- Update `docs/evidence-wayfinding.md` to link the preserved blueprint and explicitly state the no-premature-Skill rule.
- Add Evidence Wayfinding to the logical workflow families in `docs/capability-taxonomy.md` without creating a new module or active capability package.

## Source preservation policy

The preservation document keeps source identifiers `I1-I7`, `R1-R10`, and `E1-E11` so later work can distinguish internal design material, repository evidence, and external first-party evidence.

Internal source contents are not copied into the public repository. External provider facts remain dated to the source blueprint's `2026-08-07` evidence cutoff and must be reverified before implementation.

## Deferred implementation items

The following remain intentionally unimplemented:

- active `frontier-practice-scout` Skill;
- runtime-specific adapters;
- separate Decision Card schema;
- separate Outcome Receipt schema;
- separate Evolution Proposal schema;
- replay/holdout corpus;
- VDY baseline thresholds;
- automatic or default Evidence Wayfinding activation.

Each requires either stable downstream consumption evidence, replay evidence, or current provider verification. Documentation preserves the intended contracts so deferral does not become loss.

## Architectural boundaries

This PR does not:

- create or rename a Lattice module;
- reclassify Helixion, AegisFlow, Memexa, FlowGuard, OpenClaw, or DeliveryYield;
- create a new Agent;
- change runtime permissions;
- grant repository write, merge, release, deployment, or asset-promotion authority;
- convert a candidate into organizational truth.

## Follow-up trigger

Reopen active Skill authoring only when a case set can satisfy the promotion gate in `docs/evidence-wayfinding/frontier-practice-scout-candidate.md`.
