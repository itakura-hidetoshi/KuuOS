#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_repository_atomic_application_types_v0_92 import (
    RepositoryAtomicApplicationReceipt,
)
from runtime.kuuos_repository_commit_candidate_types_v0_93 import (
    RepositoryCommitCandidateCertificate,
    RepositoryCommitCandidatePolicy,
    RepositoryParentTreeInventory,
)
from runtime.kuuos_repository_object_materialization_authorization_types_v0_94 import (
    RepositoryObjectDatabaseObservation,
    RepositoryObjectMaterializationAuthorizationCertificate,
    RepositoryObjectMaterializationAuthorizationPolicy,
    RepositoryObjectMaterializationNonceStatusReceipt,
    RepositoryObjectMaterializationScope,
)
from runtime.kuuos_repository_object_materialization_authorization_v0_94 import (
    authorize_repository_object_materialization as _authorize,
    repository_object_materialization_authorization_certificate_issues as _issues,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot


def authorize_repository_object_materialization(
    authorization_id: str,
    candidate_certificate: RepositoryCommitCandidateCertificate,
    application_receipt: RepositoryAtomicApplicationReceipt,
    snapshot: RepositorySnapshot,
    parent_tree_inventory: RepositoryParentTreeInventory,
    candidate_policy: RepositoryCommitCandidatePolicy,
    policy: RepositoryObjectMaterializationAuthorizationPolicy,
    scope: RepositoryObjectMaterializationScope,
    observation: RepositoryObjectDatabaseObservation,
    nonce_status: RepositoryObjectMaterializationNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryObjectMaterializationAuthorizationCertificate:
    certificate = _authorize(
        authorization_id,
        candidate_certificate,
        application_receipt,
        snapshot,
        parent_tree_inventory,
        candidate_policy,
        policy,
        scope,
        observation,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues = repository_object_materialization_authorization_certificate_issues(
        certificate,
        candidate_certificate,
        application_receipt,
        snapshot,
        parent_tree_inventory,
        candidate_policy,
        policy,
        scope,
        observation,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"object_materialization_certificate_invalid:{issues[0]}")
    return certificate


def repository_object_materialization_authorization_certificate_issues(
    certificate: RepositoryObjectMaterializationAuthorizationCertificate,
    candidate_certificate: RepositoryCommitCandidateCertificate,
    application_receipt: RepositoryAtomicApplicationReceipt,
    snapshot: RepositorySnapshot,
    parent_tree_inventory: RepositoryParentTreeInventory,
    candidate_policy: RepositoryCommitCandidatePolicy,
    policy: RepositoryObjectMaterializationAuthorizationPolicy,
    scope: RepositoryObjectMaterializationScope,
    observation: RepositoryObjectDatabaseObservation,
    nonce_status: RepositoryObjectMaterializationNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    return _issues(
        certificate,
        candidate_certificate,
        application_receipt,
        snapshot,
        parent_tree_inventory,
        candidate_policy,
        policy,
        scope,
        observation,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
