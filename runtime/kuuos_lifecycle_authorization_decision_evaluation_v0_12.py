from __future__ import annotations

from typing import Any

from runtime.kuuos_lifecycle_decision_review_types_v0_11 import (
    CLEAR as SOURCE_CLEAR,
    LifecycleDecisionReviewArtifactV011,
    LifecycleDecisionReviewEvidenceV011,
    LifecycleDecisionReviewPolicyV011,
    LifecycleDecisionReviewSubmissionV011,
)
from runtime.kuuos_lifecycle_authorization_decision_binding_v0_12 import (
    evidence_issues,
    scope_matches,
    submission_issues,
)
from runtime.kuuos_lifecycle_authorization_decision_policy_v0_12 import (
    policy_issues,
)
from runtime.kuuos_lifecycle_authorization_decision_source_v0_12 import (
    all_source_digests,
    prior_actor_ids,
    source_recomputed_valid,
)
from runtime.kuuos_lifecycle_authorization_decision_types_v0_12 import (
    OBJECTIVE,
    LifecycleAuthorizationDecisionEvidenceV012,
    LifecycleAuthorizationDecisionPolicyV012,
    LifecycleAuthorizationDecisionSubmissionV012,
)

STRUCTURAL_CHECKS = (
    "policy_valid",
    "decision_valid",
    "evidence_valid",
    "source_recomputed_valid",
    "source_review_clear",
    "source_binding_valid",
    "identity_binding_valid",
    "decision_maker_allowed",
    "decision_maker_organization_allowed",
    "designated_decision_maker_binding_valid",
    "independent_from_prior_chain",
    "independent_from_requester",
    "independent_from_source_decision_reviewer",
    "independent_from_future_operator",
    "decision_maker_operator_separated",
    "objective_allowed",
    "decision_delay_valid",
    "evidence_fresh",
    "time_order_valid",
    "source_authorization_window_valid",
    "decision_not_expired",
    "operation_approval_deadline_valid",
    "operation_approval_route_binding_valid",
    "scope_binding_valid",
)

DENIAL_CHECKS = (
    "decision_maker_mandate_verified",
    "decision_maker_qualification_verified",
    "decision_maker_independence_declared",
    "conflict_disclosure_complete",
    "material_conflict_absent",
    "jurisdiction_verified",
    "quorum_satisfied",
    "reasoned_decision_complete",
    "proportionality_satisfied",
    "less_restrictive_alternatives_exhausted",
    "irreversibility_review_complete",
    "human_impact_review_complete",
    "operation_approval_route_available",
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
    decision: LifecycleAuthorizationDecisionSubmissionV012,
    evidence: LifecycleAuthorizationDecisionEvidenceV012,
    policy: LifecycleAuthorizationDecisionPolicyV012,
    source_review: LifecycleDecisionReviewSubmissionV011,
    source_evidence: LifecycleDecisionReviewEvidenceV011,
    source_policy: LifecycleDecisionReviewPolicyV011,
    source_record: LifecycleDecisionReviewArtifactV011,
    source_args: tuple[Any, ...],
) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(
        source_review,
        source_evidence,
        source_policy,
        source_record,
        source_args,
    )
    source_clear = (
        source_record.status == SOURCE_CLEAR
        and source_record.review_record_issued
        and source_record.review_completed
        and source_record.clear_for_authorization_decision
        and source_record.authorization_decision_required_next
        and not source_record.authorization_decision_made
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
        (
            decision.subject_id,
            decision.subject_kind,
            decision.subject_version,
        )
        == (
            evidence.subject_id,
            evidence.subject_kind,
            evidence.subject_version,
        )
        == (
            source_review.subject_id,
            source_review.subject_kind,
            source_review.subject_version,
        )
        and decision.source_decision_review_id
        == evidence.source_decision_review_id
        == source_review.decision_review_id
        and decision.source_decision_review_record_digest
        == evidence.source_decision_review_record_digest
        == source_record.record_digest
        and evidence.source_artifact_digests == expected_digests
        and decision.requester_id
        == evidence.requester_id
        == source_review.requester_id
        and decision.source_decision_reviewer_id
        == evidence.source_decision_reviewer_id
        == source_review.decision_reviewer_id
        and decision.future_operator_id
        == evidence.future_operator_id
        == source_review.future_operator_id
    )
    identity_binding = (
        decision.authorization_decision_id == evidence.authorization_decision_id
        and decision.authorization_decision_maker_id
        == evidence.authorization_decision_maker_id
        and decision.authorization_decision_maker_organization_id
        == evidence.authorization_decision_maker_organization_id
        and decision.decision_evidence_digest == evidence.evidence_digest
        and decision.decision_requested_at_epoch_seconds
        == evidence.decision_requested_at_epoch_seconds
        and decision.completed_at_epoch_seconds == evidence.completed_at_epoch_seconds
        and decision.operation_approval_route_digest
        == evidence.operation_approval_route_digest
        and decision.operation_approval_deadline_at_epoch_seconds
        == evidence.operation_approval_deadline_at_epoch_seconds
    )
    designated_binding = (
        decision.authorization_decision_maker_id
        == evidence.authorization_decision_maker_id
        == source_review.authorization_decision_maker_id
        == source_record.authorization_decision_maker_id
    )
    prior_ids = prior_actor_ids(
        decision.subject_id,
        source_review,
        source_args,
    )
    delay = (
        decision.completed_at_epoch_seconds
        - source_review.completed_at_epoch_seconds
    )
    age = (
        decision.completed_at_epoch_seconds
        - evidence.captured_at_epoch_seconds
    )
    time_order = (
        evidence.decision_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.completed_at_epoch_seconds
        == decision.completed_at_epoch_seconds
    )
    source_window = (
        decision.completed_at_epoch_seconds
        <= source_evidence.authorization_decision_deadline_at_epoch_seconds
        <= source_evidence.review_expiry_at_epoch_seconds
    )
    decision_not_expired = (
        decision.completed_at_epoch_seconds
        <= evidence.authorization_decision_expiry_at_epoch_seconds
        <= decision.completed_at_epoch_seconds + policy.max_decision_expiry_seconds
        and evidence.authorization_decision_expiry_at_epoch_seconds
        <= source_evidence.review_expiry_at_epoch_seconds
    )
    approval_deadline = (
        decision.completed_at_epoch_seconds
        < decision.operation_approval_deadline_at_epoch_seconds
        <= evidence.authorization_decision_expiry_at_epoch_seconds
        and decision.operation_approval_deadline_at_epoch_seconds
        <= decision.completed_at_epoch_seconds
        + policy.max_operation_approval_delay_seconds
    )
    scope_bounded = (
        0 < len(evidence.operation_scope_items) <= policy.max_scope_items
    )
    targets_allowed = bool(evidence.target_resource_ids) and set(
        evidence.target_resource_ids
    ).issubset(set(policy.allowed_target_resource_ids))
    protected_excluded = not (
        set(evidence.target_resource_ids) & set(evidence.protected_resource_ids)
    )
    operation_window_valid = (
        0 < evidence.operation_window_seconds
        <= policy.max_operation_window_seconds
    )
    checks = {
        "policy_valid": not policy_issues(policy),
        "decision_valid": not submission_issues(decision),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(
            source_review,
            source_evidence,
            source_policy,
            source_record,
            source_args,
        ),
        "source_review_clear": source_clear,
        "source_binding_valid": source_binding,
        "identity_binding_valid": identity_binding,
        "decision_maker_allowed": (
            decision.authorization_decision_maker_id
            in policy.allowed_authorization_decision_maker_ids
        ),
        "decision_maker_organization_allowed": (
            decision.authorization_decision_maker_organization_id
            in policy.allowed_authorization_decision_maker_organization_ids
        ),
        "designated_decision_maker_binding_valid": designated_binding,
        "decision_maker_mandate_verified": (
            evidence.decision_maker_mandate_verified
        ),
        "decision_maker_qualification_verified": (
            evidence.decision_maker_qualification_verified
        ),
        "decision_maker_independence_declared": (
            evidence.decision_maker_independence_declared
        ),
        "independent_from_prior_chain": (
            decision.authorization_decision_maker_id not in prior_ids
        ),
        "independent_from_requester": (
            decision.authorization_decision_maker_id != decision.requester_id
        ),
        "independent_from_source_decision_reviewer": (
            decision.authorization_decision_maker_id
            != decision.source_decision_reviewer_id
        ),
        "independent_from_future_operator": (
            decision.authorization_decision_maker_id
            != decision.future_operator_id
        ),
        "decision_maker_operator_separated": (
            decision.authorization_decision_maker_id
            != decision.future_operator_id
        ),
        "objective_allowed": decision.objective == OBJECTIVE,
        "decision_delay_valid": (
            0 <= delay <= policy.max_decision_delay_seconds
        ),
        "evidence_fresh": (
            0 <= age <= policy.max_evidence_age_seconds
        ),
        "time_order_valid": time_order,
        "source_authorization_window_valid": source_window,
        "decision_not_expired": decision_not_expired,
        "operation_approval_deadline_valid": approval_deadline,
        "operation_approval_route_binding_valid": (
            decision.operation_approval_route_digest
            == evidence.operation_approval_route_digest
        ),
        "operation_approval_route_available": (
            evidence.operation_approval_route_available
        ),
        "conflict_disclosure_complete": evidence.conflict_disclosure_complete,
        "material_conflict_absent": not evidence.material_conflict_present,
        "jurisdiction_verified": evidence.jurisdiction_verified,
        "quorum_satisfied": evidence.quorum_satisfied,
        "reasoned_decision_complete": evidence.reasoned_decision_complete,
        "proportionality_satisfied": evidence.proportionality_satisfied,
        "less_restrictive_alternatives_exhausted": (
            evidence.less_restrictive_alternatives_exhausted
        ),
        "irreversibility_review_complete": (
            evidence.irreversibility_review_complete
        ),
        "human_impact_review_complete": (
            evidence.human_impact_review_complete
        ),
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
        "evidence_capture_plan_complete": (
            evidence.evidence_capture_plan_complete
        ),
        "simulation_verified": evidence.simulation_verified,
        "operation_window_valid": operation_window_valid,
        "protected_core_excluded": evidence.protected_core_excluded,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
        "appeal_route_available": evidence.appeal_route_available,
        "dissent_route_available": evidence.dissent_route_available,
        "minority_opinion_recorded": evidence.minority_opinion_recorded,
    }
    return checks, expected_digests
