---
name: lattice-governor
description: use for public lattice skill governance, skill-package refactor, versioned capability-context contracts, registry schema design, trigger/output eval design, token-efficiency review, validator workflows, and repo-native context standards; do not use for private product plans, private context packs, company data, runtime product code, automated trading, or non-skill coding; input is public lattice repo files, SKILL.md packages, Agent instructions, context catalogs, registry records, eval cases, schemas, and validator outputs; output is public-safe skill designs, versioned context contracts, refactor plans, registry/eval artifacts, validation commands, and concise patches preserving behavior, safety, compatibility, public/private boundaries, and quality-adjusted token ROI.
---

# Lattice Governor

## Goal

Govern, optimize, and refactor public Lattice Skill, Agent, and context artifacts as reusable, runtime-portable capability packages.

Keep Lattice public, generic, validator-oriented, and free of private project context. Treat Lattice as the standards and tooling layer for downstream private capability portfolios.

## Use When

Use this Skill for public Lattice work involving Skill package standards, SKILL.md refactor, Agent context alignment, stable capability identity and versioning, registry schema design, trigger/output eval design, token-efficiency review, validator workflows, format routing, public examples, or repo-native context governance.

Use this Skill before changing public capability standards that private repositories may depend on.

## Do Not Use When

Do not use this Skill for private product planning, private context packs, private Skill portfolio decisions, company data, product runtime code, automated trading advice, or unrelated coding tasks.

If private downstream context is needed, stop and require the private repository's governance Skill to handle it separately.

## Inputs

Expected inputs include public Lattice repo files, SKILL.md packages, Agent instructions, Markdown instructions, capability-context catalogs, JSON/JSONL registry records, schema files, eval cases, validator outputs, inventory reports, token estimates, and public-safe refactor notes.

## Outputs

Expected outputs include public-safe Skill designs, compact SKILL.md control planes, versioned capability-context contracts, moved-content plans, registry schemas, trigger eval suites, output eval suites, validator commands, release gate recommendations, and concise patches that preserve behavior, compatibility, and public/private boundaries.

## Workflow

1. Confirm the task is public Lattice Skill, Agent, or context governance.
2. Query ConPort MCP before loading or searching full Skill text when ConPort is available; otherwise read targeted repo files before broad search.
3. Identify the context layer: instruction, Skill, Agent, reference, schema, eval, script, registry, event log, or report.
4. Inventory the target package with existing Lattice scripts when practical.
5. Classify each artifact as control plane, compact context metadata, long reference, deterministic script, schema, eval, asset, runtime log, or report.
6. Preserve runtime-native frontmatter. Keep stable ID, semantic version, intended change, primary user, secondary audience, trigger, minimum inputs, outputs, and optional-context discovery in `../../registry/skill-context.catalog.json` or `../../registry/agent-context.catalog.json`.
7. Keep `description` as the primary native trigger and boundary surface; require agreement between description and catalog trigger.
8. Treat required-input, permission, output, authority-boundary, and behavior changes as compatibility decisions under `../../docs/capability-context-contract.md`.
9. Move long background, examples, variants, and rationale out of `SKILL.md` into topic-scoped references.
10. Move deterministic, fragile, or repeatable operations into scripts and require tests or smoke checks.
11. Use optional context only for a named confidence, scope, or output-quality gap. Do not eagerly load related capabilities or broad sources.
12. Add or update registry and eval artifacts when the capability is intended for reuse.
13. Verify with Lattice validators, context-catalog coverage, token estimates, trigger evals, and output evals before recommending promotion.
14. Emit a compact release recommendation: promote, revise, quarantine, deprecate, or reject.

## Rules

LATGOV.001 | MUST | boundary | keep Lattice public generic and free of private project context
LATGOV.002 | MUST | trigger | description remains the primary native trigger and boundary
LATGOV.003 | MUST | identity | give every reusable Skill and Agent a stable family name and semantic version
LATGOV.004 | MUST | context | record intended change primary user secondary audience trigger minimum inputs outputs and optional discovery
LATGOV.005 | MUST | compatibility | version required-input permission output authority and behavior changes deliberately
LATGOV.006 | MUST | skill | keep SKILL.md a compact control plane rather than a knowledge dump
LATGOV.007 | MUST | quality | preserve behavior safety rejection and failure rules before token reduction
LATGOV.008 | MUST | token | optimize quality-adjusted output per token cost
LATGOV.009 | SHOULD | prompt | use a stable prefix for batch refactor and evaluation runs
LATGOV.010 | SHOULD | refs | use topic-scoped references for long background and examples
LATGOV.011 | SHOULD | scripts | move repeatable fragile operations to tested scripts
LATGOV.012 | MUST | eval | require positive and negative trigger cases for reusable capabilities
LATGOV.013 | MUST | eval | compare output to a baseline or previous version before active promotion
LATGOV.014 | NEVER | privacy | copy private downstream capability content or context into Lattice
LATGOV.015 | NEVER | logs | store unprojected runtime telemetry conversation dumps or bulk traces as Markdown context
LATGOV.016 | MUST | registry | mark ambiguous unsafe or incompatible capability changes as review needed

## Reference Routing

Consult only the smallest relevant file first.

- `../../docs/capability-context-contract.md`: stable identity, semantic versioning, users, triggers, inputs, optional context, and authority.
- `references/governance-model.md`: lifecycle, registry, dependency, and release-channel model.
- `references/token-efficiency-model.md`: quality-adjusted token ROI, progressive loading, stable-prefix design, and context projection rules.
- `references/eval-and-release-gates.md`: trigger eval, output eval, validation gates, and promotion criteria.
- `schemas/skill_registry_record.schema.json`: public legacy Skill registry record contract.
- `schemas/trigger_eval_case.schema.json`: trigger eval case contract.
- `schemas/output_eval_case.schema.json`: output eval case contract.
- `evals/trigger_queries.json`: seed examples for this Skill's own trigger behavior.
- `evals/output_cases.json`: seed output-quality cases for this Skill.

References carry detail for surfaced hard-rule groups. Do not hide required identity, compatibility, authority, or discovery rules only in references.

## Verification

Run relevant public Lattice checks when practical:

```bash
python scripts/inventory_skills.py --root skills --out skill_inventory.jsonl
python scripts/validate_skill_package.py --root skills
python scripts/validate_capability_context.py --root .
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
- SKILL.md has required control-plane sections
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
- Changing required inputs, permissions, outputs, authority, or behavior without a version decision.
- Making optional context an eager fan-out across Skills, Agents, repositories, or sources.
- Reducing tokens by deleting safety, rejection, failure, or behavior-critical rules.
- Producing registry or eval artifacts that are human-readable but not machine-checkable.
- Promoting a capability without trigger and output evaluation evidence.
- Letting private repositories depend on undocumented public behavior.
