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

FRONT.001 | MUST  | skill | preserve existing frontmatter schema
FRONT.008 | MUST  | skill | put use + do-not-use guidance inside description
CONPORT.001 | MUST | retrieval | query ConPort MCP before loading or searching full skill text
READ.001 | MUST  | skill | prioritize machine readability over human readability in control planes
TOK.001 | MUST  | quality | preserve quality + behavior before token reduction
TOK.002 | MUST  | metric | define token efficiency as quality-adjusted output per token cost
CACHE.001 | MUST | prompt | keep system prompt prefix stable across batch skill rewrite runs
DATA.001 | MUST  | validation | preserve required column rejection behavior
DATA.002 | NEVER | cleanup | delete rows unless source rules explicitly allow it

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
