"""v0.61 candidate: observational two-stage tagged private append adapter.

This is a PURE CPython composition of the original v0.60 private-append
auditor and v0.59 tagged-gluing reconstruction. The Lean v0.61 candidate has
its own separate fixed-Lean evidence; this file is NOT a Lean↔Python
refinement theorem, an authenticated historical issuance, or a permission
to choose a branch, act on the host, or publish a formal Lean module.

Both intermediate archive values and BOTH intermediate observation maps
must match exactly. A matching digest is not substituted for equal source
values. Native v0.60 verifies both individual stages and the direct
old-to-final stage, including every old private observation and row.
No failures are promoted to a successful gluing result.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime import kuuos_lean_python_tagged_private_append_v0_60 as native
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA,
)

VERSION = "kuuos_lean_python_two_stage_private_append_v0_61"
COMPATIBLE = "TWO_STAGE_TAGGED_COMPATIBILITY_PRESERVED_PROPOSAL_ONLY"
SHARED_MISMATCH = "TWO_STAGE_TAGGED_SHARED_MISMATCH_PERSISTS_OBSTRUCTION"
CHECKPOINT_OBSTRUCTION = "TWO_STAGE_TAGGED_CHECKPOINT_VALUE_OBSTRUCTION"
MULTIPLE_OBSTRUCTIONS = "TWO_STAGE_TAGGED_SHARED_AND_CHECKPOINT_OBSTRUCTIONS"
_VALID_NATIVE = (
    native.PRESERVED_COMPATIBILITY,
    native.PRESERVED_MISMATCH,
    native.PRESERVED_COMPATIBILITY_WITH_CHECKPOINT,
    native.PRESERVED_MULTIPLE_OBSTRUCTIONS,
)


@dataclass(frozen=True)
class TwoStagePrivateAppendAudit:
    status: str
    issues: tuple[str, ...] = ()
    first_stage: native.PrivateAppendAudit | None = None
    second_stage: native.PrivateAppendAudit | None = None
    original_to_final: native.PrivateAppendAudit | None = None
    exact_intermediate_archive_values: bool = False
    exact_intermediate_observation_values: bool = False
    both_native_stages_verified: bool = False
    direct_original_to_final_verified: bool = False
    sequential_append_counts_equal_direct: bool = False
    complete_history_concat_equal_final: bool = False
    original_final_compatibility_equivalence_observed: bool = False
    mismatch_indices: tuple[int, ...] = ()
    shared_obstruction_persists: bool = False
    checkpoint_value_obstruction_retained: bool = False
    old_private_observations_retained: bool = False
    original_branch_fork_obstruction_retained: bool = False
    original_lean_python_refinement_proved: bool = False
    source_history_issuer_authenticated: bool = False
    independent_checkpoint_custody_authenticated: bool = False
    linear_history_descended: bool = False
    global_descent_certified: bool = False
    host_execution_authorized: bool = False
    git_authority_granted: bool = False
    selected_successor: None = None


def _native_stage_valid(value: native.PrivateAppendAudit) -> bool:
    return (
        value.status in _VALID_NATIVE
        and value.preserved_exact_ancestor
        and value.all_old_rows_and_annotations_preserved
        and value.overlap_status_invariant_verified
        and value.old_fork_obstruction_preserved
        and value.old_overlap_compatible == value.new_overlap_compatible
    )


def audit_two_stage_private_append(
    *,
    original_archive: Any,
    first_new_archive: Any,
    second_old_archive: Any,
    final_archive: Any,
    original_left_values: Any,
    original_right_values: Any,
    first_new_left_values: Any,
    first_new_right_values: Any,
    second_old_left_values: Any,
    second_old_right_values: Any,
    final_left_values: Any,
    final_right_values: Any,
    separately_supplied_original_archive_sha256: Any = None,
) -> TwoStagePrivateAppendAudit:
    """Read-only observation of two genuine v0.60 append records.

    Intermediate correspondence is a prerequisite, not an inferred match.
    For failed native checks retain their evidence and do not admit a final
    compatibility claim. The input maps are NOT mutated or merged.
    """
    inputs = (
        original_archive, first_new_archive, second_old_archive, final_archive,
        original_left_values, original_right_values,
        first_new_left_values, first_new_right_values,
        second_old_left_values, second_old_right_values,
        final_left_values, final_right_values,
    )
    if any(x is None for x in inputs):
        return TwoStagePrivateAppendAudit(
            NO_DATA, ("three_archives_and_all_intermediate_observations_required",),
        )
    if first_new_archive != second_old_archive:
        return TwoStagePrivateAppendAudit(
            BLOCKED, ("intermediate_complete_archive_values_mismatch",),
        )
    if (
        first_new_left_values != second_old_left_values
        or first_new_right_values != second_old_right_values
    ):
        return TwoStagePrivateAppendAudit(
            BLOCKED, ("intermediate_left_or_right_observation_map_mismatch",),
            exact_intermediate_archive_values=True,
        )

    first = native.audit_tagged_private_append(
        original_archive, first_new_archive,
        original_left_values, original_right_values,
        first_new_left_values, first_new_right_values,
        separately_supplied_old_archive_sha256=separately_supplied_original_archive_sha256,
    )
    second = native.audit_tagged_private_append(
        second_old_archive, final_archive,
        second_old_left_values, second_old_right_values,
        final_left_values, final_right_values,
    )
    direct = native.audit_tagged_private_append(
        original_archive, final_archive,
        original_left_values, original_right_values,
        final_left_values, final_right_values,
        separately_supplied_old_archive_sha256=separately_supplied_original_archive_sha256,
    )
    common = {
        "first_stage": first, "second_stage": second,
        "original_to_final": direct,
        "exact_intermediate_archive_values": True,
        "exact_intermediate_observation_values": True,
    }
    if not all(_native_stage_valid(x) for x in (first, second, direct)):
        return TwoStagePrivateAppendAudit(
            BLOCKED, (
                "one_or_more_original_v060_append_audits_not_admissible",
                first.status, second.status, direct.status,
            ),
            **common,
        )

    same_shared = (
        first.old_shared_count == second.old_shared_count == direct.old_shared_count
        and first.mismatch_indices == second.mismatch_indices == direct.mismatch_indices
        and first.old_overlap_compatible == second.old_overlap_compatible
        == direct.old_overlap_compatible
        and first.new_overlap_compatible == second.new_overlap_compatible
        == direct.new_overlap_compatible
    )
    same_counts = (
        first.appended_left_rows + second.appended_left_rows
        == direct.appended_left_rows
        and first.appended_right_rows + second.appended_right_rows
        == direct.appended_right_rows
    )

    # Inputs are already independently validated by the three original v0.60
    # auditors; comparing actual full entry rows is stronger than equating
    # checkpoint or archive digest strings.
    histories_equal = True
    for branch_index in (0, 1):
        old = original_archive["branches"][branch_index]["snapshot"]["entries"]
        middle = first_new_archive["branches"][branch_index]["snapshot"]["entries"]
        final = final_archive["branches"][branch_index]["snapshot"]["entries"]
        if old + middle[len(old):] + final[len(middle):] != final:
            histories_equal = False
    if not (same_shared and same_counts and histories_equal):
        return TwoStagePrivateAppendAudit(
            BLOCKED, ("original_to_final_native_composition_mismatch",),
            **common,
        )

    old_mismatch = bool(direct.mismatch_indices)
    checkpoint = any(
        x.status in (
            native.PRESERVED_COMPATIBILITY_WITH_CHECKPOINT,
            native.PRESERVED_MULTIPLE_OBSTRUCTIONS,
        )
        for x in (first, second, direct)
    )
    status = (
        MULTIPLE_OBSTRUCTIONS if old_mismatch and checkpoint
        else SHARED_MISMATCH if old_mismatch
        else CHECKPOINT_OBSTRUCTION if checkpoint
        else COMPATIBLE
    )
    return TwoStagePrivateAppendAudit(
        status=status,
        issues=tuple(dict.fromkeys(first.issues + second.issues + direct.issues)),
        both_native_stages_verified=True,
        direct_original_to_final_verified=True,
        sequential_append_counts_equal_direct=True,
        complete_history_concat_equal_final=True,
        original_final_compatibility_equivalence_observed=True,
        mismatch_indices=direct.mismatch_indices,
        shared_obstruction_persists=old_mismatch,
        checkpoint_value_obstruction_retained=checkpoint,
        old_private_observations_retained=True,
        original_branch_fork_obstruction_retained=True,
        **common,
    )


__all__ = (
    "VERSION", "COMPATIBLE", "SHARED_MISMATCH", "CHECKPOINT_OBSTRUCTION",
    "MULTIPLE_OBSTRUCTIONS", "TwoStagePrivateAppendAudit",
    "audit_two_stage_private_append",
)
