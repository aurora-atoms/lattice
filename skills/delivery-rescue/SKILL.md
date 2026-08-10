---
name: delivery-rescue
description: Use for evidence-grounded diagnosis of CI failures, bug reproduction, local environment failures, and contract-breaking changes that block delivery; do not use for feature planning, release approval, production deployment, or speculative diagnosis without source evidence; input is bounded logs, diffs, environment facts, contracts, tests, and Feature Delivery Case context; output is a ranked root-cause assessment, minimum next action, validation command, evidence classification, human confirmation points, and bounded write-back that preserves behavioral constraints, safety, and quality-adjusted token ROI.
---

# Delivery Rescue

## Goal

Move one blocked Feature Delivery Case to a verified next action or restored working state without converting symptoms, correlations, or model confidence into unsupported root-cause claims.

## Use When

Select the smallest sufficient atomic path:

```text
A01 Red-to-Green CI Diagnosis
A02 Bug-to-Repro
A03 Environment Doctor
A04 Contract Break Detector
```

Use the Bug Investigation machine contract when A02 requires an independently reviewable reproduction, hypothesis, falsification, and fix-readiness boundary.

## Do Not Use When

Do not use for feature planning, release approval, production deployment, broad log summarization, or unsupported speculation. Do not use a Bug Investigation packet to approve merge, release, deployment, architecture, security, compliance, business scope, or production changes.

## Inputs

Use one task-bounded Feature Delivery Case with the minimum authorized logs, diff, tests, environment facts, contracts, permissions, evidence references, expected behavior, and observed failure needed for the selected path.

For A02, require enough evidence to distinguish reproduction state, direct observations, hypotheses, material alternatives, verification tests, unknowns, and the next falsifiable step. Missing evidence remains visible rather than being inferred.

## Outputs

Return the smallest visible artifact needed by the selected path. For A02, emit `lat.bug_investigation.v1` as JSON conforming to `schemas/bug-investigation.v1.schema.json` and the structured capability run result.

Default writeback:

```text
artifacts/delivery-rescue/<case-id>/<run-id>/bug-investigation.v1.json
artifacts/capability-runs/delivery-rescue/<run-id>/run-result.json
```

When write permission is unavailable, return the complete structured result inline with `write_status=returned_inline`.

The Bug Investigation packet records target scope, blocker, reproduction state, observations, hypotheses, verification tests, root-cause claim strength, strongest material alternative when applicable, one minimum next step, fix readiness, evidence summary, and human confirmation points.

## Machine Contract

`schemas/bug-investigation.v1.schema.json` defines the public shape. `scripts/validate_bug_investigation.py` applies structural and semantic gates.

The validator fails closed when:

- a reproduced failure lacks steps or evidence;
- a verification result references no known hypothesis or lacks evidence;
- a supported or verified root-cause claim lacks a controlled or falsifiable verification result;
- a material competing explanation is hidden when it remains live;
- a repair is proposed before reproduction or while root cause remains unknown;
- fix readiness ignores blocking unknowns or unresolved material alternative risk;
- evidence references are not addressable;
- a public synthetic fixture claims downstream adoption.

A correlated log line, timing coincidence, or model ranking can strengthen a hypothesis but cannot by itself verify root cause.

## Evidence

Separate source-supported facts from inference. Preserve addressable evidence references, reproduction evidence, counterevidence, uncertainty, unknowns, assumptions, and applicability limits.

Direct observations and controlled-change results are evidence. Hypotheses remain hypotheses until bounded verification changes their status. Record the strongest material alternative capable of reversing the root-cause conclusion when one exists. Do not infer causality from correlation, temporal proximity, stack position, or frequency alone.

When evidence cannot support a reliable next claim or safe fix-readiness boundary, stop with insufficient evidence rather than continuing speculative analysis.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- the blocker and expected behavior are bounded to the Feature Delivery Case;
- reproduction state is explicit and evidence-backed;
- facts, hypotheses, counterevidence, and unknowns remain distinguishable;
- material alternatives are visible when applicable;
- the minimum next step can falsify, reproduce, repair, collect evidence, or escalate with an observable signal;
- fix readiness does not exceed the current evidence strength;
- schema and semantic validation pass for a Bug Investigation packet;
- human authority over scope, merge, release, deployment, and production is preserved.

Producing a packet is not success when the evidence or validation signals are not met.

## Stop Conditions

Stop at the requested artifact or next reviewable stage. Stop without repeated probing when required evidence, permission, source access, reproduction prerequisites, or owner input is missing; when validation fails after one bounded corrective retry; when a second investigation step produces no new evidence or risk reduction; or when security, privacy, compliance, architecture, production, business-scope, or other human-authority boundaries are reached.

If the failure is not reproduced, root cause is unknown, a blocking unknown remains, or the strongest material alternative is unresolved, do not mark the case `ready_for_bounded_fix`. Return the smallest missing evidence or next falsification step instead.

## Workflow

1. Bound the Feature Delivery Case, failure, expected behavior, scope, non-scope, permissions, and evidence cutoff.
2. Query ConPort before loading or searching the full skill text when ConPort is available; otherwise use targeted source reads.
3. Select one atomic path before composing several.
4. Load only the minimum authorized evidence and keep stable rules, schema, and output contract in the stable prefix while task evidence stays in the dynamic suffix.
5. For A02, establish reproduction status before proposing a repair-ready state.
6. Record direct observations separately from hypotheses and name material alternatives.
7. Choose one falsifiable or controlled verification step with an expected disconfirming signal.
8. Update hypothesis and root-cause claim strength only from observed evidence.
9. Produce one minimum next step, validation signal, fix-readiness boundary, and human confirmation points.
10. Validate A02 output with `scripts/validate_bug_investigation.py`; perform at most one bounded corrective retry.
11. Stop at the current reviewable state unless the caller explicitly authorizes the next bounded stage.

## Rules

ACAT.001 | MUST | scope | use the Feature Delivery Case as the primary context boundary | enforce
ACAT.002 | MUST | routing | select one atomic capability before composing | enforce
ACAT.003 | MUST | evidence | separate fact inference hypothesis counterevidence and unknown | enforce
ACAT.004 | MUST | context | load the minimum authorized context instead of a raw dump | enforce
ACAT.005 | MUST | human | preserve owner confirmation and final judgment | enforce
ACAT.006 | MUST | token | optimize quality-adjusted token ROI | enforce
ACAT.007 | SHOULD | prompt | keep stable rules schema and output contract in a stable prefix | prefer
ACAT.008 | NEVER | authority | approve merge release deploy production or business scope | block
ACAT.009 | NEVER | memory | auto-promote output to memory belief rule or skill | block
ACAT.010 | MUST | bug | require reproduced evidence before repair-ready status | enforce
ACAT.011 | NEVER | cause | treat correlation timing or model confidence alone as verified root cause | block
ACAT.012 | MUST | challenge | preserve the strongest material alternative until evidence resolves or escalates it | enforce
ACAT.013 | MUST | readiness | block repair-ready status on blocking unknown or unresolved material alternative | enforce

## Verification

```bash
python scripts/validate_skill_package.py --root skills/delivery-rescue
python -m json.tool skills/delivery-rescue/schemas/bug-investigation.v1.schema.json >/dev/null
python skills/delivery-rescue/scripts/validate_bug_investigation.py \
  skills/delivery-rescue/evals/fixtures/valid-bug-investigation.synthetic.json
python -m unittest discover -s skills/delivery-rescue/evals -p 'test_*.py' -v
```

Also verify trigger/output evals, capability-context alignment, semantic version increase, generated registry parity, and the public/private boundary.

## Failure Modes

- treating a flaky symptom or correlated log line as a proven root cause;
- attempting repair before establishing reproducibility or bounded causal support;
- hiding a material competing explanation;
- converting model confidence into evidence strength;
- modifying global or production state without approval;
- silently accepting a breaking contract;
- loading full logs or repositories by default;
- treating public synthetic conformance as private adoption or real defect resolution.
