# Reusable Asset Dossier v0.1

## Asset
- Asset ID: `asset_no_auto_promotion_guidance`
- Name: No-Auto-Promotion Guidance
- Version: `0.1.0`
- Type: `rule`
- Status: `used_once`
- Activation: `task_scoped`
- Owner: capability-governance-owner

## Origin
- Feature Delivery Case: `fdc_reusable_asset_001`
- Contribution: `contribution_pr_review_001`
- Source: `github://aurora-atoms/lattice/pull/fixture#review-comment-1`
- Contribution kind: `review_comment`

## Problem Addressed
A successful delivery case could be overgeneralized into a team-wide rule without review.

## Summary
Require explicit human review before a reusable asset becomes qualified or team-available.

## Scope
- Current scope: Synthetic Feature Delivery Harness promotion-boundary cases.
- Out of scope: Organization-wide policy or automatic Skill activation.
- Artifact: `feature-delivery-harness-mvp/references/reusable-asset-loop.md`

## Human Review
- Decision: `approved`
- Reviewer: capability-governance-owner
- Notes: Approved for task-scoped use once. This does not authorize team-wide activation or automatic promotion.

## Observed Usage
- Used for: Validate that a review comment can become a scoped, reviewed asset candidate without automatic promotion.
- User role: `capability-maintainer`
- Outcome: `artifact_created`
- Evidence: `asset_review_001`, `reusable_asset_loop_case_001`

## Known Limitations
- Validated only on a synthetic vertical-slice fixture.

## Open Questions
- Which additional asset types require specialized validation before reuse?

## Next Iteration
Run the same path on one real PR or CI failure with sanitized evidence.

This dossier reports a scoped, evidence-linked asset state. It does not prove organization-wide ROI or authorize automatic promotion.
