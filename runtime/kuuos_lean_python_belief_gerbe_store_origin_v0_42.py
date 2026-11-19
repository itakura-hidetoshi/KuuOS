"""v0.42: original persisted Belief gerbe origin to Decision/Plural/Wa/Plan.

Read-only source audit only. The original BeliefGerbeStore native replay
and already existing v0.18 belief receipt/ledger replay are reused, not
reimplemented or silently replaced. Distinct historical source versions,
timestamps, and external authority obstructions remain explicit.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from runtime.kuuos_belief_os_gerbe_store_v0_3 import (
    BeliefGerbeStore, BeliefGerbeStoreError, build_initial_gerbe_state,
)
from runtime.kuuos_lean_python_belief_receipt_guard_v0_18 import (
    BeliefReceiptBoundaryError, _replay_belief_ledger,
)
from runtime.kuuos_lean_python_act_observe_store_compat_v0_35 import (
    _packet, _store_files,
)
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import _same
from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    BLOCKED, NO_DATA,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from runtime.kuuos_lean_python_wa_plan_store_compat_v0_39 import (
    _CapturedReads, _INPUT_ERRORS, _replay_captured, _trusted_store_root,
)
from runtime.kuuos_lean_python_plural_store_origin_v0_40 import (
    _roots_separate,
)
from runtime.kuuos_lean_python_decision_store_origin_v0_41 import (
    SCOPED_COMPATIBLE as PRIOR_PASS, audit_native_decision_store_origin,
)

VERSION = "kuuos_lean_python_belief_gerbe_store_origin_v0_42"
SOURCE_PARENT = "0272779f97c0513f8922e8e1e4c3c645cfab3810"
SCOPED_COMPATIBLE = "SCOPED_BELIEF_DECISION_PLURAL_WA_PLAN_ORIGINS_COMPATIBLE"
_BELIEF_FILES = (
    "belief-gerbe-genesis.json",
    "belief-gerbe-ledger.jsonl",
    "belief-gerbe-snapshot.json",
)
_INPUT = _INPUT_ERRORS + (BeliefGerbeStoreError, UnicodeError)


class _CapturedBeliefStore(_CapturedReads, BeliefGerbeStore):
    """Original native gerbe replay on the exact first captured file bytes."""


@dataclass(frozen=True)
class NativeBeliefStoreOriginAudit:
    status: str
    issues: tuple[str, ...] = ()
    belief_genesis_sha256: str | None = None
    belief_final_sha256: str | None = None
    supplied_last_receipt_sha256: str | None = None
    replayed_last_receipt_sha256: str | None = None
    belief_commit_count: int = 0
    belief_history_receipt_count: int = 0
    checked_source_paths: tuple[str, ...] = ()
    staged_typed_edge_statuses: tuple[tuple[str, str], ...] = ()
    belief_original_store_replayed: bool = False
    belief_genesis_matches_original_constructor: bool = False
    belief_history_data_conditions_checked: bool = False
    replayed_native_receipt_equals_supplied: bool = False
    prior_decision_plural_wa_plan_origins_checked: bool = False
    belief_store_bytes_stable_during_audit: bool = False
    prior_store_bytes_stable_during_audit: bool = False
    belief_receipt_time_ms: int | None = None
    decision_genesis_time_ms: int | None = None
    cross_source_time_relation: str | None = None
    # Source receipt time 5000 versus Decision genesis time 1000 in the
    # native fixture is an OBSERVED NUMERICAL order, not a certified clock.
    common_belief_decision_clock_proved: bool = False
    global_temporal_descent_proved: bool = False
    global_atomic_five_store_snapshot_proved: bool = False
    original_transport_issuer_authenticated: bool = False
    belief_receipt_external_issuer_authenticated: bool = False
    global_descent_proved: bool = False
    lean_python_semantic_refinement_proved: bool = False
    actual_act_numeric_witnesses_proved: bool = False
    host_license_granted: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    clinical_authority_granted: bool = False
    legal_authority_granted: bool = False
    git_authority_granted: bool = False
    memory_overwrite_authority_granted: bool = False
    original_store_mutated: bool = False


def _hold(status: str, *issues: str) -> NativeBeliefStoreOriginAudit:
    return NativeBeliefStoreOriginAudit(status=status, issues=tuple(issues))


def _history_data_conditions(
    genesis: dict, final: dict, commits: list[dict],
) -> bool:
    """Scoped Python data analogue of Lean SurfaceHolonomyHistory, no theorem."""
    history = final.get("receipt_history")
    processed = final.get("processed_packet_digests")
    if type(history) is not list or type(processed) is not list:
        return False
    n = len(commits)
    if not (
        type(genesis.get("event_count")) is int
        and genesis["event_count"] == 0
        and type(genesis.get("run_count")) is int
        and genesis["run_count"] == 0
        and genesis.get("receipt_history") == []
        and genesis.get("processed_packet_digests") == []
        and type(final.get("event_count")) is int
        and final["event_count"] == n
        and type(final.get("run_count")) is int
        and final["run_count"] == n
        and len(history) == n
        and len(processed) == n
    ):
        return False
    for i, commit in enumerate(commits, start=1):
        entry = history[i - 1]
        packet = commit.get("packet")
        if type(entry) is not dict or type(packet) is not dict:
            return False
        if not (
            type(entry.get("event_index")) is int
            and entry["event_index"] == i
            and _same(entry.get("belief_gerbe_packet_digest"),
                      commit.get("belief_gerbe_packet_digest"))
            and _same(entry.get("belief_gerbe_receipt_digest"),
                      commit.get("belief_gerbe_receipt_digest"))
            and _same(processed[i - 1],
                      commit.get("belief_gerbe_packet_digest"))
            and _same(packet.get("belief_gerbe_packet_digest"),
                      commit.get("belief_gerbe_packet_digest"))
        ):
            return False
    return _same(
        final.get("latest_receipt_digest"),
        commits[-1].get("belief_gerbe_receipt_digest"),
    )


def audit_native_belief_gerbe_store_origin(
    belief_state: Any,
    belief_receipt: Any,
    decision_state: Any,
    plural_state: Any,
    wa_state: Any,
    plan_state: Any,
    replan_activation_receipt: Any,
    original_belief_store_root: Any,
    original_decision_store_root: Any,
    original_plural_store_root: Any,
    original_wa_store_root: Any,
    original_plan_store_root: Any,
) -> NativeBeliefStoreOriginAudit:
    """Bind exactly five supplied original persisted stores and Belief receipt.

    A scoped positive answer is only the conjunction of selected native
    source checks; it never asserts an atomic snapshot or external issuance.
    """
    named = (
        ("BeliefOSState", belief_state),
        ("BeliefOSReceipt", belief_receipt),
        ("DecisionOS", decision_state),
        ("DecisionOSPlural", plural_state),
        ("DecisionOSWa", wa_state),
        ("PlanOS", plan_state),
        ("replan_receipt", replan_activation_receipt),
        ("BeliefStore", original_belief_store_root),
        ("DecisionStore", original_decision_store_root),
        ("PluralStore", original_plural_store_root),
        ("WaStore", original_wa_store_root),
        ("PlanStore", original_plan_store_root),
    )
    missing = tuple(n + ":original_source_missing" for n, v in named if v is None)
    if missing:
        return _hold(NO_DATA, *missing)
    root_values = (
        original_belief_store_root, original_decision_store_root,
        original_plural_store_root, original_wa_store_root,
        original_plan_store_root,
    )
    if any(type(v) is not str and type(v) is not type(Path())
           for v in root_values):
        return _hold(BLOCKED, "belief_decision_chain:untrusted_root_type")

    try:
        belief = _packet(belief_state, "BeliefOSState")
        supplied = _packet(belief_receipt, "BeliefOSReceipt")
        decision = _packet(decision_state, "DecisionOS")
        plural = _packet(plural_state, "DecisionOSPlural")
        wa = _packet(wa_state, "DecisionOSWa")
        plan = _packet(plan_state, "PlanOS")
        receipt = _packet(replan_activation_receipt, "replan_receipt")
        roots = tuple(_trusted_store_root(root) for root in root_values)
        if not _roots_separate(roots):
            return _hold(BLOCKED, "belief_decision_chain:roots_overlap")
        belief_root, decision_root, plural_root, wa_root, plan_root = roots
        captured = _store_files(belief_root, _BELIEF_FILES)
        genesis, final, commits = _replay_captured(
            belief_root, _CapturedBeliefStore, captured,
        )
        final = _packet(final, "BeliefStore.final")
    except FileNotFoundError:
        return _hold(NO_DATA, "belief_store:original_history_missing")
    except _INPUT as exc:
        return _hold(BLOCKED, "belief_store:original_source_invalid:"
                     + type(exc).__name__)

    if not _same(belief, final):
        return _hold(BLOCKED, "BeliefOSState:not_original_stored_final")

    failures: list[str] = []
    absent: list[str] = []
    prior = None
    replayed_receipt = None
    aligned = False

    try:
        original_genesis = build_initial_gerbe_state(
            lineage_id=genesis["lineage_id"],
            now_ms=genesis["updated_at_ms"],
        )
        if not _same(original_genesis, genesis):
            failures.append("BeliefOSState:genesis_not_original_constructor")
        aligned = _history_data_conditions(genesis, final, commits)
        if not aligned:
            failures.append("BeliefOSState:surface_holonomy_history_not_aligned")

        # This exact native source/receipt replay was implemented in v0.18.
        # Reuse its own kernel-based receipt reconstruction and source
        # metadata checks rather than duplicating its proof obligations.
        try:
            replayed_receipt, _ = _replay_belief_ledger(
                genesis, commits, final,
            )
        except BeliefReceiptBoundaryError as error:
            target = absent if error.status == NO_DATA else failures
            target.extend("v018:" + item for item in error.issues)
        if replayed_receipt is not None and not _same(replayed_receipt, supplied):
            failures.append("BeliefOSReceipt:not_original_last_replayed_receipt")

        # Exact supplied receipt, exact five original store roots, and
        # all previously certified v0.41/v0.40/v0.39 staged source edges.
        prior = audit_native_decision_store_origin(
            belief_receipt=supplied,
            decision_state=decision,
            plural_state=plural,
            wa_state=wa,
            plan_state=plan,
            replan_activation_receipt=receipt,
            original_decision_store_root=decision_root,
            original_plural_store_root=plural_root,
            original_wa_store_root=wa_root,
            original_plan_store_root=plan_root,
        )
        if prior.status == BLOCKED:
            failures.extend("v041:" + item for item in prior.issues)
            if not prior.issues:
                failures.append("v041:blocked")
        elif prior.status != PRIOR_PASS:
            absent.append("v041:unconfirmed:" + prior.status)
            absent.extend("v041:" + item for item in prior.issues)
        elif not (
            prior.decision_original_store_replayed
            and prior.decision_genesis_matches_original_constructor
            and prior.decision_history_data_conditions_checked
            and prior.supplied_belief_receipt_locally_valid
            and prior.belief_decision_source_identity_checked
            and prior.prior_plural_wa_plan_origins_checked
            and prior.decision_store_bytes_stable_during_audit
            and prior.prior_store_bytes_stable_during_audit
        ):
            absent.append("v041:original_conditions_unconfirmed")
    except _INPUT as exc:
        return _hold(BLOCKED, "belief_store:original_conditions_invalid:"
                     + type(exc).__name__)

    after = None
    try:
        _trusted_store_root(belief_root)
        after = _store_files(belief_root, _BELIEF_FILES)
        if captured != after:
            failures.append("belief_store:original_bytes_changed")
    except FileNotFoundError:
        absent.append("belief_store:original_history_disappeared")
    except _INPUT as exc:
        failures.append("belief_store:recheck_invalid:" + type(exc).__name__)

    status = BLOCKED if failures else NO_DATA if absent else SCOPED_COMPATIBLE
    passed = status == SCOPED_COMPATIBLE
    return NativeBeliefStoreOriginAudit(
        status=status,
        issues=tuple(dict.fromkeys(failures + absent)),
        belief_genesis_sha256=_fingerprint(genesis),
        belief_final_sha256=_fingerprint(final),
        supplied_last_receipt_sha256=_fingerprint(supplied),
        replayed_last_receipt_sha256=(
            _fingerprint(replayed_receipt) if replayed_receipt is not None
            else None
        ),
        belief_commit_count=len(commits),
        belief_history_receipt_count=len(final.get("receipt_history", [])),
        checked_source_paths=(
            tuple("BeliefOSState." + path for path in _BELIEF_FILES)
            + ("BeliefOSReceipt.replayed_last_packet",)
            + (prior.checked_source_paths if prior else ())
        ),
        staged_typed_edge_statuses=(
            prior.staged_typed_edge_statuses if prior else ()
        ),
        belief_original_store_replayed=passed,
        belief_genesis_matches_original_constructor=passed,
        belief_history_data_conditions_checked=passed and aligned,
        replayed_native_receipt_equals_supplied=(
            passed and replayed_receipt is not None
            and _same(replayed_receipt, supplied)
        ),
        prior_decision_plural_wa_plan_origins_checked=passed,
        belief_store_bytes_stable_during_audit=(
            after is not None and captured == after
        ),
        prior_store_bytes_stable_during_audit=(
            prior.decision_store_bytes_stable_during_audit
            and prior.prior_store_bytes_stable_during_audit if prior else False
        ),
        belief_receipt_time_ms=prior.source_receipt_created_at_ms if prior else None,
        decision_genesis_time_ms=prior.decision_genesis_updated_at_ms if prior else None,
        cross_source_time_relation=prior.cross_source_time_relation if prior else None,
    )


__all__ = (
    "VERSION", "SOURCE_PARENT", "SCOPED_COMPATIBLE", "NO_DATA", "BLOCKED",
    "NativeBeliefStoreOriginAudit", "audit_native_belief_gerbe_store_origin",
)
