"""v0.41: original DecisionOS persisted origin and source Belief receipt identity.

Separate original store replay and original-source structural checks.
Numeric clock labels are recorded without assuming a shared clock. All
historical typed edges are checked separately through certified v0.40.
No global descent, issuer authentication or execution authority is inferred.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from runtime.kuuos_belief_os_gerbe_types_v0_3 import (
    RECEIPT_VERSION as BELIEF_RECEIPT_VERSION,
    NON_AUTHORITY_FLAGS as BELIEF_NON_AUTHORITY,
    receipt_digest as belief_receipt_digest,
)
from runtime.kuuos_decision_os_state_v0_1 import build_initial_decision_state
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore, DecisionStoreError
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
    SCOPED_COMPATIBLE as PRIOR_PASS,
    _roots_separate,
    audit_native_plural_store_origin,
)

VERSION = "kuuos_lean_python_decision_store_origin_v0_41"
SOURCE_PARENT = "7d9396aa06ccb59f0b2359406ed58ba12d169aad"
SCOPED_COMPATIBLE = "SCOPED_DECISION_ORIGIN_AND_PLURAL_WA_PLAN_COMPATIBLE"
_DECISION_FILES = (
    "decision-genesis.json", "decision-ledger.jsonl", "decision-snapshot.json",
)
_INPUT = _INPUT_ERRORS + (DecisionStoreError, UnicodeError)
_CROSS_SOURCE_AFTER = "SOURCE_RECEIPT_NUMERICALLY_AFTER_DECISION_GENESIS"
_CROSS_SOURCE_NOT_AFTER = "SOURCE_RECEIPT_NUMERICALLY_NOT_AFTER_DECISION_GENESIS"


class _CapturedDecisionStore(_CapturedReads, DecisionStore):
    """Original DecisionStore replay over a fixed set of observed file bytes."""


@dataclass(frozen=True)
class NativeDecisionStoreOriginAudit:
    status: str
    issues: tuple[str, ...] = ()
    belief_receipt_sha256: str | None = None
    decision_genesis_sha256: str | None = None
    decision_final_sha256: str | None = None
    decision_ledger_commit_count: int = 0
    decision_committed_deliberation_count: int = 0
    decision_summary_count: int = 0
    checked_source_paths: tuple[str, ...] = ()
    staged_typed_edge_statuses: tuple[tuple[str, str], ...] = ()
    decision_original_store_replayed: bool = False
    decision_genesis_matches_original_constructor: bool = False
    decision_history_data_conditions_checked: bool = False
    supplied_belief_receipt_locally_valid: bool = False
    belief_decision_source_identity_checked: bool = False
    prior_plural_wa_plan_origins_checked: bool = False
    decision_store_bytes_stable_during_audit: bool = False
    prior_store_bytes_stable_during_audit: bool = False
    # The native v1.3 fixture has source receipt time 5000 and Decision
    # genesis time 1000. These numeric values have not been proved to
    # share a causal clock; never erase or interpret the gap as resolved.
    source_receipt_created_at_ms: int | None = None
    decision_genesis_updated_at_ms: int | None = None
    cross_source_time_relation: str | None = None
    common_source_decision_clock_proved: bool = False
    global_temporal_descent_proved: bool = False
    original_belief_store_replayed: bool = False
    globally_atomic_four_store_snapshot_proved: bool = False
    global_descent_proved: bool = False
    lean_python_semantic_refinement_proved: bool = False
    external_issuer_authenticated: bool = False
    actual_act_numeric_witnesses_proved: bool = False
    host_license_granted: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    clinical_authority_granted: bool = False
    legal_authority_granted: bool = False
    git_authority_granted: bool = False
    memory_overwrite_authority_granted: bool = False
    original_store_mutated: bool = False


def _hold(status: str, *issues: str) -> NativeDecisionStoreOriginAudit:
    return NativeDecisionStoreOriginAudit(status=status, issues=tuple(issues))


def _decision_history_alignment(
    genesis: dict, final: dict, commits: list[dict],
) -> tuple[bool, int, int]:
    """Python JSON data analogue of Lean DecisionHistory, not a proof link."""
    summaries = final.get("decision_summaries")
    if type(summaries) is not list:
        return False, 0, 0
    event_ids = [
        row["event"].get("decision_event_digest")
        for row in commits if row["event"].get("target_phase") == "commit"
    ]
    summary_ids = [
        row.get("commit_event_digest") for row in summaries if type(row) is dict
    ]
    n = len(event_ids)
    aligned = (
        type(genesis.get("event_index")) is int
        and genesis["event_index"] == 0
        and type(genesis.get("decision_version")) is int
        and genesis["decision_version"] == 0
        and type(genesis.get("completed_deliberations")) is int
        and genesis["completed_deliberations"] == 0
        and genesis.get("decision_summaries") == []
        and type(final.get("event_index")) is int
        and final["event_index"] == len(commits)
        and type(final.get("decision_version")) is int
        and final["decision_version"] == n
        and type(final.get("completed_deliberations")) is int
        and final["completed_deliberations"] == n
        and len(summaries) == n
        and len(summary_ids) == n
        and summary_ids == event_ids
        and all(
            type(row.get("decision_version")) is int
            and row["decision_version"] == i
            for i, row in enumerate(summaries, 1)
        )
    )
    return aligned, n, len(summaries)


def _belief_receipt_local_conditions(belief: dict, genesis: dict) -> tuple[str, ...]:
    """Check only the original receipt's JSON self-consistency and source ID."""
    failures: list[str] = []
    if belief.get("version") != BELIEF_RECEIPT_VERSION:
        failures.append("BeliefOSReceipt:version_invalid")
    if belief.get("belief_gerbe_receipt_digest") != belief_receipt_digest(belief):
        failures.append("BeliefOSReceipt:self_digest_invalid")
    if belief.get("route") != "CANDIDATE":
        failures.append("BeliefOSReceipt:candidate_route_required")
    if belief.get("planning_support_license") is not True:
        failures.append("BeliefOSReceipt:planning_support_not_observed")
    if not _same(belief.get("non_authority"), BELIEF_NON_AUTHORITY):
        failures.append("BeliefOSReceipt:non_authority_boundary_invalid")
    if belief.get("future_only") is not True or belief.get("memory_overwrite") is not False:
        failures.append("BeliefOSReceipt:future_only_or_overwrite_boundary_invalid")
    if not _same(belief.get("lineage_id"), genesis.get("lineage_id")):
        failures.append("BeliefOSReceipt:decision_lineage_mismatch")
    if not _same(belief.get("belief_gerbe_receipt_digest"),
                 genesis.get("source_belief_receipt_digest")):
        failures.append("BeliefOSReceipt:decision_source_digest_mismatch")
    return tuple(failures)


def audit_native_decision_store_origin(
    belief_receipt: Any,
    decision_state: Any,
    plural_state: Any,
    wa_state: Any,
    plan_state: Any,
    replan_activation_receipt: Any,
    original_decision_store_root: Any,
    original_plural_store_root: Any,
    original_wa_store_root: Any,
    original_plan_store_root: Any,
) -> NativeDecisionStoreOriginAudit:
    """Read-only audit of the four actual native stores and supplied receipt.

    v0.40 is called unchanged on the downstream three stores and their staged
    historical edges. No missing packet is built by this production auditor.
    """
    named = (
        ("BeliefOSReceipt", belief_receipt),
        ("DecisionOS", decision_state),
        ("DecisionOSPlural", plural_state),
        ("DecisionOSWa", wa_state),
        ("PlanOS", plan_state),
        ("replan_receipt", replan_activation_receipt),
        ("DecisionStore", original_decision_store_root),
        ("PluralStore", original_plural_store_root),
        ("WaStore", original_wa_store_root),
        ("PlanStore", original_plan_store_root),
    )
    missing = tuple(n + ":original_source_missing" for n, v in named if v is None)
    if missing:
        return _hold(NO_DATA, *missing)
    roots_input = (
        original_decision_store_root, original_plural_store_root,
        original_wa_store_root, original_plan_store_root,
    )
    if any(type(v) is not str and type(v) is not type(Path()) for v in roots_input):
        return _hold(BLOCKED, "decision_plural_wa_plan:untrusted_root_type")

    try:
        belief = _packet(belief_receipt, "BeliefOSReceipt")
        decision = _packet(decision_state, "DecisionOS")
        plural = _packet(plural_state, "DecisionOSPlural")
        wa = _packet(wa_state, "DecisionOSWa")
        plan = _packet(plan_state, "PlanOS")
        receipt = _packet(replan_activation_receipt, "replan_receipt")
        roots = tuple(_trusted_store_root(v) for v in roots_input)
        if not _roots_separate(roots):
            return _hold(BLOCKED, "decision_plural_wa_plan:roots_overlap")
        decision_root, plural_root, wa_root, plan_root = roots
        before = _store_files(decision_root, _DECISION_FILES)
        genesis, final, commits = _replay_captured(
            decision_root, _CapturedDecisionStore, before,
        )
        final = _packet(final, "DecisionStore.final")
    except FileNotFoundError:
        return _hold(NO_DATA, "decision_store:original_history_missing")
    except _INPUT as exc:
        return _hold(BLOCKED, "decision_store:original_source_invalid:"
                     + type(exc).__name__)

    if not _same(decision, final):
        return _hold(BLOCKED, "DecisionOS:not_original_stored_final")
    if final.get("current_phase") != "commit":
        return _hold(NO_DATA, "DecisionOS:committed_final_unobserved")

    failures: list[str] = []
    absent: list[str] = []
    prior = None
    aligned = False
    committed = 0
    summary_count = 0
    try:
        failures.extend(_belief_receipt_local_conditions(belief, genesis))
        reconstructed = build_initial_decision_state(
            decision_id=genesis["decision_id"],
            lineage_id=genesis["lineage_id"],
            mission_contract_digest=genesis["mission_contract_digest"],
            mission_state_digest=genesis["mission_state_digest"],
            source_belief_receipt_digest=belief["belief_gerbe_receipt_digest"],
            decision_context_digest=genesis["decision_context_digest"],
            decision_budget=genesis["decision_budget"],
            weights=genesis["weights"],
            thresholds=genesis["thresholds"],
            now_ms=genesis["updated_at_ms"],
        )
        if not _same(reconstructed, genesis):
            failures.append("DecisionOS:genesis_not_original_constructor")
        aligned, committed, summary_count = _decision_history_alignment(
            genesis, final, commits,
        )
        if not aligned:
            failures.append("DecisionOS:commit_summary_history_not_aligned")
        prior = audit_native_plural_store_origin(
            decision_state=decision,
            plural_state=plural,
            wa_state=wa,
            plan_state=plan,
            replan_activation_receipt=receipt,
            original_plural_store_root=plural_root,
            original_wa_store_root=wa_root,
            original_plan_store_root=plan_root,
        )
        if prior.status == BLOCKED:
            failures.extend("v040:" + issue for issue in prior.issues)
            if not prior.issues:
                failures.append("v040:blocked")
        elif prior.status != PRIOR_PASS:
            absent.append("v040:unconfirmed:" + prior.status)
            absent.extend("v040:" + issue for issue in prior.issues)
        elif not (
            prior.plural_original_store_replayed
            and prior.plural_genesis_matches_original_constructor
            and prior.plural_lean_history_data_conditions_checked
            and prior.decision_to_plural_original_edge_checked
            and prior.prior_wa_plan_original_stores_checked
            and prior.plural_store_bytes_stable_during_audit
            and prior.wa_plan_store_bytes_stable_during_audit
        ):
            absent.append("v040:local_conditions_unconfirmed")
    except _INPUT as exc:
        return _hold(BLOCKED, "decision_store:original_conditions_invalid:"
                     + type(exc).__name__)

    after = None
    try:
        _trusted_store_root(decision_root)
        after = _store_files(decision_root, _DECISION_FILES)
        if before != after:
            failures.append("decision_store:original_bytes_changed")
    except FileNotFoundError:
        absent.append("decision_store:original_history_disappeared")
    except _INPUT as exc:
        failures.append("decision_store:recheck_invalid:" + type(exc).__name__)

    belief_time = belief.get("created_at_ms")
    genesis_time = genesis.get("updated_at_ms")
    if type(belief_time) is not int or belief_time < 0:
        absent.append("BeliefOSReceipt:created_at_ms_not_observed")
    if type(genesis_time) is not int or genesis_time < 0:
        absent.append("DecisionOS:genesis_time_not_observed")
    numeric_relation = None
    if type(belief_time) is int and type(genesis_time) is int:
        numeric_relation = (
            _CROSS_SOURCE_AFTER if belief_time > genesis_time
            else _CROSS_SOURCE_NOT_AFTER
        )

    status = BLOCKED if failures else NO_DATA if absent else SCOPED_COMPATIBLE
    passed = status == SCOPED_COMPATIBLE
    return NativeDecisionStoreOriginAudit(
        status=status,
        issues=tuple(dict.fromkeys(failures + absent)),
        belief_receipt_sha256=_fingerprint(belief),
        decision_genesis_sha256=_fingerprint(genesis),
        decision_final_sha256=_fingerprint(final),
        decision_ledger_commit_count=len(commits),
        decision_committed_deliberation_count=committed,
        decision_summary_count=summary_count,
        checked_source_paths=(
            ("BeliefOSReceipt.belief_gerbe_receipt_digest",)
            + tuple("DecisionOS." + n for n in _DECISION_FILES)
            + (prior.checked_source_paths if prior else ())
        ),
        staged_typed_edge_statuses=(
            prior.staged_typed_edge_statuses if prior else ()
        ),
        decision_original_store_replayed=passed,
        decision_genesis_matches_original_constructor=passed,
        decision_history_data_conditions_checked=passed and aligned,
        supplied_belief_receipt_locally_valid=passed,
        belief_decision_source_identity_checked=passed,
        prior_plural_wa_plan_origins_checked=passed,
        decision_store_bytes_stable_during_audit=after is not None and before == after,
        prior_store_bytes_stable_during_audit=(
            prior.plural_store_bytes_stable_during_audit
            and prior.wa_plan_store_bytes_stable_during_audit if prior else False
        ),
        source_receipt_created_at_ms=belief_time if type(belief_time) is int else None,
        decision_genesis_updated_at_ms=genesis_time if type(genesis_time) is int else None,
        cross_source_time_relation=numeric_relation,
    )


__all__ = (
    "VERSION", "SOURCE_PARENT", "SCOPED_COMPATIBLE", "BLOCKED", "NO_DATA",
    "NativeDecisionStoreOriginAudit", "audit_native_decision_store_origin",
)
