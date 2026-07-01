#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_constructed_commit_publication_v1_21"

COMMIT_PUBLISHED = "CONSTRUCTED_COMMIT_CHECKPOINT_PUBLISHED"
PUBLICATION_REJECTED = "CONSTRUCTED_COMMIT_PUBLICATION_REJECTED"
PUBLICATION_ERROR = "CONSTRUCTED_COMMIT_PUBLICATION_ERROR"


@dataclass(frozen=True)
class RepositoryConstructedCommitPublicationPolicy:
    policy_id: str
    authorized_executor_ids: tuple[str, ...]
    allowed_repository_path_digests: tuple[str, ...]
    require_valid_v120_result: bool
    require_exact_constructed_commit_binding: bool
    require_valid_v118_request: bool
    require_exact_v118_request_binding: bool
    live_reference_update_enabled: bool
    allow_object_database_write: bool
    allow_index_write: bool
    allow_working_tree_write: bool
    allow_reflog_write: bool
    allow_force_update: bool
    allow_reference_delete: bool
    allow_head_update: bool
    allow_branch_update: bool
    allow_tag_update: bool
    allow_remote_reference_update: bool
    allow_push: bool
    allow_signing: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["authorized_executor_ids"] = list(self.authorized_executor_ids)
        payload["allowed_repository_path_digests"] = list(
            self.allowed_repository_path_digests
        )
        return payload


def repository_constructed_commit_publication_policy_digest(
    policy: RepositoryConstructedCommitPublicationPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryConstructedCommitPublicationRequest:
    publication_id: str
    v120_result_digest: str
    live_ref_cas_request_digest: str
    repository_path_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    constructed_commit_oid: str
    executor_id: str
    requested_at_epoch_seconds: int
    request_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_constructed_commit_publication_request_digest(
    request: RepositoryConstructedCommitPublicationRequest,
) -> str:
    payload = request.to_dict()
    payload.pop("request_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryConstructedCommitPublicationResult:
    publication_id: str
    status: str
    reason: str
    policy_digest: str
    request_digest: str
    v120_result_digest: str
    live_ref_cas_request_digest: str
    live_ref_cas_result_digest: str
    repository_path_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    constructed_commit_oid: str
    observed_before_oid: str
    observed_after_oid: str
    executor_id: str
    policy_valid: bool
    request_valid: bool
    v120_result_valid: bool
    v120_result_accepted: bool
    constructed_commit_binding_exact: bool
    live_ref_cas_request_valid: bool
    live_ref_cas_request_binding_exact: bool
    executor_authorized: bool
    repository_path_allowed: bool
    delegated_live_ref_cas_invoked: bool
    delegated_live_ref_cas_valid: bool
    reference_cas_committed: bool
    prior_object_database_write_performed: bool
    current_object_database_write_performed: bool
    live_repository_mutated: bool
    checkpoint_reference_write_performed: bool
    index_write_performed: bool
    working_tree_write_performed: bool
    reflog_write_performed: bool
    force_update_performed: bool
    reference_delete_performed: bool
    head_updated: bool
    branch_updated: bool
    tag_updated: bool
    remote_reference_updated: bool
    push_performed: bool
    signing_performed: bool
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    result_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_constructed_commit_publication_result_digest(
    result: RepositoryConstructedCommitPublicationResult,
) -> str:
    payload = result.to_dict()
    payload.pop("result_digest", None)
    return canonical_digest(payload)
