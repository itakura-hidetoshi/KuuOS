#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


EXECUTABLE_ACTIONS = {"advance_tick", "notify", "ticket", "handover"}
NONEXEC_ACTIONS = {"hold", "observe", "freeze"}
ALL_ACTIONS = EXECUTABLE_ACTIONS | NONEXEC_ACTIONS


@dataclass(frozen=True)
class QiAutonomousExecutionEngineResult:
    engine_version: str
    engine_status: str
    engine_packet_id: str
    selected_action: str
    execution_mode: str
    execution_intent_staged: bool
    execution_committed: bool
    process_tensor_guard_passed: bool
    decisionos_guard_passed: bool
    cbf_guard_passed: bool
    token_guard_passed: bool
    authority_guard_passed: bool
    recovery_guard_passed: bool
    nonmarkov_guard_passed: bool
    selected_reason: str
    action_blockers: list[str]
    action_warnings: list[str]
    execution_intent_packet: dict[str, Any]
    receipt_only: bool
    read_only: bool
    projection_only: bool
    scheduler_bypass_performed: bool
    runtime_control_performed: bool
    notification_sent: bool
    ticket_created: bool
    handover_performed: bool
    ledger_append_performed: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    authority: str = "qi_autonomous_execution_engine_governance_bounded"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    return default


def _float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _sha_obj(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _action(value: Any, default: str = "hold") -> str:
    text = str(value or default)
    return text if text in ALL_ACTIONS else default


def _guarded_false(prefix: str, packet: Mapping[str, Any], blockers: list[str]) -> None:
    for key in [
        "runtime_control_performed",
        "scheduler_bypass_performed",
        "notification_sent",
        "ticket_created",
        "handover_performed",
        "ledger_append_performed",
        "memory_write_performed",
        "memory_append_performed",
        "memory_overwrite_performed",
        "world_update_performed",
        "control_packet_mutation_performed",
        "probe_execution_performed",
        "grants_probe_execution_authority",
        "grants_world_update_authority",
        "grants_memory_overwrite_authority",
    ]:
        if key in packet and packet.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def build_qi_autonomous_execution_engine(
    *,
    decisionos_packet: Mapping[str, Any],
    cbf_packet: Mapping[str, Any],
    token_ledger_packet: Mapping[str, Any],
    process_tensor_packet: Mapping[str, Any],
    cadence_release_packet: Mapping[str, Any],
    execution_context: Mapping[str, Any] | None = None,
) -> QiAutonomousExecutionEngineResult:
    decision = _mapping(decisionos_packet)
    cbf = _mapping(cbf_packet)
    token = _mapping(token_ledger_packet)
    pt = _mapping(process_tensor_packet)
    release = _mapping(cadence_release_packet)
    ctx = _mapping(execution_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("qi_autonomous_execution_engine_enabled") is not True:
        blockers.append("qi_autonomous_execution_engine_enabled_not_true")
    if ctx.get("governance_bounded_execution_required") is not True:
        blockers.append("governance_bounded_execution_required_not_true")
    if ctx.get("staged_execution_only") is not True:
        blockers.append("staged_execution_only_not_true")
    if ctx.get("receipt_only_required") is not True:
        blockers.append("receipt_only_required_not_true")
    if ctx.get("read_only_required") is not True:
        blockers.append("read_only_required_not_true")
    if ctx.get("projection_only_required") is not True:
        blockers.append("projection_only_required_not_true")
    for requested in [
        "request_runtime_control",
        "request_scheduler_bypass",
        "request_notification_send",
        "request_ticket_create",
        "request_handover_perform",
        "request_ledger_append",
        "request_memory_write",
        "request_memory_append",
        "request_world_update",
        "request_probe_execution",
    ]:
        if ctx.get(requested) is True:
            blockers.append(f"{requested}_not_allowed")

    if release.get("packet_status") != "QI_CADENCE_V0_2_RELEASE_ESTABLISHED_PACKET_READY":
        blockers.append("cadence_release_established_not_ready")
    if release.get("v0_2_release_ready") is not True or release.get("v0_2_established") is not True:
        blockers.append("cadence_v0_2_not_release_established")
    if release.get("release_receipt_only") is not True or release.get("established_receipt_only") is not True:
        blockers.append("cadence_release_not_receipt_only")
    if release.get("projection_only") is not True:
        blockers.append("cadence_release_not_projection_only")
    _guarded_false("cadence_release", release, blockers)

    decision_action = _action(decision.get("decision_action"), "hold")
    cbf_action = _action(cbf.get("cbf_action"), "hold")
    token_action = _action(token.get("token_ledger_action"), "hold")
    pt_action = _action(pt.get("process_tensor_action"), "hold")
    proposed_action = _action(ctx.get("proposed_action") or pt_action or decision_action, "hold")

    decision_ok = decision_action in {proposed_action, "advance_tick"} and decision_action not in {"freeze"}
    cbf_ok = _bool(cbf.get("cbf_ok"), False) and cbf_action in {proposed_action, "advance_tick", "hold"} and not _bool(cbf.get("barrier_closed"), False)
    token_ok = _bool(token.get("token_ledger_ok"), False) and _int(token.get("remaining_tokens"), 0) >= _int(token.get("minimum_required_tokens"), 1)
    pt_ok = _bool(pt.get("process_tensor_ok"), False)
    recovery_ok = not _bool(pt.get("recovery_witness_missing"), False) and _bool(pt.get("recovery_witness_present"), True)
    nonmarkov_ok = not _bool(pt.get("non_markov_unresolved"), False)
    explicit_authority = ctx.get("execution_authority_granted") is True
    allowed_by_scope = proposed_action in set(ctx.get("allowed_actions") or []) if isinstance(ctx.get("allowed_actions"), list) else proposed_action in NONEXEC_ACTIONS
    authority_ok = explicit_authority and allowed_by_scope and proposed_action in EXECUTABLE_ACTIONS

    if proposed_action == "freeze" or _bool(pt.get("freeze_required"), False):
        selected_action = "freeze"
        reason = "freeze_required"
    elif not pt_ok or not nonmarkov_ok:
        selected_action = "observe"
        reason = "process_tensor_observe_required"
    elif not recovery_ok:
        selected_action = "handover"
        reason = "recovery_witness_missing"
    elif not cbf_ok:
        selected_action = "hold"
        reason = "cbf_guard_failed"
    elif not token_ok:
        selected_action = "hold"
        reason = "token_guard_failed"
    elif proposed_action in EXECUTABLE_ACTIONS and not authority_ok:
        selected_action = "hold"
        reason = "authority_guard_failed"
    elif proposed_action in EXECUTABLE_ACTIONS and decision_ok and cbf_ok and token_ok and pt_ok and authority_ok:
        selected_action = proposed_action
        reason = "staged_execution_intent_ready"
    else:
        selected_action = "hold"
        reason = "safe_default_hold"

    execution_mode = "nonexecuting_receipt" if selected_action in NONEXEC_ACTIONS else "staged_intent_only"
    intent_core = {
        "selected_action": selected_action,
        "execution_mode": execution_mode,
        "reason": reason,
        "decision_action": decision_action,
        "cbf_action": cbf_action,
        "token_action": token_action,
        "process_tensor_action": pt_action,
        "cadence_release_packet_id": release.get("release_packet_id"),
        "cadence_established_packet_id": release.get("established_packet_id"),
        "receipt_only": True,
        "read_only": True,
        "projection_only": True,
    }
    engine_packet_id = "qi-exec-engine-" + _sha_obj(intent_core)[:16]
    intent_packet = dict(intent_core)
    intent_packet.update({
        "engine_packet_id": engine_packet_id,
        "engine_version": "kuuos_runtime_daemon_qi_autonomous_execution_engine_v0_1",
        "execution_intent_staged": selected_action in EXECUTABLE_ACTIONS and reason == "staged_execution_intent_ready",
        "execution_committed": False,
        "runtime_control_performed": False,
        "scheduler_bypass_performed": False,
        "notification_sent": False,
        "ticket_created": False,
        "handover_performed": False,
        "ledger_append_performed": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "world_update_performed": False,
        "probe_execution_performed": False,
    })
    ready = not blockers
    return QiAutonomousExecutionEngineResult(
        engine_version="kuuos_runtime_daemon_qi_autonomous_execution_engine_v0_1",
        engine_status="QI_AUTONOMOUS_EXECUTION_ENGINE_READY" if ready else "QI_AUTONOMOUS_EXECUTION_ENGINE_BLOCKED",
        engine_packet_id=engine_packet_id,
        selected_action=selected_action,
        execution_mode=execution_mode,
        execution_intent_staged=selected_action in EXECUTABLE_ACTIONS and reason == "staged_execution_intent_ready" and ready,
        execution_committed=False,
        process_tensor_guard_passed=pt_ok,
        decisionos_guard_passed=decision_ok,
        cbf_guard_passed=cbf_ok,
        token_guard_passed=token_ok,
        authority_guard_passed=authority_ok,
        recovery_guard_passed=recovery_ok,
        nonmarkov_guard_passed=nonmarkov_ok,
        selected_reason=reason,
        action_blockers=blockers,
        action_warnings=warnings,
        execution_intent_packet=intent_packet if ready else {},
        receipt_only=True,
        read_only=True,
        projection_only=True,
        scheduler_bypass_performed=False,
        runtime_control_performed=False,
        notification_sent=False,
        ticket_created=False,
        handover_performed=False,
        ledger_append_performed=False,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
    )
