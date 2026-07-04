#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_state_adoption_v0_25 import (
    ADOPTED as SOURCE_ADOPTED,
    artifact_issues as source_artifact_issues,
    all_source_digests as adoption_source_digests,
)

VERSION = "kuuos_lifecycle_bounded_repository_mutation_review_v0_26"
APPROVED = "LIFECYCLE_BOUNDED_REPOSITORY_MUTATION_REVIEW_APPROVED_FOR_SEPARATE_REPOSITORY_MUTATION_AUTHORIZATION"
DENIED = "LIFECYCLE_BOUNDED_REPOSITORY_MUTATION_REVIEW_DENIED"
REJECTED = "LIFECYCLE_BOUNDED_REPOSITORY_MUTATION_REVIEW_REJECTED"
OBJECTIVE = "REVIEW_PROPOSED_REPOSITORY_MUTATION_FOR_SEPARATE_AUTHORIZATION_ONLY"
SOURCE_ORDER_CHECK = "source_state_adoption_precedes_repository_mutation_review_and_deadline_valid"


class Rec(SimpleNamespace):
    def to_dict(self) -> dict[str, Any]:
        out = {}
        for key, value in self.__dict__.items():
            if isinstance(value, tuple):
                out[key] = list(value)
            elif isinstance(value, dict):
                out[key] = dict(value)
            else:
                out[key] = value
        return out


def _digest(value: Rec, field: str) -> str:
    payload = value.to_dict()
    payload.pop(field, None)
    return canonical_digest(payload)


def policy_digest(value: Rec) -> str:
    return _digest(value, "policy_digest")


def evidence_digest(value: Rec) -> str:
    return _digest(value, "evidence_digest")


def review_digest(value: Rec) -> str:
    return _digest(value, "review_digest")


def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")


def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))


def make_policy(
    policy_id: str,
    *,
    allowed_mutation_reviewer_ids: tuple[str, ...],
    allowed_mutation_reviewer_organization_ids: tuple[str, ...],
    max_review_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
    max_mutation_authorization_delay_seconds: int = 900,
) -> Rec:
    value = Rec(
        policy_id=policy_id,
        allowed_mutation_reviewer_ids=_canon(allowed_mutation_reviewer_ids),
        allowed_mutation_reviewer_organization_ids=_canon(
            allowed_mutation_reviewer_organization_ids
        ),
        max_review_delay_seconds=max_review_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_mutation_authorization_delay_seconds=max_mutation_authorization_delay_seconds,
        adopted_source_required=True,
        source_recomputation_required=True,
        repository_review_route_required=True,
        mutation_reviewer_authority_required=True,
        mutation_reviewer_separation_required=True,
        repository_mutation_authorization_route_required_next=True,
        repository_read_only=True,
        file_write_absent_required=True,
        ref_update_absent_required=True,
        branch_move_absent_required=True,
        external_operation_absent_required=True,
        terminal_marker_absent_required=True,
        resource_removal_absent_required=True,
        policy_digest="",
        version=VERSION,
    )
    value.policy_digest = policy_digest(value)
    issues = policy_issues(value)
    if issues:
        raise ValueError("lifecycle_repository_mutation_review_policy_invalid:" + issues[0])
    return value


def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if (
        not value.allowed_mutation_reviewer_ids
        or not value.allowed_mutation_reviewer_organization_ids
    ):
        issues.append("allowed_mutation_reviewer_missing")
    if (
        min(
            value.max_review_delay_seconds,
            value.max_evidence_age_seconds,
            value.max_mutation_authorization_delay_seconds,
        )
        <= 0
    ):
        issues.append("bound_invalid")
    if not all(
        (
            value.repository_read_only,
            value.file_write_absent_required,
            value.ref_update_absent_required,
            value.branch_move_absent_required,
            value.external_operation_absent_required,
            value.terminal_marker_absent_required,
            value.resource_removal_absent_required,
        )
    ):
        issues.append("repository_or_external_guard_disabled")
    if value.policy_digest != policy_digest(value):
        issues.append("policy_digest_mismatch")
    return tuple(issues)


def all_source_digests(
    source_adoption, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]
) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = adoption_source_digests(
        source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:])
    )
    result.update(
        lifecycle_state_adoption=source_adoption.adoption_digest,
        lifecycle_state_adoption_evidence=source_evidence.evidence_digest,
        lifecycle_state_adoption_policy=source_policy.policy_digest,
        lifecycle_state_adoption_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(
    source_adoption, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]
) -> bool:
    return not source_artifact_issues(
        source_record, source_adoption, source_evidence, source_policy, *source_args
    )


def expected_mutation_authorization_route_digest(
    source_adoption,
    source_record,
    *,
    repository_review_id: str,
    mutation_reviewer_id: str,
    proposed_repository_mutation_package_digest: str,
    mutation_authorization_deadline_at_epoch_seconds: int,
) -> str:
    return canonical_digest(
        {
            "source_state_adoption_id": source_adoption.state_adoption_id,
            "source_state_adoption_record_digest": source_record.record_digest,
            "source_repository_review_route_digest": source_adoption.repository_review_route_digest,
            "repository_review_id": repository_review_id,
            "mutation_reviewer_id": mutation_reviewer_id,
            "adopted_lifecycle_state_digest": source_adoption.adopted_lifecycle_state_digest,
            "proposed_repository_mutation_package_digest": proposed_repository_mutation_package_digest,
            "mutation_authorization_deadline_at_epoch_seconds": mutation_authorization_deadline_at_epoch_seconds,
        }
    )


def make_evidence(
    source_adoption,
    source_evidence,
    source_policy,
    source_record,
    source_args: tuple[Any, ...],
    **overrides: Any,
) -> Rec:
    values = dict(
        source_state_adoption_id=source_adoption.state_adoption_id,
        source_state_adoption_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(
            source_adoption, source_evidence, source_policy, source_record, source_args
        ),
        source_state_adopter_id=source_adoption.state_adopter_id,
        source_state_adopter_organization_id=source_adoption.state_adopter_organization_id,
        subject_id=source_adoption.subject_id,
        requester_id=source_adoption.requester_id,
        transition_package_digest=source_adoption.transition_package_digest,
        adopted_lifecycle_state_digest=source_adoption.adopted_lifecycle_state_digest,
        source_repository_review_route_digest=source_adoption.repository_review_route_digest,
        repository_review_deadline_at_epoch_seconds=source_adoption.repository_review_deadline_at_epoch_seconds,
        package_expiry_at_epoch_seconds=source_evidence.package_expiry_at_epoch_seconds,
    )
    values.update(overrides)
    if "mutation_authorization_route_digest" not in values:
        values["mutation_authorization_route_digest"] = expected_mutation_authorization_route_digest(
            source_adoption,
            source_record,
            repository_review_id=values["repository_review_id"],
            mutation_reviewer_id=values["mutation_reviewer_id"],
            proposed_repository_mutation_package_digest=values[
                "proposed_repository_mutation_package_digest"
            ],
            mutation_authorization_deadline_at_epoch_seconds=values[
                "mutation_authorization_deadline_at_epoch_seconds"
            ],
        )
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_repository_mutation_review_evidence_invalid:" + issues[0])
    return value


def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = (
        "evidence_id",
        "repository_review_id",
        "mutation_reviewer_id",
        "mutation_reviewer_organization_id",
        "mutation_reviewer_mandate_receipt_digest",
        "mutation_reviewer_authority_receipt_digest",
        "mutation_reviewer_identity_confirmation_digest",
        "source_state_adoption_id",
        "source_state_adoption_record_digest",
        "source_repository_review_route_digest",
        "proposed_repository_mutation_package_digest",
        "mutation_authorization_route_digest",
        "adopted_lifecycle_state_digest",
        "state_adoption_record_freshness_receipt_digest",
        "adopted_state_freshness_receipt_digest",
        "repository_mutation_package_review_receipt_digest",
        "repository_mutation_package_freshness_receipt_digest",
        "repository_mutation_package_bounded_receipt_digest",
    )
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if (
        min(
            value.review_requested_at_epoch_seconds,
            value.captured_at_epoch_seconds,
            value.reviewed_at_epoch_seconds,
            value.repository_review_deadline_at_epoch_seconds,
            value.mutation_authorization_deadline_at_epoch_seconds,
            value.package_expiry_at_epoch_seconds,
        )
        < 0
    ):
        issues.append("negative_repository_review_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_submission(
    repository_review_id: str,
    mutation_reviewer_id: str,
    mutation_reviewer_organization_id: str,
    review_requested_at_epoch_seconds: int,
    reviewed_at_epoch_seconds: int,
    source_adoption,
    source_record,
    review_evidence: Rec,
    *,
    proposed_repository_mutation_package_digest: str,
    mutation_authorization_route_digest: str,
    mutation_authorization_deadline_at_epoch_seconds: int,
    review_confirmed: bool,
    denial_reason_digest: str = "",
    objective: str = OBJECTIVE,
) -> Rec:
    value = Rec(
        repository_review_id=repository_review_id,
        mutation_reviewer_id=mutation_reviewer_id,
        mutation_reviewer_organization_id=mutation_reviewer_organization_id,
        objective=objective,
        review_requested_at_epoch_seconds=review_requested_at_epoch_seconds,
        reviewed_at_epoch_seconds=reviewed_at_epoch_seconds,
        source_state_adoption_id=source_adoption.state_adoption_id,
        source_state_adoption_record_digest=source_record.record_digest,
        subject_id=source_adoption.subject_id,
        requester_id=source_adoption.requester_id,
        source_state_adopter_id=source_adoption.state_adopter_id,
        transition_package_digest=source_adoption.transition_package_digest,
        adopted_lifecycle_state_digest=source_adoption.adopted_lifecycle_state_digest,
        source_repository_review_route_digest=source_adoption.repository_review_route_digest,
        proposed_repository_mutation_package_digest=proposed_repository_mutation_package_digest,
        mutation_authorization_route_digest=mutation_authorization_route_digest,
        mutation_authorization_deadline_at_epoch_seconds=mutation_authorization_deadline_at_epoch_seconds,
        review_evidence_digest=review_evidence.evidence_digest,
        review_confirmed=review_confirmed,
        denial_reason_digest=denial_reason_digest,
        review_digest="",
        version=VERSION,
    )
    value.review_digest = review_digest(value)
    issues = submission_issues(value)
    if issues:
        raise ValueError("lifecycle_repository_mutation_review_invalid:" + issues[0])
    return value


def submission_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in ("denial_reason_digest", "review_digest", "version", "review_confirmed"):
            continue
        if content == "" or content is None:
            issues.append("required_repository_review_field_missing")
            break
    if not value.review_confirmed and not value.denial_reason_digest:
        issues.append("denial_reason_missing")
    if (
        min(
            value.review_requested_at_epoch_seconds,
            value.reviewed_at_epoch_seconds,
            value.mutation_authorization_deadline_at_epoch_seconds,
        )
        < 0
    ):
        issues.append("negative_repository_review_time")
    if value.review_digest != review_digest(value):
        issues.append("review_digest_mismatch")
    return tuple(issues)


def _source_ready(record) -> bool:
    return all(
        (
            record.status == SOURCE_ADOPTED,
            record.state_adoption_record_issued,
            record.state_adoption_completed,
            record.lifecycle_state_adopted,
            record.lifecycle_transition_performed,
            record.lifecycle_state_changed,
            record.ready_for_separate_repository_mutation_review,
            record.repository_mutation_review_required_next,
            record.repository_mutation_review_route_required_next,
            not record.external_operation_performed,
            not record.repository_changed,
            record.repository_read_only,
        )
    )


def _prior_actor_ids(source_adoption, source_evidence) -> set[str]:
    return {
        source_adoption.subject_id,
        source_adoption.requester_id,
        source_adoption.source_completion_operator_id,
        source_adoption.state_adopter_id,
        source_evidence.source_completion_operator_id,
    }


def evaluate(
    review: Rec,
    evidence: Rec,
    policy: Rec,
    source_adoption,
    source_evidence,
    source_policy,
    source_record,
    source_args: tuple[Any, ...],
) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(
        source_adoption, source_evidence, source_policy, source_record, source_args
    )
    expected_authorization_route = expected_mutation_authorization_route_digest(
        source_adoption,
        source_record,
        repository_review_id=review.repository_review_id,
        mutation_reviewer_id=review.mutation_reviewer_id,
        proposed_repository_mutation_package_digest=review.proposed_repository_mutation_package_digest,
        mutation_authorization_deadline_at_epoch_seconds=review.mutation_authorization_deadline_at_epoch_seconds,
    )
    prior = _prior_actor_ids(source_adoption, source_evidence)
    review_delay = evidence.reviewed_at_epoch_seconds - source_adoption.adopted_at_epoch_seconds
    evidence_age = evidence.reviewed_at_epoch_seconds - evidence.captured_at_epoch_seconds
    authorization_delay = (
        evidence.mutation_authorization_deadline_at_epoch_seconds - evidence.reviewed_at_epoch_seconds
    )
    checks = {
        "policy_valid": not policy_issues(policy),
        "review_valid": not submission_issues(review),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(
            source_adoption, source_evidence, source_policy, source_record, source_args
        ),
        "source_state_adoption_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests
        and review.source_state_adoption_id
        == evidence.source_state_adoption_id
        == source_adoption.state_adoption_id
        and review.source_state_adoption_record_digest
        == evidence.source_state_adoption_record_digest
        == source_record.record_digest,
        "identity_binding_valid": review.repository_review_id
        == evidence.repository_review_id
        and review.mutation_reviewer_id == evidence.mutation_reviewer_id
        and review.mutation_reviewer_organization_id
        == evidence.mutation_reviewer_organization_id
        and review.review_evidence_digest == evidence.evidence_digest,
        "source_repository_review_route_binding_valid": review.source_repository_review_route_digest
        == evidence.source_repository_review_route_digest
        == source_adoption.repository_review_route_digest,
        "mutation_authorization_route_binding_valid": review.mutation_authorization_route_digest
        == evidence.mutation_authorization_route_digest
        == expected_authorization_route,
        "transition_package_binding_valid": review.transition_package_digest
        == evidence.transition_package_digest
        == source_adoption.transition_package_digest,
        "adopted_state_binding_valid": review.adopted_lifecycle_state_digest
        == evidence.adopted_lifecycle_state_digest
        == source_adoption.adopted_lifecycle_state_digest,
        "proposed_repository_mutation_package_binding_valid": review.proposed_repository_mutation_package_digest
        == evidence.proposed_repository_mutation_package_digest,
        "mutation_reviewer_allowed": review.mutation_reviewer_id
        in policy.allowed_mutation_reviewer_ids,
        "mutation_reviewer_organization_allowed": review.mutation_reviewer_organization_id
        in policy.allowed_mutation_reviewer_organization_ids,
        "mutation_reviewer_separated_from_state_adopter": review.mutation_reviewer_id
        != source_adoption.state_adopter_id,
        "mutation_reviewer_separated_from_prior_actors": review.mutation_reviewer_id not in prior,
        "mutation_reviewer_organization_separated": review.mutation_reviewer_organization_id
        != source_adoption.state_adopter_organization_id,
        "objective_allowed": review.objective == OBJECTIVE,
        "review_delay_valid": 0 <= review_delay <= policy.max_review_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "mutation_authorization_delay_valid": 0
        < authorization_delay
        <= policy.max_mutation_authorization_delay_seconds,
        "time_order_valid": source_adoption.adopted_at_epoch_seconds
        <= evidence.review_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.reviewed_at_epoch_seconds
        < evidence.mutation_authorization_deadline_at_epoch_seconds
        <= evidence.package_expiry_at_epoch_seconds,
        "source_repository_review_deadline_valid": evidence.reviewed_at_epoch_seconds
        <= source_adoption.repository_review_deadline_at_epoch_seconds,
        "external_operation_absent": not evidence.external_operation_performed,
        "repository_change_absent": not evidence.repository_changed,
        "file_write_absent": not evidence.file_written,
        "ref_update_absent": not evidence.ref_updated,
        "branch_move_absent": not evidence.branch_moved,
        "terminal_marker_absent": not evidence.terminal_marker_written,
        "resource_removal_absent": not evidence.resource_removed,
        "mutation_reviewer_mandate_verified": evidence.mutation_reviewer_mandate_verified,
        "mutation_reviewer_authority_verified": evidence.mutation_reviewer_authority_verified,
        "mutation_reviewer_identity_confirmed": evidence.mutation_reviewer_identity_confirmed,
        "state_adoption_record_fresh": evidence.state_adoption_record_fresh,
        "adopted_state_not_stale": evidence.adopted_state_not_stale,
        "repository_mutation_package_review_valid": evidence.repository_mutation_package_review_valid,
        "repository_mutation_package_fresh": evidence.repository_mutation_package_fresh,
        "repository_mutation_package_bounded": evidence.repository_mutation_package_bounded,
        "no_unresolved_anomaly": not evidence.unresolved_anomaly_present,
        "recovery_not_in_progress": not evidence.recovery_in_progress,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests


STRUCTURAL_CHECKS = (
    "policy_valid",
    "review_valid",
    "evidence_valid",
    "source_recomputed_valid",
    "source_state_adoption_ready",
    "source_binding_valid",
    "identity_binding_valid",
    "source_repository_review_route_binding_valid",
    "mutation_authorization_route_binding_valid",
    "transition_package_binding_valid",
    "adopted_state_binding_valid",
    "proposed_repository_mutation_package_binding_valid",
    "mutation_reviewer_allowed",
    "mutation_reviewer_organization_allowed",
    "mutation_reviewer_separated_from_state_adopter",
    "mutation_reviewer_separated_from_prior_actors",
    "mutation_reviewer_organization_separated",
    "objective_allowed",
    "review_delay_valid",
    "evidence_fresh",
    "mutation_authorization_delay_valid",
    "time_order_valid",
    "source_repository_review_deadline_valid",
    "external_operation_absent",
    "repository_change_absent",
    "file_write_absent",
    "ref_update_absent",
    "branch_move_absent",
    "terminal_marker_absent",
    "resource_removal_absent",
)

DENIAL_CHECKS = (
    "mutation_reviewer_mandate_verified",
    "mutation_reviewer_authority_verified",
    "mutation_reviewer_identity_confirmed",
    "state_adoption_record_fresh",
    "adopted_state_not_stale",
    "repository_mutation_package_review_valid",
    "repository_mutation_package_fresh",
    "repository_mutation_package_bounded",
    "no_unresolved_anomaly",
    "recovery_not_in_progress",
    "institutional_hold_absent",
    "emergency_state_absent",
)


def compute_artifact(
    review: Rec,
    evidence: Rec,
    policy: Rec,
    source_adoption,
    source_evidence,
    source_policy,
    source_record,
    *source_args: Any,
) -> Rec:
    checks, expected_digests = evaluate(
        review,
        evidence,
        policy,
        source_adoption,
        source_evidence,
        source_policy,
        source_record,
        tuple(source_args),
    )
    checks[SOURCE_ORDER_CHECK] = (
        source_adoption.adopted_at_epoch_seconds
        <= review.review_requested_at_epoch_seconds
        <= review.reviewed_at_epoch_seconds
        <= source_adoption.repository_review_deadline_at_epoch_seconds
    )
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_adoption_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in DENIAL_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = DENIED, failed
        elif review.review_confirmed:
            status, reason = APPROVED, "approved_for_separate_repository_mutation_authorization_only"
        else:
            status, reason = DENIED, "repository_mutation_review_not_confirmed"
    issued = status != REJECTED
    approved = status == APPROVED
    denied = status == DENIED
    artifact = Rec(
        repository_review_id=review.repository_review_id,
        status=status,
        reason=reason,
        mutation_reviewer_id=review.mutation_reviewer_id,
        mutation_reviewer_organization_id=review.mutation_reviewer_organization_id,
        source_state_adoption_id=review.source_state_adoption_id,
        source_state_adoption_record_digest=review.source_state_adoption_record_digest,
        source_state_adopter_id=review.source_state_adopter_id,
        transition_package_digest=review.transition_package_digest,
        adopted_lifecycle_state_digest=review.adopted_lifecycle_state_digest,
        source_repository_review_route_digest=review.source_repository_review_route_digest,
        proposed_repository_mutation_package_digest=review.proposed_repository_mutation_package_digest,
        mutation_authorization_route_digest=review.mutation_authorization_route_digest,
        mutation_authorization_deadline_at_epoch_seconds=review.mutation_authorization_deadline_at_epoch_seconds,
        subject_id=review.subject_id,
        requester_id=review.requester_id,
        policy_digest=policy.policy_digest,
        review_digest=review.review_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_state_adoption_ready=checks["source_state_adoption_ready"],
        repository_mutation_review_record_issued=issued,
        repository_mutation_review_completed=issued,
        repository_mutation_review_approved=approved,
        repository_mutation_review_denied=denied,
        repository_mutation_review_rejected=status == REJECTED,
        ready_for_separate_repository_mutation_authorization=approved,
        repository_mutation_authorization_required_next=approved,
        repository_mutation_authorization_route_required_next=approved,
        repository_mutation_review_replan_required_next=denied,
        repository_mutation_review_replan_route_required_next=denied,
        lifecycle_state_adopted=checks["source_state_adoption_ready"],
        lifecycle_transition_performed=checks["source_state_adoption_ready"],
        lifecycle_state_changed=False,
        repository_mutation_performed=False,
        file_written=False,
        ref_updated=False,
        branch_moved=False,
        authority_changed=False,
        quiescence_state_changed=False,
        terminal_state_changed=False,
        terminal_marker_written=False,
        resource_removed=False,
        external_operation_performed=False,
        repository_changed=False,
        repository_read_only=True,
        record_digest="",
        version=VERSION,
    )
    artifact.record_digest = record_digest(artifact)
    return artifact


def verify_artifact(*args: Any, **kwargs: Any) -> Rec:
    artifact = compute_artifact(*args, **kwargs)
    issues = artifact_issues(artifact, *args, **kwargs)
    if issues:
        raise ValueError("lifecycle_repository_mutation_review_record_invalid:" + issues[0])
    return artifact


def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("repository_mutation_review_recomputation_mismatch")
    if artifact.status not in (APPROVED, DENIED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == APPROVED and not all(
        (
            artifact.repository_mutation_review_record_issued,
            artifact.repository_mutation_review_completed,
            artifact.repository_mutation_review_approved,
            artifact.ready_for_separate_repository_mutation_authorization,
            artifact.repository_mutation_authorization_required_next,
            artifact.repository_mutation_authorization_route_required_next,
            not artifact.repository_mutation_performed,
            not artifact.repository_changed,
        )
    ):
        issues.append("approved_gate_invalid")
    if artifact.status == DENIED and not all(
        (
            artifact.repository_mutation_review_record_issued,
            artifact.repository_mutation_review_completed,
            artifact.repository_mutation_review_denied,
            not artifact.repository_mutation_authorization_required_next,
            artifact.repository_mutation_review_replan_required_next,
        )
    ):
        issues.append("denied_gate_invalid")
    if artifact.status == REJECTED and any(
        (
            artifact.repository_mutation_review_record_issued,
            artifact.repository_mutation_review_completed,
            artifact.repository_mutation_authorization_required_next,
            artifact.repository_mutation_review_replan_required_next,
        )
    ):
        issues.append("rejected_record_issued")
    if any(
        (
            artifact.repository_mutation_performed,
            artifact.file_written,
            artifact.ref_updated,
            artifact.branch_moved,
            artifact.authority_changed,
            artifact.quiescence_state_changed,
            artifact.terminal_state_changed,
            artifact.terminal_marker_written,
            artifact.resource_removed,
            artifact.external_operation_performed,
            artifact.repository_changed,
        )
    ):
        issues.append("repository_or_external_effect_performed")
    if not artifact.repository_read_only:
        issues.append("repository_guard_disabled")
    if artifact.record_digest != record_digest(artifact):
        issues.append("record_digest_mismatch")
    return tuple(issues)
