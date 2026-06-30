#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_restore_authorization_v1_06"
AUTHORIZATION_GRANTED = "REPOSITORY_CHECKPOINT_RESTORE_AUTHORIZATION_GRANTED"
AUTHORIZATION_REJECTED = "REPOSITORY_CHECKPOINT_RESTORE_AUTHORIZATION_REJECTED"

DECISION_APPROVE = "APPROVE_RESTORE"
DECISION_REJECT = "REJECT_RESTORE"

FAILURE_NONE = "NONE"
FAILURE_EVIDENCE_INVALID = "EVIDENCE_INVALID"
FAILURE_STABILITY_NOT_ELIGIBLE = "STABILITY_DISPOSITION_NOT_ELIGIBLE"
FAILURE_CURRENT_STATE_MISMATCH = "CURRENT_CHECKPOINT_STATE_MISMATCH"
FAILURE_SCOPE_INVALID = "RESTORE_SCOPE_INVALID"
FAILURE_APPROVAL_INVALID = "HUMAN_APPROVAL_INVALID"
FAILURE_NONCE_INVALID = "RESTORE_NONCE_INVALID"
FAILURE_EXECUTOR_UNAUTHORIZED = "RESTORE_EXECUTOR_UNAUTHORIZED"
FAILURE_EXPIRED = "RESTORE_AUTHORIZATION_EXPIRED"

ZERO_OID = "0" * 40
ELIGIBLE_STABILITY_FAILURES = (
    "CHECKPOINT_LOST",
    "CHECKPOINT_SUBSTITUTED",
)


@dataclass(frozen=True)
class RepositoryCheckpointRestorePolicy:
    policy_id: str
    allowed_repository_ids: tuple[str, ...]
    allowed_checkpoint_references: tuple[str, ...]
    authorized_observer_ids: tuple[str, ...]
    authorized_approver_ids: tuple[str, ...]
    authorized_approver_classes: tuple[str, ...]
    authorized_executor_ids: tuple[str, ...]
    authorized_nonce_authority_ids: tuple[str, ...]
    max_authorization_lifetime_seconds: int
    max_observation_age_seconds: int
    max_approval_age_seconds: int
    max_nonce_status_age_seconds: int
    require_human_approval: bool
    require_exact_compare_and_swap: bool
    require_direct_checkpoint_reference: bool
    require_reference_store_source: bool
    require_object_database_source: bool
    allow_lost_reference_restore: bool
    allow_substituted_reference_restore: bool
    allow_generic_overwrite: bool
    allow_reference_delete: bool
    allow_force_update: bool
    allow_branch_update: bool
    allow_tag_update: bool
    allow_remote_reference_update: bool
    allow_push: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for key in (
            "allowed_repository_ids",
            "allowed_checkpoint_references",
            "authorized_observer_ids",
            "authorized_approver_ids",
            "authorized_approver_classes",
            "authorized_executor_ids",
            "authorized_nonce_authority_ids",
        ):
            payload[key] = list(payload[key])
        return payload


def repository_checkpoint_restore_policy_digest(
    policy: RepositoryCheckpointRestorePolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointRestoreObservation:
    observation_id: str
    observer_id: str
    stability_certificate_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_restore_oid: str
    reference_present: bool
    observed_current_oid: str
    rechecked_current_oid: str
    target_object_present: bool
    target_object_type: str
    direct: bool
    symbolic: bool
    reference_store_read: bool
    object_database_read: bool
    working_tree_read: bool
    reflog_read: bool
    remote_read: bool
    sequence_number: int
    observed_at_epoch_seconds: int
    rechecked_at_epoch_seconds: int
    observation_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_restore_observation_digest(
    observation: RepositoryCheckpointRestoreObservation,
) -> str:
    payload = observation.to_dict()
    payload.pop("observation_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointRestoreScope:
    scope_id: str
    stability_certificate_digest: str
    restore_policy_digest: str
    restore_observation_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    restore_target_oid: str
    transaction_id: str
    eligible_stability_failure: str
    executor_id: str
    authorization_nonce: str
    restore_requested: bool
    generic_overwrite_requested: bool
    delete_requested: bool
    force_update_requested: bool
    branch_update_requested: bool
    tag_update_requested: bool
    remote_reference_update_requested: bool
    push_requested: bool
    issued_at_epoch_seconds: int
    expires_at_epoch_seconds: int
    scope_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_restore_scope_digest(
    scope: RepositoryCheckpointRestoreScope,
) -> str:
    payload = scope.to_dict()
    payload.pop("scope_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointRestoreApprovalReceipt:
    approval_id: str
    approver_id: str
    approver_class: str
    decision: str
    stability_certificate_digest: str
    restore_policy_digest: str
    restore_scope_digest: str
    approved_executor_id: str
    approved_authorization_nonce: str
    approved_current_oid: str
    approved_restore_target_oid: str
    approved_at_epoch_seconds: int
    expires_at_epoch_seconds: int
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_restore_approval_receipt_digest(
    receipt: RepositoryCheckpointRestoreApprovalReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointRestoreNonceStatusReceipt:
    status_id: str
    authorization_nonce: str
    restore_scope_digest: str
    authority_id: str
    checked_at_epoch_seconds: int
    registry_snapshot_digest: str
    consumed: bool
    revoked: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_restore_nonce_status_receipt_digest(
    receipt: RepositoryCheckpointRestoreNonceStatusReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointRestoreAuthorizationCertificate:
    authorization_id: str
    status: str
    failure_kind: str
    stability_certificate_digest: str
    restore_policy_digest: str
    restore_observation_digest: str
    restore_scope_digest: str
    approval_receipt_digest: str
    nonce_status_receipt_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    restore_target_oid: str
    transaction_id: str
    executor_id: str
    authorization_nonce: str
    evaluated_at_epoch_seconds: int
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_restore_authorization_certificate_digest(
    certificate: RepositoryCheckpointRestoreAuthorizationCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
