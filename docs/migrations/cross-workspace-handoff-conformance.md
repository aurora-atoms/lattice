# Cross-Workspace Handoff Conformance Compatibility Note

## Decision

Add a workspace-neutral conformance layer over the existing Domain Context Pack and Portable Case Pack contracts. The layer produces a deterministic `lat.workspace_handoff_verification_request.v1` receipt for a receiving coding workspace.

## Compatibility

This change is additive. It does not modify or version-bump:

- `lat.domain_context_pack.v1`;
- `lat.portable_case_pack.v1`;
- any Skill, Agent, Capability Profile, active module, or registry record;
- any receiver-specific Skill discovery or runtime configuration.

The new receipt schema is justified by a stable machine I/O boundary for deterministic conformance. The synthetic fixture wrapper is test-harness input only and is not a new case lifecycle or source-synthesis record.

## Google Adapter Patch

The Google Workspace adapter source advances from `1.1.0` to `1.1.1`.

This is a patch clarification of the existing `candidate` authority ceiling and `downstream_verification_required=true` behavior. Generated guidance now states more precisely that Feature and Bug outputs require independent receiving-workspace repository/runtime verification and cannot declare work readiness, root cause, or fix readiness. It also states that the receiving workspace owns capability discovery.

The adapter's schema, required handoff sections, authority, permissions, task families, and runtime targets do not change. All generated projections are regenerated from the canonical adapter source and remain hash-bound.

## Migration

Existing downstream consumers may continue using the v1 Domain Context Pack, Portable Case Pack, and Google adapter manifest. To adopt cross-workspace conformance, generate or validate the new verification request before a coding workspace acts on Google-side candidate evidence.

No `.agents/skills`, `.github/skills`, Claude-, Codex-, Copilot-, or Gemini-specific discovery projection is required or generated.

## Evidence Boundary

The public Feature and Bug fixtures remain:

```text
simulation_status = synthetic_reference
downstream_adoption_status = not_observed
```

Passing conformance proves deterministic contract behavior only. It does not prove downstream adoption, owner acceptance, attention savings, delivery value, work readiness, root-cause verification, or production readiness.
