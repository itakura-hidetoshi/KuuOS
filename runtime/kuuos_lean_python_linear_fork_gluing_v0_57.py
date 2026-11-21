"""v0.57: impossibility of gluing local forks in ONE append-only list.

All inputs are caller-declared, independently recomputable detached snapshots.
The v0.56 classifier recognizes forks of two locally valid continuations.
A verified fork has NO common extension within this specific exact-prefix,
strictly linear history model: neither historical truth nor universal
impossibility of richer DAG/causal reconciliation follows.

When histories are comparable, the longer declared history is a possible
linear common extension. An optional later witness is checked by v0.54 and
must have BOTH histories as exact ordered prefixes. No witness is selected
to represent real-world authority, no host action or original OS runs.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime import kuuos_lean_python_common_ancestor_fork_v0_56 as fork
from runtime import kuuos_lean_python_detached_replay_witness_v0_54 as detached
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA,
)

VERSION = "kuuos_lean_python_linear_fork_gluing_v0_57"
NO_LINEAR_GLUE = "LOCAL_FORK_HAS_NO_COMMON_LINEAR_APPEND_SUCCESSOR_OBSTRUCTION"
NO_LINEAR_GLUE_AND_CHECKPOINT = (
    "LOCAL_FORK_NO_LINEAR_GLUE_AND_PRIOR_CHECKPOINT_OBSTRUCTIONS"
)
COMPARABLE_LOCAL = "LOCAL_COMPARABLE_LINEAR_GLUE_POSSIBLE_PROPOSAL_ONLY"
MATCHED_LOCAL_WITNESS = "LOCAL_COMMON_LINEAR_SUCCESSOR_VALUE_VERIFIED_PROPOSAL_ONLY"
WITNESS_OBSTRUCTION = "LOCAL_DECLARED_COMMON_LINEAR_SUCCESSOR_NOT_COMPATIBLE"
ANCESTOR_OBSTRUCTION = "LOCAL_COMMON_ANCESTOR_OBSTRUCTION"
CHECKPOINT_OBSTRUCTION = "LOCAL_PRIOR_CHECKPOINT_VALUE_OBSTRUCTION"
UNPROVED = (
    "LINEAR_PREFIX_NON_GLUING_IS_NOT_GLOBAL_IMPOSSIBILITY_IN_RICHER_MODELS",
    "NO_AUTHENTICATED_EXTERNAL_ISSUER_OR_CHECKPOINT_CUSTODY",
    "NO_CAUSAL_TIME_OR_GLOBAL_CROSS_HOST_REPLAY_GUARANTEE",
    "NO_SHA256_JSON_SQLITE_CPYTHON_FORMAL_REFINEMENT_PROOF",
    "ORIGINAL_PLANOS_THREE_RESULT_SETS_NOT_EMITTED",
    "NO_GLOBAL_DESCENT_OR_HOST_EXECUTION_AUTHORITY",
)


@dataclass(frozen=True)
class LinearForkGluingAudit:
    status: str
    issues: tuple[str, ...] = ()
    prior_chain_recomputed: bool = False
    declared_linear_fork: bool = False
    common_linear_successor_possible_in_this_model: bool = False
    supplied_successor_verifies_both_exact_prefixes: bool = False
    local_declared_preferred_witness: str | None = None
    supplied_successor_sha256: str | None = None
    caller_checkpoint_value_matches: bool = False
    independently_authenticated_history: bool = False
    independent_checkpoint_custody_authenticated: bool = False
    original_plan_result_state: str = NO_DATA
    external_issuers_authenticated: bool = False
    cross_host_replay_protected: bool = False
    original_lean_match_proved: bool = False
    global_descent_certified: bool = False
    host_execution_authorized: bool = False
    native_kernel_invocations: int = 0
    unresolved: tuple[str, ...] = UNPROVED


def audit_local_linear_fork_gluing(
    ancestor_manifest: Any,
    left_manifest: Any,
    right_manifest: Any,
    *,
    separately_supplied_ancestor_checkpoint_sha256: Any = None,
    declared_future_manifest: Any = None,
) -> LinearForkGluingAudit:
    """Bounded, offline, read-only certificate of exact-prefix compatibility.

    Concretely impossible only inside a SINGLE append-only ordered list.
    A caller can give a future manifest to test a proposed common successor;
    no wider consensus protocol, witness issuance or external authentication.
    """
    upstream = fork.audit_two_local_successors(
        ancestor_manifest, left_manifest, right_manifest,
        separately_supplied_ancestor_checkpoint_sha256=
            separately_supplied_ancestor_checkpoint_sha256,
    )
    if upstream.status in (BLOCKED, NO_DATA):
        return LinearForkGluingAudit(
            upstream.status,
            issues=("upstream_fork_audit:" + upstream.status,) +
                   tuple(upstream.issues),
        )

    issues = list(upstream.issues)
    mismatch = (
        separately_supplied_ancestor_checkpoint_sha256 is not None
        and not upstream.caller_prior_checkpoint_value_matches
    )
    if not upstream.both_strictly_extend_ancestor:
        return LinearForkGluingAudit(
            ANCESTOR_OBSTRUCTION,
            issues=tuple(issues) + ("not_both_strict_extensions",),
            caller_checkpoint_value_matches=
                upstream.caller_prior_checkpoint_value_matches,
        )

    # Even if a later document is asserted, an actual fork has no linear
    # common successor by the v0.57 theorem's exact-prefix hypotheses.
    if upstream.local_fork_observed:
        return LinearForkGluingAudit(
            NO_LINEAR_GLUE_AND_CHECKPOINT if mismatch else NO_LINEAR_GLUE,
            issues=tuple(issues) +
                   ("no_common_exact_prefix_successor_in_one_linear_list",),
            prior_chain_recomputed=True,
            declared_linear_fork=True,
            caller_checkpoint_value_matches=
                upstream.caller_prior_checkpoint_value_matches,
        )

    # Both descendants are individually complete, coherent and comparable.
    left, left_issue = fork.prior._snap(left_manifest)
    right, right_issue = fork.prior._snap(right_manifest)
    if left_issue or right_issue:
        return LinearForkGluingAudit(
            BLOCKED, tuple(x for x in (left_issue, right_issue) if x),
        )
    assert left is not None and right is not None
    preferred_witness = (
        "left" if len(left["entries"]) >= len(right["entries"]) else "right"
    )
    if declared_future_manifest is None:
        return LinearForkGluingAudit(
            CHECKPOINT_OBSTRUCTION if mismatch else COMPARABLE_LOCAL,
            issues=tuple(issues),
            prior_chain_recomputed=True,
            common_linear_successor_possible_in_this_model=True,
            local_declared_preferred_witness=preferred_witness,
            caller_checkpoint_value_matches=
                upstream.caller_prior_checkpoint_value_matches,
        )

    checked = detached.verify_detached_replay_witness(declared_future_manifest)
    if checked.status != detached.DETACHED_UNANCHORED:
        return LinearForkGluingAudit(
            BLOCKED,
            issues=tuple(issues) + (
                "invalid_declared_future:" + checked.status,
            ) + tuple(checked.issues),
            prior_chain_recomputed=True,
            common_linear_successor_possible_in_this_model=True,
            local_declared_preferred_witness=preferred_witness,
        )
    future, future_issue = fork.prior._snap(declared_future_manifest)
    if future_issue or future is None:
        return LinearForkGluingAudit(
            BLOCKED, issues=("invalid_future_snapshot_copy",),
        )
    future_rows = future["entries"]
    left_rows = left["entries"]
    right_rows = right["entries"]
    both_prefix = (
        future_rows[:len(left_rows)] == left_rows
        and future_rows[:len(right_rows)] == right_rows
    )
    if not both_prefix:
        return LinearForkGluingAudit(
            WITNESS_OBSTRUCTION,
            issues=tuple(issues) + ("declared_future_not_both_exact_prefixes",),
            prior_chain_recomputed=True,
            common_linear_successor_possible_in_this_model=True,
            supplied_successor_sha256=checked.manifest_sha256,
            local_declared_preferred_witness=preferred_witness,
            caller_checkpoint_value_matches=
                upstream.caller_prior_checkpoint_value_matches,
        )
    return LinearForkGluingAudit(
        CHECKPOINT_OBSTRUCTION if mismatch else MATCHED_LOCAL_WITNESS,
        issues=tuple(issues),
        prior_chain_recomputed=True,
        common_linear_successor_possible_in_this_model=True,
        supplied_successor_verifies_both_exact_prefixes=True,
        local_declared_preferred_witness=preferred_witness,
        supplied_successor_sha256=checked.manifest_sha256,
        caller_checkpoint_value_matches=
            upstream.caller_prior_checkpoint_value_matches,
    )


__all__ = (
    "VERSION", "NO_LINEAR_GLUE", "NO_LINEAR_GLUE_AND_CHECKPOINT",
    "COMPARABLE_LOCAL", "MATCHED_LOCAL_WITNESS", "WITNESS_OBSTRUCTION",
    "ANCESTOR_OBSTRUCTION", "CHECKPOINT_OBSTRUCTION",
    "LinearForkGluingAudit", "audit_local_linear_fork_gluing",
)
