# Incremental Skill CI Contracts

## Purpose

Strengthen Skill-package CI without forcing unrelated historical cleanup into every pull request. The gate applies strict deterministic checks to Skill packages changed by the current branch while preserving full-repository validation and human authority over semantic design decisions.

## Validation Layers

```text
full repository package validation
-> changed-package authoring contract
-> incremental warning ratchet
-> declared output-path contract
-> selector, registry, and version alignment
-> token-efficiency advisory
-> domain schemas and regression tests
-> machine-readable validation evidence
```

## Changed-Package Warning Ratchet

Warnings from `validate_skill_package.py` become blocking findings for a Skill package changed by the current branch. Existing warnings in untouched packages remain visible in the full validation output but do not force unrelated cleanup.

Stable finding codes include:

```text
SKILL.RETRIEVAL.CONPORT_FIRST_MISSING
SKILL.TOKEN.ROI_MISSING
SKILL.TOKEN.STABLE_PREFIX_MISSING
SKILL.REFERENCE.LOCAL_FILE_MISSING
SKILL.STRUCTURE.REPEATED_BULLETS
SKILL.CONTEXT.HUGE
```

The ratchet prevents new or edited packages from introducing known quality debt while allowing historical cleanup to proceed through bounded follow-up work.

## Declared Output Contract

Every changed Skill must declare at least one governed artifact path under `artifacts/` and the standard capability run-result path:

```text
artifacts/capability-runs/<skill-name>/<run-id>/run-result.json
```

Declared paths must:

- be repository-relative;
- remain under `artifacts/`;
- include `<run-id>`;
- avoid path traversal and generic filenames such as `output.json` or `latest.json`;
- declare `write_status=returned_inline` when an inline fallback is offered.

This check validates declaration quality. It does not claim that every declared artifact already has a complete domain JSON Schema; artifact-specific schemas and semantic validators remain separate capability work.

## Selector and Registry Alignment

For changed selector Skills, CI checks that referenced specialist packages:

- exist under `skills/`;
- are registered in the capability context catalog or a bounded extension;
- have semantic versions in `registry/capability-context-policy.json`;
- match the specialist set in the corresponding registry extension when that extension owns the selector family.

For changed registry extensions, every registered Skill must have a package and version. New Skill packages must begin at `1.0.0`; every later package modification remains subject to the existing monotonic version gate.

## Token-Efficiency Signals

Token efficiency is evaluated after correctness and contract fidelity. CI emits advisory findings when:

- a changed `SKILL.md` exceeds an estimated 2,500 tokens; or
- an existing Skill grows by at least 500 estimated tokens and more than 30 percent.

These are review signals rather than automatic failures. Token count alone is not a value metric; reviewers should verify that added context improves user-visible quality, evidence, safety, or contract precision.

## Machine-Readable Evidence

The incremental gate can write:

```text
skill_ci_contract_report.json
```

The report uses `lat.skill-ci-contract-report.v1` and records:

- comparison refs;
- changed Skill names;
- error and warning totals;
- stable finding codes;
- severity, path, and message for each finding.

GitHub Actions uploads this report together with the Skill inventory and quality report as validation evidence. The report is audit evidence, not approval to merge or release.

## Local Commands

```bash
python scripts/validate_skill_ci_contracts.py \
  --base-ref <base-sha> \
  --head-ref HEAD \
  --report-out skill_ci_contract_report.json

python -m unittest discover -s tests -p 'test_skill_ci_contracts.py' -v
python -m compileall -q scripts tests
```

## Boundaries

The gate does not:

- automatically rewrite Skill packages;
- auto-promote warnings into organizational rules outside the changed-package scope;
- decide whether a semantic change is patch, minor, or major beyond existing deterministic constraints;
- replace artifact-specific schemas, semantic validators, product judgment, governance review, or merge authority;
- treat token count, CI activity, or package count as the final value metric.
