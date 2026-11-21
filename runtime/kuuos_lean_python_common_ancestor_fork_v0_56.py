"""v0.56: detect two locally divergent detached successor histories.

The old, left and right inputs are caller-declared snapshots; each descendant
must independently pass the v0.55 strict-prefix check against the old one.
A fork is reported only if neither complete successor is an ordered prefix
of the other. Differences are retained as an obstruction, never voted away.

This does NOT establish the independent issuers, trusted checkpoint custody,
physical timestamps, SHA-256 security, CPython↔Lean refinement, global fork
truth, cross-host replay protection, or any PlanOS execution permission.
No database, secret, network or original OS code is executed.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime import kuuos_lean_python_prior_checkpoint_prefix_v0_55 as prior
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA,
)

VERSION = "kuuos_lean_python_common_ancestor_fork_v0_56"
LOCAL_FORK = "LOCAL_DECLARED_SUCCESSOR_FORK_OBSTRUCTION"
LOCAL_CHAIN = "LOCALLY_COMPARABLE_SUCCESSOR_CHAIN_PROPOSAL_ONLY"
LOCAL_SAME = "LOCALLY_IDENTICAL_SUCCESSOR_PROPOSAL_ONLY"
LOCAL_FORK_AND_CHECKPOINT = "LOCAL_FORK_AND_PRIOR_CHECKPOINT_OBSTRUCTIONS"
LOCAL_CHECKPOINT = "LOCAL_PRIOR_CHECKPOINT_VALUE_OBSTRUCTION"
LOCAL_ANCESTOR = "LOCAL_COMMON_ANCESTOR_EXTENSION_OBSTRUCTION"

UNPROVED = (
    "DECLARED_COMMON_ANCESTOR_IS_NOT_INDEPENDENTLY_AUTHENTICATED_HISTORY",
    "FORK_DETECTION_DOES_NOT_SELECT_A_TRUE_SUCCESSOR",
    "CALLER_CHECKPOINT_DIGEST_HAS_NO_PROVEN_CUSTODY_OR_SIGNER",
    "NO_REAL_WORLD_CAUSAL_CLOCK_OR_CROSS_HOST_REPLAY_PROOF",
    "NO_LEAN_SHA256_SQLITE_CPYTHON_REFINEMENT_THEOREM",
    "ORIGINAL_PLANOS_RESULT_FINSETS_NOT_EMITTED",
    "NO_GLOBAL_DESCENT_OR_HOST_EXECUTION_AUTHORITY",
)


@dataclass(frozen=True)
class LocalForkAudit:
    status: str
    issues: tuple[str, ...] = ()
    ancestor_entry_count: int = 0
    left_entry_count: int = 0
    right_entry_count: int = 0
    first_divergent_entry_id: int | None = None
    ancestor_manifest_sha256: str | None = None
    left_manifest_sha256: str | None = None
    right_manifest_sha256: str | None = None
    both_strictly_extend_ancestor: bool = False
    successor_histories_comparable: bool = False
    successor_histories_identical: bool = False
    local_fork_observed: bool = False
    caller_prior_checkpoint_value_matches: bool = False
    independent_checkpoint_custody_authenticated: bool = False
    independent_issuers_authenticated: bool = False
    historical_source_authenticated: bool = False
    original_plan_result_state: str = NO_DATA
    cross_host_replay_protected: bool = False
    original_lean_match_proved: bool = False
    global_descent_certified: bool = False
    host_execution_authorized: bool = False
    selected_successor: None = None
    native_kernel_invocations: int = 0
    unresolved: tuple[str, ...] = UNPROVED


def audit_two_local_successors(
    ancestor_manifest: Any,
    left_manifest: Any,
    right_manifest: Any,
    *,
    separately_supplied_ancestor_checkpoint_sha256: Any = None,
) -> LocalForkAudit:
    """Pure local comparison: fork obstruction or comparable declared routes.

    It cannot determine which proposed history actually occurred.
    """
    if (ancestor_manifest is None or left_manifest is None
            or right_manifest is None):
        return LocalForkAudit(NO_DATA, ("three_detached_snapshots_required",))

    ancestor, anc_problem = prior._snap(ancestor_manifest)
    left, left_problem = prior._snap(left_manifest)
    right, right_problem = prior._snap(right_manifest)
    problems = tuple(x for x in (anc_problem, left_problem, right_problem) if x)
    if problems:
        return LocalForkAudit(BLOCKED, problems)

    left_audit = prior.audit_local_prior_checkpoint_prefix(
        ancestor, left,
        separately_supplied_prior_checkpoint_sha256=
            separately_supplied_ancestor_checkpoint_sha256,
    )
    right_audit = prior.audit_local_prior_checkpoint_prefix(
        ancestor, right,
        separately_supplied_prior_checkpoint_sha256=
            separately_supplied_ancestor_checkpoint_sha256,
    )
    blockers = (BLOCKED, NO_DATA)
    if left_audit.status in blockers or right_audit.status in blockers:
        return LocalForkAudit(
            BLOCKED, (
                ("left_invalid:" + left_audit.status,)
                if left_audit.status in blockers else ()
            ) + (
                ("right_invalid:" + right_audit.status,)
                if right_audit.status in blockers else ()
            ) + tuple("left:" + x for x in left_audit.issues)
              + tuple("right:" + x for x in right_audit.issues),
        )

    old_rows = ancestor["entries"]
    left_rows = left["entries"]
    right_rows = right["entries"]
    counts = (len(old_rows), len(left_rows), len(right_rows))
    both_strict = (left_audit.strict_local_extension
                   and right_audit.strict_local_extension)
    checkpoint_match = (
        separately_supplied_ancestor_checkpoint_sha256 is not None
        and left_audit.caller_prior_checkpoint_value_matches
        and right_audit.caller_prior_checkpoint_value_matches
    )
    checkpoint_disagrees = (
        separately_supplied_ancestor_checkpoint_sha256 is not None
        and not checkpoint_match
    )
    issues = []
    if not left_audit.strict_local_extension:
        issues.extend("left:" + x for x in left_audit.issues)
        issues.append("left_is_not_a_strict_extension_of_ancestor")
    if not right_audit.strict_local_extension:
        issues.extend("right:" + x for x in right_audit.issues)
        issues.append("right_is_not_a_strict_extension_of_ancestor")
    if checkpoint_disagrees:
        issues.append("caller_prior_checkpoint_value_disagrees")
    if not both_strict:
        return LocalForkAudit(
            LOCAL_ANCESTOR, tuple(issues),
            ancestor_entry_count=counts[0],
            left_entry_count=counts[1], right_entry_count=counts[2],
            ancestor_manifest_sha256=left_audit.old_manifest_sha256,
            left_manifest_sha256=left_audit.new_manifest_sha256,
            right_manifest_sha256=right_audit.new_manifest_sha256,
            caller_prior_checkpoint_value_matches=checkpoint_match,
        )

    identical = left_rows == right_rows
    comparable = (identical
                  or left_rows == right_rows[:len(left_rows)]
                  or right_rows == left_rows[:len(right_rows)])
    first_divergence = None
    if not comparable:
        for pos, (a, b) in enumerate(zip(left_rows, right_rows), start=1):
            if a != b:
                first_divergence = pos
                break
        if first_divergence is None:
            return LocalForkAudit(
                BLOCKED, ("inconsistent_fork_classifier_state",),
            )
        issues.append("incompatible_declared_successor_histories")
        issues.append("first_divergence_at_entry:" + str(first_divergence))

    if not comparable:
        status = LOCAL_FORK_AND_CHECKPOINT if checkpoint_disagrees else LOCAL_FORK
    elif checkpoint_disagrees:
        status = LOCAL_CHECKPOINT
    elif identical:
        status = LOCAL_SAME
    else:
        status = LOCAL_CHAIN
    return LocalForkAudit(
        status=status,
        issues=tuple(issues),
        ancestor_entry_count=counts[0], left_entry_count=counts[1],
        right_entry_count=counts[2],
        first_divergent_entry_id=first_divergence,
        ancestor_manifest_sha256=left_audit.old_manifest_sha256,
        left_manifest_sha256=left_audit.new_manifest_sha256,
        right_manifest_sha256=right_audit.new_manifest_sha256,
        both_strictly_extend_ancestor=True,
        successor_histories_comparable=comparable,
        successor_histories_identical=identical,
        local_fork_observed=not comparable,
        caller_prior_checkpoint_value_matches=checkpoint_match,
    )


__all__ = (
    "VERSION", "LOCAL_FORK", "LOCAL_CHAIN", "LOCAL_SAME",
    "LOCAL_FORK_AND_CHECKPOINT", "LOCAL_CHECKPOINT", "LOCAL_ANCESTOR",
    "LocalForkAudit", "audit_two_local_successors",
)
