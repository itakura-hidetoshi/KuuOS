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


@dataclass(frozen=True)
class QiProcessTensorOptimizedPolicyAdapter:
    adapter_version: str
    adapter_status: str
    adapter_packet_id: str
    root_id: str | None
    source_process_tensor_id: str | None
    optimized_process_tensor_action: str
    memory_mode: str
    qcmi_value: float | None
    eps_w: float | None
    recovery_witness: bool
    memory_horizon_valid: bool
    non_markov_score: float
    fragility_score: float
    optimized_notify_threshold: float
    optimized_ticket_threshold: float
    optimized_handover_threshold: float
    advance_bias: float
    observe_bias: float
    reasons: list[str]
    blockers: list[str]
    read_only_policy_surface: bool
    policy_input_ready: bool
    write_performed: bool
    control_granted: bool
    authority: str = "qi_process_tensor_optimized_policy_adapter"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps(dict(value), ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def _float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _truthy(value: Any) -> bool:
    return value is True or str(value).strip().lower() in {"true", "yes", "1"}


def build_qi_process_tensor_optimized_policy_adapter(
    *,
    process_tensor_packet: Mapping[str, Any],
    adapter_context: Mapping[str, Any] | None = None,
) -> QiProcessTensorOptimizedPolicyAdapter:
    pt = _m(process_tensor_packet)
    ctx = _m(adapter_context)
    blockers: list[str] = []
    reasons: list[str] = []

    if ctx.get("process_tensor_optimized_policy_enabled") is not True:
        blockers.append("process_tensor_optimized_policy_enabled_not_true")
    if ctx.get("read_only_policy_surface") is not True:
        blockers.append("read_only_policy_surface_not_true")
    if pt.get("process_tensor_ok") is not True:
        blockers.append("process_tensor_not_ok")
        reasons.append("process_tensor_not_ok")

    root_id = pt.get("root_id")
    source_id = pt.get("process_tensor_id") or pt.get("packet_id")
    if not root_id:
        blockers.append("root_id_missing")
    if not source_id:
        blockers.append("process_tensor_id_missing")

    qcmi = _float(pt.get("qcmi_value"), 0.0)
    eps_w = _float(pt.get("eps_w"), _float(ctx.get("default_eps_w"), 0.05))
    recovery = _truthy(pt.get("recovery_witness"))
    horizon_valid = not _truthy(pt.get("memory_horizon_invalid"))
    non_markov = _float(pt.get("non_markov_score"), 0.0)
    fragility = _float(pt.get("fragility_score"), 0.0)

    memory_mode = "full_history"
    action = A_ADVANCE
    advance_bias = 1.0
    observe_bias = 0.0

    if recovery and qcmi <= eps_w and horizon_valid:
        memory_mode = "compressed_or_partial"
        reasons.append("recovery_compression_allowed")
    else:
        reasons.append("full_history_preferred")
        advance_bias -= 0.25
        observe_bias += 0.25

    if not recovery:
        action = A_OBSERVE
        reasons.append("recovery_witness_missing")
        observe_bias += 0.35
    if not horizon_valid:
        action = A_HOLD if action == A_ADVANCE else action
        reasons.append("memory_horizon_invalid")
        advance_bias -= 0.35
    if non_markov >= _float(ctx.get("handover_non_markov_threshold"), 0.9):
        action = A_HANDOVER
        reasons.append("non_markov_handover_band")
    elif non_markov >= _float(ctx.get("observe_non_markov_threshold"), 0.55) and action == A_ADVANCE:
        action = A_OBSERVE
        reasons.append("non_markov_observe_band")
    if fragility >= _float(ctx.get("ticket_fragility_threshold"), 0.65) and action in {A_ADVANCE, A_HOLD, A_OBSERVE}:
        action = A_TICKET
        reasons.append("fragility_ticket_band")
    if _truthy(pt.get("barrier_closed")):
        action = A_FREEZE
        reasons.append("process_tensor_barrier_closed")

    base_notify = _float(ctx.get("base_notify_uncertainty_threshold"), 0.45)
    base_ticket = _float(ctx.get("base_ticket_uncertainty_threshold"), 0.65)
    base_handover = _float(ctx.get("base_handover_uncertainty_threshold"), 0.85)
    adjustment = min(0.2, max(0.0, non_markov * 0.1 + fragility * 0.1))
    notify_threshold = max(0.25, base_notify - adjustment)
    ticket_threshold = max(0.45, base_ticket - adjustment)
    handover_threshold = max(0.65, base_handover - adjustment)

    if _truthy(pt.get("write_performed")) or _truthy(pt.get("control_granted")):
        blockers.append("source_not_read_only")
        reasons.append("read_only_boundary")

    ready = not blockers
    material = {
        "root_id": root_id,
        "source_process_tensor_id": source_id,
        "action": action,
        "memory_mode": memory_mode,
        "qcmi": qcmi,
        "eps_w": eps_w,
        "non_markov": non_markov,
        "fragility": fragility,
    }
    packet_id = "qi-pt-optimized-policy-" + _sha(material)[:16]

    return QiProcessTensorOptimizedPolicyAdapter(
        adapter_version="kuuos_runtime_daemon_qi_process_tensor_optimized_policy_adapter_v0_1",
        adapter_status="QI_PROCESS_TENSOR_OPTIMIZED_POLICY_READY" if ready else "QI_PROCESS_TENSOR_OPTIMIZED_POLICY_BLOCKED",
        adapter_packet_id=packet_id,
        root_id=str(root_id) if root_id else None,
        source_process_tensor_id=str(source_id) if source_id else None,
        optimized_process_tensor_action=action,
        memory_mode=memory_mode,
        qcmi_value=qcmi,
        eps_w=eps_w,
        recovery_witness=recovery,
        memory_horizon_valid=horizon_valid,
        non_markov_score=non_markov,
        fragility_score=fragility,
        optimized_notify_threshold=notify_threshold,
        optimized_ticket_threshold=ticket_threshold,
        optimized_handover_threshold=handover_threshold,
        advance_bias=max(0.0, advance_bias),
        observe_bias=observe_bias,
        reasons=sorted(set(reasons)),
        blockers=blockers,
        read_only_policy_surface=ctx.get("read_only_policy_surface") is True,
        policy_input_ready=ready,
        write_performed=False,
        control_granted=False,
    )
