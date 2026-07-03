from __future__ import annotations

from typing import Any

from runtime.kuuos_lifecycle_authorization_decision_types_v0_12 import (
    APPROVED as SOURCE_APPROVED,
    LifecycleAuthorizationDecisionArtifactV012,
    LifecycleAuthorizationDecisionEvidenceV012,
    LifecycleAuthorizationDecisionPolicyV012,
    LifecycleAuthorizationDecisionSubmissionV012,
)
from runtime.kuuos_lifecycle_operation_approval_binding_v0_13 import (
    evidence_issues,
    scope_matches,
    submission_issues,
)
from runtime.kuuos_lifecycle_operation_approval_policy_v0_13 import policy_issues
from runtime.kuuos_lifecycle_operation_approval_source_v0_13 import (
    all_source_digests,
    prior_actor_ids,
    source_recomputed_valid,
)
from runtime.kuuos_lifecycle_operation_approval_types_v0_13 import (
    OBJECTIVE,
    LifecycleOperationApprovalEvidenceV013,
    LifecycleOperationApprovalPolicyV013,
    LifecycleOperationApprovalSubmissionV013,
)

STRUCTURAL_CHECKS = (
    "policy_valid", "approval_valid", "evidence_valid",
    "source_recomputed_valid", "source_authorization_approved",
    "source_binding_valid", "identity_binding_valid",
    "operation_approver_allowed", "operation_approver_organization_allowed",
    "future_operator_allowed", "independent_from_prior_chain",
    "independent_from_requester", "independent_from_source_decision_reviewer",
    "independent_from_authorization_decision_maker",
    "independent_from_future_operator", "approver_operator_separated",
    "objective_allowed", "approval_delay_valid", "evidence_fresh",
    "time_order_valid", "source_authorization_window_valid",
    "source_authorization_not_expired", "approval_not_expired",
    "operation_start_deadline_valid", "operation_approval_route_binding_valid",
    "scope_binding_valid",
)

DENIAL_CHECKS = (
    "approver_mandate_verified", "approver_qualification_verified",
    "approver_independence_declared", "conflict_disclosure_complete",
    "material_conflict_absent", "jurisdiction_verified", "quorum_satisfied",
    "reasoned_approval_complete", "proportionality_satisfied",
    "operator_acknowledged", "execution_package_integrity_verified",
    "resources_reserved", "scope_bounded", "target_resources_allowed",
    "protected_resources_excluded", "no_irreversible_steps",
    "rollback_plan_verified", "recovery_route_verified",
    "stop_conditions_complete", "abort_channel_available",
    "human_oversight_available", "monitoring_plan_complete",
    "evidence_capture_plan_complete", "simulation_verified",
    "operation_window_valid", "protected_core_excluded",
    "institutional_hold_absent", "emergency_state_absent",
    "appeal_route_available", "dissent_route_available",
    "minority_opinion_recorded",
)


def evaluate(
    approval: LifecycleOperationApprovalSubmissionV013,
    evidence: LifecycleOperationApprovalEvidenceV013,
    policy: LifecycleOperationApprovalPolicyV013,
    source_decision: LifecycleAuthorizationDecisionSubmissionV012,
    source_evidence: LifecycleAuthorizationDecisionEvidenceV012,
    source_policy: LifecycleAuthorizationDecisionPolicyV012,
    source_record: LifecycleAuthorizationDecisionArtifactV012,
    source_args: tuple[Any, ...],
) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(
        source_decision, source_evidence, source_policy, source_record, source_args
    )
    source_approved = (
        source_record.status == SOURCE_APPROVED
        and source_record.authorization_decision_record_issued
        and source_record.authorization_decision_made
        and source_record.authorization_approved
        and not source_record.authorization_denied
        and source_record.operation_approval_required_next
        and source_record.operation_approval_route_required_next
        and not source_record.operation_approved
        and not source_record.operation_started
        and not source_record.operation_completed
        and not source_record.authority_changed
        and not source_record.quiescence_state_changed
        and not source_record.terminal_state_changed
        and not source_record.terminal_marker_written
        and not source_record.resource_removed
        and not source_record.external_operation_performed
        and not source_record.repository_changed
        and source_record.lifecycle_read_only
    )
    source_binding = (
        (approval.subject_id, approval.subject_kind, approval.subject_version)
        == (evidence.subject_id, evidence.subject_kind, evidence.subject_version)
        == (source_decision.subject_id, source_decision.subject_kind, source_decision.subject_version)
        and approval.source_authorization_decision_id
        == evidence.source_authorization_decision_id
        == source_decision.authorization_decision_id
        and approval.source_authorization_record_digest
        == evidence.source_authorization_record_digest
        == source_record.record_digest
        and evidence.source_artifact_digests == expected_digests
        and approval.requester_id == evidence.requester_id == source_decision.requester_id
        and approval.source_authorization_decision_maker_id
        == evidence.source_authorization_decision_maker_id
        == source_decision.authorization_decision_maker_id
        and approval.source_decision_reviewer_id
        == evidence.source_decision_reviewer_id
        == source_decision.source_decision_reviewer_id
        and approval.future_operator_id
        == evidence.future_operator_id
        == source_decision.future_operator_id
    )
    identity_binding = (
        approval.operation_approval_id == evidence.operation_approval_id
        and approval.operation_approver_id == evidence.operation_approver_id
        and approval.operation_approver_organization_id
        == evidence.operation_approver_organization_id
        and approval.approval_evidence_digest == evidence.evidence_digest
        and approval.approval_requested_at_epoch_seconds
        == evidence.approval_requested_at_epoch_seconds
        and approval.completed_at_epoch_seconds == evidence.completed_at_epoch_seconds
        and approval.operation_approval_route_digest
        == evidence.operation_approval_route_digest
        and approval.operation_start_deadline_at_epoch_seconds
        == evidence.operation_start_deadline_at_epoch_seconds
    )
    prior_ids = prior_actor_ids(approval.subject_id, source_decision, source_args)
    delay = approval.completed_at_epoch_seconds - source_decision.completed_at_epoch_seconds
    age = approval.completed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    time_order = (
        evidence.approval_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.completed_at_epoch_seconds
        == approval.completed_at_epoch_seconds
    )
    source_window = (
        approval.completed_at_epoch_seconds
        <= source_decision.operation_approval_deadline_at_epoch_seconds
        == source_evidence.operation_approval_deadline_at_epoch_seconds
    )
    source_not_expired = (
        approval.completed_at_epoch_seconds
        <= source_evidence.authorization_decision_expiry_at_epoch_seconds
    )
    approval_not_expired = (
        approval.completed_at_epoch_seconds
        <= evidence.operation_approval_expiry_at_epoch_seconds
        <= approval.completed_at_epoch_seconds + policy.max_approval_expiry_seconds
        and evidence.operation_approval_expiry_at_epoch_seconds
        <= source_evidence.authorization_decision_expiry_at_epoch_seconds
    )
    start_deadline = (
        approval.completed_at_epoch_seconds
        <= evidence.operation_start_window_open_at_epoch_seconds
        < approval.operation_start_deadline_at_epoch_seconds
        <= evidence.operation_approval_expiry_at_epoch_seconds
        and approval.operation_start_deadline_at_epoch_seconds
        <= approval.completed_at_epoch_seconds + policy.max_operation_start_delay_seconds
    )
    scope_bounded = 0 < len(evidence.operation_scope_items) <= policy.max_scope_items
    targets_allowed = bool(evidence.target_resource_ids) and set(
        evidence.target_resource_ids
    ).issubset(set(policy.allowed_target_resource_ids))
    protected_excluded = not (
        set(evidence.target_resource_ids) & set(evidence.protected_resource_ids)
    )
    checks = {
        "policy_valid": not policy_issues(policy),
        "approval_valid": not submission_issues(approval),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(
            source_decision, source_evidence, source_policy, source_record, source_args
        ),
        "source_authorization_approved": source_approved,
        "source_binding_valid": source_binding,
        "identity_binding_valid": identity_binding,
        "operation_approver_allowed": approval.operation_approver_id in policy.allowed_operation_approver_ids,
        "operation_approver_organization_allowed": approval.operation_approver_organization_id in policy.allowed_operation_approver_organization_ids,
        "future_operator_allowed": approval.future_operator_id in policy.allowed_future_operator_ids,
        "independent_from_prior_chain": approval.operation_approver_id not in prior_ids,
        "independent_from_requester": approval.operation_approver_id != approval.requester_id,
        "independent_from_source_decision_reviewer": approval.operation_approver_id != approval.source_decision_reviewer_id,
        "independent_from_authorization_decision_maker": approval.operation_approver_id != approval.source_authorization_decision_maker_id,
        "independent_from_future_operator": approval.operation_approver_id != approval.future_operator_id,
        "approver_operator_separated": approval.operation_approver_id != approval.future_operator_id,
        "objective_allowed": approval.objective == OBJECTIVE,
        "approval_delay_valid": 0 <= delay <= policy.max_approval_delay_seconds,
        "evidence_fresh": 0 <= age <= policy.max_evidence_age_seconds,
        "time_order_valid": time_order,
        "source_authorization_window_valid": source_window,
        "source_authorization_not_expired": source_not_expired,
        "approval_not_expired": approval_not_expired,
        "operation_start_deadline_valid": start_deadline,
        "operation_approval_route_binding_valid": approval.operation_approval_route_digest == evidence.operation_approval_route_digest == source_decision.operation_approval_route_digest,
        "scope_binding_valid": scope_matches(evidence, source_evidence),
        "approver_mandate_verified": evidence.approver_mandate_verified,
        "approver_qualification_verified": evidence.approver_qualification_verified,
        "approver_independence_declared": evidence.approver_independence_declared,
        "conflict_disclosure_complete": evidence.conflict_disclosure_complete,
        "material_conflict_absent": not evidence.material_conflict_present,
        "jurisdiction_verified": evidence.jurisdiction_verified,
        "quorum_satisfied": evidence.quorum_satisfied,
        "reasoned_approval_complete": evidence.reasoned_approval_complete,
        "proportionality_satisfied": evidence.proportionality_satisfied,
        "operator_acknowledged": evidence.operator_acknowledged,
        "execution_package_integrity_verified": evidence.execution_package_integrity_verified,
        "resources_reserved": evidence.resources_reserved,
        "scope_bounded": scope_bounded,
        "target_resources_allowed": targets_allowed,
        "protected_resources_excluded": protected_excluded,
        "no_irreversible_steps": not evidence.irreversible_step_ids,
        "rollback_plan_verified": evidence.rollback_plan_verified,
        "recovery_route_verified": evidence.recovery_route_verified,
        "stop_conditions_complete": evidence.stop_conditions_complete,
        "abort_channel_available": evidence.abort_channel_available,
        "human_oversight_available": evidence.human_oversight_available,
        "monitoring_plan_complete": evidence.monitoring_plan_complete,
        "evidence_capture_plan_complete": evidence.evidence_capture_plan_complete,
        "simulation_verified": evidence.simulation_verified,
        "operation_window_valid": 0 < evidence.operation_window_seconds <= policy.max_operation_window_seconds,
        "protected_core_excluded": evidence.protected_core_excluded,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
        "appeal_route_available": evidence.appeal_route_available,
        "dissent_route_available": evidence.dissent_route_available,
        "minority_opinion_recorded": evidence.minority_opinion_recorded,
    }
    return checks, expected_digests
