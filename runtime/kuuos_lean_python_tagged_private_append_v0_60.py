"""v0.60: preserve/refute tagged overlap gluing across PRIVATE appends.

Two v0.58 tagged archives must be independently recomputable and have
identical common ancestors. Each later branch must retain every old row,
in its original order, then add zero or more COMPLETE LOCAL two-row pairs
(at least one pair overall). Prior observation VALUES, including each
private old observation, must be preserved exactly on both branches.

Under these explicit local premises, the ancestor mismatch indices and
compatibility status cannot change. The result is NOT authentication of
historical issuance or an externally held checkpoint, nor global descent,
single-linear gluing, or host-execution authority. All original OS kernels
and SQLite are untouched by this pure verification.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
import hmac
from typing import Any

from runtime import kuuos_lean_python_tagged_fork_archive_v0_58 as tagged
from runtime import kuuos_lean_python_tagged_span_gluing_v0_59 as tagged_glue
from runtime import kuuos_lean_python_detached_replay_witness_v0_54 as detached
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA,
)

VERSION = "kuuos_lean_python_tagged_private_append_v0_60"
PRESERVED_COMPATIBILITY = (
    "PRIVATE_APPEND_TAGGED_COMPATIBILITY_PRESERVED_PROPOSAL_ONLY"
)
PRESERVED_MISMATCH = (
    "PRIVATE_APPEND_TAGGED_SHARED_MISMATCH_PERSISTS_OBSTRUCTION"
)
PRESERVED_COMPATIBILITY_WITH_CHECKPOINT = (
    "PRIVATE_APPEND_COMPATIBLE_WITH_PRIOR_CHECKPOINT_VALUE_OBSTRUCTION"
)
PRESERVED_MULTIPLE_OBSTRUCTIONS = (
    "PRIVATE_APPEND_SHARED_AND_CHECKPOINT_OBSTRUCTIONS_PERSIST"
)
NO_NEW_PRIVATE_ROWS = "PRIVATE_APPEND_NO_NEW_COMPLETE_PAIR_OBSTRUCTION"
HISTORY_REWRITE = "PRIVATE_APPEND_OLD_HISTORY_REWRITE_OBSTRUCTION"
OBSERVATION_REWRITE = "PRIVATE_APPEND_OLD_OBSERVATION_REWRITE_OBSTRUCTION"
ANCESTOR_CHANGE = "PRIVATE_APPEND_ANCESTOR_CHANGE_OBSTRUCTION"
RELATION_CHANGE = "PRIVATE_APPEND_BRANCH_RELATION_CHANGE_OBSTRUCTION"

UNPROVED = (
    "LOCAL_APPEND_AND_LABEL_PRESERVATION_ARE_VERIFIED_NOT_AUTHENTICATED_ISSUANCE",
    "SET_LEVEL_TAGGED_COMPATIBILITY_IS_NOT_LINEAR_HISTORY_DESCENT",
    "CHECKPOINT_VALUE_HAS_NO_VERIFIED_EXTERNAL_INDEPENDENT_CUSTODY",
    "NO_CAUSAL_TIME_ISSUER_SIGNATURE_OR_GLOBAL_CROSS_HOST_REPLAY_PROOF",
    "NO_LEAN_SHA256_CPYTHON_JSON_SQLITE_REFINEMENT_OR_SECURITY_THEOREM",
    "ORIGINAL_PLANOS_THREE_RESULT_FINSETS_STILL_NO_DATA",
    "NO_GLOBAL_DESCENT_OR_HOST_EXECUTION_AUTHORITY",
)


@dataclass(frozen=True)
class PrivateAppendAudit:
    status: str
    issues: tuple[str, ...] = ()
    older_archive_sha256: str | None = None
    newer_archive_sha256: str | None = None
    old_shared_count: int = 0
    old_left_count: int = 0
    old_right_count: int = 0
    appended_left_rows: int = 0
    appended_right_rows: int = 0
    preserved_exact_ancestor: bool = False
    all_old_rows_and_annotations_preserved: bool = False
    old_overlap_compatible: bool = False
    new_overlap_compatible: bool = False
    mismatch_indices: tuple[int, ...] = ()
    overlap_status_invariant_verified: bool = False
    old_fork_obstruction_preserved: bool = False
    caller_old_archive_value_matches: bool = False
    newly_glued: dict[str, Any] | None = None
    independent_custody_authenticated: bool = False
    actual_historical_issuance_authenticated: bool = False
    original_plan_result_state: str = NO_DATA
    original_lean_python_refinement_proved: bool = False
    linear_history_descended: bool = False
    global_descent_certified: bool = False
    host_execution_authorized: bool = False
    selected_successor: None = None
    native_kernel_invocations: int = 0
    unresolved: tuple[str, ...] = UNPROVED


def audit_tagged_private_append(
    older_archive: Any, newer_archive: Any,
    older_left_values: Any, older_right_values: Any,
    newer_left_values: Any, newer_right_values: Any,
    *, separately_supplied_old_archive_sha256: Any = None,
) -> PrivateAppendAudit:
    """Check exact source/observation retention before making any gluing claim.

    The old and new ancestors must be identical canonical manifest objects;
    matching a checksum string alone is deliberately insufficient.
    """
    inputs = (
        older_archive, newer_archive, older_left_values, older_right_values,
        newer_left_values, newer_right_values,
    )
    if any(x is None for x in inputs):
        return PrivateAppendAudit(NO_DATA, ("both_archives_and_four_value_lists_required",))

    old = tagged.verify_local_tagged_fork_archive(
        older_archive,
        separately_supplied_archive_sha256=separately_supplied_old_archive_sha256,
    )
    new = tagged.verify_local_tagged_fork_archive(newer_archive)
    if old.archive is None or new.archive is None or old.status in (BLOCKED, NO_DATA) or new.status in (BLOCKED, NO_DATA):
        return PrivateAppendAudit(
            BLOCKED,
            ("old_or_new_tagged_archive_invalid",) + tuple(old.issues)
            + tuple(new.issues),
        )
    a, b = old.archive, new.archive
    if a["ancestor"] != b["ancestor"]:
        return PrivateAppendAudit(
            ANCESTOR_CHANGE, ("different_complete_ancestor_manifests",),
            older_archive_sha256=old.archive_sha256,
            newer_archive_sha256=new.archive_sha256,
        )
    if a["prior_checkpoint_sha256"] != b["prior_checkpoint_sha256"]:
        return PrivateAppendAudit(
            ANCESTOR_CHANGE, ("prior_checkpoint_value_was_replaced",),
            older_archive_sha256=old.archive_sha256,
            newer_archive_sha256=new.archive_sha256,
        )
    if a["declared_relation"] != b["declared_relation"]:
        return PrivateAppendAudit(
            RELATION_CHANGE, ("local_fork_vs_comparable_relation_changed",),
            older_archive_sha256=old.archive_sha256,
            newer_archive_sha256=new.archive_sha256,
            preserved_exact_ancestor=True,
        )

    old_rows = [a["branches"][i]["snapshot"]["entries"] for i in (0, 1)]
    new_rows = [b["branches"][i]["snapshot"]["entries"] for i in (0, 1)]
    old_length = tuple(map(len, old_rows))
    new_length = tuple(map(len, new_rows))
    if any(
        new_length[i] < old_length[i]
        or new_rows[i][:old_length[i]] != old_rows[i]
        for i in (0, 1)
    ):
        return PrivateAppendAudit(
            HISTORY_REWRITE, ("old_rows_not_exact_ordered_prefix_of_new_rows",),
            older_archive_sha256=old.archive_sha256,
            newer_archive_sha256=new.archive_sha256,
            preserved_exact_ancestor=True,
            old_fork_obstruction_preserved=old.fork_obstruction_preserved,
        )

    added_left = new_length[0] - old_length[0]
    added_right = new_length[1] - old_length[1]
    if added_left + added_right == 0:
        return PrivateAppendAudit(
            NO_NEW_PRIVATE_ROWS, ("at_least_one_new_complete_pair_required",),
            older_archive_sha256=old.archive_sha256,
            newer_archive_sha256=new.archive_sha256,
            preserved_exact_ancestor=True,
            old_fork_obstruction_preserved=old.fork_obstruction_preserved,
        )
    # Each v0.54 snapshot has been validated as an even-length pair sequence.
    if added_left % 2 or added_right % 2:
        return PrivateAppendAudit(
            BLOCKED, ("not_a_complete_append_pair",),
        )
    vecs = (
        older_left_values, older_right_values,
        newer_left_values, newer_right_values,
    )
    if any(not tagged_glue._valid_annotations(vecs[i], counts)
           for i, counts in enumerate(
               (old_length[0], old_length[1], new_length[0], new_length[1])
           )):
        return PrivateAppendAudit(
            BLOCKED, ("invalid_or_misaligned_position_observations",),
        )
    if (newer_left_values[:old_length[0]] != older_left_values
            or newer_right_values[:old_length[1]] != older_right_values):
        return PrivateAppendAudit(
            OBSERVATION_REWRITE, ("old_shared_or_private_observation_changed",),
            older_archive_sha256=old.archive_sha256,
            newer_archive_sha256=new.archive_sha256,
            preserved_exact_ancestor=True,
            appended_left_rows=added_left, appended_right_rows=added_right,
            old_fork_obstruction_preserved=old.fork_obstruction_preserved,
        )
    n = len(a["ancestor"]["entries"])
    old_bad = tuple(i for i in range(n)
                    if older_left_values[i] != older_right_values[i])
    new_bad = tuple(i for i in range(n)
                    if newer_left_values[i] != newer_right_values[i])
    if old_bad != new_bad:
        return PrivateAppendAudit(
            BLOCKED, ("shared_observation_invariance_failed",),
        )

    # Use the original v0.59 implementation for both old and new,
    # not an independent unproved substitute for its gluing algorithm.
    old_audit = tagged_glue.glue_tagged_observations(
        a, older_left_values, older_right_values,
    )
    new_audit = tagged_glue.glue_tagged_observations(
        b, newer_left_values, newer_right_values,
    )
    if (old_audit.status in (BLOCKED, NO_DATA)
            or new_audit.status in (BLOCKED, NO_DATA)
            or old_audit.common_observations_compatible != (not old_bad)
            or new_audit.common_observations_compatible != (not new_bad)
            or old_audit.tagged_gluing_constructed != (not old_bad)
            or new_audit.tagged_gluing_constructed != (not new_bad)):
        return PrivateAppendAudit(
            BLOCKED, ("v059_gluing_observation_crosscheck_failed",),
        )
    old_value_mismatch = (
        separately_supplied_old_archive_sha256 is not None
        and not old.caller_archive_digest_value_matches
    )
    checkpoint_obstruction = (
        old_value_mismatch or
        old.status in (tagged.ARCHIVED_FORK_AND_CHECKPOINT,
                       tagged.ARCHIVED_CHECKPOINT)
    )
    issues = tuple(
        "retained_shared_observation_mismatch:" + str(i) for i in old_bad
    )
    if old_value_mismatch:
        issues += ("caller_old_archive_digest_disagrees",)
    if old.status in (tagged.ARCHIVED_FORK_AND_CHECKPOINT,
                       tagged.ARCHIVED_CHECKPOINT):
        issues += tuple(old.issues)
    if old_bad:
        status = (PRESERVED_MULTIPLE_OBSTRUCTIONS if checkpoint_obstruction
                  else PRESERVED_MISMATCH)
    else:
        status = (PRESERVED_COMPATIBILITY_WITH_CHECKPOINT
                  if checkpoint_obstruction else PRESERVED_COMPATIBILITY)
    return PrivateAppendAudit(
        status=status,
        issues=issues,
        older_archive_sha256=old.archive_sha256,
        newer_archive_sha256=new.archive_sha256,
        old_shared_count=n,
        old_left_count=old_length[0],
        old_right_count=old_length[1],
        appended_left_rows=added_left,
        appended_right_rows=added_right,
        preserved_exact_ancestor=True,
        all_old_rows_and_annotations_preserved=True,
        old_overlap_compatible=not old_bad,
        new_overlap_compatible=not new_bad,
        mismatch_indices=old_bad,
        overlap_status_invariant_verified=True,
        old_fork_obstruction_preserved=old.fork_obstruction_preserved,
        caller_old_archive_value_matches=
            old.caller_archive_digest_value_matches,
        newly_glued=new_audit.glued if not old_bad else None,
    )


__all__ = (
    "VERSION", "PRESERVED_COMPATIBILITY", "PRESERVED_MISMATCH",
    "PRESERVED_COMPATIBILITY_WITH_CHECKPOINT",
    "PRESERVED_MULTIPLE_OBSTRUCTIONS", "NO_NEW_PRIVATE_ROWS",
    "HISTORY_REWRITE", "OBSERVATION_REWRITE", "ANCESTOR_CHANGE",
    "RELATION_CHANGE", "PrivateAppendAudit", "audit_tagged_private_append",
)
