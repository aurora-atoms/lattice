---
name: lattice-governor
description: use for public lattice skill governance, skill creation or modification gates, skill-package refactor, versioned capability-context contracts, registry schema design, trigger/output eval design, token-efficiency review, validator workflows, and repo-native context standards; do not use for private product plans, private context packs, company data, runtime product code, automated trading, or non-skill coding; input is public lattice repo files, SKILL.md packages, Agent instructions, context catalogs, registry records, eval cases, schemas, and validator outputs; output is public-safe skill designs, versioned context contracts, authoring-gate decisions, registry/eval artifacts, validation commands, and concise patches preserving behavior, safety, compatibility, public/private boundaries, and quality-adjusted token ROI.
---

# Lattice Governor

## Goal

Govern, optimize, create, and refactor public Lattice Skill, Agent, and context artifacts as reusable, runtime-portable capability packages.

Keep Lattice public, generic, validator-oriented, and free of private project context. Treat Lattice as the standards and tooling layer for downstream private capability portfolios.

## Use When

Use this Skill for public Lattice work involving Skill creation or modification, Skill package standards, SKILL.md refactor, Agent context alignment, stable capability identity and versioning, registry schema design, trigger/output eval design, token-efficiency review, validator workflows, format routing, public examples, or repo-native context governance.

Use this Skill before changing any file under `../../skills/` and before changing public capability standards that private repositories may depend on.

## Do Not Use When

Do not use this Skill for private product planning, private context packs, private Skill portfolio decisions, company data, product runtime code, automated trading advice, or unrelated coding tasks.

If private downstream context is needed, stop and require the private repository's governance Skill to handle it separately.

## Inputs

Expected inputs include public Lattice repo files, SKILL.md packages, Agent instructions, Markdown instructions, capability-context catalogs, JSON/JSONL registry records, schema files, eval cases, validator outputs, inventory reports, token estimates, source behavior, compatibility baseline, and public-safe refactor notes.

## Outputs

Produce visible, structured governance artifacts:

```text
authoring or compatibility decision
changed Skill or Agent package
updated catalog and semantic version policy
validation and regression evidence
review-needed or blocked items
lat.capability.run_result.v1
```

Default writeback for the structured run result:

```text
../../artifacts/capability-runs/lattice-governor/<run-id>/run-result.json
```

When write permission is unavailable, return the complete result inline and set `write_status=returned_inline`.

## Evidence

Separate:

- facts supported by repository paths, commit refs, schemas, validator output, tests, or authoritative runtime documentation;
- inference and compatibility judgment derived from those facts;
- citations or stable repository references;
- uncertainty and conflicting source behavior;
- unknowns such as missing baseline, unavailable history, or unsupported runtime behavior;
- assumptions and their impact if false.

Do not treat a proposed convention, generated patch, passing syntax check, or existing registry entry as sufficient evidence of behavioral compatibility.

## Success Signals

Evaluate at least these signals:

```text
requested governance change is represented in the owned contract -> met | not_met | not_evaluated
changed Skill packages have increased semantic versions -> met | not_met | not_evaluated
catalog, schema, validator, and CI checks pass -> met | not_met | not_evaluated
behavior, safety, evidence, stop, and authority boundaries are preserved -> met | not_met | not_evaluated
```

File creation alone is not success. A capability cannot be promoted when any required signal is not met or cannot be evaluated without accountable review.

## Stop Conditions

Stop and emit a structured result when:

- the requested governance target or next reviewable stage is reached;
- source behavior, current version, compatibility baseline, or required repository history cannot be established;
- required read or write permission is missing;
- evidence is insufficient to classify a change safely;
- a security, privacy, public/private, compliance, data-governance, architecture, or release authority boundary is reached;
- validation remains failed after one bounded corrective retry;
- a major-version, deprecation, or authority decision requires an accountable human;
- the user explicitly stops the task or the retry budget is exhausted.

For a permission stop, name the exact permission, accountable owner, reason, and resumable next step. Do not repeatedly probe or attempt bypasses.

## Workflow

1. Confirm the task is public Lattice Skill, Agent, or context governance.
2. Query ConPort MCP before loading or searching full Skill text when ConPort is available; otherwise read targeted repo files before broad search.
3. For any `skills/<name>/` change, read `../../docs/skill-authoring-gate.md`, `../../docs/capability-context-contract.md`, the target catalog entry, and the current semantic version before editing.
4. Identify the context layer: instruction, Skill, Agent, reference, schema, eval, script, registry, event log, or report.
5. Inventory the target package with existing Lattice scripts when practical.
6. Classify each artifact as control plane, compact context metadata, long reference, deterministic script, schema, eval, asset, runtime log, or report.
7. Preserve runtime-native frontmatter. Keep stable ID, semantic version, intended change, primary user, secondary audience, trigger, minimum inputs, outputs, and optional-context discovery in `../../registry/skill-context.catalog.json` or `../../registry/agent-context.catalog.json`.
8. Keep `description` as the primary native trigger and boundary surface; require agreement between description and catalog trigger.
9. Require non-empty `Outputs`, `Evidence`, `Success Signals`, and `Stop Conditions` in every changed Skill. Use `../../templates/skill-contract-sections.template.md` as the minimum pattern.
10. Treat required-input, permission, output, evidence, success, stop, authority-boundary, and behavior changes as compatibility decisions under `../../docs/capability-context-contract.md`.
11. Increase the semantic version for every changed Skill package; choose patch, minor, or major based on the behavior contract.
12. Move long background, examples, variants, and rationale out of `SKILL.md` into topic-scoped references.
13. Move deterministic, fragile, or repeatable operations into scripts and require tests or smoke checks.
14. Use optional context only for a named confidence, scope, or output-quality gap. Do not eagerly load related capabilities or broad sources.
15. Add or update registry and eval artifacts when the capability is intended for reuse.
16. Verify with package validation, capability-context validation, the Skill change contract gate, token estimates, trigger evals, and output evals before recommending promotion.
17. Emit a structured visible run result and a compact release recommendation: promote, revise, quarantine, deprecate, or reject.

## Rules

LATGOV.001 | MUST | boundary | keep Lattice public generic and free of private project context
LATGOV.002 | MUST | trigger | description remains the primary native trigger and boundary
LATGOV.003 | MUST | identity | give every reusable Skill and Agent a stable family name and semantic version
LATGOV.004 | MUST | context | record intended change primary user secondary audience trigger minimum inputs outputs and optional discovery
LATGOV.005 | MUST | compatibility | version required-input permission output evidence success stop authority and behavior changes deliberately
LATGOV.006 | MUST | authoring | apply the mandatory Skill authoring gate to every changed Skill package
LATGOV.007 | MUST | version | increase the semantic version for every changed Skill package
LATGOV.008 | MUST | output | require visible structured output and governed writeback behavior
LATGOV.009 | MUST | evidence | separate facts inference citations uncertainty unknowns and assumptions
LATGOV.010 | MUST | success | require explicit evaluated success signals
LATGOV.011 | MUST | stop | require bounded retries stage gates permission stops evidence stops and risk stops
LATGOV.012 | MUST | skill | keep SKILL.md a compact control plane rather than a knowledge dump
LATGOV.013 | MUST | quality | preserve behavior safety rejection and failure rules before token reduction
LATGOV.014 | MUST | token | optimize quality-adjusted output per token cost
LATGOV.015 | SHOULD | prompt | use a stable prefix for batch refactor and evaluation runs
LATGOV.016 | SHOULD | refs | use topic-scoped references for long background and examples
LATGOV.017 | SHOULD | scripts | move repeatable fragile operations to tested scripts
LATGOV.018 | MUST | eval | require positive and negative trigger cases for reusable capabilities
LATGOV.019 | MUST | eval | compare output to a baseline or previous version before active promotion
LATGOV.020 | NEVER | privacy | copy private downstream capability content or context into Lattice
LATGOV.021 | NEVER | logs | store unprojected runtime telemetry conversation dumps or bulk traces as Markdown context
LATGOV.022 | MUST | registry | mark ambiguous unsafe or incompatible capability changes as review needed

## Reference Routing

Consult only the smallest relevant file first.

- `../../docs/skill-authoring-gate.md`: mandatory creation and modification workflow.
- `../../templates/skill-contract-sections.template.md`: required output, evidence, success, and stop sections.
- `../../docs/capability-context-contract.md`: stable identity, semantic versioning, users, triggers, inputs, optional context, output, evidence, success, stop, and authority.
- `references/governance-model.md`: lifecycle, registry, dependency, and release-channel model.
- `references/token-efficiency-model.md`: quality-adjusted token ROI, progressive loading, stable-prefix design, and context projection rules.
- `references/eval-and-release-gates.md`: trigger eval, output eval, validation gates, and promotion criteria.
- `schemas/skill_registry_record.schema.json`: public legacy Skill registry record contract.
- `schemas/trigger_eval_case.schema.json`: trigger eval case contract.
- `schemas/output_eval_case.schema.json`: output eval case contract.
- `evals/trigger_queries.json`: seed examples for this Skill's own trigger behavior.
- `evals/output_cases.json`: seed output-quality cases for this Skill.

References carry detail for surfaced hard-rule groups. Do not hide required identity, compatibility, output, evidence, success, stop, authority, or discovery rules only in references.

## Verification

Run relevant public Lattice checks when practical:

```bash
python scripts/inventory_skills.py --root skills --out skill_inventory.jsonl
python scripts/validate_skill_package.py --root skills
python scripts/validate_capability_context.py --root .
python scripts/validate_skill_change_contract.py --base-ref <base-sha> --head-ref <head-sha>
python -m unittest discover -s tests -p 'test_capability_context.py' -v
python scripts/generate_skill_refactor_report.py --inventory skill_inventory.jsonl --out skill_quality_report.md
python scripts/estimate_skill_tokens.py --root skills
```

For a changed reusable capability, also verify:

```text
- frontmatter preserves the target runtime contract
- description has use and do-not-use boundaries
- context catalog contains stable ID/version semantics and all required context fields
- catalog trigger agrees with native description
- optional discovery is advisory and bounded
- SKILL.md has Outputs Evidence Success Signals and Stop Conditions
- structured output declares writeback and inline fallback
- evidence separates facts inference citations uncertainty unknowns and assumptions
- success and stop behavior is explicit and evaluable
- references do not hide hard rules absent from SKILL.md
- trigger eval has positive and negative cases
- output eval preserves behavior-critical rules
- public/private boundary review passes
```

## Failure Modes

- Treating Lattice as a private downstream context repository.
- Adding private company or user-specific context to public standards.
- Expanding SKILL.md into a long knowledge dump.
- Adding capability identity fields to runtime frontmatter that does not support them.
- Changing required inputs, permissions, outputs, evidence, success, stop, authority, or behavior without a version decision.
- Modifying a Skill package without increasing its version.
- Creating a README-only rule without validator or CI enforcement.
- Creating a parallel governance Skill that duplicates `lattice-governor`.
- Making optional context an eager fan-out across Skills, Agents, repositories, or sources.
- Reducing tokens by deleting safety, rejection, evidence, stop, or behavior-critical rules.
- Producing registry or eval artifacts that are human-readable but not machine-checkable.
- Promoting a capability without trigger and output evaluation evidence.
- Letting private repositories depend on undocumented public behavior.
