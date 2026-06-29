#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_stability_v1_04"
STABILITY_CONFIRMED = "REPOSITORY_CHECKPOINT_STABILITY_CONFIRMED"
STABILITY_REJECTED = "REPOSITORY_CHECKPOINT_STABILITY_REJECTED"
FAILURE_NONE = "NONE"
FAILURE_EVIDENCE_INVALID = "EVIDENCE_INVALID"
FAILURE_CHECKPOINT_LOST = "CHECKPOINT_LOST"
FAILURE_CHECKPOINT_SUBSTITUTED = "CHECKPOINT_SUBSTITUTED"
FAILURE_NAME_CONFLICT = "CHECKPOINT_NAME_CONFLICT"
FAILURE_UNREACHABLE = "CHECKPOINT_OBJECT_UNREACHABLE"
FAILURE_UNSTABLE_WINDOW = "CHECKPOINT_UNSTABLE_WINDOW"
ZERO_OID = "0" * 40


@dataclass(frozen=True)
class RepositoryCheckpointStabilityPolicy:
    policy_id: str
    authorized_observer_ids: tuple[str, ...]
    min_stability_interval_seconds: int
    max_stability_interval_seconds: int
    max_observation_age_seconds: int
    max_reachability_age_seconds: int
    checkpoint_namespace_prefix: str
    require_direct_checkpoint_reference: bool
    require_reference_store_source: bool
    require_object_database_source: bool
    require_unique_checkpoint_name: bool
    immutable_by_default: bool
    allow_checkpoint_overwrite: bool
    allow_checkpoint_delete: bool
    allow_force_update: bool
    allow_branch_update: bool
    allow_tag_update: bool
    allow_remote_reference_update: bool
    allow_push: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["authorized_observer_ids"] = list(self.authorized_observer_ids)
        return payload


def repository_checkpoint_stability_policy_digest(
    policy: RepositoryCheckpointStabilityPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryDelayedCheckpointObservation:
    observation_id: str
    observer_id: str
    transaction_id: str
    creation_receipt_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_oid: str
    observed_oid: str
    reference_present: bool
    direct: bool
    symbolic: bool
    reference_store_read: bool
    object_database_read: bool
    working_tree_read: bool
    reflog_read: bool
    remote_read: bool
    overwrite_observed: bool
    force_update_observed: bool
    sequence_number: int
    observed_at_epoch_seconds: int
    observation_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_delayed_checkpoint_observation_digest(
    observation: RepositoryDelayedCheckpointObservation,
) -> str:
    payload = observation.to_dict()
    payload.pop("observation_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointReachabilityObservation:
    observation_id: str
    observer_id: str
    transaction_id: str
    creation_receipt_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    object_oid: str
    object_present: bool
    object_type: str
    object_database_read: bool
    working_tree_read: bool
    reflog_read: bool
    remote_read: bool
    sequence_number: int
    observed_at_epoch_seconds: int
    observation_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_reachability_observation_digest(
    observation: RepositoryCheckpointReachabilityObservation,
) -> str:
    payload = observation.to_dict()
    payload.pop("observation_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointNamespaceObservation:
    observation_id: str
    observer_id: str
    transaction_id: str
    creation_receipt_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_namespace_prefix: str
    checkpoint_reference: str
    observed_checkpoint_references: tuple[str, ...]
    conflicting_reference_names: tuple[str, ...]
    target_occurrences: int
    reference_store_read: bool
    working_tree_read: bool
    reflog_read: bool
    remote_read: bool
    sequence_number: int
    observed_at_epoch_seconds: int
    observation_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["observed_checkpoint_references"] = list(
            self.observed_checkpoint_references
        )
        payload["conflicting_reference_names"] = list(
            self.conflicting_reference_names
        )
        return payload


def repository_checkpoint_namespace_observation_digest(
    observation: RepositoryCheckpointNamespaceObservation,
) -> str:
    payload = observation.to_dict()
    payload.pop("observation_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointStabilityCertificate:
    certificate_id: str
    status: str
    failure_kind: str
    creation_receipt_digest: str
    stability_policy_digest: str
    delayed_observation_digest: str
    reachability_observation_digest: str
    namespace_observation_digest: str
    transaction_id: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_oid: str
    evaluated_at_epoch_seconds: int
    checks: dict[str, bool]
    evidence_digests: dict[str, str]
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_stability_certificate_digest(
    certificate: RepositoryCheckpointStabilityCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
