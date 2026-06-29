#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_local_frontier_finality_v1_00"
CERTIFICATE_COMMITTED = "REPOSITORY_LOCAL_FRONTIER_FINALITY_COMMITTED"
CERTIFICATE_REJECTED = "REPOSITORY_LOCAL_FRONTIER_FINALITY_REJECTED"


@dataclass(frozen=True)
class RepositoryLocalFrontierFinalityPolicy:
    policy_id: str
    authorized_observer_ids: tuple[str, ...]
    min_sample_count: int
    max_sample_count: int
    min_total_interval_seconds: int
    max_total_interval_seconds: int
    min_inter_sample_interval_seconds: int
    max_inter_sample_interval_seconds: int
    max_history_age_seconds: int
    max_candidate_reachability_depth: int
    max_transition_depth: int
    max_total_queried_nodes: int
    allow_equal_tip: bool
    allow_tip_advance: bool
    require_common_observer: bool
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


def repository_local_frontier_finality_policy_digest(
    policy: RepositoryLocalFrontierFinalityPolicy,
) -> str:
    payload = policy.to_dict()
    payload.pop("policy_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryLocalFrontierSample:
    sample_id: str
    observer_id: str
    transaction_id: str
    repository_id: str
    git_dir_fingerprint: str
    target_reference: str
    candidate_commit_oid: str
    observed_tip_oid: str
    previous_tip_oid: str
    sequence_number: int
    observed_at_epoch_seconds: int
    candidate_path_oids: tuple[str, ...]
    candidate_parent_edges: tuple[tuple[str, str], ...]
    transition_path_oids: tuple[str, ...]
    transition_parent_edges: tuple[tuple[str, str], ...]
    queried_oids: tuple[str, ...]
    object_database_commit_oids: tuple[str, ...]
    queried_oid_set_complete: bool
    all_objects_are_commits: bool
    direct: bool
    symbolic: bool
    reference_store_read: bool
    object_database_read: bool
    working_tree_read: bool
    reflog_read: bool
    remote_read: bool
    reference_deleted: bool
    force_update_observed: bool
    sample_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["candidate_path_oids"] = list(self.candidate_path_oids)
        payload["candidate_parent_edges"] = [
            list(edge) for edge in self.candidate_parent_edges
        ]
        payload["transition_path_oids"] = list(self.transition_path_oids)
        payload["transition_parent_edges"] = [
            list(edge) for edge in self.transition_parent_edges
        ]
        payload["queried_oids"] = list(self.queried_oids)
        payload["object_database_commit_oids"] = list(
            self.object_database_commit_oids
        )
        return payload


def repository_local_frontier_sample_digest(
    sample: RepositoryLocalFrontierSample,
) -> str:
    payload = sample.to_dict()
    payload.pop("sample_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryLocalFrontierHistory:
    history_id: str
    reference_stability_certificate_digest: str
    samples: tuple[RepositoryLocalFrontierSample, ...]
    history_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "history_id": self.history_id,
            "reference_stability_certificate_digest": (
                self.reference_stability_certificate_digest
            ),
            "samples": [sample.to_dict() for sample in self.samples],
            "history_digest": self.history_digest,
            "version": self.version,
        }


def repository_local_frontier_history_digest(
    history: RepositoryLocalFrontierHistory,
) -> str:
    payload = history.to_dict()
    payload.pop("history_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryLocalFrontierFinalityCertificate:
    certificate_id: str
    status: str
    reference_stability_certificate_digest: str
    policy_digest: str
    history_digest: str
    repository_id: str
    git_dir_fingerprint: str
    target_reference: str
    candidate_commit_oid: str
    transaction_id: str
    first_tip_oid: str
    final_tip_oid: str
    first_observed_at_epoch_seconds: int
    final_observed_at_epoch_seconds: int
    sample_count: int
    evaluated_at_epoch_seconds: int
    reference_stability_certificate_valid: bool
    reference_stability_certificate_committed: bool
    reference_stability_binding_exact: bool
    policy_valid: bool
    history_valid: bool
    history_binding_exact: bool
    anchor_sample_exact: bool
    sample_count_within_policy: bool
    sample_bindings_exact: bool
    sample_digests_valid: bool
    common_observer_exact: bool
    observers_authorized: bool
    sequences_strictly_increasing: bool
    observation_times_strictly_increasing: bool
    inter_sample_intervals_within_policy: bool
    total_interval_within_policy: bool
    history_fresh: bool
    no_future_evidence: bool
    all_references_direct: bool
    all_references_not_symbolic: bool
    all_reference_store_sources: bool
    all_object_database_sources: bool
    all_working_tree_ignored: bool
    all_reflog_ignored: bool
    all_remote_ignored: bool
    no_reference_deleted: bool
    no_force_update_observed: bool
    candidate_paths_complete: bool
    candidate_parent_edges_exact: bool
    transition_paths_complete: bool
    transition_parent_edges_exact: bool
    queried_oid_sets_complete: bool
    all_path_objects_are_commits: bool
    candidate_present_in_every_sample: bool
    tips_present_in_every_sample: bool
    previous_tips_present: bool
    candidate_reachable_in_every_sample: bool
    frontier_transitions_monotone: bool
    equal_tip_policy_satisfied: bool
    tip_advance_policy_satisfied: bool
    candidate_depths_within_policy: bool
    transition_depths_within_policy: bool
    total_queried_nodes_within_policy: bool
    local_frontier_history_monotone: bool
    candidate_reachability_continuous: bool
    bounded_local_finality_verified: bool
    certificate_committed: bool
    absolute_finality_claimed: bool
    remote_finality_claimed: bool
    branch_protection_verified: bool
    garbage_collection_retention_guaranteed: bool
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


def repository_local_frontier_finality_certificate_digest(
    certificate: RepositoryLocalFrontierFinalityCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
