"""KuuOS Lean→Python v0.34: actual Plan→Act genesis/commit source binding.

Use the original persisted ActStore genesis + full replayed ledger and
snapshot, not a synthetic initial Act state. The original Plan→initial
Act admission and the original final Act native authorization checker
retain distinct evidence scopes. In particular, numeric jobsClaimed and
slicesRun and external issuer authenticity remain UNPROVED.

Read-only local source audit; no store mutation, host invocation,
Lean proof construction, global descent, or execution authority.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from runtime.kuuos_act_os_store_v0_1 import ActStore, ActStoreError
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json, _fingerprint
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import _same
from runtime.kuuos_lean_python_plan_native_binding_v0_28 import (
    audit_native_plan_effect_guards,
)
from runtime.kuuos_lean_python_act_native_binding_v0_28 import (
    audit_native_act_authorization,
)
from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    PASS as NATIVE_PASS, BLOCKED, NO_DATA,
)
from runtime.kuuos_lean_python_plan_act_admission_v0_4 import (
    PASS as ADMISSION_PASS, audit_plan_act_admission,
)

VERSION = "kuuos_lean_python_plan_act_store_provenance_v0_34"
SOURCE_PARENT = "6f4e3b5f89ef7090839c76ffabdf409ee12adbf7"
SCOPED_COMPATIBLE = "SCOPED_PLAN_ACT_STORE_COMPATIBLE"
NUMERIC_AND_ISSUER_OBSTRUCTIONS = (
    "ActOS:actual_jobsClaimed_numeric_witness_unavailable",
    "ActOS:actual_slicesRun_numeric_witness_unavailable",
    "ActOS:original_activation_receipt_issuer_unverified",
)
_STORE_NAMES = ("act-genesis.json", "act-ledger.jsonl", "act-snapshot.json")
_MAX_FILE_BYTES = 16_000_000


@dataclass(frozen=True)
class NativePlanActStoreAudit:
    status: str
    issues: tuple[str, ...] = ()
    plan_digest: str | None = None
    activation_digest: str | None = None
    genesis_digest: str | None = None
    final_act_digest: str | None = None
    ledger_commit_count: int = 0
    checked_source_paths: tuple[str, ...] = ()
    original_plan_guard_checked: bool = False
    original_initial_admission_checked: bool = False
    original_act_ledger_replayed: bool = False
    original_final_act_local_conditions_checked: bool = False
    missing_lean_witnesses: tuple[str, ...] = ()
    whole_act_lean_conditions_certified: bool = False
    formal_descent_certified: bool = False
    global_gluing_proved: bool = False
    complete_lean_python_refinement_proved: bool = False
    external_activation_issuer_authenticated: bool = False
    actual_numeric_job_and_slice_counts_proved: bool = False
    execution_authority_granted: bool = False
    host_license_granted: bool = False
    truth_authority_granted: bool = False
    git_authority_granted: bool = False
    original_store_mutated: bool = False


def _hold(status: str, reason: str) -> NativePlanActStoreAudit:
    return NativePlanActStoreAudit(status=status, issues=(reason,))


def _packet(value: Any, name: str) -> dict[str, Any]:
    if type(value) is not dict:
        raise TypeError(name + ":built_in_dict_required")
    try:
        copied = _finite_json(value)
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError) as exc:
        raise ValueError(name + ":invalid_finite_json:" + type(exc).__name__) from exc
    if type(copied) is not dict:
        raise ValueError(name + ":object_not_preserved")
    return copied


def _read_store_bytes(root: Path) -> dict[str, bytes]:
    # Missing input is NOT a contradicting source. Symlinks are not
    # ordinary native files and cannot be silently trusted.
    if not root.is_dir():
        raise FileNotFoundError("original_ActStore_root_missing")
    if root.is_symlink():
        raise ValueError("original_ActStore_root_symlink_forbidden")
    observed = {}
    for name in _STORE_NAMES:
        path = root / name
        if path.is_symlink():
            raise ValueError("original_ActStore_symlink_forbidden:" + name)
        if not path.is_file():
            raise FileNotFoundError("original_ActStore_file_missing:" + name)
        if path.stat().st_size > _MAX_FILE_BYTES:
            raise ValueError("original_ActStore_file_too_large:" + name)
        observed[name] = path.read_bytes()
    return observed


def audit_native_plan_act_store_compatibility(
    plan_state: Any,
    activation_receipt: Any,
    final_act_state: Any,
    original_act_store_root: Any,
) -> NativePlanActStoreAudit:
    """Read-only provenance consistency, NEVER execution or proof transfer."""
    for name, value in (
        ("plan", plan_state), ("activation", activation_receipt),
        ("final_act", final_act_state), ("ActStore_root", original_act_store_root),
    ):
        if value is None:
            return _hold(NO_DATA, name + ":original_source_missing")
    try:
        plan = _packet(plan_state, "plan")
        receipt = _packet(activation_receipt, "activation")
        final = _packet(final_act_state, "final_act")
        if type(original_act_store_root) is not str and not isinstance(
            original_act_store_root, Path
        ):
            return _hold(BLOCKED, "ActStore_root:trusted_path_type_required")
        root = Path(original_act_store_root)
        before = _read_store_bytes(root)
        store = ActStore(root)
        genesis = store._read_json(store.genesis_path)
        recovered, commits = store._recover_unlocked()
        snapshot = store._read_json(store.snapshot_path)
        after = _read_store_bytes(root)
    except FileNotFoundError:
        return _hold(NO_DATA, "original_ActStore_incomplete")
    except (ActStoreError, ValueError, TypeError, OSError, RecursionError) as exc:
        return _hold(BLOCKED, "original_ActStore_invalid:" + type(exc).__name__)
    if before != after:
        return _hold(BLOCKED, "original_ActStore_changed_during_read_only_audit")
    if not _same(snapshot, recovered):
        return _hold(BLOCKED, "original_ActStore_snapshot_not_exact_replay")
    if not _same(final, recovered):
        return _hold(BLOCKED, "supplied_final_ActOS_not_exact_store_replay")
    if recovered.get("current_phase") != "commit" or not commits:
        return _hold(NO_DATA, "original_ActOS_final_commit_unobserved")
    if any(type(row.get("commit_index")) is not int or row["commit_index"] != i
           for i, row in enumerate(commits, 1)):
        return _hold(BLOCKED, "original_ActStore_commit_index_inconsistent")

    # Both native snapshots are separately validated; it is not enough
    # to match hash strings or an unvalidated receipt.
    plan_check = audit_native_plan_effect_guards(plan)
    if plan_check.status == BLOCKED:
        return _hold(BLOCKED, "original_PlanOS:" + ";".join(plan_check.issues))
    if plan_check.status != NATIVE_PASS:
        return _hold(NO_DATA, "original_PlanOS:" + ";".join(plan_check.issues))

    admission = audit_plan_act_admission(plan, receipt, genesis)
    if admission.status == BLOCKED:
        return _hold(BLOCKED, "original_Plan_Act_initial_admission:"
                     + ";".join(admission.violations))
    if admission.status != ADMISSION_PASS or not admission.runtime_checked:
        return _hold(NO_DATA, "original_Plan_Act_initial_admission:"
                     + ";".join(admission.missing))

    final_check = audit_native_act_authorization(plan, recovered)
    if final_check.status == BLOCKED:
        return _hold(BLOCKED, "original_ActOS:" + ";".join(final_check.issues))
    if final_check.status != NO_DATA or not final_check.original_state_validated:
        return _hold(NO_DATA, "original_ActOS_source_scope_unverified")
    if tuple(final_check.issues) != NUMERIC_AND_ISSUER_OBSTRUCTIONS:
        return _hold(NO_DATA, "original_ActOS_missing_witness_scope_changed")
    if not _same(genesis.get("plan_activation_receipt_digest"),
                 receipt.get("plan_activation_receipt_digest")):
        return _hold(BLOCKED, "original_genesis_activation_digest_mismatch")
    if not _same(final.get("plan_activation_receipt_digest"),
                 receipt.get("plan_activation_receipt_digest")):
        return _hold(BLOCKED, "final_ActOS_activation_digest_mismatch")

    return NativePlanActStoreAudit(
        status=SCOPED_COMPATIBLE,
        plan_digest=_fingerprint(plan),
        activation_digest=_fingerprint(receipt),
        genesis_digest=_fingerprint(genesis),
        final_act_digest=_fingerprint(final),
        ledger_commit_count=len(commits),
        checked_source_paths=(
            "PlanOS.plan_state_digest",
            "PlanOS.steps[*].step_digest",
            "PlanOS.guard_summary",
            "activation_receipt.plan_activation_receipt_digest",
            "ActStore.act-genesis.json",
            "ActStore.act-ledger.jsonl",
            "ActStore.act-snapshot.json",
            "ActOS.source_plan_state_digest",
            "ActOS.selected_step_id",
            "ActOS.step_authorization",
            "ActOS.host_license",
            "ActOS.host_receipt",
            "ActOS.event_history[target_phase=authorize]",
        ),
        original_plan_guard_checked=True,
        original_initial_admission_checked=True,
        original_act_ledger_replayed=True,
        original_final_act_local_conditions_checked=True,
        missing_lean_witnesses=NUMERIC_AND_ISSUER_OBSTRUCTIONS,
    )


__all__ = (
    "VERSION", "SOURCE_PARENT", "SCOPED_COMPATIBLE", "NO_DATA", "BLOCKED",
    "NUMERIC_AND_ISSUER_OBSTRUCTIONS", "NativePlanActStoreAudit",
    "audit_native_plan_act_store_compatibility",
)
