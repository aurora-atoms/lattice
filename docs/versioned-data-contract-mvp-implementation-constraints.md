# Versioned Data Contract MVP — Implementation Constraints

This companion note closes practical gaps that can otherwise turn the MVP into duplicated schema governance or an overbuilt registry.

It is part of the architecture review for `versioned-data-contract-mvp.md`; it does not add runtime implementation.

## 1. Keep one authority per concern

The MVP deliberately uses more than one artifact, so the authority split must be explicit.

| Concern | Authority in the MVP | Not authoritative for this concern |
|---|---|---|
| JSON payload structure and validation keywords | released JSON Schema artifact | ODCS prose, binding file, Silver table shape |
| contract identity, lifecycle, owner-facing semantics, stable source field identity | ODCS contract release | JSON property name alone, physical table version |
| source-to-canonical interpretation | consumer Canonical Binding release | producer contract, ad hoc Gold logic |
| actual transformation behavior | downstream implementation release | binding prose alone |
| raw historical evidence | Bronze/source archive plus provenance | Elasticsearch index, DataHub projection |
| business metric meaning | governed downstream/Gold semantic authority | source schema or physical field name |

If two artifacts disagree on the concern they are supposed to coordinate, the release is `blocked`; do not choose whichever value is more convenient at runtime.

## 2. Avoid dual-authored structural schemas

ODCS has a schema section and JSON Schema also describes structure. Maintaining two complete independently-authored structural definitions creates drift risk.

For JSON producers in this MVP:

- JSON Schema is the detailed physical validation authority;
- the ODCS schema section carries the stable element IDs and only the semantic/physical information needed for cross-team coordination;
- do not copy every JSON Schema constraint into ODCS;
- the contract release links to the exact JSON Schema artifact;
- a reviewer verifies that every ODCS field used by a binding resolves to the intended JSON Schema field/path for that release.

A later validator may automate this cross-check if a second real use demonstrates value. Do not build a generator or synchronization service in Phase 0.

## 3. Bootstrap existing active versions without changing firmware

The contract layer must work for systems that already have old and new devices in production.

Use a one-time baseline process:

1. inventory only the currently active source schema generations required by the pilot;
2. snapshot each active payload schema into an immutable release artifact;
3. assign stable contract and field IDs with producer/domain-owner review;
4. document whether similarly named/located fields are actually semantically equivalent;
5. create the first consumer binding across those active releases;
6. associate historical/future Bronze batches with the baseline contract release through ingestion metadata or a batch manifest.

Do not require device firmware to emit the new contract metadata if source generation can be resolved reliably from existing device type, firmware version, topic, file path, or ingestion routing metadata.

Do not retroactively assign field identity without producer/domain review when semantics are uncertain. Mark the mapping `unknown` or `blocked` instead.

## 4. Activation is not the same as publication

A producer may publish a contract before every consumer supports it.

Use separate states:

```text
producer contract: proposed -> active -> deprecated -> retired
consumer binding:  proposed -> active -> deprecated -> retired
```

For one producer/consumer relationship, rollout is allowed only when:

```text
source release exists
AND payload schema is immutable/recoverable
AND required semantic changes are reviewed
AND the consumer binding declares support
AND the downstream implementation declares the binding release it implements
AND unsupported-version behavior is fail-closed
```

This avoids making producer publication depend on editing downstream repositories while still preventing an unsupported source version from being silently canonicalized.

## 5. Minimal logical persistence if files are not enough

Do not start with a new registry database. If an existing system needs queryable metadata, three logical record types are sufficient.

### `contract_release`

```text
contract_id
contract_version
status
schema_artifact_ref
schema_bundle_digest?        # only when bundling/pinning requires it
published_at
producer_owner_ref
```

### `binding_release`

```text
binding_id
binding_version
source_contract_id
supported_source_versions
target_model_id
target_model_version
status
implementation_ref?
```

### `runtime_provenance`

```text
source_record_or_batch_id
source_contract_id
source_contract_version
schema_artifact_ref
binding_id
binding_version
transform_release
ingested_at
```

These may be files, Delta tables, registry metadata, or catalog entities. The architecture defines the information, not the storage product.

Do not create a fourth value-level lineage table unless a real debugging/regulatory case proves that schema-level binding plus event/batch provenance is insufficient.

## 6. Consumer support matrix is a projection, not another contract

For operational visibility, a team may project:

```text
source contract version x consumer binding -> supported / unsupported / deprecating
```

This can live in DataHub, a catalog, a generated report, or an ES index. It should be derived from released contracts/bindings where possible instead of becoming another manually maintained authority.

## 7. Explicit failure states

A runtime or review path should distinguish at least:

- `unknown_contract`: source contract/version cannot be resolved;
- `schema_invalid`: payload does not satisfy the resolved structural schema;
- `unsupported_version`: no active binding supports the resolved source release;
- `mapping_blocked`: a required canonical field has no non-ambiguous mapping;
- `semantic_conflict`: producer/consumer meaning is unresolved;
- `transform_mismatch`: implementation cannot prove which binding release it implements.

For Bronze ingestion, preserve raw evidence whenever permitted. For Silver canonicalization, fail closed or quarantine rather than selecting the nearest-looking schema/mapping.

## 8. MVP verification sequence

The first downstream pilot should be reviewed in this order:

1. **Identity test** — v1 `result_code` and v2 `conversion_status` are confirmed by the producer/domain owner to represent the same stable field identity.
2. **Structure test** — each version validates against its own immutable JSON Schema release.
3. **Concurrent-routing test** — records from both source generations are present in the same operating window and resolve to the correct source release.
4. **Binding-completeness test** — both releases produce every canonical field required by the pilot without guessing.
5. **Negative semantic test** — mutate a fixture so the same-looking field has different units/meaning; the binding must not silently accept it as equivalent.
6. **Unknown-version test** — an unrecognized version preserves raw evidence and does not enter canonical Silver as if it were a supported release.
7. **Replay test** — select one historical batch/event and recover raw payload, source contract, schema artifact, binding release, and transform release.
8. **Legacy-path test** — if the existing transformer is hard-coded, verify that it can declare the same binding release without framework rewrite.

A successful architecture review is not production proof. Real adoption, operational burden, and replay evidence belong in the private downstream pilot.

## 9. Stop conditions

Stop before adding more infrastructure when any of these remain true after one bounded pilot:

- producer/domain ownership of field meaning is unavailable;
- active source versions cannot be reliably identified;
- source-to-canonical mapping still depends on guessing;
- the binding duplicates a large ETL language rather than expressing a small interface boundary;
- a new registry/graph/service is required only to make the design appear complete rather than to solve an observed operational gap;
- the contract process adds more cross-team coordination cost than the version/debugging problem it replaces.

If the pilot succeeds, the next investment should be the smallest automation for the observed repeated burden, not a preplanned contract platform.
