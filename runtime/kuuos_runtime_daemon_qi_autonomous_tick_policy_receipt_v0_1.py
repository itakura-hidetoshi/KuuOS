#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

A_ADVANCE = "advance_tick"
A_HOLD = "hold"
A_OBSERVE = "observe"
A_NOTIFY = "notify"
A_TICKET = "ticket"
A_HANDOVER = "handover"
A_FREEZE = "freeze"
ACTIONS = [A_ADVANCE, A_HOLD, A_OBSERVE, A_NOTIFY, A_TICKET, A_HANDOVER, A_FREEZE]


@dataclass(frozen=True)
class QiAutonomousTickPolicyReceipt:
    receipt_version: str
    receipt_status: str
    receipt_id: str
    policy_packet_id: str | None
    selected_action: str
    daemon_loop_action: str
    root_id: str | None
    same_root: bool
    next_tick_number: int | None
    safe_resume_allowed: bool
    safe_resume_start_tick: int | None
    safe_resume_tick_count: int
    process_tensor_optimization_mode: str
    process_tensor_rollout_mode: str
    process_tensor_pressure: str
    process_tensor_memory_complexity_score: float
    process_tensor_memory_complexity_threshold: float
    process_tensor_qcmi_value: float
    process_tensor_recovery_epsilon: float
    process_tensor_recovery_witness_present: bool
    process_tensor_non_markov_unresolved: bool
    process_tensor_recovery_witness_missing: bool
    process_tensor_baseline_fallback_required: bool
    process_tensor_observation_required: bool
    process_tensor_full_history_required: bool
    process_tensor_advance_optimized: bool
    hold_required: bool
    observe_required: bool
    notify_required: bool
    ticket_required: bool
    handover_required: bool
    freeze_required: bool
    read_only_policy_surface: bool
    grants_new_authority: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    receipt_blockers: list[str]
    receipt_warnings: list[str]
    authority: str = "autonomous_tick_policy_receipt_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _truthy(value: Any) -> bool:
    return value is True or str(value).strip().lower() in {"true", "yes", "1"}


def _float(payload: Mapping[str, Any], key: str, default: float) -> float:
    try:
        return float(payload.get(key, default))
    except (TypeError, ValueError):
        return default


def _int_or_none(value: Any) -> int | None:
    try:
        if value is None:
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _sha(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _pressure(metrics: Mapping[str, Any], memory_score: float, qcmi_value: float, eps: float) -> str:
    explicit = metrics.get("process_tensor_pressure")
    if explicit in {"low", "moderate", "high", "critical"}:
        return str(explicit)
    observation = _float(metrics, "observation_debt_resolution_priority", 0.0)
    reentry = _float(metrics, "safe_reentry_window_score", 1.0)
    nonmarkov = _float(metrics, "nonmarkov_link_density", 1.0)
    kernel = _float(metrics, "memory_kernel_preservation_score", 1.0)
    if memory_score > 1.5 or qcmi_value > eps * 2.0 or observation >= 0.9 or reentry <= 0.2 or nonmarkov <= 0.2 or kernel <= 0.3:
        return "critical"
    if memory_score > 1.0 or qcmi_value > eps or observation >= 0.8 or reentry <= 0.25 or nonmarkov <= 0.25 or kernel <= 0.35:
        return "high"
    if observation >= 0.55 or reentry <= 0.5 or nonmarkov <= 0.5 or kernel <= 0.6:
        return "moderate"
    return "low"


def _rollout_mode(
    *,
    memory_score: float,
    memory_threshold: float,
    qcmi_value: float,
    eps: float,
    recovery_witness_present: bool,
    non_markov_unresolved: bool,
) -> tuple[str, str]:
    if non_markov_unresolved and not recovery_witness_present:
        return "full_history", "full_history_hold"
    if memory_score <= memory_threshold:
        if recovery_witness_present and qcmi_value <= eps:
            return "compressed", "compressed_recovery_advance"
        return "markov", "markov_advance"
    if recovery_witness_present and qcmi_value <= eps:
        return "partial_history", "partial_history_observe"
    return "full_history", "full_history_hold"


def build_qi_autonomous_tick_policy_receipt(
    *,
    policy_packet: Mapping[str, Any],
    process_tensor_packet: Mapping[str, Any] | None = None,
    receipt_context: Mapping[str, Any] | None = None,
) -> QiAutonomousTickPolicyReceipt:
    policy = _m(policy_packet)
    pt = _m(process_tensor_packet)
    ctx = _m(receipt_context)
    blockers: list[str] = []
    warnings: list[str] = []

    policy_packet_id = policy.get("policy_packet_id")
    selected_action = str(policy.get("selected_action") or A_HOLD)
    if selected_action not in ACTIONS:
        selected_action = A_HOLD
        blockers.append("selected_action_unknown")

    root_id = policy.get("root_id") or pt.get("root_id") or ctx.get("root_id")
    policy_status = str(policy.get("policy_status") or "")
    same_root = policy.get("same_root") is True
    if policy_status != "QI_AUTONOMOUS_TICK_POLICY_READY":
        blockers.append("policy_not_ready")
    if not policy_packet_id:
        blockers.append("policy_packet_id_missing")
    if not same_root:
        blockers.append("same_root_not_true")
    if policy.get("read_only_policy_surface") is not True:
        blockers.append("read_only_policy_surface_not_true")
    if _truthy(policy.get("grants_new_authority")) or _truthy(ctx.get("grants_new_authority")):
        blockers.append("new_authority_requested")

    memory_threshold = _float(ctx, "memory_complexity_threshold", _float(pt, "memory_complexity_threshold", 1.0))
    memory_score = _float(pt, "memory_complexity_score", _float(pt, "process_tensor_memory_complexity_score", 0.0))
    qcmi_value = _float(pt, "qcmi_value", _float(pt, "process_tensor_qcmi_value", 0.0))
    eps = _float(pt, "recovery_epsilon", _float(ctx, "recovery_epsilon", 0.1))
    recovery_present = (
        pt.get("recovery_witness") is True
        or pt.get("recovery_witness_present") is True
        or pt.get("process_tensor_recovery_witness_present") is True
    )
    recovery_missing = (
        _truthy(pt.get("recovery_witness_missing"))
        or _truthy(pt.get("process_tensor_recovery_witness_missing"))
        or (memory_score > memory_threshold and not recovery_present)
    )
    non_markov_unresolved = _truthy(pt.get("non_markov_unresolved")) or _truthy(pt.get("nonmarkov_unresolved"))
    rollout_mode, opt_mode = _rollout_mode(
        memory_score=memory_score,
        memory_threshold=memory_threshold,
        qcmi_value=qcmi_value,
        eps=eps,
        recovery_witness_present=recovery_present,
        non_markov_unresolved=non_markov_unresolved,
    )
    pressure = _pressure(pt, memory_score, qcmi_value, eps)

    observation_required = selected_action == A_OBSERVE or non_markov_unresolved or opt_mode == "partial_history_observe"
    full_history_required = rollout_mode == "full_history"
    baseline_fallback_required = selected_action != A_ADVANCE or full_history_required or pressure in {"high", "critical"}
    hold_required = selected_action == A_HOLD or (full_history_required and selected_action == A_ADVANCE)
    freeze_required = selected_action == A_FREEZE or pressure == "critical" and _truthy(ctx.get("freeze_on_critical_process_tensor_pressure"))

    next_tick = _int_or_none(policy.get("next_tick_number"))
    safe_resume_allowed = (
        not blockers
        and selected_action == A_ADVANCE
        and policy.get("advance_tick_allowed") is True
        and next_tick is not None
        and not observation_required
        and not hold_required
        and not freeze_required
        and not recovery_missing
    )
    if selected_action == A_ADVANCE and not safe_resume_allowed:
        warnings.append("advance_suppressed_by_process_tensor_receipt")

    daemon_loop_action = selected_action
    if freeze_required:
        daemon_loop_action = A_FREEZE
    elif observation_required and selected_action == A_ADVANCE:
        daemon_loop_action = A_OBSERVE
    elif hold_required and selected_action == A_ADVANCE:
        daemon_loop_action = A_HOLD

    material = {
        "policy_packet_id": policy_packet_id,
        "selected_action": selected_action,
        "daemon_loop_action": daemon_loop_action,
        "root_id": root_id,
        "next_tick_number": next_tick,
        "rollout_mode": rollout_mode,
        "optimization_mode": opt_mode,
        "memory_score": memory_score,
        "qcmi": qcmi_value,
        "eps": eps,
        "safe_resume_allowed": safe_resume_allowed,
    }
    receipt_id = "qi-tick-receipt-" + _sha(material)[:16]
    ready = not blockers

    return QiAutonomousTickPolicyReceipt(
        receipt_version="kuuos_runtime_daemon_qi_autonomous_tick_policy_receipt_v0_1",
        receipt_status="QI_AUTONOMOUS_TICK_POLICY_RECEIPT_READY" if ready else "QI_AUTONOMOUS_TICK_POLICY_RECEIPT_BLOCKED",
        receipt_id=receipt_id,
        policy_packet_id=str(policy_packet_id) if policy_packet_id else None,
        selected_action=selected_action,
        daemon_loop_action=daemon_loop_action,
        root_id=str(root_id) if root_id else None,
        same_root=same_root,
        next_tick_number=next_tick,
        safe_resume_allowed=safe_resume_allowed,
        safe_resume_start_tick=next_tick if safe_resume_allowed else None,
        safe_resume_tick_count=1 if safe_resume_allowed else 0,
        process_tensor_optimization_mode=opt_mode,
        process_tensor_rollout_mode=rollout_mode,
        process_tensor_pressure=pressure,
        process_tensor_memory_complexity_score=memory_score,
        process_tensor_memory_complexity_threshold=memory_threshold,
        process_tensor_qcmi_value=qcmi_value,
        process_tensor_recovery_epsilon=eps,
        process_tensor_recovery_witness_present=recovery_present,
        process_tensor_non_markov_unresolved=non_markov_unresolved,
        process_tensor_recovery_witness_missing=recovery_missing,
        process_tensor_baseline_fallback_required=baseline_fallback_required,
        process_tensor_observation_required=observation_required,
        process_tensor_full_history_required=full_history_required,
        process_tensor_advance_optimized=safe_resume_allowed and opt_mode in {"markov_advance", "compressed_recovery_advance"},
        hold_required=hold_required,
        observe_required=daemon_loop_action == A_OBSERVE,
        notify_required=daemon_loop_action == A_NOTIFY,
        ticket_required=daemon_loop_action == A_TICKET,
        handover_required=daemon_loop_action == A_HANDOVER,
        freeze_required=daemon_loop_action == A_FREEZE,
        read_only_policy_surface=policy.get("read_only_policy_surface") is True,
        grants_new_authority=False,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        receipt_blockers=blockers,
        receipt_warnings=warnings,
    )
