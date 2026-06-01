# Skill Rewrite / Skill Refactor only

This phase is only for building a reusable, repo-native system to rewrite existing Markdown-based skills into token-efficient, machine-readable, high-accuracy Skill packages.

## 0. License

Use Apache License 2.0.

If `LICENSE` does not exist, add the full Apache License 2.0 text.

Use SPDX identifiers where appropriate:

```text
SPDX-License-Identifier: Apache-2.0
```

For Python scripts, add this near the top when reasonable:

```python
# SPDX-License-Identifier: Apache-2.0
```

Do not add company-specific copyright notices.

## 1. Repo purpose for this phase

This repo phase provides generic tooling, standards, schemas, examples, and agent instructions for skill rewriting.

The immediate feature is:

```text
Skill Rewrite / Skill Refactor System
```

It should help refactor many existing Markdown-based skills into optimized Skill packages.

Primary objective:

```text
old Markdown skill
  -> ConPort-first retrieval
  -> inventory
  -> classification
  -> token-friendly rewrite plan
  -> optimized SKILL.md
  -> moved content plan
  -> validation report
```

Do not automatically rewrite thousands of skills yet.

Build the agent instruction, skill package, scripts, schemas, examples, and validation workflow needed to support that process.

## 2. Project identity

Lattice is the project name only.

Rules:

```text
project_display_name = Lattice
project_id = lattice
namespace = lat
```

Never use `lattice` as a module name, agent name, schema name, artifact name, or record type.

Active modules exist but are not in current implementation scope:

```text
Helixion
AegisFlow
Memexa
FlowGuard
OpenClaw
DeliveryYield
```

Do not mark them as legacy, deprecated, historical, or reference-only.

Focus only on the skill rewrite/refactor feature.

## 4. Target repo structure

Inspect the current repo first. Preserve useful existing files. Do not blindly overwrite.

Create or update this minimal structure:

```text
README.md
LICENSE

docs/
  skill_refactor_pipeline.md
  skill_format_policy.md

agents/
  skill_refactor_agent.md

skills/
  skill-token-refactor/
    SKILL.md
    references/
    scripts/
    schemas/
    evals/

scripts/
  inventory_skills.py
  validate_skill_package.py
  estimate_skill_tokens.py
  generate_skill_refactor_report.py

schemas/
  skill.inventory.v1.schema.json
  skill.refactor_report.v1.schema.json
  skill.package_check.v1.schema.json

templates/
  skill_refactor_report.template.md

examples/
  sanitized/
    sample_skill_before.md
    sample_skill_after.md

.github/
  workflows/
    skill-validate.yml
```

If the repo already has a reasonable structure, adapt rather than duplicate.

## 5. Add global context format routing policy

Add the following decision matrix into `docs/skill_format_policy.md`. The goal is to make future skill rewrites token-friendly, machine-readable, and unambiguous by choosing the correct format for each context layer.

```text
Need | Recommended format | Avoid
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
```

Also add these rules:

```text
CTXFMT.001 | MUST  | format | separate_authoring_storage_boundary_projection_report_formats | enforce
CTXFMT.002 | MUST  | skill  | keep_SKILL_md_as_control_plane_not_knowledge_dump | enforce
CTXFMT.003 | MUST  | prompt | use_schema_once_compact_rows_for_bulk_model_visible_context | enforce
CTXFMT.004 | MUST  | boundary | use_JSON_Schema_or_Structured_Outputs_for_tool_function_boundaries | enforce
CTXFMT.005 | SHOULD | docs  | use_topic_scoped_markdown_for_long_reference_context | prefer
CTXFMT.006 | NEVER | skill  | hide_hard_rules_only_inside_references | block
CTXFMT.007 | NEVER | prompt | use_verbose_JSON_or_Markdown_tables_for_bulk_context_when_compact_rows_suffice | warn
CTXFMT.008 | NEVER | logs   | store_runtime_logs_or_raw_transcripts_as_Markdown_memory | block
```

## 6. Add Markdown Policy

Add the following Markdown Policy into `docs/skill_format_policy.md`.

Markdown is acceptable for:

```text
instructions
module contracts
SKILL.md
references
architecture explanations
manager-facing reports
```

Markdown is not appropriate for:

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

Prefer:

```text
Markdown as container.
Compact machine-readable blocks inside it.
```

Example:

```text
DY.001 | MUST  | report | use_feature_delivery_case_as_primary_unit | enforce
DY.002 | NEVER | report | lead_with_PR_trace_for_manager_report     | block
```

Avoid:

```text
The system should generally try to focus on feature-level delivery rather than PR-level details because managers usually care more about whether the feature is usable...
```

Also add these rule lines:

```text
MD.001 | MUST  | markdown | use_Markdown_as_container_for_instructions_references_and_reports | enforce
MD.002 | SHOULD | markdown | embed_compact_machine_readable_blocks_inside_Markdown_when_precision_matters | prefer
MD.003 | NEVER | markdown | use_Markdown_for_raw_OTel_span_dumps_token_records_event_ledgers_or_bulk_memory | block
MD.004 | SHOULD | markdown | avoid_long_prose_repeated_bullets_tables_deep_headings_repeated_examples_and_raw_logs | prefer
MD.005 | MUST  | skill    | rewrite_verbose_Markdown_skill_sections_into_compact_control_plane_rules_when_behavior_is_preserved | enforce
```

## 7. Add ConPort-First Retrieval Policy

Add this policy to `docs/skill_format_policy.md`, `agents/skill_refactor_agent.md`, and `skills/skill-token-refactor/SKILL.md`.

For skill rewrite/refactor work, always query ConPort MCP before searching or loading raw skill file text.

Goal:

Reduce token usage by using structured memory, indexes, summaries, inventories, and prior extraction results before reading large Markdown skill files.

Rules:

```text
CONPORT.001 | MUST  | retrieval | query_ConPort_MCP_before_raw_skill_file_text_search | enforce
CONPORT.002 | MUST  | retrieval | use_ConPort_for_skill_inventory_trigger_summary_prior_refactor_notes_and_known_risks_first | enforce
CONPORT.003 | SHOULD | retrieval | use_raw_skill_file_text_only_after_ConPort_result_is_missing_stale_incomplete_or_conflicting | prefer
CONPORT.004 | MUST  | retrieval | preserve_ConPort_record_ids_or_source_refs_when_using_ConPort_results | enforce
CONPORT.005 | MUST  | retrieval | verify_against_source_file_before_final_rewrite_when_behavior_critical_rules_are_changed | enforce
CONPORT.006 | NEVER | retrieval | rely_on_ConPort_summary_alone_to_delete_or_weaken_source_skill_constraints | block
CONPORT.007 | NEVER | retrieval | load_entire_skill_library_text_when_inventory_or_targeted_lookup_suffices | block
```

Required retrieval order:

```text
1. Query ConPort MCP for existing skill inventory, trigger summary, prior refactor notes, known risks, duplicates, and extracted rules.
2. If ConPort has sufficient current records, use those records to plan the rewrite.
3. Load raw source skill text only for targeted verification, missing sections, conflicts, behavior-critical rules, or final rewrite.
4. Prefer targeted file reads over full-library search.
5. Preserve source path, ConPort record ID, and source commit when available.
```

Agent behavior:

```text
- Before scanning raw Markdown skill text, ask ConPort MCP for the relevant skill name/path/domain.
- If ConPort returns an inventory record, use it as the first-pass source.
- If ConPort returns stale or incomplete data, mark it `needs_source_verification`.
- Do not use ConPort as the only authority for deleting constraints.
- Use ConPort to avoid repeated parsing of the same skill files.
- After a skill is refactored, record or emit an update candidate for ConPort containing:
  - skill path
  - optimized name
  - optimized description
  - trigger summary
  - source behavior-critical rules
  - moved content plan
  - review_needed items
  - estimated before/after token size
  - refactor status
```

Important:

If ConPort MCP is unavailable in the current environment, scripts should still work on local files, but agent instructions must prefer this order:

```text
ConPort MCP -> targeted source file read -> broader file search
```

Do not make local scripts hard-depend on ConPort unless explicitly implementing a ConPort adapter.

Add these risk flags to inventory and validation docs:

```text
conport_record_missing
conport_record_stale
source_verification_needed
raw_file_loaded_without_conport_first
```

## 8. Documentation to add

### docs/skill_format_policy.md

Define token-friendly Skill package rules.

Start with:

1. Global context format routing policy from section 5.
2. Markdown Policy from section 6.
3. ConPort-First Retrieval Policy from section 7.

Then define this skill package layout policy:

```text
SKILL.md = compact control plane
references/ = long background, examples, variants
scripts/ = deterministic repeatable operations
schemas/ = input/output contracts
evals/ = regression examples
assets/ = final output assets only
```

Rules:

* Documents should be machine-readable and token-friendly.
* Human readability is optional and should not be prioritized when it conflicts with compactness, structure, or machine processing efficiency.
* Use compact rule lines when possible.

Example:

```text
CTX.001 | MUST | context | separate_authoring_storage_boundary_projection_report_formats | enforce
```

Skill-specific rules:

```text
SKILL.001 | MUST  | skill | SKILL_md_token_budget=minimize | enforce
SKILL.002 | MUST  | skill | SKILL_md_control_plane_only | enforce
SKILL.003 | NEVER | skill | SKILL_md_contains_long_background_or_redundant_examples | warn
SKILL.004 | MUST  | skill | description_is_trigger_surface | enforce
SKILL.005 | MUST  | skill | include_clear_Use_When_and_Do_Not_Use_When_boundaries | enforce
SKILL.006 | MUST  | skill | preserve_behavior_critical_rules | enforce
SKILL.007 | MUST  | skill | preserve_safety_rejection_and_failure_behavior | enforce
SKILL.008 | SHOULD | skill | move_long_examples_and_background_to_references | prefer
SKILL.009 | SHOULD | skill | move_deterministic_work_to_scripts | prefer
SKILL.010 | MUST  | skill | mark_ambiguity_as_review_needed | enforce
```

Target optimized Skill structure:

```text
skill-name/
  SKILL.md
  references/
  scripts/
  schemas/
  evals/
  assets/
```

`SKILL.md` should act as the control plane and should include:

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

### docs/skill_refactor_pipeline.md

Define three phases:

```text
Phase 1: Inventory
Phase 2: Rewrite
Phase 3: Validate
```

Batch outputs:

```text
skill_inventory.jsonl
skill_quality_report.md
review_queue.jsonl
duplicate_candidates.jsonl
script_candidates.jsonl
optimized_skills/
migration_report.md
```

Include batch status categories:

```text
auto_safe
review_needed
duplicate_candidate
split_candidate
merge_candidate
deprecated_candidate
blocked
```

## 9. Add agent instruction

Create or update:

```text
agents/skill_refactor_agent.md
```

It should define:

```text
agent_role = skill_refactor_agent
scope = skill_rewrite, skill_compression, skill_package_refactor
activation = task_scoped
primary_output = optimized_skill_package_or_patch
```

Mission:

```text
Rewrite existing Markdown-based skills into token-efficient, machine-readable, high-accuracy skill packages while preserving behavior.
```

Required behavior:

* preserve behavior-critical constraints;
* preserve trigger intent;
* preserve inputs and outputs;
* preserve safety, privacy, rejection, and failure behavior;
* separate rules from procedures;
* rewrite `SKILL.md` as a compact control plane;
* apply the context format routing policy from `docs/skill_format_policy.md`;
* apply the Markdown Policy from `docs/skill_format_policy.md`;
* apply ConPort-First Retrieval Policy before searching or loading raw source skill text;
* flag ambiguity as `review_needed`;
* never silently delete or weaken constraints;
* never invent new behavior.

Classify source sections as:

```text
KEEP_SKILL
MOVE_REFERENCE
MOVE_SCRIPT
MOVE_SCHEMA
MOVE_EVAL
DISCARD_DUP
REVIEW_NEEDED
```

Output template for one skill:

```text
# Skill Refactor Report

## Verdict
auto_safe | review_needed | blocked

## Source Inventory
- current name:
- current description:
- detected purpose:
- inputs:
- outputs:
- tools/scripts:
- references:
- risk areas:

## Behavior-Critical Rules Preserved
- ...

## Proposed Package Layout
...

## Optimized Description
...

## Optimized SKILL.md
...

## Moved Content Plan
| Source Section | Destination | Reason |
|---|---|---|

## Script / Schema / Eval Candidates
- ...

## Review Needed
- ...
```

## 10. Add skill package: skill-token-refactor

Create:

```text
skills/skill-token-refactor/
  SKILL.md
  references/
  scripts/
  schemas/
  evals/
```

`SKILL.md` frontmatter:

```yaml
---
name: skill-token-refactor
description: Rewrite existing Markdown-based skills into token-efficient, machine-readable, high-accuracy skill packages. Use when the user has existing SKILL.md files or Markdown skill instructions and wants to compress, restructure, split, validate, or batch-optimize them while preserving behavior.
---
```

The skill must include these sections:

```text
Goal
Use When
Do Not Use When
Inputs
Outputs
Refactor Workflow
SKILL.md Rewrite Rules
Description Rules
Token Optimization Rules
Markdown Policy
ConPort-First Retrieval Policy
Machine-Readability Rules
Content Classification Rules
Behavior Preservation Rules
Script Candidate Rules
Batch Processing Rules
Output Template: Single Skill
Output Template: Batch
Verification
Failure Modes
```

Keep `SKILL.md` concise. Move long detail to `references/`.

The skill must emphasize:

* `SKILL.md` is the control plane, not a knowledge dump.
* Query ConPort MCP before searching or loading raw source skill text.
* Raw source skill files should be loaded only when ConPort is missing, stale, incomplete, conflicting, or when final behavior-preservation verification requires source text.
* Markdown is acceptable as a container, but not for raw logs, telemetry dumps, token records, event ledgers, or bulk machine records.
* Long examples go to `references/`.
* Deterministic repeatable work goes to `scripts/`.
* Input/output contracts go to `schemas/`.
* Regression examples go to `evals/`.
* Behavior-critical rules must be preserved.
* Ambiguity must be marked `review_needed`.
* Token reduction must not damage correctness.
* The context format routing policy must guide all rewrite decisions.

## 11. Add deterministic scripts

Implement dependency-light Python scripts. They should work without external APIs.

### scripts/inventory_skills.py

Arguments:

```text
--root <skills_dir>
--out <skill_inventory.jsonl>
```

Scan for `SKILL.md` and Markdown skill-like files.

Output JSONL records with at least:

```text
path
name
description
line_count
estimated_tokens
has_frontmatter
has_goal
has_use_when
has_do_not_use_when
has_inputs
has_outputs
has_workflow
has_rules
has_verification
has_failure_modes
reference_count
script_count
schema_count
eval_count
risk_flags
```

Approximate token estimate may be `chars / 4`.

Risk flags should include at least:

```text
missing_frontmatter
missing_description
missing_goal
missing_use_when
missing_workflow
missing_verification
missing_failure_modes
large_skill_md
possible_knowledge_dump
raw_log_or_transcript_pattern
vague_description
markdown_table_bulk_context
verbose_json_bulk_context
hidden_hard_rules_in_references
long_prose_explanations
repeated_bullets
deeply_nested_headings
repeated_examples
conport_record_missing
conport_record_stale
source_verification_needed
raw_file_loaded_without_conport_first
```

### scripts/validate_skill_package.py

Arguments:

```text
--root <skills_dir_or_skill_dir>
```

Checks:

* `SKILL.md` exists;
* YAML frontmatter exists;
* `name` exists and is lowercase;
* `description` exists;
* required sections are present;
* description is not empty or excessively huge;
* `SKILL.md` is not a huge knowledge dump;
* referenced local files exist when easy to detect;
* no obvious raw transcript/log dump patterns;
* no obvious bulk Markdown tables in machine-facing context;
* no hard rules hidden only in references when detectable;
* no excessive repeated bullets or deeply nested heading structure in `SKILL.md` when avoidable.

Exit nonzero on errors. Print warnings separately.

### scripts/estimate_skill_tokens.py

Arguments:

```text
--root <skills_dir_or_skill_dir>
```

Output:

```text
path
estimated_tokens
file_count
skill_md_tokens
reference_tokens
script_count
```

### scripts/generate_skill_refactor_report.py

Arguments:

```text
--inventory <skill_inventory.jsonl>
--out <skill_quality_report.md>
```

Generate Markdown report:

* total skills;
* largest skills;
* missing sections;
* risk flags;
* top refactor candidates;
* review queue.

Keep all scripts deterministic and dependency-light.

ConPort note:

* Do not make these local scripts hard-depend on ConPort unless explicitly implementing a ConPort adapter.
* Scripts must work on local files.
* Agent-level retrieval should still prefer ConPort MCP before raw source file reads.

## 12. Add schemas

Create minimal valid JSON Schemas:

```text
schemas/skill.inventory.v1.schema.json
schemas/skill.refactor_report.v1.schema.json
schemas/skill.package_check.v1.schema.json
```

Keep schemas simple but valid.

`skill.inventory.v1.schema.json` should match the JSONL records emitted by `inventory_skills.py`.

`skill.package_check.v1.schema.json` should cover validation result shape.

`skill.refactor_report.v1.schema.json` should cover report metadata, verdict, moved content plan, candidates, and review-needed items.

## 13. Add examples

Create sanitized examples only:

```text
examples/sanitized/sample_skill_before.md
examples/sanitized/sample_skill_after.md
```

The before example should show an overly verbose Markdown-style skill.

The after example should show:

```text
SKILL.md as compact control plane
long examples moved to references
deterministic step marked as script_candidate
failure modes explicit
context format routing applied
Markdown Policy applied
ConPort-first retrieval noted
```

Do not include company examples.

## 14. Add GitHub Action

Create:

```text
.github/workflows/skill-validate.yml
```

It should run on pull request and optionally push.

Suggested commands:

```bash
python scripts/inventory_skills.py --root skills --out skill_inventory.jsonl
python scripts/validate_skill_package.py --root skills
python scripts/generate_skill_refactor_report.py --inventory skill_inventory.jsonl --out skill_quality_report.md
```

If `skills/` is missing or empty, handle gracefully.

Do not require external services or secrets.

## 15. README

Update README to explain:

* What this repo is;
* Apache-2.0 license;
* This phase focuses only on Skill Rewrite / Skill Refactor;
* The core context format routing policy;
* The Markdown Policy;
* The ConPort-first retrieval policy;
* Quickstart commands:

```bash
python scripts/inventory_skills.py --root skills --out skill_inventory.jsonl
python scripts/validate_skill_package.py --root skills
python scripts/generate_skill_refactor_report.py --inventory skill_inventory.jsonl --out skill_quality_report.md
```

* What outputs mean;
* What is deferred.

Keep README focused. Do not add DeliveryYield implementation instructions in this phase.

## 16. Quality gates

Before finishing, run:

```bash
find . -maxdepth 4 -type f | sort
python scripts/inventory_skills.py --root skills --out /tmp/skill_inventory.jsonl
python scripts/validate_skill_package.py --root skills
python scripts/generate_skill_refactor_report.py --inventory /tmp/skill_inventory.jsonl --out /tmp/skill_quality_report.md
```

Fix errors.

If something cannot run, report the exact failure and why.

## 17. Final response

When done, report:

```text
Summary:
- files created/updated
- scripts added
- skill package added
- schemas added
- validation result

How to run:
- commands

Notes:
- assumptions
- deferred work
- review-needed decisions
```
