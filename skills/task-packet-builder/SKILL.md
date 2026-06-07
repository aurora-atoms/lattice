---
name: task-packet-builder
description: "Convert an approved feature spec or feature_delivery_case JSONL input into a bounded task.packet JSONL handoff while preserving acceptance criteria, forbidden changes, validation requirements, evidence requirements, safety constraints, and quality-adjusted token ROI. Use for creating coding-agent task packets from approved synthetic/open feature cases. Do not use for broad rewrites, raw repo dumps, speculative design, unsafe commands, company-derived examples, or delivery approval. Output task_packet.md and lat.task.packet.v1 records; query ConPort before loading or searching full skill text when inventory exists."
---

# Task Packet Builder

## Goal

Convert approved feature specs into bounded AI coding task packets.

## Use When

```text
approved_feature_spec -> task_packet
feature_delivery_case JSONL -> coding_agent_handoff
acceptance_criteria -> validation_commands_and_evidence_requirements
```

## Do Not Use When

```text
raw_repo_dump_or_full_diff_context
whole_repo_or_all_files_scope
unsafe_destructive_network_production_secret_deploy_commands
speculative_broad_rewrite
delivery_verdict_or_token_economics_report
```

## Inputs

```text
feature spec
feature_delivery_case JSONL
acceptance criteria
repo/module hints
constraints
validation expectations
```

## Outputs

```text
task_packet.md
lat.task.packet.v1 JSONL
validation command list
evidence requirements
risk controls
```

## Workflow

1. Query ConPort before loading or searching full skill text when inventory exists.
2. Map each acceptance criterion to validation commands and evidence requirements.
3. State allowed changes, forbidden changes, target files or target areas, risk controls, and rollback notes.
4. Reject unbounded scope and unsafe validation commands unless explicitly reviewed.
5. Emit a `task.packet` record matching `../../feature-delivery-harness-mvp/schemas/records/task.packet.v1.schema.json`.

## Rules

```text
TPB.001 | MUST  | scope  | task_packet_has_bounded_target_files_or_areas | enforce
TPB.002 | MUST  | safety | include_forbidden_changes_and_risk_controls | enforce
TPB.003 | MUST  | verify | include_automated_and_user_usability_validation_when_code_changes | enforce
TPB.004 | MUST  | evidence | include_evidence_requirements | enforce
TPB.005 | NEVER | input  | include_raw_repo_jira_log_trace_pr_or_ci_dump | block
TPB.006 | MUST  | tokens | optimize_quality_adjusted_token_ROI_not_blind_minimization | enforce
TPB.007 | MUST  | prompt | keep stable prefix and put variable spec context in suffix | enforce
```

## Verification

```text
python ../../feature-delivery-harness-mvp/scripts/validate_jsonl.py <task-packet.jsonl>
python ../../feature-delivery-harness-mvp/scripts/validate_task_packet.py <task-packet.jsonl>
```

## Failure Modes

```text
missing_forbidden_changes
missing_validation_commands
missing_evidence_requirements
unbounded_scope
scope_too_large
unsafe_command
raw_context_forbidden
```

## References

- `references/task-packet-patterns.md`
- `../../feature-delivery-harness-mvp/references/validator-failure-codes.md`
- `../../feature-delivery-harness-mvp/schemas/records/task.packet.v1.schema.json`
