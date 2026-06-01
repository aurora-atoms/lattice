# Classification Guide

KEEP_SKILL | Stays in `SKILL.md` because it controls activation, workflow, rules, verification, or failure behavior.
MOVE_REFERENCE | Move long background, examples, variants, and explanatory context to `references/`.
MOVE_SCRIPT | Move repeatable deterministic operations to `scripts/`.
MOVE_SCHEMA | Move input/output contracts and structured report formats to `schemas/`.
MOVE_EVAL | Move regression examples and expected behavior checks to `evals/`.
DISCARD_DUP | Remove only when duplicate content has no unique constraint or behavior.
REVIEW_NEEDED | Use for ambiguity, conflicts, stale ConPort records, missing source verification, or behavior-critical uncertainty.

Risk flags:

```text
conport_record_missing
conport_record_stale
conport_unavailable
source_verification_needed
raw_file_loaded_without_conport_first
missing_frontmatter
missing_description
large_skill_md
possible_knowledge_dump
hidden_hard_rules_in_references
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
