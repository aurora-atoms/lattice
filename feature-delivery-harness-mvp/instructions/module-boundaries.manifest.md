# Module Boundaries

```text
BOUND.001 | MUST  | project | project_display_name=Lattice; project_id=lattice; namespace=lat
BOUND.002 | NEVER | naming  | do not create module or record named lattice
BOUND.003 | MUST  | unit    | feature_delivery_case is primary value unit
BOUND.004 | MUST  | evidence| PR, commit, CI, review, merge, release are evidence_refs only
BOUND.005 | NEVER | yield   | DeliveryYield approves or rejects delivery
```
