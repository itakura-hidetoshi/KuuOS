#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_object_materialization_receipt_v0_95"
MATERIALIZATION_COMMITTED = "REPOSITORY_OBJECT_MATERIALIZATION_COMMITTED"
MATERIALIZATION_ABORTED = "REPOSITORY_OBJECT_MATERIALIZATION_ABORTED"
ITEM_WRITTEN = "OBJECT_WRITTEN"
ITEM_REUSED = "OBJECT_REUSED"


@dataclass(frozen=True)
class RepositoryObjectMaterializationPolicy:
    policy_id: str
    authorized_executor_ids: tuple[str, ...]
    max_materialization_duration_seconds: int
    max_post_observation_age_seconds: int
    require_exact_plan_order: bool
    require_nonce_atomicity: bool
    require_reference_nonmutation: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_object_materialization_policy_digest(
    policy: RepositoryObjectMaterializationPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryObjectMaterializationExecutionItem:
    kind: str
    oid: str
    payload_size: int
    payload_digest: str
    outcome: str
    write_order: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepositoryObjectMaterializationExecutionReport:
    execution_id: str
    authorization_certificate_digest: str
    repository_id: str
    git_dir_fingerprint: str
    executor_id: str
    started_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    items: tuple[RepositoryObjectMaterializationExecutionItem, ...]
    object_database_write_attempted: bool
    index_write_performed: bool
    working_tree_write_performed: bool
    reference_mutated: bool
    signing_performed: bool
    report_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["items"] = [item.to_dict() for item in self.items]
        return payload


def repository_object_materialization_execution_report_digest(
    report: RepositoryObjectMaterializationExecutionReport,
) -> str:
    payload = report.to_dict()
    payload.pop("report_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryObjectMaterializationNonceConsumptionReceipt:
    transaction_id: str
    authorization_nonce: str
    authorization_scope_digest: str
    authorization_certificate_digest: str
    registry_before_digest: str
    registry_after_digest: str
    consumed_before: bool
    consumed_after: bool
    revoked: bool
    materialization_committed: bool
    atomic_with_materialization: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_object_materialization_nonce_consumption_receipt_digest(
    receipt: RepositoryObjectMaterializationNonceConsumptionReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryObjectMaterializationReceipt:
    transaction_id: str
    status: str
    authorization_certificate_digest: str
    materialization_policy_digest: str
    execution_report_digest: str
    pre_observation_digest: str
    post_observation_digest: str
    nonce_consumption_receipt_digest: str
    repository_id: str
    git_dir_fingerprint: str
    parent_commit_sha: str
    candidate_commit_oid: str
    expected_object_count: int
    expected_new_object_count: int
    expected_reused_object_count: int
    expected_new_payload_bytes: int
    actual_written_object_count: int
    actual_reused_object_count: int
    actual_written_payload_bytes: int
    executor_id: str
    started_at_epoch_seconds: int
    completed_at_epoch_seconds: int
    authorization_valid: bool
    authorization_granted: bool
    authorization_binding_exact: bool
    authorization_not_expired_at_completion: bool
    materialization_policy_bound: bool
    executor_authorized: bool
    transaction_time_order_valid: bool
    duration_within_policy: bool
    execution_report_bound: bool
    repository_identity_exact: bool
    plan_item_set_exact: bool
    plan_order_exact: bool
    write_set_exact: bool
    reuse_set_exact: bool
    execution_payloads_exact: bool
    object_database_write_attempted: bool
    post_observation_bound: bool
    post_observation_fresh: bool
    post_observation_object_database_source: bool
    post_observation_working_tree_ignored: bool
    post_query_set_exact: bool
    parent_commit_preserved: bool
    all_candidate_objects_present: bool
    all_candidate_payloads_exact: bool
    reused_objects_preserved: bool
    candidate_commit_present: bool
    nonce_scope_bound: bool
    nonce_authorization_bound: bool
    nonce_unused_before: bool
    nonce_consumed_after: bool
    nonce_not_revoked: bool
    nonce_consumption_committed: bool
    nonce_atomic_with_materialization: bool
    object_database_materialization_committed: bool
    commit_object_written: bool
    atomic_state_transition: bool
    failure_no_effect: bool
    index_write_performed: bool
    working_tree_write_performed: bool
    reference_mutated: bool
    signing_performed: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_object_materialization_receipt_digest(
    receipt: RepositoryObjectMaterializationReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)
