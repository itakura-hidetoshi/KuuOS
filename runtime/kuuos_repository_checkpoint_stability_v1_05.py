#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_repository_checkpoint_stability_types_v1_05 import (
    FAILURE_CHECKPOINT_LOST,
    FAILURE_CHECKPOINT_SUBSTITUTED,
    FAILURE_EVIDENCE_INVALID,
    FAILURE_NAME_CONFLICT,
    FAILURE_NONE,
    FAILURE_UNREACHABLE,
    FAILURE_UNSTABLE_WINDOW,
    STABILITY_CONFIRMED,
    STABILITY_REJECTED,
    repository_checkpoint_stability_certificate_digest,
)
from runtime.v105_checkpoint_stability_core import (
    construct_repository_checkpoint_stability_certificate,
)
from runtime.v105_checkpoint_stability_delayed import (
    build_repository_delayed_checkpoint_observation,
    repository_delayed_checkpoint_observation_issues,
)
from runtime.v105_checkpoint_stability_namespace import (
    build_repository_checkpoint_namespace_observation,
)
from runtime.v105_checkpoint_stability_namespace_validation import (
    repository_checkpoint_namespace_observation_issues,
)
from runtime.v105_checkpoint_stability_policy import (
    build_repository_checkpoint_stability_policy,
    repository_checkpoint_stability_policy_issues,
)
from runtime.v105_checkpoint_stability_reachability import (
    build_repository_checkpoint_reachability_observation,
)
from runtime.v105_checkpoint_stability_reachability_validation import (
    repository_checkpoint_reachability_observation_issues,
)

_FAILURE_KINDS = {
    FAILURE_NONE,
    FAILURE_EVIDENCE_INVALID,
    FAILURE_CHECKPOINT_LOST,
    FAILURE_CHECKPOINT_SUBSTITUTED,
    FAILURE_NAME_CONFLICT,
    FAILURE_UNREACHABLE,
    FAILURE_UNSTABLE_WINDOW,
}


def certify_repository_checkpoint_stability(
    certificate_id: str,
    creation_receipt,
    v103_context: Mapping[str, Any],
    policy,
    delayed_observation,
    reachability_observation,
    namespace_observation,
    *,
    evaluated_at_epoch_seconds: int,
):
    if not certificate_id:
        raise ValueError("checkpoint_stability_certificate_id_missing")
    if evaluated_at_epoch_seconds < 0:
        raise ValueError("checkpoint_stability_evaluation_time_negative")
    for issues, prefix in (
        (
            repository_checkpoint_stability_policy_issues(policy),
            "checkpoint_stability_policy_invalid",
        ),
        (
            repository_delayed_checkpoint_observation_issues(delayed_observation),
            "delayed_checkpoint_observation_invalid",
        ),
        (
            repository_checkpoint_reachability_observation_issues(
                reachability_observation
            ),
            "checkpoint_reachability_observation_invalid",
        ),
        (
            repository_checkpoint_namespace_observation_issues(
                namespace_observation
            ),
            "checkpoint_namespace_observation_invalid",
        ),
    ):
        if issues:
            raise ValueError(f"{prefix}:{issues[0]}")
    certificate = construct_repository_checkpoint_stability_certificate(
        certificate_id,
        creation_receipt,
        v103_context,
        policy,
        delayed_observation,
        reachability_observation,
        namespace_observation,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues = repository_checkpoint_stability_certificate_issues(
        certificate,
        creation_receipt,
        v103_context,
        policy,
        delayed_observation,
        reachability_observation,
        namespace_observation,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"checkpoint_stability_certificate_invalid:{issues[0]}")
    return certificate


def repository_checkpoint_stability_certificate_issues(
    certificate,
    creation_receipt,
    v103_context: Mapping[str, Any],
    policy,
    delayed_observation,
    reachability_observation,
    namespace_observation,
    *,
    evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    expected = construct_repository_checkpoint_stability_certificate(
        certificate.certificate_id,
        creation_receipt,
        v103_context,
        policy,
        delayed_observation,
        reachability_observation,
        namespace_observation,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues: list[str] = []
    if certificate.to_dict() != expected.to_dict():
        issues.append("checkpoint_stability_recomputation_mismatch")
    if certificate.status not in (STABILITY_CONFIRMED, STABILITY_REJECTED):
        issues.append("checkpoint_stability_status_invalid")
    if certificate.failure_kind not in _FAILURE_KINDS:
        issues.append("checkpoint_stability_failure_kind_invalid")
    if certificate.status == STABILITY_CONFIRMED:
        if certificate.failure_kind != FAILURE_NONE:
            issues.append("checkpoint_stability_confirmed_with_failure")
        if not certificate.checks.get("checkpoint_stability_confirmed", False):
            issues.append("checkpoint_stability_confirmation_missing")
    forbidden_claims = (
        "checkpoint_overwrite_authorized",
        "checkpoint_delete_authorized",
        "force_update_authorized",
        "restore_authorized",
        "recovery_authorized",
        "branch_update_authorized",
        "tag_update_authorized",
        "remote_reference_update_authorized",
        "push_authorized",
        "certificate_performed_reference_mutation",
        "certificate_performed_object_write",
        "certificate_invoked_live_git_command",
        "certificate_mutated_live_repository",
    )
    if any(certificate.checks.get(key, False) for key in forbidden_claims):
        issues.append("checkpoint_stability_forbidden_claim")
    if (
        certificate.certificate_digest
        != repository_checkpoint_stability_certificate_digest(certificate)
    ):
        issues.append("checkpoint_stability_certificate_digest_mismatch")
    return tuple(issues)


__all__ = [
    "build_repository_checkpoint_stability_policy",
    "build_repository_delayed_checkpoint_observation",
    "build_repository_checkpoint_reachability_observation",
    "build_repository_checkpoint_namespace_observation",
    "repository_checkpoint_stability_policy_issues",
    "repository_delayed_checkpoint_observation_issues",
    "repository_checkpoint_reachability_observation_issues",
    "repository_checkpoint_namespace_observation_issues",
    "certify_repository_checkpoint_stability",
    "repository_checkpoint_stability_certificate_issues",
]
