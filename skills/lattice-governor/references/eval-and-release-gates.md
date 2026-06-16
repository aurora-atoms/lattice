# Eval And Release Gates

## Trigger Eval

A reusable skill must prove that it triggers for intended tasks and does not trigger for adjacent tasks outside its scope.

Trigger cases should include:

```text
positive/direct
positive/implicit
positive/typo_or_alias
negative/adjacent_domain
negative/private_context
negative/unsafe_or_out_of_scope
```

## Output Eval

Output eval checks whether skill invocation improves the result while preserving behavior-critical rules.

Minimum comparison:

```text
same prompt with current skill -> output
same prompt without skill or with previous version -> baseline
judge against assertions -> pass/fail/revise
```

## Required Assertions

Assertions should be specific and observable:

```text
- preserves required terminology
- includes required sections
- rejects prohibited scope
- uses correct repo boundary
- includes validation commands
- avoids private data leakage
- avoids overbuilding
```

## Release Gate Matrix

```text
candidate -> experimental:
  validator: pass
  boundary_review: pass
  trigger_eval: present
  output_eval: present

experimental -> active:
  validator: pass
  trigger_eval: pass
  output_eval: pass
  registry_record: updated
  release_notes: present

active -> deprecated:
  replacement_or_reason: present
  registry_record: updated
  downstream_dependency_review: complete
```

## Risk Flags

```text
missing_registry_record
missing_trigger_eval
missing_output_eval
oversized_SKILL_md
hidden_reference_rule
private_context_in_public_repo
frontmatter_schema_drift
unvalidated_script
unsafe_side_effect
runtime_target_ambiguous
```

## Report Template

```text
skill_id:
path:
status:
recommendation:
validator:
trigger_eval:
output_eval:
boundary_review:
risk_flags:
required_changes:
release_channel:
```
