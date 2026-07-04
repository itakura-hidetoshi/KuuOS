#!/usr/bin/env python3
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_lifecycle_governance_repository_mutation_review_v0_26 import (
    APPROVED as SOURCE_APPROVED,
    artifact_issues as source_artifact_issues,
    all_source_digests as review_source_digests,
)

VERSION = "kuuos_lifecycle_bounded_repository_mutation_authorization_v0_27"
AUTHORIZED = "LIFECYCLE_BOUNDED_REPOSITORY_MUTATION_AUTHORIZATION_AUTHORIZED_FOR_SEPARATE_REPOSITORY_MUTATION_EXECUTION_PREPARATION"
DENIED = "LIFECYCLE_BOUNDED_REPOSITORY_MUTATION_AUTHORIZATION_DENIED"
REJECTED = "LIFECYCLE_BOUNDED_REPOSITORY_MUTATION_AUTHORIZATION_REJECTED"
OBJECTIVE = "AUTHORIZE_REPOSITORY_MUTATION_FOR_SEPARATE_EXECUTION_PREPARATION_ONLY"
SOURCE_ORDER_CHECK = "source_repository_mutation_review_precedes_authorization_and_deadline_valid"


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


def authorization_digest(value: Rec) -> str:
    return _digest(value, "authorization_digest")


def record_digest(value: Rec) -> str:
    return _digest(value, "record_digest")


def _canon(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(items)))


def make_policy(
    policy_id: str,
    *,
    allowed_authorizer_ids: tuple[str, ...],
    allowed_authorizer_organization_ids: tuple[str, ...],
    max_authorization_delay_seconds: int = 900,
    max_evidence_age_seconds: int = 300,
    max_execution_preparation_delay_seconds: int = 900,
) -> Rec:
    value = Rec(
        policy_id=policy_id,
        allowed_authorizer_ids=_canon(allowed_authorizer_ids),
        allowed_authorizer_organization_ids=_canon(allowed_authorizer_organization_ids),
        max_authorization_delay_seconds=max_authorization_delay_seconds,
        max_evidence_age_seconds=max_evidence_age_seconds,
        max_execution_preparation_delay_seconds=max_execution_preparation_delay_seconds,
        approved_source_required=True,
        source_recomputation_required=True,
        mutation_authorization_route_required=True,
        authorizer_authority_required=True,
        authorizer_separation_required=True,
        execution_preparation_route_required_next=True,
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
        raise ValueError("lifecycle_repository_mutation_authorization_policy_invalid:" + issues[0])
    return value


def policy_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    if not value.policy_id:
        issues.append("policy_id_missing")
    if not value.allowed_authorizer_ids or not value.allowed_authorizer_organization_ids:
        issues.append("allowed_authorizer_missing")
    if (
        min(
            value.max_authorization_delay_seconds,
            value.max_evidence_age_seconds,
            value.max_execution_preparation_delay_seconds,
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
    source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]
) -> dict[str, str]:
    if len(source_args) < 4:
        raise ValueError("source_argument_count_invalid")
    result = review_source_digests(
        source_args[0], source_args[1], source_args[2], source_args[3], tuple(source_args[4:])
    )
    result.update(
        lifecycle_repository_mutation_review=source_review.review_digest,
        lifecycle_repository_mutation_review_evidence=source_evidence.evidence_digest,
        lifecycle_repository_mutation_review_policy=source_policy.policy_digest,
        lifecycle_repository_mutation_review_record=source_record.record_digest,
    )
    return result


def source_recomputed_valid(
    source_review, source_evidence, source_policy, source_record, source_args: tuple[Any, ...]
) -> bool:
    return not source_artifact_issues(
        source_record, source_review, source_evidence, source_policy, *source_args
    )


def expected_execution_preparation_route_digest(
    source_review,
    source_record,
    *,
    authorization_id: str,
    authorizer_id: str,
    proposed_repository_mutation_package_digest: str,
    execution_preparation_deadline_at_epoch_seconds: int,
) -> str:
    return canonical_digest(
        {
            "source_repository_review_id": source_review.repository_review_id,
            "source_repository_review_record_digest": source_record.record_digest,
            "source_mutation_authorization_route_digest": source_review.mutation_authorization_route_digest,
            "authorization_id": authorization_id,
            "authorizer_id": authorizer_id,
            "adopted_lifecycle_state_digest": source_review.adopted_lifecycle_state_digest,
            "proposed_repository_mutation_package_digest": proposed_repository_mutation_package_digest,
            "execution_preparation_deadline_at_epoch_seconds": execution_preparation_deadline_at_epoch_seconds,
        }
    )


def make_evidence(
    source_review,
    source_evidence,
    source_policy,
    source_record,
    source_args: tuple[Any, ...],
    **overrides: Any,
) -> Rec:
    values = dict(
        source_repository_review_id=source_review.repository_review_id,
        source_repository_review_record_digest=source_record.record_digest,
        source_artifact_digests=all_source_digests(
            source_review, source_evidence, source_policy, source_record, source_args
        ),
        source_mutation_reviewer_id=source_review.mutation_reviewer_id,
        source_mutation_reviewer_organization_id=source_review.mutation_reviewer_organization_id,
        subject_id=source_review.subject_id,
        requester_id=source_review.requester_id,
        transition_package_digest=source_review.transition_package_digest,
        adopted_lifecycle_state_digest=source_review.adopted_lifecycle_state_digest,
        proposed_repository_mutation_package_digest=source_review.proposed_repository_mutation_package_digest,
        source_mutation_authorization_route_digest=source_review.mutation_authorization_route_digest,
        mutation_authorization_deadline_at_epoch_seconds=source_review.mutation_authorization_deadline_at_epoch_seconds,
        package_expiry_at_epoch_seconds=source_evidence.package_expiry_at_epoch_seconds,
    )
    values.update(overrides)
    if "execution_preparation_route_digest" not in values:
        values["execution_preparation_route_digest"] = expected_execution_preparation_route_digest(
            source_review,
            source_record,
            authorization_id=values["authorization_id"],
            authorizer_id=values["authorizer_id"],
            proposed_repository_mutation_package_digest=values[
                "proposed_repository_mutation_package_digest"
            ],
            execution_preparation_deadline_at_epoch_seconds=values[
                "execution_preparation_deadline_at_epoch_seconds"
            ],
        )
    value = Rec(version=VERSION, evidence_digest="", **values)
    value.evidence_digest = evidence_digest(value)
    issues = evidence_issues(value)
    if issues:
        raise ValueError("lifecycle_repository_mutation_authorization_evidence_invalid:" + issues[0])
    return value


def evidence_issues(value: Rec) -> tuple[str, ...]:
    required = (
        "evidence_id",
        "authorization_id",
        "authorizer_id",
        "authorizer_organization_id",
        "authorizer_mandate_receipt_digest",
        "authorizer_authority_receipt_digest",
        "authorizer_identity_confirmation_digest",
        "source_repository_review_id",
        "source_repository_review_record_digest",
        "source_mutation_authorization_route_digest",
        "execution_preparation_route_digest",
        "proposed_repository_mutation_package_digest",
        "adopted_lifecycle_state_digest",
        "repository_review_record_freshness_receipt_digest",
        "authorization_receipt_digest",
        "repository_mutation_package_freshness_receipt_digest",
        "repository_mutation_package_bounded_receipt_digest",
        "adopted_state_freshness_receipt_digest",
    )
    issues = []
    if not all(getattr(value, name, None) for name in required):
        issues.append("required_evidence_field_missing")
    if (
        min(
            value.authorization_requested_at_epoch_seconds,
            value.captured_at_epoch_seconds,
            value.authorized_at_epoch_seconds,
            value.mutation_authorization_deadline_at_epoch_seconds,
            value.execution_preparation_deadline_at_epoch_seconds,
            value.package_expiry_at_epoch_seconds,
        )
        < 0
    ):
        issues.append("negative_authorization_time")
    if value.evidence_digest != evidence_digest(value):
        issues.append("evidence_digest_mismatch")
    return tuple(issues)


def make_submission(
    authorization_id: str,
    authorizer_id: str,
    authorizer_organization_id: str,
    authorization_requested_at_epoch_seconds: int,
    authorized_at_epoch_seconds: int,
    source_review,
    source_record,
    authorization_evidence: Rec,
    *,
    proposed_repository_mutation_package_digest: str,
    execution_preparation_route_digest: str,
    execution_preparation_deadline_at_epoch_seconds: int,
    authorization_confirmed: bool,
    denial_reason_digest: str = "",
    objective: str = OBJECTIVE,
) -> Rec:
    value = Rec(
        authorization_id=authorization_id,
        authorizer_id=authorizer_id,
        authorizer_organization_id=authorizer_organization_id,
        objective=objective,
        authorization_requested_at_epoch_seconds=authorization_requested_at_epoch_seconds,
        authorized_at_epoch_seconds=authorized_at_epoch_seconds,
        source_repository_review_id=source_review.repository_review_id,
        source_repository_review_record_digest=source_record.record_digest,
        subject_id=source_review.subject_id,
        requester_id=source_review.requester_id,
        source_mutation_reviewer_id=source_review.mutation_reviewer_id,
        transition_package_digest=source_review.transition_package_digest,
        adopted_lifecycle_state_digest=source_review.adopted_lifecycle_state_digest,
        source_mutation_authorization_route_digest=source_review.mutation_authorization_route_digest,
        proposed_repository_mutation_package_digest=proposed_repository_mutation_package_digest,
        execution_preparation_route_digest=execution_preparation_route_digest,
        execution_preparation_deadline_at_epoch_seconds=execution_preparation_deadline_at_epoch_seconds,
        authorization_evidence_digest=authorization_evidence.evidence_digest,
        authorization_confirmed=authorization_confirmed,
        denial_reason_digest=denial_reason_digest,
        authorization_digest="",
        version=VERSION,
    )
    value.authorization_digest = authorization_digest(value)
    issues = submission_issues(value)
    if issues:
        raise ValueError("lifecycle_repository_mutation_authorization_invalid:" + issues[0])
    return value


def submission_issues(value: Rec) -> tuple[str, ...]:
    issues = []
    for name, content in value.to_dict().items():
        if name in (
            "denial_reason_digest",
            "authorization_digest",
            "version",
            "authorization_confirmed",
        ):
            continue
        if content == "" or content is None:
            issues.append("required_authorization_field_missing")
            break
    if not value.authorization_confirmed and not value.denial_reason_digest:
        issues.append("denial_reason_missing")
    if (
        min(
            value.authorization_requested_at_epoch_seconds,
            value.authorized_at_epoch_seconds,
            value.execution_preparation_deadline_at_epoch_seconds,
        )
        < 0
    ):
        issues.append("negative_authorization_time")
    if value.authorization_digest != authorization_digest(value):
        issues.append("authorization_digest_mismatch")
    return tuple(issues)


def _source_ready(record) -> bool:
    return all(
        (
            record.status == SOURCE_APPROVED,
            record.repository_mutation_review_record_issued,
            record.repository_mutation_review_completed,
            record.repository_mutation_review_approved,
            record.ready_for_separate_repository_mutation_authorization,
            record.repository_mutation_authorization_required_next,
            record.repository_mutation_authorization_route_required_next,
            not record.repository_mutation_performed,
            not record.file_written,
            not record.ref_updated,
            not record.branch_moved,
            not record.external_operation_performed,
            not record.repository_changed,
            record.repository_read_only,
        )
    )


def _prior_actor_ids(source_review, source_evidence) -> set[str]:
    return {
        source_review.subject_id,
        source_review.requester_id,
        source_review.source_state_adopter_id,
        source_review.mutation_reviewer_id,
        source_evidence.source_state_adopter_id,
    }


def evaluate(
    authorization: Rec,
    evidence: Rec,
    policy: Rec,
    source_review,
    source_evidence,
    source_policy,
    source_record,
    source_args: tuple[Any, ...],
) -> tuple[dict[str, bool], dict[str, str]]:
    expected_digests = all_source_digests(
        source_review, source_evidence, source_policy, source_record, source_args
    )
    expected_execution_route = expected_execution_preparation_route_digest(
        source_review,
        source_record,
        authorization_id=authorization.authorization_id,
        authorizer_id=authorization.authorizer_id,
        proposed_repository_mutation_package_digest=authorization.proposed_repository_mutation_package_digest,
        execution_preparation_deadline_at_epoch_seconds=authorization.execution_preparation_deadline_at_epoch_seconds,
    )
    prior = _prior_actor_ids(source_review, source_evidence)
    authorization_delay = evidence.authorized_at_epoch_seconds - source_review.reviewed_at_epoch_seconds
    evidence_age = evidence.authorized_at_epoch_seconds - evidence.captured_at_epoch_seconds
    execution_preparation_delay = (
        evidence.execution_preparation_deadline_at_epoch_seconds - evidence.authorized_at_epoch_seconds
    )
    checks = {
        "policy_valid": not policy_issues(policy),
        "authorization_valid": not submission_issues(authorization),
        "evidence_valid": not evidence_issues(evidence),
        "source_recomputed_valid": source_recomputed_valid(
            source_review, source_evidence, source_policy, source_record, source_args
        ),
        "source_repository_mutation_review_ready": _source_ready(source_record),
        "source_binding_valid": evidence.source_artifact_digests == expected_digests
        and authorization.source_repository_review_id
        == evidence.source_repository_review_id
        == source_review.repository_review_id
        and authorization.source_repository_review_record_digest
        == evidence.source_repository_review_record_digest
        == source_record.record_digest,
        "identity_binding_valid": authorization.authorization_id == evidence.authorization_id
        and authorization.authorizer_id == evidence.authorizer_id
        and authorization.authorizer_organization_id == evidence.authorizer_organization_id
        and authorization.authorization_evidence_digest == evidence.evidence_digest,
        "source_mutation_authorization_route_binding_valid": authorization.source_mutation_authorization_route_digest
        == evidence.source_mutation_authorization_route_digest
        == source_review.mutation_authorization_route_digest,
        "execution_preparation_route_binding_valid": authorization.execution_preparation_route_digest
        == evidence.execution_preparation_route_digest
        == expected_execution_route,
        "transition_package_binding_valid": authorization.transition_package_digest
        == evidence.transition_package_digest
        == source_review.transition_package_digest,
        "adopted_state_binding_valid": authorization.adopted_lifecycle_state_digest
        == evidence.adopted_lifecycle_state_digest
        == source_review.adopted_lifecycle_state_digest,
        "proposed_repository_mutation_package_binding_valid": authorization.proposed_repository_mutation_package_digest
        == evidence.proposed_repository_mutation_package_digest
        == source_review.proposed_repository_mutation_package_digest,
        "authorizer_allowed": authorization.authorizer_id in policy.allowed_authorizer_ids,
        "authorizer_organization_allowed": authorization.authorizer_organization_id
        in policy.allowed_authorizer_organization_ids,
        "authorizer_separated_from_reviewer": authorization.authorizer_id
        != source_review.mutation_reviewer_id,
        "authorizer_separated_from_prior_actors": authorization.authorizer_id not in prior,
        "authorizer_organization_separated": authorization.authorizer_organization_id
        != source_review.mutation_reviewer_organization_id,
        "objective_allowed": authorization.objective == OBJECTIVE,
        "authorization_delay_valid": 0
        <= authorization_delay
        <= policy.max_authorization_delay_seconds,
        "evidence_fresh": 0 <= evidence_age <= policy.max_evidence_age_seconds,
        "execution_preparation_delay_valid": 0
        < execution_preparation_delay
        <= policy.max_execution_preparation_delay_seconds,
        "time_order_valid": source_review.reviewed_at_epoch_seconds
        <= evidence.authorization_requested_at_epoch_seconds
        <= evidence.captured_at_epoch_seconds
        <= evidence.authorized_at_epoch_seconds
        < evidence.execution_preparation_deadline_at_epoch_seconds
        <= evidence.package_expiry_at_epoch_seconds,
        "source_authorization_deadline_valid": evidence.authorized_at_epoch_seconds
        <= source_review.mutation_authorization_deadline_at_epoch_seconds,
        "external_operation_absent": not evidence.external_operation_performed,
        "repository_change_absent": not evidence.repository_changed,
        "file_write_absent": not evidence.file_written,
        "ref_update_absent": not evidence.ref_updated,
        "branch_move_absent": not evidence.branch_moved,
        "terminal_marker_absent": not evidence.terminal_marker_written,
        "resource_removal_absent": not evidence.resource_removed,
        "authorizer_mandate_verified": evidence.authorizer_mandate_verified,
        "authorizer_authority_verified": evidence.authorizer_authority_verified,
        "authorizer_identity_confirmed": evidence.authorizer_identity_confirmed,
        "repository_review_record_fresh": evidence.repository_review_record_fresh,
        "authorization_receipt_valid": evidence.authorization_receipt_valid,
        "repository_mutation_package_fresh": evidence.repository_mutation_package_fresh,
        "repository_mutation_package_bounded": evidence.repository_mutation_package_bounded,
        "adopted_state_not_stale": evidence.adopted_state_not_stale,
        "no_unresolved_anomaly": not evidence.unresolved_anomaly_present,
        "recovery_not_in_progress": not evidence.recovery_in_progress,
        "institutional_hold_absent": not evidence.institutional_hold_active,
        "emergency_state_absent": not evidence.emergency_state_active,
    }
    return checks, expected_digests


STRUCTURAL_CHECKS = (
    "policy_valid",
    "authorization_valid",
    "evidence_valid",
    "source_recomputed_valid",
    "source_repository_mutation_review_ready",
    "source_binding_valid",
    "identity_binding_valid",
    "source_mutation_authorization_route_binding_valid",
    "execution_preparation_route_binding_valid",
    "transition_package_binding_valid",
    "adopted_state_binding_valid",
    "proposed_repository_mutation_package_binding_valid",
    "authorizer_allowed",
    "authorizer_organization_allowed",
    "authorizer_separated_from_reviewer",
    "authorizer_separated_from_prior_actors",
    "authorizer_organization_separated",
    "objective_allowed",
    "authorization_delay_valid",
    "evidence_fresh",
    "execution_preparation_delay_valid",
    "time_order_valid",
    "source_authorization_deadline_valid",
    "external_operation_absent",
    "repository_change_absent",
    "file_write_absent",
    "ref_update_absent",
    "branch_move_absent",
    "terminal_marker_absent",
    "resource_removal_absent",
)

DENIAL_CHECKS = (
    "authorizer_mandate_verified",
    "authorizer_authority_verified",
    "authorizer_identity_confirmed",
    "repository_review_record_fresh",
    "authorization_receipt_valid",
    "repository_mutation_package_fresh",
    "repository_mutation_package_bounded",
    "adopted_state_not_stale",
    "no_unresolved_anomaly",
    "recovery_not_in_progress",
    "institutional_hold_absent",
    "emergency_state_absent",
)


def compute_artifact(
    authorization: Rec,
    evidence: Rec,
    policy: Rec,
    source_review,
    source_evidence,
    source_policy,
    source_record,
    *source_args: Any,
) -> Rec:
    checks, expected_digests = evaluate(
        authorization,
        evidence,
        policy,
        source_review,
        source_evidence,
        source_policy,
        source_record,
        tuple(source_args),
    )
    checks[SOURCE_ORDER_CHECK] = (
        source_review.reviewed_at_epoch_seconds
        <= authorization.authorization_requested_at_epoch_seconds
        <= authorization.authorized_at_epoch_seconds
        <= source_review.mutation_authorization_deadline_at_epoch_seconds
    )
    if not checks[SOURCE_ORDER_CHECK] or not all(checks[name] for name in STRUCTURAL_CHECKS):
        status, reason = REJECTED, "source_review_policy_route_or_binding_invalid"
    else:
        failed = next((name for name in DENIAL_CHECKS if not checks[name]), None)
        if failed is not None:
            status, reason = DENIED, failed
        elif authorization.authorization_confirmed:
            status, reason = AUTHORIZED, "authorized_for_separate_repository_mutation_execution_preparation_only"
        else:
            status, reason = DENIED, "repository_mutation_authorization_not_confirmed"
    issued = status != REJECTED
    authorized = status == AUTHORIZED
    denied = status == DENIED
    artifact = Rec(
        authorization_id=authorization.authorization_id,
        status=status,
        reason=reason,
        authorizer_id=authorization.authorizer_id,
        authorizer_organization_id=authorization.authorizer_organization_id,
        source_repository_review_id=authorization.source_repository_review_id,
        source_repository_review_record_digest=authorization.source_repository_review_record_digest,
        source_mutation_reviewer_id=authorization.source_mutation_reviewer_id,
        transition_package_digest=authorization.transition_package_digest,
        adopted_lifecycle_state_digest=authorization.adopted_lifecycle_state_digest,
        source_mutation_authorization_route_digest=authorization.source_mutation_authorization_route_digest,
        proposed_repository_mutation_package_digest=authorization.proposed_repository_mutation_package_digest,
        execution_preparation_route_digest=authorization.execution_preparation_route_digest,
        execution_preparation_deadline_at_epoch_seconds=authorization.execution_preparation_deadline_at_epoch_seconds,
        subject_id=authorization.subject_id,
        requester_id=authorization.requester_id,
        policy_digest=policy.policy_digest,
        authorization_digest=authorization.authorization_digest,
        evidence_digest=evidence.evidence_digest,
        checks=checks,
        evidence_digests=expected_digests,
        source_repository_mutation_review_ready=checks["source_repository_mutation_review_ready"],
        repository_mutation_authorization_record_issued=issued,
        repository_mutation_authorization_completed=issued,
        repository_mutation_authorized=authorized,
        repository_mutation_authorization_denied=denied,
        repository_mutation_authorization_rejected=status == REJECTED,
        ready_for_separate_repository_mutation_execution_preparation=authorized,
        repository_mutation_execution_preparation_required_next=authorized,
        repository_mutation_execution_preparation_route_required_next=authorized,
        repository_mutation_authorization_replan_required_next=denied,
        repository_mutation_authorization_replan_route_required_next=denied,
        repository_mutation_performed=False,
        repository_mutation_execution_prepared=False,
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
        raise ValueError("lifecycle_repository_mutation_authorization_record_invalid:" + issues[0])
    return artifact


def artifact_issues(artifact: Rec, *args: Any, **kwargs: Any) -> tuple[str, ...]:
    expected = compute_artifact(*args, **kwargs)
    issues = []
    if artifact.to_dict() != expected.to_dict():
        issues.append("repository_mutation_authorization_recomputation_mismatch")
    if artifact.status not in (AUTHORIZED, DENIED, REJECTED):
        issues.append("status_invalid")
    if artifact.status == AUTHORIZED and not all(
        (
            artifact.repository_mutation_authorization_record_issued,
            artifact.repository_mutation_authorization_completed,
            artifact.repository_mutation_authorized,
            artifact.ready_for_separate_repository_mutation_execution_preparation,
            artifact.repository_mutation_execution_preparation_required_next,
            artifact.repository_mutation_execution_preparation_route_required_next,
            not artifact.repository_mutation_performed,
            not artifact.repository_changed,
        )
    ):
        issues.append("authorized_gate_invalid")
    if artifact.status == DENIED and not all(
        (
            artifact.repository_mutation_authorization_record_issued,
            artifact.repository_mutation_authorization_completed,
            artifact.repository_mutation_authorization_denied,
            not artifact.repository_mutation_execution_preparation_required_next,
            artifact.repository_mutation_authorization_replan_required_next,
        )
    ):
        issues.append("denied_gate_invalid")
    if artifact.status == REJECTED and any(
        (
            artifact.repository_mutation_authorization_record_issued,
            artifact.repository_mutation_authorization_completed,
            artifact.repository_mutation_execution_preparation_required_next,
            artifact.repository_mutation_authorization_replan_required_next,
        )
    ):
        issues.append("rejected_record_issued")
    if any(
        (
            artifact.repository_mutation_performed,
            artifact.repository_mutation_execution_prepared,
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
