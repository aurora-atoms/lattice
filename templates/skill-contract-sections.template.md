<!-- For a newly created Skill package, copy and complete the Direction Fit block below. Existing Skills do not need it solely because they are edited. -->

## Direction Fit

```yaml
primary_value_path: current_product_delivery | strategic_asset | team_reuse
direction_verdict: proceed
evidence_refs: <one or more stable source or case references>
existing_capability_gap: <why the smallest existing capability combination is insufficient>

user_outcome: <required for current_product_delivery>

proprietary_input: <required for strategic_asset>
verifiable_artifact: <required for strategic_asset>
second_use: <required for strategic_asset>
maintenance_owner: <required for strategic_asset>

second_use_evidence: <required for team_reuse>
adoption_owner: <required for team_reuse>
```

See `direction-fit.template.md` and `../docs/direction-investment-gate.md`. Remove unused path-specific fields and replace every placeholder.

## Outputs

- Structured result: `lat.capability.run_result.v1`.
- Visible artifact(s): `<artifact kind and format>`.
- Default writeback: `<governed path>`.
- Without write permission: return the complete structured result inline and mark `write_status=returned_inline`.

## Evidence

- Facts: cite authoritative bounded source references.
- Inference: state the conclusion, supporting facts, and uncertainty.
- Citations: preserve stable references for all material claims.
- Uncertainty: list confidence limits and conflicting evidence.
- Unknowns: list material facts that could not be established.
- Assumptions: label each assumption and its effect if false.
- Insufficient evidence: stop when the missing evidence prevents a supportable result.

## Success Signals

- `<signal 1>` -> `met | not_met | not_evaluated` with evidence refs.
- `<signal 2>` -> `met | not_met | not_evaluated` with evidence refs.
- Do not infer success only from file creation or task activity.

## Stop Conditions

Stop and emit a structured result when:

- the requested goal is reached;
- the next reviewable stage gate is reached and end-to-end continuation was not explicitly authorized;
- a required input or permission is missing;
- a required repository, source, tool, or internet connection is unavailable;
- evidence is insufficient for further analysis or recommendation;
- validation remains failed after the bounded retry;
- a security, privacy, compliance, data-governance, architecture, production, or other high-risk boundary is reached;
- human authority is required;
- the retry budget is exhausted.

For a permission stop, identify the exact permission, accountable owner, reason, and resumable next step. Do not probe repeatedly or attempt a bypass.