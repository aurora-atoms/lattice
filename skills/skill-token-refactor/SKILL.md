---
name: skill-token-refactor
description: "Rewrite existing SKILL.md or Markdown-based skill instructions into token-efficient, machine-readable Skill packages while preserving behavior and existing YAML frontmatter schema. Use for skill compression, restructuring, validation, batch refactor planning, or splitting long skill content into references/scripts/schemas/evals; do not use to execute the domain task described by a skill or when source material is insufficient to preserve constraints. Before loading raw skill text, use ConPort MCP summaries or inventory when available; optimize for quality-adjusted token ROI."
---

# Skill Token Refactor

## Goal

Rewrite Markdown-based skills into compact, machine-readable Skill packages while preserving behavior, existing frontmatter schema, and quality-adjusted token ROI.

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

## SKILL.md Rewrite Rules

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

## Description Rules

DESC.001 | MUST | description | identify_trigger_surface_and_user_intent | enforce
DESC.002 | MUST | description | remain_specific_enough_for_skill_selection | enforce
DESC.003 | NEVER | description | become_marketing_copy_or_background_summary | block
DESC.004 | MUST | description | include_when_to_use_and_when_not_to_use_guidance | enforce
DESC.005 | MUST | description | mention_expected_source_or_input_and_output_type | enforce
DESC.006 | MUST | description | mention_behavior_preservation_and_token_ROI | enforce

## Token Optimization Rules

TOK.001 | MUST  | quality | preserve_quality_and_behavior_before_token_reduction | enforce
TOK.002 | MUST  | metric  | define_token_efficiency_as_quality_adjusted_output_per_token_cost | enforce
TOK.003 | NEVER | rewrite | reduce_tokens_by_deleting_constraints_exceptions_or_failure_modes | block
TOK.004 | SHOULD | rewrite | spend_tokens_when_needed_for_behavior_preservation_and_verification | prefer
TOK.005 | MUST  | report  | distinguish_token_reduction_from_quality_adjusted_token_ROI | enforce

## Context Format Routing Policy

CTXFMT.001 | MUST  | format | separate_authoring_storage_boundary_projection_report_formats | enforce
CTXFMT.002 | MUST  | skill  | keep_SKILL_md_as_control_plane_not_knowledge_dump | enforce
CTXFMT.003 | MUST  | prompt | use_schema_once_compact_rows_for_bulk_model_visible_context | enforce
CTXFMT.004 | MUST  | boundary | use_JSON_Schema_or_Structured_Outputs_for_tool_function_boundaries | enforce
CTXFMT.005 | SHOULD | docs  | use_topic_scoped_markdown_for_long_reference_context | prefer
CTXFMT.006 | NEVER | skill  | hide_hard_rules_only_inside_references | block
CTXFMT.007 | NEVER | prompt | use_verbose_JSON_or_Markdown_tables_for_bulk_context_when_compact_rows_suffice | warn
CTXFMT.008 | NEVER | logs   | store_runtime_logs_or_raw_transcripts_as_Markdown_memory | block

## Rules

Apply all rule lines in this control plane, plus `../../docs/skill_format_policy.md`.

## Markdown Policy

MD.001 | MUST  | markdown | use_Markdown_as_container_for_instructions_references_and_reports | enforce
MD.002 | SHOULD | markdown | embed_compact_machine_readable_blocks_inside_Markdown_when_precision_matters | prefer
MD.003 | NEVER | markdown | use_Markdown_for_raw_OTel_span_dumps_token_records_event_ledgers_or_bulk_memory | block
MD.004 | SHOULD | markdown | avoid_long_prose_repeated_bullets_tables_deep_headings_repeated_examples_and_raw_logs | prefer
MD.005 | MUST  | skill    | rewrite_verbose_Markdown_skill_sections_into_compact_control_plane_rules_when_behavior_is_preserved | enforce

## ConPort-First Retrieval Policy

CONPORT.001 | MUST  | retrieval | query_ConPort_MCP_before_loading_or_searching_full_skill_text | enforce
CONPORT.002 | MUST  | retrieval | use_ConPort_for_skill_inventory_trigger_summary_prior_refactor_notes_extracted_rules_known_risks_first | enforce
CONPORT.003 | SHOULD | retrieval | use_raw_skill_file_text_only_after_ConPort_result_is_missing_stale_incomplete_or_conflicting | prefer
CONPORT.004 | MUST  | retrieval | verify_against_source_file_before_final_rewrite_when_behavior_critical_rules_are_changed | enforce
CONPORT.005 | NEVER | retrieval | rely_on_ConPort_summary_alone_to_delete_or_weaken_source_skill_constraints | block
CONPORT.006 | NEVER | retrieval | load_entire_skill_library_text_when_inventory_or_targeted_lookup_suffices | block

Required order: `ConPort MCP -> targeted source file read -> broader file search`.

If ConPort MCP is unavailable: continue with targeted local reads and mark `conport_unavailable` or `source_verification_needed` when relevant.

## Machine-Readability Rules

MR.001 | MUST | boundary | use_JSON_Schema_or_Structured_Outputs_for_tool_function_boundaries | enforce
MR.002 | MUST | bulk | use_schema_once_compact_rows_for_bulk_context | enforce
MR.003 | NEVER | logs | store_runtime_logs_or_raw_transcripts_as_Markdown_memory | block
READ.001 | MUST  | skill | prioritize_machine_readability_over_human_readability_in_control_planes | enforce
READ.002 | SHOULD | docs  | allow_human_readable_summary_only_when_it_improves_navigation_or_review | prefer
READ.003 | NEVER | skill | use_long_narrative_prose_for_behavior_rules_when_compact_rule_lines_suffice | warn
READ.004 | SHOULD | refs  | place_human_readable_explanations_in_detailed_reference_docs_not_SKILL_md | prefer

## Stable Prefix Guidance

CACHE.001 | MUST  | prompt | keep_system_prompt_prefix_stable_across_batch_skill_rewrite_runs | enforce
CACHE.002 | SHOULD | prompt | put_global_rules_format_policies_and_output_contracts_in_stable_prefix | prefer
CACHE.003 | SHOULD | prompt | put_variable_skill_specific_source_material_in_dynamic_suffix | prefer
CACHE.004 | NEVER | prompt | interleave_large_variable_source_text_inside_global_instruction_prefix | warn
CACHE.005 | SHOULD | batch  | reuse_same_agent_instruction_and_output_template_across_batch_runs | prefer

Stable prefix: project identity, scope/non-goals, rewrite rules, frontmatter preservation, description-based progressive disclosure, ConPort-first retrieval, machine-readability, token ROI, output contract, validation rules.

Dynamic suffix: target skill path, ConPort lookup result, targeted source excerpts, inventory record, rewrite-specific notes.

## Content Classification Rules

CLASS.001 | MUST | classify | assign_each_source_section_one_primary_destination | enforce
CLASS.002 | MUST | classify | mark_conflicting_or_unclear_sections_REVIEW_NEEDED | enforce
CLASS.003 | SHOULD | classify | mark_repeated_content_DISCARD_DUP_only_after_behavior_check | prefer

## Behavior Preservation Rules

PRES.001 | MUST  | preserve | keep_behavior_critical_constraints | enforce
PRES.002 | MUST  | preserve | keep_safety_privacy_rejection_failure_behavior | enforce
PRES.003 | MUST  | preserve | verify_changed_constraints_against_source | enforce
PRES.004 | NEVER | preserve | weaken_or_delete_constraints_from_ConPort_summary_alone | block
PRES.005 | NEVER | behavior | invent_new_behavior | block
PRES.006 | MUST  | frontmatter | preserve_existing_YAML_properties_like_allowed_tools_or_model | enforce

## Script Candidate Rules

SCRIPT.001 | SHOULD | script | move_repeatable_deterministic_steps_to_scripts | prefer
SCRIPT.002 | SHOULD | script | keep_scripts_dependency_light | prefer
SCRIPT.003 | MUST   | script | keep_agent_judgment_in_SKILL_md_not_scripts | enforce

## Batch Processing Rules

BATCH.001 | MUST  | batch | inventory_before_rewrite | enforce
BATCH.002 | MUST  | batch | emit_review_queue_for_ambiguous_or_risky_skills | enforce
BATCH.003 | NEVER | batch | rewrite_entire_library_without_inventory_and_review_plan | block

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
