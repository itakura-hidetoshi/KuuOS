#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_repository_local_frontier_checkpoint_authorization_types_v1_01 import (
    RepositoryCheckpointReferenceObservation,
    RepositoryLocalFrontierCheckpointAuthorizationCertificate,
    RepositoryLocalFrontierCheckpointNonceStatusReceipt,
    RepositoryLocalFrontierCheckpointPolicy,
    RepositoryLocalFrontierCheckpointScope,
)
from runtime.kuuos_repository_local_frontier_checkpoint_authorization_v1_01 import (
    authorize_repository_local_frontier_checkpoint_creation as _authorize,
    repository_local_frontier_checkpoint_authorization_certificate_issues as _issues,
)
from runtime.kuuos_repository_local_frontier_finality_types_v1_00 import (
    RepositoryLocalFrontierFinalityCertificate,
)


def _policy_binding_issues(
    policy: RepositoryLocalFrontierCheckpointPolicy,
    scope: RepositoryLocalFrontierCheckpointScope,
    certificate: RepositoryLocalFrontierCheckpointAuthorizationCertificate | None = None,
) -> tuple[str, ...]:
    issues: list[str] = []
    if scope.authorization_policy_digest != policy.policy_digest:
        issues.append("checkpoint_scope_policy_digest_mismatch")
    if certificate is not None:
        if certificate.authorization_policy_digest != policy.policy_digest:
            issues.append("checkpoint_certificate_policy_digest_mismatch")
        if certificate.checkpoint_scope_digest != scope.scope_digest:
            issues.append("checkpoint_certificate_scope_digest_mismatch")
    return tuple(issues)


def authorize_repository_local_frontier_checkpoint_creation(
    authorization_id: str,
    finality_certificate: RepositoryLocalFrontierFinalityCertificate,
    finality_inputs: Mapping[str, Any],
    policy: RepositoryLocalFrontierCheckpointPolicy,
    observation: RepositoryCheckpointReferenceObservation,
    scope: RepositoryLocalFrontierCheckpointScope,
    nonce_status: RepositoryLocalFrontierCheckpointNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryLocalFrontierCheckpointAuthorizationCertificate:
    binding_issues = _policy_binding_issues(policy, scope)
    if binding_issues:
        raise ValueError(f"checkpoint_policy_binding_invalid:{binding_issues[0]}")
    return _authorize(
        authorization_id,
        finality_certificate,
        finality_inputs,
        policy,
        observation,
        scope,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )


def repository_local_frontier_checkpoint_authorization_certificate_issues(
    certificate: RepositoryLocalFrontierCheckpointAuthorizationCertificate,
    finality_certificate: RepositoryLocalFrontierFinalityCertificate,
    finality_inputs: Mapping[str, Any],
    policy: RepositoryLocalFrontierCheckpointPolicy,
    observation: RepositoryCheckpointReferenceObservation,
    scope: RepositoryLocalFrontierCheckpointScope,
    nonce_status: RepositoryLocalFrontierCheckpointNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    binding_issues = _policy_binding_issues(policy, scope, certificate)
    if binding_issues:
        return binding_issues
    return _issues(
        certificate,
        finality_certificate,
        finality_inputs,
        policy,
        observation,
        scope,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )


__all__ = (
    "authorize_repository_local_frontier_checkpoint_creation",
    "repository_local_frontier_checkpoint_authorization_certificate_issues",
)
