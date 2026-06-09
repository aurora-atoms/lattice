# Module Boundaries

```text
BOUND.001 | MUST  | project | project_display_name=Lattice; project_id=lattice; namespace=lat | enforce
BOUND.002 | NEVER | naming  | do_not_create_module_or_record_named_lattice | block
BOUND.003 | MUST  | unit    | feature_delivery_case_is_primary_value_unit | enforce
BOUND.004 | MUST  | evidence| pr_commit_ci_review_merge_release_are_evidence_refs_only | enforce
BOUND.005 | NEVER | yield   | deliveryyield_approves_or_rejects_delivery | block
```
