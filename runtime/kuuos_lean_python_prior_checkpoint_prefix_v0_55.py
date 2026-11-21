"""v0.55: compare two v0.54 detached snapshots for strict local extension.

The older list must be an EXACT ordered prefix of the later list, with at
least one new complete two-row reservation appended. Both snapshots are first
verified independently by the unchanged v0.54 offline verifier.

An optional prior checkpoint is a separately supplied SHA-256 *value* for
the WHOLE old manifest (not a chain head). This module checks equality but
does not verify independent custody, signature, real-world timing or source
identity. Matching a checkpoint does not prove the old or new history true.
No database, network, secret or original VerifyOS/PlanOS kernel is invoked.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
import hmac
import json
from typing import Any

from runtime import kuuos_lean_python_detached_replay_witness_v0_54 as detached
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA,
)

VERSION = "kuuos_lean_python_prior_checkpoint_prefix_v0_55"
PREFIX_UNANCHORED = "STRICT_LOCAL_REPLAY_PREFIX_UNANCHORED_PROPOSAL_ONLY"
PREFIX_CHECKPOINT_VALUE_MATCH = (
    "STRICT_LOCAL_REPLAY_PREFIX_PRIOR_CHECKPOINT_VALUE_MATCH_PROPOSAL_ONLY"
)
PREFIX_DIVERGENCE = "LOCAL_REPLAY_PREFIX_DIVERGENCE_OBSTRUCTION"
PREFIX_NO_NEW_ROWS = "LOCAL_REPLAY_NO_STRICT_EXTENSION_OBSTRUCTION"
PREFIX_CHECKPOINT_MISMATCH = "PRIOR_CHECKPOINT_VALUE_MISMATCH_OBSTRUCTION"
PREFIX_COMPOSITE_OBSTRUCTION = "LOCAL_REPLAY_PREFIX_MULTIPLE_OBSTRUCTIONS"

UNPROVED = (
    "BOTH_SNAPSHOTS_RECOMPUTABLE_DOES_NOT_PROVE_HISTORIC_ISSUANCE",
    "EXACT_PREFIX_CHECK_IS_NOT_EXTERNAL_IMMUTABILITY_OR_CUSTODY",
    "CALLER_SUPPLIED_PRIOR_CHECKPOINT_VALUE_HAS_NO_AUTHENTICATED_ORIGIN",
    "NO_VERIFIED_INDEPENDENT_CHECKPOINT_KEEPER_OR_SIGNATURE",
    "NO_REAL_WORLD_ORDER_CLOCK_OR_CROSS_HOST_REPLAY_PROTECTION",
    "NO_LEAN_PROOF_OF_JSON_SHA256_SQLITE_OR_CPYTHON_REFINEMENT",
    "ORIGINAL_PLANOS_THREE_RESULT_FINSETS_STILL_NO_DATA",
    "NO_GLOBAL_DESCENT_OR_HOST_EXECUTION_AUTHORITY",
)


@dataclass(frozen=True)
class PriorCheckpointPrefixAudit:
    status: str
    issues: tuple[str, ...] = ()
    old_entry_count: int = 0
    new_entry_count: int = 0
    added_complete_pairs: int = 0
    old_manifest_sha256: str | None = None
    new_manifest_sha256: str | None = None
    old_chain_head: str | None = None
    new_chain_head: str | None = None
    older_snapshot_recomputed: bool = False
    newer_snapshot_recomputed: bool = False
    exact_ordered_prefix_compatible: bool = False
    strict_local_extension: bool = False
    caller_prior_checkpoint_value_matches: bool = False
    independent_checkpoint_custody_authenticated: bool = False
    historical_receipt_authenticated: bool = False
    external_issuers_authenticated: bool = False
    cross_host_replay_protected: bool = False
    original_plan_result_state: str = NO_DATA
    original_lean_match_proved: bool = False
    global_descent_certified: bool = False
    host_execution_authorized: bool = False
    native_kernel_invocations: int = 0
    unresolved: tuple[str, ...] = UNPROVED


def _snap(value: Any) -> tuple[dict[str, Any] | None, str | None]:
    """Bounded JSON copy plus stability check; no change to the caller object."""
    if type(value) is not dict:
        return None, "snapshot_must_be_exact_dict"
    try:
        before = detached._canonical(value)
        if len(before) > detached.MAX_MANIFEST_BYTES:
            return None, "detached_snapshot_byte_limit"
        copied = json.loads(before)
        if before != detached._canonical(value):
            return None, "caller_snapshot_changed_during_copy"
        return copied, None
    except (TypeError, ValueError, RecursionError, OverflowError, UnicodeError):
        return None, "invalid_snapshot_json"


def audit_local_prior_checkpoint_prefix(
    older_manifest: Any,
    newer_manifest: Any,
    *,
    separately_supplied_prior_checkpoint_sha256: Any = None,
) -> PriorCheckpointPrefixAudit:
    """Pure verification of two *declared* snapshots, not historical trust.

    Verify every row in each snapshot independently, require exact preserved
    past rows and positive even-length append, then compare an optionally
    supplied OLD manifest digest VALUE without promoting it to provenance.
    Multiple obstructions are preserved in issues rather than voted away.
    """
    if older_manifest is None or newer_manifest is None:
        return PriorCheckpointPrefixAudit(
            status=NO_DATA, issues=("both_detached_snapshots_required",),
        )
    old, old_error = _snap(older_manifest)
    new, new_error = _snap(newer_manifest)
    if old_error or new_error:
        return PriorCheckpointPrefixAudit(
            status=BLOCKED,
            issues=tuple(x for x in (old_error, new_error) if x),
        )

    old_check = detached.verify_detached_replay_witness(old)
    new_check = detached.verify_detached_replay_witness(new)
    issues: list[str] = []
    if old_check.status != detached.DETACHED_UNANCHORED:
        issues.append("older_snapshot_invalid:" + old_check.status)
        issues.extend(old_check.issues)
    if new_check.status != detached.DETACHED_UNANCHORED:
        issues.append("newer_snapshot_invalid:" + new_check.status)
        issues.extend(new_check.issues)
    if issues:
        return PriorCheckpointPrefixAudit(
            BLOCKED, tuple(issues),
            older_snapshot_recomputed=old_check.local_chain_recomputed,
            newer_snapshot_recomputed=new_check.local_chain_recomputed,
        )

    old_rows = old["entries"]
    new_rows = new["entries"]
    old_count, new_count = len(old_rows), len(new_rows)
    exact_prefix = new_rows[:old_count] == old_rows
    if new_count <= old_count:
        issues.append("no_new_complete_pair_after_prior_snapshot")
    if not exact_prefix:
        issues.append("old_rows_not_exact_ordered_prefix")
    if new_count >= old_count and exact_prefix:
        if not hmac.compare_digest(
            new_rows[old_count - 1]["row_sha256"], old_check.chain_head,
        ):
            issues.append("old_chain_head_not_preserved")

    matching_value = False
    if separately_supplied_prior_checkpoint_sha256 is not None:
        if not detached._sha256_shape(
            separately_supplied_prior_checkpoint_sha256
        ):
            return PriorCheckpointPrefixAudit(
                BLOCKED, ("invalid_prior_checkpoint_sha256",),
                old_entry_count=old_count,
                new_entry_count=new_count,
                old_manifest_sha256=old_check.manifest_sha256,
                new_manifest_sha256=new_check.manifest_sha256,
                older_snapshot_recomputed=True,
                newer_snapshot_recomputed=True,
            )
        matching_value = hmac.compare_digest(
            old_check.manifest_sha256,
            separately_supplied_prior_checkpoint_sha256,
        )
        if not matching_value:
            issues.append("caller_prior_checkpoint_value_disagrees")

    strict = new_count > old_count and exact_prefix
    if issues:
        if len(issues) > 1:
            status = PREFIX_COMPOSITE_OBSTRUCTION
        elif issues[0] == "caller_prior_checkpoint_value_disagrees":
            status = PREFIX_CHECKPOINT_MISMATCH
        elif issues[0] == "no_new_complete_pair_after_prior_snapshot":
            status = PREFIX_NO_NEW_ROWS
        else:
            status = PREFIX_DIVERGENCE
    else:
        status = (
            PREFIX_CHECKPOINT_VALUE_MATCH
            if separately_supplied_prior_checkpoint_sha256 is not None
            else PREFIX_UNANCHORED
        )
    return PriorCheckpointPrefixAudit(
        status=status,
        issues=tuple(issues),
        old_entry_count=old_count,
        new_entry_count=new_count,
        added_complete_pairs=(new_count - old_count) // 2
            if strict else 0,
        old_manifest_sha256=old_check.manifest_sha256,
        new_manifest_sha256=new_check.manifest_sha256,
        old_chain_head=old_check.chain_head,
        new_chain_head=new_check.chain_head,
        older_snapshot_recomputed=True,
        newer_snapshot_recomputed=True,
        exact_ordered_prefix_compatible=exact_prefix,
        strict_local_extension=strict,
        caller_prior_checkpoint_value_matches=matching_value,
    )


__all__ = (
    "VERSION", "PREFIX_UNANCHORED", "PREFIX_CHECKPOINT_VALUE_MATCH",
    "PREFIX_DIVERGENCE", "PREFIX_NO_NEW_ROWS",
    "PREFIX_CHECKPOINT_MISMATCH", "PREFIX_COMPOSITE_OBSTRUCTION",
    "PriorCheckpointPrefixAudit", "audit_local_prior_checkpoint_prefix",
)
