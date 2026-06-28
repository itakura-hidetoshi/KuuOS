#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Iterable

from runtime.kuuos_repository_alignment_normal_form_v0_80 import (
    certify_repository_alignment_normal_form,
)
from runtime.kuuos_repository_certificate_chain_types_v0_82 import (
    RepositoryCertificateChainRecord,
)
from runtime.kuuos_repository_certificate_chain_v0_82 import (
    certificate_chain_record_issues,
)
from runtime.kuuos_repository_git_revision_adapter_v0_83 import (
    _canonical_inventory,
    capture_git_object_snapshot,
    git_changed_paths,
    git_commit_parents,
    resolve_git_commit,
)
from runtime.kuuos_repository_merge_certificate_types_v0_84 import (
    RepositoryMergeCertificate,
    RepositoryMergeObservation,
    repository_merge_certificate_digest,
    repository_merge_observation_digest,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot


def _common_prefix(
    left: tuple[str, ...],
    right: tuple[str, ...],
) -> tuple[str, ...]:
    prefix: list[str] = []
    for left_sha, right_sha in zip(left, right):
        if left_sha != right_sha:
            break
        prefix.append(left_sha)
    return tuple(prefix)


def _normal_form_bound(snapshot: RepositorySnapshot, certificate) -> bool:
    return (
        certificate.initial_snapshot_digest == snapshot.digest
        and certificate.initial_score == 0
        and certificate.all_transitions_strictly_decreasing
        and certificate.all_terminals_fixed_points
        and certificate.unique_terminal
        and certificate.unique_terminal_digest == snapshot.digest
        and certificate.deterministic_trace_matches_terminal
    )


def repository_merge_certificate_issues(
    certificate: RepositoryMergeCertificate,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not certificate.merge_id:
        issues.append("merge_id_missing")
    if not certificate.chain_id:
        issues.append("chain_id_missing")
    if certificate.certificate_digest != repository_merge_certificate_digest(
        certificate
    ):
        issues.append("certificate_digest_mismatch")
    if certificate.common_prefix_length <= 0:
        issues.append("common_prefix_missing")
    if not certificate.parent_order_exact:
        issues.append("parent_order_mismatch")
    if not certificate.branch_histories_disjoint_after_fork:
        issues.append("branch_history_overlap")
    if not certificate.changed_paths_disjoint:
        issues.append("changed_path_overlap")
    if not certificate.merge_normal_form_preserved:
        issues.append("merge_normal_form_not_preserved")
    if certificate.external_approval_required:
        issues.append("unexpected_external_approval")
    return tuple(issues)


def observe_repository_merge_from_git(
    root: Path,
    left_revision: str,
    right_revision: str,
    merge_revision: str,
    relative_paths: Iterable[str],
) -> tuple[
    RepositorySnapshot,
    RepositorySnapshot,
    RepositorySnapshot,
    RepositoryMergeObservation,
]:
    root = root.resolve()
    inventory = _canonical_inventory(relative_paths)
    left_sha = resolve_git_commit(root, left_revision)
    right_sha = resolve_git_commit(root, right_revision)
    merge_sha = resolve_git_commit(root, merge_revision)
    merge_parents = git_commit_parents(root, merge_sha)
    if merge_parents != (left_sha, right_sha):
        raise ValueError("merge_parent_order_mismatch")

    left_changed = git_changed_paths(root, left_sha, merge_sha)
    right_changed = git_changed_paths(root, right_sha, merge_sha)
    union_changed = tuple(sorted(set(left_changed) | set(right_changed)))
    overlap = tuple(sorted(set(left_changed) & set(right_changed)))
    outside = tuple(sorted(set(union_changed) - set(inventory)))
    if outside:
        raise ValueError(f"merge_changed_path_outside_inventory:{outside[0]}")

    left_snapshot = capture_git_object_snapshot(root, left_sha, inventory)
    right_snapshot = capture_git_object_snapshot(root, right_sha, inventory)
    merge_snapshot = capture_git_object_snapshot(root, merge_sha, inventory)
    observation = RepositoryMergeObservation(
        root.name,
        left_sha,
        right_sha,
        merge_sha,
        merge_parents,
        left_changed,
        right_changed,
        union_changed,
        overlap,
        inventory,
        left_snapshot.digest,
        right_snapshot.digest,
        merge_snapshot.digest,
        True,
        False,
        "",
    )
    observation = replace(
        observation,
        observation_digest=repository_merge_observation_digest(observation),
    )
    return left_snapshot, right_snapshot, merge_snapshot, observation


def certify_repository_merge_from_git(
    merge_id: str,
    chain_id: str,
    left_record: RepositoryCertificateChainRecord,
    right_record: RepositoryCertificateChainRecord,
    root: Path,
    left_revision: str,
    right_revision: str,
    merge_revision: str,
    relative_paths: Iterable[str],
    max_states: int = 4096,
) -> tuple[
    RepositorySnapshot,
    RepositoryMergeObservation,
    RepositoryMergeCertificate,
]:
    if not merge_id:
        raise ValueError("merge_id_missing")
    left_issues = certificate_chain_record_issues(left_record)
    if left_issues:
        raise ValueError(f"left_record_invalid:{left_issues[0]}")
    right_issues = certificate_chain_record_issues(right_record)
    if right_issues:
        raise ValueError(f"right_record_invalid:{right_issues[0]}")
    if chain_id != left_record.chain_id or chain_id != right_record.chain_id:
        raise ValueError("merge_chain_id_mismatch")
    if left_record.root_commit_sha != right_record.root_commit_sha:
        raise ValueError("merge_root_commit_mismatch")
    if not left_record.current_normal_form_preserved:
        raise ValueError("left_normal_form_not_preserved")
    if not right_record.current_normal_form_preserved:
        raise ValueError("right_normal_form_not_preserved")
    if left_record.current_commit_sha == right_record.current_commit_sha:
        raise ValueError("merge_parents_not_distinct")

    prefix = _common_prefix(left_record.commit_shas, right_record.commit_shas)
    if not prefix:
        raise ValueError("merge_common_prefix_missing")
    left_suffix = left_record.commit_shas[len(prefix):]
    right_suffix = right_record.commit_shas[len(prefix):]
    if not left_suffix or not right_suffix:
        raise ValueError("merge_branch_suffix_missing")
    suffix_disjoint = not (set(left_suffix) & set(right_suffix))
    if not suffix_disjoint:
        raise ValueError("merge_branch_history_overlap")

    left_snapshot, right_snapshot, merge_snapshot, observation = (
        observe_repository_merge_from_git(
            root,
            left_revision,
            right_revision,
            merge_revision,
            relative_paths,
        )
    )
    if observation.left_parent_sha != left_record.current_commit_sha:
        raise ValueError("left_record_commit_mismatch")
    if observation.right_parent_sha != right_record.current_commit_sha:
        raise ValueError("right_record_commit_mismatch")
    if left_snapshot.digest != left_record.current_snapshot_digest:
        raise ValueError("left_record_snapshot_mismatch")
    if right_snapshot.digest != right_record.current_snapshot_digest:
        raise ValueError("right_record_snapshot_mismatch")
    if observation.overlapping_changed_paths:
        raise ValueError(
            f"merge_changed_path_overlap:{observation.overlapping_changed_paths[0]}"
        )

    normal_form = certify_repository_alignment_normal_form(
        merge_snapshot,
        max_states=max_states,
    )
    preserved = _normal_form_bound(merge_snapshot, normal_form)
    certificate = RepositoryMergeCertificate(
        merge_id,
        chain_id,
        left_record.root_commit_sha,
        prefix[-1],
        left_record.record_digest,
        right_record.record_digest,
        observation.left_parent_sha,
        observation.right_parent_sha,
        observation.merge_commit_sha,
        observation.observation_digest,
        normal_form.certificate_digest,
        normal_form.initial_score,
        len(prefix),
        left_suffix,
        right_suffix,
        observation.merge_parent_shas
        == (observation.left_parent_sha, observation.right_parent_sha),
        suffix_disjoint,
        not observation.overlapping_changed_paths,
        preserved,
        False,
        "",
    )
    certificate = replace(
        certificate,
        certificate_digest=repository_merge_certificate_digest(certificate),
    )
    return merge_snapshot, observation, certificate
