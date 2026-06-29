#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import re
from typing import Any, Mapping

from runtime.kuuos_repository_local_frontier_finality_types_v1_00 import (
    CERTIFICATE_COMMITTED,
    CERTIFICATE_REJECTED,
    RepositoryLocalFrontierFinalityCertificate,
    RepositoryLocalFrontierFinalityPolicy,
    RepositoryLocalFrontierHistory,
    RepositoryLocalFrontierSample,
    repository_local_frontier_finality_certificate_digest,
    repository_local_frontier_finality_policy_digest,
    repository_local_frontier_history_digest,
    repository_local_frontier_sample_digest,
)
from runtime.kuuos_repository_reference_stability_types_v0_99 import (
    CERTIFICATE_COMMITTED as STABILITY_COMMITTED,
    RepositoryReferenceStabilityReachabilityCertificate,
)
from runtime.kuuos_repository_reference_stability_v0_99 import (
    repository_reference_stability_reachability_certificate_issues,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _canonical_strings(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def _path_edges(path_oids: tuple[str, ...]) -> tuple[tuple[str, str], ...]:
    return tuple(zip(path_oids, path_oids[1:]))


def _pairwise(values: tuple[Any, ...]) -> tuple[tuple[Any, Any], ...]:
    return tuple(zip(values, values[1:]))


def build_repository_local_frontier_finality_policy(
    policy_id: str,
    *,
    authorized_observer_ids: tuple[str, ...],
    min_sample_count: int,
    max_sample_count: int,
    min_total_interval_seconds: int,
    max_total_interval_seconds: int,
    min_inter_sample_interval_seconds: int,
    max_inter_sample_interval_seconds: int,
    max_history_age_seconds: int,
    max_candidate_reachability_depth: int,
    max_transition_depth: int,
    max_total_queried_nodes: int,
    allow_equal_tip: bool = True,
    allow_tip_advance: bool = True,
) -> RepositoryLocalFrontierFinalityPolicy:
    policy = RepositoryLocalFrontierFinalityPolicy(
        policy_id=policy_id,
        authorized_observer_ids=_canonical_strings(authorized_observer_ids),
        min_sample_count=min_sample_count,
        max_sample_count=max_sample_count,
        min_total_interval_seconds=min_total_interval_seconds,
        max_total_interval_seconds=max_total_interval_seconds,
        min_inter_sample_interval_seconds=min_inter_sample_interval_seconds,
        max_inter_sample_interval_seconds=max_inter_sample_interval_seconds,
        max_history_age_seconds=max_history_age_seconds,
        max_candidate_reachability_depth=max_candidate_reachability_depth,
        max_transition_depth=max_transition_depth,
        max_total_queried_nodes=max_total_queried_nodes,
        allow_equal_tip=allow_equal_tip,
        allow_tip_advance=allow_tip_advance,
        require_common_observer=True,
        require_direct_local_branch=True,
        require_reference_store_source=True,
        require_object_database_source=True,
        require_working_tree_ignored=True,
        require_reflog_ignored=True,
        require_remote_ignored=True,
        allow_force_update=False,
        allow_reference_delete=False,
        allow_push=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_local_frontier_finality_policy_digest(policy),
    )
    issues = repository_local_frontier_finality_policy_issues(policy)
    if issues:
        raise ValueError(f"local_frontier_finality_policy_invalid:{issues[0]}")
    return policy


def repository_local_frontier_finality_policy_issues(
    policy: RepositoryLocalFrontierFinalityPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("local_frontier_policy_id_missing")
    if (
        policy.authorized_observer_ids
        != _canonical_strings(policy.authorized_observer_ids)
        or not policy.authorized_observer_ids
        or any(not value for value in policy.authorized_observer_ids)
    ):
        issues.append("local_frontier_observer_ids_invalid")
    if policy.min_sample_count < 2:
        issues.append("local_frontier_min_sample_count_invalid")
    if policy.max_sample_count < policy.min_sample_count:
        issues.append("local_frontier_sample_count_bounds_invalid")
    if policy.min_total_interval_seconds <= 0:
        issues.append("local_frontier_min_total_interval_invalid")
    if policy.max_total_interval_seconds < policy.min_total_interval_seconds:
        issues.append("local_frontier_total_interval_bounds_invalid")
    if policy.min_inter_sample_interval_seconds <= 0:
        issues.append("local_frontier_min_inter_sample_interval_invalid")
    if (
        policy.max_inter_sample_interval_seconds
        < policy.min_inter_sample_interval_seconds
    ):
        issues.append("local_frontier_inter_sample_bounds_invalid")
    if policy.max_history_age_seconds <= 0:
        issues.append("local_frontier_history_age_invalid")
    if policy.max_candidate_reachability_depth < 0:
        issues.append("local_frontier_candidate_depth_invalid")
    if policy.max_transition_depth < 0:
        issues.append("local_frontier_transition_depth_invalid")
    if policy.max_total_queried_nodes <= 0:
        issues.append("local_frontier_total_nodes_invalid")
    required = (
        policy.require_common_observer,
        policy.require_direct_local_branch,
        policy.require_reference_store_source,
        policy.require_object_database_source,
        policy.require_working_tree_ignored,
        policy.require_reflog_ignored,
        policy.require_remote_ignored,
    )
    if not all(required):
        issues.append("local_frontier_required_safeguard_disabled")
    if not (policy.allow_equal_tip or policy.allow_tip_advance):
        issues.append("local_frontier_no_tip_relation_allowed")
    if policy.allow_force_update:
        issues.append("local_frontier_force_policy_forbidden")
    if policy.allow_reference_delete:
        issues.append("local_frontier_delete_policy_forbidden")
    if policy.allow_push:
        issues.append("local_frontier_push_policy_forbidden")
    if (
        policy.policy_digest
        != repository_local_frontier_finality_policy_digest(policy)
    ):
        issues.append("local_frontier_policy_digest_mismatch")
    return tuple(issues)


def build_repository_local_frontier_sample(
    sample_id: str,
    observer_id: str,
    *,
    transaction_id: str,
    repository_id: str,
    git_dir_fingerprint: str,
    target_reference: str,
    candidate_commit_oid: str,
    observed_tip_oid: str,
    previous_tip_oid: str,
    sequence_number: int,
    observed_at_epoch_seconds: int,
    candidate_path_oids: tuple[str, ...],
    transition_path_oids: tuple[str, ...],
    queried_oid_set_complete: bool = True,
    all_objects_are_commits: bool = True,
    direct: bool = True,
    symbolic: bool = False,
    reference_store_read: bool = True,
    object_database_read: bool = True,
    working_tree_read: bool = False,
    reflog_read: bool = False,
    remote_read: bool = False,
    reference_deleted: bool = False,
    force_update_observed: bool = False,
) -> RepositoryLocalFrontierSample:
    candidate_path = tuple(candidate_path_oids)
    transition_path = tuple(transition_path_oids)
    queried_oids = _canonical_strings(candidate_path + transition_path)
    sample = RepositoryLocalFrontierSample(
        sample_id=sample_id,
        observer_id=observer_id,
        transaction_id=transaction_id,
        repository_id=repository_id,
        git_dir_fingerprint=git_dir_fingerprint,
        target_reference=target_reference,
        candidate_commit_oid=candidate_commit_oid,
        observed_tip_oid=observed_tip_oid,
        previous_tip_oid=previous_tip_oid,
        sequence_number=sequence_number,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        candidate_path_oids=candidate_path,
        candidate_parent_edges=_path_edges(candidate_path),
        transition_path_oids=transition_path,
        transition_parent_edges=_path_edges(transition_path),
        queried_oids=queried_oids,
        object_database_commit_oids=queried_oids,
        queried_oid_set_complete=queried_oid_set_complete,
        all_objects_are_commits=all_objects_are_commits,
        direct=direct,
        symbolic=symbolic,
        reference_store_read=reference_store_read,
        object_database_read=object_database_read,
        working_tree_read=working_tree_read,
        reflog_read=reflog_read,
        remote_read=remote_read,
        reference_deleted=reference_deleted,
        force_update_observed=force_update_observed,
        sample_digest="",
    )
    sample = replace(
        sample,
        sample_digest=repository_local_frontier_sample_digest(sample),
    )
    issues = repository_local_frontier_sample_issues(sample)
    if issues:
        raise ValueError(f"local_frontier_sample_invalid:{issues[0]}")
    return sample


def repository_local_frontier_sample_issues(
    sample: RepositoryLocalFrontierSample,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        sample.sample_id,
        sample.observer_id,
        sample.transaction_id,
        sample.repository_id,
        sample.target_reference,
    )
    if any(not value for value in required):
        issues.append("local_frontier_sample_required_field_missing")
    if not _HEX64.fullmatch(sample.git_dir_fingerprint):
        issues.append("local_frontier_sample_git_dir_invalid")
    for oid in (
        sample.candidate_commit_oid,
        sample.observed_tip_oid,
        sample.previous_tip_oid,
    ):
        if not _HEX40.fullmatch(oid):
            issues.append("local_frontier_sample_oid_invalid")
            break
    if not sample.candidate_path_oids:
        issues.append("local_frontier_candidate_path_empty")
    elif any(not _HEX40.fullmatch(oid) for oid in sample.candidate_path_oids):
        issues.append("local_frontier_candidate_path_oid_invalid")
    if not sample.transition_path_oids:
        issues.append("local_frontier_transition_path_empty")
    elif any(not _HEX40.fullmatch(oid) for oid in sample.transition_path_oids):
        issues.append("local_frontier_transition_path_oid_invalid")
    if len(set(sample.candidate_path_oids)) != len(sample.candidate_path_oids):
        issues.append("local_frontier_candidate_path_cycle")
    if len(set(sample.transition_path_oids)) != len(sample.transition_path_oids):
        issues.append("local_frontier_transition_path_cycle")
    for edges in (
        sample.candidate_parent_edges,
        sample.transition_parent_edges,
    ):
        if any(
            len(edge) != 2
            or not _HEX40.fullmatch(edge[0])
            or not _HEX40.fullmatch(edge[1])
            for edge in edges
        ):
            issues.append("local_frontier_parent_edge_invalid")
            break
    if sample.queried_oids != _canonical_strings(sample.queried_oids):
        issues.append("local_frontier_queried_oids_not_canonical")
    if sample.object_database_commit_oids != _canonical_strings(
        sample.object_database_commit_oids
    ):
        issues.append("local_frontier_commit_oids_not_canonical")
    if any(not _HEX40.fullmatch(oid) for oid in sample.queried_oids):
        issues.append("local_frontier_queried_oid_invalid")
    if any(
        not _HEX40.fullmatch(oid)
        for oid in sample.object_database_commit_oids
    ):
        issues.append("local_frontier_object_oid_invalid")
    if sample.sequence_number < 0:
        issues.append("local_frontier_sequence_negative")
    if sample.observed_at_epoch_seconds < 0:
        issues.append("local_frontier_time_negative")
    if sample.sample_digest != repository_local_frontier_sample_digest(sample):
        issues.append("local_frontier_sample_digest_mismatch")
    return tuple(issues)


def build_repository_local_frontier_history(
    history_id: str,
    reference_stability_certificate: (
        RepositoryReferenceStabilityReachabilityCertificate
    ),
    *,
    samples: tuple[RepositoryLocalFrontierSample, ...],
) -> RepositoryLocalFrontierHistory:
    history = RepositoryLocalFrontierHistory(
        history_id=history_id,
        reference_stability_certificate_digest=(
            reference_stability_certificate.certificate_digest
        ),
        samples=tuple(samples),
        history_digest="",
    )
    history = replace(
        history,
        history_digest=repository_local_frontier_history_digest(history),
    )
    issues = repository_local_frontier_history_issues(history)
    if issues:
        raise ValueError(f"local_frontier_history_invalid:{issues[0]}")
    return history


def repository_local_frontier_history_issues(
    history: RepositoryLocalFrontierHistory,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not history.history_id:
        issues.append("local_frontier_history_id_missing")
    if not _HEX64.fullmatch(history.reference_stability_certificate_digest):
        issues.append("local_frontier_stability_digest_invalid")
    if not history.samples:
        issues.append("local_frontier_history_empty")
    sample_ids = tuple(sample.sample_id for sample in history.samples)
    if len(set(sample_ids)) != len(sample_ids):
        issues.append("local_frontier_sample_id_duplicate")
    for sample in history.samples:
        if repository_local_frontier_sample_issues(sample):
            issues.append("local_frontier_history_sample_invalid")
            break
    if history.history_digest != repository_local_frontier_history_digest(history):
        issues.append("local_frontier_history_digest_mismatch")
    return tuple(issues)


def _stability_issues(
    certificate: RepositoryReferenceStabilityReachabilityCertificate,
    inputs: Mapping[str, Any],
) -> tuple[str, ...]:
    try:
        return repository_reference_stability_reachability_certificate_issues(
            certificate,
            **dict(inputs),
        )
    except (TypeError, ValueError, AttributeError, KeyError):
        return ("reference_stability_inputs_invalid",)


def _construct_local_frontier_finality_certificate(
    certificate_id: str,
    reference_stability_certificate: (
        RepositoryReferenceStabilityReachabilityCertificate
    ),
    reference_stability_inputs: Mapping[str, Any],
    policy: RepositoryLocalFrontierFinalityPolicy,
    history: RepositoryLocalFrontierHistory,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryLocalFrontierFinalityCertificate:
    samples = history.samples
    first = samples[0]
    final = samples[-1]
    delayed_observation = reference_stability_inputs.get("delayed_observation")
    reachability = reference_stability_inputs.get("reachability")
    stability_issues = _stability_issues(
        reference_stability_certificate,
        reference_stability_inputs,
    )
    reference_stability_certificate_valid = not stability_issues
    reference_stability_certificate_committed = bool(
        reference_stability_certificate_valid
        and reference_stability_certificate.status == STABILITY_COMMITTED
        and reference_stability_certificate.certificate_committed
        and reference_stability_certificate.reference_stability_verified
        and reference_stability_certificate.candidate_reachability_preserved
    )
    reference_stability_binding_exact = bool(
        delayed_observation is not None
        and reachability is not None
        and reference_stability_certificate.repository_id
        == delayed_observation.repository_id
        and reference_stability_certificate.git_dir_fingerprint
        == delayed_observation.git_dir_fingerprint
        and reference_stability_certificate.target_reference
        == delayed_observation.target_reference
        and reference_stability_certificate.candidate_commit_oid
        == delayed_observation.candidate_commit_oid
        and reference_stability_certificate.delayed_tip_oid
        == delayed_observation.observed_tip_oid
        and reference_stability_certificate.transaction_id
        == delayed_observation.transaction_id
        and reference_stability_certificate.reachability_certificate_digest
        == reachability.certificate_digest
    )
    policy_valid = not repository_local_frontier_finality_policy_issues(policy)
    history_valid = not repository_local_frontier_history_issues(history)
    history_binding_exact = (
        history.reference_stability_certificate_digest
        == reference_stability_certificate.certificate_digest
    )
    anchor_sample_exact = bool(
        delayed_observation is not None
        and reachability is not None
        and first.observer_id == delayed_observation.observer_id
        and first.transaction_id == delayed_observation.transaction_id
        and first.repository_id == delayed_observation.repository_id
        and first.git_dir_fingerprint
        == delayed_observation.git_dir_fingerprint
        and first.target_reference == delayed_observation.target_reference
        and first.candidate_commit_oid
        == delayed_observation.candidate_commit_oid
        and first.observed_tip_oid == delayed_observation.observed_tip_oid
        and first.previous_tip_oid == delayed_observation.observed_tip_oid
        and first.sequence_number == delayed_observation.sequence_number
        and first.observed_at_epoch_seconds
        == delayed_observation.observed_at_epoch_seconds
        and first.candidate_path_oids == reachability.path_oids
        and first.candidate_parent_edges == reachability.parent_edges
        and first.transition_path_oids == (first.observed_tip_oid,)
        and first.transition_parent_edges == ()
        and first.queried_oids == reachability.queried_oids
        and first.object_database_commit_oids
        == reachability.object_database_commit_oids
    )
    sample_count = len(samples)
    sample_count_within_policy = (
        policy.min_sample_count <= sample_count <= policy.max_sample_count
    )
    sample_bindings_exact = all(
        sample.transaction_id == reference_stability_certificate.transaction_id
        and sample.repository_id == reference_stability_certificate.repository_id
        and sample.git_dir_fingerprint
        == reference_stability_certificate.git_dir_fingerprint
        and sample.target_reference
        == reference_stability_certificate.target_reference
        and sample.candidate_commit_oid
        == reference_stability_certificate.candidate_commit_oid
        for sample in samples
    )
    sample_digests_valid = all(
        not repository_local_frontier_sample_issues(sample)
        for sample in samples
    )
    observer_ids = tuple(sample.observer_id for sample in samples)
    common_observer_exact = bool(
        not policy.require_common_observer or len(set(observer_ids)) == 1
    )
    observers_authorized = all(
        observer_id in policy.authorized_observer_ids
        for observer_id in observer_ids
    )
    sequences = tuple(sample.sequence_number for sample in samples)
    sequences_strictly_increasing = all(
        left < right for left, right in _pairwise(sequences)
    )
    times = tuple(sample.observed_at_epoch_seconds for sample in samples)
    observation_times_strictly_increasing = all(
        left < right for left, right in _pairwise(times)
    )
    intervals = tuple(right - left for left, right in _pairwise(times))
    inter_sample_intervals_within_policy = bool(
        intervals
        and all(
            policy.min_inter_sample_interval_seconds
            <= interval
            <= policy.max_inter_sample_interval_seconds
            for interval in intervals
        )
    )
    total_interval = final.observed_at_epoch_seconds - first.observed_at_epoch_seconds
    total_interval_within_policy = bool(
        policy.min_total_interval_seconds
        <= total_interval
        <= policy.max_total_interval_seconds
    )
    history_age = evaluated_at_epoch_seconds - final.observed_at_epoch_seconds
    history_fresh = 0 <= history_age <= policy.max_history_age_seconds
    no_future_evidence = bool(
        first.observed_at_epoch_seconds
        <= reference_stability_certificate.evaluated_at_epoch_seconds
        and all(
            sample.observed_at_epoch_seconds <= evaluated_at_epoch_seconds
            for sample in samples
        )
        and (
            sample_count < 2
            or samples[1].observed_at_epoch_seconds
            >= reference_stability_certificate.evaluated_at_epoch_seconds
        )
    )
    all_references_direct = all(
        sample.direct and policy.require_direct_local_branch
        for sample in samples
    )
    all_references_not_symbolic = all(not sample.symbolic for sample in samples)
    all_reference_store_sources = all(
        sample.reference_store_read and policy.require_reference_store_source
        for sample in samples
    )
    all_object_database_sources = all(
        sample.object_database_read and policy.require_object_database_source
        for sample in samples
    )
    all_working_tree_ignored = all(
        not sample.working_tree_read and policy.require_working_tree_ignored
        for sample in samples
    )
    all_reflog_ignored = all(
        not sample.reflog_read and policy.require_reflog_ignored
        for sample in samples
    )
    all_remote_ignored = all(
        not sample.remote_read and policy.require_remote_ignored
        for sample in samples
    )
    no_reference_deleted = all(not sample.reference_deleted for sample in samples)
    no_force_update_observed = all(
        not sample.force_update_observed for sample in samples
    )
    candidate_paths_complete = all(
        sample.candidate_path_oids
        and sample.candidate_path_oids[0] == sample.observed_tip_oid
        and sample.candidate_path_oids[-1] == sample.candidate_commit_oid
        for sample in samples
    )
    candidate_parent_edges_exact = all(
        sample.candidate_parent_edges
        == _path_edges(sample.candidate_path_oids)
        for sample in samples
    )
    transition_paths_complete_values: list[bool] = []
    for index, sample in enumerate(samples):
        expected_previous = (
            sample.observed_tip_oid
            if index == 0
            else samples[index - 1].observed_tip_oid
        )
        transition_paths_complete_values.append(
            bool(
                sample.transition_path_oids
                and sample.transition_path_oids[0]
                == sample.observed_tip_oid
                and sample.transition_path_oids[-1] == expected_previous
                and sample.previous_tip_oid == expected_previous
            )
        )
    transition_paths_complete = all(transition_paths_complete_values)
    transition_parent_edges_exact = all(
        sample.transition_parent_edges
        == _path_edges(sample.transition_path_oids)
        for sample in samples
    )
    queried_oid_sets_complete = all(
        sample.queried_oid_set_complete
        and sample.queried_oids
        == _canonical_strings(
            sample.candidate_path_oids + sample.transition_path_oids
        )
        for sample in samples
    )
    all_path_objects_are_commits = all(
        sample.all_objects_are_commits
        and sample.object_database_commit_oids == sample.queried_oids
        for sample in samples
    )
    candidate_present_in_every_sample = all(
        sample.candidate_commit_oid in sample.object_database_commit_oids
        for sample in samples
    )
    tips_present_in_every_sample = all(
        sample.observed_tip_oid in sample.object_database_commit_oids
        for sample in samples
    )
    previous_tips_present = all(
        sample.previous_tip_oid in sample.object_database_commit_oids
        for sample in samples
    )
    candidate_reachable_in_every_sample = all(
        (
            candidate_paths_complete,
            candidate_parent_edges_exact,
            queried_oid_sets_complete,
            all_path_objects_are_commits,
            candidate_present_in_every_sample,
            tips_present_in_every_sample,
            all_object_database_sources,
        )
    )
    frontier_transitions_monotone = all(
        (
            transition_paths_complete,
            transition_parent_edges_exact,
            queried_oid_sets_complete,
            all_path_objects_are_commits,
            tips_present_in_every_sample,
            previous_tips_present,
            all_object_database_sources,
        )
    )
    equal_relations = tuple(
        sample.observed_tip_oid == sample.previous_tip_oid
        for sample in samples
    )
    advanced_relations = tuple(not value for value in equal_relations)
    equal_tip_policy_satisfied = bool(
        not any(equal_relations) or policy.allow_equal_tip
    )
    tip_advance_policy_satisfied = bool(
        not any(advanced_relations) or policy.allow_tip_advance
    )
    candidate_depths_within_policy = all(
        len(sample.candidate_path_oids) - 1
        <= policy.max_candidate_reachability_depth
        for sample in samples
    )
    transition_depths_within_policy = all(
        len(sample.transition_path_oids) - 1 <= policy.max_transition_depth
        for sample in samples
    )
    total_queried_nodes = sum(len(sample.queried_oids) for sample in samples)
    total_queried_nodes_within_policy = (
        total_queried_nodes <= policy.max_total_queried_nodes
    )
    local_frontier_history_monotone = all(
        (
            anchor_sample_exact,
            sample_bindings_exact,
            common_observer_exact,
            observers_authorized,
            sequences_strictly_increasing,
            observation_times_strictly_increasing,
            inter_sample_intervals_within_policy,
            total_interval_within_policy,
            all_references_direct,
            all_references_not_symbolic,
            all_reference_store_sources,
            all_object_database_sources,
            all_working_tree_ignored,
            all_reflog_ignored,
            all_remote_ignored,
            no_reference_deleted,
            no_force_update_observed,
            frontier_transitions_monotone,
            equal_tip_policy_satisfied,
            tip_advance_policy_satisfied,
        )
    )
    candidate_reachability_continuous = all(
        (
            anchor_sample_exact,
            candidate_reachable_in_every_sample,
            frontier_transitions_monotone,
            candidate_depths_within_policy,
            transition_depths_within_policy,
            total_queried_nodes_within_policy,
        )
    )
    bounded_local_finality_verified = all(
        (
            reference_stability_certificate_committed,
            reference_stability_binding_exact,
            history_binding_exact,
            sample_count_within_policy,
            history_fresh,
            no_future_evidence,
            local_frontier_history_monotone,
            candidate_reachability_continuous,
        )
    )
    committed = all(
        (
            reference_stability_certificate_valid,
            reference_stability_certificate_committed,
            reference_stability_binding_exact,
            policy_valid,
            history_valid,
            history_binding_exact,
            anchor_sample_exact,
            sample_count_within_policy,
            sample_bindings_exact,
            sample_digests_valid,
            common_observer_exact,
            observers_authorized,
            sequences_strictly_increasing,
            observation_times_strictly_increasing,
            inter_sample_intervals_within_policy,
            total_interval_within_policy,
            history_fresh,
            no_future_evidence,
            all_references_direct,
            all_references_not_symbolic,
            all_reference_store_sources,
            all_object_database_sources,
            all_working_tree_ignored,
            all_reflog_ignored,
            all_remote_ignored,
            no_reference_deleted,
            no_force_update_observed,
            candidate_paths_complete,
            candidate_parent_edges_exact,
            transition_paths_complete,
            transition_parent_edges_exact,
            queried_oid_sets_complete,
            all_path_objects_are_commits,
            candidate_present_in_every_sample,
            tips_present_in_every_sample,
            previous_tips_present,
            candidate_reachable_in_every_sample,
            frontier_transitions_monotone,
            equal_tip_policy_satisfied,
            tip_advance_policy_satisfied,
            candidate_depths_within_policy,
            transition_depths_within_policy,
            total_queried_nodes_within_policy,
            local_frontier_history_monotone,
            candidate_reachability_continuous,
            bounded_local_finality_verified,
            not policy.allow_force_update,
            not policy.allow_reference_delete,
            not policy.allow_push,
        )
    )
    certificate = RepositoryLocalFrontierFinalityCertificate(
        certificate_id=certificate_id,
        status=CERTIFICATE_COMMITTED if committed else CERTIFICATE_REJECTED,
        reference_stability_certificate_digest=(
            reference_stability_certificate.certificate_digest
        ),
        policy_digest=policy.policy_digest,
        history_digest=history.history_digest,
        repository_id=reference_stability_certificate.repository_id,
        git_dir_fingerprint=(
            reference_stability_certificate.git_dir_fingerprint
        ),
        target_reference=reference_stability_certificate.target_reference,
        candidate_commit_oid=(
            reference_stability_certificate.candidate_commit_oid
        ),
        transaction_id=reference_stability_certificate.transaction_id,
        first_tip_oid=first.observed_tip_oid,
        final_tip_oid=final.observed_tip_oid,
        first_observed_at_epoch_seconds=first.observed_at_epoch_seconds,
        final_observed_at_epoch_seconds=final.observed_at_epoch_seconds,
        sample_count=sample_count,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        reference_stability_certificate_valid=(
            reference_stability_certificate_valid
        ),
        reference_stability_certificate_committed=(
            reference_stability_certificate_committed
        ),
        reference_stability_binding_exact=reference_stability_binding_exact,
        policy_valid=policy_valid,
        history_valid=history_valid,
        history_binding_exact=history_binding_exact,
        anchor_sample_exact=anchor_sample_exact,
        sample_count_within_policy=sample_count_within_policy,
        sample_bindings_exact=sample_bindings_exact,
        sample_digests_valid=sample_digests_valid,
        common_observer_exact=common_observer_exact,
        observers_authorized=observers_authorized,
        sequences_strictly_increasing=sequences_strictly_increasing,
        observation_times_strictly_increasing=(
            observation_times_strictly_increasing
        ),
        inter_sample_intervals_within_policy=(
            inter_sample_intervals_within_policy
        ),
        total_interval_within_policy=total_interval_within_policy,
        history_fresh=history_fresh,
        no_future_evidence=no_future_evidence,
        all_references_direct=all_references_direct,
        all_references_not_symbolic=all_references_not_symbolic,
        all_reference_store_sources=all_reference_store_sources,
        all_object_database_sources=all_object_database_sources,
        all_working_tree_ignored=all_working_tree_ignored,
        all_reflog_ignored=all_reflog_ignored,
        all_remote_ignored=all_remote_ignored,
        no_reference_deleted=no_reference_deleted,
        no_force_update_observed=no_force_update_observed,
        candidate_paths_complete=candidate_paths_complete,
        candidate_parent_edges_exact=candidate_parent_edges_exact,
        transition_paths_complete=transition_paths_complete,
        transition_parent_edges_exact=transition_parent_edges_exact,
        queried_oid_sets_complete=queried_oid_sets_complete,
        all_path_objects_are_commits=all_path_objects_are_commits,
        candidate_present_in_every_sample=(
            candidate_present_in_every_sample
        ),
        tips_present_in_every_sample=tips_present_in_every_sample,
        previous_tips_present=previous_tips_present,
        candidate_reachable_in_every_sample=(
            candidate_reachable_in_every_sample
        ),
        frontier_transitions_monotone=frontier_transitions_monotone,
        equal_tip_policy_satisfied=equal_tip_policy_satisfied,
        tip_advance_policy_satisfied=tip_advance_policy_satisfied,
        candidate_depths_within_policy=candidate_depths_within_policy,
        transition_depths_within_policy=transition_depths_within_policy,
        total_queried_nodes_within_policy=(
            total_queried_nodes_within_policy
        ),
        local_frontier_history_monotone=local_frontier_history_monotone,
        candidate_reachability_continuous=candidate_reachability_continuous,
        bounded_local_finality_verified=bounded_local_finality_verified,
        certificate_committed=committed,
        absolute_finality_claimed=False,
        remote_finality_claimed=False,
        branch_protection_verified=False,
        garbage_collection_retention_guaranteed=False,
        force_update_authorized=False,
        reference_delete_authorized=False,
        push_authorized=False,
        reference_mutation_performed=False,
        object_database_write_performed=False,
        working_tree_write_performed=False,
        index_write_performed=False,
        reflog_write_performed=False,
        remote_reference_updated=False,
        push_performed=False,
        signing_performed=False,
        certificate_digest="",
    )
    return replace(
        certificate,
        certificate_digest=repository_local_frontier_finality_certificate_digest(
            certificate
        ),
    )


def certify_repository_local_frontier_finality(
    certificate_id: str,
    reference_stability_certificate: (
        RepositoryReferenceStabilityReachabilityCertificate
    ),
    reference_stability_inputs: Mapping[str, Any],
    policy: RepositoryLocalFrontierFinalityPolicy,
    history: RepositoryLocalFrontierHistory,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryLocalFrontierFinalityCertificate:
    if not certificate_id:
        raise ValueError("local_frontier_finality_certificate_id_missing")
    if evaluated_at_epoch_seconds < 0:
        raise ValueError("local_frontier_evaluated_at_negative")
    stability_issues = _stability_issues(
        reference_stability_certificate,
        reference_stability_inputs,
    )
    if stability_issues:
        raise ValueError(
            f"reference_stability_certificate_invalid:{stability_issues[0]}"
        )
    for issues, prefix in (
        (
            repository_local_frontier_finality_policy_issues(policy),
            "local_frontier_finality_policy_invalid",
        ),
        (
            repository_local_frontier_history_issues(history),
            "local_frontier_history_invalid",
        ),
    ):
        if issues:
            raise ValueError(f"{prefix}:{issues[0]}")
    certificate = _construct_local_frontier_finality_certificate(
        certificate_id,
        reference_stability_certificate,
        reference_stability_inputs,
        policy,
        history,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues = repository_local_frontier_finality_certificate_issues(
        certificate,
        reference_stability_certificate,
        reference_stability_inputs,
        policy,
        history,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"local_frontier_finality_certificate_invalid:{issues[0]}")
    return certificate


def repository_local_frontier_finality_certificate_issues(
    certificate: RepositoryLocalFrontierFinalityCertificate,
    reference_stability_certificate: (
        RepositoryReferenceStabilityReachabilityCertificate
    ),
    reference_stability_inputs: Mapping[str, Any],
    policy: RepositoryLocalFrontierFinalityPolicy,
    history: RepositoryLocalFrontierHistory,
    *,
    evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    issues: list[str] = []
    if _stability_issues(
        reference_stability_certificate,
        reference_stability_inputs,
    ):
        issues.append("reference_stability_certificate_invalid")
        return tuple(issues)
    if repository_local_frontier_finality_policy_issues(policy):
        issues.append("local_frontier_policy_invalid")
        return tuple(issues)
    if repository_local_frontier_history_issues(history):
        issues.append("local_frontier_history_invalid")
        return tuple(issues)
    expected = _construct_local_frontier_finality_certificate(
        certificate.certificate_id,
        reference_stability_certificate,
        reference_stability_inputs,
        policy,
        history,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if certificate.to_dict() != expected.to_dict():
        issues.append("local_frontier_certificate_recomputation_mismatch")
    if certificate.status not in (CERTIFICATE_COMMITTED, CERTIFICATE_REJECTED):
        issues.append("local_frontier_certificate_status_invalid")
    forbidden_claims = (
        certificate.absolute_finality_claimed,
        certificate.remote_finality_claimed,
        certificate.branch_protection_verified,
        certificate.garbage_collection_retention_guaranteed,
    )
    if any(forbidden_claims):
        issues.append("local_frontier_certificate_forbidden_claim")
    forbidden_effects = (
        certificate.force_update_authorized,
        certificate.reference_delete_authorized,
        certificate.push_authorized,
        certificate.reference_mutation_performed,
        certificate.object_database_write_performed,
        certificate.working_tree_write_performed,
        certificate.index_write_performed,
        certificate.reflog_write_performed,
        certificate.remote_reference_updated,
        certificate.push_performed,
        certificate.signing_performed,
    )
    if any(forbidden_effects):
        issues.append("local_frontier_certificate_forbidden_effect")
    if certificate.status == CERTIFICATE_COMMITTED:
        required_true = (
            certificate.reference_stability_certificate_valid,
            certificate.reference_stability_certificate_committed,
            certificate.reference_stability_binding_exact,
            certificate.policy_valid,
            certificate.history_valid,
            certificate.history_binding_exact,
            certificate.anchor_sample_exact,
            certificate.sample_count_within_policy,
            certificate.sample_bindings_exact,
            certificate.sample_digests_valid,
            certificate.common_observer_exact,
            certificate.observers_authorized,
            certificate.sequences_strictly_increasing,
            certificate.observation_times_strictly_increasing,
            certificate.inter_sample_intervals_within_policy,
            certificate.total_interval_within_policy,
            certificate.history_fresh,
            certificate.no_future_evidence,
            certificate.all_references_direct,
            certificate.all_references_not_symbolic,
            certificate.all_reference_store_sources,
            certificate.all_object_database_sources,
            certificate.all_working_tree_ignored,
            certificate.all_reflog_ignored,
            certificate.all_remote_ignored,
            certificate.no_reference_deleted,
            certificate.no_force_update_observed,
            certificate.candidate_paths_complete,
            certificate.candidate_parent_edges_exact,
            certificate.transition_paths_complete,
            certificate.transition_parent_edges_exact,
            certificate.queried_oid_sets_complete,
            certificate.all_path_objects_are_commits,
            certificate.candidate_present_in_every_sample,
            certificate.tips_present_in_every_sample,
            certificate.previous_tips_present,
            certificate.candidate_reachable_in_every_sample,
            certificate.frontier_transitions_monotone,
            certificate.equal_tip_policy_satisfied,
            certificate.tip_advance_policy_satisfied,
            certificate.candidate_depths_within_policy,
            certificate.transition_depths_within_policy,
            certificate.total_queried_nodes_within_policy,
            certificate.local_frontier_history_monotone,
            certificate.candidate_reachability_continuous,
            certificate.bounded_local_finality_verified,
            certificate.certificate_committed,
        )
        if not all(required_true):
            issues.append("local_frontier_committed_invariant_false")
    elif certificate.certificate_committed:
        issues.append("local_frontier_rejected_marked_committed")
    if (
        certificate.certificate_digest
        != repository_local_frontier_finality_certificate_digest(certificate)
    ):
        issues.append("local_frontier_certificate_digest_mismatch")
    return tuple(issues)
