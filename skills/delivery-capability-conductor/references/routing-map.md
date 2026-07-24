# Delivery Capability Routing Map

Use this reference only after the request, role, lifecycle stage, evidence, and desired visible outcome are known.

## Stage Routing

```text
understand + unfamiliar_system -> context_mastery
prepare + ambiguous_requirement -> work_ready
implement + blocked -> delivery_rescue
review + material_change -> review_ready
release + candidate_present -> release_readiness
outcome + measurement_window -> outcome_learning
learn + release_incident_or_rework -> organizational_learning
any_stage + evidence_backed_combination_risk -> risk_ahead
any_stage + expert_decision_needed -> human_judgment_amplifier
any_stage + manager_decision_or_update_needed -> management_narrative
```

## Atomic-First Selection

Prefer one atomic capability when it can produce the requested state change. Use a pack or agent only when multiple outputs are required and have explicit dependencies.

```text
ci_failed -> red_to_green_ci
bug_not_reproducible -> bug_to_repro
environment_mismatch -> environment_doctor
contract_change -> contract_break_detector
new_codebase -> codebase_understanding
missing_domain_context -> domain_context_pack
conflicting_sources -> contradiction_finder
expired_assumption -> assumption_expiry_radar
hidden_dependency -> shadow_dependency_map
stakeholder_surprise_risk -> stakeholder_surprise_detector
ticket_not_ready -> ticket_ready_package
pr_not_ready -> pr_ready_package
release_status_unclear -> delivery_readiness_card
post_incident_learning -> delivery_immune_system
executive_update_needed -> executive_feature_brief
escalation_decision_needed -> risk_escalation_packet
```

## Selection Constraints

ROUTE.001 | MUST  | prefer_atomic_before_pack | enforce
ROUTE.002 | MUST  | require_output_dependency_before_adding_next_capability | enforce
ROUTE.003 | MUST  | avoid_duplicate_lint_summary_or_retrieval_work | enforce
ROUTE.004 | MUST  | preserve_active_module_boundaries | enforce
ROUTE.005 | NEVER | treat_DeliveryYield_as_delivery_approval_or_agent_orchestrator | block
ROUTE.006 | NEVER | classify_active_modules_as_deprecated_without_explicit_instruction | block

## Stop And Escalate

Stop and request human action when the route requires production mutation, permission escalation, compliance or legal judgment, architecture authority, business scope commitment, release approval, or personnel evaluation.
