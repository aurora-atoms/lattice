# End-to-End Synthetic Private Consumer — PR 4

## Decision

PR 4 completes the public conformance stage with explicit heterogeneous eval manifests, deterministic dispatch, machine-readable summaries, a generated synthetic downstream asset pack, negative mutation checks, golden comparison, and full-suite CI.

## Heterogeneous Eval Contract

Every directory under `feature-delivery-harness-mvp/evals/` has `case.json` using `lat.eval-case.v1@1.0.0`.

Supported case types:

```text
feature_delivery
reusable_asset_loop
synthetic_downstream
```

`run_mvp_evals.py` validates the manifest and required files before dispatch. Missing or malformed manifests, incompatible versions, unknown case types, unsafe paths, or missing required files fail and remain visible in `lat.conformance-summary.v1`.

No directory is silently skipped.

## Synthetic Consumer

`examples/synthetic-private-consumer/` simulates:

```text
synthetic PR review
-> experience contribution
-> Feature Delivery Case
-> reusable asset candidate and change proposal
-> synthetic format review
-> never-by-default activation
-> evidence-linked manager claims
-> Manager-Ready Delivery Asset Pack
-> local validation and golden comparison
```

The committed golden pack contains:

```text
asset-pack.manifest.json
feature-delivery-case.json
evidence-ledger.jsonl
contribution-ledger.jsonl
reusable-assets/dangling-evidence-ref-guard/
reusable-asset-dossier.md
manager-brief.json
manager-brief.md
validation-report.json
```

All records are `synthetic_reference`; downstream adoption remains `not_observed`; usage observations are empty; simulated review validates format only.

## Negative Gates

The synthetic runner must reject:

- dangling evidence references;
- synthetic `used_once`;
- unsupported private-extension capability versions;
- unreviewed activation;
- a single synthetic case expressed as team-wide adoption.

Runner unit tests additionally reject malformed manifests, missing required files, incompatible schema versions, and unknown case types. Existing public/private tests retain secret, private-path, DeliveryYield, transition, and adoption gates.

## Machine Evidence

```bash
python feature-delivery-harness-mvp/scripts/run_mvp_evals.py \
  --summary-out conformance-summary.json
```

The full suite includes all Feature Delivery Harness cases, the reusable-asset golden case, and the synthetic downstream golden case. GitHub Actions runs the same command and uploads the summary plus generated reports.

## Compatibility

Existing eval inputs and `expected.json` files remain unchanged. The former homogeneous directory convention is replaced by explicit `case.json` dispatch; consumers invoking `run_mvp_evals.py` without arguments retain the same command surface and now receive a summary file.

No Skill package, active module, public capability identity, or adoption state changed. This PR proves public contract conformance only.
