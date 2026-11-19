"""KuuOS Lean→Python v0.38: five original persisted OS stores, four typed edges.

This is a bounded, read-only compatibility audit for the *same supplied*
PlanOS→ActOS→ObserveOS→VerifyOS→LearnOS native history. The four original
v0.34–v0.37 adapters are invoked, plus a fresh original PlanStore replay,
a typed five-node path audit and 15-file before/after comparison.
Passing local checks does not establish global descent, externally
authenticated receipts, Lean/Python semantic refinement, or authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from runtime.kuuos_plan_os_store_v0_1 import PlanStore, PlanStoreError
from runtime.kuuos_lean_python_act_observe_store_compat_v0_35 import (
    _native_store, _packet, _store_files,
)
from runtime.kuuos_lean_python_plan_act_store_provenance_v0_34 import (
    NUMERIC_AND_ISSUER_OBSTRUCTIONS,
    SCOPED_COMPATIBLE as PLAN_ACT_PASS,
    audit_native_plan_act_store_compatibility,
)
from runtime.kuuos_lean_python_act_observe_store_compat_v0_35 import (
    SCOPED_COMPATIBLE as ACT_OBSERVE_PASS,
    audit_native_act_observe_store_compatibility,
)
from runtime.kuuos_lean_python_observe_verify_store_compat_v0_36 import (
    SCOPED_COMPATIBLE as OBSERVE_VERIFY_PASS,
    audit_native_observe_verify_store_compatibility,
)
from runtime.kuuos_lean_python_verify_learn_store_compat_v0_37 import (
    SCOPED_COMPATIBLE as VERIFY_LEARN_PASS,
    audit_native_verify_learn_store_compatibility,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import (
    PASS as TYPED_PATH_PASS, audit_typed_path, _fingerprint,
)
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import _same
from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    NO_DATA, BLOCKED,
)

VERSION = "kuuos_lean_python_five_store_chain_compat_v0_38"
SOURCE_PARENT = "d0340d150312696b508595d9c24a864c0f7bae11"
SCOPED_COMPATIBLE = "SCOPED_FIVE_STORE_CHAIN_COMPATIBLE"
NODES = ("PlanOS", "ActOS", "ObserveOS", "VerifyOS", "LearnOS")
EDGES = ("PlanOS->ActOS", "ActOS->ObserveOS",
         "ObserveOS->VerifyOS", "VerifyOS->LearnOS")
_STORE_FILES = {
    name: (stem + "-genesis.json", stem + "-ledger.jsonl",
           stem + "-snapshot.json")
    for name, stem in (
        ("PlanOS", "plan"), ("ActOS", "act"),
        ("ObserveOS", "observe"), ("VerifyOS", "verify"),
        ("LearnOS", "learn"),
    )
}
_EXPECTED_EDGE_STATUSES = (
    PLAN_ACT_PASS, ACT_OBSERVE_PASS, OBSERVE_VERIFY_PASS, VERIFY_LEARN_PASS,
)


@dataclass(frozen=True)
class FiveStoreChainAudit:
    status: str
    issues: tuple[str, ...] = ()
    edge_statuses: tuple[tuple[str, str], ...] = ()
    persisted_store_commit_counts: tuple[tuple[str, int], ...] = ()
    final_native_state_digests: tuple[tuple[str, str], ...] = ()
    checked_original_store_paths: tuple[str, ...] = ()
    path_audit_status: str | None = None
    numeric_and_issuer_obstructions: tuple[str, ...] = NUMERIC_AND_ISSUER_OBSTRUCTIONS
    five_stores_individually_replayed: bool = False
    four_original_typed_edges_checked: bool = False
    full_native_path_local_conditions_checked: bool = False
    store_bytes_stable_during_audit: bool = False
    external_activation_issuer_authenticated: bool = False
    actual_act_numeric_witnesses_proved: bool = False
    external_receipt_authenticated: bool = False
    global_atomic_snapshot_proved: bool = False
    formal_global_descent_proved: bool = False
    lean_python_semantic_refinement_proved: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    causal_authority_granted: bool = False
    clinical_authority_granted: bool = False
    git_authority_granted: bool = False
    memory_overwrite_authority_granted: bool = False
    future_learning_activated_now: bool = False
    original_store_mutated: bool = False


def _hold(status: str, *issues: str) -> FiveStoreChainAudit:
    return FiveStoreChainAudit(status=status, issues=tuple(issues))


def audit_native_five_store_chain_compatibility(
    states: Any,
    plan_activation_receipt: Any,
    original_store_roots: Any,
) -> FiveStoreChainAudit:
    """Join only *observed* exact native snapshots, receipts and stores.

    Root identities and supplied state objects are kept fixed across all
    edges. BLOCKED dominates NO_DATA, which dominates scoped success.
    The result never grants authority or a Lean proof term.
    """
    if states is None or plan_activation_receipt is None or original_store_roots is None:
        return _hold(NO_DATA, "five_store_chain:input_missing")
    if type(states) is not dict or type(original_store_roots) is not dict:
        return _hold(BLOCKED, "five_store_chain:plain_named_objects_required")
    if set(states).difference(NODES) or set(original_store_roots).difference(NODES):
        return _hold(BLOCKED, "five_store_chain:unexpected_named_os")
    missing = tuple("five_store_chain:missing:" + name
                    for name in NODES
                    if states.get(name) is None or original_store_roots.get(name) is None)
    if missing:
        return _hold(NO_DATA, *missing)
    if any(type(original_store_roots[name]) is not str and
           type(original_store_roots[name]) is not type(Path())
           for name in NODES):
        return _hold(BLOCKED, "five_store_chain:untrusted_root_type")

    try:
        snapshots = {name: _packet(states[name], name) for name in NODES}
        activation = _packet(plan_activation_receipt, "Plan_activation")
        roots = {name: Path(original_store_roots[name]) for name in NODES}
        # A repeated root cannot stand for two independently original stores.
        if len({root.resolve() for root in roots.values()}) != len(NODES):
            return _hold(BLOCKED, "five_store_chain:store_roots_not_distinct")
        before = {name: _store_files(roots[name], _STORE_FILES[name])
                  for name in NODES}
        plan_genesis, plan_final, plan_commits = _native_store(
            roots["PlanOS"], PlanStore, _STORE_FILES["PlanOS"]
        )
    except FileNotFoundError:
        return _hold(NO_DATA, "five_store_chain:original_store_missing")
    except (TypeError, ValueError, OSError, RecursionError, PlanStoreError) as exc:
        return _hold(BLOCKED, "five_store_chain:original_store_invalid:"
                     + type(exc).__name__)

    if not _same(plan_final, snapshots["PlanOS"]):
        return _hold(BLOCKED, "five_store_chain:PlanOS_not_original_final")
    if plan_final.get("current_phase") != "commit":
        return _hold(NO_DATA, "five_store_chain:PlanOS_commit_missing")
    if any(type(c.get("commit_index")) is not int or
           c["commit_index"] != i for i, c in enumerate(plan_commits, 1)):
        return _hold(BLOCKED, "five_store_chain:PlanOS_commit_indices_invalid")
    if not _same(plan_genesis.get("lineage_id"), plan_final.get("lineage_id")):
        return _hold(BLOCKED, "five_store_chain:PlanOS_lineage_changed")

    edge_audits = (
        audit_native_plan_act_store_compatibility(
            snapshots["PlanOS"], activation, snapshots["ActOS"], roots["ActOS"]
        ),
        audit_native_act_observe_store_compatibility(
            snapshots["ActOS"], snapshots["ObserveOS"],
            roots["ActOS"], roots["ObserveOS"]
        ),
        audit_native_observe_verify_store_compatibility(
            snapshots["ObserveOS"], snapshots["VerifyOS"],
            roots["ObserveOS"], roots["VerifyOS"]
        ),
        audit_native_verify_learn_store_compatibility(
            snapshots["VerifyOS"], snapshots["LearnOS"],
            roots["VerifyOS"], roots["LearnOS"]
        ),
    )
    path = audit_typed_path(
        snapshots, receipts={"PlanOS->ActOS": activation},
        start="PlanOS", end="LearnOS",
    )
    failures: list[str] = []
    absent: list[str] = []
    for edge, expected, audit in zip(EDGES, _EXPECTED_EDGE_STATUSES, edge_audits):
        if audit.status == BLOCKED:
            failures.extend("edge:" + edge + ":" + issue
                            for issue in audit.issues)
            if not audit.issues:
                failures.append("edge:" + edge + ":blocked")
        elif audit.status != expected:
            absent.append("edge:" + edge + ":unconfirmed:" + audit.status)
            absent.extend("edge:" + edge + ":" + issue for issue in audit.issues)
    if path.status == BLOCKED:
        failures.extend("typed_path:" + x for x in path.violations)
        if not path.violations:
            failures.append("typed_path:blocked")
    elif path.status != TYPED_PATH_PASS:
        absent.append("typed_path:unconfirmed:" + path.status)
        absent.extend("typed_path:" + x for x in path.missing)

    if edge_audits[0].missing_lean_witnesses != NUMERIC_AND_ISSUER_OBSTRUCTIONS:
        absent.append("PlanOS->ActOS:numeric_issuer_obstruction_scope_changed")
    # Keep the actual source references on the *same* intermediate states.
    for a, b in zip(NODES, NODES[1:]):
        source = snapshots[a]
        target = snapshots[b]
        for field in ("lineage_id", "mission_contract_digest"):
            if source.get(field) is None or target.get(field) is None:
                absent.append(a + "->" + b + ":" + field + ":missing")
            elif not _same(source[field], target[field]):
                failures.append(a + "->" + b + ":" + field + ":mismatch")

    # A cross-store read is never claimed to be atomic. This only checks
    # individually observed source bytes remained identical during audit.
    try:
        after = {name: _store_files(roots[name], _STORE_FILES[name])
                 for name in NODES}
        if before != after:
            failures.append("five_store_chain:original_bytes_changed")
    except FileNotFoundError:
        absent.append("five_store_chain:original_store_disappeared")
    except (TypeError, ValueError, OSError, RecursionError) as exc:
        failures.append("five_store_chain:recheck_invalid:" + type(exc).__name__)

    status = BLOCKED if failures else NO_DATA if absent else SCOPED_COMPATIBLE
    paths = tuple(name + "." + path_name
                  for name in NODES for path_name in _STORE_FILES[name])
    counts = (("PlanOS", len(plan_commits)),
              ("ActOS", edge_audits[0].ledger_commit_count),
              ("ObserveOS", edge_audits[1].observe_commit_count),
              ("VerifyOS", edge_audits[2].verify_commit_count),
              ("LearnOS", edge_audits[3].learn_commit_count))
    return FiveStoreChainAudit(
        status=status,
        issues=tuple(dict.fromkeys(failures + absent)),
        edge_statuses=tuple((edge, audit.status)
                            for edge, audit in zip(EDGES, edge_audits)),
        persisted_store_commit_counts=counts,
        final_native_state_digests=tuple(
            (name, _fingerprint(snapshots[name])) for name in NODES
        ),
        checked_original_store_paths=paths,
        path_audit_status=path.status,
        five_stores_individually_replayed=(status == SCOPED_COMPATIBLE),
        four_original_typed_edges_checked=(status == SCOPED_COMPATIBLE),
        full_native_path_local_conditions_checked=(status == SCOPED_COMPATIBLE),
        store_bytes_stable_during_audit=(before == after),
    )


__all__ = (
    "VERSION", "SOURCE_PARENT", "SCOPED_COMPATIBLE", "NO_DATA", "BLOCKED",
    "NODES", "EDGES", "FiveStoreChainAudit",
    "audit_native_five_store_chain_compatibility",
)
