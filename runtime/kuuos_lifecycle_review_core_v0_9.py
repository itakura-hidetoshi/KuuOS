from __future__ import annotations

from dataclasses import replace
from typing import Any

from runtime.kuuos_apoptosis_bounded_execution_preparation_types_v0_8 import (
    BOUNDED_EXECUTION_PREPARATION_READY,
    ApoptosisBoundedExecutionPreparationEvidence,
    ApoptosisBoundedExecutionPreparationPolicy,
    ApoptosisBoundedExecutionPreparationRecord,
    ApoptosisBoundedExecutionPreparationRequest,
)
from runtime.kuuos_apoptosis_bounded_execution_preparation_v0_8 import (
    apoptosis_bounded_execution_preparation_record_issues,
)
from runtime.kuuos_lifecycle_review_binding_v0_9 import (
    evidence_issues,
    request_issues,
    scope_matches,
)
from runtime.kuuos_lifecycle_review_chain_v0_9 import (
    named_source,
    source_digests,
)
from runtime.kuuos_lifecycle_review_policy_v0_9 import policy_issues
from runtime.kuuos_lifecycle_review_types_v0_9 import (
    BLOCKED,
    CLEAR,
    OBJECTIVE,
    REJECTED,
    LifecycleReviewArtifactV09,
    LifecycleReviewEvidenceV09,
    LifecycleReviewPolicyV09,
    LifecycleReviewRequestV09,
    lifecycle_review_record_digest,
)


def compute_artifact(
    request: LifecycleReviewRequestV09,
    evidence: LifecycleReviewEvidenceV09,
    policy: LifecycleReviewPolicyV09,
    preparation_request: ApoptosisBoundedExecutionPreparationRequest,
    preparation_evidence: ApoptosisBoundedExecutionPreparationEvidence,
    preparation_policy: ApoptosisBoundedExecutionPreparationPolicy,
    preparation_record: ApoptosisBoundedExecutionPreparationRecord,
    *source_args: Any,
) -> LifecycleReviewArtifactV09:
    source = tuple(source_args)
    source_recomputed = not apoptosis_bounded_execution_preparation_record_issues(
        preparation_record,
        preparation_request,
        preparation_evidence,
        preparation_policy,
        *source,
    )
    source_ready = (
        preparation_record.status == BOUNDED_EXECUTION_PREPARATION_READY
        and preparation_record.preparation_record_issued
        and preparation_record.bounded_execution_package_prepared
        and preparation_record.ready_for_execution_review
        and preparation_record.execution_review_required_next
    )
    expected_digests = source_digests(
        preparation_request,
        preparation_evidence,
        preparation_policy,
        preparation_record,
        source,
    )
    source_binding = (
        (request.subject_id, request.subject_kind, request.subject_version)
        == (evidence.subject_id, evidence.subject_kind, evidence.subject_version)
        == (
            preparation_record.subject_id,
            preparation_record.subject_kind,
            preparation_record.subject_version,
        )
        and request.source_preparation_id
        == evidence.source_preparation_id
        == preparation_record.preparation_id
        and request.source_preparation_record_digest
        == evidence.source_preparation_record_digest
        == preparation_record.record_digest
        and evidence.source_artifact_digests == expected_digests
        and request.future_execution_authority_id
        == evidence.future_execution_authority_id
        == preparation_record.future_execution_authority_id
        and request.future_execution_operator_id
        == evidence.future_execution_operator_id
    )
    identity_binding = (
        request.review_id == evidence.review_id
        and request.reviewer_id == evidence.reviewer_id
        and request.reviewer_organization_id == evidence.reviewer_organization_id
        and request.review_evidence_digest == evidence.evidence_digest
        and request.review_requested_at_epoch_seconds
        == evidence.review_requested_at_epoch_seconds
        and request.completed_at_epoch_seconds == evidence.completed_at_epoch_seconds
    )
    named = named_source(source)
    prior_ids = {
        request.subject_id,
        named["candidate_record"].issuer_id,
        named["dependency_record"].reviewer_id,
        named["authority_record"].reviewer_id,
        named["authority_evidence"].responsible_authority_id,
        named["quiescence_record"].reviewer_id,
        named["external_record"].reviewer_id,
        named["external_evidence"].quiescence_evidence_producer_id,
    }
    prior_independent = request.reviewer_id not in prior_ids
    authorization_independent = (
        request.reviewer_id != named["authorization_record"].authority_id
    )
    preparer_independent = request.reviewer_id != preparation_record.preparer_id
    operator_independent = request.reviewer_id != request.future_execution_operator_id
    authority_operator_separated = (
        request.future_execution_authority_id != request.future_execution_operator_id
    )
    time_order = (
        evidence.review_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.completed_at_epoch_seconds
        == request.completed_at_epoch_seconds
    )
    delay = request.completed_at_epoch_seconds - preparation_record.completed_at_epoch_seconds
    age = request.completed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    source_not_expired = (
        request.completed_at_epoch_seconds
        <= preparation_evidence.package_expiry_at_epoch_seconds
    )
    review_not_expired = (
        request.completed_at_epoch_seconds
        <= evidence.review_expiry_at_epoch_seconds
        <= request.completed_at_epoch_seconds + policy.max_review_expiry_seconds
    )
    scope_binding = scope_matches(evidence, preparation_evidence)
    scope_bounded = 0 < len(evidence.execution_scope_items) <= policy.max_scope_items
    targets_allowed = bool(evidence.target_resource_ids) and set(
        evidence.target_resource_ids
    ).issubset(set(policy.allowed_target_resource_ids))
    protected_excluded = not (
        set(evidence.target_resource_ids) & set(evidence.protected_resource_ids)
    )
    no_irreversible = not evidence.irreversible_step_ids
    window_valid = (
        0 < evidence.execution_window_seconds
        <= policy.max_execution_window_seconds
    )
    checks = {
        "policy_valid": not policy_issues(policy),
        "request_valid": not request_issues(request),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed,
        "source_preparation_ready": source_ready,
        "source_binding_valid": source_binding,
        "identity_binding_valid": identity_binding,
        "reviewer_allowed": request.reviewer_id in policy.allowed_reviewer_ids,
        "reviewer_organization_allowed": (
            request.reviewer_organization_id
            in policy.allowed_reviewer_organization_ids
        ),
        "reviewer_qualification_verified": evidence.reviewer_qualification_verified,
        "reviewer_independence_declared": evidence.reviewer_independence_declared,
        "independent_from_prior_chain": prior_independent,
        "independent_from_authorization_authority": authorization_independent,
        "independent_from_preparer": preparer_independent,
        "independent_from_execution_operator": operator_independent,
        "authority_operator_separated": authority_operator_separated,
        "objective_allowed": request.objective == OBJECTIVE,
        "review_delay_valid": 0 <= delay <= policy.max_review_delay_seconds,
        "evidence_fresh": 0 <= age <= policy.max_evidence_age_seconds,
        "time_order_valid": time_order,
        "source_package_not_expired": source_not_expired,
        "review_not_expired": review_not_expired,
        "conflict_disclosure_complete": evidence.conflict_disclosure_complete,
        "material_conflict_absent": not evidence.material_conflict_present,
        "scope_binding_valid": scope_binding,
        "scope_bounded": scope_bounded,
        "target_resources_allowed": targets_allowed,
        "protected_resources_excluded": protected_excluded,
        "no_irreversible_steps": no_irreversible,
        "rollback_plan_verified": evidence.rollback_plan_verified,
        "recovery_route_verified": evidence.recovery_route_verified,
        "stop_conditions_complete": evidence.stop_conditions_complete,
        "abort_channel_available": evidence.abort_channel_available,
        "human_oversight_available": evidence.human_oversight_available,
        "monitoring_plan_complete": evidence.monitoring_plan_complete,
        "evidence_capture_plan_complete": evidence.evidence_capture_plan_complete,
        "simulation_verified": evidence.simulation_verified,
        "execution_window_valid": window_valid,
        "protected_core_excluded": evidence.protected_core_excluded,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
        "appeal_route_available": evidence.appeal_route_available,
        "dissent_route_available": evidence.dissent_route_available,
    }
    structural = (
        "policy_valid", "request_valid", "evidence_valid",
        "source_recomputed_valid", "source_preparation_ready",
        "source_binding_valid", "identity_binding_valid", "reviewer_allowed",
        "reviewer_organization_allowed", "independent_from_prior_chain",
        "independent_from_authorization_authority", "independent_from_preparer",
        "independent_from_execution_operator", "authority_operator_separated",
        "objective_allowed", "review_delay_valid", "evidence_fresh",
        "time_order_valid", "source_package_not_expired",
        "review_not_expired", "scope_binding_valid",
    )
    if not all(checks[name] for name in structural):
        status = REJECTED
        reason = "source_request_policy_or_binding_invalid"
    else:
        blockers = (
            "reviewer_qualification_verified", "reviewer_independence_declared",
            "conflict_disclosure_complete", "material_conflict_absent",
            "scope_bounded", "target_resources_allowed",
            "protected_resources_excluded", "no_irreversible_steps",
            "rollback_plan_verified", "recovery_route_verified",
            "stop_conditions_complete", "abort_channel_available",
            "human_oversight_available", "monitoring_plan_complete",
            "evidence_capture_plan_complete", "simulation_verified",
            "execution_window_valid", "protected_core_excluded",
            "institutional_hold_absent", "emergency_state_absent",
            "appeal_route_available", "dissent_route_available",
        )
        failed = next((name for name in blockers if not checks[name]), None)
        if failed is None:
            status = CLEAR
            reason = "clear_for_separate_request_layer_only"
        else:
            status = BLOCKED
            reason = failed
    issued = status != REJECTED
    clear = status == CLEAR
    artifact = LifecycleReviewArtifactV09(
        review_id=request.review_id,
        status=status,
        reason=reason,
        reviewer_id=request.reviewer_id,
        reviewer_organization_id=request.reviewer_organization_id,
        subject_id=request.subject_id,
        source_preparation_id=request.source_preparation_id,
        future_execution_authority_id=request.future_execution_authority_id,
        future_execution_operator_id=request.future_execution_operator_id,
        policy_digest=policy.policy_digest,
        request_digest=request.request_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        review_record_issued=issued,
        review_completed=issued,
        clear_for_next_request_layer=clear,
        next_request_layer_required=clear,
        effect_free=True,
        read_only=True,
        record_digest="",
    )
    return replace(artifact, record_digest=lifecycle_review_record_digest(artifact))


def verify_artifact(*args: Any, **kwargs: Any) -> LifecycleReviewArtifactV09:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError(f"execution_review_record_invalid:{issues[0]}")
    return artifact


def artifact_issues(
    artifact: LifecycleReviewArtifactV09,
    *args: Any,
    **kwargs: Any,
) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues: list[str] = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("review_recomputation_mismatch")
    if artifact.status not in (CLEAR, BLOCKED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == CLEAR and not (
        artifact.review_record_issued and artifact.review_completed
        and artifact.clear_for_next_request_layer
        and artifact.next_request_layer_required
    ):
        issues.append("clear_gate_invalid")
    if artifact.status == BLOCKED and (
        not artifact.review_record_issued or not artifact.review_completed
        or artifact.clear_for_next_request_layer
        or artifact.next_request_layer_required
    ):
        issues.append("blocked_advanced")
    if artifact.status == REJECTED and (
        artifact.review_record_issued or artifact.review_completed
        or artifact.clear_for_next_request_layer
        or artifact.next_request_layer_required
    ):
        issues.append("rejected_record_issued")
    if not artifact.effect_free or not artifact.read_only:
        issues.append("non_read_only_artifact")
    if artifact.record_digest != lifecycle_review_record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
