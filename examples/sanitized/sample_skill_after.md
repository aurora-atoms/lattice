---
name: sample-data-cleaner
description: "Clean and normalize CSV/JSON cleanup skill instructions with deterministic scripts while preserving validation, rejection behavior, and existing frontmatter schema. Use for refactoring data-cleaning skills into compact packages; do not use for unrelated data analysis or when source rules are insufficient. Query ConPort summaries before loading raw skill text when available and optimize for quality-adjusted token ROI."
allowed-tools: Read Write Bash
model: sonnet
---

# Sample Data Cleaner

## Goal

Refactor data-cleaning skill instructions into a compact package without changing validation behavior.

## Use When

- Source is an existing CSV/JSON cleanup skill or skill-like Markdown instruction.

## Do Not Use When

- Task is unrelated data analysis.
- Source rules are insufficient to preserve constraints.

## Inputs

```text
source_skill_path
ConPort inventory or summary when available
targeted source excerpts
```

## Outputs

```text
optimized SKILL.md
moved content plan
script candidates
validation report
```

## Workflow

1. Query ConPort MCP before loading or searching full skill text.
2. Read targeted source excerpts only when ConPort is missing, stale, incomplete, or conflicting.
3. Preserve existing frontmatter properties: `name`, `description`, `allowed-tools`, `model`.
4. Keep validation and rejection behavior.
5. Move deterministic cleanup steps to `scripts/`.
6. Keep global policy in a stable prefix and source-specific material in a dynamic suffix.

## Rules

FRONT.001 | MUST  | skill | preserve_existing_frontmatter_schema | enforce
FRONT.008 | MUST  | skill | put_when_to_use_and_when_not_to_use_guidance_inside_description | enforce
CONPORT.001 | MUST | retrieval | query_ConPort_MCP_before_loading_or_searching_full_skill_text | enforce
READ.001 | MUST  | skill | prioritize_machine_readability_over_human_readability_in_control_planes | enforce
TOK.001 | MUST  | quality | preserve_quality_and_behavior_before_token_reduction | enforce
TOK.002 | MUST  | metric | define_token_efficiency_as_quality_adjusted_output_per_token_cost | enforce
CACHE.001 | MUST | prompt | keep_system_prompt_prefix_stable_across_batch_skill_rewrite_runs | enforce
DATA.001 | MUST  | validation | preserve_required_column_rejection_behavior | enforce
DATA.002 | NEVER | cleanup | delete_rows_unless_source_rules_explicitly_allow_it | block

## References

- `references/data-cleaning-examples.md`

## Scripts

- script_candidate: header normalization
- script_candidate: whitespace trimming
- script_candidate: required-column validation

## Verification

- Confirm `allowed-tools` and `model` remain in frontmatter.
- Confirm no `use_when`, `do_not_use_when`, `required_inputs`, `expected_outputs`, `retrieval_policy`, or `token_policy` YAML fields were added.
- Confirm validation/rejection rules are preserved.

## Failure Modes

- `conport_unavailable`: continue with targeted reads and mark source verification needs.
- `source_verification_needed`: ConPort record is missing, stale, incomplete, or conflicting.
- `review_needed`: frontmatter change is ambiguous or behavior preservation cannot be verified.
