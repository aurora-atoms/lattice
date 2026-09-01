# Versioned Data Contract MVP — Synthetic Example

This folder is a design fixture for `docs/versioned-data-contract-mvp.md`. It is not a runtime implementation, registered Lattice capability, production schema, or claim of downstream adoption.

The example models two device generations that emit concurrently:

```text
contract 1.0.0 -> JSON field `result_code`
contract 2.0.0 -> JSON field `conversion_status`
```

The producer asserts that both physical fields have the same meaning, so the ODCS contract keeps the stable schema-property ID `conversion-status` across the rename. The consumer-owned `canonical-binding.yaml` maps that stable source identity to one canonical field.

Files:

- `source-contract-v1.odcs.yaml` — producer contract 1.0.0;
- `source-contract-v2.odcs.yaml` — producer contract 2.0.0;
- `payload-v1.schema.json` — immutable JSON Schema example for v1;
- `payload-v2.schema.json` — immutable JSON Schema example for v2;
- `canonical-binding.yaml` — intentionally small consumer mapping example; it is **not** proposed as a universal transformation DSL.

What this example proves only at the design level:

- a physical rename does not have to create two canonical Silver columns;
- old and new source versions can be active simultaneously;
- stable semantic identity can be separated from physical field name;
- producer and consumer artifacts can be reviewed/versioned independently.

What it does not prove:

- real runtime compatibility;
- ODCS/tool-specific validation behavior;
- a real Schema Registry integration;
- replay under a specific parser/validator implementation;
- real producer/consumer agreement or production adoption.
