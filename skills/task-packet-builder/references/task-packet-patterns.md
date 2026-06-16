# Task Packet Patterns

```text
required_fields:
  objective
  allowed_changes
  forbidden_changes
  target_files_or_target_areas
  acceptance_ids
  validation_commands
  evidence_requirements
  risk_controls
  rollback_notes

validation_command:
  id
  purpose
  cwd
  command_or_manual_steps
  timeout
  expected_outcome
  target_acceptance_ids
```
