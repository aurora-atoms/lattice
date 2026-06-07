---
name: skill-token-refactor
description: "Use in GitHub Copilot or Claude Code when rewriting existing SKILL.md or Markdown skill instructions into accurate, dense, token-efficient, machine-readable skill packages while preserving behavior and existing YAML frontmatter schema. Use for skill compression, restructuring, validation, batch refactor planning, language-format selection, or splitting content into references/scripts/schemas/evals. Do not use to execute the domain task described by a skill, invent behavior, weaken constraints, or refactor when source material is insufficient to preserve rules. Put when-to-use and when-not-to-use guidance inside description instead of adding Claude-specific frontmatter fields unless explicitly required. Before raw skill text, use ConPort MCP summaries/inventory when available; optimize for quality-adjusted token ROI, not blind token minimization."
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
GLOBAL.001 | MUST  | quality | accuracy + behavior preservation before compression | fail if degraded
GLOBAL.002 | MUST  | tokens  | token efficiency = quality-adjusted output per token | reject blind minimization
GLOBAL.003 | MUST  | runtime | portable for GitHub Copilot + Claude Code unless source requires otherwise | flag runtime-specific drift
GLOBAL.004 | MUST  | frontmatter | preserve existing YAML properties; optimize values only | fail schema drift
GLOBAL.005 | MUST  | description | include use + do-not-use boundaries in description | fail weak trigger
GLOBAL.006 | NEVER | frontmatter | add use_when/do_not_use_when/required_inputs/expected_outputs/retrieval_policy/token_policy unless explicit | block schema expansion
GLOBAL.007 | MUST  | language | choose fit-for-case LLM format: dense prose, schema-once rows, JSON Schema, code, or references | fail wrong format
GLOBAL.008 | NEVER | wording | duplicate obligation signal in one rule line | compress
GLOBAL.009 | NEVER | identifiers | use underscore IDs for prose-rule slugs | use hyphenated or plain terms
GLOBAL.010 | MUST  | identifiers | reserve underscores for real structured keys/properties/columns from source contracts | preserve source names
```

## Refactor Workflow

1. Query ConPort MCP for inventory, trigger summary, prior refactor notes, extracted rules, known risks, duplicates, and refactor status.
2. If ConPort is missing, stale, incomplete, or conflicting, read targeted source sections.
3. Inventory purpose, description, inputs, outputs, tools, references, rules, risks, and token-heavy areas.
4. Classify each section as `KEEP_SKILL`, `MOVE_REFERENCE`, `MOVE_SCRIPT`, `MOVE_SCHEMA`, `MOVE_EVAL`, `DISCARD_DUP`, or `REVIEW_NEEDED`.
5. Preserve existing YAML frontmatter schema; optimize existing values only.
6. Move long examples/background to `references/`; deterministic operations to `scripts/`; contracts to `schemas/`; regressions to `evals/`.
7. Verify behavior-critical rules against source before finalizing changed constraints.
8. Emit report and ConPort update candidate.

## Frontmatter Policy

FRONT.001 | MUST  | skill | preserve existing frontmatter schema | fail schema drift
FRONT.002 | MUST  | skill | preserve all existing frontmatter properties | fail property loss
FRONT.003 | NEVER | skill | add new frontmatter property during refactor without explicit instruction | block
FRONT.004 | NEVER | skill | delete existing frontmatter property during refactor without explicit instruction | block
FRONT.005 | NEVER | skill | rename existing frontmatter property without explicit instruction | block
FRONT.006 | SHOULD | skill | optimize existing frontmatter values for trigger precision + token efficiency | prefer
FRONT.007 | MUST  | skill | description = primary portable trigger surface | fail weak trigger
FRONT.008 | MUST  | skill | put use + do-not-use guidance inside description | fail incomplete trigger
FRONT.009 | MUST  | skill | unsupported or ambiguous frontmatter change -> review-needed | fail silent ambiguity

FRONT.NEW.001 | SHOULD | skill | minimal frontmatter when no existing schema is present | prefer
FRONT.NEW.002 | MUST   | skill | include name + description | fail missing trigger
FRONT.NEW.003 | NEVER  | skill | add use_when/do_not_use_when/required_inputs/expected_outputs/retrieval_policy/token_policy without explicit instruction | block
FRONT.NEW.004 | MAY    | skill | preserve/add tool-specific properties only when target runtime requires them | allow

## SKILL.md Rewrite Rules

SKILL.001 | MUST  | skill | token budget = quality-adjusted ROI | fail blind compression
SKILL.002 | MUST  | skill | SKILL.md = control plane only | fail knowledge dump
SKILL.003 | NEVER | skill | long background/redundant examples in SKILL.md | warn
SKILL.004 | MUST  | skill | description is trigger surface | fail missing trigger
SKILL.005 | MUST  | skill | clear use + do-not-use boundaries | fail ambiguous routing
SKILL.006 | MUST  | skill | preserve behavior-critical rules | fail behavior drift
SKILL.007 | MUST  | skill | preserve safety/rejection/failure behavior | fail safety drift
SKILL.008 | SHOULD | skill | move long examples/background to references | prefer
SKILL.009 | SHOULD | skill | move deterministic work to scripts | prefer
SKILL.010 | MUST  | skill | ambiguity -> review-needed | fail silent ambiguity

## Description Rules

DESC.001 | MUST  | description | identify trigger surface + user intent | fail weak trigger
DESC.002 | MUST  | description | specific enough for skill selection | fail broad trigger
DESC.003 | NEVER | description | marketing copy/background summary | block
DESC.004 | MUST  | description | include use + do-not-use guidance | fail incomplete trigger
DESC.005 | MUST  | description | mention expected source/input + output type | fail missing contract
DESC.006 | MUST  | description | mention behavior preservation + token ROI | fail missing optimization goal

## Token Optimization Rules

TOK.001 | MUST  | quality | preserve quality + behavior before token reduction | fail degraded rewrite
TOK.002 | MUST  | metric  | token efficiency = quality-adjusted output per token cost | fail blind minimization
TOK.003 | NEVER | rewrite | reduce tokens by deleting constraints/exceptions/failure modes | block
TOK.004 | SHOULD | rewrite | spend tokens for behavior preservation + verification when needed | prefer
TOK.005 | MUST  | report  | distinguish token reduction from quality-adjusted token ROI | fail vague report

## Context Format Routing Policy

CTXFMT.001 | MUST  | format | separate authoring/storage/boundary/projection/report formats | fail format conflation
CTXFMT.002 | MUST  | skill  | keep SKILL.md as control plane, not knowledge dump | fail bloat
CTXFMT.003 | MUST  | prompt | schema-once compact rows for bulk model-visible context | fail verbose bulk
CTXFMT.004 | MUST  | boundary | JSON Schema or Structured Outputs for tool/function boundaries | fail loose boundary
CTXFMT.005 | SHOULD | docs  | topic-scoped Markdown for long reference context | prefer
CTXFMT.006 | NEVER | skill  | hide hard rules only inside references | block
CTXFMT.007 | NEVER | prompt | verbose JSON/Markdown tables for bulk context when compact rows suffice | warn
CTXFMT.008 | NEVER | logs   | runtime logs/conversation dumps as Markdown memory | block

## LLM Language Routing

Choose the most information-dense representation for the case; human readability is secondary to model precision.

```text
LANG.001 | MUST  | nuance       | use dense natural language for semantic judgment, caveats, and exceptions | fail underspecified nuance
LANG.002 | MUST  | repeated data| use schema-once compact rows for repeated records/rules | fail verbose repetition
LANG.003 | MUST  | boundary     | use JSON Schema/Structured Outputs for tool contracts | fail ambiguous interface
LANG.004 | MUST  | deterministic| use scripts/code for repeatable transformations/validators | fail manual procedure bloat
LANG.005 | SHOULD| references   | use Markdown references for long explanatory context loaded on demand | prefer
LANG.006 | NEVER | control      | optimize for human-readable prose when compact LLM-readable rules suffice | block
LANG.007 | MUST  | identifiers  | use hyphenated/plain rule slugs unless preserving real structured keys | fail inefficient slug
```

## Rules

Apply all rule lines in this control plane, plus `../../docs/skill_format_policy.md`.

## Markdown Policy

MD.001 | MUST  | markdown | Markdown = container for instructions/references/reports | fail wrong container
MD.002 | SHOULD | markdown | embed compact machine-readable blocks when precision matters | prefer
MD.003 | NEVER | markdown | Markdown for raw OTel span dumps/token records/event ledgers/bulk memory | block
MD.004 | SHOULD | markdown | avoid long prose/repeated bullets/deep headings/repeated examples/raw logs | prefer
MD.005 | MUST  | skill    | verbose Markdown skill section -> compact control-plane rules when behavior preserved | fail bloat

## ConPort-First Retrieval Policy

CONPORT.001 | MUST  | retrieval | query ConPort MCP before loading/searching full skill text | fail retrieval order
CONPORT.002 | MUST  | retrieval | use ConPort for inventory/trigger summary/prior notes/rules/risks first | fail missed summary
CONPORT.003 | SHOULD | retrieval | raw skill text only after ConPort missing/stale/incomplete/conflicting | prefer
CONPORT.004 | MUST  | retrieval | verify source file before final rewrite when behavior-critical rules change | fail unverified change
CONPORT.005 | NEVER | retrieval | use ConPort summary alone to delete/weaken source constraints | block
CONPORT.006 | NEVER | retrieval | load entire skill library when inventory/targeted lookup suffices | block

Required order: `ConPort MCP -> targeted source file read -> broader file search`.

If ConPort MCP is unavailable: continue with targeted local reads and mark `conport_unavailable` or `source_verification_needed` when relevant.

## Machine-Readability Rules

MR.001 | MUST  | boundary | JSON Schema or Structured Outputs for tool/function boundaries | fail ambiguous boundary
MR.002 | MUST  | bulk     | schema-once compact rows for bulk context | fail verbose bulk
MR.003 | NEVER | logs     | runtime logs/conversation dumps as Markdown memory | block
READ.001 | MUST  | skill    | machine readability over human readability in control planes | fail low-density prose
READ.002 | SHOULD| docs     | human-readable summary only when it improves navigation/review | prefer
READ.003 | NEVER | skill    | long narrative prose for behavior rules when compact rule lines suffice | warn
READ.004 | SHOULD| refs     | human explanations in detailed references, not SKILL.md | prefer

## Stable Prefix Guidance

CACHE.001 | MUST  | prompt | stable system prompt prefix across batch skill rewrite runs | fail cache churn
CACHE.002 | SHOULD | prompt | global rules/format policies/output contracts in stable prefix | prefer
CACHE.003 | SHOULD | prompt | variable skill-specific source material in dynamic suffix | prefer
CACHE.004 | NEVER | prompt | large variable source text inside global instruction prefix | warn
CACHE.005 | SHOULD | batch  | same agent instruction + output template across batch runs | prefer

Stable prefix: project identity, scope/non-goals, rewrite rules, frontmatter preservation, description-based progressive disclosure, ConPort-first retrieval, machine-readability, token ROI, output contract, validation rules.

Dynamic suffix: target skill path, ConPort lookup result, targeted source excerpts, inventory record, rewrite-specific notes.

## Content Classification Rules

CLASS.001 | MUST  | classify | assign each source section one primary destination | fail unclassified section
CLASS.002 | MUST  | classify | conflicting/unclear section -> REVIEW_NEEDED | fail silent ambiguity
CLASS.003 | SHOULD | classify | repeated content -> DISCARD_DUP only after behavior check | prefer

## Behavior Preservation Rules

PRES.001 | MUST  | preserve | keep behavior-critical constraints | fail behavior drift
PRES.002 | MUST  | preserve | keep safety/privacy/rejection/failure behavior | fail safety drift
PRES.003 | MUST  | preserve | verify changed constraints against source | fail unverified change
PRES.004 | NEVER | preserve | weaken/delete constraints from ConPort summary alone | block
PRES.005 | NEVER | behavior | invent new behavior | block
PRES.006 | MUST  | frontmatter | preserve existing YAML properties such as allowed_tools/model | fail property drift

## Script Candidate Rules

SCRIPT.001 | SHOULD | script | repeatable deterministic steps -> scripts | prefer
SCRIPT.002 | SHOULD | script | scripts stay dependency-light | prefer
SCRIPT.003 | MUST   | script | agent judgment stays in SKILL.md, not scripts | fail misplaced judgment

## Batch Processing Rules

BATCH.001 | MUST  | batch | inventory before rewrite | fail missing inventory
BATCH.002 | MUST  | batch | emit review queue for ambiguous/risky skills | fail missing review queue
BATCH.003 | NEVER | batch | rewrite entire library without inventory + review plan | block

## Output Template: Single Skill

Use `references/refactor_templates.md#single-skill-report`.

## Output Template: Batch

Use `references/refactor_templates.md#batch-report`.

## Verification

- Validate package structure with `../../scripts/validate_skill_package.py`.
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
