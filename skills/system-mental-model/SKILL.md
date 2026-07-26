---
name: system-mental-model
description: Use for rapidly understanding an unfamiliar software system, service, codebase, data platform, or operational workflow by building and validating its purpose, runtime topology, key entry points, core modules, workflows, data flows, control points, and impact boundaries. Input is bounded source code, configuration, schemas, tests, traces, official documentation, incidents, and authorized stakeholder explanations; output is an evidence-linked system map, open-question queue, validation plan, and teach-back check. Do not use for raw code summaries, exhaustive repository dumps, unsupported architecture claims, or implementation before critical unknowns are exposed; preserve provenance, uncertainty, validation behavior, security boundaries, and human authority.
---

# System Mental Model

## Goal

Build a verifiable mental model of how a bounded system works at runtime, what controls its behavior, where data moves, and what a change can affect.

## Use When

Use for unfamiliar-system onboarding, codebase orientation, incident comprehension, architecture-review preparation, or change-impact preparation.

## Do Not Use When

Do not use as a repository summarizer, as architecture approval, or when no authoritative entry point, interface, runtime observation, or owner-approved source is available.

## Inputs

Require a bounded system or task objective, source locations, permissions, and at least one authoritative starting point: executable entry point, deployment configuration, interface contract, runtime trace, test, or owner-approved architecture source.

## Outputs

Produce `system-map.v1.json`, a concise Markdown companion, and `lat.capability.run_result.v1`.

Default writeback:

```text
artifacts/system-understanding/<scope-id>/<run-id>/system-map.v1.json
artifacts/system-understanding/<scope-id>/<run-id>/summary.md
artifacts/capability-runs/system-mental-model/<run-id>/run-result.json
```

When write permission is unavailable, return the complete structured result inline with `write_status=returned_inline`.

The map must contain system purpose and observable outcome, runtime topology, key entry points, core modules, golden and failure workflows, data flows, control points, impact boundaries, unknowns, open questions, validation actions, evidence references, and teach-back checks.

## Evidence

Separate source-supported facts from inference. Preserve resolvable citations, source scope and version or observation time, uncertainty, unknowns, assumptions, conflicts, and guesses. Do not continue beyond the evidence boundary. A plausible explanation, generated summary, or repeated statement is not proof. Prefer runtime configuration and traces, interface schemas and tests, then source entry points and call paths. Documentation alone does not prove runtime behavior.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- purpose and observable outcome are explicit;
- topology and key entry points are evidence-linked;
- one golden path and one representative failure path are traced end to end;
- material data flows, control points, and impact boundaries are explicit;
- critical unknowns have owners or validation actions;
- the user can explain the purpose, path, control points, and a key exception in their own words.

Teach-back remains `not_evaluated` until the learner explains without copying the artifact.

## Stop Conditions

Stop at the requested artifact or next reviewable stage. Stop without repeated probing when required permission, source access, critical facts, or sufficient evidence is unavailable; when a security, privacy, compliance, data-governance, architecture, production, or other high-risk boundary is reached; when validation fails after one bounded corrective retry; or when the goal, stage gate, retry budget, or user stop condition is reached. State the exact missing permission or evidence, accountable owner, reason, and resumable next step.

## Workflow

1. Bound the system, learner role, task, and time horizon.
2. Query ConPort first when available; otherwise inspect compact metadata and targeted entry points.
3. State purpose, users, observable outcomes, and non-goals.
4. Identify deployment/runtime units, trust boundaries, and ingress, scheduler, worker, event, CLI, UI, or API entry points.
5. Trace one golden path and one representative failure path.
6. Map core modules by responsibility and identify policy, routing, permission, validation, state, and side-effect control points.
7. Map material data flows: source, transform, store, sink, owner, classification, and time behavior when known.
8. Define direct and downstream impact boundaries and explicitly unestablished areas.
9. Build the evidence ledger, conflicts, unknowns, questions, and validation plan.
10. Generate teach-back prompts and evaluate the response when supplied.
11. Keep invariant mapping rules in a stable prefix and task evidence in a bounded dynamic suffix.

## Rules

SMM.001 | MUST | topology | distinguish documented design from observed runtime topology
SMM.002 | MUST | entry | identify evidence-linked runtime entry points before deep module detail
SMM.003 | MUST | flow | trace triggers data state side effects and observable outcomes end to end
SMM.004 | MUST | control | identify policy routing permission validation and state-transition control points
SMM.005 | MUST | boundary | expose trust compatibility ownership and change-impact boundaries
SMM.006 | MUST | learning | require teach-back for critical controls and exceptions
SMM.007 | SHOULD | context | load the smallest source slice that can prove or disprove the next claim
SMM.008 | SHOULD | token | optimize quality-adjusted token ROI after evidence quality passes
SMM.009 | NEVER | claim | present inferred topology or causality as verified fact
SMM.010 | NEVER | context | dump the full repository logs or knowledge base

## References

Apply `../../docs/capability-context-contract.md` and compose through `../context-mastery/SKILL.md` when broader routing is needed.

## Verification

```bash
python scripts/validate_skill_package.py --root skills/system-mental-model
```

## Failure Modes

- architecture-fiction: a plausible diagram lacks runtime or interface evidence;
- entry-point-blindness: modules are summarized before executable entry points;
- happy-path-only: failures and recovery are omitted;
- false-completeness: unknowns are hidden;
- borrowed-understanding: the learner repeats the artifact but cannot explain controls.
