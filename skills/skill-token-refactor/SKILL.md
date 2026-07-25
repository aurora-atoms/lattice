---
name: skill-token-refactor
description: "Rewrite existing SKILL.md/Markdown skill instructions into accurate, dense, token-efficient, machine-readable packages while preserving behavior, compatibility, and YAML frontmatter schema. Use for compression, restructuring, validation, batch refactor planning, language-format selection, or splitting content into references/scripts/schemas/evals. Require the Lattice Skill authoring contract, semantic version bump, structured output, evidence, success signals, and stop conditions. Do not use to execute the source skill's domain task, invent behavior, weaken constraints, or refactor insufficient source. Prefer ConPort summaries before raw skill text; optimize quality-adjusted token ROI."
---

# Skill Token Refactor

## Goal

Rewrite Skills into accurate, dense, token-efficient, machine-readable packages. Preserve behavior, frontmatter schema, compatibility, and quality-adjusted token ROI.

## Use When

- User provides existing `SKILL.md` files or Markdown Skill instructions.
- Task asks to compress, restructure, split, validate, migrate, or batch-optimize Skills.
- Output should preserve trigger intent, inputs, outputs, safety behavior, evidence behavior, stop behavior, and failure behavior.

## Do Not Use When

- Task asks to create unrelated product features.
- Source is not a Skill or Skill-like instruction.
- User asks to weaken constraints, remove safety behavior, or invent new behavior.
- Source behavior, compatibility baseline, or required permission is unavailable.

## Inputs

```text
source_skill_path
current capability-context catalog entry
current semantic version and base revision
optional ConPort record IDs
optional source commit
rewrite scope
validation requirements
```

## Outputs

```text
optimized SKILL.md
updated capability-context catalog entry when needed
increased semantic version in capability-context-policy.json
moved content plan
script/schema/eval candidates
validation report
review-needed items
ConPort update candidate
lat.capability.run_result.v1
```

Default run-result writeback:

```text
../../artifacts/capability-runs/skill-token-refactor/<run-id>/run-result.json
```

When write permission is unavailable, return the complete structured result inline and set `write_status=returned_inline`.

## Evidence

Record:

- source facts from the original Skill, current catalog, version policy, references, tests, and validator output;
- inference explaining why content is kept, moved, removed as duplicate, or marked review needed;
- stable citations to source paths, revisions, and validation evidence;
- uncertainty about runtime behavior, compatibility, or ambiguous source intent;
- unknowns caused by missing history, source files, permissions, or unavailable repositories;
- assumptions used in the refactor and the impact if false.

Do not infer behavior preservation from token reduction or validator success alone. Verify behavior-critical rules against authoritative source text.

## Success Signals

Evaluate:

```text
behavior-critical trigger input output safety evidence stop and failure rules preserved -> met | not_met | not_evaluated
required Skill contract sections are present and capability specific -> met | not_met | not_evaluated
semantic version increased and compatibility level is justified -> met | not_met | not_evaluated
package context and change-gate validation passes -> met | not_met | not_evaluated
moved content destinations and references resolve -> met | not_met | not_evaluated
```

File rewriting or token reduction alone is not success.

## Stop Conditions

Stop and emit a structured result when:

- the requested refactor or next reviewable stage is complete;
- source behavior, current version, compatibility baseline, or required files cannot be established;
- required read or write permission is missing;
- evidence is insufficient to preserve behavior safely;
- a security, privacy, public/private, compliance, data-governance, or authority risk is discovered;
- validation remains failed after one bounded corrective retry;
- a major-version, deprecation, or behavior decision requires accountable review;
- the user explicitly stops the task or the retry budget is exhausted.

For missing permission, state the exact permission, accountable owner, reason, and resumable next step. Do not repeatedly probe or attempt bypasses.

## Workflow

Use the Refactor Workflow below.

## Global Skill Rules

All refactored Skills follow this control plane unless a more specific source rule conflicts.

```text
GLOBAL.001 | MUST | quality | accuracy and behavior preservation before compression
GLOBAL.002 | MUST | tokens | token efficiency equals quality-adjusted output per token
GLOBAL.003 | MUST | runtime | portable across coding-agent Skill runtimes unless source requires otherwise and flag runtime-specific drift
GLOBAL.004 | MUST | frontmatter | preserve existing YAML properties and optimize values only
GLOBAL.005 | MUST | description | include use and do-not-use boundaries in description
GLOBAL.006 | NEVER | frontmatter | add unsupported metadata fields unless the target runtime explicitly requires them
GLOBAL.007 | MUST | language | choose fit-for-case LLM format dense prose schema-once rows JSON Schema code or references
GLOBAL.008 | NEVER | wording | duplicate obligation signal in one rule line
GLOBAL.009 | NEVER | identifiers | use underscore IDs for prose-rule slugs and use hyphenated or plain terms
GLOBAL.010 | MUST | identifiers | reserve underscores for real structured keys properties columns and source contracts
GLOBAL.011 | MUST | validation | run validator underscore rule for SKILL.md rule prose
GLOBAL.012 | MUST | authoring | apply docs/skill-authoring-gate.md to every changed Skill package
GLOBAL.013 | MUST | contract | require Outputs Evidence Success Signals and Stop Conditions
GLOBAL.014 | MUST | version | increase semantic version for every changed Skill package
```

## Refactor Workflow

1. Read `../../docs/skill-authoring-gate.md` and `../../docs/capability-context-contract.md`.
2. Query ConPort MCP for inventory, trigger summary, prior refactor notes, extracted rules, known risks, duplicates, and refactor status.
3. If ConPort is missing, stale, incomplete, or conflicting, read targeted source sections.
4. Read the target catalog entry and current semantic version before editing.
5. Inventory purpose, description, inputs, outputs, tools, references, rules, evidence, success signals, stop conditions, risks, and token-heavy areas.
6. Classify each section as `KEEP_SKILL`, `MOVE_REFERENCE`, `MOVE_SCRIPT`, `MOVE_SCHEMA`, `MOVE_EVAL`, `DISCARD_DUP`, or `REVIEW_NEEDED`.
7. Preserve existing YAML frontmatter schema; optimize existing values only.
8. Require capability-specific `Outputs`, `Evidence`, `Success Signals`, and `Stop Conditions`; use `../../templates/skill-contract-sections.template.md` as a starting pattern.
9. Move long examples/background to `references/`; deterministic operations to `scripts/`; contracts to `schemas/`; regressions to `evals/`.
10. Verify behavior-critical rules against source before finalizing changed constraints.
11. Update catalog metadata when trigger, users, minimum inputs, outputs, intended change, or runtime targets change.
12. Increase the target Skill version and classify the change as patch, minor, or major.
13. Run package, context, and Skill change contract validators so prose rule slugs, catalog drift, missing contract sections, and missing version bumps fail.
14. Emit report, structured run result, and ConPort update candidate.
15. Stop at the current reviewable stage unless end-to-end continuation is explicitly authorized.

## Frontmatter Policy

FRONT.001 | MUST | skill | preserve existing frontmatter schema
FRONT.002 | MUST | skill | preserve all existing frontmatter properties
FRONT.003 | NEVER | skill | add new frontmatter property during refactor without explicit instruction
FRONT.004 | NEVER | skill | delete existing frontmatter property during refactor without explicit instruction
FRONT.005 | NEVER | skill | rename existing frontmatter property without explicit instruction
FRONT.006 | SHOULD | skill | optimize existing frontmatter values for trigger precision and token efficiency
FRONT.007 | MUST | skill | description is primary portable trigger surface
FRONT.008 | MUST | skill | put use and do-not-use guidance inside description
FRONT.009 | MUST | skill | unsupported or ambiguous frontmatter change becomes review needed
FRONT.NEW.001 | SHOULD | skill | use minimal frontmatter when no existing schema is present
FRONT.NEW.002 | MUST | skill | include name and description
FRONT.NEW.003 | NEVER | skill | add unsupported metadata fields without explicit runtime need
FRONT.NEW.004 | MAY | skill | preserve or add tool-specific properties only when target runtime requires them
SKILL.001 | MUST | skill | token budget equals quality-adjusted ROI
SKILL.002 | MUST | skill | SKILL.md is control plane only
SKILL.003 | NEVER | skill | long background or redundant examples in SKILL.md
SKILL.004 | MUST | skill | description is trigger surface
SKILL.005 | MUST | skill | clear use and do-not-use boundaries
SKILL.006 | MUST | skill | preserve behavior-critical rules
SKILL.007 | MUST | skill | preserve safety rejection failure evidence and stop behavior
SKILL.008 | SHOULD | skill | move long examples and background to references
SKILL.009 | SHOULD | skill | move deterministic work to scripts
SKILL.010 | MUST | skill | ambiguity becomes review needed
SKILL.011 | MUST | skill | changed package has required contract sections and increased version

## Description Rules

DESC.001 | MUST | description | identify trigger surface and user intent
DESC.002 | MUST | description | specific enough for Skill selection
DESC.003 | NEVER | description | marketing copy or background summary
DESC.004 | MUST | description | include use and do-not-use guidance
DESC.005 | MUST | description | mention expected source input and output type
DESC.006 | MUST | description | mention behavior preservation and token ROI

## Token Optimization Rules

TOK.001 | MUST | quality | preserve quality and behavior before token reduction
TOK.002 | MUST | metric | token efficiency equals quality-adjusted output per token cost
TOK.003 | NEVER | rewrite | reduce tokens by deleting constraints exceptions or failure modes
TOK.004 | SHOULD | rewrite | spend tokens for behavior preservation and verification when needed
TOK.005 | MUST | report | distinguish token reduction from quality-adjusted token ROI

## Context Format Routing Policy

CTXFMT.001 | MUST | format | separate authoring storage boundary projection and report formats
CTXFMT.002 | MUST | skill | keep SKILL.md as control plane not knowledge dump
CTXFMT.003 | MUST | prompt | schema-once compact rows for bulk model-visible context
CTXFMT.004 | MUST | boundary | JSON Schema or Structured Outputs for tool boundaries
CTXFMT.005 | SHOULD | docs | topic-scoped Markdown for long reference context
CTXFMT.006 | NEVER | skill | hide hard rules only inside references
CTXFMT.007 | NEVER | prompt | verbose JSON or Markdown tables for bulk context when compact rows suffice
CTXFMT.008 | NEVER | logs | runtime logs or conversation dumps as Markdown memory
Choose the most information-dense representation for the case; human readability is secondary to model precision.

```text
LANG.001 | MUST | nuance | use dense natural language for semantic judgment caveats and exceptions
LANG.002 | MUST | repeated-data | use schema-once compact rows for repeated records and rules
LANG.003 | MUST | boundary | use JSON Schema or Structured Outputs for tool contracts
LANG.004 | MUST | deterministic | use scripts or code for repeatable transformations and validators
LANG.005 | SHOULD | references | use Markdown references for long explanatory context loaded on demand
LANG.006 | NEVER | control | optimize for human-readable prose when compact LLM-readable rules suffice
LANG.007 | MUST | identifiers | use hyphenated or plain rule slugs unless preserving real structured keys
```

## Rules

Apply all rule lines in this control plane, plus `../../docs/skill_format_policy.md` and `../../docs/skill-authoring-gate.md`.

## Markdown Policy

MD.001 | MUST | markdown | Markdown is container for instructions references and reports
MD.002 | SHOULD | markdown | embed compact machine-readable blocks when precision matters
MD.003 | NEVER | markdown | Markdown for raw OTel span dumps token records event ledgers or bulk memory
MD.004 | SHOULD | markdown | avoid long prose repeated bullets deep headings repeated examples and raw logs
MD.005 | MUST | skill | verbose Markdown Skill section becomes compact control-plane rules when behavior is preserved

## ConPort-First Retrieval Policy

CONPORT.001 | MUST | retrieval | query ConPort MCP before loading or searching full Skill text
CONPORT.002 | MUST | retrieval | use ConPort for inventory trigger summary prior notes rules and risks first
CONPORT.003 | SHOULD | retrieval | raw Skill text only after ConPort is missing stale incomplete or conflicting
CONPORT.004 | MUST | retrieval | verify source file before final rewrite when behavior-critical rules change
CONPORT.005 | NEVER | retrieval | use ConPort summary alone to delete or weaken source constraints
CONPORT.006 | NEVER | retrieval | load entire Skill library when inventory or targeted lookup suffices
If ConPort MCP is unavailable, continue with targeted local reads and mark `conport_unavailable` or `source_verification_needed` when relevant.

## Machine-Readability Rules

MR.001 | MUST | boundary | JSON Schema or Structured Outputs for tool boundaries
MR.002 | MUST | bulk | schema-once compact rows for bulk context
MR.003 | NEVER | logs | runtime logs or conversation dumps as Markdown memory
READ.001 | MUST | skill | machine readability over human readability in control planes
READ.002 | SHOULD | docs | human-readable summary only when it improves navigation or review
READ.003 | NEVER | skill | long narrative prose for behavior rules when compact rows suffice
READ.004 | SHOULD | refs | human explanations in detailed references not SKILL.md
CACHE.001 | MUST | prompt | stable system prompt prefix across batch Skill rewrite runs
CACHE.002 | SHOULD | prompt | global rules format policies and output contracts in stable prefix
CACHE.003 | SHOULD | prompt | variable Skill-specific source material in dynamic suffix
CACHE.004 | NEVER | prompt | large variable source text inside global instruction prefix
CACHE.005 | SHOULD | batch | same agent instruction and output template across batch runs
Dynamic suffix: target Skill path, ConPort lookup result, targeted source excerpts, inventory record, rewrite-specific notes.

## Content Classification Rules

CLASS.001 | MUST | classify | assign each source section one primary destination
CLASS.002 | MUST | classify | conflicting or unclear section becomes REVIEW_NEEDED
CLASS.003 | SHOULD | classify | repeated content becomes DISCARD_DUP only after behavior check
PRES.001 | MUST | preserve | keep behavior-critical constraints
PRES.002 | MUST | preserve | keep safety privacy rejection failure evidence and stop behavior
PRES.003 | MUST | preserve | verify changed constraints against source
PRES.004 | NEVER | preserve | weaken or delete constraints from ConPort summary alone
PRES.005 | NEVER | behavior | invent new behavior
PRES.006 | MUST | frontmatter | preserve existing YAML properties such as allowed tools or model

## Script Candidate Rules

SCRIPT.001 | SHOULD | script | repeatable deterministic steps become scripts
SCRIPT.002 | SHOULD | script | scripts stay dependency-light
SCRIPT.003 | MUST | script | agent judgment stays in SKILL.md not scripts

## Batch Processing Rules

BATCH.001 | MUST | batch | inventory before rewrite
BATCH.002 | MUST | batch | emit review queue for ambiguous or risky Skills
BATCH.003 | NEVER | batch | rewrite entire library without inventory and review plan
Use `references/refactor_templates.md#single-skill-report`.

## Output Template: Batch

Use `references/refactor_templates.md#batch-report`.

## Verification

- Validate package structure with `../../scripts/validate_skill_package.py`.
- Validate context and version contracts with `../../scripts/validate_capability_context.py`.
- Validate changed Skill packages with `../../scripts/validate_skill_change_contract.py --base-ref <base-sha> --head-ref <head-sha>`.
- Confirm SKILL.md rule text avoids underscore prose slugs except real keys, IDs, enum values, file names, or source contract terms.
- Compare behavior-critical rules against source when constraints change.
- Check moved content destinations exist.
- Check unresolved ambiguity is listed in review needed.

## Failure Modes

- `conport_record_missing`: ConPort unavailable or no matching record.
- `source_verification_needed`: summary insufficient for safe rewrite.
- `review_needed`: ambiguity, conflict, compatibility uncertainty, or behavior-critical uncertainty.
- `blocked`: source unavailable, permission unavailable, unsafe instruction, insufficient evidence, or impossible preservation requirement.
- missing version bump or required Skill contract section.

## References

- `../../docs/skill-authoring-gate.md`
- `../../templates/skill-contract-sections.template.md`
- `references/refactor_templates.md`
- `references/classification_guide.md`
- `../../docs/skill_format_policy.md`

## Scripts

- `../../scripts/inventory_skills.py`
- `../../scripts/validate_skill_package.py`
- `../../scripts/validate_capability_context.py`
- `../../scripts/validate_skill_change_contract.py`
- `../../scripts/estimate_skill_tokens.py`
- `../../scripts/generate_skill_refactor_report.py`
