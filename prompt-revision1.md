The first implementation is done and needs revision.

Scope of this revision only:

1. Preserve existing SKILL.md YAML frontmatter schema.
2. Do not add new YAML fields such as `use_when`, `do_not_use_when`, `required_inputs`, `expected_outputs`, `retrieval_policy`, or `token_policy`.
3. Do not delete or rename existing YAML fields.
4. Improve existing YAML field values only when behavior is preserved.
5. Put “when to use” and “when not to use” guidance into the `description` field.
6. Enforce ConPort-first retrieval before loading/searching full skill content.
7. Make machine readability and token efficiency higher priority than human readability.
8. Define token efficiency as quality-adjusted ROI, not blind token minimization.
9. Add stable-prefix guidance for token caching.

Do not implement unrelated features.

Do not implement DeliveryYield, dashboards, GraphDB, OTel processing, token economics reporting, model routing, or full platform features.

## 1. Inspect current implementation first

Before making changes, inspect relevant files:

```bash
find . -maxdepth 4 -type f | sort
```

Then review files related to:

```text
docs/skill_format_policy.md
docs/skill_refactor_pipeline.md
agents/skill_refactor_agent.md
skills/*/SKILL.md
scripts/inventory_skills.py
scripts/validate_skill_package.py
schemas/*.json
examples/sanitized/*
README.md
```

Preserve useful existing work. Make focused revisions only.

## 2. Correct frontmatter policy

Replace any rule that says new or rewritten skills must add fields like:

```text
use_when
do_not_use_when
required_inputs
expected_outputs
retrieval_policy
token_policy
x-lattice
```

with this rule:

```text
Do not add new YAML frontmatter fields.
Preserve the existing frontmatter schema.
Only optimize existing field values.
Use `description` as the primary progressive-disclosure trigger surface.
```

Required rule lines:

```text
FRONT.001 | MUST  | skill | preserve_existing_frontmatter_schema | enforce
FRONT.002 | MUST  | skill | preserve_all_existing_frontmatter_properties | enforce
FRONT.003 | NEVER | skill | add_new_frontmatter_property_during_refactor_without_explicit_instruction | block
FRONT.004 | NEVER | skill | delete_existing_frontmatter_property_during_refactor_without_explicit_instruction | block
FRONT.005 | NEVER | skill | rename_existing_frontmatter_property_without_explicit_instruction | block
FRONT.006 | SHOULD | skill | optimize_existing_frontmatter_values_for_trigger_precision_and_token_efficiency | prefer
FRONT.007 | MUST  | skill | keep_description_as_primary_portable_trigger_surface | enforce
FRONT.008 | MUST  | skill | put_when_to_use_and_when_not_to_use_guidance_inside_description | enforce
FRONT.009 | MUST  | skill | mark_unsupported_or_ambiguous_frontmatter_changes_as_review_needed | enforce
```

For newly created skills in this repo:

```text
FRONT.NEW.001 | SHOULD | skill | use_minimal_frontmatter_when_no_existing_schema_is_present | prefer
FRONT.NEW.002 | MUST   | skill | include_name_and_description | enforce
FRONT.NEW.003 | NEVER  | skill | add_use_when_do_not_use_when_required_inputs_expected_outputs_retrieval_policy_or_token_policy_fields_without_explicit_instruction | block
FRONT.NEW.004 | MAY    | skill | preserve_or_add_tool_specific_properties_only_when_target_runtime_requires_them | allow
```

## 3. Progressive disclosure via description only

Progressive disclosure is still mandatory, but it must be implemented through `description`, not through new YAML fields.

The optimized `description` should compactly include:

```text
what the skill does
when to use it
when not to use it
expected source/input type
expected output type
behavior-preservation requirement
token-efficiency requirement
ConPort-first retrieval expectation when relevant
```

Example:

```yaml
---
name: skill-token-refactor
description: "Rewrite existing SKILL.md or Markdown-based skill instructions into token-efficient, machine-readable Skill packages while preserving behavior. Use for skill compression, restructuring, validation, batch refactor planning, or splitting long skill content into references/scripts/schemas/evals. Before loading raw skill text, use ConPort MCP summaries or inventory when available. Do not use to execute the domain task described by a skill or when source material is insufficient to preserve constraints."
---
```

Do not create this:

```yaml
use_when:
  - ...
do_not_use_when:
  - ...
retrieval_policy:
  - ...
token_policy:
  - ...
```

## 4. ConPort-first retrieval

Add or preserve this rule across docs, agent instruction, skill package, examples, and validation docs:

```text
Query ConPort MCP before loading or searching the full content of any skill.
```

Purpose:

```text
Use ConPort as the first-pass structured index for skill inventory, trigger summary, prior refactor notes, extracted rules, known risks, duplicate candidates, and refactor status.
```

Required rule lines:

```text
CONPORT.001 | MUST  | retrieval | query_ConPort_MCP_before_loading_or_searching_full_skill_text | enforce
CONPORT.002 | MUST  | retrieval | use_ConPort_for_skill_inventory_trigger_summary_prior_refactor_notes_extracted_rules_known_risks_first | enforce
CONPORT.003 | SHOULD | retrieval | use_raw_skill_file_text_only_after_ConPort_result_is_missing_stale_incomplete_or_conflicting | prefer
CONPORT.004 | MUST  | retrieval | verify_against_source_file_before_final_rewrite_when_behavior_critical_rules_are_changed | enforce
CONPORT.005 | NEVER | retrieval | rely_on_ConPort_summary_alone_to_delete_or_weaken_source_skill_constraints | block
CONPORT.006 | NEVER | retrieval | load_entire_skill_library_text_when_inventory_or_targeted_lookup_suffices | block
```

Required retrieval order:

```text
ConPort MCP -> targeted source file read -> broader file search
```

If ConPort MCP is unavailable:

```text
- local scripts must still work on local files;
- agent instructions must still prefer ConPort first;
- mark output with conport_unavailable or source_verification_needed when relevant;
- do not make deterministic local scripts hard-depend on ConPort unless implementing an optional adapter.
```

Add risk flags where relevant:

```text
conport_record_missing
conport_record_stale
conport_unavailable
source_verification_needed
raw_file_loaded_without_conport_first
```

## 5. Human readability is not the default goal

Update docs and skill rules to state this clearly:

```text
Human-readable prose is not required by default.
Machine readability, low ambiguity, and token efficiency take priority.
```

Allowed human-readable areas:

```text
- short summary section at the top of a file
- manager-facing reports
- detailed reference documents intentionally written for humans
- examples intended for learning or review
```

Not allowed in default control planes:

```text
- long explanatory prose in SKILL.md
- narrative-only rules
- large Markdown tables for machine-facing data
- repeated bullet explanations when compact rules suffice
- deep heading trees that do not add machine-actionable structure
```

Add rule lines:

```text
READ.001 | MUST  | skill | prioritize_machine_readability_over_human_readability_in_control_planes | enforce
READ.002 | SHOULD | docs  | allow_human_readable_summary_only_when_it_improves_navigation_or_review | prefer
READ.003 | NEVER | skill | use_long_narrative_prose_for_behavior_rules_when_compact_rule_lines_suffice | warn
READ.004 | SHOULD | refs  | place_human_readable_explanations_in_detailed_reference_docs_not_SKILL_md | prefer
```

## 6. Token efficiency means quality-adjusted ROI

Revise all relevant docs and skill instructions to define token efficiency as:

```text
Token efficiency = high-quality output per token cost.
```

It does not mean:

```text
use the fewest tokens at any cost
```

It means:

```text
use tokens rationally to maximize quality-adjusted ROI.
```

Quality is fundamental and non-negotiable.

Do not reduce token usage by:

```text
- deleting behavior-critical rules;
- weakening safety, rejection, privacy, or failure behavior;
- removing edge cases or exceptions;
- skipping source verification when source verification is needed;
- producing lower-quality rewrites just to reduce token count.
```

Add rule lines:

```text
TOK.001 | MUST  | quality | preserve_quality_and_behavior_before_token_reduction | enforce
TOK.002 | MUST  | metric  | define_token_efficiency_as_quality_adjusted_output_per_token_cost | enforce
TOK.003 | NEVER | rewrite | reduce_tokens_by_deleting_constraints_exceptions_or_failure_modes | block
TOK.004 | SHOULD | rewrite | spend_tokens_when_needed_for_behavior_preservation_and_verification | prefer
TOK.005 | MUST  | report  | distinguish_token_reduction_from_quality_adjusted_token_ROI | enforce
```

## 7. Stable prefix and token caching

Add stable-prefix guidance to docs and agent instruction.

Goal:

```text
Improve token ROI by enabling provider-side prompt caching where available.
```

Rules:

```text
CACHE.001 | MUST  | prompt | keep_system_prompt_prefix_stable_across_batch_skill_rewrite_runs | enforce
CACHE.002 | SHOULD | prompt | put_global_rules_format_policies_and_output_contracts_in_stable_prefix | prefer
CACHE.003 | SHOULD | prompt | put_variable_skill_specific_source_material_in_dynamic_suffix | prefer
CACHE.004 | NEVER | prompt | interleave_large_variable_source_text_inside_global_instruction_prefix | warn
CACHE.005 | SHOULD | batch  | reuse_same_agent_instruction_and_output_template_across_batch_runs | prefer
```

Implementation guidance:

```text
Stable prefix:
- project identity
- current scope and non-goals
- skill rewrite rules
- frontmatter preservation policy
- description-based progressive disclosure policy
- ConPort-first retrieval policy
- machine-readability policy
- token ROI and quality rules
- output contract
- validation rules

Dynamic suffix:
- target skill path
- ConPort lookup result
- targeted source excerpts
- current inventory record
- rewrite-specific notes
```

State clearly:

```text
Prompt caching is not the only goal, but stable-prefix structure improves token economics, repeatability, and batch efficiency.
```

## 8. Script and schema updates

Update `scripts/inventory_skills.py` and `scripts/validate_skill_package.py` to support this revision.

Add or preserve inventory fields:

```text
frontmatter_keys
frontmatter_key_count
frontmatter_schema_preserved
description_has_use_boundary
description_has_do_not_use_boundary
description_mentions_inputs_or_source_type
description_mentions_outputs_or_result_type
description_mentions_behavior_preservation
description_mentions_conport_when_relevant
description_progressive_disclosure_ready
has_conport_first_policy
has_token_roi_policy
has_stable_prefix_guidance
```

Do not use these as errors:

```text
frontmatter_has_extra_keys
frontmatter_only_name_description
missing_use_when_frontmatter
missing_do_not_use_when_frontmatter
```

Replace with these risk flags:

```text
frontmatter_schema_changed
frontmatter_property_deleted
frontmatter_property_renamed
frontmatter_schema_change_review_needed
description_missing_use_boundary
description_missing_do_not_use_boundary
description_not_progressive_disclosure_ready
missing_conport_first_policy
missing_token_roi_policy
stable_prefix_guidance_missing
human_prose_overused_in_control_plane
```

Validation behavior:

```text
- For refactoring existing skills, do not delete or rename existing frontmatter properties unless explicitly instructed.
- For newly created skills, prefer minimal frontmatter with name and description unless target runtime requires more.
- Do not require use_when or do_not_use_when fields.
- Description must carry progressive disclosure information.
- Scripts must remain dependency-light.
- Scripts must not require ConPort to run.
```

## 9. Example updates

Update sanitized examples so `sample_skill_after.md` demonstrates:

```text
- existing frontmatter schema preserved;
- no existing frontmatter property deleted;
- when-to-use and when-not-to-use guidance included in description;
- ConPort-first retrieval rule;
- compact machine-readable control plane;
- minimal human prose;
- token efficiency as quality-adjusted ROI;
- stable-prefix/token-cache guidance;
- behavior-critical rules preserved.
```

Use an example with extra frontmatter fields to prove preservation, for example:

```yaml
---
name: sample-data-cleaner
description: "Clean and normalize tabular data with deterministic scripts while preserving validation behavior. Use for existing CSV/JSON cleanup skill refactors; do not use for unrelated data analysis or when source rules are insufficient. Query ConPort summaries before loading raw skill text when available."
allowed-tools: Read Write Bash
model: sonnet
---
```

The optimized skill may improve `description`, but must preserve:

```text
allowed-tools
model
```

## 10. README updates

Update README to mention that the current revision enforces:

```text
- preserving existing frontmatter schemas during refactor;
- not adding use_when or do_not_use_when YAML fields;
- putting when-to-use and when-not-to-use guidance inside description;
- ConPort-first retrieval before loading full skill text;
- machine readability over human readability in control planes;
- token efficiency as quality-adjusted ROI;
- stable prefix guidance for token caching.
```

Keep README focused on Skill Rewrite / Skill Refactor only.

Do not add DeliveryYield implementation details.

## 11. Quality gates

Run:

```bash
find . -maxdepth 4 -type f | sort
python scripts/inventory_skills.py --root skills --out /tmp/skill_inventory.jsonl
python scripts/validate_skill_package.py --root skills
python scripts/generate_skill_refactor_report.py --inventory /tmp/skill_inventory.jsonl --out /tmp/skill_quality_report.md
```

Fix errors if possible.

If warnings remain intentionally, report them.

## 12. Final response

Report:

```text
Summary:
- files changed
- frontmatter schema preservation updates
- description-based progressive disclosure updates
- ConPort-first policy updates
- machine-readability updates
- token ROI / quality rule updates
- stable prefix / caching updates
- script/schema/example updates
- validation result

Remaining warnings:
- list warnings and whether acceptable

Deferred:
- anything intentionally not done
```
