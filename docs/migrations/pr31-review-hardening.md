# PR 31 Contract Review Hardening

## Decision

The pre-merge review found that the happy-path implementation passed CI while several cross-file and failure-path invariants remained unenforced. This correction keeps the existing `1.0.0` downstream contracts because they have not been released from the stacked PR, and tightens them before merge.

## Corrected Invariants

- A completed asset pack includes both `manager_brief` JSON and `manager_brief_rendered` Markdown.
- Rendered Markdown must equal the canonical structured projection byte-for-byte; hand-edited additions and omitted limitations fail.
- Evidence, contributions, the Feature Delivery Case, the manager brief, reusable-asset records, and the validation report must agree on pack, case, simulation, origin, adoption, asset, and version identities where applicable.
- A declared validation report is required for a completed pack and conforms to `lat.delivery-asset-pack-validation-report.v1@1.0.0`.
- Synthetic evidence and consumer classifications cannot be mixed with real-downstream classifications.
- Only the exact `v0.0.0-synthetic` plus all-zero SHA sentinel bypasses local checkout resolution. Every other declared pin is resolved locally.
- `UNKNOWN` statements visibly communicate uncertainty rather than hiding an affirmative assertion behind a machine classification.
- Human challenge, human review, governance approval, proposal, and review evidence references resolve locally.
- Usage observations remain empty for synthetic fixtures and meet the minimum count implied by `used_once`, `reused`, or `team_available`.
- Eval manifests reject invalid case IDs, duplicate or incomplete required-file declarations, empty suites, missing suite roots, and timed-out handlers.
- The synthetic conformance runner requires its full negative-case set and refuses destructive output replacement without explicit `--force`.

## CI

CI now:

1. validates downstream schemas against committed instances with Draft 2020-12;
2. runs the adversarial validator and runner regressions;
3. runs the complete heterogeneous suite;
4. checks whitespace against the actual PR base or push predecessor with full history.

## Compatibility

This is a pre-release correction to the stacked PR, not a released-contract migration. A downstream prototype copied from an earlier commit on the branch must:

1. add `lat.delivery-asset-pack-validation-report.v1: 1.0.0` to `contract_versions`;
2. add `artifacts.manager_brief_rendered`;
3. generate the canonical Markdown projection;
4. regenerate the validation report;
5. rerun local schema, consumer, asset-pack, manager-claim, negative-case, and golden checks.

No Skill package or active module was changed. Public conformance remains separate from private adoption, manager acceptance, ROI, and business value.
