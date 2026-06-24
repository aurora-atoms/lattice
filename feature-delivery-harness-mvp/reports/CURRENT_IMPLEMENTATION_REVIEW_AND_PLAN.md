# Current Implementation Review And Plan

Review date: 2026-06-08

Status: current implementation accepted as a P1.5 hardening candidate.

## Review Findings

No blocking findings remain in the current FDH implementation review.

Resolved review items:

```text
schema_runtime_validation:
  validate_jsonl now rejects schema/type mismatches through dependency-light JSON Schema subset checks.

evidence_graph_validation:
  check_evidence_completeness now resolves FDH machine ref arrays and delivery_status_ref.

delivery_verdict_contract:
  author_delivery_verdict treats any failed validation.result as not user usable unless blocked takes precedence.

dossier_contract:
  run_mvp_evals generates delivery.verdict before Token Economics Dossier when both are expected.

dependency_light_validation:
  Power BI semantic spec validator no longer requires PyYAML for ordinary nested catalog validation.
```

Verified gates:

```text
python3.14 feature-delivery-harness-mvp\scripts\validate_contract_alignment.py
python3.14 feature-delivery-harness-mvp\scripts\run_mvp_evals.py
python3.14 scripts\validate_skill_package.py --root skills
temporary malformed FDH JSONL smoke test -> INVALID_SCHEMA_VALUE
temporary Power BI semantic specs smoke test -> OK: semantic specs are valid
```

## Updated Plan

Next priority: P2 Contract Corpus And CI Readiness.

Goal:

```text
Turn the accepted P0-beta/P1/P1.5 vertical slice into a repo-grade validation corpus that can run in CI and catch contract drift without relying on generated-report side effects.
```

Priority work:

```text
P2.1 validator self-test corpus:
  add focused positive and negative fixtures for schema values, envelope mismatches, evidence graph refs, verdict precedence, context-pack projection, and dossier claim evidence.

P2.2 single CI entrypoint:
  add a dependency-light run_fdh_checks.py script that runs contract alignment, evals, generated JSONL validation, and skill package validation with stable exit codes.

P2.3 generated artifact freshness:
  add a check that generated reports match eval goldens or are explicitly regenerated, so dossier/verdict output drift is visible.

P2.4 failure-code hygiene:
  decide whether schema additionalProperties failures should remain separate from UNKNOWN_PAYLOAD_FIELD or be de-duplicated for cleaner expected codes.

P2.5 evidence graph matrix:
  document which payload *_refs fields are resolvable evidence graph edges and which fields are artifact identifiers.

P2.6 Power BI validator portability:
  add a small in-repo synthetic Power BI spec fixture to prove the PyYAML fallback path under the normal skill validation workflow.
```

Out of scope for P2:

```text
model routing
automatic promotion
release approval
raw transcript/log ingestion
company-derived fixtures
```
