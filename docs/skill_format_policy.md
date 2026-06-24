# Skill Format Policy

## Global Context Format Routing Policy

Need | Recommended format | Avoid
---|---|---
Always-loaded project rules | Markdown container + compact rule manifest | Long prose, deep YAML, deep JSON
Module contract | Markdown + line-oriented rules | Narrative-only docs
Skill control plane | SKILL.md + references/scripts/schemas/evals | Huge all-in-one skill file
Long reference context | Topic-scoped Markdown | Hidden hard rules inside references
Agent handoff | JSONL + JSON Schema | Freeform chat handoff
Tool/function input/output | JSON Schema / Structured Outputs | Unvalidated plain text
Runtime event log | Append-only JSONL | Markdown logs, raw transcript memory
Operational query store | SQLite/Postgres | Markdown as database
Bulk context into LLM | LATPACK / schema-once compact rows | Verbose JSON, Markdown tables
Graph relationships | GraphDB internally; compact edge list for prompt | Raw Cypher path / RDF dump in prompt
Analytics/eval | Parquet / DuckDB / Arrow | Prompt-level aggregation
Manager report | Markdown | Compact machine rows
Token economics report | Markdown dossier + JSON structured result | Raw telemetry dump

CTXFMT.001 | MUST  | format | separate authoring, storage, boundary, projection, report formats
CTXFMT.002 | MUST  | skill  | keep SKILL.md as control plane, not knowledge dump
CTXFMT.003 | MUST  | prompt | use schema-once compact rows for bulk model-visible context
CTXFMT.004 | MUST  | boundary | use JSON Schema or Structured Outputs for tool/function boundaries
CTXFMT.005 | SHOULD | docs  | use topic-scoped Markdown for long reference context
CTXFMT.006 | NEVER | skill  | hide hard rules only inside references
CTXFMT.007 | NEVER | prompt | use verbose JSON or Markdown tables for bulk context when compact rows suffice
CTXFMT.008 | NEVER | logs   | store runtime logs or raw transcripts as Markdown memory
Markdown acceptable:

```text
instructions
module contracts
SKILL.md
references
architecture explanations
manager-facing reports
```

Markdown not appropriate:

```text
OTel span dumps
token usage records
event ledger
bulk memory records
graph edge lists
tool result batches
stage breakdown data
```

Markdown token risk comes less from syntax and more from misuse.

High-cost Markdown patterns:

```text
long prose explanations
repeated bullets
Markdown tables
deeply nested headings
repeated examples
raw logs pasted as Markdown
```

Prefer Markdown as container with compact machine-readable blocks inside it.

Example:

```text
DY.001 | MUST  | report | use feature_delivery_case as primary unit
DY.002 | NEVER | report | lead with PR trace for manager report
```

Avoid:

```text
The system should generally try to focus on feature-level delivery rather than PR-level details because managers usually care more about whether the feature is usable...
```

MD.001 | MUST  | markdown | use Markdown as container for instructions, references, reports
MD.002 | SHOULD | markdown | embed compact machine-readable blocks in Markdown when precision matters
MD.003 | NEVER | markdown | use Markdown for raw OTel span dumps, token records, event ledgers, bulk memory
MD.004 | SHOULD | markdown | avoid long prose, repeated bullets/tables/headings/examples, raw logs
MD.005 | MUST  | skill    | rewrite verbose Markdown skill sections as compact control-plane rules when behavior is preserved
Do not add new YAML frontmatter fields. Preserve the existing frontmatter schema. Only optimize existing field values. Use `description` as the primary progressive-disclosure trigger surface.

FRONT.001 | MUST  | skill | preserve existing frontmatter schema
FRONT.002 | MUST  | skill | preserve all existing frontmatter properties
FRONT.003 | NEVER | skill | add new frontmatter property during refactor without explicit instruction
FRONT.004 | NEVER | skill | delete existing frontmatter property during refactor without explicit instruction
FRONT.005 | NEVER | skill | rename existing frontmatter property without explicit instruction
FRONT.006 | SHOULD | skill | optimize existing frontmatter values for trigger precision + token efficiency
FRONT.007 | MUST  | skill | description is primary portable trigger surface
FRONT.008 | MUST  | skill | put use + do-not-use guidance inside description
FRONT.009 | MUST  | skill | mark unsupported or ambiguous frontmatter changes as review_needed
FRONT.NEW.001 | SHOULD | skill | use minimal frontmatter when no existing schema is present
FRONT.NEW.002 | MUST   | skill | include name + description
FRONT.NEW.003 | NEVER  | skill | add use_when/do_not_use_when/required_inputs/expected_outputs/retrieval_policy/token_policy fields without explicit instruction
FRONT.NEW.004 | MAY    | skill | preserve or add tool-specific properties only when target runtime requires them
## ConPort-First Retrieval Policy

For skill rewrite/refactor work, query ConPort MCP before loading or searching the full content of any skill.

Goal: use ConPort as the first-pass structured index for skill inventory, trigger summary, prior refactor notes, extracted rules, known risks, duplicate candidates, and refactor status.

CONPORT.001 | MUST  | retrieval | query ConPort MCP before loading or searching full skill text
CONPORT.002 | MUST  | retrieval | use ConPort for skill inventory, trigger summary, prior notes, rules, risks first
CONPORT.003 | SHOULD | retrieval | use raw skill text only after ConPort result missing, stale, incomplete, or conflicting
CONPORT.004 | MUST  | retrieval | verify source file before final rewrite when behavior-critical rules change
CONPORT.005 | NEVER | retrieval | rely on ConPort summary alone to delete or weaken source constraints
CONPORT.006 | NEVER | retrieval | load entire skill library when inventory or targeted lookup suffices
```text
ConPort MCP -> targeted source file read -> broader file search
```

Agent behavior:

```text
- Before scanning raw Markdown skill text, ask ConPort MCP for the relevant skill name/path/domain.
- If ConPort returns an inventory record, use it as the first-pass source.
- If ConPort returns stale or incomplete data, mark it `needs_source_verification`.
- Do not use ConPort as the only authority for deleting constraints.
- Use ConPort to avoid repeated parsing of the same skill files.
- After a skill is refactored, record or emit an update candidate for ConPort containing skill path, optimized name, optimized description, trigger summary, source behavior-critical rules, moved content plan, review_needed items, estimated before/after token size, and refactor status.
```

If ConPort MCP is unavailable, local scripts must still work on local files, agent instructions must still prefer ConPort first, outputs should mark `conport_unavailable` or `source_verification_needed` when relevant, and deterministic scripts must not hard-depend on ConPort unless implementing an optional adapter.

Risk flags:

```text
conport_record_missing
conport_record_stale
conport_unavailable
source_verification_needed
raw_file_loaded_without_conport_first
```

## Machine Readability Policy

Human-readable prose is not required by default. Machine readability, low ambiguity, and token efficiency take priority.

Allowed human-readable areas:

```text
short summary section at the top of a file
manager-facing reports
detailed reference documents intentionally written for humans
examples intended for learning or review
```

Not allowed in default control planes:

```text
long explanatory prose in SKILL.md
narrative-only rules
large Markdown tables for machine-facing data
repeated bullet explanations when compact rules suffice
deep heading trees that do not add machine-actionable structure
```

READ.001 | MUST  | skill | prioritize machine readability over human readability in control planes
READ.002 | SHOULD | docs  | allow human-readable summary only when it improves navigation or review
READ.003 | NEVER | skill | use long narrative prose for behavior rules when compact rows suffice
READ.004 | SHOULD | refs  | place human-readable explanations in detailed references, not SKILL.md
Token efficiency = high-quality output per token cost.

Token efficiency does not mean using the fewest tokens at any cost. Use tokens rationally to maximize quality-adjusted ROI. Quality is fundamental and non-negotiable.

Do not reduce token usage by deleting behavior-critical rules, weakening safety/rejection/privacy/failure behavior, removing edge cases or exceptions, skipping needed source verification, or producing lower-quality rewrites just to reduce token count.

TOK.001 | MUST  | quality | preserve quality + behavior before token reduction
TOK.002 | MUST  | metric  | define token efficiency as quality-adjusted output per token cost
TOK.003 | NEVER | rewrite | reduce tokens by deleting constraints, exceptions, or failure modes
TOK.004 | SHOULD | rewrite | spend tokens when needed for behavior preservation + verification
TOK.005 | MUST  | report  | distinguish token reduction from quality-adjusted token ROI
Prompt caching is not the only goal, but stable-prefix structure improves token economics, repeatability, and batch efficiency.

CACHE.001 | MUST  | prompt | keep system prompt prefix stable across batch skill rewrite runs
CACHE.002 | SHOULD | prompt | put global rules, format policies, output contracts in stable prefix
CACHE.003 | SHOULD | prompt | put variable skill-specific source material in dynamic suffix
CACHE.004 | NEVER | prompt | interleave large variable source text inside global instruction prefix
CACHE.005 | SHOULD | batch  | reuse same agent instruction + output template across batch runs
```text
project identity
current scope and non-goals
skill rewrite rules
frontmatter preservation policy
description-based progressive disclosure policy
ConPort-first retrieval policy
machine-readability policy
token ROI and quality rules
output contract
validation rules
```

Dynamic suffix:

```text
target skill path
ConPort lookup result
targeted source excerpts
current inventory record
rewrite-specific notes
```

## Skill Package Layout Policy

```text
SKILL.md = compact control plane
references/ = long background, examples, variants
scripts/ = deterministic repeatable operations
schemas/ = input/output contracts
evals/ = regression examples
assets/ = final output assets only
```

Documents should be machine-readable, low-ambiguity, and token-efficient. Human readability is optional and should not be prioritized when it conflicts with compactness, structure, or machine processing efficiency.

Example compact rule:

```text
CTX.001 | MUST | context | separate authoring, storage, boundary, projection, report formats
SKILL.001 | MUST  | skill | SKILL.md token budget = quality-adjusted ROI
SKILL.002 | MUST  | skill | SKILL.md control plane only
SKILL.003 | NEVER | skill | SKILL.md contains long background or redundant examples
SKILL.004 | MUST  | skill | description is trigger surface
SKILL.005 | MUST  | skill | include clear Use When + Do Not Use When boundaries
SKILL.006 | MUST  | skill | preserve behavior-critical rules
SKILL.007 | MUST  | skill | preserve safety, rejection, failure behavior
SKILL.008 | SHOULD | skill | move long examples + background to references
SKILL.009 | SHOULD | skill | move deterministic work to scripts
SKILL.010 | MUST  | skill | mark ambiguity as review_needed
```

```text
skill-name/
  SKILL.md
  references/
  scripts/
  schemas/
  evals/
  assets/
```

`SKILL.md` control plane sections:

```text
Goal
Use When
Do Not Use When
Inputs
Outputs
Workflow
Rules
References
Scripts
Verification
Failure Modes
```
