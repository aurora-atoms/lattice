# Governance Model

## Purpose

Use this model to manage public, reusable skill packages as versioned capability assets rather than one-off prompts.

## Lifecycle

```text
idea -> draft -> candidate -> experimental -> active -> deprecated -> archived
                         \-> quarantine
```

## Status Rules

GOVPUB.001 | MUST  | lifecycle | generated or imported skills start as candidate or quarantine, not active
GOVPUB.002 | MUST  | active    | active skills pass validator, trigger eval, output eval, boundary review
GOVPUB.003 | SHOULD | draft    | draft skills keep examples + open questions in references, not SKILL.md
GOVPUB.004 | MUST  | archive   | archived skills preserve registry history + last known reason
GOVPUB.005 | NEVER | public    | publish private downstream context in Lattice
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
