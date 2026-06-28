#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_alignment_normal_form_types_v0_80 import (
    AlignmentNormalFormCertificate,
)
from runtime.kuuos_repository_alignment_normal_form_v0_80 import (
    certify_repository_alignment_normal_form,
)
from runtime.kuuos_repository_alignment_scopes_v0_81 import (
    compare_alignment_scope_indexes,
    scope_snapshot,
)
from runtime.kuuos_repository_incremental_preservation_types_v0_81 import (
    GLOBAL_SCOPE_ID,
    IncrementalPreservationCertificate,
    incremental_preservation_certificate_digest,
)
from runtime.kuuos_repository_structure_observer_v0_79 import (
    observe_repository_structure,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot


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


def _certificate_at_current_zero(
    snapshot: RepositorySnapshot,
    certificate: AlignmentNormalFormCertificate,
) -> bool:
    return (
        certificate.initial_snapshot_digest == snapshot.digest
        and certificate.initial_score == 0
        and certificate.unique_terminal
        and certificate.unique_terminal_digest == snapshot.digest
        and certificate.all_terminals_fixed_points
        and certificate.deterministic_trace_matches_terminal
    )


def preserve_repository_normal_form_incrementally(
    previous_snapshot: RepositorySnapshot,
    current_snapshot: RepositorySnapshot,
    previous_certificate: AlignmentNormalFormCertificate,
    max_states: int = 4096,
) -> IncrementalPreservationCertificate:
    previous_bound = _normal_form_bound(previous_snapshot, previous_certificate)
    if not previous_bound:
        raise ValueError("previous_normal_form_certificate_invalid")

    previous_index, current_index, delta = compare_alignment_scope_indexes(
        previous_snapshot,
        current_snapshot,
    )
    previous_scopes = {scope.scope_id: scope for scope in previous_index.scopes}
    current_scopes = {scope.scope_id: scope for scope in current_index.scopes}
    reused_equal = all(
        previous_scopes[scope_id].scope_digest
        == current_scopes[scope_id].scope_digest
        for scope_id in delta.reused_scope_ids
    )

    rechecked_scope_ids: tuple[str, ...]
    rechecked_digests: tuple[str, ...]
    full_recheck_performed = delta.full_recheck_required
    full_certificate_digest = ""

    if full_recheck_performed:
        full_certificate = certify_repository_alignment_normal_form(
            current_snapshot,
            max_states=max_states,
        )
        rechecked_scope_ids = tuple(scope.scope_id for scope in current_index.scopes)
        rechecked_digests = (full_certificate.certificate_digest,)
        full_certificate_digest = full_certificate.certificate_digest
        all_rechecked_zero = _certificate_at_current_zero(
            current_snapshot,
            full_certificate,
        )
    else:
        local_certificates: list[AlignmentNormalFormCertificate] = []
        local_scope_ids: list[str] = []
        for scope_id in delta.invalidated_scope_ids:
            if scope_id == GLOBAL_SCOPE_ID:
                raise ValueError("global_scope_requires_full_recheck")
            scope = current_scopes[scope_id]
            local_snapshot = scope_snapshot(current_snapshot, scope)
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
        all_rechecked_zero = all(
            _certificate_at_current_zero(
                scope_snapshot(current_snapshot, current_scopes[scope_id]),
                certificate,
            )
            for scope_id, certificate in zip(
                rechecked_scope_ids,
                local_certificates,
                strict=True,
            )
        )

    current_score = observe_repository_structure(
        current_snapshot
    ).weighted_defect_score
    current_preserved = bool(
        previous_bound
        and reused_equal
        and all_rechecked_zero
        and current_score == 0
        and not delta.added_scope_ids
        and not delta.removed_scope_ids
    )
    if full_recheck_performed:
        current_preserved = bool(all_rechecked_zero and current_score == 0)

    certificate = IncrementalPreservationCertificate(
        previous_snapshot.digest,
        current_snapshot.digest,
        previous_certificate.certificate_digest,
        previous_certificate.initial_score,
        current_score,
        delta.delta_digest,
        delta.reused_scope_ids,
        rechecked_scope_ids,
        rechecked_digests,
        full_recheck_performed,
        full_certificate_digest,
        previous_bound,
        reused_equal,
        all_rechecked_zero,
        current_preserved,
        False,
        "",
    )
    return replace(
        certificate,
        certificate_digest=incremental_preservation_certificate_digest(
            certificate
        ),
    )
