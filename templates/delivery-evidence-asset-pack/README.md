# Manager-Ready Delivery Asset Pack Template

This is a public-safe file layout template. Copy it to a private repository, replace synthetic placeholders with locally governed records, and keep the resulting pack private.

```text
asset-pack.manifest.json
feature-delivery-case.json
evidence-ledger.jsonl
contribution-ledger.jsonl
reusable-assets/<asset-id>/
reusable-asset-dossier.md
manager-brief.json
manager-brief.md
validation-report.json
```

The structured `manager-brief.json` is the validation boundary. Generate `manager-brief.md` with the canonical renderer in `scripts/validate_manager_claims.py`; validation rejects any byte-level divergence so Markdown cannot add claims or omit limitations, unknowns, evidence origin, or review status.
