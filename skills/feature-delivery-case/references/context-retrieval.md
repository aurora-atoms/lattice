# Context Retrieval Policy

## Retrieval Order

Use progressive disclosure:

1. case identity, current revision, requested outcome, and known source refs;
2. compact indexes, ConPort, registries, architecture maps, and decision indexes;
3. targeted business-rule and system-constraint sources;
4. similar cases and negative knowledge;
5. bounded implementation, PR, test, review, metric, and operational evidence;
6. broader search only when a named gap remains.

Do not load all Skills, repository files, Jira issues, PRs, logs, or historical cases.

## Coverage Categories

For each category record `found`, `none_found`, `not_applicable`, or `pending` plus search scope and refs.

### Business rules

Look for eligibility, policy, entitlement, pricing, workflow, compliance, ownership, data-handling, and user-experience rules.

### System constraints

Look for architecture boundaries, APIs, schemas, compatibility, performance, security, deployment, observability, operational, and environment constraints.

### Similar cases

Retrieve cases with comparable outcomes, affected surfaces, dependencies, failures, or validation patterns. Similarity is evidence for investigation, not permission to copy a solution.

### Negative knowledge

Search for rejected designs, failed experiments, deprecated APIs, known incidents, invalid assumptions, rollbacks, security findings, performance regressions, and approaches that only worked under narrower conditions.

Record why the negative knowledge applies or does not apply. Do not silently discard contradictory sources.

### Source facts

Use authoritative requirement, policy, repository, runtime, metric, review, or stakeholder sources. Separate facts from inference and unresolved interpretation.

## Freshness and Authority

For sources whose validity can change, record observed time, source owner, freshness window, supersession state, and review trigger.

When sources conflict:

1. preserve both refs;
2. state the conflict precisely;
3. identify the authority needed to resolve it;
4. block readiness when the conflict affects scope, acceptance, safety, compatibility, or deployment.

## Projection Boundary

Project raw sources into concise case facts. Preserve the source ref and enough context to verify the projection. Never replace a source with an untraceable summary.
