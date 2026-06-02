#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import pathlib
from typing import Any, Mapping, Sequence

try:
    from runtime.kuuos_runtime_daemon_qi_autonomous_multi_tick_window_governor_v0_1 import run_qi_autonomous_multi_tick_window_governor
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_autonomous_multi_tick_window_governor_v0_1 import run_qi_autonomous_multi_tick_window_governor


@dataclass(frozen=True)
class QiAdaptiveWindowSchedulerResult:
    adaptive_scheduler_version: str
    adaptive_scheduler_status: str
    cadence_mode: str
    pressure_class: str
    recommended_window_ticks: int
    max_window_ticks: int
    stop_on_observe: bool
    stop_on_full_history: bool
    stop_on_freeze: bool
    adaptive_window_packet: dict[str, Any]
    delegated_window_status: str | None
    delegated_completed_tick_count: int
    delegated_stop_reason: str | None
    event_log_path: str
    ledger_state_path: str
    process_tensor_pressure_score: float
    memory_complexity_score: float
    qcmi_value: float
    recovery_witness_present: bool
    token_budget_available: int
    bounded_adaptation_enforced: bool
    delegates_only_to_multi_tick_window_governor: bool
    scheduler_grants_no_new_authority: bool
    memory_read_performed: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    delegated_window_packet: dict[str, Any]
    scheduler_blockers: list[str]
    scheduler_warnings: list[str]
    authority: str = "adaptive_window_scheduler_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _float(payload: Mapping[str, Any], key: str, default: float) -> float:
    try:
        return float(payload.get(key, default))
    except (TypeError, ValueError):
        return default


def _int(payload: Mapping[str, Any], key: str, default: int) -> int:
    try:
        return int(payload.get(key, default))
    except (TypeError, ValueError):
        return default


def _truthy(value: Any) -> bool:
    return value is True or str(value).strip().lower() in {"true", "yes", "1"}


def _clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def _require_false(prefix: str, packet: Mapping[str, Any], blockers: list[str]) -> None:
    for key in [
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


def _pressure_score(process_tensor_packet: Mapping[str, Any], metrics: Mapping[str, Any], memory_score: float, qcmi: float, token_budget: int) -> float:
    observation = _float(metrics, "observation_debt_resolution_priority", _float(process_tensor_packet, "observation_debt_resolution_priority", 0.0))
    reentry = 1.0 - _float(metrics, "safe_reentry_window_score", _float(process_tensor_packet, "safe_reentry_window_score", 1.0))
    nonmarkov = 1.0 - _float(metrics, "nonmarkov_link_density", _float(process_tensor_packet, "nonmarkov_link_density", 1.0))
    kernel_loss = 1.0 - _float(metrics, "memory_kernel_preservation_score", _float(process_tensor_packet, "memory_kernel_preservation_score", 1.0))
    token_pressure = 0.0 if token_budget >= 4 else (4 - max(token_budget, 0)) / 4.0
    return max(0.0, min(1.0, 0.25 * observation + 0.2 * reentry + 0.2 * nonmarkov + 0.15 * kernel_loss + 0.1 * min(memory_score, 2.0) / 2.0 + 0.05 * min(qcmi, 1.0) + 0.05 * token_pressure))


def _pressure_class(score: float, recovery_witness_present: bool, non_markov_unresolved: bool) -> str:
    if non_markov_unresolved:
        return "observe_first"
    if not recovery_witness_present and score >= 0.5:
        return "full_history_guarded"
    if score >= 0.75:
        return "high"
    if score >= 0.45:
        return "moderate"
    return "low"


def _recommended_ticks(pressure_class: str, token_budget: int, min_ticks: int, max_ticks: int) -> int:
    if pressure_class in {"observe_first", "full_history_guarded", "high"}:
        base = 1
    elif pressure_class == "moderate":
        base = min(2, max_ticks)
    else:
        base = min(4, max_ticks)
    if token_budget > 0:
        base = min(base, token_budget)
    else:
        base = 1
    return _clamp(base, min_ticks, max_ticks)


def run_qi_adaptive_window_scheduler(
    *,
    decisionos_packet: Mapping[str, Any],
    cbf_packet: Mapping[str, Any],
    token_ledger_packet: Mapping[str, Any],
    process_tensor_packet: Mapping[str, Any],
    memory_entries: Sequence[Mapping[str, Any]] | Mapping[str, Any],
    scheduler_state: Mapping[str, Any],
    scheduler_proposal: Mapping[str, Any],
    process_tensor_metrics: Mapping[str, Any],
    event_log_path: str | pathlib.Path,
    ledger_state_path: str | pathlib.Path,
    adaptive_context: Mapping[str, Any] | None = None,
) -> QiAdaptiveWindowSchedulerResult:
    ctx = _mapping(adaptive_context)
    pt = _mapping(process_tensor_packet)
    metrics = _mapping(process_tensor_metrics)
    token = _mapping(token_ledger_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("adaptive_window_scheduler_enabled") is not True:
        blockers.append("adaptive_window_scheduler_enabled_not_true")
    if ctx.get("read_only_adaptive_scheduler") is not True:
        blockers.append("read_only_adaptive_scheduler_not_true")
    if ctx.get("jsonl_backend_required") is not True:
        blockers.append("jsonl_backend_required_not_true")
    if ctx.get("request_probe_execution") is True:
        blockers.append("request_probe_execution")
    if ctx.get("request_memory_write") is True:
        blockers.append("request_memory_write")
    if ctx.get("request_world_update") is True:
        blockers.append("request_world_update")
    if ctx.get("request_control_packet_mutation") is True:
        blockers.append("request_control_packet_mutation")

    min_ticks = max(1, _int(ctx, "min_window_ticks", 1))
    max_ticks = max(min_ticks, _int(ctx, "max_window_ticks", 4))
    absolute_cap = max(1, _int(ctx, "absolute_max_window_ticks", 16))
    if max_ticks > absolute_cap:
        max_ticks = absolute_cap
        warnings.append("max_window_clamped_to_absolute_cap")
    remaining = _int(token, "remaining_tokens", _int(ctx, "token_budget_available", max_ticks))
    minimum_required = _int(token, "minimum_required_tokens", 1)
    token_budget = max(0, remaining - max(0, minimum_required - 1))

    memory_score = _float(pt, "memory_complexity_score", _float(pt, "process_tensor_memory_complexity_score", 0.0))
    qcmi = _float(pt, "qcmi_value", _float(pt, "process_tensor_qcmi_value", 0.0))
    recovery_present = pt.get("recovery_witness_present") is True or pt.get("process_tensor_recovery_witness_present") is True or pt.get("recovery_witness") is True
    non_markov = _truthy(pt.get("non_markov_unresolved")) or _truthy(pt.get("nonmarkov_unresolved"))
    score = _pressure_score(pt, metrics, memory_score, qcmi, token_budget)
    pclass = _pressure_class(score, recovery_present, non_markov)
    recommended = _recommended_ticks(pclass, token_budget, min_ticks, max_ticks)

    stop_on_observe = True
    stop_on_full_history = True
    stop_on_freeze = True
    cadence_mode = {
        "low": "wide_compressed_window",
        "moderate": "moderate_guarded_window",
        "high": "single_tick_high_pressure",
        "observe_first": "observe_first_single_tick",
        "full_history_guarded": "full_history_single_tick",
    }.get(pclass, "single_tick_high_pressure")

    schedule = ctx.get("process_tensor_schedule")
    if not isinstance(schedule, list):
        schedule = []
    adaptive_window_packet = {
        "window_governor_enabled": True,
        "read_only_window_governor": True,
        "jsonl_backend_required": True,
        "requested_window_ticks": recommended,
        "max_window_ticks": recommended,
        "absolute_max_window_ticks": absolute_cap,
        "current_tick": _int(ctx, "current_tick", _int(token, "current_tick", 0)),
        "tick_id_prefix": str(ctx.get("tick_id_prefix", "qi-adaptive")),
        "stop_on_observe": stop_on_observe,
        "stop_on_full_history": stop_on_full_history,
        "freeze_on_critical_process_tensor_pressure": True,
        "process_tensor_schedule": schedule,
        "memory_complexity_threshold": ctx.get("memory_complexity_threshold", pt.get("memory_complexity_threshold", 1.0)),
        "recovery_epsilon": ctx.get("recovery_epsilon", pt.get("recovery_epsilon", 0.1)),
    }

    delegated: dict[str, Any] = {}
    if not blockers:
        delegated = run_qi_autonomous_multi_tick_window_governor(
            decisionos_packet=decisionos_packet,
            cbf_packet=cbf_packet,
            token_ledger_packet=token_ledger_packet,
            process_tensor_packet=process_tensor_packet,
            memory_entries=memory_entries,
            scheduler_state=scheduler_state,
            scheduler_proposal=scheduler_proposal,
            process_tensor_metrics=process_tensor_metrics,
            event_log_path=event_log_path,
            ledger_state_path=ledger_state_path,
            window_context=adaptive_window_packet,
        ).to_dict()
        if delegated.get("window_governor_status") != "QI_AUTONOMOUS_MULTI_TICK_WINDOW_GOVERNOR_COMPLETED":
            blockers.append("delegated_window_not_completed")
        _require_false("delegated_window", delegated, blockers)

    ready = not blockers
    return QiAdaptiveWindowSchedulerResult(
        adaptive_scheduler_version="kuuos_runtime_daemon_qi_adaptive_window_scheduler_v0_1",
        adaptive_scheduler_status="QI_ADAPTIVE_WINDOW_SCHEDULER_COMPLETED" if ready else "QI_ADAPTIVE_WINDOW_SCHEDULER_BLOCKED",
        cadence_mode=cadence_mode,
        pressure_class=pclass,
        recommended_window_ticks=recommended,
        max_window_ticks=max_ticks,
        stop_on_observe=stop_on_observe,
        stop_on_full_history=stop_on_full_history,
        stop_on_freeze=stop_on_freeze,
        adaptive_window_packet=adaptive_window_packet,
        delegated_window_status=str(delegated.get("window_governor_status")) if delegated.get("window_governor_status") else None,
        delegated_completed_tick_count=int(delegated.get("completed_tick_count", 0)) if delegated else 0,
        delegated_stop_reason=str(delegated.get("stop_reason")) if delegated.get("stop_reason") else None,
        event_log_path=str(event_log_path),
        ledger_state_path=str(ledger_state_path),
        process_tensor_pressure_score=score,
        memory_complexity_score=memory_score,
        qcmi_value=qcmi,
        recovery_witness_present=recovery_present,
        token_budget_available=token_budget,
        bounded_adaptation_enforced=True,
        delegates_only_to_multi_tick_window_governor=True,
        scheduler_grants_no_new_authority=True,
        memory_read_performed=delegated.get("memory_read_performed") is True if delegated else False,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        delegated_window_packet=delegated,
        scheduler_blockers=blockers,
        scheduler_warnings=warnings,
    )
