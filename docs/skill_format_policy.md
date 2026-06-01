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

CTXFMT.001 | MUST  | format | separate_authoring_storage_boundary_projection_report_formats | enforce
CTXFMT.002 | MUST  | skill  | keep_SKILL_md_as_control_plane_not_knowledge_dump | enforce
CTXFMT.003 | MUST  | prompt | use_schema_once_compact_rows_for_bulk_model_visible_context | enforce
CTXFMT.004 | MUST  | boundary | use_JSON_Schema_or_Structured_Outputs_for_tool_function_boundaries | enforce
CTXFMT.005 | SHOULD | docs  | use_topic_scoped_markdown_for_long_reference_context | prefer
CTXFMT.006 | NEVER | skill  | hide_hard_rules_only_inside_references | block
CTXFMT.007 | NEVER | prompt | use_verbose_JSON_or_Markdown_tables_for_bulk_context_when_compact_rows_suffice | warn
CTXFMT.008 | NEVER | logs   | store_runtime_logs_or_raw_transcripts_as_Markdown_memory | block

## Markdown Policy

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
DY.001 | MUST  | report | use_feature_delivery_case_as_primary_unit | enforce
DY.002 | NEVER | report | lead_with_PR_trace_for_manager_report     | block
```

Avoid:

```text
The system should generally try to focus on feature-level delivery rather than PR-level details because managers usually care more about whether the feature is usable...
```

MD.001 | MUST  | markdown | use_Markdown_as_container_for_instructions_references_and_reports | enforce
MD.002 | SHOULD | markdown | embed_compact_machine_readable_blocks_inside_Markdown_when_precision_matters | prefer
MD.003 | NEVER | markdown | use_Markdown_for_raw_OTel_span_dumps_token_records_event_ledgers_or_bulk_memory | block
MD.004 | SHOULD | markdown | avoid_long_prose_repeated_bullets_tables_deep_headings_repeated_examples_and_raw_logs | prefer
MD.005 | MUST  | skill    | rewrite_verbose_Markdown_skill_sections_into_compact_control_plane_rules_when_behavior_is_preserved | enforce

## Frontmatter Preservation Policy

Do not add new YAML frontmatter fields. Preserve the existing frontmatter schema. Only optimize existing field values. Use `description` as the primary progressive-disclosure trigger surface.

FRONT.001 | MUST  | skill | preserve_existing_frontmatter_schema | enforce
FRONT.002 | MUST  | skill | preserve_all_existing_frontmatter_properties | enforce
FRONT.003 | NEVER | skill | add_new_frontmatter_property_during_refactor_without_explicit_instruction | block
FRONT.004 | NEVER | skill | delete_existing_frontmatter_property_during_refactor_without_explicit_instruction | block
FRONT.005 | NEVER | skill | rename_existing_frontmatter_property_without_explicit_instruction | block
FRONT.006 | SHOULD | skill | optimize_existing_frontmatter_values_for_trigger_precision_and_token_efficiency | prefer
FRONT.007 | MUST  | skill | keep_description_as_primary_portable_trigger_surface | enforce
FRONT.008 | MUST  | skill | put_when_to_use_and_when_not_to_use_guidance_inside_description | enforce
FRONT.009 | MUST  | skill | mark_unsupported_or_ambiguous_frontmatter_changes_as_review_needed | enforce

FRONT.NEW.001 | SHOULD | skill | use_minimal_frontmatter_when_no_existing_schema_is_present | prefer
FRONT.NEW.002 | MUST   | skill | include_name_and_description | enforce
FRONT.NEW.003 | NEVER  | skill | add_use_when_do_not_use_when_required_inputs_expected_outputs_retrieval_policy_or_token_policy_fields_without_explicit_instruction | block
FRONT.NEW.004 | MAY    | skill | preserve_or_add_tool_specific_properties_only_when_target_runtime_requires_them | allow

The optimized `description` compactly includes what the skill does, when to use it, when not to use it, expected source/input type, expected output type, behavior-preservation requirement, token-efficiency requirement, and ConPort-first retrieval expectation when relevant.

## ConPort-First Retrieval Policy

For skill rewrite/refactor work, query ConPort MCP before loading or searching the full content of any skill.

Goal: use ConPort as the first-pass structured index for skill inventory, trigger summary, prior refactor notes, extracted rules, known risks, duplicate candidates, and refactor status.

CONPORT.001 | MUST  | retrieval | query_ConPort_MCP_before_loading_or_searching_full_skill_text | enforce
CONPORT.002 | MUST  | retrieval | use_ConPort_for_skill_inventory_trigger_summary_prior_refactor_notes_extracted_rules_known_risks_first | enforce
CONPORT.003 | SHOULD | retrieval | use_raw_skill_file_text_only_after_ConPort_result_is_missing_stale_incomplete_or_conflicting | prefer
CONPORT.004 | MUST  | retrieval | verify_against_source_file_before_final_rewrite_when_behavior_critical_rules_are_changed | enforce
CONPORT.005 | NEVER | retrieval | rely_on_ConPort_summary_alone_to_delete_or_weaken_source_skill_constraints | block
CONPORT.006 | NEVER | retrieval | load_entire_skill_library_text_when_inventory_or_targeted_lookup_suffices | block

Required retrieval order:

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

READ.001 | MUST  | skill | prioritize_machine_readability_over_human_readability_in_control_planes | enforce
READ.002 | SHOULD | docs  | allow_human_readable_summary_only_when_it_improves_navigation_or_review | prefer
READ.003 | NEVER | skill | use_long_narrative_prose_for_behavior_rules_when_compact_rule_lines_suffice | warn
READ.004 | SHOULD | refs  | place_human_readable_explanations_in_detailed_reference_docs_not_SKILL_md | prefer

## Token ROI Policy

Token efficiency = high-quality output per token cost.

Token efficiency does not mean using the fewest tokens at any cost. Use tokens rationally to maximize quality-adjusted ROI. Quality is fundamental and non-negotiable.

Do not reduce token usage by deleting behavior-critical rules, weakening safety/rejection/privacy/failure behavior, removing edge cases or exceptions, skipping needed source verification, or producing lower-quality rewrites just to reduce token count.

TOK.001 | MUST  | quality | preserve_quality_and_behavior_before_token_reduction | enforce
TOK.002 | MUST  | metric  | define_token_efficiency_as_quality_adjusted_output_per_token_cost | enforce
TOK.003 | NEVER | rewrite | reduce_tokens_by_deleting_constraints_exceptions_or_failure_modes | block
TOK.004 | SHOULD | rewrite | spend_tokens_when_needed_for_behavior_preservation_and_verification | prefer
TOK.005 | MUST  | report  | distinguish_token_reduction_from_quality_adjusted_token_ROI | enforce

## Stable Prefix And Token Caching

Prompt caching is not the only goal, but stable-prefix structure improves token economics, repeatability, and batch efficiency.

CACHE.001 | MUST  | prompt | keep_system_prompt_prefix_stable_across_batch_skill_rewrite_runs | enforce
CACHE.002 | SHOULD | prompt | put_global_rules_format_policies_and_output_contracts_in_stable_prefix | prefer
CACHE.003 | SHOULD | prompt | put_variable_skill_specific_source_material_in_dynamic_suffix | prefer
CACHE.004 | NEVER | prompt | interleave_large_variable_source_text_inside_global_instruction_prefix | warn
CACHE.005 | SHOULD | batch  | reuse_same_agent_instruction_and_output_template_across_batch_runs | prefer

Stable prefix:

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
CTX.001 | MUST | context | separate_authoring_storage_boundary_projection_report_formats | enforce
```

SKILL.001 | MUST  | skill | SKILL_md_token_budget=quality_adjusted_ROI | enforce
SKILL.002 | MUST  | skill | SKILL_md_control_plane_only | enforce
SKILL.003 | NEVER | skill | SKILL_md_contains_long_background_or_redundant_examples | warn
SKILL.004 | MUST  | skill | description_is_trigger_surface | enforce
SKILL.005 | MUST  | skill | include_clear_Use_When_and_Do_Not_Use_When_boundaries | enforce
SKILL.006 | MUST  | skill | preserve_behavior_critical_rules | enforce
SKILL.007 | MUST  | skill | preserve_safety_rejection_and_failure_behavior | enforce
SKILL.008 | SHOULD | skill | move_long_examples_and_background_to_references | prefer
SKILL.009 | SHOULD | skill | move_deterministic_work_to_scripts | prefer
SKILL.010 | MUST  | skill | mark_ambiguity_as_review_needed | enforce

Target optimized structure:

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
