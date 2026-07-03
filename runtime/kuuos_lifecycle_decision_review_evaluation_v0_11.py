from __future__ import annotations

from typing import Any

from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import (
    ISSUED as SOURCE_ISSUED,
    LifecycleBoundedRequestArtifactV010,
    LifecycleBoundedRequestEvidenceV010,
    LifecycleBoundedRequestPolicyV010,
    LifecycleBoundedRequestSubmissionV010,
)
from runtime.kuuos_lifecycle_decision_review_binding_v0_11 import (
    evidence_issues,
    scope_matches,
    submission_issues,
)
from runtime.kuuos_lifecycle_decision_review_policy_v0_11 import policy_issues
from runtime.kuuos_lifecycle_decision_review_source_v0_11 import (
    all_source_digests,
    prior_actor_ids,
    source_recomputed_valid,
)
from runtime.kuuos_lifecycle_decision_review_types_v0_11 import (
    OBJECTIVE,
    LifecycleDecisionReviewEvidenceV011,
    LifecycleDecisionReviewPolicyV011,
    LifecycleDecisionReviewSubmissionV011,
)

STRUCTURAL_CHECKS = (
    "policy_valid",
    "review_valid",
    "evidence_valid",
    "source_recomputed_valid",
    "source_request_issued",
    "source_binding_valid",
    "identity_binding_valid",
    "decision_reviewer_allowed",
    "decision_reviewer_organization_allowed",
    "authorization_decision_maker_allowed",
    "independent_from_prior_chain",
    "independent_from_requester",
    "independent_from_authorization_decision_maker",
    "independent_from_future_operator",
    "authorization_maker_operator_separated",
    "objective_allowed",
    "review_delay_valid",
    "evidence_fresh",
    "time_order_valid",
    "source_request_not_expired",
    "source_package_not_expired",
    "review_not_expired",
    "authorization_deadline_valid",
    "authorization_route_binding_valid",
    "scope_binding_valid",
)

BLOCKING_CHECKS = (
    "reviewer_qualification_verified",
    "reviewer_independence_declared",
    "conflict_disclosure_complete",
    "material_conflict_absent",
    "authorization_route_available",
    "scope_bounded",
    "target_resources_allowed",
    "protected_resources_excluded",
    "no_irreversible_steps",
    "rollback_plan_verified",
    "recovery_route_verified",
    "stop_conditions_complete",
    "abort_channel_available",
    "human_oversight_available",
    "monitoring_plan_complete",
    "evidence_capture_plan_complete",
    "simulation_verified",
    "operation_window_valid",
    "protected_core_excluded",
    "institutional_hold_absent",
    "emergency_state_absent",
    "appeal_route_available",
    "dissent_route_available",
    "minority_opinion_recorded",
)


def evaluate(
    review: LifecycleDecisionReviewSubmissionV011,
    evidence: LifecycleDecisionReviewEvidenceV011,
    policy: LifecycleDecisionReviewPolicyV011,
    source_request: LifecycleBoundedRequestSubmissionV010,
    source_evidence: LifecycleBoundedRequestEvidenceV010,
    source_policy: LifecycleBoundedRequestPolicyV010,
    source_record: LifecycleBoundedRequestArtifactV010,
    source_args: tuple[Any, ...],
) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(
        source_request, source_evidence, source_policy, source_record, source_args
    )
    source_issued = (
        source_record.status == SOURCE_ISSUED
        and source_record.request_record_issued
        and source_record.bounded_request_issued
        and source_record.ready_for_decision_review
        and source_record.decision_review_required_next
        and not source_record.decision_made
        and not source_record.operation_started
        and not source_record.operation_completed
        and not source_record.lifecycle_effect_performed
        and not source_record.repository_change_performed
        and source_record.lifecycle_read_only
    )
    source_binding = (
        (review.subject_id, review.subject_kind, review.subject_version)
        == (evidence.subject_id, evidence.subject_kind, evidence.subject_version)
        == (
            source_request.subject_id,
            source_request.subject_kind,
            source_request.subject_version,
        )
        and review.source_bounded_request_id
        == evidence.source_bounded_request_id
        == source_request.bounded_request_id
        and review.source_bounded_request_record_digest
        == evidence.source_bounded_request_record_digest
        == source_record.record_digest
        and evidence.source_artifact_digests == expected_digests
        and review.requester_id == evidence.requester_id == source_request.requester_id
        and review.authorization_decision_maker_id
        == evidence.authorization_decision_maker_id
        == source_request.decision_authority_id
        and review.future_operator_id
        == evidence.future_operator_id
        == source_request.future_operator_id
    )
    identity_binding = (
        review.decision_review_id == evidence.decision_review_id
        and review.decision_reviewer_id == evidence.decision_reviewer_id
        and review.decision_reviewer_organization_id
        == evidence.decision_reviewer_organization_id
        and review.review_evidence_digest == evidence.evidence_digest
        and review.review_requested_at_epoch_seconds
        == evidence.review_requested_at_epoch_seconds
        and review.completed_at_epoch_seconds == evidence.completed_at_epoch_seconds
        and review.authorization_route_digest == evidence.authorization_route_digest
        and review.authorization_decision_deadline_at_epoch_seconds
        == evidence.authorization_decision_deadline_at_epoch_seconds
    )
    prior_ids = prior_actor_ids(review.subject_id, source_request, source_args)
    delay = review.completed_at_epoch_seconds - source_request.completed_at_epoch_seconds
    age = review.completed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    time_order = (
        evidence.review_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.completed_at_epoch_seconds
        == review.completed_at_epoch_seconds
    )
    preparation_evidence = source_args[5] if len(source_args) > 5 else None
    source_package_not_expired = bool(preparation_evidence) and (
        review.authorization_decision_deadline_at_epoch_seconds
        <= preparation_evidence.package_expiry_at_epoch_seconds
    )
    source_request_not_expired = (
        review.completed_at_epoch_seconds <= source_evidence.request_expiry_at_epoch_seconds
    )
    review_not_expired = (
        review.completed_at_epoch_seconds
        <= evidence.review_expiry_at_epoch_seconds
        <= review.completed_at_epoch_seconds + policy.max_review_expiry_seconds
    )
    authorization_deadline_valid = (
        review.completed_at_epoch_seconds
        < review.authorization_decision_deadline_at_epoch_seconds
        <= evidence.review_expiry_at_epoch_seconds
        <= source_evidence.request_expiry_at_epoch_seconds
    )
    scope_bounded = 0 < len(evidence.operation_scope_items) <= policy.max_scope_items
    targets_allowed = bool(evidence.target_resource_ids) and set(
        evidence.target_resource_ids
    ).issubset(set(policy.allowed_target_resource_ids))
    protected_excluded = not (
        set(evidence.target_resource_ids) & set(evidence.protected_resource_ids)
    )
    window_valid = (
        0 < evidence.operation_window_seconds
        <= policy.max_operation_window_seconds
    )
    checks = {
        "policy_valid": not policy_issues(policy),
        "review_valid": not submission_issues(review),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(
            source_request,
            source_evidence,
            source_policy,
            source_record,
            source_args,
        ),
        "source_request_issued": source_issued,
        "source_binding_valid": source_binding,
        "identity_binding_valid": identity_binding,
        "decision_reviewer_allowed": (
            review.decision_reviewer_id in policy.allowed_decision_reviewer_ids
        ),
        "decision_reviewer_organization_allowed": (
            review.decision_reviewer_organization_id
            in policy.allowed_decision_reviewer_organization_ids
        ),
        "authorization_decision_maker_allowed": (
            review.authorization_decision_maker_id
            in policy.allowed_authorization_decision_maker_ids
        ),
        "reviewer_qualification_verified": evidence.reviewer_qualification_verified,
        "reviewer_independence_declared": evidence.reviewer_independence_declared,
        "independent_from_prior_chain": review.decision_reviewer_id not in prior_ids,
        "independent_from_requester": review.decision_reviewer_id != review.requester_id,
        "independent_from_authorization_decision_maker": (
            review.decision_reviewer_id != review.authorization_decision_maker_id
        ),
        "independent_from_future_operator": (
            review.decision_reviewer_id != review.future_operator_id
        ),
        "authorization_maker_operator_separated": (
            review.authorization_decision_maker_id != review.future_operator_id
        ),
        "objective_allowed": review.objective == OBJECTIVE,
        "review_delay_valid": 0 <= delay <= policy.max_review_delay_seconds,
        "evidence_fresh": 0 <= age <= policy.max_evidence_age_seconds,
        "time_order_valid": time_order,
        "source_request_not_expired": source_request_not_expired,
        "source_package_not_expired": source_package_not_expired,
        "review_not_expired": review_not_expired,
        "authorization_deadline_valid": authorization_deadline_valid,
        "authorization_route_binding_valid": (
            review.authorization_route_digest == evidence.authorization_route_digest
        ),
        "authorization_route_available": evidence.authorization_route_available,
        "conflict_disclosure_complete": evidence.conflict_disclosure_complete,
        "material_conflict_absent": not evidence.material_conflict_present,
        "scope_binding_valid": scope_matches(evidence, source_evidence),
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
        "operation_window_valid": window_valid,
        "protected_core_excluded": evidence.protected_core_excluded,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
        "appeal_route_available": evidence.appeal_route_available,
        "dissent_route_available": evidence.dissent_route_available,
        "minority_opinion_recorded": evidence.minority_opinion_recorded,
    }
    return checks, expected_digests
