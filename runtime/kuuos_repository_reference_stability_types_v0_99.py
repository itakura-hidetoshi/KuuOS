#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_reference_stability_reachability_v0_99"
CERTIFICATE_COMMITTED = "REPOSITORY_REFERENCE_STABILITY_REACHABILITY_COMMITTED"
CERTIFICATE_REJECTED = "REPOSITORY_REFERENCE_STABILITY_REACHABILITY_REJECTED"


@dataclass(frozen=True)
class RepositoryReferenceStabilityPolicy:
    policy_id: str
    authorized_observer_ids: tuple[str, ...]
    min_stability_interval_seconds: int
    max_stability_interval_seconds: int
    max_delayed_observation_age_seconds: int
    max_reachability_certificate_age_seconds: int
    max_reachability_depth: int
    max_reachability_nodes: int
    allow_tip_advance: bool
    require_direct_local_branch: bool
    require_reference_store_source: bool
    require_object_database_source: bool
    require_working_tree_ignored: bool
    require_reflog_ignored: bool
    require_remote_ignored: bool
    allow_force_update: bool
    allow_reference_delete: bool
    allow_push: bool
    policy_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["authorized_observer_ids"] = list(self.authorized_observer_ids)
        return payload


def repository_reference_stability_policy_digest(
    policy: RepositoryReferenceStabilityPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryDelayedReferenceObservation:
    observation_id: str
    observer_id: str
    transaction_id: str
    repository_id: str
    git_dir_fingerprint: str
    target_reference: str
    candidate_commit_oid: str
    observed_tip_oid: str
    direct: bool
    symbolic: bool
    reference_store_read: bool
    object_database_read: bool
    working_tree_read: bool
    reflog_read: bool
    remote_read: bool
    reference_deleted: bool
    force_update_observed: bool
    sequence_number: int
    observed_at_epoch_seconds: int
    observation_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_delayed_reference_observation_digest(
    observation: RepositoryDelayedReferenceObservation,
) -> str:
    payload = observation.to_dict()
    payload.pop("observation_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCommitReachabilityCertificate:
    certificate_id: str
    observer_id: str
    transaction_id: str
    repository_id: str
    git_dir_fingerprint: str
    target_reference: str
    tip_oid: str
    candidate_commit_oid: str
    path_oids: tuple[str, ...]
    parent_edges: tuple[tuple[str, str], ...]
    queried_oids: tuple[str, ...]
    object_database_commit_oids: tuple[str, ...]
    queried_oid_set_complete: bool
    all_objects_are_commits: bool
    object_database_read: bool
    working_tree_read: bool
    reflog_read: bool
    remote_read: bool
    observed_at_epoch_seconds: int
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["path_oids"] = list(self.path_oids)
        payload["parent_edges"] = [list(edge) for edge in self.parent_edges]
        payload["queried_oids"] = list(self.queried_oids)
        payload["object_database_commit_oids"] = list(
            self.object_database_commit_oids
        )
        return payload


def repository_commit_reachability_certificate_digest(
    certificate: RepositoryCommitReachabilityCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryReferenceStabilityReachabilityCertificate:
    certificate_id: str
    status: str
    reference_update_receipt_digest: str
    stability_policy_digest: str
    delayed_reference_observation_digest: str
    reachability_certificate_digest: str
    repository_id: str
    git_dir_fingerprint: str
    target_reference: str
    candidate_commit_oid: str
    delayed_tip_oid: str
    transaction_id: str
    evaluated_at_epoch_seconds: int
    reference_update_receipt_valid: bool
    reference_update_receipt_committed: bool
    reference_update_receipt_binding_exact: bool
    stability_policy_valid: bool
    delayed_observation_valid: bool
    delayed_observation_binding_exact: bool
    delayed_observation_fresh: bool
    stability_interval_within_policy: bool
    delayed_reference_direct: bool
    delayed_reference_not_symbolic: bool
    delayed_reference_store_source: bool
    delayed_object_database_source: bool
    delayed_working_tree_ignored: bool
    delayed_reflog_ignored: bool
    delayed_remote_ignored: bool
    delayed_reference_not_deleted: bool
    no_force_update_observed: bool
    delayed_sequence_monotone: bool
    observer_authorized: bool
    reachability_certificate_valid: bool
    reachability_certificate_binding_exact: bool
    reachability_certificate_fresh: bool
    reachability_evidence_time_exact: bool
    reachability_path_complete: bool
    reachability_parent_edges_exact: bool
    queried_oid_set_complete: bool
    all_reachability_objects_are_commits: bool
    candidate_commit_present: bool
    delayed_tip_present: bool
    candidate_is_delayed_tip: bool
    delayed_tip_advanced: bool
    tip_advance_allowed: bool
    candidate_reachable_from_delayed_tip: bool
    reachability_depth_within_policy: bool
    reachability_nodes_within_policy: bool
    no_future_evidence: bool
    reference_stability_verified: bool
    candidate_reachability_preserved: bool
    certificate_committed: bool
    force_update_authorized: bool
    reference_delete_authorized: bool
    push_authorized: bool
    reference_mutation_performed: bool
    object_database_write_performed: bool
    working_tree_write_performed: bool
    index_write_performed: bool
    reflog_write_performed: bool
    remote_reference_updated: bool
    push_performed: bool
    signing_performed: bool
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_reference_stability_reachability_certificate_digest(
    certificate: RepositoryReferenceStabilityReachabilityCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
