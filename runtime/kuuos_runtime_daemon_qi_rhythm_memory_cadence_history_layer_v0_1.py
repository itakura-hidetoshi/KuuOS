#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import pathlib
from typing import Any, Mapping, Sequence

try:
    from runtime.kuuos_runtime_daemon_qi_adaptive_window_scheduler_v0_1 import run_qi_adaptive_window_scheduler
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_adaptive_window_scheduler_v0_1 import run_qi_adaptive_window_scheduler


@dataclass(frozen=True)
class QiRhythmMemoryCadenceHistoryResult:
    rhythm_layer_version: str
    rhythm_layer_status: str
    rhythm_mode: str
    history_entry_count: int
    recent_pressure_mean: float
    recent_completion_ratio: float
    recent_observe_stop_ratio: float
    recent_full_history_stop_ratio: float
    recent_freeze_stop_ratio: float
    rhythm_stability_score: float
    recommended_max_window_ticks: int
    recommended_min_window_ticks: int
    rhythm_bias: str
    rhythm_history_projection_only: bool
    rhythm_entry_candidate: dict[str, Any]
    adaptive_context_packet: dict[str, Any]
    delegated_adaptive_status: str | None
    delegated_cadence_mode: str | None
    delegated_recommended_window_ticks: int
    delegated_completed_tick_count: int
    delegated_stop_reason: str | None
    event_log_path: str
    ledger_state_path: str
    delegates_only_to_adaptive_window_scheduler: bool
    rhythm_layer_grants_no_new_authority: bool
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
    delegated_adaptive_packet: dict[str, Any]
    rhythm_blockers: list[str]
    rhythm_warnings: list[str]
    authority: str = "rhythm_memory_cadence_history_projection_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _entries(value: Any) -> list[Mapping[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, Mapping)]
    if isinstance(value, Mapping) and isinstance(value.get("entries"), list):
        return [item for item in value.get("entries", []) if isinstance(item, Mapping)]
    if isinstance(value, Mapping):
        return [value]
    return []


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


def _mean(values: list[float], default: float = 0.0) -> float:
    return sum(values) / len(values) if values else default


def _ratio(entries: list[Mapping[str, Any]], predicate) -> float:
    return sum(1 for item in entries if predicate(item)) / len(entries) if entries else 0.0


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


def _stability(completion: float, observe: float, full_history: float, freeze: float, pressure: float) -> float:
    penalty = 0.25 * observe + 0.25 * full_history + 0.35 * freeze + 0.15 * min(max(pressure, 0.0), 1.0)
    return max(0.0, min(1.0, completion * (1.0 - penalty)))


def _rhythm_bias(stability: float, observe: float, full_history: float, freeze: float) -> str:
    if freeze >= 0.2:
        return "freeze_guarded"
    if observe >= 0.35:
        return "observe_sensitive"
    if full_history >= 0.25:
        return "full_history_sensitive"
    if stability >= 0.75:
        return "expand_if_low_pressure"
    if stability >= 0.45:
        return "hold_steady"
    return "contract_window"


def _window_bounds(bias: str, base_min: int, base_max: int) -> tuple[int, int, str]:
    if bias == "expand_if_low_pressure":
        return base_min, min(max(base_max, 4), 8), "stable_expansion"
    if bias == "hold_steady":
        return base_min, min(base_max, 4), "steady_guarded"
    if bias == "observe_sensitive":
        return 1, min(base_max, 2), "observation_guarded"
    if bias == "full_history_sensitive":
        return 1, min(base_max, 1), "full_history_guarded"
    if bias == "freeze_guarded":
        return 1, 1, "freeze_guarded"
    return 1, min(base_max, 2), "contracted_guarded"


def run_qi_rhythm_memory_cadence_history_layer(
    *,
    decisionos_packet: Mapping[str, Any],
    cbf_packet: Mapping[str, Any],
    token_ledger_packet: Mapping[str, Any],
    process_tensor_packet: Mapping[str, Any],
    memory_entries: Sequence[Mapping[str, Any]] | Mapping[str, Any],
    scheduler_state: Mapping[str, Any],
    scheduler_proposal: Mapping[str, Any],
    process_tensor_metrics: Mapping[str, Any],
    rhythm_history: Mapping[str, Any] | Sequence[Mapping[str, Any]],
    event_log_path: str | pathlib.Path,
    ledger_state_path: str | pathlib.Path,
    rhythm_context: Mapping[str, Any] | None = None,
) -> QiRhythmMemoryCadenceHistoryResult:
    ctx = _mapping(rhythm_context)
    blockers: list[str] = []
    warnings: list[str] = []
    if ctx.get("rhythm_memory_layer_enabled") is not True:
        blockers.append("rhythm_memory_layer_enabled_not_true")
    if ctx.get("read_only_rhythm_memory") is not True:
        blockers.append("read_only_rhythm_memory_not_true")
    if ctx.get("jsonl_backend_required") is not True:
        blockers.append("jsonl_backend_required_not_true")
    if ctx.get("request_probe_execution") is True:
        blockers.append("request_probe_execution")
    if ctx.get("request_memory_write") is True:
        blockers.append("request_memory_write")
    if ctx.get("request_memory_append") is True:
        blockers.append("request_memory_append")
    if ctx.get("request_world_update") is True:
        blockers.append("request_world_update")
    if ctx.get("request_control_packet_mutation") is True:
        blockers.append("request_control_packet_mutation")

    raw_entries = _entries(rhythm_history)
    history_limit = max(1, _int(ctx, "history_window_size", 8))
    entries = raw_entries[-history_limit:]
    pressures = [_float(item, "process_tensor_pressure_score", _float(item, "pressure_score", 0.0)) for item in entries]
    completion_values = []
    for item in entries:
        requested = max(1, _int(item, "recommended_window_ticks", _int(item, "requested_window_ticks", 1)))
        completed = _int(item, "delegated_completed_tick_count", _int(item, "completed_tick_count", 0))
        completion_values.append(min(1.0, max(0.0, completed / requested)))
    pressure_mean = _mean(pressures, 0.0)
    completion_ratio = _mean(completion_values, 1.0 if not entries else 0.0)
    observe_ratio = _ratio(entries, lambda item: str(item.get("delegated_stop_reason") or item.get("stop_reason")) == "process_tensor_observe_required")
    full_history_ratio = _ratio(entries, lambda item: str(item.get("delegated_stop_reason") or item.get("stop_reason")) in {"process_tensor_full_history_required", "process_tensor_full_history_after_tick"})
    freeze_ratio = _ratio(entries, lambda item: str(item.get("delegated_stop_reason") or item.get("stop_reason")) == "freeze_required")
    stability = _stability(completion_ratio, observe_ratio, full_history_ratio, freeze_ratio, pressure_mean)
    bias = _rhythm_bias(stability, observe_ratio, full_history_ratio, freeze_ratio)

    base_min = max(1, _int(ctx, "base_min_window_ticks", 1))
    base_max = max(base_min, _int(ctx, "base_max_window_ticks", 4))
    rec_min, rec_max, rhythm_mode = _window_bounds(bias, base_min, base_max)
    absolute_cap = max(1, _int(ctx, "absolute_max_window_ticks", 16))
    rec_max = min(rec_max, absolute_cap)
    rec_min = min(rec_min, rec_max)

    process_tensor_schedule = ctx.get("process_tensor_schedule") if isinstance(ctx.get("process_tensor_schedule"), list) else []
    adaptive_context = {
        "adaptive_window_scheduler_enabled": True,
        "read_only_adaptive_scheduler": True,
        "jsonl_backend_required": True,
        "min_window_ticks": rec_min,
        "max_window_ticks": rec_max,
        "absolute_max_window_ticks": absolute_cap,
        "current_tick": _int(ctx, "current_tick", _int(_mapping(token_ledger_packet), "current_tick", 0)),
        "tick_id_prefix": str(ctx.get("tick_id_prefix", "qi-rhythm")),
        "process_tensor_schedule": process_tensor_schedule,
        "memory_complexity_threshold": ctx.get("memory_complexity_threshold", _mapping(process_tensor_packet).get("memory_complexity_threshold", 1.0)),
        "recovery_epsilon": ctx.get("recovery_epsilon", _mapping(process_tensor_packet).get("recovery_epsilon", 0.1)),
    }

    delegated: dict[str, Any] = {}
    if not blockers:
        delegated = run_qi_adaptive_window_scheduler(
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
            adaptive_context=adaptive_context,
        ).to_dict()
        if delegated.get("adaptive_scheduler_status") != "QI_ADAPTIVE_WINDOW_SCHEDULER_COMPLETED":
            blockers.append("delegated_adaptive_scheduler_not_completed")
        _require_false("delegated_adaptive", delegated, blockers)

    entry_candidate = {
        "entry_kind": "rhythm_cadence_history_candidate",
        "projection_only": True,
        "rhythm_mode": rhythm_mode,
        "rhythm_bias": bias,
        "process_tensor_pressure_score": delegated.get("process_tensor_pressure_score", pressure_mean) if delegated else pressure_mean,
        "recommended_window_ticks": delegated.get("recommended_window_ticks", rec_max) if delegated else rec_max,
        "delegated_completed_tick_count": delegated.get("delegated_completed_tick_count", 0) if delegated else 0,
        "delegated_stop_reason": delegated.get("delegated_stop_reason") if delegated else None,
        "cadence_mode": delegated.get("cadence_mode") if delegated else None,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "world_update_performed": False,
    }

    ready = not blockers
    return QiRhythmMemoryCadenceHistoryResult(
        rhythm_layer_version="kuuos_runtime_daemon_qi_rhythm_memory_cadence_history_layer_v0_1",
        rhythm_layer_status="QI_RHYTHM_MEMORY_CADENCE_HISTORY_LAYER_COMPLETED" if ready else "QI_RHYTHM_MEMORY_CADENCE_HISTORY_LAYER_BLOCKED",
        rhythm_mode=rhythm_mode,
        history_entry_count=len(entries),
        recent_pressure_mean=pressure_mean,
        recent_completion_ratio=completion_ratio,
        recent_observe_stop_ratio=observe_ratio,
        recent_full_history_stop_ratio=full_history_ratio,
        recent_freeze_stop_ratio=freeze_ratio,
        rhythm_stability_score=stability,
        recommended_max_window_ticks=rec_max,
        recommended_min_window_ticks=rec_min,
        rhythm_bias=bias,
        rhythm_history_projection_only=True,
        rhythm_entry_candidate=entry_candidate,
        adaptive_context_packet=adaptive_context,
        delegated_adaptive_status=str(delegated.get("adaptive_scheduler_status")) if delegated.get("adaptive_scheduler_status") else None,
        delegated_cadence_mode=str(delegated.get("cadence_mode")) if delegated.get("cadence_mode") else None,
        delegated_recommended_window_ticks=int(delegated.get("recommended_window_ticks", 0)) if delegated else 0,
        delegated_completed_tick_count=int(delegated.get("delegated_completed_tick_count", 0)) if delegated else 0,
        delegated_stop_reason=str(delegated.get("delegated_stop_reason")) if delegated.get("delegated_stop_reason") else None,
        event_log_path=str(event_log_path),
        ledger_state_path=str(ledger_state_path),
        delegates_only_to_adaptive_window_scheduler=True,
        rhythm_layer_grants_no_new_authority=True,
        memory_read_performed=bool(entries) or delegated.get("memory_read_performed") is True,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        delegated_adaptive_packet=delegated,
        rhythm_blockers=blockers,
        rhythm_warnings=warnings,
    )
