---
name: skill-token-refactor
description: "Rewrite existing SKILL.md/Markdown skill instructions into accurate, dense, token-efficient, machine-readable packages while preserving behavior and YAML frontmatter schema. Use for compression, restructuring, validation, batch refactor planning, language-format selection, or splitting content into references/scripts/schemas/evals. Do not use to execute the source skill's domain task, invent behavior, weaken constraints, or refactor insufficient source. Prefer ConPort summaries before raw skill text; optimize quality-adjusted token ROI."
---

# Skill Token Refactor

## Goal

Rewrite skills into accurate, dense, token-efficient, machine-readable packages. Preserve behavior, frontmatter schema, and quality-adjusted token ROI.

## Use When

- User provides existing `SKILL.md` files or Markdown skill instructions.
- Task asks to compress, restructure, split, validate, or batch-optimize skills.
- Output should preserve trigger intent, inputs, outputs, safety behavior, and failure behavior.

## Do Not Use When

- Task asks to create unrelated product features.
- Source is not a skill or skill-like instruction.
- User asks to weaken constraints, remove safety behavior, or invent new behavior.

## Inputs

```text
source_skill_path
optional ConPort record IDs
optional source commit
rewrite scope
validation requirements
```

## Outputs

```text
optimized SKILL.md
moved content plan
script/schema/eval candidates
validation report
review_needed items
ConPort update candidate
```

## Workflow

Use the Refactor Workflow below.

## Global Skill Rules

All refactored skills follow this control plane unless a more specific source rule conflicts.

```text
GLOBAL.001 | MUST  | quality | accuracy + behavior preservation before compression
GLOBAL.002 | MUST  | tokens  | token efficiency = quality-adjusted output per token
GLOBAL.003 | MUST  | runtime | portable across coding-agent skill runtimes unless source requires otherwise; flag runtime-specific drift
GLOBAL.004 | MUST  | frontmatter | preserve existing YAML properties; optimize values only
GLOBAL.005 | MUST  | description | include use + do-not-use boundaries in description
GLOBAL.006 | NEVER | frontmatter | add use_when/do_not_use_when/required_inputs/expected_outputs/retrieval_policy/token_policy unless explicit
GLOBAL.007 | MUST  | language | choose fit-for-case LLM format: dense prose, schema-once rows, JSON Schema, code, or references
GLOBAL.008 | NEVER | wording | duplicate obligation signal in one rule line
GLOBAL.009 | NEVER | identifiers | use underscore IDs for prose-rule slugs; use hyphenated or plain terms
GLOBAL.010 | MUST  | identifiers | reserve underscores for real structured keys/properties/columns from source contracts; preserve source names
GLOBAL.011 | MUST  | validation | run validator underscore rule for SKILL.md rule prose
```

## Refactor Workflow

1. Query ConPort MCP for inventory, trigger summary, prior refactor notes, extracted rules, known risks, duplicates, and refactor status.
2. If ConPort is missing, stale, incomplete, or conflicting, read targeted source sections.
3. Inventory purpose, description, inputs, outputs, tools, references, rules, risks, and token-heavy areas.
4. Classify each section as `KEEP_SKILL`, `MOVE_REFERENCE`, `MOVE_SCRIPT`, `MOVE_SCHEMA`, `MOVE_EVAL`, `DISCARD_DUP`, or `REVIEW_NEEDED`.
5. Preserve existing YAML frontmatter schema; optimize existing values only.
6. Move long examples/background to `references/`; deterministic operations to `scripts/`; contracts to `schemas/`; regressions to `evals/`.
7. Verify behavior-critical rules against source before finalizing changed constraints.
8. Run package validator so prose rule slugs with underscores fail unless they are structured terms.
9. Emit report and ConPort update candidate.

## Frontmatter Policy

FRONT.001 | MUST  | skill | preserve existing frontmatter schema
FRONT.002 | MUST  | skill | preserve all existing frontmatter properties
FRONT.003 | NEVER | skill | add new frontmatter property during refactor without explicit instruction
FRONT.004 | NEVER | skill | delete existing frontmatter property during refactor without explicit instruction
FRONT.005 | NEVER | skill | rename existing frontmatter property without explicit instruction
FRONT.006 | SHOULD | skill | optimize existing frontmatter values for trigger precision + token efficiency
FRONT.007 | MUST  | skill | description = primary portable trigger surface
FRONT.008 | MUST  | skill | put use + do-not-use guidance inside description
FRONT.009 | MUST  | skill | unsupported or ambiguous frontmatter change -> review-needed
FRONT.NEW.001 | SHOULD | skill | minimal frontmatter when no existing schema is present
FRONT.NEW.002 | MUST   | skill | include name + description
FRONT.NEW.003 | NEVER  | skill | add use_when/do_not_use_when/required_inputs/expected_outputs/retrieval_policy/token_policy without explicit instruction
FRONT.NEW.004 | MAY    | skill | preserve/add tool-specific properties only when target runtime requires them
SKILL.001 | MUST  | skill | token budget = quality-adjusted ROI
SKILL.002 | MUST  | skill | SKILL.md = control plane only
SKILL.003 | NEVER | skill | long background/redundant examples in SKILL.md
SKILL.004 | MUST  | skill | description is trigger surface
SKILL.005 | MUST  | skill | clear use + do-not-use boundaries
SKILL.006 | MUST  | skill | preserve behavior-critical rules
SKILL.007 | MUST  | skill | preserve safety/rejection/failure behavior
SKILL.008 | SHOULD | skill | move long examples/background to references
SKILL.009 | SHOULD | skill | move deterministic work to scripts
SKILL.010 | MUST  | skill | ambiguity -> review-needed
## Description Rules

DESC.001 | MUST  | description | identify trigger surface + user intent
DESC.002 | MUST  | description | specific enough for skill selection
DESC.003 | NEVER | description | marketing copy/background summary
DESC.004 | MUST  | description | include use + do-not-use guidance
DESC.005 | MUST  | description | mention expected source/input + output type
DESC.006 | MUST  | description | mention behavior preservation + token ROI
## Token Optimization Rules

TOK.001 | MUST  | quality | preserve quality + behavior before token reduction
TOK.002 | MUST  | metric  | token efficiency = quality-adjusted output per token cost
TOK.003 | NEVER | rewrite | reduce tokens by deleting constraints/exceptions/failure modes
TOK.004 | SHOULD | rewrite | spend tokens for behavior preservation + verification when needed
TOK.005 | MUST  | report  | distinguish token reduction from quality-adjusted token ROI
## Context Format Routing Policy

CTXFMT.001 | MUST  | format | separate authoring/storage/boundary/projection/report formats
CTXFMT.002 | MUST  | skill  | keep SKILL.md as control plane, not knowledge dump
CTXFMT.003 | MUST  | prompt | schema-once compact rows for bulk model-visible context
CTXFMT.004 | MUST  | boundary | JSON Schema or Structured Outputs for tool/function boundaries
CTXFMT.005 | SHOULD | docs  | topic-scoped Markdown for long reference context
CTXFMT.006 | NEVER | skill  | hide hard rules only inside references
CTXFMT.007 | NEVER | prompt | verbose JSON/Markdown tables for bulk context when compact rows suffice
CTXFMT.008 | NEVER | logs   | runtime logs/conversation dumps as Markdown memory
Choose the most information-dense representation for the case; human readability is secondary to model precision.

```text
LANG.001 | MUST  | nuance       | use dense natural language for semantic judgment, caveats, and exceptions
LANG.002 | MUST  | repeated data| use schema-once compact rows for repeated records/rules
LANG.003 | MUST  | boundary     | use JSON Schema/Structured Outputs for tool contracts
LANG.004 | MUST  | deterministic| use scripts/code for repeatable transformations/validators
LANG.005 | SHOULD| references   | use Markdown references for long explanatory context loaded on demand
LANG.006 | NEVER | control      | optimize for human-readable prose when compact LLM-readable rules suffice
LANG.007 | MUST  | identifiers  | use hyphenated/plain rule slugs unless preserving real structured keys
```

## Rules

Apply all rule lines in this control plane, plus `../../docs/skill_format_policy.md`.

## Markdown Policy

MD.001 | MUST  | markdown | Markdown = container for instructions/references/reports
MD.002 | SHOULD | markdown | embed compact machine-readable blocks when precision matters
MD.003 | NEVER | markdown | Markdown for raw OTel span dumps/token records/event ledgers/bulk memory
MD.004 | SHOULD | markdown | avoid long prose/repeated bullets/deep headings/repeated examples/raw logs
MD.005 | MUST  | skill    | verbose Markdown skill section -> compact control-plane rules when behavior preserved
## ConPort-First Retrieval Policy

CONPORT.001 | MUST  | retrieval | query ConPort MCP before loading/searching full skill text
CONPORT.002 | MUST  | retrieval | use ConPort for inventory/trigger summary/prior notes/rules/risks first
CONPORT.003 | SHOULD | retrieval | raw skill text only after ConPort missing/stale/incomplete/conflicting
CONPORT.004 | MUST  | retrieval | verify source file before final rewrite when behavior-critical rules change
CONPORT.005 | NEVER | retrieval | use ConPort summary alone to delete/weaken source constraints
CONPORT.006 | NEVER | retrieval | load entire skill library when inventory/targeted lookup suffices
If ConPort MCP is unavailable: continue with targeted local reads and mark `conport_unavailable` or `source_verification_needed` when relevant.

## Machine-Readability Rules

MR.001 | MUST  | boundary | JSON Schema or Structured Outputs for tool/function boundaries
MR.002 | MUST  | bulk     | schema-once compact rows for bulk context
MR.003 | NEVER | logs     | runtime logs/conversation dumps as Markdown memory
READ.001 | MUST  | skill    | machine readability over human readability in control planes
READ.002 | SHOULD| docs     | human-readable summary only when it improves navigation/review
READ.003 | NEVER | skill    | long narrative prose for behavior rules when compact rule lines suffice
READ.004 | SHOULD| refs     | human explanations in detailed references, not SKILL.md
CACHE.001 | MUST  | prompt | stable system prompt prefix across batch skill rewrite runs
CACHE.002 | SHOULD | prompt | global rules/format policies/output contracts in stable prefix
CACHE.003 | SHOULD | prompt | variable skill-specific source material in dynamic suffix
CACHE.004 | NEVER | prompt | large variable source text inside global instruction prefix
CACHE.005 | SHOULD | batch  | same agent instruction + output template across batch runs
Dynamic suffix: target skill path, ConPort lookup result, targeted source excerpts, inventory record, rewrite-specific notes.

## Content Classification Rules

CLASS.001 | MUST  | classify | assign each source section one primary destination
CLASS.002 | MUST  | classify | conflicting/unclear section -> REVIEW_NEEDED
CLASS.003 | SHOULD | classify | repeated content -> DISCARD_DUP only after behavior check
PRES.001 | MUST  | preserve | keep behavior-critical constraints
PRES.002 | MUST  | preserve | keep safety/privacy/rejection/failure behavior
PRES.003 | MUST  | preserve | verify changed constraints against source
PRES.004 | NEVER | preserve | weaken/delete constraints from ConPort summary alone
PRES.005 | NEVER | behavior | invent new behavior
PRES.006 | MUST  | frontmatter | preserve existing YAML properties such as allowed_tools/model
## Script Candidate Rules

SCRIPT.001 | SHOULD | script | repeatable deterministic steps -> scripts
SCRIPT.002 | SHOULD | script | scripts stay dependency-light
SCRIPT.003 | MUST   | script | agent judgment stays in SKILL.md, not scripts
## Batch Processing Rules

BATCH.001 | MUST  | batch | inventory before rewrite
BATCH.002 | MUST  | batch | emit review queue for ambiguous/risky skills
BATCH.003 | NEVER | batch | rewrite entire library without inventory + review plan
Use `references/refactor_templates.md#single-skill-report`.

## Output Template: Batch

Use `references/refactor_templates.md#batch-report`.

## Verification

- Validate package structure with `../../scripts/validate_skill_package.py`.
- Confirm `SKILL.md` rule text avoids underscore prose slugs except real keys, ids, enum values, file names, or source contract terms.
- Compare behavior-critical rules against source when constraints change.
- Check moved content destinations exist.
- Check unresolved ambiguity is listed in `review_needed`.

## Failure Modes

- `conport_record_missing`: ConPort unavailable or no matching record.
- `source_verification_needed`: summary insufficient for safe rewrite.
- `review_needed`: ambiguity, conflict, or behavior-critical uncertainty.
- `blocked`: source unavailable, unsafe instruction, or impossible preservation requirement.

## References

- `references/refactor_templates.md`
- `references/classification_guide.md`
- `../../docs/skill_format_policy.md`

## Scripts

- `../../scripts/inventory_skills.py`
- `../../scripts/validate_skill_package.py`
- `../../scripts/estimate_skill_tokens.py`
- `../../scripts/generate_skill_refactor_report.py`
