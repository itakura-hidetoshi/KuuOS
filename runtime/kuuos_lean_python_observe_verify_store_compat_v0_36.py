"""Lean→Python v0.36: original persisted ObserveOS→VerifyOS typed compatibility.

Read-only replay of the original two file-backed stores. Checks the
committed ObserveOS -> INITIAL VerifyOS source edge, then the native FINAL
VerifyOS evidence/debt projection. These are bounded Python checks, not
a Lean proof of the Python interpreter or of global descent, authenticity,
truth, causality, or any power to act.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from runtime.kuuos_observe_os_store_v0_1 import ObserveStore, ObserveStoreError
from runtime.kuuos_verify_os_store_v0_1 import VerifyStore, VerifyStoreError
from runtime.kuuos_lean_python_act_observe_store_compat_v0_35 import (
    _native_store, _packet, _store_files,
)
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import _same
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from runtime.kuuos_lean_python_lineage_handoff_v0_2 import (
    HANDOFF_CONTRACTS, audit_handoff,
)
from runtime.kuuos_lean_python_verify_native_binding_v0_28 import (
    audit_native_verify_from_observe,
)
from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    PASS as NATIVE_PASS, NO_DATA, BLOCKED,
)
from runtime.kuuos_lean_python_contract_bridge_v0_1 import PASSED as EDGE_PASS


VERSION = "kuuos_lean_python_observe_verify_store_compat_v0_36"
SOURCE_PARENT = "269648c480cffd8f35d7cccdd0feaacf6ffb1e07"
SCOPED_COMPATIBLE = "SCOPED_OBSERVE_VERIFY_STORE_COMPATIBLE"
EDGE = ("ObserveOS", "VerifyOS")
_OBSERVE_FILES = (
    "observe-genesis.json", "observe-ledger.jsonl", "observe-snapshot.json",
)
_VERIFY_FILES = (
    "verify-genesis.json", "verify-ledger.jsonl", "verify-snapshot.json",
)


@dataclass(frozen=True)
class NativeObserveVerifyStoreAudit:
    status: str
    issues: tuple[str, ...] = ()
    original_observe_digest: str | None = None
    original_verify_genesis_digest: str | None = None
    original_verify_final_digest: str | None = None
    adjudication_verdict: str | None = None
    observe_commit_count: int = 0
    verify_commit_count: int = 0
    checked_source_paths: tuple[str, ...] = ()
    observe_original_store_replayed: bool = False
    verify_original_store_replayed: bool = False
    original_observe_to_verify_genesis_edge_checked: bool = False
    original_final_verify_lean_data_checked: bool = False
    # Deliberately never promoted by this compatibility result.
    external_receipt_authenticated: bool = False
    verification_is_truth: bool = False
    causal_attribution_authority_granted: bool = False
    whole_program_lean_python_refinement_proved: bool = False
    global_descent_proved: bool = False
    clinical_authority_granted: bool = False
    execution_authority_granted: bool = False
    host_license_granted: bool = False
    git_authority_granted: bool = False
    original_store_mutated: bool = False


def _hold(status: str, reason: str) -> NativeObserveVerifyStoreAudit:
    return NativeObserveVerifyStoreAudit(status=status, issues=(reason,))


def audit_native_observe_verify_store_compatibility(
    observe_state: Any,
    verify_state: Any,
    original_observe_store_root: Any,
    original_verify_store_root: Any,
) -> NativeObserveVerifyStoreAudit:
    """Audit precisely the saved original Observe→Verify relation.

    The initial Verify genesis preserves the original Observe source
    identity. The final Verify ledger is independently replayed and
    checked through the registered native VerifyOS Lean-condition adapter.
    No store method that writes or invokes the host is used.
    """
    for label, value in (
        ("ObserveOS", observe_state),
        ("VerifyOS", verify_state),
        ("ObserveStore", original_observe_store_root),
        ("VerifyStore", original_verify_store_root),
    ):
        if value is None:
            return _hold(NO_DATA, label + ":source_missing")
    try:
        observe = _packet(observe_state, "ObserveOS")
        verify = _packet(verify_state, "VerifyOS")
        # Path is a factory; concrete trusted roots are PosixPath/WindowsPath.
        if not all(
            type(root) is str or isinstance(root, Path)
            for root in (original_observe_store_root, original_verify_store_root)
        ):
            return _hold(BLOCKED, "trusted_store_paths_required")
        observe_root = Path(original_observe_store_root)
        verify_root = Path(original_verify_store_root)
        if observe_root.resolve() == verify_root.resolve():
            return _hold(BLOCKED, "ObserveOS_VerifyOS_roots_must_be_distinct")
        observe_before = _store_files(observe_root, _OBSERVE_FILES)
        verify_before = _store_files(verify_root, _VERIFY_FILES)
        _, original_observe, observe_commits = _native_store(
            observe_root, ObserveStore, _OBSERVE_FILES
        )
        verify_genesis, original_verify, verify_commits = _native_store(
            verify_root, VerifyStore, _VERIFY_FILES
        )
    except FileNotFoundError:
        return _hold(NO_DATA, "original_store_missing_or_uncommitted")
    except (
        TypeError, ValueError, OSError, RecursionError,
        ObserveStoreError, VerifyStoreError,
    ) as exc:
        return _hold(BLOCKED, "original_store_failed:" + type(exc).__name__)

    if not _same(observe, original_observe):
        return _hold(BLOCKED, "supplied_ObserveOS_not_original_stored_final")
    if not _same(verify, original_verify):
        return _hold(BLOCKED, "supplied_VerifyOS_not_original_stored_final")
    if observe.get("current_phase") != "commit":
        return _hold(NO_DATA, "ObserveOS_commit_not_observed")
    if verify.get("current_phase") != "commit":
        return _hold(NO_DATA, "VerifyOS_commit_not_observed")

    initial_edge = audit_handoff(*EDGE, observe, verify_genesis)
    if initial_edge.status == BLOCKED:
        return _hold(
            BLOCKED, "original_initial_Observe_Verify_edge:"
            + ";".join(initial_edge.issues),
        )
    if initial_edge.status != EDGE_PASS:
        return _hold(
            NO_DATA, "original_initial_Observe_Verify_edge:"
            + ";".join(initial_edge.issues),
        )

    native = audit_native_verify_from_observe(observe, verify)
    if native.status == BLOCKED:
        return _hold(
            BLOCKED, "original_final_VerifyOS:" + ";".join(native.issues),
        )
    if native.status != NATIVE_PASS:
        return _hold(
            NO_DATA, "original_final_VerifyOS:" + ";".join(native.issues),
        )
    if not (
        native.original_state_validated
        and native.original_edge_validated
        and native.source_bound_python_conditions_checked
    ):
        return _hold(NO_DATA, "original_final_VerifyOS_conditions_incomplete")
    if native.source_digest != _fingerprint(verify):
        return _hold(BLOCKED, "original_final_VerifyOS_digest_mismatch")

    contract = HANDOFF_CONTRACTS.get(EDGE)
    if contract is None:
        return _hold(NO_DATA, "registered_Observe_Verify_handoff_missing")
    for source_field, target_field in contract.equal_fields:
        if source_field not in observe or target_field not in verify_genesis:
            return _hold(NO_DATA, "typed_Observe_Verify_field_missing:" + target_field)
        if not _same(observe[source_field], verify_genesis[target_field]):
            return _hold(BLOCKED, "typed_Observe_Verify_source_mismatch:" + target_field)
        if target_field not in verify:
            return _hold(NO_DATA, "final_VerifyOS_field_missing:" + target_field)
        if not _same(verify_genesis[target_field], verify[target_field]):
            return _hold(BLOCKED, "VerifyOS_source_history_mismatch:" + target_field)

    # These conditions hold independently of the PASSED/FAILED/INDETERMINATE
    # verdict. Debt is adjudicated by the original VerifyOS kernel.
    if verify.get("verification_recorded") is not True:
        return _hold(NO_DATA, "original_verification_not_recorded")
    if verify.get("learning_required") is not True:
        return _hold(BLOCKED, "original_verification_learning_debt_missing")
    adjudication = verify.get("adjudication_receipt")
    if type(adjudication) is not dict or adjudication.get("verdict") not in (
        "PASSED", "FAILED", "INDETERMINATE",
    ):
        return _hold(BLOCKED, "original_adjudication_verdict_unavailable")

    # The two stores are separate; check that neither's file bytes changed
    # while auditing, without pretending to provide a global atomic snapshot.
    try:
        if (
            _store_files(observe_root, _OBSERVE_FILES) != observe_before
            or _store_files(verify_root, _VERIFY_FILES) != verify_before
        ):
            return _hold(BLOCKED, "original_store_changed_during_audit")
    except FileNotFoundError:
        return _hold(NO_DATA, "original_store_disappeared_during_audit")
    except (ValueError, OSError, RecursionError) as exc:
        return _hold(BLOCKED, "original_store_recheck_failed:" + type(exc).__name__)

    return NativeObserveVerifyStoreAudit(
        status=SCOPED_COMPATIBLE,
        original_observe_digest=_fingerprint(observe),
        original_verify_genesis_digest=_fingerprint(verify_genesis),
        original_verify_final_digest=_fingerprint(verify),
        adjudication_verdict=adjudication["verdict"],
        observe_commit_count=len(observe_commits),
        verify_commit_count=len(verify_commits),
        checked_source_paths=(
            "ObserveStore.observe-genesis.json",
            "ObserveStore.observe-ledger.jsonl",
            "ObserveStore.observe-snapshot.json",
            "VerifyStore.verify-genesis.json",
            "VerifyStore.verify-ledger.jsonl",
            "VerifyStore.verify-snapshot.json",
            "ObserveOS.comparison_receipt.comparison_receipt_digest",
            "VerifyOS.criterion_packet.criterion_packet_digest",
            "VerifyOS.challenge_packet.challenge_packet_digest",
            "VerifyOS.corroboration_report.corroboration_report_digest",
            "VerifyOS.adjudication_receipt.adjudication_receipt_digest",
            "VerifyOS.verification_debt_discharged",
            "VerifyOS.verification_required",
            "VerifyOS.reobservation_required",
            "VerifyOS.corrective_action_required",
            "VerifyOS.learning_required",
        ) + tuple(
            "ObserveOS." + a + "=VerifyOS." + b
            for a, b in contract.equal_fields
        ),
        observe_original_store_replayed=True,
        verify_original_store_replayed=True,
        original_observe_to_verify_genesis_edge_checked=True,
        original_final_verify_lean_data_checked=True,
    )


__all__ = (
    "VERSION", "SOURCE_PARENT", "SCOPED_COMPATIBLE", "NO_DATA", "BLOCKED",
    "NativeObserveVerifyStoreAudit",
    "audit_native_observe_verify_store_compatibility",
)
