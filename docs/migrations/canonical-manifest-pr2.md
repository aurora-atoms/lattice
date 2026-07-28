# Canonical Capability Manifest and Lifecycle Separation — PR 2

## Decision

`registry/capability-manifest.json` is the canonical source for public capability identity, semantic version, role, public package status, path, discovery, outputs, evidence, success, stop, authority, compatibility, and projection metadata.

Generated compatibility projections:

```text
registry/capability-context-policy.json
registry/skill-context.catalog.json
registry/agent-context.catalog.json
registry/skill-context.extensions/*.json
registry/skills.index.jsonl
registry/agents.index.jsonl
registry/mcp_servers.index.jsonl
registry/knowledge_packs.index.jsonl
registry/workspace_templates.index.jsonl
registry/capabilities.index.jsonl
```

Do not hand-edit generated capability records. Edit the canonical manifest and regenerate:

```bash
python scripts/generate_capability_registry_projections.py --root .
python scripts/generate_capability_registry_projections.py --root . --check
python scripts/validate_capability_manifest.py --root .
```

## Migration Result

```text
canonical records = 78
Skills = 62
Agents = 13
MCP contracts = 1
knowledge packs = 1
workspace profiles = 1

public_package_status
  contract_validated = 75 Skill/Agent packages
  draft = 3 MCP/knowledge/workspace contracts
```

Skill and Agent packages moved through the one-time migration baseline `legacy experimental -> draft -> contract_validated` only after package, context, Agent-record, path, and parity validation. None is marked `conformance_validated` or `released`.

## Compatibility

Legacy fields are retained:

```text
status
release_channel
owner
domain or role
risk metadata
runtime targets
install scopes
eval metadata
dependency metadata
```

New projection fields:

```text
version
capability_role
public_package_status
description
trigger
```

Downstream consumers must use `public_package_status` for dependency readiness. Legacy `status=experimental` remains a compatibility field and does not express adoption.

## Role Assignment

The migration uses explicit role overrides for governance contracts, selectors, validators, profiles, and projections; unoverridden bounded packages are `atomic_capability`. These assignments are presented for accountable human review and are not evidence of downstream use.

Notable assignments:

```text
lattice-governor -> governance_contract
delivery-capability-conductor and family selectors -> selector
feature-understanding-loop -> selector compatibility entry
knowledge-profile-evaluator -> validator
capability-harness-engineer -> validator
manager and release renderers -> projection
pr-review-template -> capability_profile
remaining bounded Skills and Agents -> atomic_capability
```

No package was moved, renamed, deprecated, released, or made team-available.

## Lifecycle Separation

Public package status:

```text
draft -> contract_validated -> conformance_validated -> released -> deprecated
```

Private downstream adoption:

```text
not_observed -> imported -> task_scoped -> used_once -> reused -> team_available -> deprecated
```

Public fixtures now declare:

```text
simulation_status = synthetic_reference
downstream_adoption_status = not_observed
```

The reusable-asset fixture remains `never_by_default`, public package `draft`, legacy maturity `runnable`, and adoption `not_observed`. Its synthetic review and usage record simulate shape only.

## Validation and Negative Gates

PR 2 adds deterministic rejection for:

- identity or version mismatch;
- missing role or public package status;
- missing package path;
- native description drift or description/trigger conflict;
- projection drift;
- deprecated capability in an active route or profile;
- downstream adoption state in the public canonical manifest;
- synthetic `used_once`, `reused`, or `team_available`;
- skipped adoption transitions;
- use/reuse without addressable private evidence;
- `team_available` without separate governance approval;
- private paths, secrets, or private keys in public fixtures;
- DeliveryYield used as asset-promotion authority.

## Remaining Compatibility Work

PR 3 owns downstream consumer, private-extension, evidence-pack, manager-claim schemas, templates, and validators. PR 4 owns heterogeneous eval dispatch, full synthetic private-consumer generation, golden asset-pack comparison, and the complete conformance runner.
