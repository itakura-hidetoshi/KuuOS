#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_discrepancy_review_v1_06"
REVIEW_CLEAN = "REPOSITORY_CHECKPOINT_REVIEW_CLEAN"
REVIEW_REQUIRED = "REPOSITORY_CHECKPOINT_REVIEW_REQUIRED"
REVIEW_REJECTED = "REPOSITORY_CHECKPOINT_REVIEW_REJECTED"
DISCREPANCY_NONE = "NONE"
DISCREPANCY_LOST = "CHECKPOINT_LOST"
DISCREPANCY_SUBSTITUTED = "CHECKPOINT_SUBSTITUTED"
DISCREPANCY_OTHER = "OTHER_STABILITY_DISPOSITION"
DISCREPANCY_EVIDENCE_INVALID = "EVIDENCE_INVALID"
ZERO_OID = "0" * 40


@dataclass(frozen=True)
class RepositoryCheckpointReviewPolicy:
    policy_id: str
    allowed_repository_ids: tuple[str, ...]
    allowed_checkpoint_references: tuple[str, ...]
    authorized_observer_ids: tuple[str, ...]
    max_observation_age_seconds: int
    require_direct_reference: bool
    require_reference_store_source: bool
    require_object_database_source: bool
    read_only: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_repository_ids"] = list(self.allowed_repository_ids)
        payload["allowed_checkpoint_references"] = list(self.allowed_checkpoint_references)
        payload["authorized_observer_ids"] = list(self.authorized_observer_ids)
        return payload


def repository_checkpoint_review_policy_digest(policy: RepositoryCheckpointReviewPolicy) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointReviewObservation:
    observation_id: str
    observer_id: str
    stability_certificate_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_oid: str
    reference_present: bool
    observed_oid: str
    rechecked_oid: str
    target_object_present: bool
    target_object_type: str
    direct: bool
    symbolic: bool
    reference_store_read: bool
    object_database_read: bool
    working_tree_read: bool
    reflog_read: bool
    remote_read: bool
    observed_at_epoch_seconds: int
    rechecked_at_epoch_seconds: int
    observation_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_review_observation_digest(observation: RepositoryCheckpointReviewObservation) -> str:
    payload = observation.to_dict()
    payload.pop("observation_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointReviewRecord:
    review_id: str
    status: str
    discrepancy_kind: str
    stability_certificate_digest: str
    review_policy_digest: str
    review_observation_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_current_oid: str
    expected_target_oid: str
    human_review_required: bool
    evaluated_at_epoch_seconds: int
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    record_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_review_record_digest(record: RepositoryCheckpointReviewRecord) -> str:
    payload = record.to_dict()
    payload.pop("record_digest", None)
    return canonical_digest(payload)
