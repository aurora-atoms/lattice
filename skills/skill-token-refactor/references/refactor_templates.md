# Refactor Templates

## Single Skill Report

```markdown
# Skill Refactor Report

## Verdict
auto_safe | review_needed | blocked

## Source Inventory
- current name:
- current description:
- frontmatter keys:
- frontmatter schema preserved:
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

## Frontmatter Preservation
- preserved properties:
- optimized values:
- review_needed changes:

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

## Batch Report

```markdown
# Skill Refactor Batch Report

## Summary
- total skills:
- auto_safe:
- review_needed:
- blocked:

## Largest Skills
- path | estimated_tokens | risk_flags

## Risk Flags
- flag | count | examples

## Review Queue
- path | reason

## Duplicate Candidates
- path_a | path_b | reason

## Script Candidates
- path | candidate | reason
```
