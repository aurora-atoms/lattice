# Skill Authoring Gate

## Decision

Use a layered authoring gate rather than a new standalone enforcement Skill or a README-only convention.

```text
root AGENTS.md discovery rule
-> Direction Investment Gate for new capability investment
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

## Direction Gate Before New Skills

Before creating a new Skill family, apply `direction-investment-gate.md` and evaluate the smallest existing capability combination first.

A newly created `skills/<name>/SKILL.md` must contain the machine-checkable `## Direction Fit` block from `../templates/direction-fit.template.md`.

The block must:

- select exactly one `primary_value_path`: `current_product_delivery`, `strategic_asset`, or `team_reuse`;
- select one direction verdict: `proceed`, `bind_to_delivery`, `retain_candidate`, or `stop`;
- cite bounded evidence and state the existing capability gap;
- include path-specific evidence;
- contain no unfilled placeholders.

The direction block does not grant permission to create, promote, merge, release, deploy, or operate the capability. It only establishes that implementation effort has a reviewable value path.

Existing Skill packages are not forced to add the block solely because they are modified. Add it when a change materially expands the Skill's purpose, authority, or investment scope.

## Required Authoring Flow

1. For a new Skill family, complete the Direction Investment Gate and select a reviewable verdict before implementation.
2. Identify the target Skill family and current semantic version in `registry/capability-context-policy.json`.
3. Read the compact entry in `registry/skill-context.catalog.json` before loading broad Skill context.
4. State the intended change and classify it as patch, minor, or major.
5. Preserve runtime-native frontmatter. Keep `name` and `description` as the native discovery surface.
6. Ensure `description` clearly covers the task, trigger, input/output type, exclusions, and behavior boundary.
7. For a new Skill, include a valid `## Direction Fit` section.
8. Ensure the selected `SKILL.md` contains non-empty sections named `Outputs`, `Evidence`, `Success Signals`, and `Stop Conditions`.
9. Define visible artifacts and their default writeback location. Inherit `lat.capability.run_result.v1` and use the repository default run-result path unless the Skill has a more specific governed location.
10. Define evidence as facts plus source references, inference basis, citations, uncertainty, unknowns, and assumptions.
11. Define measurable or reviewable success signals with explicit met, not-met, or not-evaluated outcomes.
12. Define stop conditions for goal completion, stage review, missing inputs, missing permissions, unavailable sources or internet, insufficient evidence, failed validation, retry exhaustion, human authority, and high-risk boundaries as applicable.
13. Update the Skill catalog entry when intended change, users, trigger, minimum inputs, outputs, or runtime targets change.
14. Bump the Skill version in `registry/capability-context-policy.json` for every changed Skill package. Do not reuse a prior version for changed package content.
15. Add or update trigger, output, validation, and failure regression cases when observable behavior changes.
16. Run package, context, change-gate, schema, and relevant domain validations.
17. Emit a structured visible run result with evidence, success signals, stop reason, and writeback status.

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
- valid paths and shared capability context contracts;
- a valid Direction Fit block for newly created Skill packages.

CI runs this check on pull requests with full Git history. A failure is a hard stop until the package, direction decision, or version contract is corrected.

## Authority and Stop Rules

The authoring agent must stop and request review when:

- required repository or source access is unavailable;
- the current version or compatibility impact cannot be determined;
- behavior-critical source rules are missing or contradictory;
- a new Skill lacks a defensible direction, beneficiary, verification method, existing-capability gap, or path-specific evidence;
- the requested change would weaken safety, privacy, evidence, or authority boundaries;
- a major version or deprecation decision needs an accountable owner;
- validation remains failed after one bounded corrective retry.

Do not create a new governance Skill to bypass this gate. Extend `lattice-governor` only when the owned governance boundary itself changes.