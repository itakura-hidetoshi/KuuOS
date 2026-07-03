from __future__ import annotations

from typing import Any

from runtime.kuuos_lifecycle_operation_approval_types_v0_13 import (
    APPROVED as SOURCE_APPROVED,
    LifecycleOperationApprovalArtifactV013,
    LifecycleOperationApprovalEvidenceV013,
    LifecycleOperationApprovalPolicyV013,
    LifecycleOperationApprovalSubmissionV013,
)
from runtime.kuuos_lifecycle_operation_start_binding_v0_14 import (
    evidence_issues,
    scope_matches,
    submission_issues,
)
from runtime.kuuos_lifecycle_operation_start_policy_v0_14 import policy_issues
from runtime.kuuos_lifecycle_operation_start_source_v0_14 import (
    all_source_digests,
    expected_operation_start_route_digest,
    source_recomputed_valid,
)
from runtime.kuuos_lifecycle_operation_start_types_v0_14 import (
    OBJECTIVE,
    LifecycleOperationStartEvidenceV014,
    LifecycleOperationStartPolicyV014,
    LifecycleOperationStartSubmissionV014,
)

STRUCTURAL_CHECKS = (
    "policy_valid", "start_valid", "evidence_valid",
    "source_recomputed_valid", "source_operation_approval_approved",
    "source_binding_valid", "identity_binding_valid",
    "operator_allowed", "operator_organization_allowed",
    "operator_matches_approved_future_operator",
    "operator_separated_from_operation_approver",
    "operator_separated_from_requester",
    "operator_separated_from_source_decision_reviewer",
    "operator_separated_from_authorization_decision_maker",
    "operator_separated_from_subject", "objective_allowed",
    "start_delay_valid", "evidence_fresh", "time_order_valid",
    "source_operation_approval_not_expired", "operation_start_window_valid",
    "operation_completion_deadline_valid", "operation_start_route_binding_valid",
    "scope_binding_valid", "scope_bounded", "target_resources_allowed",
    "protected_resources_excluded", "no_irreversible_steps",
)

DENIAL_CHECKS = (
    "operator_mandate_verified", "operator_qualification_verified",
    "operator_identity_confirmed", "conflict_disclosure_complete",
    "material_conflict_absent", "jurisdiction_verified", "operator_ready",
    "start_authorization_acknowledged",
    "execution_package_integrity_reconfirmed",
    "resources_reserved_reconfirmed", "rollback_readiness_reconfirmed",
    "recovery_readiness_reconfirmed", "stop_conditions_reconfirmed",
    "abort_channel_reconfirmed", "human_oversight_reconfirmed",
    "monitoring_reconfirmed", "evidence_capture_reconfirmed",
    "protected_core_excluded", "protected_core_exclusion_reconfirmed",
    "institutional_hold_absent", "institutional_hold_absence_reconfirmed",
    "emergency_state_absent", "emergency_state_absence_reconfirmed",
)


def evaluate(
    start: LifecycleOperationStartSubmissionV014,
    evidence: LifecycleOperationStartEvidenceV014,
    policy: LifecycleOperationStartPolicyV014,
    source_approval: LifecycleOperationApprovalSubmissionV013,
    source_evidence: LifecycleOperationApprovalEvidenceV013,
    source_policy: LifecycleOperationApprovalPolicyV013,
    source_record: LifecycleOperationApprovalArtifactV013,
    source_args: tuple[Any, ...],
) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(
        source_approval, source_evidence, source_policy, source_record, source_args
    )
    source_approved = (
        source_record.status == SOURCE_APPROVED
        and source_record.operation_approval_record_issued
        and source_record.operation_approval_made
        and source_record.operation_approved
        and not source_record.operation_denied
        and source_record.operation_start_required_next
        and source_record.operation_start_route_required_next
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
        (start.subject_id, start.subject_kind, start.subject_version)
        == (evidence.subject_id, evidence.subject_kind, evidence.subject_version)
        == (source_approval.subject_id, source_approval.subject_kind, source_approval.subject_version)
        and start.source_operation_approval_id
        == evidence.source_operation_approval_id
        == source_approval.operation_approval_id
        and start.source_operation_approval_record_digest
        == evidence.source_operation_approval_record_digest
        == source_record.record_digest
        and evidence.source_artifact_digests == expected_digests
        and start.requester_id == evidence.requester_id == source_approval.requester_id
        and start.source_operation_approver_id
        == evidence.source_operation_approver_id
        == source_approval.operation_approver_id
        and start.source_authorization_decision_maker_id
        == evidence.source_authorization_decision_maker_id
        == source_approval.source_authorization_decision_maker_id
        and start.source_decision_reviewer_id
        == evidence.source_decision_reviewer_id
        == source_approval.source_decision_reviewer_id
        and start.approved_future_operator_id
        == evidence.approved_future_operator_id
        == source_approval.future_operator_id
    )
    identity_binding = (
        start.operation_start_id == evidence.operation_start_id
        and start.operator_id == evidence.operator_id
        and start.operator_organization_id == evidence.operator_organization_id
        and start.start_evidence_digest == evidence.evidence_digest
        and start.start_requested_at_epoch_seconds
        == evidence.start_requested_at_epoch_seconds
        and start.started_at_epoch_seconds == evidence.started_at_epoch_seconds
        and start.operation_start_route_digest == evidence.operation_start_route_digest
        and start.operation_completion_deadline_at_epoch_seconds
        == evidence.operation_completion_deadline_at_epoch_seconds
    )
    delay = start.started_at_epoch_seconds - source_approval.completed_at_epoch_seconds
    age = start.started_at_epoch_seconds - evidence.captured_at_epoch_seconds
    time_order = (
        evidence.start_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.started_at_epoch_seconds
        == start.started_at_epoch_seconds
    )
    source_not_expired = (
        start.started_at_epoch_seconds
        <= source_evidence.operation_approval_expiry_at_epoch_seconds
    )
    start_window = (
        source_approval.completed_at_epoch_seconds
        <= start.start_requested_at_epoch_seconds
        <= start.started_at_epoch_seconds
        and source_evidence.operation_start_window_open_at_epoch_seconds
        <= start.started_at_epoch_seconds
        <= source_evidence.operation_start_deadline_at_epoch_seconds
        == evidence.operation_start_deadline_at_epoch_seconds
    )
    completion_deadline = (
        start.started_at_epoch_seconds
        < start.operation_completion_deadline_at_epoch_seconds
        == evidence.operation_completion_deadline_at_epoch_seconds
        <= start.started_at_epoch_seconds + evidence.operation_window_seconds
        and evidence.operation_window_seconds <= policy.max_operation_window_seconds
    )
    expected_route = expected_operation_start_route_digest(
        source_approval, source_evidence, source_record
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
        "start_valid": not submission_issues(start),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(
            source_approval, source_evidence, source_policy, source_record, source_args
        ),
        "source_operation_approval_approved": source_approved,
        "source_binding_valid": source_binding,
        "identity_binding_valid": identity_binding,
        "operator_allowed": start.operator_id in policy.allowed_operator_ids,
        "operator_organization_allowed": (
            start.operator_organization_id in policy.allowed_operator_organization_ids
        ),
        "operator_matches_approved_future_operator": (
            start.operator_id == start.approved_future_operator_id
        ),
        "operator_separated_from_operation_approver": (
            start.operator_id != start.source_operation_approver_id
        ),
        "operator_separated_from_requester": start.operator_id != start.requester_id,
        "operator_separated_from_source_decision_reviewer": (
            start.operator_id != start.source_decision_reviewer_id
        ),
        "operator_separated_from_authorization_decision_maker": (
            start.operator_id != start.source_authorization_decision_maker_id
        ),
        "operator_separated_from_subject": start.operator_id != start.subject_id,
        "objective_allowed": start.objective == OBJECTIVE,
        "start_delay_valid": 0 <= delay <= policy.max_start_delay_seconds,
        "evidence_fresh": 0 <= age <= policy.max_evidence_age_seconds,
        "time_order_valid": time_order,
        "source_operation_approval_not_expired": source_not_expired,
        "operation_start_window_valid": start_window,
        "operation_completion_deadline_valid": completion_deadline,
        "operation_start_route_binding_valid": (
            start.operation_start_route_digest
            == evidence.operation_start_route_digest
            == expected_route
        ),
        "scope_binding_valid": scope_matches(evidence, source_evidence),
        "scope_bounded": scope_bounded,
        "target_resources_allowed": targets_allowed,
        "protected_resources_excluded": protected_excluded,
        "no_irreversible_steps": not evidence.irreversible_step_ids,
        "operator_mandate_verified": evidence.operator_mandate_verified,
        "operator_qualification_verified": evidence.operator_qualification_verified,
        "operator_identity_confirmed": evidence.operator_identity_confirmed,
        "conflict_disclosure_complete": evidence.conflict_disclosure_complete,
        "material_conflict_absent": not evidence.material_conflict_present,
        "jurisdiction_verified": evidence.jurisdiction_verified,
        "operator_ready": evidence.operator_ready,
        "start_authorization_acknowledged": evidence.start_authorization_acknowledged,
        "execution_package_integrity_reconfirmed": evidence.execution_package_integrity_reconfirmed,
        "resources_reserved_reconfirmed": evidence.resources_reserved_reconfirmed,
        "rollback_readiness_reconfirmed": evidence.rollback_readiness_reconfirmed,
        "recovery_readiness_reconfirmed": evidence.recovery_readiness_reconfirmed,
        "stop_conditions_reconfirmed": evidence.stop_conditions_reconfirmed,
        "abort_channel_reconfirmed": evidence.abort_channel_reconfirmed,
        "human_oversight_reconfirmed": evidence.human_oversight_reconfirmed,
        "monitoring_reconfirmed": evidence.monitoring_reconfirmed,
        "evidence_capture_reconfirmed": evidence.evidence_capture_reconfirmed,
        "protected_core_excluded": evidence.protected_core_excluded,
        "protected_core_exclusion_reconfirmed": evidence.protected_core_exclusion_reconfirmed,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "institutional_hold_absence_reconfirmed": evidence.institutional_hold_absence_reconfirmed,
        "emergency_state_absent": not evidence.emergency_state_active,
        "emergency_state_absence_reconfirmed": evidence.emergency_state_absence_reconfirmed,
    }
    return checks, expected_digests
