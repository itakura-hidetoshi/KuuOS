from __future__ import annotations

from typing import Any

from runtime.kuuos_lifecycle_review_types_v0_9 import (
    CLEAR as SOURCE_CLEAR,
    LifecycleReviewArtifactV09,
    LifecycleReviewEvidenceV09,
    LifecycleReviewPolicyV09,
    LifecycleReviewRequestV09,
)
from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import (
    OBJECTIVE,
    LifecycleBoundedRequestEvidenceV010,
    LifecycleBoundedRequestPolicyV010,
    LifecycleBoundedRequestSubmissionV010,
)
from runtime.kuuos_lifecycle_request_binding_v0_10 import (
    evidence_issues,
    scope_matches,
    submission_issues,
)
from runtime.kuuos_lifecycle_request_policy_v0_10 import policy_issues
from runtime.kuuos_lifecycle_source_chain_v0_10 import (
    all_source_digests,
    prior_actor_ids,
    source_authority,
    source_operator,
    source_recomputed_valid,
)


STRUCTURAL_CHECKS = (
    "policy_valid",
    "request_valid",
    "evidence_valid",
    "source_recomputed_valid",
    "source_review_clear",
    "source_binding_valid",
    "identity_binding_valid",
    "requester_allowed",
    "requester_organization_allowed",
    "decision_authority_allowed",
    "independent_from_prior_chain",
    "independent_from_decision_authority",
    "independent_from_future_operator",
    "authority_operator_separated",
    "objective_allowed",
    "request_delay_valid",
    "evidence_fresh",
    "time_order_valid",
    "source_package_not_expired",
    "source_review_not_expired",
    "request_not_expired",
    "decision_deadline_valid",
    "decision_route_binding_valid",
    "scope_binding_valid",
)

BLOCKING_CHECKS = (
    "requester_qualification_verified",
    "requester_independence_declared",
    "decision_route_available",
    "conflict_disclosure_complete",
    "material_conflict_absent",
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
)


def evaluate(
    request: LifecycleBoundedRequestSubmissionV010,
    evidence: LifecycleBoundedRequestEvidenceV010,
    policy: LifecycleBoundedRequestPolicyV010,
    review_request: LifecycleReviewRequestV09,
    review_evidence: LifecycleReviewEvidenceV09,
    review_policy: LifecycleReviewPolicyV09,
    review_record: LifecycleReviewArtifactV09,
    source_args: tuple[Any, ...],
) -> tuple[dict[str, bool], dict[str, str]]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    preparation_evidence = source_args[1]
    expected_digests = all_source_digests(
        review_request,
        review_evidence,
        review_policy,
        review_record,
        source_args,
    )
    source_clear = (
        review_record.status == SOURCE_CLEAR
        and review_record.review_record_issued
        and review_record.review_completed
        and review_record.clear_for_next_request_layer
        and review_record.next_request_layer_required
        and review_record.effect_free
        and review_record.read_only
    )
    source_binding = (
        (request.subject_id, request.subject_kind, request.subject_version)
        == (evidence.subject_id, evidence.subject_kind, evidence.subject_version)
        == (
            review_request.subject_id,
            review_request.subject_kind,
            review_request.subject_version,
        )
        and request.source_review_id
        == evidence.source_review_id
        == review_record.review_id
        and request.source_review_record_digest
        == evidence.source_review_record_digest
        == review_record.record_digest
        and evidence.source_artifact_digests == expected_digests
        and request.decision_authority_id
        == evidence.decision_authority_id
        == source_authority(review_record)
        and request.future_operator_id
        == evidence.future_operator_id
        == source_operator(review_record)
    )
    identity_binding = (
        request.bounded_request_id == evidence.bounded_request_id
        and request.requester_id == evidence.requester_id
        and request.requester_organization_id == evidence.requester_organization_id
        and request.request_evidence_digest == evidence.evidence_digest
        and request.requested_at_epoch_seconds == evidence.requested_at_epoch_seconds
        and request.completed_at_epoch_seconds == evidence.completed_at_epoch_seconds
        and request.decision_route_digest == evidence.decision_route_digest
        and request.decision_deadline_at_epoch_seconds
        == evidence.decision_deadline_at_epoch_seconds
    )
    prior_ids = prior_actor_ids(request.subject_id, review_record, source_args)
    time_order = (
        evidence.requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.completed_at_epoch_seconds
        == request.completed_at_epoch_seconds
    )
    delay = request.completed_at_epoch_seconds - review_evidence.completed_at_epoch_seconds
    age = request.completed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    source_package_not_expired = (
        request.decision_deadline_at_epoch_seconds
        <= preparation_evidence.package_expiry_at_epoch_seconds
    )
    source_review_not_expired = (
        request.completed_at_epoch_seconds
        <= review_evidence.review_expiry_at_epoch_seconds
    )
    request_not_expired = (
        request.completed_at_epoch_seconds
        <= evidence.request_expiry_at_epoch_seconds
        <= request.completed_at_epoch_seconds + policy.max_request_expiry_seconds
    )
    deadline_valid = (
        request.completed_at_epoch_seconds
        < request.decision_deadline_at_epoch_seconds
        <= evidence.request_expiry_at_epoch_seconds
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
        "request_valid": not submission_issues(request),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(
            review_request,
            review_evidence,
            review_policy,
            review_record,
            source_args,
        ),
        "source_review_clear": source_clear,
        "source_binding_valid": source_binding,
        "identity_binding_valid": identity_binding,
        "requester_allowed": request.requester_id in policy.allowed_requester_ids,
        "requester_organization_allowed": (
            request.requester_organization_id
            in policy.allowed_requester_organization_ids
        ),
        "decision_authority_allowed": (
            request.decision_authority_id in policy.allowed_decision_authority_ids
        ),
        "requester_qualification_verified": evidence.requester_qualification_verified,
        "requester_independence_declared": evidence.requester_independence_declared,
        "independent_from_prior_chain": request.requester_id not in prior_ids,
        "independent_from_decision_authority": (
            request.requester_id != request.decision_authority_id
        ),
        "independent_from_future_operator": (
            request.requester_id != request.future_operator_id
        ),
        "authority_operator_separated": (
            request.decision_authority_id != request.future_operator_id
        ),
        "objective_allowed": request.objective == OBJECTIVE,
        "request_delay_valid": 0 <= delay <= policy.max_request_delay_seconds,
        "evidence_fresh": 0 <= age <= policy.max_evidence_age_seconds,
        "time_order_valid": time_order,
        "source_package_not_expired": source_package_not_expired,
        "source_review_not_expired": source_review_not_expired,
        "request_not_expired": request_not_expired,
        "decision_deadline_valid": deadline_valid,
        "decision_route_binding_valid": (
            request.decision_route_digest == evidence.decision_route_digest
        ),
        "decision_route_available": evidence.decision_route_available,
        "conflict_disclosure_complete": evidence.conflict_disclosure_complete,
        "material_conflict_absent": not evidence.material_conflict_present,
        "scope_binding_valid": scope_matches(evidence, review_evidence),
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
    }
    return checks, expected_digests
