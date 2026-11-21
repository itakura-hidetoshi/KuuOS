"""v0.58: a detached, fork-preserving, explicitly tagged LOCAL archive.

v0.57 proves two incomparable histories have no common exact-prefix future
within one linear List. This module retains an ancestor and BOTH independently
checked successor manifests in a richer tagged representation. It never
collapses the branches to one asserted history or chooses a preferred truth.

The archive is locally recomputable, not signed or independently custodial;
this code does not read SQLite, use a network, re-run original OS kernels,
authenticate issuers, or grant PlanOS execution permission.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import hmac
import json
from typing import Any

from runtime import kuuos_lean_python_common_ancestor_fork_v0_56 as fork
from runtime import kuuos_lean_python_detached_replay_witness_v0_54 as detached
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA,
)

VERSION = "kuuos_lean_python_tagged_fork_archive_v0_58"
SCHEMA = "kuuos.planos.tagged-local-branch-archive.v0.58"
ARCHIVED_FORK = "LOCAL_TAGGED_FORK_BOTH_BRANCHES_PRESERVED_PROPOSAL_ONLY"
ARCHIVED_FORK_AND_CHECKPOINT = (
    "LOCAL_TAGGED_FORK_AND_PRIOR_CHECKPOINT_OBSTRUCTIONS"
)
ARCHIVED_COMPARABLE = "LOCAL_TAGGED_COMPARABLE_BRANCHES_PRESERVED_PROPOSAL_ONLY"
ARCHIVED_CHECKPOINT = "LOCAL_TAGGED_PRIOR_CHECKPOINT_VALUE_OBSTRUCTION"
ANCESTOR_OBSTRUCTION = "LOCAL_TAGGED_ARCHIVE_COMMON_ANCESTOR_OBSTRUCTION"
ARCHIVE_DIGEST_MISMATCH = "LOCAL_TAGGED_ARCHIVE_DIGEST_MISMATCH_OBSTRUCTION"
MAX_ARCHIVE_BYTES = 48 * 1024 * 1024
FIELDS = frozenset((
    "schema", "source_boundary", "ancestor", "branches",
    "declared_relation", "prior_checkpoint_sha256",
))
UNPROVED = (
    "FORK_ARCHIVE_REPRESENTATION_IS_NOT_SINGLE_LINEAR_HISTORY_GLUING",
    "LOCAL_TAGGED_PROJECTIONS_ARE_NOT_AUTHENTICATED_EXTERNAL_EVENTS",
    "NO_REAL_CAUSAL_TIME_CHECKPOINT_KEEPER_OR_ISSUER_AUTHENTICATION",
    "NO_GLOBAL_CROSS_HOST_REPLAY_OR_SHA256_SECURITY_THEOREM_IN_LEAN",
    "NO_SQLITE_JSON_CPYTHON_REFINEMENT_OR_ORIGINAL_PLANOS_OUTPUT_PROOF",
    "NO_GLOBAL_DESCENT_OR_HOST_EXECUTION_AUTHORITY",
)


@dataclass(frozen=True)
class TaggedForkArchiveAudit:
    status: str
    issues: tuple[str, ...] = ()
    archive: dict[str, Any] | None = None
    archive_sha256: str | None = None
    ancestor_sha256: str | None = None
    left_sha256: str | None = None
    right_sha256: str | None = None
    independently_recomputed_snapshots: bool = False
    both_branches_locally_retained: bool = False
    fork_obstruction_preserved: bool = False
    caller_prior_checkpoint_value_matches: bool = False
    caller_archive_digest_value_matches: bool = False
    independent_archive_custody_authenticated: bool = False
    historical_branch_issuers_authenticated: bool = False
    original_plan_result_state: str = NO_DATA
    global_descent_certified: bool = False
    host_execution_authorized: bool = False
    selected_successor: None = None
    native_kernel_invocations: int = 0
    unresolved: tuple[str, ...] = UNPROVED


def _copy(value: Any) -> dict[str, Any] | None:
    if type(value) is not dict:
        return None
    try:
        raw = detached._canonical(value)
        if len(raw) > MAX_ARCHIVE_BYTES:
            return None
        copied = json.loads(raw)
        if raw != detached._canonical(value):
            return None
        if type(copied) is not dict:
            return None
        return copied
    except (TypeError, ValueError, OverflowError, RecursionError, UnicodeError):
        return None


def build_local_tagged_fork_archive(
    ancestor_manifest: Any,
    left_manifest: Any,
    right_manifest: Any,
    *,
    separately_supplied_ancestor_checkpoint_sha256: Any = None,
) -> TaggedForkArchiveAudit:
    """Retain both paths as distinct tags; never collapse forks into a list."""
    if (ancestor_manifest is None or left_manifest is None
            or right_manifest is None):
        return TaggedForkArchiveAudit(NO_DATA, ("three_detached_snapshots_required",))
    ancestor = _copy(ancestor_manifest)
    left = _copy(left_manifest)
    right = _copy(right_manifest)
    if ancestor is None or left is None or right is None:
        return TaggedForkArchiveAudit(BLOCKED, ("invalid_detached_snapshot_copy",))

    checked = fork.audit_two_local_successors(
        ancestor, left, right,
        separately_supplied_ancestor_checkpoint_sha256=
            separately_supplied_ancestor_checkpoint_sha256,
    )
    if checked.status in (BLOCKED, NO_DATA):
        return TaggedForkArchiveAudit(
            checked.status, ("upstream_local_fork_invalid",) + tuple(checked.issues),
        )
    if not checked.both_strictly_extend_ancestor:
        return TaggedForkArchiveAudit(
            ANCESTOR_OBSTRUCTION,
            issues=tuple(checked.issues) +
                ("not_both_strict_extensions_of_one_ancestor",),
        )

    relation = "fork" if checked.local_fork_observed else "comparable"
    archive = {
        "schema": SCHEMA,
        "source_boundary": fork.VERSION,
        "ancestor": ancestor,
        "branches": [
            {"tag": "left", "snapshot": left},
            {"tag": "right", "snapshot": right},
        ],
        "declared_relation": relation,
        "prior_checkpoint_sha256": separately_supplied_ancestor_checkpoint_sha256,
    }
    try:
        raw = detached._canonical(archive)
        if len(raw) > MAX_ARCHIVE_BYTES:
            return TaggedForkArchiveAudit(BLOCKED, ("archive_size_limit",))
        digest = hashlib.sha256(raw).hexdigest()
    except (TypeError, ValueError, OverflowError, RecursionError, UnicodeError):
        return TaggedForkArchiveAudit(BLOCKED, ("invalid_archive_encoding",))
    wrong_checkpoint = (
        separately_supplied_ancestor_checkpoint_sha256 is not None
        and not checked.caller_prior_checkpoint_value_matches
    )
    if relation == "fork":
        status = ARCHIVED_FORK_AND_CHECKPOINT if wrong_checkpoint else ARCHIVED_FORK
    else:
        status = ARCHIVED_CHECKPOINT if wrong_checkpoint else ARCHIVED_COMPARABLE
    return TaggedForkArchiveAudit(
        status,
        issues=tuple(checked.issues),
        archive=archive,
        archive_sha256=digest,
        ancestor_sha256=checked.ancestor_manifest_sha256,
        left_sha256=checked.left_manifest_sha256,
        right_sha256=checked.right_manifest_sha256,
        independently_recomputed_snapshots=True,
        both_branches_locally_retained=True,
        fork_obstruction_preserved=checked.local_fork_observed,
        caller_prior_checkpoint_value_matches=
            checked.caller_prior_checkpoint_value_matches,
    )


def verify_local_tagged_fork_archive(
    archive: Any, *, separately_supplied_archive_sha256: Any = None,
) -> TaggedForkArchiveAudit:
    """Pure independent replay of a caller-declared detached branch archive."""
    if archive is None:
        return TaggedForkArchiveAudit(NO_DATA, ("tagged_archive_missing",))
    parsed = _copy(archive)
    if parsed is None or frozenset(parsed) != FIELDS:
        return TaggedForkArchiveAudit(BLOCKED, ("invalid_tagged_archive_schema",))
    if parsed["schema"] != SCHEMA or parsed["source_boundary"] != fork.VERSION:
        return TaggedForkArchiveAudit(BLOCKED, ("tagged_archive_version_mismatch",))
    branches = parsed["branches"]
    if (type(branches) is not list or len(branches) != 2
            or type(branches[0]) is not dict or type(branches[1]) is not dict
            or frozenset(branches[0]) != {"tag", "snapshot"}
            or frozenset(branches[1]) != {"tag", "snapshot"}
            or branches[0]["tag"] != "left" or branches[1]["tag"] != "right"):
        return TaggedForkArchiveAudit(BLOCKED, ("invalid_tag_order_or_branch_fields",))
    if parsed["declared_relation"] not in ("fork", "comparable"):
        return TaggedForkArchiveAudit(BLOCKED, ("invalid_tagged_relation",))
    assembled = build_local_tagged_fork_archive(
        parsed["ancestor"], branches[0]["snapshot"], branches[1]["snapshot"],
        separately_supplied_ancestor_checkpoint_sha256=
            parsed["prior_checkpoint_sha256"],
    )
    if assembled.archive is None or assembled.archive != parsed:
        return TaggedForkArchiveAudit(
            BLOCKED, ("tagged_archive_not_reproducible",) +
                    tuple(assembled.issues),
        )

    if separately_supplied_archive_sha256 is None:
        return assembled
    if not detached._sha256_shape(separately_supplied_archive_sha256):
        return replace(assembled, status=BLOCKED,
                       issues=assembled.issues + ("invalid_archive_sha256_shape",))
    if not hmac.compare_digest(
            assembled.archive_sha256, separately_supplied_archive_sha256):
        return replace(
            assembled, status=ARCHIVE_DIGEST_MISMATCH,
            issues=assembled.issues + ("caller_archive_digest_disagrees",),
        )
    return replace(assembled, caller_archive_digest_value_matches=True)


__all__ = (
    "VERSION", "SCHEMA", "ARCHIVED_FORK", "ARCHIVED_FORK_AND_CHECKPOINT",
    "ARCHIVED_COMPARABLE", "ARCHIVED_CHECKPOINT",
    "ANCESTOR_OBSTRUCTION", "ARCHIVE_DIGEST_MISMATCH",
    "TaggedForkArchiveAudit", "build_local_tagged_fork_archive",
    "verify_local_tagged_fork_archive",
)
