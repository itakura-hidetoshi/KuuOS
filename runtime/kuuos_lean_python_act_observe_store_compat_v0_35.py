"""KuuOS Lean→Python v0.35 — original ActOS→ObserveOS persisted typed handoff.

This is read-only local compatibility of two independently original
file-backed OS stores and their source-target Lean data conditions.
An observation does not verify an effect, establish external evidence
authenticity, prove CPython semantics or global Lean descent, or grant
host/truth/execution/clinical/repository authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from runtime.kuuos_act_os_store_v0_1 import ActStore, ActStoreError
from runtime.kuuos_observe_os_store_v0_1 import ObserveStore, ObserveStoreError
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json, _fingerprint
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import _same
from runtime.kuuos_lean_python_lineage_handoff_v0_2 import (
    HANDOFF_CONTRACTS, audit_handoff,
)
from runtime.kuuos_lean_python_observe_native_binding_v0_28 import (
    audit_native_observe_from_act,
)
from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    PASS as NATIVE_PASS, NO_DATA, BLOCKED,
)
from runtime.kuuos_lean_python_contract_bridge_v0_1 import PASSED as EDGE_PASS

VERSION = "kuuos_lean_python_act_observe_store_compat_v0_35"
SOURCE_PARENT = "b782f5a34607ff645e7bccb9d8934b38301517a1"
SCOPED_COMPATIBLE = "SCOPED_ACT_OBSERVE_STORE_COMPATIBLE"
EDGE = ("ActOS", "ObserveOS")
_MAX_FILE_BYTES = 16_000_000
_SPEC = (
    ("ActOS", ActStore, ("act-genesis.json", "act-ledger.jsonl", "act-snapshot.json")),
    ("ObserveOS", ObserveStore,
     ("observe-genesis.json", "observe-ledger.jsonl", "observe-snapshot.json")),
)


@dataclass(frozen=True)
class NativeActObserveStoreAudit:
    status: str
    issues: tuple[str, ...] = ()
    original_act_digest: str | None = None
    original_observe_genesis_digest: str | None = None
    original_observe_final_digest: str | None = None
    act_commit_count: int = 0
    observe_commit_count: int = 0
    checked_source_paths: tuple[str, ...] = ()
    act_original_store_replayed: bool = False
    observe_original_store_replayed: bool = False
    original_act_to_observe_genesis_edge_checked: bool = False
    original_final_observe_lean_data_checked: bool = False
    act_jobs_claimed_numeric_witness_proved: bool = False
    act_slices_run_numeric_witness_proved: bool = False
    external_receipt_authenticated: bool = False
    observation_is_verification: bool = False
    observation_grants_truth: bool = False
    whole_program_lean_python_refinement_proved: bool = False
    global_descent_proved: bool = False
    execution_authority_granted: bool = False
    host_license_granted: bool = False
    git_authority_granted: bool = False
    original_store_mutated: bool = False


def _hold(status: str, reason: str) -> NativeActObserveStoreAudit:
    return NativeActObserveStoreAudit(status=status, issues=(reason,))


def _packet(value: Any, label: str) -> dict:
    if type(value) is not dict:
        raise TypeError(label + ":plain_json_object_required")
    try:
        copied = _finite_json(value)
    except (TypeError, ValueError, UnicodeError, OverflowError, RecursionError) as exc:
        raise ValueError(label + ":invalid_json:" + type(exc).__name__) from exc
    if type(copied) is not dict:
        raise ValueError(label + ":json_object_not_preserved")
    return copied


def _store_files(root: Path, names: tuple[str, ...]) -> dict[str, bytes]:
    if root.is_symlink():
        raise ValueError("store_root_symlink_forbidden")
    if not root.is_dir():
        raise FileNotFoundError("original_store_directory_missing")
    files = {}
    for name in names:
        path = root / name
        if path.is_symlink():
            raise ValueError("store_file_symlink_forbidden:" + name)
        if not path.is_file():
            raise FileNotFoundError("original_store_file_missing:" + name)
        if path.stat().st_size > _MAX_FILE_BYTES:
            raise ValueError("store_file_too_large:" + name)
        files[name] = path.read_bytes()
    return files


def _native_store(root: Path, store_type: type, names: tuple[str, ...]):
    before = _store_files(root, names)
    native = store_type(root)
    genesis = native._read_json(native.genesis_path)
    # Original append-only replay, NOT a host call or store mutation.
    final, commits = native._recover_unlocked()
    snapshot = native._read_json(native.snapshot_path)
    after = _store_files(root, names)
    if before != after:
        raise ValueError("original_store_bytes_changed")
    if not _same(snapshot, final):
        raise ValueError("original_store_snapshot_replay_mismatch")
    if not commits:
        raise FileNotFoundError("original_store_commits_not_observed")
    if any(type(c.get("commit_index")) is not int or c["commit_index"] != i
           for i, c in enumerate(commits, 1)):
        raise ValueError("original_store_commit_indices_not_exact")
    return genesis, final, commits


def audit_native_act_observe_store_compatibility(
    act_state: Any,
    observe_state: Any,
    original_act_store_root: Any,
    original_observe_store_root: Any,
) -> NativeActObserveStoreAudit:
    """Check only existing native, registered, source-identical relations."""
    for label, value in (
        ("ActOS", act_state),
        ("ObserveOS", observe_state),
        ("ActStore", original_act_store_root),
        ("ObserveStore", original_observe_store_root),
    ):
        if value is None:
            return _hold(NO_DATA, label + ":source_missing")
    try:
        act = _packet(act_state, "ActOS")
        observe = _packet(observe_state, "ObserveOS")
        if not all(type(v) is str or type(v) is Path
                   for v in (original_act_store_root, original_observe_store_root)):
            return _hold(BLOCKED, "trusted_store_paths_required")
        act_root = Path(original_act_store_root)
        obs_root = Path(original_observe_store_root)
        if act_root.resolve() == obs_root.resolve():
            return _hold(BLOCKED, "ActOS_ObserveOS_roots_must_be_distinct")
        act_genesis, act_original, act_commits = _native_store(
            act_root, _SPEC[0][1], _SPEC[0][2]
        )
        observe_genesis, observe_original, observe_commits = _native_store(
            obs_root, _SPEC[1][1], _SPEC[1][2]
        )
    except FileNotFoundError:
        return _hold(NO_DATA, "original_store_missing_or_uncommitted")
    except (TypeError, ValueError, OSError, RecursionError,
            ActStoreError, ObserveStoreError) as exc:
        return _hold(BLOCKED, "original_store_failed:" + type(exc).__name__)

    if not _same(act, act_original):
        return _hold(BLOCKED, "supplied_ActOS_not_original_stored_final")
    if not _same(observe, observe_original):
        return _hold(BLOCKED, "supplied_ObserveOS_not_original_stored_final")
    if act.get("current_phase") != "commit":
        return _hold(NO_DATA, "ActOS_commit_not_observed")
    if observe.get("current_phase") != "commit":
        return _hold(NO_DATA, "ObserveOS_commit_not_observed")

    # The original source->initial-Observe edge is the missing local
    # compatibility witness; checking only the final Observe is insufficient.
    initial_edge = audit_handoff(*EDGE, act, observe_genesis)
    if initial_edge.status == BLOCKED:
        return _hold(BLOCKED, "original_initial_Act_Observe_edge:"
                     + ";".join(initial_edge.issues))
    if initial_edge.status != EDGE_PASS:
        return _hold(NO_DATA, "original_initial_Act_Observe_edge:"
                     + ";".join(initial_edge.issues))

    final_observation = audit_native_observe_from_act(act, observe)
    if final_observation.status == BLOCKED:
        return _hold(BLOCKED, "original_final_ObserveOS:"
                     + ";".join(final_observation.issues))
    if final_observation.status != NATIVE_PASS:
        return _hold(NO_DATA, "original_final_ObserveOS:"
                     + ";".join(final_observation.issues))
    if not (final_observation.original_state_validated
            and final_observation.original_edge_validated
            and final_observation.source_bound_python_conditions_checked):
        return _hold(NO_DATA, "original_final_ObserveOS_conditions_incomplete")
    if final_observation.source_digest != _fingerprint(observe):
        return _hold(BLOCKED, "original_final_ObserveOS_digest_mismatch")

    contract = HANDOFF_CONTRACTS.get(EDGE)
    if contract is None:
        return _hold(NO_DATA, "registered_Act_Observe_handoff_missing")
    for source_field, target_field in contract.equal_fields:
        if source_field not in act or target_field not in observe_genesis:
            return _hold(NO_DATA, "typed_Act_Observe_field_missing:" + target_field)
        if not _same(act[source_field], observe_genesis[target_field]):
            return _hold(BLOCKED, "typed_Act_Observe_source_mismatch:" + target_field)
        if target_field not in observe:
            return _hold(NO_DATA, "final_ObserveOS_field_missing:" + target_field)
        if not _same(observe_genesis[target_field], observe[target_field]):
            return _hold(BLOCKED, "ObserveOS_source_history_mismatch:" + target_field)

    # A local source match proves neither host execution counters nor
    # external authenticity. The previous v0.34 Act numeric obstruction stands.
    return NativeActObserveStoreAudit(
        status=SCOPED_COMPATIBLE,
        original_act_digest=_fingerprint(act),
        original_observe_genesis_digest=_fingerprint(observe_genesis),
        original_observe_final_digest=_fingerprint(observe),
        act_commit_count=len(act_commits),
        observe_commit_count=len(observe_commits),
        checked_source_paths=(
            "ActStore.act-genesis.json",
            "ActStore.act-ledger.jsonl",
            "ActStore.act-snapshot.json",
            "ObserveStore.observe-genesis.json",
            "ObserveStore.observe-ledger.jsonl",
            "ObserveStore.observe-snapshot.json",
            "ActOS.host_receipt.host_receipt_digest",
            "ObserveOS.comparison_receipt.comparison_receipt_digest",
            "ObserveOS.observation_debt_discharged",
            "ObserveOS.verification_required",
        ) + tuple(
            "ActOS." + a + "=ObserveOS." + b
            for a, b in contract.equal_fields
        ),
        act_original_store_replayed=True,
        observe_original_store_replayed=True,
        original_act_to_observe_genesis_edge_checked=True,
        original_final_observe_lean_data_checked=True,
    )


__all__ = (
    "VERSION", "SOURCE_PARENT", "SCOPED_COMPATIBLE", "NO_DATA",
    "BLOCKED", "NativeActObserveStoreAudit",
    "audit_native_act_observe_store_compatibility",
)
