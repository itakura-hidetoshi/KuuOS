#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import re
from typing import Any, Mapping

from runtime.kuuos_repository_reference_stability_types_v0_99 import (
    CERTIFICATE_COMMITTED,
    CERTIFICATE_REJECTED,
    RepositoryCommitReachabilityCertificate,
    RepositoryDelayedReferenceObservation,
    RepositoryReferenceStabilityPolicy,
    RepositoryReferenceStabilityReachabilityCertificate,
    repository_commit_reachability_certificate_digest,
    repository_delayed_reference_observation_digest,
    repository_reference_stability_policy_digest,
    repository_reference_stability_reachability_certificate_digest,
)
from runtime.kuuos_repository_reference_update_receipt_types_v0_98 import (
    RECEIPT_COMMITTED,
    RepositoryReferenceUpdateReceipt,
)
from runtime.kuuos_repository_reference_update_receipt_v0_98 import (
    repository_reference_update_receipt_issues,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _canonical_strings(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def _canonical_edges(
    values: tuple[tuple[str, str], ...],
) -> tuple[tuple[str, str], ...]:
    return tuple(values)


def _path_edges(path_oids: tuple[str, ...]) -> tuple[tuple[str, str], ...]:
    return tuple(zip(path_oids, path_oids[1:]))


def build_repository_reference_stability_policy(
    policy_id: str,
    *,
    authorized_observer_ids: tuple[str, ...],
    min_stability_interval_seconds: int,
    max_stability_interval_seconds: int,
    max_delayed_observation_age_seconds: int,
    max_reachability_certificate_age_seconds: int,
    max_reachability_depth: int,
    max_reachability_nodes: int,
    allow_tip_advance: bool = True,
) -> RepositoryReferenceStabilityPolicy:
    policy = RepositoryReferenceStabilityPolicy(
        policy_id=policy_id,
        authorized_observer_ids=_canonical_strings(authorized_observer_ids),
        min_stability_interval_seconds=min_stability_interval_seconds,
        max_stability_interval_seconds=max_stability_interval_seconds,
        max_delayed_observation_age_seconds=max_delayed_observation_age_seconds,
        max_reachability_certificate_age_seconds=(
            max_reachability_certificate_age_seconds
        ),
        max_reachability_depth=max_reachability_depth,
        max_reachability_nodes=max_reachability_nodes,
        allow_tip_advance=allow_tip_advance,
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
        policy_digest=repository_reference_stability_policy_digest(policy),
    )
    issues = repository_reference_stability_policy_issues(policy)
    if issues:
        raise ValueError(f"reference_stability_policy_invalid:{issues[0]}")
    return policy


def repository_reference_stability_policy_issues(
    policy: RepositoryReferenceStabilityPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("reference_stability_policy_id_missing")
    if (
        policy.authorized_observer_ids
        != _canonical_strings(policy.authorized_observer_ids)
        or not policy.authorized_observer_ids
        or any(not value for value in policy.authorized_observer_ids)
    ):
        issues.append("reference_stability_observer_ids_invalid")
    if policy.min_stability_interval_seconds <= 0:
        issues.append("reference_stability_min_interval_invalid")
    if (
        policy.max_stability_interval_seconds
        < policy.min_stability_interval_seconds
    ):
        issues.append("reference_stability_interval_bounds_invalid")
    if any(
        value <= 0
        for value in (
            policy.max_delayed_observation_age_seconds,
            policy.max_reachability_certificate_age_seconds,
            policy.max_reachability_nodes,
        )
    ):
        issues.append("reference_stability_positive_bound_invalid")
    if policy.max_reachability_depth < 0:
        issues.append("reference_stability_depth_bound_invalid")
    if policy.max_reachability_nodes < policy.max_reachability_depth + 1:
        issues.append("reference_stability_node_bound_too_small")
    required = (
        policy.require_direct_local_branch,
        policy.require_reference_store_source,
        policy.require_object_database_source,
        policy.require_working_tree_ignored,
        policy.require_reflog_ignored,
        policy.require_remote_ignored,
    )
    if not all(required):
        issues.append("reference_stability_required_safeguard_disabled")
    if policy.allow_force_update:
        issues.append("reference_stability_force_policy_forbidden")
    if policy.allow_reference_delete:
        issues.append("reference_stability_delete_policy_forbidden")
    if policy.allow_push:
        issues.append("reference_stability_push_policy_forbidden")
    if policy.policy_digest != repository_reference_stability_policy_digest(policy):
        issues.append("reference_stability_policy_digest_mismatch")
    return tuple(issues)


def build_repository_delayed_reference_observation(
    observation_id: str,
    observer_id: str,
    receipt: RepositoryReferenceUpdateReceipt,
    *,
    observed_tip_oid: str,
    sequence_number: int,
    observed_at_epoch_seconds: int,
    direct: bool = True,
    symbolic: bool = False,
    reference_store_read: bool = True,
    object_database_read: bool = True,
    working_tree_read: bool = False,
    reflog_read: bool = False,
    remote_read: bool = False,
    reference_deleted: bool = False,
    force_update_observed: bool = False,
) -> RepositoryDelayedReferenceObservation:
    observation = RepositoryDelayedReferenceObservation(
        observation_id=observation_id,
        observer_id=observer_id,
        transaction_id=receipt.transaction_id,
        repository_id=receipt.repository_id,
        git_dir_fingerprint=receipt.git_dir_fingerprint,
        target_reference=receipt.target_reference,
        candidate_commit_oid=receipt.proposed_new_oid,
        observed_tip_oid=observed_tip_oid,
        direct=direct,
        symbolic=symbolic,
        reference_store_read=reference_store_read,
        object_database_read=object_database_read,
        working_tree_read=working_tree_read,
        reflog_read=reflog_read,
        remote_read=remote_read,
        reference_deleted=reference_deleted,
        force_update_observed=force_update_observed,
        sequence_number=sequence_number,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        observation_digest="",
    )
    observation = replace(
        observation,
        observation_digest=repository_delayed_reference_observation_digest(
            observation
        ),
    )
    issues = repository_delayed_reference_observation_issues(observation)
    if issues:
        raise ValueError(f"delayed_reference_observation_invalid:{issues[0]}")
    return observation


def repository_delayed_reference_observation_issues(
    observation: RepositoryDelayedReferenceObservation,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        observation.observation_id,
        observation.observer_id,
        observation.transaction_id,
        observation.repository_id,
        observation.target_reference,
    )
    if any(not value for value in required):
        issues.append("delayed_reference_observation_required_field_missing")
    if not _HEX64.fullmatch(observation.git_dir_fingerprint):
        issues.append("delayed_reference_observation_git_dir_invalid")
    if not _HEX40.fullmatch(observation.candidate_commit_oid):
        issues.append("delayed_reference_observation_candidate_oid_invalid")
    if not _HEX40.fullmatch(observation.observed_tip_oid):
        issues.append("delayed_reference_observation_tip_oid_invalid")
    if observation.sequence_number < 0:
        issues.append("delayed_reference_observation_sequence_negative")
    if observation.observed_at_epoch_seconds < 0:
        issues.append("delayed_reference_observation_time_negative")
    if (
        observation.observation_digest
        != repository_delayed_reference_observation_digest(observation)
    ):
        issues.append("delayed_reference_observation_digest_mismatch")
    return tuple(issues)


def build_repository_commit_reachability_certificate(
    certificate_id: str,
    observer_id: str,
    receipt: RepositoryReferenceUpdateReceipt,
    delayed_observation: RepositoryDelayedReferenceObservation,
    *,
    path_oids: tuple[str, ...],
    observed_at_epoch_seconds: int,
    queried_oid_set_complete: bool = True,
    all_objects_are_commits: bool = True,
    object_database_read: bool = True,
    working_tree_read: bool = False,
    reflog_read: bool = False,
    remote_read: bool = False,
) -> RepositoryCommitReachabilityCertificate:
    canonical_path = tuple(path_oids)
    queried_oids = _canonical_strings(canonical_path)
    certificate = RepositoryCommitReachabilityCertificate(
        certificate_id=certificate_id,
        observer_id=observer_id,
        transaction_id=receipt.transaction_id,
        repository_id=receipt.repository_id,
        git_dir_fingerprint=receipt.git_dir_fingerprint,
        target_reference=receipt.target_reference,
        tip_oid=delayed_observation.observed_tip_oid,
        candidate_commit_oid=receipt.proposed_new_oid,
        path_oids=canonical_path,
        parent_edges=_path_edges(canonical_path),
        queried_oids=queried_oids,
        object_database_commit_oids=queried_oids,
        queried_oid_set_complete=queried_oid_set_complete,
        all_objects_are_commits=all_objects_are_commits,
        object_database_read=object_database_read,
        working_tree_read=working_tree_read,
        reflog_read=reflog_read,
        remote_read=remote_read,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        certificate_digest="",
    )
    certificate = replace(
        certificate,
        certificate_digest=repository_commit_reachability_certificate_digest(
            certificate
        ),
    )
    issues = repository_commit_reachability_certificate_issues(certificate)
    if issues:
        raise ValueError(f"commit_reachability_certificate_invalid:{issues[0]}")
    return certificate


def repository_commit_reachability_certificate_issues(
    certificate: RepositoryCommitReachabilityCertificate,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        certificate.certificate_id,
        certificate.observer_id,
        certificate.transaction_id,
        certificate.repository_id,
        certificate.target_reference,
    )
    if any(not value for value in required):
        issues.append("commit_reachability_required_field_missing")
    if not _HEX64.fullmatch(certificate.git_dir_fingerprint):
        issues.append("commit_reachability_git_dir_invalid")
    if not _HEX40.fullmatch(certificate.tip_oid):
        issues.append("commit_reachability_tip_oid_invalid")
    if not _HEX40.fullmatch(certificate.candidate_commit_oid):
        issues.append("commit_reachability_candidate_oid_invalid")
    if not certificate.path_oids:
        issues.append("commit_reachability_path_empty")
    elif any(not _HEX40.fullmatch(oid) for oid in certificate.path_oids):
        issues.append("commit_reachability_path_oid_invalid")
    if len(set(certificate.path_oids)) != len(certificate.path_oids):
        issues.append("commit_reachability_path_cycle")
    if certificate.parent_edges != _canonical_edges(certificate.parent_edges):
        issues.append("commit_reachability_edges_invalid")
    if any(
        len(edge) != 2
        or not _HEX40.fullmatch(edge[0])
        or not _HEX40.fullmatch(edge[1])
        for edge in certificate.parent_edges
    ):
        issues.append("commit_reachability_edge_oid_invalid")
    if certificate.queried_oids != _canonical_strings(certificate.queried_oids):
        issues.append("commit_reachability_queried_oids_not_canonical")
    if certificate.object_database_commit_oids != _canonical_strings(
        certificate.object_database_commit_oids
    ):
        issues.append("commit_reachability_commit_oids_not_canonical")
    if any(not _HEX40.fullmatch(oid) for oid in certificate.queried_oids):
        issues.append("commit_reachability_queried_oid_invalid")
    if any(
        not _HEX40.fullmatch(oid)
        for oid in certificate.object_database_commit_oids
    ):
        issues.append("commit_reachability_object_oid_invalid")
    if certificate.observed_at_epoch_seconds < 0:
        issues.append("commit_reachability_time_negative")
    if (
        certificate.certificate_digest
        != repository_commit_reachability_certificate_digest(certificate)
    ):
        issues.append("commit_reachability_digest_mismatch")
    return tuple(issues)


def _receipt_issues(
    receipt: RepositoryReferenceUpdateReceipt,
    receipt_inputs: Mapping[str, Any],
) -> tuple[str, ...]:
    try:
        return repository_reference_update_receipt_issues(
            receipt,
            **dict(receipt_inputs),
        )
    except (TypeError, ValueError, AttributeError, KeyError):
        return ("reference_update_receipt_inputs_invalid",)


def _construct_reference_stability_certificate(
    certificate_id: str,
    receipt: RepositoryReferenceUpdateReceipt,
    receipt_inputs: Mapping[str, Any],
    policy: RepositoryReferenceStabilityPolicy,
    delayed_observation: RepositoryDelayedReferenceObservation,
    reachability: RepositoryCommitReachabilityCertificate,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryReferenceStabilityReachabilityCertificate:
    post_observation = receipt_inputs.get("post_reference_observation")
    receipt_issues = _receipt_issues(receipt, receipt_inputs)
    reference_update_receipt_valid = not receipt_issues
    reference_update_receipt_committed = bool(
        reference_update_receipt_valid
        and receipt.status == RECEIPT_COMMITTED
        and receipt.receipt_committed
        and receipt.reference_update_confirmed
        and receipt.atomic_reference_nonce_transition_confirmed
    )
    reference_update_receipt_binding_exact = bool(
        post_observation is not None
        and receipt.post_reference_observation_digest
        == post_observation.receipt_digest
        and receipt.repository_id == post_observation.repository_id
        and receipt.git_dir_fingerprint == post_observation.git_dir_fingerprint
        and receipt.target_reference == post_observation.target_reference
        and receipt.proposed_new_oid == post_observation.observed_oid
        and receipt.transaction_id == post_observation.transaction_id
    )
    stability_policy_valid = not repository_reference_stability_policy_issues(
        policy
    )
    delayed_observation_valid = not repository_delayed_reference_observation_issues(
        delayed_observation
    )
    delayed_observation_binding_exact = bool(
        delayed_observation.transaction_id == receipt.transaction_id
        and delayed_observation.repository_id == receipt.repository_id
        and delayed_observation.git_dir_fingerprint == receipt.git_dir_fingerprint
        and delayed_observation.target_reference == receipt.target_reference
        and delayed_observation.candidate_commit_oid == receipt.proposed_new_oid
    )
    delayed_age = (
        evaluated_at_epoch_seconds
        - delayed_observation.observed_at_epoch_seconds
    )
    delayed_observation_fresh = bool(
        0 <= delayed_age <= policy.max_delayed_observation_age_seconds
    )
    stability_interval = (
        delayed_observation.observed_at_epoch_seconds
        - receipt.evaluated_at_epoch_seconds
    )
    stability_interval_within_policy = bool(
        policy.min_stability_interval_seconds
        <= stability_interval
        <= policy.max_stability_interval_seconds
    )
    delayed_reference_direct = bool(
        delayed_observation.direct and policy.require_direct_local_branch
    )
    delayed_reference_not_symbolic = not delayed_observation.symbolic
    delayed_reference_store_source = bool(
        delayed_observation.reference_store_read
        and policy.require_reference_store_source
    )
    delayed_object_database_source = bool(
        delayed_observation.object_database_read
        and policy.require_object_database_source
    )
    delayed_working_tree_ignored = bool(
        not delayed_observation.working_tree_read
        and policy.require_working_tree_ignored
    )
    delayed_reflog_ignored = bool(
        not delayed_observation.reflog_read and policy.require_reflog_ignored
    )
    delayed_remote_ignored = bool(
        not delayed_observation.remote_read and policy.require_remote_ignored
    )
    delayed_reference_not_deleted = not delayed_observation.reference_deleted
    no_force_update_observed = not delayed_observation.force_update_observed
    delayed_sequence_monotone = bool(
        post_observation is not None
        and delayed_observation.sequence_number >= post_observation.sequence_number
    )
    observer_authorized = bool(
        delayed_observation.observer_id == reachability.observer_id
        and delayed_observation.observer_id in policy.authorized_observer_ids
    )

    reachability_certificate_valid = not (
        repository_commit_reachability_certificate_issues(reachability)
    )
    reachability_certificate_binding_exact = bool(
        reachability.transaction_id == receipt.transaction_id
        and reachability.repository_id == receipt.repository_id
        and reachability.git_dir_fingerprint == receipt.git_dir_fingerprint
        and reachability.target_reference == receipt.target_reference
        and reachability.tip_oid == delayed_observation.observed_tip_oid
        and reachability.candidate_commit_oid == receipt.proposed_new_oid
    )
    reachability_age = (
        evaluated_at_epoch_seconds - reachability.observed_at_epoch_seconds
    )
    reachability_certificate_fresh = bool(
        0
        <= reachability_age
        <= policy.max_reachability_certificate_age_seconds
    )
    reachability_evidence_time_exact = (
        reachability.observed_at_epoch_seconds
        == delayed_observation.observed_at_epoch_seconds
    )
    reachability_path_complete = bool(
        reachability.path_oids
        and reachability.path_oids[0] == reachability.tip_oid
        and reachability.path_oids[-1] == reachability.candidate_commit_oid
    )
    reachability_parent_edges_exact = (
        reachability.parent_edges == _path_edges(reachability.path_oids)
    )
    canonical_path_set = _canonical_strings(reachability.path_oids)
    queried_oid_set_complete = bool(
        reachability.queried_oid_set_complete
        and reachability.queried_oids == canonical_path_set
    )
    all_reachability_objects_are_commits = bool(
        reachability.all_objects_are_commits
        and reachability.object_database_commit_oids
        == reachability.queried_oids
    )
    candidate_commit_present = (
        receipt.proposed_new_oid in reachability.object_database_commit_oids
    )
    delayed_tip_present = (
        delayed_observation.observed_tip_oid
        in reachability.object_database_commit_oids
    )
    candidate_is_delayed_tip = (
        delayed_observation.observed_tip_oid == receipt.proposed_new_oid
    )
    delayed_tip_advanced = not candidate_is_delayed_tip
    tip_advance_allowed = bool(
        candidate_is_delayed_tip or policy.allow_tip_advance
    )
    reachability_sources_exact = bool(
        reachability.object_database_read
        and not reachability.working_tree_read
        and not reachability.reflog_read
        and not reachability.remote_read
    )
    candidate_reachable_from_delayed_tip = all(
        (
            reachability_path_complete,
            reachability_parent_edges_exact,
            queried_oid_set_complete,
            all_reachability_objects_are_commits,
            candidate_commit_present,
            delayed_tip_present,
            reachability_sources_exact,
        )
    )
    reachability_depth = max(len(reachability.path_oids) - 1, 0)
    reachability_depth_within_policy = (
        reachability_depth <= policy.max_reachability_depth
    )
    reachability_nodes_within_policy = (
        0 < len(reachability.path_oids) <= policy.max_reachability_nodes
    )
    no_future_evidence = bool(
        receipt.evaluated_at_epoch_seconds
        <= delayed_observation.observed_at_epoch_seconds
        == reachability.observed_at_epoch_seconds
        <= evaluated_at_epoch_seconds
    )
    reference_stability_verified = all(
        (
            reference_update_receipt_committed,
            delayed_observation_binding_exact,
            delayed_observation_fresh,
            stability_interval_within_policy,
            delayed_reference_direct,
            delayed_reference_not_symbolic,
            delayed_reference_store_source,
            delayed_object_database_source,
            delayed_working_tree_ignored,
            delayed_reflog_ignored,
            delayed_remote_ignored,
            delayed_reference_not_deleted,
            no_force_update_observed,
            delayed_sequence_monotone,
            observer_authorized,
        )
    )
    candidate_reachability_preserved = all(
        (
            candidate_reachable_from_delayed_tip,
            reachability_certificate_binding_exact,
            reachability_certificate_fresh,
            reachability_evidence_time_exact,
            reachability_depth_within_policy,
            reachability_nodes_within_policy,
            tip_advance_allowed,
        )
    )
    committed = all(
        (
            reference_update_receipt_valid,
            reference_update_receipt_committed,
            reference_update_receipt_binding_exact,
            stability_policy_valid,
            delayed_observation_valid,
            delayed_observation_binding_exact,
            delayed_observation_fresh,
            stability_interval_within_policy,
            delayed_reference_direct,
            delayed_reference_not_symbolic,
            delayed_reference_store_source,
            delayed_object_database_source,
            delayed_working_tree_ignored,
            delayed_reflog_ignored,
            delayed_remote_ignored,
            delayed_reference_not_deleted,
            no_force_update_observed,
            delayed_sequence_monotone,
            observer_authorized,
            reachability_certificate_valid,
            reachability_certificate_binding_exact,
            reachability_certificate_fresh,
            reachability_evidence_time_exact,
            reachability_path_complete,
            reachability_parent_edges_exact,
            queried_oid_set_complete,
            all_reachability_objects_are_commits,
            candidate_commit_present,
            delayed_tip_present,
            tip_advance_allowed,
            candidate_reachable_from_delayed_tip,
            reachability_depth_within_policy,
            reachability_nodes_within_policy,
            no_future_evidence,
            reference_stability_verified,
            candidate_reachability_preserved,
            not policy.allow_force_update,
            not policy.allow_reference_delete,
            not policy.allow_push,
        )
    )
    certificate = RepositoryReferenceStabilityReachabilityCertificate(
        certificate_id=certificate_id,
        status=CERTIFICATE_COMMITTED if committed else CERTIFICATE_REJECTED,
        reference_update_receipt_digest=receipt.receipt_digest,
        stability_policy_digest=policy.policy_digest,
        delayed_reference_observation_digest=(
            delayed_observation.observation_digest
        ),
        reachability_certificate_digest=reachability.certificate_digest,
        repository_id=receipt.repository_id,
        git_dir_fingerprint=receipt.git_dir_fingerprint,
        target_reference=receipt.target_reference,
        candidate_commit_oid=receipt.proposed_new_oid,
        delayed_tip_oid=delayed_observation.observed_tip_oid,
        transaction_id=receipt.transaction_id,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        reference_update_receipt_valid=reference_update_receipt_valid,
        reference_update_receipt_committed=reference_update_receipt_committed,
        reference_update_receipt_binding_exact=(
            reference_update_receipt_binding_exact
        ),
        stability_policy_valid=stability_policy_valid,
        delayed_observation_valid=delayed_observation_valid,
        delayed_observation_binding_exact=delayed_observation_binding_exact,
        delayed_observation_fresh=delayed_observation_fresh,
        stability_interval_within_policy=stability_interval_within_policy,
        delayed_reference_direct=delayed_reference_direct,
        delayed_reference_not_symbolic=delayed_reference_not_symbolic,
        delayed_reference_store_source=delayed_reference_store_source,
        delayed_object_database_source=delayed_object_database_source,
        delayed_working_tree_ignored=delayed_working_tree_ignored,
        delayed_reflog_ignored=delayed_reflog_ignored,
        delayed_remote_ignored=delayed_remote_ignored,
        delayed_reference_not_deleted=delayed_reference_not_deleted,
        no_force_update_observed=no_force_update_observed,
        delayed_sequence_monotone=delayed_sequence_monotone,
        observer_authorized=observer_authorized,
        reachability_certificate_valid=reachability_certificate_valid,
        reachability_certificate_binding_exact=(
            reachability_certificate_binding_exact
        ),
        reachability_certificate_fresh=reachability_certificate_fresh,
        reachability_evidence_time_exact=reachability_evidence_time_exact,
        reachability_path_complete=reachability_path_complete,
        reachability_parent_edges_exact=reachability_parent_edges_exact,
        queried_oid_set_complete=queried_oid_set_complete,
        all_reachability_objects_are_commits=(
            all_reachability_objects_are_commits
        ),
        candidate_commit_present=candidate_commit_present,
        delayed_tip_present=delayed_tip_present,
        candidate_is_delayed_tip=candidate_is_delayed_tip,
        delayed_tip_advanced=delayed_tip_advanced,
        tip_advance_allowed=tip_advance_allowed,
        candidate_reachable_from_delayed_tip=(
            candidate_reachable_from_delayed_tip
        ),
        reachability_depth_within_policy=reachability_depth_within_policy,
        reachability_nodes_within_policy=reachability_nodes_within_policy,
        no_future_evidence=no_future_evidence,
        reference_stability_verified=reference_stability_verified,
        candidate_reachability_preserved=candidate_reachability_preserved,
        certificate_committed=committed,
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
        certificate_digest=(
            repository_reference_stability_reachability_certificate_digest(
                certificate
            )
        ),
    )


def certify_repository_reference_stability_and_reachability(
    certificate_id: str,
    receipt: RepositoryReferenceUpdateReceipt,
    receipt_inputs: Mapping[str, Any],
    policy: RepositoryReferenceStabilityPolicy,
    delayed_observation: RepositoryDelayedReferenceObservation,
    reachability: RepositoryCommitReachabilityCertificate,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryReferenceStabilityReachabilityCertificate:
    if not certificate_id:
        raise ValueError("reference_stability_certificate_id_missing")
    if evaluated_at_epoch_seconds < 0:
        raise ValueError("reference_stability_evaluated_at_negative")
    receipt_issues = _receipt_issues(receipt, receipt_inputs)
    if receipt_issues:
        raise ValueError(f"reference_update_receipt_invalid:{receipt_issues[0]}")
    for issues, prefix in (
        (
            repository_reference_stability_policy_issues(policy),
            "reference_stability_policy_invalid",
        ),
        (
            repository_delayed_reference_observation_issues(
                delayed_observation
            ),
            "delayed_reference_observation_invalid",
        ),
        (
            repository_commit_reachability_certificate_issues(reachability),
            "commit_reachability_certificate_invalid",
        ),
    ):
        if issues:
            raise ValueError(f"{prefix}:{issues[0]}")
    certificate = _construct_reference_stability_certificate(
        certificate_id,
        receipt,
        receipt_inputs,
        policy,
        delayed_observation,
        reachability,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues = repository_reference_stability_reachability_certificate_issues(
        certificate,
        receipt,
        receipt_inputs,
        policy,
        delayed_observation,
        reachability,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"reference_stability_certificate_invalid:{issues[0]}")
    return certificate


def repository_reference_stability_reachability_certificate_issues(
    certificate: RepositoryReferenceStabilityReachabilityCertificate,
    receipt: RepositoryReferenceUpdateReceipt,
    receipt_inputs: Mapping[str, Any],
    policy: RepositoryReferenceStabilityPolicy,
    delayed_observation: RepositoryDelayedReferenceObservation,
    reachability: RepositoryCommitReachabilityCertificate,
    *,
    evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    issues: list[str] = []
    if _receipt_issues(receipt, receipt_inputs):
        issues.append("reference_update_receipt_invalid")
        return tuple(issues)
    for validator, name in (
        (
            repository_reference_stability_policy_issues(policy),
            "stability_policy_invalid",
        ),
        (
            repository_delayed_reference_observation_issues(
                delayed_observation
            ),
            "delayed_observation_invalid",
        ),
        (
            repository_commit_reachability_certificate_issues(reachability),
            "reachability_certificate_invalid",
        ),
    ):
        if validator:
            issues.append(name)
            return tuple(issues)
    expected = _construct_reference_stability_certificate(
        certificate.certificate_id,
        receipt,
        receipt_inputs,
        policy,
        delayed_observation,
        reachability,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if certificate.to_dict() != expected.to_dict():
        issues.append("reference_stability_certificate_recomputation_mismatch")
    if certificate.status not in (CERTIFICATE_COMMITTED, CERTIFICATE_REJECTED):
        issues.append("reference_stability_certificate_status_invalid")
    forbidden = (
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
    if any(forbidden):
        issues.append("reference_stability_certificate_forbidden_effect")
    if certificate.status == CERTIFICATE_COMMITTED:
        required_true = (
            certificate.reference_update_receipt_valid,
            certificate.reference_update_receipt_committed,
            certificate.reference_update_receipt_binding_exact,
            certificate.stability_policy_valid,
            certificate.delayed_observation_valid,
            certificate.delayed_observation_binding_exact,
            certificate.delayed_observation_fresh,
            certificate.stability_interval_within_policy,
            certificate.delayed_reference_direct,
            certificate.delayed_reference_not_symbolic,
            certificate.delayed_reference_store_source,
            certificate.delayed_object_database_source,
            certificate.delayed_working_tree_ignored,
            certificate.delayed_reflog_ignored,
            certificate.delayed_remote_ignored,
            certificate.delayed_reference_not_deleted,
            certificate.no_force_update_observed,
            certificate.delayed_sequence_monotone,
            certificate.observer_authorized,
            certificate.reachability_certificate_valid,
            certificate.reachability_certificate_binding_exact,
            certificate.reachability_certificate_fresh,
            certificate.reachability_evidence_time_exact,
            certificate.reachability_path_complete,
            certificate.reachability_parent_edges_exact,
            certificate.queried_oid_set_complete,
            certificate.all_reachability_objects_are_commits,
            certificate.candidate_commit_present,
            certificate.delayed_tip_present,
            certificate.tip_advance_allowed,
            certificate.candidate_reachable_from_delayed_tip,
            certificate.reachability_depth_within_policy,
            certificate.reachability_nodes_within_policy,
            certificate.no_future_evidence,
            certificate.reference_stability_verified,
            certificate.candidate_reachability_preserved,
            certificate.certificate_committed,
        )
        if not all(required_true):
            issues.append("reference_stability_committed_invariant_false")
        if not (
            certificate.candidate_is_delayed_tip
            or certificate.delayed_tip_advanced
        ):
            issues.append("reference_stability_tip_relation_missing")
    elif certificate.certificate_committed:
        issues.append("reference_stability_rejected_marked_committed")
    if (
        certificate.certificate_digest
        != repository_reference_stability_reachability_certificate_digest(
            certificate
        )
    ):
        issues.append("reference_stability_certificate_digest_mismatch")
    return tuple(issues)
