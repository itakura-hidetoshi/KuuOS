"""Lean→Python v0.37: original persisted VerifyOS→LearnOS compatibility.

Read-only replay of the two ORIGINAL file-backed stores, with the
committed VerifyOS final state bound to the INITIAL LearnOS genesis
and the original FINAL LearnOS future-only / evidence-bound obligations.
No claim of Lean→Python refinement, global gluing, external authenticity,
reality/truth, memory rewriting, policy activation or execution authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from runtime.kuuos_verify_os_store_v0_1 import VerifyStore, VerifyStoreError
from runtime.kuuos_learn_os_store_v0_1 import LearnStore, LearnStoreError
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_learn_os_kernel_v0_1 import (
    ALLOWED_KIND_BY_VERIFY_ROUTE, ROUTE_BY_KIND,
)
from runtime.kuuos_lean_python_act_observe_store_compat_v0_35 import (
    _native_store, _packet, _store_files,
)
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import _same
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from runtime.kuuos_lean_python_lineage_handoff_v0_2 import (
    HANDOFF_CONTRACTS, audit_handoff,
)
from runtime.kuuos_lean_python_learn_native_binding_v0_28 import (
    audit_native_learn_from_verify,
)
from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    PASS as NATIVE_PASS, NO_DATA, BLOCKED,
)
from runtime.kuuos_lean_python_contract_bridge_v0_1 import PASSED as EDGE_PASS

VERSION = "kuuos_lean_python_verify_learn_store_compat_v0_37"
SOURCE_PARENT = "6672365b1bba5739d7fd1b30a250395647d46c89"
SCOPED_COMPATIBLE = "SCOPED_VERIFY_LEARN_STORE_COMPATIBLE"
EDGE = ("VerifyOS", "LearnOS")
_VERIFY_FILES = ("verify-genesis.json", "verify-ledger.jsonl", "verify-snapshot.json")
_LEARN_FILES = ("learn-genesis.json", "learn-ledger.jsonl", "learn-snapshot.json")


@dataclass(frozen=True)
class NativeVerifyLearnStoreAudit:
    status: str
    issues: tuple[str, ...] = ()
    original_verify_digest: str | None = None
    original_learn_genesis_digest: str | None = None
    original_learn_final_digest: str | None = None
    verification_verdict: str | None = None
    learning_route: str | None = None
    learning_kind: str | None = None
    verify_commit_count: int = 0
    learn_commit_count: int = 0
    checked_source_paths: tuple[str, ...] = ()
    verify_original_store_replayed: bool = False
    learn_original_store_replayed: bool = False
    original_verify_to_learn_genesis_edge_checked: bool = False
    original_final_learn_lean_data_checked: bool = False
    external_receipt_authenticated: bool = False
    learning_is_truth: bool = False
    learning_grants_causality: bool = False
    memory_overwrite_authority_granted: bool = False
    learning_activated_now: bool = False
    whole_program_lean_python_refinement_proved: bool = False
    global_descent_proved: bool = False
    clinical_authority_granted: bool = False
    execution_authority_granted: bool = False
    host_license_granted: bool = False
    git_authority_granted: bool = False
    original_store_mutated: bool = False


def _hold(status: str, reason: str) -> NativeVerifyLearnStoreAudit:
    return NativeVerifyLearnStoreAudit(status=status, issues=(reason,))


def audit_native_verify_learn_store_compatibility(
    verify_state: Any,
    learn_state: Any,
    original_verify_store_root: Any,
    original_learn_store_root: Any,
) -> NativeVerifyLearnStoreAudit:
    """Check exactly existing original Verify→Learn saved source relations.

    No self-generated evidence, no host call or store write. Individual
    store byte stability does NOT certify a globally atomic observation.
    """
    for label, value in (
        ("VerifyOS", verify_state),
        ("LearnOS", learn_state),
        ("VerifyStore", original_verify_store_root),
        ("LearnStore", original_learn_store_root),
    ):
        if value is None:
            return _hold(NO_DATA, label + ":source_missing")
    try:
        verify = _packet(verify_state, "VerifyOS")
        learn = _packet(learn_state, "LearnOS")
        if not all(
            type(root) is str or isinstance(root, Path)
            for root in (original_verify_store_root, original_learn_store_root)
        ):
            return _hold(BLOCKED, "trusted_store_paths_required")
        verify_root = Path(original_verify_store_root)
        learn_root = Path(original_learn_store_root)
        if verify_root.resolve() == learn_root.resolve():
            return _hold(BLOCKED, "VerifyOS_LearnOS_roots_must_be_distinct")
        verify_before = _store_files(verify_root, _VERIFY_FILES)
        learn_before = _store_files(learn_root, _LEARN_FILES)
        _, original_verify, verify_commits = _native_store(
            verify_root, VerifyStore, _VERIFY_FILES
        )
        learn_genesis, original_learn, learn_commits = _native_store(
            learn_root, LearnStore, _LEARN_FILES
        )
    except FileNotFoundError:
        return _hold(NO_DATA, "original_store_missing_or_uncommitted")
    except (
        TypeError, ValueError, OSError, RecursionError,
        VerifyStoreError, LearnStoreError,
    ) as exc:
        return _hold(BLOCKED, "original_store_failed:" + type(exc).__name__)

    if not _same(verify, original_verify):
        return _hold(BLOCKED, "supplied_VerifyOS_not_original_stored_final")
    if not _same(learn, original_learn):
        return _hold(BLOCKED, "supplied_LearnOS_not_original_stored_final")
    if verify.get("current_phase") != "commit":
        return _hold(NO_DATA, "VerifyOS_commit_not_observed")
    if learn.get("current_phase") != "commit":
        return _hold(NO_DATA, "LearnOS_commit_not_observed")

    initial_edge = audit_handoff(*EDGE, verify, learn_genesis)
    if initial_edge.status == BLOCKED:
        return _hold(BLOCKED, "original_initial_Verify_Learn_edge:"
                     + ";".join(initial_edge.issues))
    if initial_edge.status != EDGE_PASS:
        return _hold(NO_DATA, "original_initial_Verify_Learn_edge:"
                     + ";".join(initial_edge.issues))

    native = audit_native_learn_from_verify(verify, learn)
    if native.status == BLOCKED:
        return _hold(BLOCKED, "original_final_LearnOS:" + ";".join(native.issues))
    if native.status != NATIVE_PASS:
        return _hold(NO_DATA, "original_final_LearnOS:" + ";".join(native.issues))
    if not (
        native.original_state_validated
        and native.original_edge_validated
        and native.source_bound_python_conditions_checked
    ):
        return _hold(NO_DATA, "original_final_LearnOS_conditions_incomplete")
    if native.source_digest != _fingerprint(learn):
        return _hold(BLOCKED, "original_final_LearnOS_digest_mismatch")

    contract = HANDOFF_CONTRACTS.get(EDGE)
    if contract is None:
        return _hold(NO_DATA, "registered_Verify_Learn_handoff_missing")
    for source_field, target_field in contract.equal_fields:
        if source_field not in verify or target_field not in learn_genesis:
            return _hold(NO_DATA, "typed_Verify_Learn_field_missing:" + target_field)
        if not _same(verify[source_field], learn_genesis[target_field]):
            return _hold(BLOCKED, "typed_Verify_Learn_source_mismatch:" + target_field)
        if target_field not in learn:
            return _hold(NO_DATA, "final_LearnOS_field_missing:" + target_field)
        if not _same(learn_genesis[target_field], learn[target_field]):
            return _hold(BLOCKED, "LearnOS_source_history_mismatch:" + target_field)

    # The formal VerifySourceBinding does not erase counterevidence:
    # check real Verify challenge and both original Learn states, in addition
    # to the existing typed edge fields and original replayed OS kernel.
    challenge = verify.get("challenge_packet")
    corroboration = verify.get("corroboration_report")
    if type(challenge) is not dict or type(corroboration) is not dict:
        return _hold(NO_DATA, "original_verification_evidence_not_present")
    if "counterevidence_digests" not in challenge or "unresolved_conflict" not in corroboration:
        return _hold(NO_DATA, "original_counterevidence_or_conflict_missing")
    counterevidence = challenge["counterevidence_digests"]
    if type(counterevidence) is not list:
        return _hold(BLOCKED, "counterevidence_type_mismatch")
    for stage, value in (("genesis", learn_genesis), ("final", learn)):
        if "source_counterevidence_digests" not in value:
            return _hold(NO_DATA, "LearnOS_" + stage + "_counterevidence_missing")
        if not _same(value["source_counterevidence_digests"], counterevidence):
            return _hold(BLOCKED, "LearnOS_" + stage + "_counterevidence_mismatch")
        if not _same(value.get("source_counterevidence_digest"), sha(counterevidence)):
            return _hold(BLOCKED, "LearnOS_" + stage + "_counterevidence_digest_mismatch")
        if not _same(value.get("source_unresolved_conflict"), corroboration["unresolved_conflict"]):
            return _hold(BLOCKED, "LearnOS_" + stage + "_conflict_history_mismatch")

    delta = learn.get("learning_delta")
    gate = learn.get("middle_way_report")
    if type(delta) is not dict or type(gate) is not dict:
        return _hold(NO_DATA, "original_learning_delta_or_gate_missing")
    kind = delta.get("learning_kind")
    verify_route = verify.get("route")
    if kind not in ALLOWED_KIND_BY_VERIFY_ROUTE.get(verify_route, set()):
        return _hold(BLOCKED, "original_learning_kind_incompatible")
    expected_route = (
        ROUTE_BY_KIND[kind]
        if kind == "hold" or gate.get("candidate_admissible") is True
        else "LEARNING_HOLD"
    )
    if learn.get("route") != expected_route:
        return _hold(BLOCKED, "original_learning_route_inconsistent")
    for field in (
        "learning_recorded", "learning_debt_discharged", "replan_required",
        "current_cycle_unchanged", "past_records_unchanged",
    ):
        if learn.get(field) is not True:
            return _hold(BLOCKED, "original_learning_commit_condition_missing:" + field)
    if learn.get("active_now") is not False:
        return _hold(BLOCKED, "original_learning_activated_without_replan")
    if (
        delta.get("future_only") is not True
        or delta.get("memory_overwrite") is not False
        or delta.get("active_now") is not False
        or delta.get("activation_requires_replan") is not True
    ):
        return _hold(BLOCKED, "original_learning_delta_violates_future_only")

    try:
        if (
            _store_files(verify_root, _VERIFY_FILES) != verify_before
            or _store_files(learn_root, _LEARN_FILES) != learn_before
        ):
            return _hold(BLOCKED, "original_store_changed_during_audit")
    except FileNotFoundError:
        return _hold(NO_DATA, "original_store_disappeared_during_audit")
    except (ValueError, OSError, RecursionError) as exc:
        return _hold(BLOCKED, "original_store_recheck_failed:" + type(exc).__name__)

    return NativeVerifyLearnStoreAudit(
        status=SCOPED_COMPATIBLE,
        original_verify_digest=_fingerprint(verify),
        original_learn_genesis_digest=_fingerprint(learn_genesis),
        original_learn_final_digest=_fingerprint(learn),
        verification_verdict=str(verify["adjudication_receipt"]["verdict"]),
        learning_route=str(learn["route"]),
        learning_kind=str(kind),
        verify_commit_count=len(verify_commits),
        learn_commit_count=len(learn_commits),
        checked_source_paths=(
            "VerifyStore.verify-genesis.json",
            "VerifyStore.verify-ledger.jsonl",
            "VerifyStore.verify-snapshot.json",
            "LearnStore.learn-genesis.json",
            "LearnStore.learn-ledger.jsonl",
            "LearnStore.learn-snapshot.json",
            "VerifyOS.challenge_packet.counterevidence_digests",
            "VerifyOS.corroboration_report.unresolved_conflict",
            "LearnOS.source_counterevidence_digests",
            "LearnOS.source_unresolved_conflict",
            "LearnOS.learning_delta.future_only",
            "LearnOS.learning_delta.memory_overwrite",
            "LearnOS.learning_delta.activation_requires_replan",
            "LearnOS.middle_way_report.candidate_admissible",
            "LearnOS.learning_debt_discharged",
            "LearnOS.replan_required",
            "LearnOS.active_now",
        ) + tuple(
            "VerifyOS." + a + "=LearnOS." + b
            for a, b in contract.equal_fields
        ),
        verify_original_store_replayed=True,
        learn_original_store_replayed=True,
        original_verify_to_learn_genesis_edge_checked=True,
        original_final_learn_lean_data_checked=True,
    )


__all__ = (
    "VERSION", "SOURCE_PARENT", "SCOPED_COMPATIBLE", "NO_DATA",
    "BLOCKED", "NativeVerifyLearnStoreAudit",
    "audit_native_verify_learn_store_compatibility",
)
