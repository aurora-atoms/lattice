## Direction Fit

```yaml
primary_value_path: current_product_delivery | strategic_asset | team_reuse
direction_verdict: proceed | bind_to_delivery | retain_candidate | stop
evidence_refs: <one or more stable source or case references>
existing_capability_gap: <why the smallest existing capability combination is insufficient>

# Complete only the fields required by the selected path.
user_outcome: <required for current_product_delivery>

proprietary_input: <required for strategic_asset>
verifiable_artifact: <required for strategic_asset>
second_use: <required for strategic_asset>
maintenance_owner: <required for strategic_asset>

second_use_evidence: <required for team_reuse>
adoption_owner: <required for team_reuse>
```

Rules:

- Select exactly one `primary_value_path` value and one `direction_verdict` value.
- Replace all placeholders; placeholder text does not satisfy validation.
- `evidence_refs` must identify bounded evidence, not a generic claim that the idea is valuable.
- `existing_capability_gap` must name what was evaluated and why composition or extension is insufficient.
- A `proceed` verdict does not grant delivery, security, architecture, asset-promotion, merge, release, deployment, or production authority.