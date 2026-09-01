# Versioned Data Contract MVP

## Status

Architecture and delivery plan only. This document does not implement a runtime service, ETL pipeline, Schema Registry, DataHub extension, Silver table, or Gold model.

The design is intentionally bounded around one recurring problem:

> Multiple producer schema generations remain active at the same time, while downstream systems need one stable canonical representation without forcing every consumer to understand every historical source schema.

The public Lattice repository contains only the portable architecture and synthetic examples. Real schemas, device payloads, mappings, endpoints, owners, and adoption evidence remain in private downstream repositories.

## Decision

Use a **Git-first, versioned contract layer** with three small artifacts:

1. a producer-owned **Data Contract release** using ODCS 3.1.0 as the portable envelope;
2. an immutable or immutably-addressed **payload schema artifact** (JSON Schema 2020-12 for JSON payloads);
3. a consumer-owned **Canonical Binding release** that maps stable source field identities to the downstream canonical model.

Do **not** build a new contract registry service for the MVP. Git is the authoring and review authority. Existing Schema Registry, DataHub, catalog, or lakehouse metadata surfaces may project or index the released metadata later, but they are not prerequisites for proving the design.

Keep these versions separate:

```text
contract standard version   e.g. ODCS v3.1.0
source contract version     e.g. 2.1.0
payload schema identity     e.g. immutable schema URI / registry ID / bundle digest
physical table version      e.g. Delta/Iceberg table history
```

Semantic compatibility is a decision about producer meaning and consumer expectations. It is not inferred solely from SemVer or a schema-registry compatibility result.

## Why this is the MVP

The smallest useful capability is not a new platform. It is a portable agreement that lets one producer and one downstream model answer five questions deterministically:

1. Which source contract produced this data?
2. Which immutable payload schema explains its physical shape?
3. Which stable source field identity does each renamed or relocated field represent?
4. Which canonical binding converted that source identity into the downstream model?
5. Which source and binding releases must be recovered to replay or investigate the transformation?

If these questions can be answered for two simultaneously active schema generations, the core problem is solved. Everything else can remain optional until real downstream evidence justifies it.

## Standards and feasibility basis

This design reuses existing standards and lakehouse behavior rather than inventing a second schema language.

- **ODCS 3.1.0** separates `apiVersion` (the standard version) from `version` (the data-contract version) and supports stable IDs on schema elements, which is useful across rename/refactor.
- **JSON Schema 2020-12** remains the structural contract for JSON payloads. Root schemas and referenced resources need immutable identities or a release-time bundle; hashing only a mutable root file is not enough for historical interpretation.
- **Schema Registry compatibility** is useful structural evidence, but JSON Schema compatibility depends on policy and content model. It is one gate, not the complete contract decision.
- **Medallion architecture** preserves raw fidelity in Bronze and performs validation/normalization in Silver, which fits concurrent source versions converging into one canonical model.
- **Iceberg/Delta schema and table history** remain physical storage concerns and do not replace producer contract versioning.

Reference basis:

- https://bitol-io.github.io/open-data-contract-standard/v3.1.0/
- https://bitol-io.github.io/open-data-contract-standard/v3.1.0/fundamentals/
- https://json-schema.org/draft/2020-12
- https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html
- https://docs.databricks.com/aws/en/lakehouse/medallion
- https://iceberg.apache.org/spec/

## Architecture

```text
                    PRODUCER BOUNDARY

       Data Contract release + payload schema
       identity / version / stable field IDs / semantics
                         |
                         v
                Contract artifacts in Git
                         |
        +----------------+----------------+
        |                                 |
        v                                 v
 optional Schema Registry             DataHub/catalog
 runtime schema identity              discovery/index only
        |                                 |
        +----------------+----------------+
                         |
                         v
                     BRONZE
              raw source fidelity
              + contract/schema ref
                         |
                         v
               Canonical Binding
          source identities -> canonical
              consumer-owned release
                         |
                         v
                     SILVER
             stable canonical model
             + replay/lineage metadata
                         |
                         v
                      GOLD
        business metrics / aggregates / UI
        no normal source-version branching
```

The contract layer is architecture-independent. A legacy ETL job may hard-code the mapping in code; a modern pipeline may interpret a declarative binding. Both are valid if they declare the same released contract/binding identity and satisfy the same conformance checks.

## Artifact 1: Producer Data Contract release

### Producer responsibility

Producer owns:

- contract identity and lifecycle;
- physical payload schema;
- stable source field identity;
- field meaning, units, nullability, code-set meaning, temporal meaning, and deprecation intent;
- source-side compatibility declaration;
- support window for active source versions.

The producer does **not** own every downstream canonical model or transformation implementation.

### Minimum contract shape

Use ODCS 3.1.0 for the outer contract and keep the MVP subset small:

```yaml
apiVersion: v3.1.0
kind: DataContract
id: <stable-contract-id>
name: <source-interface-name>
version: 2.0.0
status: active
schema:
  - id: <stable-object-id>
    name: <source-object-name>
    physicalType: object
    properties:
      - id: <stable-field-id>
        name: <physical-field-name>
        logicalType: string
        description: <semantic meaning>
```

A rename should preserve the field `id` when meaning is unchanged. A semantic replacement should receive a new field `id` even if the physical name is reused.

```text
same name + different meaning  -> different identity
new name + same meaning        -> same identity when equivalence is owned and reviewed
```

### Payload schema identity

The contract release must identify the payload schema artifact used to interpret the physical data. For JSON payloads, use JSON Schema 2020-12.

The MVP does not prescribe one vendor registry. The schema reference may be:

- immutable Schema Registry ID plus subject/version;
- immutable repository URI at a commit/tag;
- release-time schema bundle digest;
- another immutable content-addressed artifact supported by the runtime.

A mutable path such as `schemas/current.json` is not sufficient for replay.

### Referenced JSON Schemas

A root-file checksum alone is not enough when `$ref` or `$dynamicRef` can resolve mutable resources.

For the MVP, use one of two patterns:

1. **bundle at release**: publish the root schema and required dependency closure as one immutable artifact; or
2. **pin every dependency**: every external reference resolves to an immutable version/content identity.

Exact validator binary/version capture is deferred unless a downstream case requires byte-for-byte historical validation behavior. The MVP promises recoverable contract interpretation, not universal deterministic execution across all future validator implementations.

## Artifact 2: Consumer Canonical Binding release

ODCS describes the producer/consumer agreement and schema, but it should not be stretched into a general transformation language. The downstream mapping is a separate artifact because ownership is different.

### Consumer responsibility

The downstream/canonical-model owner owns:

- target canonical model identity/version;
- accepted source contract releases;
- mapping from stable source field IDs to stable canonical field IDs;
- normalization decisions required to preserve canonical meaning;
- explicit unsupported, lossy, ambiguous, or blocked mappings;
- transformation implementation reference used by a real pipeline.

The producer is consulted when semantic clarification is required, but is not required to edit downstream implementation code.

### Minimal binding shape

```yaml
bindingId: <stable-binding-id>
bindingVersion: 1.0.0
sourceContract:
  id: <source-contract-id>
  supportedVersions: [1.0.0, 2.0.0]
targetModel:
  id: <canonical-model-id>
  version: 1.0.0
mappings:
  - sourceFieldId: conversion-status
    targetFieldId: conversion-status
    operation: identity
```

Reference stable identities rather than physical names. A physical-path override is allowed only when the runtime needs one and the source schema cannot resolve it.

### Do not build a mapping language

The MVP binding supports only enough metadata to declare:

- identity mapping;
- rename/path relocation;
- explicit safe type/unit normalization;
- dropped/unmapped source field;
- required target field with no valid source (`blocked`);
- custom transformation implemented elsewhere, identified by a stable transformation reference.

Complex joins, aggregations, stateful event logic, business KPIs, and arbitrary SQL remain in implementation code or downstream model logic. The binding records the contract boundary; it does not become a new ETL engine.

## Artifact 3: Runtime provenance

A contract is useful during an incident only when a record or batch can be associated with the release that governed it.

### Bronze

Bronze preserves raw source fidelity plus the minimum provenance needed to identify interpretation.

Use the **lowest necessary lineage granularity**:

- per event when schema can vary event-by-event;
- per file/batch/partition when all contained records share one release.

Minimum logical metadata:

```text
source_contract_id
source_contract_version
schema_artifact_ref
source_record_or_batch_id
ingested_at
```

Do not repeat large schema documents or long digests on every row when a batch manifest can carry the same fact. Failed interpretation must not silently destroy the raw source record.

### Silver

Silver converges multiple active source versions into the canonical model.

Minimum replay metadata is logically:

```text
source_record_or_batch_id
source_contract_id + source_contract_version
canonical_binding_id + canonical_binding_version
transform_release
```

This may be stored directly, referenced through a compact lineage key, or kept in a separate operational lineage/index table. The design does **not** require a giant value-level `source row x target field` mapping table.

Field mapping is primarily a **schema-version-to-canonical binding artifact**, not per-value lineage.

### Gold

Gold should normally be source-version blind and consume canonical Silver semantics.

If a source change cannot be mapped without changing canonical meaning, do not hide the change behind a mapping. Version or split the canonical semantic model and make the Gold consumer choose deliberately.

## Concurrent active versions

The design assumes old and new producer versions can remain active together for months or years.

```text
old device -> contract 1.0 -> physical `result_code`        --+
                                                             +--> canonical `conversion_status`
new device -> contract 2.0 -> physical `conversion_status` --+
```

If both physical fields carry the same semantics, both contract releases preserve the same stable source field ID and the binding maps that identity to one canonical field.

Do not force the producer to make v2 parse v1 data merely because both versions coexist. A consumer binding declares exactly which active contract releases it supports. This is more precise than treating `BACKWARD_TRANSITIVE` as a universal default.

## Compatibility model

Compatibility is evaluated across independent gates.

### Gate 1: Structural compatibility

Can the payload be parsed/validated under the intended schema policy? A Schema Registry check is useful evidence here, not the final verdict.

### Gate 2: Stable identity continuity

For each load-bearing source field:

- same identity + rename/reorder/path move is allowed when meaning is preserved;
- changed meaning requires a new identity;
- deleted identity must be visible to affected bindings.

### Gate 3: Semantic compatibility

Check meaning that JSON Schema cannot reliably prove:

- unit/currency;
- code-set meaning;
- timestamp semantics;
- default/null meaning;
- entity/event grain;
- authoritative source meaning;
- enum values whose business interpretation changed.

### Gate 4: Binding completeness

For each supported source contract version, can every required canonical field be produced without guessing? A deleted or semantically changed source field that feeds a required target must fail closed until an explicit downstream decision exists.

### Gate 5: Consumer compatibility

Record at least:

- versions supported by the binding;
- minimum support window;
- known unsupported versions;
- deprecation date when known;
- replay requirements when they actually exist.

### SemVer rule

Use SemVer as a release label, not a compatibility oracle.

- PATCH: metadata/documentation correction with no behavior or semantic change;
- MINOR: compatible additive change under the declared consumer policy;
- MAJOR: breaking structural/semantic identity change or removal requiring consumer action.

The compatibility gates determine whether a change is compatible; SemVer records that decision.

## Canonical model versioning

The canonical model is also versioned. A stable canonical field ID should survive physical renames. When canonical meaning changes, introduce a new canonical identity or major/epoch boundary rather than silently reusing the old identity.

```text
producer v1 meaning A -> canonical field X
producer v2 meaning B -> canonical field X  # prohibited if A != B
```

If A and B are not equivalent, the binding must not merge them merely to keep Gold unchanged.

## Team boundary and PR model

Do not require one cross-repository mega-PR.

```text
Producer PR
  -> publishes source contract/schema release
  -> declares changed stable identities and semantics
  -> does not edit downstream implementation

Consumer PR
  -> updates canonical binding when needed
  -> declares newly supported source release
  -> updates legacy or modern implementation separately

Activation decision
  -> producer and consumer support windows overlap
  -> required binding checks pass
  -> rollout can proceed
```

The contract can exist before every downstream migrates. A consumer becomes compatible only when its binding declares and validates support.

Ownership remains explicit:

- producer owns what it emits;
- consumer owns what it needs;
- platform owns distribution/validation mechanics;
- domain authority resolves semantic disputes;
- contract format ownership does not grant authority over another team's implementation.

## Legacy and modern downstream implementations

### Legacy code path

A hard-coded transformer is acceptable when it:

- declares which `source_contract_id/version` it supports;
- declares which `canonical_binding_id/version` it implements;
- preserves replay metadata;
- passes the same contract/binding cases as any newer implementation;
- fails closed for unsupported or ambiguous source releases.

### Medallion path

```text
Bronze: raw fidelity + source contract/schema provenance
Silver: version-aware parse/normalize -> canonical model
Gold: business metrics/aggregates over stable canonical semantics
```

Do not add a new physical layer solely for mapping. A logical normalization stage inside Silver is sufficient unless a real workload proves otherwise.

### Streaming path

A stream message can carry or inherit the source schema/contract identity. Version routing chooses a supported binding, then emits the canonical event.

### Non-medallion warehouse / ETL path

The same contract/binding pair can govern staging-to-core or source-to-dimensional transformations. `Bronze` and `Silver` are implementation labels, not part of the contract itself.

## Git-first storage layout

The MVP can be represented without a service:

```text
contracts/
  <source-contract-id>/
    <contract-version>/
      contract.odcs.yaml
      payload.schema.json
      manifest.yaml          # optional for bundled/pinned schema dependencies

bindings/
  <canonical-model-id>/
    <source-contract-id>/
      <binding-version>.yaml
```

The exact repository may be producer-owned, consumer-owned, or a governed contract repository. Logical IDs must not depend on Git paths.

A future registry may index these artifacts, but the MVP should prove the lifecycle before introducing another service.

## Access interfaces

The MVP requires interfaces conceptually, not a new API implementation.

### Authoring

```text
create/edit -> validate -> compatibility review -> merge -> immutable release/tag
```

### Producer lookup

```text
contract ID + contract version -> schema artifact reference
```

This can be compiled into deployment configuration or resolved through an existing registry.

### Consumer lookup

```text
source contract ID/version + target model -> supported binding release
```

For an MVP this may be configuration checked into the downstream repository. A network lookup is not required.

### Investigation

```text
record/batch -> contract -> schema -> binding -> transform release
```

Lakehouse metadata is the durable replay record. Elasticsearch/Kibana/ES|QL may index the same metadata for fast troubleshooting, but should not be the only authority.

### Discovery

DataHub or an existing catalog can index contract ID/version/status, owner/domain, stable field IDs, binding relationships, canonical target, and deprecation/support metadata. Do not build a second metadata graph in Lattice when an existing catalog can hold the projection.

## MVP release lifecycle

Use a simple independent lifecycle for source contracts and bindings:

```text
proposed -> active -> deprecated -> retired
```

A source contract can be `active` while one consumer does not support it. A binding can be retired while the source contract remains active for other consumers.

An active release is immutable. Interpretation-changing corrections create a new release.

## Required review questions

Every producer contract change should answer:

1. Which stable field identities were added, removed, renamed, or semantically replaced?
2. Does the payload schema dependency closure remain immutable/recoverable?
3. Is the source contract structurally compatible under the declared policy?
4. Which changes require semantic review rather than structural inference?
5. Which known bindings consume the changed identities?
6. What is the producer support/deprecation window?

Every affected consumer binding change should answer:

1. Which source contract versions are supported?
2. Can every required canonical field be produced without guessing?
3. Did canonical meaning remain stable?
4. Is any transformation lossy, custom, or blocked?
5. Does the implementation declare the binding/transform release used?
6. Can historical data be traced to the artifacts required for replay?

## Synthetic conformance cases for a downstream pilot

| Case | Expected decision |
|---|---|
| physical field rename, stable meaning and stable field ID | both versions map to one canonical field |
| field moves JSON path, stable identity | parser/path resolution changes; canonical meaning does not |
| optional unused source field added | no binding change unless policy says otherwise |
| mapped source field deleted | affected binding blocked until explicit decision |
| same physical name reused with new meaning | new source identity; old binding must not silently accept |
| unit seconds -> milliseconds | explicit normalization or new semantic identity required |
| old and new devices emit concurrently | both contract releases route during same window |
| unknown contract version arrives | preserve raw data; canonicalization fails closed/quarantines |
| legacy hard-coded transformer | acceptable if it declares and satisfies the same binding |
| external JSON Schema reference changes | invalid release unless reference was immutable or bundled/pinned |

The examples under `examples/versioned-data-contract-mvp/` illustrate the rename and concurrent-version cases. They are synthetic architecture fixtures, not production validation.

## Replay and audit boundary

Practical canonicalization replay requires:

```text
raw source payload
+ source contract release
+ payload schema artifact/bundle
+ canonical binding release
+ transformation release
```

This is stronger than storing only a `schema_version` column.

The MVP does **not** claim universal byte-for-byte deterministic replay across future runtime libraries. If a regulated or safety-critical downstream case requires that stronger property, extend the release manifest to pin parser/validator/runtime versions and prove it in a preserved replay test before promoting the requirement globally.

## Red-team findings retained

1. **Stable IDs can be misused.** Same ID is a producer claim, not proof of unchanged semantics; semantic review remains separate.
2. **ODCS is not a runtime registry.** It standardizes the document; runtime resolution still uses existing registry/configuration surfaces.
3. **Schema compatibility does not prove semantic compatibility.** Structural and semantic gates remain separate.
4. **Per-value lineage can explode storage.** Keep field mapping at schema/binding level and runtime provenance at the lowest necessary event/batch granularity.
5. **Canonical models can hide breaking changes.** Fail closed when equivalence cannot be established; version/split canonical semantics when necessary.
6. **A new platform can become the project.** No registry service, generic mapping engine, DataHub replacement, or code generation is part of the MVP.

## Highest-return downstream pilot

```text
one source interface
+ two simultaneously active schema versions
+ one renamed or relocated field with stable meaning
+ one canonical Silver target
+ one legacy or modern transformer
+ replay metadata for one batch/event path
```

Deliver only:

1. two immutable source contract/schema releases;
2. one canonical model identity;
3. one binding release supporting both source versions;
4. one implementation declaration tying the transformer to the binding release;
5. synthetic and sampled-private conformance evidence;
6. one replay/troubleshooting walkthrough.

Do not start with a fleet-wide migration, company-wide registry, generic contract API, universal compatibility policy, or automatic code generation.

## Phase plan

### Phase 0 — Public architecture reference

This PR.

Success means ownership boundaries are explicit, artifacts and IDs are concrete enough to implement downstream, concurrent source versions are first-class, legacy and medallion paths are both supported, and unresolved guarantees are visible rather than implied.

### Phase 1 — Private single-interface pilot

Required evidence:

- two real active source schema generations;
- producer semantic review;
- consumer binding;
- transformer declaration of binding release;
- historical raw-to-canonical replay or investigation;
- measured operational burden versus current hard-coded version handling.

Decision after the pilot:

```text
keep simple files
| add validator/CI only
| integrate existing Schema Registry/DataHub more deeply
| stop if ceremony does not reduce change/debug cost
```

### Phase 2 — Only after observed second use

Possible extensions after another interface/consumer demonstrates the same need:

- machine validation of binding documents;
- changed-field impact reports;
- DataHub/catalog indexing;
- Schema Registry release projection;
- generated runtime configuration;
- ES|QL troubleshooting projection;
- stronger deterministic replay manifests.

None are implied by Phase 0.

## Exit criteria

Retain the architecture only if a pilot demonstrates that:

- two active source versions coexist without version branches leaking into Gold;
- rename/path move uses stable identity and one reviewed binding rather than duplicated canonical columns;
- unsupported semantic changes fail visibly instead of being silently coerced;
- a downstream engineer can trace canonical output back to source contract, schema, binding, and transform release;
- legacy code can participate without framework rewrite;
- contract maintenance effort is lower than repeated bespoke downstream interpretation.

If these do not hold, keep source schema/version metadata but stop before creating more contract-layer infrastructure.

## Non-goals

This MVP does not:

- implement a new Lattice Skill or active module;
- replace DataHub, Schema Registry, Delta, Iceberg, or an existing catalog;
- define a universal canonical model;
- implement ETL, Silver tables, Gold metrics, or runtime code;
- require one producer PR to modify consumer repositories;
- require `BACKWARD_TRANSITIVE` or any one compatibility mode globally;
- create value-level lineage for every mapped field;
- claim that SemVer proves compatibility;
- claim that a schema checksum alone proves replayability;
- automatically approve architecture, semantic meaning, deployment, or production promotion.
