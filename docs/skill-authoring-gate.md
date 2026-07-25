# Skill Authoring Gate

## Decision

Use a layered authoring gate rather than a new standalone enforcement Skill or a README-only convention.

```text
root AGENTS.md discovery rule
-> lattice-governor governance Skill
-> skill-token-refactor when rewriting an existing package
-> capability context catalogs and version policy
-> deterministic change validator and CI gate
```

A standalone enforcement Skill would duplicate `lattice-governor` and could be missed before native Skill discovery. A README is informative but not enforceable. The layered gate is both discoverable and machine-enforced.

## Mandatory Trigger

Any task that creates, copies, renames, restructures, or modifies a file under `skills/<name>/` must invoke or follow `lattice-governor` before finalizing the change.

Use `skill-token-refactor` in addition when the task compresses, restructures, splits, migrates, or behavior-preservingly rewrites an existing Skill.

The authoring agent must read this file and `capability-context-contract.md` before changing the behavior contract.

## Required Authoring Flow

1. Identify the target Skill family and current semantic version in `registry/capability-context-policy.json`.
2. Read the compact entry in `registry/skill-context.catalog.json` before loading broad Skill context.
3. State the intended change and classify it as patch, minor, or major.
4. Preserve runtime-native frontmatter. Keep `name` and `description` as the native discovery surface.
5. Ensure `description` clearly covers the task, trigger, input/output type, exclusions, and behavior boundary.
6. Ensure the selected `SKILL.md` contains non-empty sections named `Outputs`, `Evidence`, `Success Signals`, and `Stop Conditions`.
7. Define visible artifacts and their default writeback location. Inherit `lat.capability.run_result.v1` and use the repository default run-result path unless the Skill has a more specific governed location.
8. Define evidence as facts plus source references, inference basis, citations, uncertainty, unknowns, and assumptions.
9. Define measurable or reviewable success signals with explicit met, not-met, or not-evaluated outcomes.
10. Define stop conditions for goal completion, stage review, missing inputs, missing permissions, unavailable sources or internet, insufficient evidence, failed validation, retry exhaustion, human authority, and high-risk boundaries as applicable.
11. Update the Skill catalog entry when intended change, users, trigger, minimum inputs, outputs, or runtime targets change.
12. Bump the Skill version in `registry/capability-context-policy.json` for every changed Skill package. Do not reuse a prior version for changed package content.
13. Add or update trigger, output, validation, and failure regression cases when observable behavior changes.
14. Run package, context, change-gate, schema, and relevant domain validations.
15. Emit a structured visible run result with evidence, success signals, stop reason, and writeback status.

## Version Decision

```text
patch = wording, examples, references, validation fixes, or discovery clarity without behavior-contract change
minor = backward-compatible trigger, optional context, output, tool, workflow, evidence, success, or stop capability
major = incompatible required input, permission, output removal, trigger narrowing, authority change, or behavior semantic change
```

Every modification under a Skill package requires a monotonically higher version. The version level remains a reviewable semantic decision; the deterministic gate verifies that a bump occurred.

## Required SKILL.md Sections

Use `../templates/skill-contract-sections.template.md` as a compact starting point. The sections may be brief, but they must be capability-specific and cannot merely say “follow the global contract.”

### Outputs

State:

- visible artifact or structured result;
- format;
- default writeback location;
- inline fallback when write permission is unavailable.

### Evidence

State:

- authoritative facts and source references;
- inference basis;
- citations;
- uncertainty, unknowns, and assumptions;
- conditions that make evidence insufficient.

### Success Signals

State the observable conditions that mean the Skill succeeded, partially succeeded, failed, or could not be evaluated.

### Stop Conditions

State when to stop rather than retry, including missing permission, missing required input, unavailable required source, insufficient evidence, high-risk boundary, failed bounded retry, stage gate, or goal completion.

## Deterministic Gate

Run:

```bash
python scripts/validate_skill_change_contract.py --base-ref <base-sha> --head-ref <head-sha>
```

The gate checks changed Skill packages for:

- catalog registration;
- a monotonically increased semantic version;
- required contract sections;
- valid paths and shared capability context contracts.

CI runs this check on pull requests with full Git history. A failure is a hard stop until the package or version contract is corrected.

## Authority and Stop Rules

The authoring agent must stop and request review when:

- required repository or source access is unavailable;
- the current version or compatibility impact cannot be determined;
- behavior-critical source rules are missing or contradictory;
- the requested change would weaken safety, privacy, evidence, or authority boundaries;
- a major version or deprecation decision needs an accountable owner;
- validation remains failed after one bounded corrective retry.

Do not create a new governance Skill to bypass this gate. Extend `lattice-governor` only when the owned governance boundary itself changes.
