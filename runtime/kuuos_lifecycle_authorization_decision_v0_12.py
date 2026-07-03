#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import fields, replace
from typing import Any

from runtime.kuuos_lifecycle_decision_review_core_v0_11 import (
    artifact_issues as source_artifact_issues,
)
from runtime.kuuos_lifecycle_decision_review_policy_v0_11 import canon
from runtime.kuuos_lifecycle_decision_review_source_v0_11 import (
    all_source_digests as prior_source_digests,
    prior_actor_ids as prior_review_actor_ids,
)
from runtime.kuuos_lifecycle_decision_review_types_v0_11 import (
    CLEAR as SOURCE_CLEAR,
    LifecycleDecisionReviewArtifactV011,
    LifecycleDecisionReviewEvidenceV011,
    LifecycleDecisionReviewPolicyV011,
    LifecycleDecisionReviewSubmissionV011,
)
from runtime.kuuos_lifecycle_authorization_decision_types_v0_12 import (
    APPROVED,
    DENIED,
    OBJECTIVE,
    REJECTED,
    LifecycleAuthorizationDecisionArtifactV012,
    LifecycleAuthorizationDecisionEvidenceV012,
    LifecycleAuthorizationDecisionPolicyV012,
    LifecycleAuthorizationDecisionSubmissionV012,
    evidence_digest,
    policy_digest,
    record_digest,
    submission_digest,
)

SEQUENCE_FIELDS = (
    "operation_scope_items",
    "target_resource_ids",
    "protected_resource_ids",
    "reversible_step_ids",
    "irreversible_step_ids",
)

STRUCTURAL_CHECKS = (
    "policy_valid",
    "decision_valid",
    "evidence_valid",
    "source_recomputed_valid",
    "source_review_clear",
    "source_binding_valid",
    "identity_binding_valid",
    "authorization_decision_maker_allowed",
    "authorization_decision_maker_organization_allowed",
    "future_operator_allowed",
    "independent_from_prior_chain",
    "independent_from_decision_reviewer",
    "independent_from_requester",
    "authorization_maker_operator_separated",
    "objective_allowed",
    "decision_delay_valid",
    "evidence_fresh",
    "time_order_valid",
    "source_review_not_expired",
    "approval_expiry_valid",
    "scope_binding_valid",
)

DECISION_CHECKS = (
    "authority_mandate_verified",
    "authority_qualification_verified",
    "authority_independence_declared",
    "conflict_disclosure_complete",
    "material_conflict_absent",
    "jurisdiction_verified",
    "quorum_verified",
    "decision_rationale_complete",
    "proportionality_satisfied",
    "less_restrictive_alternatives_exhausted",
    "irreversibility_review_complete",
    "human_impact_review_complete",
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


def all_source_digests(
    source_review: LifecycleDecisionReviewSubmissionV011,
    source_evidence: LifecycleDecisionReviewEvidenceV011,
    source_policy: LifecycleDecisionReviewPolicyV011,
    source_record: LifecycleDecisionReviewArtifactV011,
    source_args: tuple[Any, ...],
) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = prior_source_digests(
        source_args[0],
        source_args[1],
        source_args[2],
        source_args[3],
        tuple(source_args[4:]),
    )
    result.update(
        bounded_decision_review=source_review.review_digest,
        bounded_decision_review_evidence=source_evidence.evidence_digest,
        bounded_decision_review_policy=source_policy.policy_digest,
        bounded_decision_review_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(
    source_review: LifecycleDecisionReviewSubmissionV011,
    source_evidence: LifecycleDecisionReviewEvidenceV011,
    source_policy: LifecycleDecisionReviewPolicyV011,
    source_record: LifecycleDecisionReviewArtifactV011,
    source_args: tuple[Any, ...],
) -> bool:
    return not source_artifact_issues(
        source_record,
        source_review,
        source_evidence,
        source_policy,
        *source_args,
    )


def prior_actor_ids(
    subject_id: str,
    source_review: LifecycleDecisionReviewSubmissionV011,
    source_args: tuple[Any, ...],
) -> set[str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = prior_review_actor_ids(
        subject_id, source_args[0], tuple(source_args[4:])
    )
    result.update({source_review.decision_reviewer_id, source_review.requester_id})
    return result


def make_policy(
    policy_id: str,
    *,
    allowed_authorization_decision_maker_ids: tuple[str, ...],
    allowed_authorization_decision_maker_organization_ids: tuple[str, ...],
    allowed_future_operator_ids: tuple[str, ...],
    allowed_target_resource_ids: tuple[str, ...],
    max_decision_delay_seconds: int = 86_400,
    max_evidence_age_seconds: int = 3_600,
    max_approval_expiry_seconds: int = 3_600,
    max_operation_window_seconds: int = 900,
    max_scope_items: int = 32,
) -> LifecycleAuthorizationDecisionPolicyV012:
    value = LifecycleAuthorizationDecisionPolicyV012(
        policy_id=policy_id,
        allowed_authorization_decision_maker_ids=canon(
            allowed_authorization_decision_maker_ids
        ),
        allowed_authorization_decision_maker_organization_ids=canon(
            allowed_authorization_decision_maker_organization_ids
        ),
        allowed_future_operator_ids=canon(allowed_future_operator_ids),
        allowed_target_resource_ids=canon(allowed_target_resource_ids),
        max_decision_delay_seconds=max_decision_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_approval_expiry_seconds=max_approval_expiry_seconds,
        max_operation_window_seconds=max_operation_window_seconds,
        max_scope_items=max_scope_items,
        require_complete_source_recomputation=True,
        require_clear_source_review=True,
        require_authority_mandate=True,
        require_authority_qualification=True,
        require_authority_independence=True,
        require_conflict_disclosure=True,
        require_jurisdiction=True,
        require_quorum=True,
        require_reasoned_decision=True,
        require_proportionality=True,
        require_less_restrictive_alternatives=True,
        require_irreversibility_review=True,
        require_human_impact_review=True,
        require_exact_scope_binding=True,
        require_package_safety=True,
        require_appeal_route=True,
        require_dissent_route=True,
        require_minority_opinion_record=True,
        require_role_separation=True,
        authorization_decision_enabled=True,
        operation_approval_enabled=True,
        operation_start_enabled=False,
        policy_digest="",
    )
    value = replace(value, policy_digest=policy_digest(value))
    issues = policy_issues(value)
    if issues:
        raise ValueError(
            f"lifecycle_authorization_decision_policy_invalid:{issues[0]}"
        )
    return value


def policy_issues(
    value: LifecycleAuthorizationDecisionPolicyV012,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    for name in (
        "allowed_authorization_decision_maker_ids",
        "allowed_authorization_decision_maker_organization_ids",
        "allowed_future_operator_ids",
        "allowed_target_resource_ids",
    ):
        items = getattr(value, name)
        if not items or items != canon(items):
            issues.append(f"{name}_invalid")
    if min(
        value.max_decision_delay_seconds,
        value.max_evidence_age_seconds,
        value.max_approval_expiry_seconds,
        value.max_operation_window_seconds,
        value.max_scope_items,
    ) <= 0:
        issues.append("bound_invalid")
    guards = tuple(
        getattr(value, item.name)
        for item in fields(value)
        if item.name.startswith("require_")
    )
    if not all(guards):
        issues.append("required_guard_disabled")
    if not value.authorization_decision_enabled or not value.operation_approval_enabled:
        issues.append("decision_or_approval_disabled")
    if value.operation_start_enabled:
        issues.append("operation_start_enabled_in_decision_stage")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)


def make_evidence(
    source_review: LifecycleDecisionReviewSubmissionV011,
    source_evidence: LifecycleDecisionReviewEvidenceV011,
    source_policy: LifecycleDecisionReviewPolicyV011,
    source_record: LifecycleDecisionReviewArtifactV011,
    source_args: tuple[Any, ...],
    **overrides: Any,
) -> LifecycleAuthorizationDecisionEvidenceV012:
    values: dict[str, Any] = {
        "subject_id": source_review.subject_id,
        "subject_kind": source_review.subject_kind,
        "subject_version": source_review.subject_version,
        "source_decision_review_id": source_review.decision_review_id,
        "source_decision_review_record_digest": source_record.record_digest,
        "source_artifact_digests": all_source_digests(
            source_review,
            source_evidence,
            source_policy,
            source_record,
            source_args,
        ),
        "decision_reviewer_id": source_review.decision_reviewer_id,
        "requester_id": source_review.requester_id,
        "future_operator_id": source_review.future_operator_id,
        "authorized_scope_digest": source_evidence.reviewed_scope_digest,
        "operation_scope_items": source_evidence.operation_scope_items,
        "target_resource_ids": source_evidence.target_resource_ids,
        "protected_resource_ids": source_evidence.protected_resource_ids,
        "reversible_step_ids": source_evidence.reversible_step_ids,
        "irreversible_step_ids": source_evidence.irreversible_step_ids,
        "rollback_plan_digest": source_evidence.rollback_plan_digest,
        "rollback_plan_verified": source_evidence.rollback_plan_verified,
        "recovery_route_digest": source_evidence.recovery_route_digest,
        "recovery_route_verified": source_evidence.recovery_route_verified,
        "stop_condition_digest": source_evidence.stop_condition_digest,
        "stop_conditions_complete": source_evidence.stop_conditions_complete,
        "abort_channel_digest": source_evidence.abort_channel_digest,
        "abort_channel_available": source_evidence.abort_channel_available,
        "human_oversight_digest": source_evidence.human_oversight_digest,
        "human_oversight_available": source_evidence.human_oversight_available,
        "monitoring_plan_digest": source_evidence.monitoring_plan_digest,
        "monitoring_plan_complete": source_evidence.monitoring_plan_complete,
        "evidence_capture_plan_digest": source_evidence.evidence_capture_plan_digest,
        "evidence_capture_plan_complete": (
            source_evidence.evidence_capture_plan_complete
        ),
        "simulation_receipt_digest": source_evidence.simulation_receipt_digest,
        "simulation_verified": source_evidence.simulation_verified,
        "operation_window_seconds": source_evidence.operation_window_seconds,
        "protected_core_excluded": source_evidence.protected_core_excluded,
        "institutional_hold_active": source_evidence.institutional_hold_active,
        "emergency_state_active": source_evidence.emergency_state_active,
        "appeal_route_digest": source_evidence.appeal_route_digest,
        "appeal_route_available": source_evidence.appeal_route_available,
        "dissent_route_digest": source_evidence.dissent_route_digest,
        "dissent_route_available": source_evidence.dissent_route_available,
        "minority_opinion_digest": source_evidence.minority_opinion_digest,
        "minority_opinion_recorded": source_evidence.minority_opinion_recorded,
    }
    values.update(overrides)
    for name in SEQUENCE_FIELDS:
        values[name] = canon(tuple(values[name]))
    value = LifecycleAuthorizationDecisionEvidenceV012(
        evidence_digest="", **values
    )
    value = replace(value, evidence_digest=evidence_digest(value))
    issues = evidence_issues(value)
    if issues:
        raise ValueError(
            f"lifecycle_authorization_decision_evidence_invalid:{issues[0]}"
        )
    return value


def evidence_issues(
    value: LifecycleAuthorizationDecisionEvidenceV012,
) -> tuple[str, ...]:
    issues: list[str] = []
    excluded = {
        "evidence_digest",
        "version",
        "source_artifact_digests",
        "operation_scope_items",
        "target_resource_ids",
        "protected_resource_ids",
        "reversible_step_ids",
        "irreversible_step_ids",
        "decision_requested_at_epoch_seconds",
        "captured_at_epoch_seconds",
        "completed_at_epoch_seconds",
        "approval_expiry_at_epoch_seconds",
        "operation_window_seconds",
    }
    required = tuple(
        getattr(value, item.name)
        for item in fields(value)
        if item.name not in excluded and item.type == "str"
    )
    if not all(required):
        issues.append("required_identity_or_binding_missing")
    if not value.source_artifact_digests:
        issues.append("source_digests_missing")
    if min(
        value.decision_requested_at_epoch_seconds,
        value.captured_at_epoch_seconds,
        value.completed_at_epoch_seconds,
        value.approval_expiry_at_epoch_seconds,
        value.operation_window_seconds,
    ) < 0:
        issues.append("negative_time_or_window")
    for name in SEQUENCE_FIELDS:
        if getattr(value, name) != canon(getattr(value, name)):
            issues.append(f"{name}_not_canonical")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_submission(
    authorization_decision_id: str,
    authorization_decision_maker_id: str,
    authorization_decision_maker_organization_id: str,
    decision_requested_at_epoch_seconds: int,
    completed_at_epoch_seconds: int,
    source_review: LifecycleDecisionReviewSubmissionV011,
    source_record: LifecycleDecisionReviewArtifactV011,
    authorization_evidence: LifecycleAuthorizationDecisionEvidenceV012,
    *,
    approval_expiry_at_epoch_seconds: int,
    objective: str = OBJECTIVE,
) -> LifecycleAuthorizationDecisionSubmissionV012:
    value = LifecycleAuthorizationDecisionSubmissionV012(
        authorization_decision_id=authorization_decision_id,
        authorization_decision_maker_id=authorization_decision_maker_id,
        authorization_decision_maker_organization_id=(
            authorization_decision_maker_organization_id
        ),
        objective=objective,
        decision_requested_at_epoch_seconds=decision_requested_at_epoch_seconds,
        completed_at_epoch_seconds=completed_at_epoch_seconds,
        source_decision_review_id=source_review.decision_review_id,
        source_decision_review_record_digest=source_record.record_digest,
        subject_id=source_review.subject_id,
        subject_kind=source_review.subject_kind,
        subject_version=source_review.subject_version,
        authorization_evidence_digest=authorization_evidence.evidence_digest,
        decision_reviewer_id=source_review.decision_reviewer_id,
        requester_id=source_review.requester_id,
        future_operator_id=source_review.future_operator_id,
        approval_expiry_at_epoch_seconds=approval_expiry_at_epoch_seconds,
        decision_digest="",
    )
    value = replace(value, decision_digest=submission_digest(value))
    issues = submission_issues(value)
    if issues:
        raise ValueError(
            f"lifecycle_authorization_decision_invalid:{issues[0]}"
        )
    return value


def submission_issues(
    value: LifecycleAuthorizationDecisionSubmissionV012,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = tuple(
        getattr(value, item.name)
        for item in fields(value)
        if item.name
        not in {
            "decision_digest",
            "version",
            "decision_requested_at_epoch_seconds",
            "completed_at_epoch_seconds",
            "approval_expiry_at_epoch_seconds",
        }
    )
    if not all(required):
        issues.append("required_decision_field_missing")
    if min(
        value.decision_requested_at_epoch_seconds,
        value.completed_at_epoch_seconds,
        value.approval_expiry_at_epoch_seconds,
    ) < 0:
        issues.append("negative_decision_time")
    if value.decision_digest != submission_digest(value):
        issues.append("decision_digest_mismatch")
    return tuple(issues)


def scope_matches(
    evidence: LifecycleAuthorizationDecisionEvidenceV012,
    source: LifecycleDecisionReviewEvidenceV011,
) -> bool:
    pairs = (
        ("authorized_scope_digest", "reviewed_scope_digest"),
        ("operation_scope_items", "operation_scope_items"),
        ("target_resource_ids", "target_resource_ids"),
        ("protected_resource_ids", "protected_resource_ids"),
        ("reversible_step_ids", "reversible_step_ids"),
        ("irreversible_step_ids", "irreversible_step_ids"),
        ("rollback_plan_digest", "rollback_plan_digest"),
        ("recovery_route_digest", "recovery_route_digest"),
        ("stop_condition_digest", "stop_condition_digest"),
        ("abort_channel_digest", "abort_channel_digest"),
        ("human_oversight_digest", "human_oversight_digest"),
        ("monitoring_plan_digest", "monitoring_plan_digest"),
        ("evidence_capture_plan_digest", "evidence_capture_plan_digest"),
        ("simulation_receipt_digest", "simulation_receipt_digest"),
        ("operation_window_seconds", "operation_window_seconds"),
    )
    for target, source_name in pairs:
        left = getattr(evidence, target)
        right = getattr(source, source_name)
        if target in SEQUENCE_FIELDS:
            right = canon(tuple(right))
        if left != right:
            return False
    return True


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
        and source_record.lifecycle_read_only
    )
    source_binding = (
        (decision.subject_id, decision.subject_kind, decision.subject_version)
        == (evidence.subject_id, evidence.subject_kind, evidence.subject_version)
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
        and decision.decision_reviewer_id
        == evidence.decision_reviewer_id
        == source_review.decision_reviewer_id
        and decision.requester_id
        == evidence.requester_id
        == source_review.requester_id
        and decision.future_operator_id
        == evidence.future_operator_id
        == source_review.future_operator_id
        and decision.authorization_decision_maker_id
        == evidence.authorization_decision_maker_id
        == source_review.authorization_decision_maker_id
    )
    identity_binding = (
        decision.authorization_decision_id == evidence.authorization_decision_id
        and decision.authorization_decision_maker_organization_id
        == evidence.authorization_decision_maker_organization_id
        and decision.authorization_evidence_digest == evidence.evidence_digest
        and decision.decision_requested_at_epoch_seconds
        == evidence.decision_requested_at_epoch_seconds
        and decision.completed_at_epoch_seconds
        == evidence.completed_at_epoch_seconds
        and decision.approval_expiry_at_epoch_seconds
        == evidence.approval_expiry_at_epoch_seconds
    )
    prior_ids = prior_actor_ids(decision.subject_id, source_review, source_args)
    delay = (
        decision.completed_at_epoch_seconds
        - source_review.completed_at_epoch_seconds
    )
    age = decision.completed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    time_order = (
        evidence.decision_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.completed_at_epoch_seconds
        == decision.completed_at_epoch_seconds
    )
    source_review_not_expired = (
        decision.completed_at_epoch_seconds
        <= source_evidence.authorization_decision_deadline_at_epoch_seconds
        <= source_evidence.review_expiry_at_epoch_seconds
    )
    request_expiry = (
        getattr(source_args[1], "request_expiry_at_epoch_seconds", 0)
        if len(source_args) > 1
        else 0
    )
    approval_expiry_valid = (
        decision.completed_at_epoch_seconds
        < decision.approval_expiry_at_epoch_seconds
        <= source_evidence.review_expiry_at_epoch_seconds
        and decision.approval_expiry_at_epoch_seconds
        <= decision.completed_at_epoch_seconds + policy.max_approval_expiry_seconds
        and (
            request_expiry == 0
            or decision.approval_expiry_at_epoch_seconds <= request_expiry
        )
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
    window_valid = (
        0
        < evidence.operation_window_seconds
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
        "authorization_decision_maker_allowed": (
            decision.authorization_decision_maker_id
            in policy.allowed_authorization_decision_maker_ids
        ),
        "authorization_decision_maker_organization_allowed": (
            decision.authorization_decision_maker_organization_id
            in policy.allowed_authorization_decision_maker_organization_ids
        ),
        "future_operator_allowed": (
            decision.future_operator_id in policy.allowed_future_operator_ids
        ),
        "independent_from_prior_chain": (
            decision.authorization_decision_maker_id not in prior_ids
        ),
        "independent_from_decision_reviewer": (
            decision.authorization_decision_maker_id
            != decision.decision_reviewer_id
        ),
        "independent_from_requester": (
            decision.authorization_decision_maker_id != decision.requester_id
        ),
        "authorization_maker_operator_separated": (
            decision.authorization_decision_maker_id
            != decision.future_operator_id
        ),
        "objective_allowed": decision.objective == OBJECTIVE,
        "decision_delay_valid": (
            0 <= delay <= policy.max_decision_delay_seconds
        ),
        "evidence_fresh": 0 <= age <= policy.max_evidence_age_seconds,
        "time_order_valid": time_order,
        "source_review_not_expired": source_review_not_expired,
        "approval_expiry_valid": approval_expiry_valid,
        "scope_binding_valid": scope_matches(evidence, source_evidence),
        "authority_mandate_verified": evidence.authority_mandate_verified,
        "authority_qualification_verified": (
            evidence.authority_qualification_verified
        ),
        "authority_independence_declared": (
            evidence.authority_independence_declared
        ),
        "conflict_disclosure_complete": evidence.conflict_disclosure_complete,
        "material_conflict_absent": not evidence.material_conflict_present,
        "jurisdiction_verified": evidence.jurisdiction_verified,
        "quorum_verified": evidence.quorum_verified,
        "decision_rationale_complete": evidence.decision_rationale_complete,
        "proportionality_satisfied": evidence.proportionality_satisfied,
        "less_restrictive_alternatives_exhausted": (
            evidence.less_restrictive_alternatives_exhausted
        ),
        "irreversibility_review_complete": (
            evidence.irreversibility_review_complete
        ),
        "human_impact_review_complete": evidence.human_impact_review_complete,
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
        "operation_window_valid": window_valid,
        "protected_core_excluded": evidence.protected_core_excluded,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
        "appeal_route_available": evidence.appeal_route_available,
        "dissent_route_available": evidence.dissent_route_available,
        "minority_opinion_recorded": evidence.minority_opinion_recorded,
    }
    return checks, expected_digests


def compute_artifact(
    decision: LifecycleAuthorizationDecisionSubmissionV012,
    evidence: LifecycleAuthorizationDecisionEvidenceV012,
    policy: LifecycleAuthorizationDecisionPolicyV012,
    source_review: LifecycleDecisionReviewSubmissionV011,
    source_evidence: LifecycleDecisionReviewEvidenceV011,
    source_policy: LifecycleDecisionReviewPolicyV011,
    source_record: LifecycleDecisionReviewArtifactV011,
    *source_args: Any,
) -> LifecycleAuthorizationDecisionArtifactV012:
    checks, expected_digests = evaluate(
        decision,
        evidence,
        policy,
        source_review,
        source_evidence,
        source_policy,
        source_record,
        tuple(source_args),
    )
    if not all(checks[name] for name in STRUCTURAL_CHECKS):
        status = REJECTED
        reason = "source_review_policy_or_binding_invalid"
    else:
        failed = next(
            (name for name in DECISION_CHECKS if not checks[name]), None
        )
        if failed is None:
            status = APPROVED
            reason = "bounded_operation_approved_for_separate_start"
        else:
            status = DENIED
            reason = failed
    decision_issued = status != REJECTED
    approved = status == APPROVED
    artifact = LifecycleAuthorizationDecisionArtifactV012(
        authorization_decision_id=decision.authorization_decision_id,
        status=status,
        reason=reason,
        authorization_decision_maker_id=(
            decision.authorization_decision_maker_id
        ),
        authorization_decision_maker_organization_id=(
            decision.authorization_decision_maker_organization_id
        ),
        subject_id=decision.subject_id,
        source_decision_review_id=decision.source_decision_review_id,
        decision_reviewer_id=decision.decision_reviewer_id,
        requester_id=decision.requester_id,
        future_operator_id=decision.future_operator_id,
        policy_digest=policy.policy_digest,
        decision_digest=decision.decision_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        decision_record_issued=decision_issued,
        authorization_decision_made=decision_issued,
        operation_approved=approved,
        operation_start_required_next=approved,
        operation_started=False,
        operation_completed=False,
        authority_changed=False,
        quiescence_state_changed=False,
        terminal_state_changed=False,
        terminal_marker_written=False,
        resource_removed=False,
        external_operation_performed=False,
        repository_changed=False,
        governance_decision_only=True,
        record_digest="",
    )
    return replace(artifact, record_digest=record_digest(artifact))


def verify_artifact(
    *args: Any, **kwargs: Any
) -> LifecycleAuthorizationDecisionArtifactV012:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError(
            f"lifecycle_authorization_decision_record_invalid:{issues[0]}"
        )
    return artifact


def artifact_issues(
    artifact: LifecycleAuthorizationDecisionArtifactV012,
    *args: Any,
    **kwargs: Any,
) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues: list[str] = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("authorization_decision_recomputation_mismatch")
    if artifact.status not in (APPROVED, DENIED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == APPROVED and not (
        artifact.decision_record_issued
        and artifact.authorization_decision_made
        and artifact.operation_approved
        and artifact.operation_start_required_next
    ):
        issues.append("approved_gate_invalid")
    if artifact.status == DENIED and (
        not artifact.decision_record_issued
        or not artifact.authorization_decision_made
        or artifact.operation_approved
        or artifact.operation_start_required_next
    ):
        issues.append("denied_gate_invalid")
    if artifact.status == REJECTED and (
        artifact.decision_record_issued
        or artifact.authorization_decision_made
        or artifact.operation_approved
        or artifact.operation_start_required_next
    ):
        issues.append("rejected_record_issued")
    later_effects = (
        artifact.operation_started,
        artifact.operation_completed,
        artifact.authority_changed,
        artifact.quiescence_state_changed,
        artifact.terminal_state_changed,
        artifact.terminal_marker_written,
        artifact.resource_removed,
        artifact.external_operation_performed,
        artifact.repository_changed,
    )
    if any(later_effects) or not artifact.governance_decision_only:
        issues.append("operation_or_lifecycle_effect_performed")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)


__all__ = [
    "make_policy",
    "policy_issues",
    "make_evidence",
    "evidence_issues",
    "make_submission",
    "submission_issues",
    "compute_artifact",
    "verify_artifact",
    "artifact_issues",
    "prior_actor_ids",
    "source_recomputed_valid",
]
