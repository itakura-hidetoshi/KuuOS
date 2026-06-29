#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_reference_update_receipt_v0_98"
RECEIPT_COMMITTED = "REPOSITORY_REFERENCE_UPDATE_RECEIPT_COMMITTED"
RECEIPT_REJECTED = "REPOSITORY_REFERENCE_UPDATE_RECEIPT_REJECTED"


@dataclass(frozen=True)
class RepositoryReferenceUpdateReceiptPolicy:
    policy_id: str
    authorized_observer_ids: tuple[str, ...]
    max_execution_report_age_seconds: int
    max_post_reference_observation_age_seconds: int
    max_nonce_consumption_receipt_age_seconds: int
    require_exact_transaction_binding: bool
    require_reference_store_source: bool
    require_working_tree_ignored: bool
    require_atomic_reference_nonce_transition: bool
    allow_force_update: bool
    allow_reference_delete: bool
    allow_push: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["authorized_observer_ids"] = list(self.authorized_observer_ids)
        return payload


def repository_reference_update_receipt_policy_digest(
    policy: RepositoryReferenceUpdateReceiptPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryReferenceUpdateExecutionReport:
    report_id: str
    transaction_id: str
    atomic_update_result_digest: str
    repository_id: str
    git_dir_fingerprint: str
    target_reference: str
    expected_old_oid: str
    proposed_new_oid: str
    authorization_nonce: str
    executor_id: str
    reference_update_attempted: bool
    reference_update_performed: bool
    compare_and_swap_succeeded: bool
    branch_updated: bool
    nonce_consumed: bool
    force_update_performed: bool
    reference_delete_performed: bool
    head_updated: bool
    tag_updated: bool
    remote_reference_updated: bool
    push_performed: bool
    index_write_performed: bool
    working_tree_write_performed: bool
    object_database_write_performed: bool
    signing_performed: bool
    execution_started_at_epoch_seconds: int
    execution_completed_at_epoch_seconds: int
    report_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_reference_update_execution_report_digest(
    report: RepositoryReferenceUpdateExecutionReport,
) -> str:
    payload = report.to_dict()
    payload.pop("report_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryPostReferenceObservation:
    observation_id: str
    observer_id: str
    transaction_id: str
    repository_id: str
    git_dir_fingerprint: str
    target_reference: str
    observed_oid: str
    direct: bool
    symbolic: bool
    reference_store_read: bool
    working_tree_read: bool
    sequence_number: int
    observed_at_epoch_seconds: int
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_post_reference_observation_digest(
    observation: RepositoryPostReferenceObservation,
) -> str:
    payload = observation.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryReferenceNonceConsumptionReceipt:
    receipt_id: str
    observer_id: str
    transaction_id: str
    authorization_nonce: str
    authority_id: str
    source_registry_digest: str
    final_registry_digest: str
    consumed: bool
    revoked: bool
    final_sequence_number: int
    consumed_at_epoch_seconds: int
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_reference_nonce_consumption_receipt_digest(
    receipt: RepositoryReferenceNonceConsumptionReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryReferenceUpdateReceipt:
    receipt_id: str
    status: str
    atomic_update_result_digest: str
    receipt_policy_digest: str
    execution_report_digest: str
    post_reference_observation_digest: str
    nonce_consumption_receipt_digest: str
    repository_id: str
    git_dir_fingerprint: str
    target_reference: str
    expected_old_oid: str
    proposed_new_oid: str
    authorization_nonce: str
    transaction_id: str
    evaluated_at_epoch_seconds: int
    atomic_update_result_valid: bool
    atomic_update_committed: bool
    atomic_update_binding_exact: bool
    receipt_policy_valid: bool
    execution_report_valid: bool
    execution_report_binding_exact: bool
    execution_report_fresh: bool
    execution_timing_exact: bool
    reference_update_attempted: bool
    reference_update_performed: bool
    compare_and_swap_succeeded: bool
    branch_updated: bool
    execution_nonce_consumed: bool
    post_reference_observation_valid: bool
    post_reference_observation_binding_exact: bool
    post_reference_observation_fresh: bool
    post_reference_direct: bool
    post_reference_not_symbolic: bool
    post_reference_store_source: bool
    post_reference_working_tree_ignored: bool
    post_reference_oid_exact: bool
    post_reference_sequence_exact: bool
    nonce_consumption_receipt_valid: bool
    nonce_consumption_receipt_binding_exact: bool
    nonce_consumption_receipt_fresh: bool
    nonce_registry_transition_exact: bool
    nonce_consumption_confirmed: bool
    nonce_not_revoked: bool
    observer_authorized: bool
    transaction_binding_exact: bool
    no_future_evidence: bool
    no_forbidden_execution_effect: bool
    atomic_reference_nonce_transition_confirmed: bool
    reference_update_confirmed: bool
    receipt_committed: bool
    force_update_confirmed: bool
    reference_delete_confirmed: bool
    head_update_confirmed: bool
    tag_update_confirmed: bool
    remote_reference_update_confirmed: bool
    push_confirmed: bool
    index_write_confirmed: bool
    working_tree_write_confirmed: bool
    object_database_write_confirmed: bool
    signing_confirmed: bool
    receipt_performed_reference_mutation: bool
    receipt_performed_nonce_consumption: bool
    receipt_performed_push: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_reference_update_receipt_digest(
    receipt: RepositoryReferenceUpdateReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)
