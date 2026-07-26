# Reusable Asset Loop Vertical Slice

## Purpose

This reference defines the first bounded Experience-to-Asset implementation inside the existing Feature Delivery Harness testbed. It does not create a new Lattice module and does not authorize automatic promotion.

```text
PR, failure, review comment, or delivery observation
-> experience.contribution
-> reusable_asset.candidate
-> reusable_asset.change_proposal
-> reusable_asset.review
-> reusable_asset.usage_observation
-> Reusable Asset Dossier
```

The Feature Delivery Case remains the common value and evidence boundary. Every record in one vertical slice must use the same `feature_delivery_case_id`.

## Record Responsibilities

- `experience.contribution`: preserves the bounded original contribution, contributor, source, time, and evidence class.
- `reusable_asset.candidate`: describes one versioned candidate, its type, scope, activation, maturity, limitations, owner, and evidence.
- `reusable_asset.change_proposal`: makes create, update, split, merge, reclassify, or deprecate changes reviewable.
- `reusable_asset.review`: records the accountable human decision and validation references.
- `reusable_asset.usage_observation`: records one scoped use and observable outcome without claiming general ROI.
- Reusable Asset Dossier: manager-facing projection of origin, scope, review, usage, limitations, and next iteration.

## Human-Control Boundary

A candidate is not automatically promoted because it was generated, used once, or associated with a successful Feature Delivery Case.

```text
unapproved candidate
  activation_mode = never_by_default
  maturity <= runnable

approved candidate
  may be task_scoped or profile_selected within the reviewed scope

team_available
  requires explicit approved review and separate governance decision
```

The initial fixture approves only `task_scoped` and `used_once`. It does not prove cross-project transferability.

## Evidence Classification

Contributions should distinguish:

- `observed`: directly recorded fact or human comment;
- `derived`: deterministic calculation or comparison;
- `judged`: human or model judgment;
- `unknown`: unresolved information.

Unknown results remain unknown. The dossier must not manufacture ROI, success rates, or organization-wide claims.

## Feature Delivery Case Compatibility

The canonical rich lifecycle entity remains `feature-delivery-case.lifecycle.v1`. The FDH `lat.feature_delivery_case.v1` record is a bounded compatibility projection and uses the runtime-compatible statuses:

```text
draft
ready
in_progress
delivered
failed
blocked
```

The contract-alignment validator checks fields, required fields, `additionalProperties`, and runtime/schema enums so status drift becomes visible in CI.

## Validation

```bash
python feature-delivery-harness-mvp/scripts/validate_contract_alignment.py
python feature-delivery-harness-mvp/scripts/run_reusable_asset_loop.py \
  feature-delivery-harness-mvp/evals/reusable_asset_loop_case_001/input.jsonl \
  --out /tmp/reusable_asset_dossier.md \
  --expected feature-delivery-harness-mvp/evals/reusable_asset_loop_case_001/expected_dossier.md
python -m unittest discover -s tests -p 'test_reusable_asset_loop.py' -v
```

## Deferred

This first PR intentionally defers:

- ingestion from live GitHub PR APIs;
- database or remote registry storage;
- automatic asset matching;
- automatic Skill rewriting;
- team-wide activation;
- organization-level ROI evaluation;
- changes to Helixion, AegisFlow, Memexa, FlowGuard, OpenClaw, or DeliveryYield boundaries.
