---
name: lattice-governor
description: use for public lattice skill governance, skill-package refactor, registry schema design, trigger/output eval design, token-efficiency review, validator workflows, and repo-native context standards; do not use for private product plans, private context packs, company data, runtime product code, automated trading, or non-skill coding; input is public lattice repo files, SKILL.md packages, markdown instructions, json/jsonl registry records, eval cases, schemas, and validator outputs; output is public-safe skill designs, refactor plans, registry/eval artifacts, validation commands, and concise patches preserving behavior, safety, public/private boundaries, and quality-adjusted token ROI.
---

# Lattice Governor

## Goal

Govern, optimize, and refactor public Lattice skill and context artifacts as reusable, runtime-portable capability packages.

Keep Lattice public, generic, validator-oriented, and free of private project context. Treat Lattice as the standards and tooling layer for downstream private skill portfolios.

## Use When

Use this skill for public Lattice work involving skill package standards, SKILL.md refactor, registry schema design, trigger/output eval design, token-efficiency review, validator workflows, format routing, public examples, or repo-native context governance.

Use this skill before changing public skill standards that private repositories may depend on.

## Do Not Use When

Do not use this skill for private product planning, private context packs, private skill portfolio decisions, company data, product runtime code, automated trading advice, or unrelated coding tasks.

If private downstream context is needed, stop and require the private repository's governance skill to handle it separately.

## Inputs

Expected inputs include public Lattice repo files, SKILL.md packages, markdown instructions, JSON/JSONL registry records, schema files, eval cases, validator outputs, inventory reports, token estimates, and public-safe refactor notes.

## Outputs

Expected outputs include public-safe skill designs, optimized SKILL.md control planes, moved-content plans, registry schemas, trigger eval suites, output eval suites, validator commands, release gate recommendations, and concise patches that preserve behavior and public/private boundaries.

## Workflow

1. Confirm the task is public Lattice skill/context governance.
2. Query ConPort MCP before loading or searching full skill text when ConPort is available; otherwise read targeted repo files before broad search.
3. Identify the context layer: instruction, skill, reference, schema, eval, script, registry, event log, or report.
4. Inventory the target package with existing Lattice scripts when practical.
5. Classify each artifact as control plane, long reference, deterministic script, schema, eval, asset, runtime log, or report.
6. Preserve existing frontmatter schema; optimize only existing frontmatter values unless the target runtime requires extra metadata.
7. Keep `description` as the primary trigger and boundary surface.
8. Move long background, examples, variants, and rationale out of `SKILL.md` into topic-scoped references.
9. Move deterministic, fragile, or repeatable operations into scripts and require tests or smoke checks.
10. Add or update registry and eval artifacts when the skill is intended for reuse.
11. Verify with Lattice validators, token estimates, trigger evals, and output evals before recommending promotion.
12. Emit a compact release recommendation: promote, revise, quarantine, deprecate, or reject.

## Rules

LATGOV.001 | MUST  | boundary | keep Lattice public, generic, free of private project context
LATGOV.002 | MUST  | trigger  | description is primary trigger + boundary
LATGOV.003 | MUST  | skill    | keep SKILL.md compact control plane, not knowledge dump
LATGOV.004 | MUST  | quality  | preserve behavior, safety, rejection, failure rules before token reduction
LATGOV.005 | MUST  | token    | optimize quality-adjusted output per token cost
LATGOV.006 | SHOULD | prompt   | use stable prefix for batch refactor + eval runs
LATGOV.007 | SHOULD | refs     | use topic-scoped references for long background + examples
LATGOV.008 | SHOULD | scripts  | move repeatable fragile operations to tested scripts
LATGOV.009 | MUST  | eval     | require positive + negative trigger cases for reusable skills
LATGOV.010 | MUST  | eval     | compare output to baseline or previous version before active promotion
LATGOV.011 | NEVER | privacy  | copy private downstream skill content or context into Lattice
LATGOV.012 | NEVER | logs     | store unprojected runtime telemetry, conversation dumps, or bulk traces as Markdown context
LATGOV.013 | MUST  | registry | mark ambiguous or unsafe skill changes as review_needed
## Reference Routing

Consult only the smallest relevant file first.

- `references/governance-model.md`: lifecycle, registry, dependency, and release-channel model.
- `references/token-efficiency-model.md`: quality-adjusted token ROI, progressive loading, stable-prefix design, and context projection rules.
- `references/eval-and-release-gates.md`: trigger eval, output eval, validation gates, and promotion criteria.
- `schemas/skill_registry_record.schema.json`: public registry record contract.
- `schemas/trigger_eval_case.schema.json`: trigger eval case contract.
- `schemas/output_eval_case.schema.json`: output eval case contract.
- `evals/trigger_queries.json`: seed examples for this skill's own trigger behavior.
- `evals/output_cases.json`: seed output-quality cases for this skill.

References carry detail for these surfaced hard-rule groups: lifecycle/registry model, token-efficiency model, eval/release gates, and schema contracts.

## Verification

Run relevant public Lattice checks when practical:

```bash
python3.14 scripts/inventory_skills.py --root skills --out skill_inventory.jsonl
python3.14 scripts/validate_skill_package.py --root skills
python3.14 scripts/generate_skill_refactor_report.py --inventory skill_inventory.jsonl --out skill_quality_report.md
python3.14 scripts/estimate_skill_tokens.py --root skills
```

For a changed reusable skill, also verify:

```text
- frontmatter has name and description only unless runtime metadata is required elsewhere
- description has use and do-not-use boundaries
- SKILL.md has required control-plane sections
- references do not hide hard rules absent from SKILL.md
- trigger eval has positive and negative cases
- output eval preserves behavior-critical rules
- public/private boundary review passes
```

## Failure Modes

- Treating Lattice as a private downstream context repository.
- Adding private Auralis, Aurora, company, or user-specific context to public standards.
- Expanding `SKILL.md` into a long knowledge dump.
- Reducing tokens by deleting safety, rejection, failure, or behavior-critical rules.
- Adding new YAML frontmatter fields without target-runtime need.
- Producing registry or eval artifacts that are human-readable but not machine-checkable.
- Promoting a skill without trigger and output eval evidence.
- Letting private repositories depend on undocumented public behavior.
