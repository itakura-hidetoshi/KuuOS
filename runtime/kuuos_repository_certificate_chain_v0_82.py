#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import string

from runtime.kuuos_repository_alignment_normal_form_types_v0_80 import (
    AlignmentNormalFormCertificate,
)
from runtime.kuuos_repository_alignment_normal_form_v0_80 import (
    certify_repository_alignment_normal_form,
)
from runtime.kuuos_repository_alignment_scopes_v0_81 import (
    GLOBAL_SCOPE_ID,
    compare_alignment_scope_indexes,
    scope_snapshot,
)
from runtime.kuuos_repository_certificate_chain_types_v0_82 import (
    RepositoryCertificateChainRecord,
    certificate_chain_record_digest,
)
from runtime.kuuos_repository_structure_observer_v0_79 import (
    observe_repository_structure,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot

_HEX = frozenset(string.hexdigits.lower())


def _valid_commit_sha(value: str) -> bool:
    return (
        len(value) in {40, 64}
        and value == value.lower()
        and all(character in _HEX for character in value)
    )


def _normal_form_bound(
    snapshot: RepositorySnapshot,
    certificate: AlignmentNormalFormCertificate,
) -> bool:
    return (
        certificate.initial_snapshot_digest == snapshot.digest
        and certificate.initial_score == 0
        and certificate.all_transitions_strictly_decreasing
        and certificate.all_terminals_fixed_points
        and certificate.unique_terminal
        and certificate.unique_terminal_digest == snapshot.digest
        and certificate.deterministic_trace_matches_terminal
    )


def certificate_chain_record_issues(
    record: RepositoryCertificateChainRecord,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not record.chain_id:
        issues.append("chain_id_missing")
    if record.record_digest != certificate_chain_record_digest(record):
        issues.append("record_digest_mismatch")
    if record.sequence < 0:
        issues.append("sequence_invalid")
    if record.max_chain_length <= 0:
        issues.append("max_chain_length_invalid")
    if len(record.commit_shas) > record.max_chain_length:
        issues.append("chain_length_exceeded")
    if record.sequence != len(record.commit_shas) - 1:
        issues.append("sequence_commit_count_mismatch")
    if not record.commit_shas:
        issues.append("commit_chain_empty")
    else:
        if record.root_commit_sha != record.commit_shas[0]:
            issues.append("root_commit_mismatch")
        if record.current_commit_sha != record.commit_shas[-1]:
            issues.append("current_commit_mismatch")
    if len(set(record.commit_shas)) != len(record.commit_shas):
        issues.append("commit_replay_detected")
    if any(not _valid_commit_sha(value) for value in record.commit_shas):
        issues.append("commit_sha_invalid")
    if record.sequence == 0:
        if record.parent_commit_sha:
            issues.append("genesis_parent_present")
        if record.previous_record_digest:
            issues.append("genesis_previous_record_present")
        if record.previous_snapshot_digest != record.current_snapshot_digest:
            issues.append("genesis_snapshot_mismatch")
    elif len(record.commit_shas) >= 2:
        if record.parent_commit_sha != record.commit_shas[-2]:
            issues.append("parent_commit_mismatch")
        if not record.previous_record_digest:
            issues.append("previous_record_digest_missing")
    if tuple(sorted(set(record.declared_changed_paths))) != record.declared_changed_paths:
        issues.append("declared_changed_paths_not_canonical")
    if tuple(sorted(set(record.computed_changed_paths))) != record.computed_changed_paths:
        issues.append("computed_changed_paths_not_canonical")
    if record.declared_changed_paths != record.computed_changed_paths:
        issues.append("changed_paths_mismatch")
    if record.external_approval_required:
        issues.append("unexpected_external_approval")
    return tuple(issues)


def start_repository_certificate_chain(
    chain_id: str,
    commit_sha: str,
    snapshot: RepositorySnapshot,
    normal_form_certificate: AlignmentNormalFormCertificate,
    max_chain_length: int = 1024,
) -> RepositoryCertificateChainRecord:
    if not chain_id:
        raise ValueError("chain_id_missing")
    if not _valid_commit_sha(commit_sha):
        raise ValueError("commit_sha_invalid")
    if max_chain_length <= 0:
        raise ValueError("max_chain_length_invalid")
    if not _normal_form_bound(snapshot, normal_form_certificate):
        raise ValueError("genesis_normal_form_certificate_invalid")

    record = RepositoryCertificateChainRecord(
        chain_id,
        0,
        commit_sha,
        "",
        commit_sha,
        "",
        snapshot.digest,
        snapshot.digest,
        (),
        (),
        "",
        (),
        (),
        (normal_form_certificate.certificate_digest,),
        True,
        normal_form_certificate.initial_score,
        True,
        (commit_sha,),
        max_chain_length,
        False,
        "",
    )
    return replace(
        record,
        record_digest=certificate_chain_record_digest(record),
    )


def advance_repository_certificate_chain(
    chain_id: str,
    previous_record: RepositoryCertificateChainRecord,
    previous_snapshot: RepositorySnapshot,
    current_snapshot: RepositorySnapshot,
    parent_commit_sha: str,
    current_commit_sha: str,
    declared_changed_paths: tuple[str, ...],
    max_states: int = 4096,
) -> RepositoryCertificateChainRecord:
    previous_issues = certificate_chain_record_issues(previous_record)
    if previous_issues:
        raise ValueError(f"previous_record_invalid:{previous_issues[0]}")
    if chain_id != previous_record.chain_id:
        raise ValueError("chain_id_binding_mismatch")
    if not previous_record.current_normal_form_preserved:
        raise ValueError("previous_normal_form_not_preserved")
    if previous_record.current_snapshot_digest != previous_snapshot.digest:
        raise ValueError("previous_snapshot_binding_mismatch")
    if parent_commit_sha != previous_record.current_commit_sha:
        raise ValueError("parent_commit_binding_mismatch")
    if not _valid_commit_sha(current_commit_sha):
        raise ValueError("current_commit_sha_invalid")
    if current_commit_sha in set(previous_record.commit_shas):
        raise ValueError("commit_replay_detected")
    if len(previous_record.commit_shas) >= previous_record.max_chain_length:
        raise ValueError("chain_length_exceeded")

    canonical_declared = tuple(sorted(set(declared_changed_paths)))
    if canonical_declared != declared_changed_paths:
        raise ValueError("declared_changed_paths_not_canonical")

    previous_index, current_index, delta = compare_alignment_scope_indexes(
        previous_snapshot,
        current_snapshot,
    )
    if canonical_declared != delta.changed_paths:
        raise ValueError("declared_changed_paths_mismatch")

    previous_scopes = {scope.scope_id: scope for scope in previous_index.scopes}
    current_scopes = {scope.scope_id: scope for scope in current_index.scopes}
    reused_equal = all(
        previous_scopes[scope_id].scope_digest
        == current_scopes[scope_id].scope_digest
        for scope_id in delta.reused_scope_ids
    )
    current_score = observe_repository_structure(
        current_snapshot
    ).weighted_defect_score

    if delta.full_recheck_required:
        full_certificate = certify_repository_alignment_normal_form(
            current_snapshot,
            max_states=max_states,
        )
        rechecked_scope_ids = tuple(scope.scope_id for scope in current_index.scopes)
        rechecked_digests = (full_certificate.certificate_digest,)
        preserved = _normal_form_bound(current_snapshot, full_certificate)
        full_recheck = True
    else:
        local_certificates: list[AlignmentNormalFormCertificate] = []
        local_scope_ids: list[str] = []
        for scope_id in delta.invalidated_scope_ids:
            if scope_id == GLOBAL_SCOPE_ID:
                raise ValueError("global_scope_requires_full_recheck")
            local_snapshot = scope_snapshot(
                current_snapshot,
                current_scopes[scope_id],
            )
            local_certificate = certify_repository_alignment_normal_form(
                local_snapshot,
                max_states=max_states,
            )
            local_scope_ids.append(scope_id)
            local_certificates.append(local_certificate)
        rechecked_scope_ids = tuple(local_scope_ids)
        rechecked_digests = tuple(
            certificate.certificate_digest
            for certificate in local_certificates
        )
        local_zero = all(
            _normal_form_bound(
                scope_snapshot(current_snapshot, current_scopes[scope_id]),
                certificate,
            )
            for scope_id, certificate in zip(
                rechecked_scope_ids,
                local_certificates,
                strict=True,
            )
        )
        preserved = bool(
            reused_equal
            and local_zero
            and current_score == 0
            and not delta.added_scope_ids
            and not delta.removed_scope_ids
        )
        full_recheck = False

    record = RepositoryCertificateChainRecord(
        previous_record.chain_id,
        previous_record.sequence + 1,
        previous_record.root_commit_sha,
        parent_commit_sha,
        current_commit_sha,
        previous_record.record_digest,
        previous_snapshot.digest,
        current_snapshot.digest,
        canonical_declared,
        delta.changed_paths,
        delta.delta_digest,
        delta.reused_scope_ids,
        rechecked_scope_ids,
        rechecked_digests,
        full_recheck,
        current_score,
        preserved,
        previous_record.commit_shas + (current_commit_sha,),
        previous_record.max_chain_length,
        False,
        "",
    )
    return replace(
        record,
        record_digest=certificate_chain_record_digest(record),
    )
