from __future__ import annotations

from typing import Any

from runtime.kuuos_lifecycle_transition_preparation_binding_v0_19 import (
    evidence_issues,
    submission_issues,
)
from runtime.kuuos_lifecycle_transition_preparation_package_v0_19 import (
    package_issues,
)
from runtime.kuuos_lifecycle_transition_preparation_policy_v0_19 import (
    policy_issues,
)
from runtime.kuuos_lifecycle_transition_preparation_source_v0_19 import (
    all_source_digests,
    expected_transition_approval_route_digest,
    source_recomputed_valid,
)
from runtime.kuuos_lifecycle_transition_preparation_types_v0_19 import (
    OBJECTIVE,
    LifecycleTransitionPreparationEvidenceV019,
    LifecycleTransitionPreparationPolicyV019,
    LifecycleTransitionPreparationSubmissionV019,
)
from runtime.kuuos_lifecycle_transition_decision_types_v0_18 import (
    APPROVED as SOURCE_APPROVED,
    LifecycleTransitionDecisionArtifactV018,
    LifecycleTransitionDecisionEvidenceV018,
    LifecycleTransitionDecisionPolicyV018,
    LifecycleTransitionDecisionSubmissionV018,
)

STRUCTURAL_CHECKS = (
    "policy_valid",
    "preparation_valid",
    "evidence_valid",
    "package_valid",
    "source_recomputed_valid",
    "source_transition_decision_approved",
    "source_binding_valid",
    "identity_binding_valid",
    "preparer_bound_to_source",
    "preparer_allowed",
    "preparer_organization_allowed",
    "transition_approver_allowed",
    "future_transition_operator_allowed",
    "transition_kind_allowed",
    "action_kinds_allowed",
    "target_resources_allowed",
    "package_step_count_valid",
    "package_execution_window_bounded",
    "preparer_separated_from_prior_actors",
    "preparer_organization_separated",
    "approver_separated_from_preparer",
    "approver_separated_from_decision_maker",
    "approver_separated_from_prior_actors",
    "approver_separated_from_future_operator",
    "future_operator_separated_from_preparer",
    "future_operator_separated_from_decision_maker",
    "future_operator_separated_from_prior_actors",
    "objective_allowed",
    "preparation_delay_valid",
    "evidence_fresh",
    "package_expiry_valid",
    "approval_delay_valid",
    "time_order_valid",
    "source_preparation_deadline_valid",
    "package_source_binding_valid",
    "package_state_binding_valid",
    "package_rule_binding_valid",
    "approval_route_binding_valid",
    "preparer_mandate_verified",
    "preparer_qualification_verified",
    "preparer_identity_confirmed",
    "conflict_disclosure_complete",
    "material_conflict_absent",
    "jurisdiction_verified",
    "preparation_ready",
    "external_operation_absent",
    "repository_change_absent",
)

BLOCKING_CHECKS = (
    "rollback_plan_complete",
    "recovery_plan_complete",
    "monitoring_plan_complete",
    "evidence_capture_plan_complete",
    "resource_reservations_valid",
    "authority_continuity_planned",
    "irreversible_steps_justified",
    "all_steps_bounded",
    "stop_conditions_complete",
    "no_unresolved_anomaly",
    "recovery_not_in_progress",
    "institutional_hold_absent",
    "emergency_state_absent",
)


def _source_approved(record: LifecycleTransitionDecisionArtifactV018) -> bool:
    return all(
        (
            record.status == SOURCE_APPROVED,
            record.transition_decision_record_issued,
            record.transition_decision_made,
            record.transition_approved_for_preparation,
            not record.transition_denied,
            record.transition_preparation_required_next,
            record.transition_preparation_route_required_next,
            not record.transition_appeal_or_reconsideration_available,
            not record.lifecycle_transition_prepared,
            not record.lifecycle_transition_approved,
            not record.lifecycle_transition_started,
            not record.lifecycle_transition_completed,
            not record.lifecycle_transition_performed,
            not record.authority_changed,
            not record.quiescence_state_changed,
            not record.terminal_state_changed,
            not record.terminal_marker_written,
            not record.resource_removed,
            not record.external_operation_performed,
            not record.repository_changed,
            record.lifecycle_state_read_only,
            record.repository_read_only,
        )
    )


def evaluate(
    preparation: LifecycleTransitionPreparationSubmissionV019,
    evidence: LifecycleTransitionPreparationEvidenceV019,
    policy: LifecycleTransitionPreparationPolicyV019,
    source_decision: LifecycleTransitionDecisionSubmissionV018,
    source_evidence: LifecycleTransitionDecisionEvidenceV018,
    source_policy: LifecycleTransitionDecisionPolicyV018,
    source_record: LifecycleTransitionDecisionArtifactV018,
    source_args: tuple[Any, ...],
) -> tuple[dict[str, bool], dict[str, str]]:
    package = evidence.transition_package
    expected_digests = all_source_digests(
        source_decision,
        source_evidence,
        source_policy,
        source_record,
        source_args,
    )
    source_binding = all(
        (
            preparation.source_transition_decision_id
            == evidence.source_transition_decision_id
            == source_decision.transition_decision_id,
            preparation.source_transition_decision_record_digest
            == evidence.source_transition_decision_record_digest
            == source_record.record_digest,
            evidence.source_artifact_digests == expected_digests,
            preparation.source_transition_decision_maker_id
            == evidence.source_transition_decision_maker_id
            == source_decision.transition_decision_maker_id,
            evidence.source_transition_decision_maker_organization_id
            == source_decision.transition_decision_maker_organization_id,
            preparation.subject_id
            == evidence.subject_id
            == source_decision.subject_id,
            preparation.subject_kind
            == evidence.subject_kind
            == source_decision.subject_kind,
            preparation.subject_version
            == evidence.subject_version
            == source_decision.subject_version,
            preparation.requester_id
            == evidence.requester_id
            == source_decision.requester_id,
        )
    )
    identity_binding = all(
        (
            preparation.transition_preparation_id
            == evidence.transition_preparation_id,
            preparation.transition_preparer_id == evidence.transition_preparer_id,
            preparation.transition_preparer_organization_id
            == evidence.transition_preparer_organization_id,
            preparation.transition_preparation_evidence_digest
            == evidence.evidence_digest,
            preparation.transition_approver_id == evidence.transition_approver_id,
            preparation.future_transition_operator_id
            == evidence.future_transition_operator_id,
            preparation.transition_package_digest == package.package_digest,
            preparation.expected_current_lifecycle_state_digest
            == package.expected_current_lifecycle_state_digest,
            preparation.proposed_target_lifecycle_state_digest
            == package.proposed_target_lifecycle_state_digest,
            preparation.transition_approval_route_digest
            == evidence.transition_approval_route_digest,
            preparation.preparation_requested_at_epoch_seconds
            == evidence.preparation_requested_at_epoch_seconds,
            preparation.prepared_at_epoch_seconds
            == evidence.prepared_at_epoch_seconds,
            preparation.package_expiry_at_epoch_seconds
            == evidence.package_expiry_at_epoch_seconds,
            preparation.transition_approval_deadline_at_epoch_seconds
            == evidence.transition_approval_deadline_at_epoch_seconds,
        )
    )
    expected_route = expected_transition_approval_route_digest(
        source_decision,
        source_record,
        transition_package_digest=package.package_digest,
        transition_approver_id=evidence.transition_approver_id,
        future_transition_operator_id=evidence.future_transition_operator_id,
        expected_current_lifecycle_state_digest=(
            package.expected_current_lifecycle_state_digest
        ),
        proposed_target_lifecycle_state_digest=(
            package.proposed_target_lifecycle_state_digest
        ),
        transition_approval_deadline_at_epoch_seconds=(
            evidence.transition_approval_deadline_at_epoch_seconds
        ),
    )
    prior_without_preparer = {
        evidence.subject_id,
        evidence.requester_id,
        evidence.source_decision_reviewer_id,
        evidence.source_authorization_decision_maker_id,
        evidence.source_operation_approver_id,
        evidence.source_operator_id,
        evidence.source_completion_reviewer_id,
        evidence.source_post_operation_reviewer_id,
        evidence.source_transition_reviewer_id,
        evidence.source_transition_decision_maker_id,
    }
    all_prior = prior_without_preparer | {source_decision.transition_preparer_id}
    preparation_delay = (
        evidence.prepared_at_epoch_seconds - source_decision.decided_at_epoch_seconds
    )
    evidence_age = (
        evidence.prepared_at_epoch_seconds - evidence.captured_at_epoch_seconds
    )
    expiry_span = (
        evidence.package_expiry_at_epoch_seconds - evidence.prepared_at_epoch_seconds
    )
    approval_delay = (
        evidence.transition_approval_deadline_at_epoch_seconds
        - evidence.prepared_at_epoch_seconds
    )
    execution_window_span = (
        package.execution_window_end_epoch_seconds
        - package.execution_window_start_epoch_seconds
    )
    time_order = (
        source_decision.decided_at_epoch_seconds
        <= evidence.preparation_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.prepared_at_epoch_seconds
        < evidence.transition_approval_deadline_at_epoch_seconds
        <= package.execution_window_start_epoch_seconds
        < package.execution_window_end_epoch_seconds
        <= evidence.package_expiry_at_epoch_seconds
    )
    checks = {
        "policy_valid": not policy_issues(policy),
        "preparation_valid": not submission_issues(preparation),
        "evidence_valid": not evidence_issues(evidence),
        "package_valid": not package_issues(package),
        "source_recomputed_valid": source_recomputed_valid(
            source_decision,
            source_evidence,
            source_policy,
            source_record,
            source_args,
        ),
        "source_transition_decision_approved": _source_approved(source_record),
        "source_binding_valid": source_binding,
        "identity_binding_valid": identity_binding,
        "preparer_bound_to_source": (
            preparation.transition_preparer_id
            == source_decision.transition_preparer_id
        ),
        "preparer_allowed": (
            preparation.transition_preparer_id
            in policy.allowed_transition_preparer_ids
        ),
        "preparer_organization_allowed": (
            preparation.transition_preparer_organization_id
            in policy.allowed_transition_preparer_organization_ids
        ),
        "transition_approver_allowed": (
            preparation.transition_approver_id
            in policy.allowed_transition_approver_ids
        ),
        "future_transition_operator_allowed": (
            preparation.future_transition_operator_id
            in policy.allowed_future_transition_operator_ids
        ),
        "transition_kind_allowed": (
            package.transition_kind in policy.allowed_transition_kinds
        ),
        "action_kinds_allowed": all(
            step.action_kind in policy.allowed_action_kinds
            for step in package.steps
        ),
        "target_resources_allowed": all(
            step.target_resource_id in policy.allowed_target_resource_ids
            for step in package.steps
        ),
        "package_step_count_valid": 0 < len(package.steps) <= policy.max_steps,
        "package_execution_window_bounded": (
            0 < execution_window_span <= policy.max_execution_window_seconds
        ),
        "preparer_separated_from_prior_actors": (
            preparation.transition_preparer_id not in prior_without_preparer
        ),
        "preparer_organization_separated": (
            preparation.transition_preparer_organization_id
            != evidence.source_transition_decision_maker_organization_id
        ),
        "approver_separated_from_preparer": (
            preparation.transition_approver_id
            != preparation.transition_preparer_id
        ),
        "approver_separated_from_decision_maker": (
            preparation.transition_approver_id
            != evidence.source_transition_decision_maker_id
        ),
        "approver_separated_from_prior_actors": (
            preparation.transition_approver_id not in all_prior
        ),
        "approver_separated_from_future_operator": (
            preparation.transition_approver_id
            != preparation.future_transition_operator_id
        ),
        "future_operator_separated_from_preparer": (
            preparation.future_transition_operator_id
            != preparation.transition_preparer_id
        ),
        "future_operator_separated_from_decision_maker": (
            preparation.future_transition_operator_id
            != evidence.source_transition_decision_maker_id
        ),
        "future_operator_separated_from_prior_actors": (
            preparation.future_transition_operator_id not in all_prior
        ),
        "objective_allowed": preparation.objective == OBJECTIVE,
        "preparation_delay_valid": (
            0 <= preparation_delay <= policy.max_preparation_delay_seconds
        ),
        "evidence_fresh": (
            0 <= evidence_age <= policy.max_evidence_age_seconds
        ),
        "package_expiry_valid": (
            0 < expiry_span <= policy.max_package_expiry_seconds
        ),
        "approval_delay_valid": (
            0 < approval_delay <= policy.max_approval_delay_seconds
        ),
        "time_order_valid": time_order,
        "source_preparation_deadline_valid": (
            evidence.prepared_at_epoch_seconds
            <= source_decision.transition_preparation_deadline_at_epoch_seconds
        ),
        "package_source_binding_valid": (
            package.source_transition_decision_id
            == source_decision.transition_decision_id
        ),
        "package_state_binding_valid": (
            package.expected_current_lifecycle_state_digest
            == source_record.expected_current_lifecycle_state_digest
            and package.proposed_target_lifecycle_state_digest
            == source_record.proposed_target_lifecycle_state_digest
        ),
        "package_rule_binding_valid": (
            package.transition_rule_digest == source_record.transition_rule_digest
            and package.transition_kind == source_record.proposed_transition_kind
        ),
        "approval_route_binding_valid": (
            preparation.transition_approval_route_digest
            == evidence.transition_approval_route_digest
            == expected_route
        ),
        "preparer_mandate_verified": evidence.preparer_mandate_verified,
        "preparer_qualification_verified": evidence.preparer_qualification_verified,
        "preparer_identity_confirmed": evidence.preparer_identity_confirmed,
        "conflict_disclosure_complete": evidence.conflict_disclosure_complete,
        "material_conflict_absent": not evidence.material_conflict_present,
        "jurisdiction_verified": evidence.jurisdiction_verified,
        "preparation_ready": evidence.preparation_ready,
        "external_operation_absent": not evidence.external_operation_performed,
        "repository_change_absent": not evidence.repository_changed,
        "rollback_plan_complete": evidence.rollback_plan_complete,
        "recovery_plan_complete": evidence.recovery_plan_complete,
        "monitoring_plan_complete": evidence.monitoring_plan_complete,
        "evidence_capture_plan_complete": evidence.evidence_capture_plan_complete,
        "resource_reservations_valid": evidence.resource_reservations_valid,
        "authority_continuity_planned": evidence.authority_continuity_planned,
        "irreversible_steps_justified": evidence.irreversible_steps_justified,
        "all_steps_bounded": evidence.all_steps_bounded,
        "stop_conditions_complete": evidence.stop_conditions_complete,
        "no_unresolved_anomaly": not evidence.unresolved_anomaly_present,
        "recovery_not_in_progress": not evidence.recovery_in_progress,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests
