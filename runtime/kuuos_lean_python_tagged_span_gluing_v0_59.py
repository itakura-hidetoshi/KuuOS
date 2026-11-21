"""v0.59: conditionally glue branch-local observations onto TAGGED slots.

This is a SET-LEVEL, position-preserving amalgam of two local observation
functions that agree at all shared ancestor indices. Branch-only slots stay
separate, even with coincident text values or identical ticket payloads.
It is NOT a single append-only chronology, verified external issuer record,
Lean↔CPython refinement theorem, or permission to execute any host action.

The input v0.58 archive must be independently recomputable using the
existing exact chain verifier. No new SQLite or original PlanOS is invoked.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any

from runtime import kuuos_lean_python_tagged_fork_archive_v0_58 as tagged
from runtime import kuuos_lean_python_detached_replay_witness_v0_54 as detached
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA,
)

VERSION = "kuuos_lean_python_tagged_span_gluing_v0_59"
SCHEMA = "kuuos.planos.tagged-observation-gluing.v0.59"
LOCAL_GLUED = "TAGGED_BRANCH_OBSERVATIONS_COMPATIBLE_PROPOSAL_ONLY"
OVERLAP_OBSTRUCTION = "TAGGED_SHARED_OBSERVATION_MISMATCH_OBSTRUCTION"
CHECKPOINT_OBSTRUCTION = "TAGGED_OBSERVATIONS_WITH_CHECKPOINT_VALUE_OBSTRUCTION"
COMPOSITE_OBSTRUCTION = "TAGGED_SHARED_AND_CHECKPOINT_MULTIPLE_OBSTRUCTIONS"
MAX_OBSERVATION_UTF8_BYTES = 1024
MAX_GLUING_BYTES = 48 * 1024 * 1024
UNPROVED = (
    "SET_LEVEL_TAGGED_GLUE_IS_NOT_SINGLE_LINEAR_HISTORY_DESCENT",
    "MATCHING_OBSERVATIONS_DO_NOT_AUTHENTICATE_PRIOR_ARCHIVE_CUSTODY",
    "NO_REAL_WORLD_ISSUER_OR_INDEPENDENT_CAUSAL_TIME_PROOF",
    "NO_CROSS_HOST_REPLAY_OR_CRYPTOGRAPHIC_SECURITY_PROOF_IN_LEAN",
    "NO_FORMAL_LEAN_TO_CPYTHON_JSON_SQLITE_REFINEMENT",
    "ORIGINAL_PLANOS_THREE_RESULT_FINSETS_STILL_NO_DATA",
    "NO_GLOBAL_DESCENT_OR_HOST_EXECUTION_AUTHORITY",
)


@dataclass(frozen=True)
class TaggedObservationGluingAudit:
    status: str
    issues: tuple[str, ...] = ()
    glued: dict[str, Any] | None = None
    glued_sha256: str | None = None
    archive_sha256: str | None = None
    shared_count: int = 0
    left_only_count: int = 0
    right_only_count: int = 0
    shared_value_agreement_checked: bool = False
    common_observations_compatible: bool = False
    tagged_gluing_constructed: bool = False
    branch_projections_preserved: bool = False
    fork_obstruction_preserved: bool = False
    archive_custody_authenticated: bool = False
    original_plan_result_state: str = NO_DATA
    linear_history_descended: bool = False
    universal_lean_python_refinement_proved: bool = False
    global_descent_certified: bool = False
    host_execution_authorized: bool = False
    selected_successor: None = None
    native_kernel_invocations: int = 0
    unresolved: tuple[str, ...] = UNPROVED


def _valid_annotations(value: Any, required: int) -> bool:
    if type(value) is not list or len(value) != required:
        return False
    for item in value:
        if type(item) is not str or not item:
            return False
        try:
            size = len(item.encode("utf-8", errors="strict"))
        except UnicodeError:
            return False
        if size > MAX_OBSERVATION_UTF8_BYTES:
            return False
    return True


def glue_tagged_observations(
    archive: Any, left_observations: Any, right_observations: Any,
    *, separately_supplied_archive_sha256: Any = None,
) -> TaggedObservationGluingAudit:
    """Glue only the two local VALUE functions on tagged positional slots.

    Equal shared ancestor values are the necessary/sufficient condition for
    this tagged construction. All branch-only indices remain distinct.
    """
    if archive is None or left_observations is None or right_observations is None:
        return TaggedObservationGluingAudit(
            NO_DATA, ("archive_and_both_branch_observations_required",),
        )

    verified = tagged.verify_local_tagged_fork_archive(
        archive,
        separately_supplied_archive_sha256=separately_supplied_archive_sha256,
    )
    if verified.status in (BLOCKED, NO_DATA) or verified.archive is None:
        return TaggedObservationGluingAudit(
            BLOCKED,
            ("tagged_archive_unverified:" + verified.status,) +
            tuple(verified.issues),
        )

    actual = verified.archive
    left = actual["branches"][0]["snapshot"]
    right = actual["branches"][1]["snapshot"]
    common = actual["ancestor"]["entries"]
    left_rows = left["entries"]
    right_rows = right["entries"]
    n = len(common)
    if (not _valid_annotations(left_observations, len(left_rows))
            or not _valid_annotations(right_observations, len(right_rows))):
        return TaggedObservationGluingAudit(
            BLOCKED, ("invalid_or_misaligned_branch_observations",),
            archive_sha256=verified.archive_sha256,
        )

    # Copy user values; no mutation, no raw secrets from the source manifests.
    left_values = list(left_observations)
    right_values = list(right_observations)
    mismatch_positions = [
        i for i in range(n) if left_values[i] != right_values[i]
    ]
    inherited_checkpoint_issue = (
        verified.status in (
            tagged.ARCHIVED_FORK_AND_CHECKPOINT,
            tagged.ARCHIVED_CHECKPOINT,
            tagged.ARCHIVE_DIGEST_MISMATCH,
        )
    )
    issues = list(verified.issues)
    if mismatch_positions:
        issues.extend(
            "shared_observation_disagreement:" + str(i)
            for i in mismatch_positions
        )
    if inherited_checkpoint_issue and not issues:
        issues.append("caller_checkpoint_value_disagrees")

    counts = dict(
        archive_sha256=verified.archive_sha256,
        shared_count=n,
        left_only_count=len(left_rows)-n,
        right_only_count=len(right_rows)-n,
        shared_value_agreement_checked=True,
        common_observations_compatible=not mismatch_positions,
        fork_obstruction_preserved=verified.fork_obstruction_preserved,
    )
    if mismatch_positions:
        return TaggedObservationGluingAudit(
            COMPOSITE_OBSTRUCTION if inherited_checkpoint_issue
            else OVERLAP_OBSTRUCTION,
            issues=tuple(issues),
            **counts,
        )

    positions = []
    for i, row in enumerate(common):
        positions.append(dict(
            id=f"common:{i:06d}", value=left_values[i],
            row_sha256=row["row_sha256"],
        ))
    for i, row in enumerate(left_rows[n:]):
        positions.append(dict(
            id=f"left:{i:06d}", value=left_values[n+i],
            row_sha256=row["row_sha256"],
        ))
    for i, row in enumerate(right_rows[n:]):
        positions.append(dict(
            id=f"right:{i:06d}", value=right_values[n+i],
            row_sha256=row["row_sha256"],
        ))
    payload = dict(
        schema=SCHEMA,
        source_boundary=tagged.VERSION,
        source_archive_sha256=verified.archive_sha256,
        ancestor_length=n,
        left_length=len(left_rows),
        right_length=len(right_rows),
        positions=positions,
    )
    try:
        raw = detached._canonical(payload)
        if len(raw) > MAX_GLUING_BYTES:
            return TaggedObservationGluingAudit(
                BLOCKED, ("tagged_gluing_byte_limit",), **counts,
            )
        digest = hashlib.sha256(raw).hexdigest()
    except (TypeError, ValueError, OverflowError, RecursionError, UnicodeError):
        return TaggedObservationGluingAudit(
            BLOCKED, ("tagged_gluing_encoding_failure",), **counts,
        )

    # The reconstruction is the computational analogue of exact projections
    # on finite positions. It is NOT a formal Lean↔Python refinement proof.
    left_recovered = [x["value"] for x in positions[:n]] + [
        x["value"] for x in positions[n:n+len(left_rows)-n]
    ]
    right_recovered = [x["value"] for x in positions[:n]] + [
        x["value"] for x in positions[n+len(left_rows)-n:]
    ]
    projections_match = left_recovered == left_values and right_recovered == right_values
    if not projections_match:
        return TaggedObservationGluingAudit(
            BLOCKED, ("branch_projection_recovery_failed",), **counts,
        )

    return TaggedObservationGluingAudit(
        CHECKPOINT_OBSTRUCTION if inherited_checkpoint_issue else LOCAL_GLUED,
        issues=tuple(issues),
        glued=payload, glued_sha256=digest,
        tagged_gluing_constructed=True,
        branch_projections_preserved=True,
        **counts,
    )


__all__ = (
    "VERSION", "SCHEMA", "LOCAL_GLUED", "OVERLAP_OBSTRUCTION",
    "CHECKPOINT_OBSTRUCTION", "COMPOSITE_OBSTRUCTION",
    "TaggedObservationGluingAudit", "glue_tagged_observations",
)
