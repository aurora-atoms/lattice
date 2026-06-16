# Governance Model

## Purpose

Use this model to manage public, reusable skill packages as versioned capability assets rather than one-off prompts.

## Lifecycle

```text
idea -> draft -> candidate -> experimental -> active -> deprecated -> archived
                         \-> quarantine
```

## Status Rules

GOVPUB.001 | MUST  | lifecycle | generated_or_imported_skills_start_as_candidate_or_quarantine_not_active | enforce
GOVPUB.002 | MUST  | active    | active_skills_pass_validator_trigger_eval_output_eval_and_boundary_review | enforce
GOVPUB.003 | SHOULD | draft    | draft_skills_keep_examples_and_open_questions_in_references_not_SKILL_md | prefer
GOVPUB.004 | MUST  | archive   | archived_skills_preserve_registry_history_and_last_known_reason | enforce
GOVPUB.005 | NEVER | public    | publish_private_downstream_context_in_lattice | block

## Registry Record

Each reusable skill SHOULD have a JSONL registry record with:

```text
skill_id,path,status,owner,domain,runtime_targets,risk_tier,auto_invocation,side_effects,uses_scripts,uses_network,contains_private_context,public_export_allowed,depends_on,last_validated_at,trigger_eval,output_eval,release_channel,notes
```

The canonical schema is `schemas/skill_registry_record.schema.json`.

## Dependency Direction

```text
public lattice standards -> private downstream governance -> private domain skills
```

Never reverse this direction. Public Lattice artifacts must not depend on private repositories or private skill behavior.

## Release Channels

```text
stable       active and validated for routine use
experimental usable but still collecting eval evidence
candidate    generated or imported, not installed by default
quarantine   untrusted, unsafe, unclear, or privacy-risk artifact
archived     preserved for history only
```

## Promotion Gate

Promote a skill only when:

```text
- SKILL.md validates
- description has positive and negative trigger boundaries
- hard rules are surfaced in SKILL.md
- long context is moved to references
- deterministic work is scripted when useful
- trigger eval includes realistic positive and negative cases
- output eval preserves behavior-critical requirements
- boundary review passes
- registry record is updated
```

## Review Recommendation Format

```text
recommendation: promote | revise | quarantine | deprecate | reject
reason: one sentence
required_changes:
  - change
risk_flags:
  - flag
validation:
  validator: pass|fail|not_run
  trigger_eval: pass|fail|not_run
  output_eval: pass|fail|not_run
```
