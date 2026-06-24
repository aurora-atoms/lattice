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
TPB.001 | MUST  | scope  | task.packet has bounded target files or areas
TPB.002 | MUST  | safety | include forbidden changes + risk controls
TPB.003 | MUST  | verify | include automated + user usability validation when code changes
TPB.004 | MUST  | evidence | include evidence requirements
TPB.005 | NEVER | input  | include raw repo/Jira/log/trace/PR/CI dump
TPB.006 | MUST  | tokens | optimize quality-adjusted token ROI, not blind minimization
TPB.007 | MUST  | prompt | keep stable prefix and put variable spec context in suffix
```

## Verification

```text
python3.14 ../../feature-delivery-harness-mvp/scripts/validate_jsonl.py <task-packet.jsonl>
python3.14 ../../feature-delivery-harness-mvp/scripts/validate_task_packet.py <task-packet.jsonl>
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
