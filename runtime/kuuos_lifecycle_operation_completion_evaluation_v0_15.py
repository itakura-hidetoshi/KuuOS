from __future__ import annotations

from typing import Any

from runtime.kuuos_lifecycle_operation_start_types_v0_14 import (
    STARTED as SOURCE_STARTED,
    LifecycleOperationStartArtifactV014,
    LifecycleOperationStartEvidenceV014,
    LifecycleOperationStartPolicyV014,
    LifecycleOperationStartSubmissionV014,
)
from runtime.kuuos_lifecycle_operation_completion_binding_v0_15 import (
    evidence_issues,
    scope_matches,
    submission_issues,
)
from runtime.kuuos_lifecycle_operation_completion_policy_v0_15 import (
    policy_issues,
)
from runtime.kuuos_lifecycle_operation_completion_source_v0_15 import (
    all_source_digests,
    expected_operation_completion_route_digest,
    source_recomputed_valid,
)
from runtime.kuuos_lifecycle_operation_completion_types_v0_15 import (
    OBJECTIVE,
    LifecycleOperationCompletionEvidenceV015,
    LifecycleOperationCompletionPolicyV015,
    LifecycleOperationCompletionSubmissionV015,
)

STRUCTURAL_CHECKS = (
    "policy_valid",
    "completion_valid",
    "evidence_valid",
    "source_recomputed_valid",
    "source_operation_started",
    "source_binding_valid",
    "identity_binding_valid",
    "completion_reviewer_allowed",
    "completion_reviewer_organization_allowed",
    "completion_reviewer_separated_from_operator",
    "completion_reviewer_separated_from_requester",
    "completion_reviewer_separated_from_source_decision_reviewer",
    "completion_reviewer_separated_from_authorization_decision_maker",
    "completion_reviewer_separated_from_operation_approver",
    "completion_reviewer_separated_from_subject",
    "objective_allowed",
    "completion_delay_valid",
    "evidence_fresh",
    "time_order_valid",
    "operation_completion_deadline_valid",
    "operation_completion_route_binding_valid",
    "scope_binding_valid",
    "scope_bounded",
    "target_resources_allowed",
    "protected_resources_excluded",
    "no_irreversible_steps",
    "step_results_exactly_bound",
    "external_operation_absent",
    "repository_change_absent",
)

DENIAL_CHECKS = (
    "completion_reviewer_mandate_verified",
    "completion_reviewer_qualification_verified",
    "completion_reviewer_identity_confirmed",
    "conflict_disclosure_complete",
    "material_conflict_absent",
    "jurisdiction_verified",
    "completion_ready",
    "operation_execution_finished",
    "execution_result_integrity_verified",
    "all_scope_items_accounted",
    "all_reversible_steps_accounted",
    "target_post_state_verified",
    "protected_resources_intact",
    "protected_core_intact",
    "resource_reservations_released",
    "monitoring_completed",
    "evidence_capture_completed",
    "no_unresolved_stop_condition",
    "abort_not_triggered",
    "rollback_not_pending",
    "recovery_not_pending",
)


def evaluate(
    completion: LifecycleOperationCompletionSubmissionV015,
    evidence: LifecycleOperationCompletionEvidenceV015,
    policy: LifecycleOperationCompletionPolicyV015,
    source_start: LifecycleOperationStartSubmissionV014,
    source_evidence: LifecycleOperationStartEvidenceV014,
    source_policy: LifecycleOperationStartPolicyV014,
    source_record: LifecycleOperationStartArtifactV014,
    source_args: tuple[Any, ...],
) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(
        source_start,
        source_evidence,
        source_policy,
        source_record,
        source_args,
    )
    source_started = (
        source_record.status == SOURCE_STARTED
        and source_record.operation_start_record_issued
        and source_record.operation_start_decision_made
        and source_record.operation_started
        and not source_record.operation_start_denied
        and source_record.operation_completion_required_next
        and source_record.operation_completion_route_required_next
        and not source_record.operation_completed
        and not source_record.authority_changed
        and not source_record.quiescence_state_changed
        and not source_record.terminal_state_changed
        and not source_record.terminal_marker_written
        and not source_record.resource_removed
        and not source_record.external_operation_performed
        and not source_record.repository_changed
        and source_record.lifecycle_state_read_only
        and source_record.repository_read_only
    )
    source_binding = (
        (
            completion.subject_id,
            completion.subject_kind,
            completion.subject_version,
        )
        == (
            evidence.subject_id,
            evidence.subject_kind,
            evidence.subject_version,
        )
        == (
            source_start.subject_id,
            source_start.subject_kind,
            source_start.subject_version,
        )
        and completion.source_operation_start_id
        == evidence.source_operation_start_id
        == source_start.operation_start_id
        and completion.source_operation_start_record_digest
        == evidence.source_operation_start_record_digest
        == source_record.record_digest
        and evidence.source_artifact_digests == expected_digests
        and completion.requester_id
        == evidence.requester_id
        == source_start.requester_id
        and completion.source_operator_id
        == evidence.source_operator_id
        == source_start.operator_id
        and evidence.source_operator_organization_id
        == source_start.operator_organization_id
        and completion.source_operation_approver_id
        == evidence.source_operation_approver_id
        == source_start.source_operation_approver_id
        and completion.source_authorization_decision_maker_id
        == evidence.source_authorization_decision_maker_id
        == source_start.source_authorization_decision_maker_id
        and completion.source_decision_reviewer_id
        == evidence.source_decision_reviewer_id
        == source_start.source_decision_reviewer_id
    )
    identity_binding = (
        completion.operation_completion_id
        == evidence.operation_completion_id
        and completion.completion_reviewer_id
        == evidence.completion_reviewer_id
        and completion.completion_reviewer_organization_id
        == evidence.completion_reviewer_organization_id
        and completion.completion_evidence_digest
        == evidence.evidence_digest
        and completion.completion_requested_at_epoch_seconds
        == evidence.completion_requested_at_epoch_seconds
        and completion.completed_at_epoch_seconds
        == evidence.completed_at_epoch_seconds
        and completion.operation_completion_route_digest
        == evidence.operation_completion_route_digest
    )
    delay = (
        completion.completed_at_epoch_seconds
        - source_start.started_at_epoch_seconds
    )
    age = (
        completion.completed_at_epoch_seconds
        - evidence.captured_at_epoch_seconds
    )
    time_order = (
        source_start.started_at_epoch_seconds
        <= evidence.completion_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.completed_at_epoch_seconds
        == completion.completed_at_epoch_seconds
    )
    deadline_valid = (
        completion.completed_at_epoch_seconds
        <= evidence.operation_completion_deadline_at_epoch_seconds
        == source_start.operation_completion_deadline_at_epoch_seconds
    )
    expected_route = expected_operation_completion_route_digest(
        source_start, source_evidence, source_record
    )
    scope_bounded = (
        0 < len(evidence.operation_scope_items) <= policy.max_scope_items
    )
    targets_allowed = bool(evidence.target_resource_ids) and set(
        evidence.target_resource_ids
    ).issubset(set(policy.allowed_target_resource_ids))
    protected_excluded = not (
        set(evidence.target_resource_ids)
        & set(evidence.protected_resource_ids)
    )
    step_results_bound = (
        set(evidence.step_result_digests)
        == set(evidence.reversible_step_ids)
    )
    checks = {
        "policy_valid": not policy_issues(policy),
        "completion_valid": not submission_issues(completion),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(
            source_start,
            source_evidence,
            source_policy,
            source_record,
            source_args,
        ),
        "source_operation_started": source_started,
        "source_binding_valid": source_binding,
        "identity_binding_valid": identity_binding,
        "completion_reviewer_allowed": (
            completion.completion_reviewer_id
            in policy.allowed_completion_reviewer_ids
        ),
        "completion_reviewer_organization_allowed": (
            completion.completion_reviewer_organization_id
            in policy.allowed_completion_reviewer_organization_ids
        ),
        "completion_reviewer_separated_from_operator": (
            completion.completion_reviewer_id
            != completion.source_operator_id
        ),
        "completion_reviewer_separated_from_requester": (
            completion.completion_reviewer_id != completion.requester_id
        ),
        "completion_reviewer_separated_from_source_decision_reviewer": (
            completion.completion_reviewer_id
            != completion.source_decision_reviewer_id
        ),
        "completion_reviewer_separated_from_authorization_decision_maker": (
            completion.completion_reviewer_id
            != completion.source_authorization_decision_maker_id
        ),
        "completion_reviewer_separated_from_operation_approver": (
            completion.completion_reviewer_id
            != completion.source_operation_approver_id
        ),
        "completion_reviewer_separated_from_subject": (
            completion.completion_reviewer_id != completion.subject_id
        ),
        "objective_allowed": completion.objective == OBJECTIVE,
        "completion_delay_valid": (
            0 <= delay <= policy.max_completion_delay_seconds
        ),
        "evidence_fresh": (
            0 <= age <= policy.max_evidence_age_seconds
        ),
        "time_order_valid": time_order,
        "operation_completion_deadline_valid": deadline_valid,
        "operation_completion_route_binding_valid": (
            completion.operation_completion_route_digest
            == evidence.operation_completion_route_digest
            == expected_route
        ),
        "scope_binding_valid": scope_matches(evidence, source_evidence),
        "scope_bounded": scope_bounded,
        "target_resources_allowed": targets_allowed,
        "protected_resources_excluded": protected_excluded,
        "no_irreversible_steps": not evidence.irreversible_step_ids,
        "step_results_exactly_bound": step_results_bound,
        "external_operation_absent": (
            not evidence.external_operation_performed
        ),
        "repository_change_absent": not evidence.repository_changed,
        "completion_reviewer_mandate_verified": (
            evidence.completion_reviewer_mandate_verified
        ),
        "completion_reviewer_qualification_verified": (
            evidence.completion_reviewer_qualification_verified
        ),
        "completion_reviewer_identity_confirmed": (
            evidence.completion_reviewer_identity_confirmed
        ),
        "conflict_disclosure_complete": (
            evidence.conflict_disclosure_complete
        ),
        "material_conflict_absent": (
            not evidence.material_conflict_present
        ),
        "jurisdiction_verified": evidence.jurisdiction_verified,
        "completion_ready": evidence.completion_ready,
        "operation_execution_finished": (
            evidence.operation_execution_finished
        ),
        "execution_result_integrity_verified": (
            evidence.execution_result_integrity_verified
        ),
        "all_scope_items_accounted": (
            evidence.all_scope_items_accounted
        ),
        "all_reversible_steps_accounted": (
            evidence.all_reversible_steps_accounted
        ),
        "target_post_state_verified": (
            evidence.target_post_state_verified
        ),
        "protected_resources_intact": (
            evidence.protected_resources_intact
        ),
        "protected_core_intact": evidence.protected_core_intact,
        "resource_reservations_released": (
            evidence.resource_reservations_released
        ),
        "monitoring_completed": evidence.monitoring_completed,
        "evidence_capture_completed": (
            evidence.evidence_capture_completed
        ),
        "no_unresolved_stop_condition": (
            not evidence.unresolved_stop_condition_present
        ),
        "abort_not_triggered": not evidence.abort_triggered,
        "rollback_not_pending": not evidence.rollback_pending,
        "recovery_not_pending": not evidence.recovery_pending,
    }
    return checks, expected_digests
