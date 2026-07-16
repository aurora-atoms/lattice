# Control Plane Contract

## Plane Boundaries

```text
system of record -> canonical registry -> rebuildable projection -> task context pack
                                            ^
capability registry -> task profile -> governed retrieval and tools
```

- System of record: versioned human or application authority.
- Knowledge registry: identity, ownership, source pointer, lifecycle, access, provenance, and projection pointers.
- Projection: lexical, vector, or graph indexes that may be deleted and rebuilt.
- Context pack: minimum authorized evidence selected for one task.
- Memory: session state or reviewed long-term facts; never an alias for the full knowledge base.

## Project Knowledge Contract Minimum

Declare:

```text
project and task boundary
authority sources and owners
reviewers and approvers
classification and ACL vocabulary
freshness and review deadlines
forbidden or candidate-only sources
golden-question dataset reference
allowed projections and clients
write and export policy
```

## Registry Minimum

Use stable IDs and explicit versions. Preserve:

```text
id kind status owner source source_version scope classification ACL
valid_from review_by expires_at provenance evidence_refs
supersedes conflict_refs projection pointers content hash
```

Omit `expires_at` only when a policy states why. Never infer access from similarity or from the user prompt.

## Lifecycle

```text
captured -> candidate -> verified -> active -> superseded | expired | revoked
                    \-> rejected
```

- Capture is evidence collection, not approval.
- Verification records the reviewer or deterministic validator and evidence.
- Activation makes the item retrievable only within its ACL and scope.
- Supersession retains the prior item and links the replacement.
- Revocation stops use without deleting audit history.

## Control Points

Fail closed when:

- the source or version cannot be resolved;
- identity or ACL evaluation is unavailable;
- classification is missing;
- an active record is expired or superseded;
- a material claim lacks a resolvable evidence locator;
- conflicts are hidden rather than returned;
- a candidate is presented as approved knowledge.

## POC Decision Sequence

1. Freeze 20-30 representative questions before tuning.
2. Start with two source types and read-only access.
3. Register 30-100 knowledge objects rather than copying a whole enterprise corpus.
4. Establish lexical plus vector retrieval and citation resolution.
5. Test ACL, conflict, stale, and no-answer behavior.
6. Add graph only for failed multi-hop or global questions with measured improvement.
7. Add write actions or agent delegation only after approval, rollback, audit, and task ownership exist.

Suggested targets are project decisions, not universal standards. Always report numerator, denominator, dataset version, and confidence interval or sample size with a rate.
