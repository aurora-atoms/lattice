# Skill Refactor Pipeline

## Phase 1: Inventory

Goal: identify skill packages, trigger surfaces, package shape, token risk, missing sections, script/schema/eval candidates, and ConPort verification flags.

Inputs:

```text
skills_root
optional ConPort records
target skill paths
```

Outputs:

```text
skill_inventory.jsonl
duplicate_candidates.jsonl
script_candidates.jsonl
review_queue.jsonl
```

Status categories:

```text
auto_safe
review_needed
duplicate_candidate
split_candidate
merge_candidate
deprecated_candidate
blocked
```

## Phase 2: Rewrite

Goal: transform each source skill into a compact control-plane `SKILL.md` with long material moved to references, deterministic work moved to scripts, contracts moved to schemas, and regression examples moved to evals.

Classification:

```text
KEEP_SKILL
MOVE_REFERENCE
MOVE_SCRIPT
MOVE_SCHEMA
MOVE_EVAL
DISCARD_DUP
REVIEW_NEEDED
```

Required behavior:

```text
preserve existing frontmatter schema
preserve all existing frontmatter properties
put when-to-use and when-not-to-use guidance in description
use description as primary progressive-disclosure trigger surface
preserve trigger intent
preserve behavior-critical constraints
preserve inputs and outputs
preserve safety/privacy/rejection/failure behavior
optimize for quality-adjusted token ROI, not blind token minimization
keep stable prompt prefix across batch runs
never invent new behavior
never silently delete or weaken constraints
mark ambiguity as review_needed
```

Outputs:

```text
optimized_skills/
migration_report.md
review_queue.jsonl
```

## Phase 3: Validate

Goal: check optimized packages for structure, trigger quality, missing required sections, token risks, bad Markdown usage, missing references, and unresolved review flags.

Outputs:

```text
skill_quality_report.md
review_queue.jsonl
```

Quality gates:

```text
SKILL.md exists
frontmatter exists
name is lowercase
description exists and is trigger-oriented
description carries progressive disclosure boundaries
existing frontmatter properties are preserved
required sections exist
behavior-critical rules are represented
source verification completed when constraints changed
no obvious raw transcript/log dumps
no bulk Markdown tables for machine-facing records
ConPort-first policy present
token ROI policy present
stable-prefix guidance present
```
