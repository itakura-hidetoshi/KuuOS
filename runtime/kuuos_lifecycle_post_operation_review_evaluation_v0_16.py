from __future__ import annotations

from typing import Any

from runtime.kuuos_lifecycle_operation_completion_types_v0_15 import (
    COMPLETED as SOURCE_COMPLETED,
    LifecycleOperationCompletionArtifactV015,
    LifecycleOperationCompletionEvidenceV015,
    LifecycleOperationCompletionPolicyV015,
    LifecycleOperationCompletionSubmissionV015,
)
from runtime.kuuos_lifecycle_post_operation_review_binding_v0_16 import (
    evidence_issues,
    scope_matches,
    submission_issues,
)
from runtime.kuuos_lifecycle_post_operation_review_policy_v0_16 import (
    policy_issues,
)
from runtime.kuuos_lifecycle_post_operation_review_source_v0_16 import (
    all_source_digests,
    expected_post_operation_review_route_digest,
    source_recomputed_valid,
)
from runtime.kuuos_lifecycle_post_operation_review_types_v0_16 import (
    OBJECTIVE,
    LifecyclePostOperationReviewEvidenceV016,
    LifecyclePostOperationReviewPolicyV016,
    LifecyclePostOperationReviewSubmissionV016,
)

STRUCTURAL_CHECKS = (
    "policy_valid",
    "review_valid",
    "evidence_valid",
    "source_recomputed_valid",
    "source_operation_completed",
    "source_binding_valid",
    "identity_binding_valid",
    "post_operation_reviewer_allowed",
    "post_operation_reviewer_organization_allowed",
    "post_operation_reviewer_separated_from_completion_reviewer",
    "post_operation_reviewer_separated_from_operator",
    "post_operation_reviewer_separated_from_requester",
    "post_operation_reviewer_separated_from_source_decision_reviewer",
    "post_operation_reviewer_separated_from_authorization_decision_maker",
    "post_operation_reviewer_separated_from_operation_approver",
    "post_operation_reviewer_separated_from_subject",
    "post_operation_reviewer_organization_separated",
    "objective_allowed",
    "review_delay_valid",
    "evidence_fresh",
    "time_order_valid",
    "post_operation_review_route_binding_valid",
    "scope_binding_valid",
    "scope_bounded",
    "target_resources_allowed",
    "protected_resources_excluded",
    "external_operation_absent",
    "repository_change_absent",
)

DENIAL_CHECKS = (
    "post_operation_reviewer_mandate_verified",
    "post_operation_reviewer_qualification_verified",
    "post_operation_reviewer_identity_confirmed",
    "conflict_disclosure_complete",
    "material_conflict_absent",
    "jurisdiction_verified",
    "review_ready",
    "intended_result_matches_observed",
    "target_post_state_verified",
    "collateral_effects_absent",
    "protected_resources_intact",
    "protected_core_intact",
    "monitoring_evidence_sufficient",
    "completion_evidence_sufficient",
    "no_unresolved_anomaly",
    "rollback_not_required",
    "recovery_not_required",
)


def evaluate(
    review: LifecyclePostOperationReviewSubmissionV016,
    evidence: LifecyclePostOperationReviewEvidenceV016,
    policy: LifecyclePostOperationReviewPolicyV016,
    source_completion: LifecycleOperationCompletionSubmissionV015,
    source_evidence: LifecycleOperationCompletionEvidenceV015,
    source_policy: LifecycleOperationCompletionPolicyV015,
    source_record: LifecycleOperationCompletionArtifactV015,
    source_args: tuple[Any, ...],
) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(
        source_completion,
        source_evidence,
        source_policy,
        source_record,
        source_args,
    )
    source_completed = (
        source_record.status == SOURCE_COMPLETED
        and source_record.operation_started
        and source_record.operation_completion_record_issued
        and source_record.operation_completion_decision_made
        and source_record.operation_completed
        and not source_record.operation_completion_denied
        and source_record.post_operation_review_required_next
        and source_record.post_operation_review_route_required_next
        and not source_record.operation_recovery_required_next
        and not source_record.operation_recovery_route_required_next
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
            review.subject_id,
            review.subject_kind,
            review.subject_version,
        )
        == (
            evidence.subject_id,
            evidence.subject_kind,
            evidence.subject_version,
        )
        == (
            source_completion.subject_id,
            source_completion.subject_kind,
            source_completion.subject_version,
        )
        and review.source_operation_completion_id
        == evidence.source_operation_completion_id
        == source_completion.operation_completion_id
        and review.source_operation_completion_record_digest
        == evidence.source_operation_completion_record_digest
        == source_record.record_digest
        and evidence.source_artifact_digests == expected_digests
        and review.requester_id
        == evidence.requester_id
        == source_completion.requester_id
        and review.source_completion_reviewer_id
        == evidence.source_completion_reviewer_id
        == source_completion.completion_reviewer_id
        and evidence.source_completion_reviewer_organization_id
        == source_completion.completion_reviewer_organization_id
        and review.source_operator_id
        == evidence.source_operator_id
        == source_completion.source_operator_id
        and review.source_operation_approver_id
        == evidence.source_operation_approver_id
        == source_completion.source_operation_approver_id
        and review.source_authorization_decision_maker_id
        == evidence.source_authorization_decision_maker_id
        == source_completion.source_authorization_decision_maker_id
        and review.source_decision_reviewer_id
        == evidence.source_decision_reviewer_id
        == source_completion.source_decision_reviewer_id
    )
    identity_binding = (
        review.post_operation_review_id
        == evidence.post_operation_review_id
        and review.post_operation_reviewer_id
        == evidence.post_operation_reviewer_id
        and review.post_operation_reviewer_organization_id
        == evidence.post_operation_reviewer_organization_id
        and review.post_operation_review_evidence_digest
        == evidence.evidence_digest
        and review.review_requested_at_epoch_seconds
        == evidence.review_requested_at_epoch_seconds
        and review.reviewed_at_epoch_seconds
        == evidence.reviewed_at_epoch_seconds
        and review.post_operation_review_route_digest
        == evidence.post_operation_review_route_digest
    )
    delay = (
        review.reviewed_at_epoch_seconds
        - source_completion.completed_at_epoch_seconds
    )
    age = (
        review.reviewed_at_epoch_seconds
        - evidence.captured_at_epoch_seconds
    )
    time_order = (
        source_completion.completed_at_epoch_seconds
        <= evidence.review_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.reviewed_at_epoch_seconds
        == review.reviewed_at_epoch_seconds
    )
    expected_route = expected_post_operation_review_route_digest(
        source_completion, source_evidence, source_record
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
    checks = {
        "policy_valid": not policy_issues(policy),
        "review_valid": not submission_issues(review),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(
            source_completion,
            source_evidence,
            source_policy,
            source_record,
            source_args,
        ),
        "source_operation_completed": source_completed,
        "source_binding_valid": source_binding,
        "identity_binding_valid": identity_binding,
        "post_operation_reviewer_allowed": (
            review.post_operation_reviewer_id
            in policy.allowed_post_operation_reviewer_ids
        ),
        "post_operation_reviewer_organization_allowed": (
            review.post_operation_reviewer_organization_id
            in policy.allowed_post_operation_reviewer_organization_ids
        ),
        "post_operation_reviewer_separated_from_completion_reviewer": (
            review.post_operation_reviewer_id
            != review.source_completion_reviewer_id
        ),
        "post_operation_reviewer_separated_from_operator": (
            review.post_operation_reviewer_id != review.source_operator_id
        ),
        "post_operation_reviewer_separated_from_requester": (
            review.post_operation_reviewer_id != review.requester_id
        ),
        "post_operation_reviewer_separated_from_source_decision_reviewer": (
            review.post_operation_reviewer_id
            != review.source_decision_reviewer_id
        ),
        "post_operation_reviewer_separated_from_authorization_decision_maker": (
            review.post_operation_reviewer_id
            != review.source_authorization_decision_maker_id
        ),
        "post_operation_reviewer_separated_from_operation_approver": (
            review.post_operation_reviewer_id
            != review.source_operation_approver_id
        ),
        "post_operation_reviewer_separated_from_subject": (
            review.post_operation_reviewer_id != review.subject_id
        ),
        "post_operation_reviewer_organization_separated": (
            review.post_operation_reviewer_organization_id
            != evidence.source_completion_reviewer_organization_id
        ),
        "objective_allowed": review.objective == OBJECTIVE,
        "review_delay_valid": (
            0 <= delay <= policy.max_review_delay_seconds
        ),
        "evidence_fresh": (
            0 <= age <= policy.max_evidence_age_seconds
        ),
        "time_order_valid": time_order,
        "post_operation_review_route_binding_valid": (
            review.post_operation_review_route_digest
            == evidence.post_operation_review_route_digest
            == expected_route
        ),
        "scope_binding_valid": scope_matches(evidence, source_evidence),
        "scope_bounded": scope_bounded,
        "target_resources_allowed": targets_allowed,
        "protected_resources_excluded": protected_excluded,
        "external_operation_absent": (
            not evidence.external_operation_performed
        ),
        "repository_change_absent": not evidence.repository_changed,
        "post_operation_reviewer_mandate_verified": (
            evidence.post_operation_reviewer_mandate_verified
        ),
        "post_operation_reviewer_qualification_verified": (
            evidence.post_operation_reviewer_qualification_verified
        ),
        "post_operation_reviewer_identity_confirmed": (
            evidence.post_operation_reviewer_identity_confirmed
        ),
        "conflict_disclosure_complete": (
            evidence.conflict_disclosure_complete
        ),
        "material_conflict_absent": (
            not evidence.material_conflict_present
        ),
        "jurisdiction_verified": evidence.jurisdiction_verified,
        "review_ready": evidence.review_ready,
        "intended_result_matches_observed": (
            evidence.intended_result_matches_observed
        ),
        "target_post_state_verified": (
            evidence.target_post_state_verified
        ),
        "collateral_effects_absent": (
            evidence.collateral_effects_absent
        ),
        "protected_resources_intact": (
            evidence.protected_resources_intact
        ),
        "protected_core_intact": evidence.protected_core_intact,
        "monitoring_evidence_sufficient": (
            evidence.monitoring_evidence_sufficient
        ),
        "completion_evidence_sufficient": (
            evidence.completion_evidence_sufficient
        ),
        "no_unresolved_anomaly": (
            not evidence.unresolved_anomaly_present
        ),
        "rollback_not_required": not evidence.rollback_required,
        "recovery_not_required": not evidence.recovery_required,
    }
    return checks, expected_digests
